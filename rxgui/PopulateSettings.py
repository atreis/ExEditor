# Helper for populating settings into the UI after opening a new file

def populateRecursive(fh, t, keys):
    def __newKeyList(keys, key):
        l = []
        for k in keys:
            l.append(k)
        l.append(key)
        return l

    def __makeInsertKey(keys):
        s = ''
        if len(keys) > 0:
            first = True
            for k in keys:
                if first:
                    first = False
                else:
                    s += '-'
                s += k
        return s

    levelkeys = fh.getKeys(keys)
    for key in levelkeys:
        newkeys = __newKeyList(keys, key)
        insertkey = __makeInsertKey(keys)
        nextlevelkeys = fh.getKeys(newkeys)
        if len(nextlevelkeys) > 0:
            t.insert(insertkey, 'end', __makeInsertKey(newkeys), text=key)
            populateRecursive(fh, t, newkeys)
        else:
            val = fh.getValue(newkeys)
            t.insert(insertkey, 'end', __makeInsertKey(newkeys), text=key, values=[str(val)])

def populateAdvancedTree(fh, t):
    populateRecursive(fh, t, [])

def clear(t):
    t.delete(*t.get_children())
