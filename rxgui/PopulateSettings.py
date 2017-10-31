# Helper for populating settings into the UI after opening a new file

def populateRecursive(fh, t, keys, s):
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

    levelkeys = fh.getKeys(keys, s)
    for key in levelkeys:
        newkeys = __newKeyList(keys, key)
        insertkey = __makeInsertKey(keys)
        nextlevelkeys = fh.getKeys(newkeys, s)
        if len(nextlevelkeys) > 0:
            t.insert(insertkey, 'end', __makeInsertKey(newkeys), text=key)
            populateRecursive(fh, t, newkeys, s)
        else:
            val = fh.getValue(newkeys, s)
            if val is not None:
                t.insert(insertkey, 'end', __makeInsertKey(newkeys), text=key, values=[str(val)])

def populateAdvancedTree(fh, t):
    populateAdvancedTreeFiltered(fh, t, None)

def populateAdvancedTreeFiltered(fh, t, s):
    populateRecursive(fh, t, [], s)

def clear(t):
    t.delete(*t.get_children())
