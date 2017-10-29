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
        l = []
        try:
            for k in self.__getData(keys).keys():
                l.append(k)
        except:
            pass
        return l

    def getValue(self, keys):
        return self.__getData(keys)

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
