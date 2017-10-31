from rxfile import RxFile

# Basic file operations.
class RxFileWrapper:
    def __getData(self, keys):
        hold = self.rxfile.getData()
        for inputkey in keys:
            hold = hold[inputkey]
        return hold

    def __setData(self, keys, value):
        hold = self.rxfile.getData()
        c = 1
        for inputkey in keys:
            if len(keys) == c:
                hold[inputkey] = value
            else:
                hold = hold[inputkey]
            c += 1

    def getKeys(self, keys):
        return self.getKeys(keys, None)

    # Recursively check all child keys to see if they contain the filter string
    def __checkKeys(self, keys, s):
        try:
            childkeys = self.__getData(keys).keys()
            print("Child keys: "+str(childkeys))
            for k in childkeys:
                if s in k.lower():
                    return True

            for k in childkeys:
                newkeys = []
                for k1 in keys:
                    newkeys.append(k1)
                newkeys.append(k)
                if self.__checkKeys(newkeys, s):
                    return True
        except:
            pass
        return False

    def getKeys(self, keys, s):
        l = []
        returnThis = False
        if s is None:
            returnThis = True
        else:
            for key in keys:
                if s in key.lower():
                    returnThis = True
                    break

            if not returnThis:
                # Check child keys recursively to see if any of them contain the filter string
                print("Checking children for keys: "+str(keys)+" and s: "+str(s))
                returnThis = self.__checkKeys(keys, s)
                print("children: "+str(returnThis))

        # Return all keys
        try:
            for k in self.__getData(keys).keys():
                if returnThis:
                    # Return all keys
                    l.append(k)
                elif s in k.lower():
                    l.append(k)
        except:
            pass

        return l

    def getValue(self, keys):
        return self.getValue(keys, None)

    def getValue(self, keys, s):
        returnThis = False
        if s is None:
            returnThis = True
        else:
            for key in keys:
                if s in key.lower():
                    returnThis = True
                    break

        if returnThis:
            return self.__getData(keys)
        else:
            return None

    def setValue(self, keys, value):
        self.__setData(keys, value)
        self.dirty = True

    def save(self):
        if self.dirty:
            self.rxfile.save()
            self.dirty = False

    def saveAs(self, filename):
        self.rxfile.saveAs(filename)
        self.dirty = False

    def isDirty(self):
        return self.dirty

    def __init__(self, filename):
        self.rxfile = RxFile.RxFile(filename)
        self.rxfile.load()
        self.dirty = False
