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
    global label1
    global infolabel
    global valuestring
    global valuehex
    global valuebinary
    global valuetype
    global ignorestring
    global ignorehex
    global ignorebinary
    global isusersave
    global isstringhidden
    global isbinhidden
    label1 = StringVar()
    label1.set("String:")
    infolabel = StringVar()
    infolabel.set("Select value to edit")
    valuestring = StringVar()
    valuehex = StringVar()
    valuebinary = StringVar()
    valuetype = StringVar()
    ignorestring = BooleanVar(False)
    ignorehex = BooleanVar(False)
    ignorebinary = BooleanVar(False)
    isusersave = BooleanVar(False)
    isstringhidden = BooleanVar(False)
    isbinhidden = BooleanVar(False)

def _DialogAdvancedEdit__cancel():
    global isusersave
    isusersave.set(False)
    destroy_window()

def _DialogAdvancedEdit__save():
    global isusersave
    isusersave.set(True)
    destroy_window()

def validate(val, valtype):
    global infolabel

    if len(val)==0 or val=="-":
        infolabel.set('')
        return False
    elif valtype in ["int_8bit_signed","int_8bit_unsigned"]:
        try:
            valint = int(val)
            if valint > 255 or valint < -128:
                infolabel.set("ERROR: Value must be between -128 and 255 (8 bit binary)")
                return False
            else:
                infolabel.set('')
                return True
        except:
            infolabel.set("ERROR: Value must a number")
            return False
    elif valtype == "hex_8bit":
        try:
            print("val: "+val)
            valint = int(val,16)
            if valint > 255 or valint < -128:
                infolabel.set("ERROR: Value must be between -128 and 255 (8 bit binary)")
                return False
            else:
                infolabel.set('')
                return True
        except:
            infolabel.set("ERROR: Value must a number")
            return False
    infolabel.set('')
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
                        values[c1][c2] = int(valuestring.get())
                        break
                    c2 += 1
            elif item==str(c1):
                values[c1] = int(valuestring.get())
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
    global valuehex
    global valuebinary
    global valuetype
    global ignorestring
    global ignorehex
    global ignorebinary

    if valtype is not None:
        valuetype.set(valtype)
    else:
        valtype = valuetype.get()

    if validate(val, valtype):
        if valtype=="int_8bit_unsigned":
            label1.set("Integer:")
            valhex = '{0:02x}'.format(int(val))
            valbin = '{0:08b}'.format(int(val))
            if valuehex.get()!=valhex:
                ignorehex.set(True)
                valuehex.set(valhex)
            if valuebinary.get()!=valbin:
                ignorebinary.set(True)
                valuebinary.set(valbin)
        elif valtype == "hex_8bit":
            label1.set("Hex:")
            valhex = '{0:02x}'.format(int(val, 16))
            valbin = '{0:08b}'.format(int(val, 16))
            if valuehex.get() != valhex:
                ignorehex.set(True)
                valuehex.set(valhex)
            if valuebinary.get() != valbin:
                ignorebinary.set(True)
                valuebinary.set(valbin)
        elif valtype=="int_8bit_signed":
            label1.set("Integer:")
            vali = int(val)
            if vali > 127:
                vali -= 256
            valhex = '{0:02x}'.format(int(vali))
            valbin = '{0:08b}'.format(int(vali))
            if valuehex.get()!=valhex:
                ignorehex.set(True)
                valuehex.set(valhex)
            if valuebinary.get()!=valbin:
                ignorebinary.set(True)
                valuebinary.set(valbin)
        elif valtype=="string":
            label1.set("String:")
            if valuehex.get()!='':
                ignorehex.set(True)
                valuehex.set('')
            if valuebinary.get()!='':
                ignorebinary.set(True)
                valuebinary.set('')

        updateValues()

def showHide(widgets):
    global valuetype
    global isstringhidden
    global isbinhidden

    if valuetype.get()=="string" and not isbinhidden.get():
        top = widgets["top"]
        for widget in widgets["hex"]:
            widget.lower(top)
        for widget in widgets["binary"]:
            widget.lower(top)
        isbinhidden.set(True)
    elif valuetype.get() in ["int_8bit_unsigned","int_8bit_signed"] and isbinhidden.get():
        top = widgets["top"]
        for widget in widgets["hex"]:
            widget.lift(top)
        for widget in widgets["binary"]:
            widget.lift(top)
        isbinhidden.set(False)
    elif valuetype.get() == "hex_8bit" and isbinhidden.get():
        top = widgets["top"]
        for widget in widgets["hex"]:
            widget.lift(top)
        for widget in widgets["binary"]:
            widget.lift(top)
        isbinhidden.set(False)

    if valuetype.get()=="string" and isstringhidden.get():
        top = widgets["top"]
        for widget in widgets["string"]:
            widget.lift(top)
        isstringhidden.set(False)
    elif valuetype.get() in ["int_8bit_unsigned","int_8bit_signed"] and isstringhidden.get():
        top = widgets["top"]
        for widget in widgets["string"]:
            widget.lift(top)
        isstringhidden.set(False)
    elif valuetype.get() == "hex_8bit" and not isstringhidden.get():
        top = widgets["top"]
        for widget in widgets["string"]:
            widget.lower(top)
        isstringhidden.set(True)

def valueStringChange():
    global valuestring
    global ignorestring
    if ignorestring.get():
        ignorestring.set(False)
    else:
        populateValue(valuestring.get())

def valueHexChange():
    global infolabel
    infolabel.set("")

def _DialogAdvancedEdit__applyHex():
    global valuehex
    global valuestring
    global valuetype
    global infolabel

    # Validate the value
    if valuetype.get() in ["int_8bit_signed","int_8bit_unsigned","hex_8bit"]:
        try:
            valint = int(valuehex.get(), 16)
            if valint > 255 or valint < 0:
                infolabel.set("ERROR: Value must be between 0 and 255 (FF)")
            else:
                if valuetype.get() == "hex_8bit":
                    valuestring.set('0x'+('{0:02x}'.format(valint).upper()))
                else:
                    valuestring.set(str(valint))
        except:
            infolabel.set("ERROR: Value must be a hexadecimal number")

def valueBinaryChange():
    global infolabel
    infolabel.set("")

def _DialogAdvancedEdit__applyBinary():
    global valuebinary
    global valuestring
    global infolabel
    global valuetype

    # Validate the value
    if valuetype.get() in ["int_8bit_signed","int_8bit_unsigned","hex_8bit"]:
        try:
            valint = int(valuebinary.get(), 2)
            if valint > 255 or valint < 0:
                infolabel.set("ERROR: Value must be between 0 and 255 (8 bit binary)")
            else:
                valuestring.set(str(valint))
        except:
            infolabel.set("ERROR: Value must be a binary number")

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
