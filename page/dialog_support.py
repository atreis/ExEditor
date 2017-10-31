import json
import traceback
import rxgui
import rxfile

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

def set_Tk_var():
    global valuestring
    valuestring = StringVar()
    global valueint
    valueint = StringVar()
    global valuehex
    valuehex = StringVar()
    global valuebinary
    valuebinary = StringVar()
    global valuetype
    valuetype = StringVar()
    global ignorestring
    ignorestring = BooleanVar(False)
    global ignoreint
    ignoreint = BooleanVar(False)
    global ignorehex
    ignorehex = BooleanVar(False)
    global ignorebinary
    ignorebinary = BooleanVar(False)
    global isusersave
    isusersave = BooleanVar(False)

def _DialogAdvancedEdit__cancel():
    global isusersave
    isusersave.set(False)
    destroy_window()

def _DialogAdvancedEdit__save():
    global isusersave
    isusersave.set(True)
    destroy_window()

def validate(val, valtype):
    if len(val)==0:
        return False
    return True

def getValues():
    global values
    global isusersave

    if isusersave.get():
        return values
    return None

def updateValues():
    global valuestring
    global w
    global values

    item = w.getTree().selection()[0]

    if isinstance(values,str):
        values = valuestring.get()
    elif isinstance(values, list):
        c1 = 0
        for v1 in values:
            if isinstance(v1,list):
                c2 = 0
                for v2 in v1:
                    if item==(str(c1)+'-'+str(c2)):
                        v2 = int(valuestring.get())
                        break
                    c2 += 1
            elif item==str(c1):
                v1 = int(valuestring.get())
                break
            c1 += 1
    else:
        values = int(valuestring.get())

    # Populate into list
    valuess = w.getTree().item(item)["values"]
    valuess[1] = valuestring.get()
    w.getTree().item(item, text=item, values=valuess)



def populateValue(val, valtype=None):
    global valuestring
    global valueint
    global valuehex
    global valuebinary
    global valuetype
    global ignorestring
    global ignoreint
    global ignorehex
    global ignorebinary

    if valtype is not None:
        valuetype.set(valtype)
    else:
        valtype = valuetype.get()

    if validate(val, valtype):
        if valtype=="int_8bit_unsigned":
            valint = str(int(val))
            valhex = '{0:02x}'.format(int(val))
            valbin = '{0:08b}'.format(int(val))
            if valueint.get()!=valint:
                ignoreint.set(True)
                valueint.set(valint)
            if valuehex.get()!=valhex:
                ignorehex.set(True)
                valuehex.set(valhex)
            if valuebinary.get()!=valbin:
                ignorebinary.set(True)
                valuebinary.set(valbin)
        elif valtype == "hex_8bit":
            valint = str(int(val, 16))
            valhex = '{0:02x}'.format(int(val, 16))
            valbin = '{0:08b}'.format(int(val, 16))
            if valueint.get() != valint:
                ignoreint.set(True)
                valueint.set(valint)
            if valuehex.get() != valhex:
                ignorehex.set(True)
                valuehex.set(valhex)
            if valuebinary.get() != valbin:
                ignorebinary.set(True)
                valuebinary.set(valbin)
        elif valtype=="int_8bit_signed":
            vali = int(val)
            if vali > 127:
                vali -= 256
            valint = str(int(vali))
            valhex = '{0:02x}'.format(int(vali))
            valbin = '{0:08b}'.format(int(vali))
            if valueint.get()!=valint:
                ignoreint.set(True)
                valueint.set(valint)
            if valuehex.get()!=valhex:
                ignorehex.set(True)
                valuehex.set(valhex)
            if valuebinary.get()!=valbin:
                ignorebinary.set(True)
                valuebinary.set(valbin)
        elif valtype=="string":
            if valueint.get()!='':
                ignoreint.set(True)
                valueint.set('')
            if valuehex.get()!='':
                ignorehex.set(True)
                valuehex.set('')
            if valuebinary.get()!='':
                ignorebinary.set(True)
                valuebinary.set('')

        updateValues()

def valueStringChange():
    global valuestring
    global ignorestring
    if ignorestring.get():
        ignorestring.set(False)
    else:
        populateValue(valuestring.get())

def valueIntChange():
    global valueint
    global valuestring
    global ignoreint
    if ignoreint.get():
        ignoreint.set(False)
    elif valueint.get()!='':
        valuestring.set(valueint.get())

def valueHexChange():
    pass

def _DialogAdvancedEdit__applyHex():
    global valuehex
    global valuestring
#    global ignorehex
#    if ignorehex.get():
#        ignorehex.set(False)
#    elif valuehex.get()!='':
    valuestring.set(str(int(valuehex.get(), 16)))

def valueBinaryChange():
    pass

def _DialogAdvancedEdit__applyBinary():
    global valuebinary
    global valuestring
#    global ignorebinary
#    if ignorebinary.get():
#        ignorebinary.set(False)
#    elif valuebinary.get()!='':
    valuestring.set(str(int(valuebinary.get(), 2)))

def populateList():
    global w
    global values
    global valuetype
    t = w.getTree()

    # Try to figure out what the value is
    if isinstance(values,str):
        if values.startswith("0x") and len(values)<=4:
            valuetype.set('hex_8bit')
        else:
            valuetype.set('string')
        t.insert('', 'end', '0', text='0', values=[values, values])
    elif isinstance(values, list):
        valuetype.set('int_8bit_unsigned')
        c1 = 0
        for v1 in values:
            if isinstance(v1,list):
                c2 = 0
                for v2 in v1:
                    t.insert('', 'end', str(c1)+'-'+str(c2), text=str(c1)+'-'+str(c2), values=[str(v2), str(v2)])
                    c2 += 1
            else:
                t.insert('', 'end', str(c1), text=str(c1), values=[str(v1), str(v1)])
            c1 += 1
    else:
        valuetype.set('int_8bit_unsigned')
        t.insert('', 'end', '0', text='0', values=[str(values), str(values)])

def tree_selection(event):
    global w
    global valuestring
    item = w.getTree().selection()[0]
    values = w.getTree().item(item)["values"]

    valuestring.set(values[1])

def init(top, gui, fhin, keysin, valuesin):
    global w, top_level, root, fh, keys, values
    w = gui
    top_level = top
    root = top
    fh = fhin
    keys = keysin
    values = valuesin
    populateList()

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None
