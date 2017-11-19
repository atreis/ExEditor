import traceback
from page import ScrolledTreeView

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

class Dialog_AdvancedEdit:
    def __treeSelection(self, event):
        self.__tree_selection(event)
        self.__showHide({"top":self.frame,"string":[self.TLabel1,self.Entry1],"hex":[self.TLabel3,self.Entry3,self.TButton3],"binary":[self.TLabel4,self.Entry4,self.TButton4]})

    def __cancel(self):
        self.isusersave.set(False)
        self.__destroy_window()

    def __save(self):
        self.isusersave.set(True)
        self.__destroy_window()

    def __validate(self, val, valtype):
        if len(val) == 0 or val == "-":
            self.infolabeltext.set('')
            return False
        elif valtype in ["int_8bit_signed", "int_8bit_unsigned"]:
            try:
                valint = int(val)
                if valint > 255 or valint < -128:
                    self.infolabeltext.set("ERROR: Value must be between -128 and 255 (8 bit binary)")
                    return False
                else:
                    self.infolabeltext.set('')
                    return True
            except:
                self.infolabeltext.set("ERROR: Value must be a number")
                return False
        elif valtype in ["int_16bit_signed"]:
            try:
                valint = int(val)
                if valint > 32767 or valint < -32768:
                    self.infolabeltext.set("ERROR: Value must be between -32768 and 32767 (16 bit binary)")
                    return False
                else:
                    self.infolabeltext.set('')
                    return True
            except:
                self.infolabeltext.set("ERROR: Value must be a number")
                return False
        elif valtype == "hex_8bit":
            try:
                valint = int(val, 16)
                if valint > 255 or valint < -128:
                    self.infolabeltext.set("ERROR: Value must be between -128 and 255 (8 bit binary)")
                    return False
                else:
                    self.infolabeltext.set('')
                    return True
            except:
                self.infolabeltext.set("ERROR: Value must be a number")
                return False
        self.infolabeltext.set('')
        return True

    def getValues(self):
        if self.isusersave.get():
            # print('values: '+str(self.values))
            return self.values
        return None

    def __updateValues(self):
        item = self.Scrolledtreeview1.selection()[0]

        if isinstance(self.values, str):
            # print('values is str: '+str(self.values))
            self.values = self.valuestring.get()
        elif isinstance(self.values, list):
            # print('values is list: '+str(self.values))
            c1 = 0
            for v1 in self.values:
                if isinstance(v1, list):
                    c2 = 0
                    for v2 in v1:
                        if item == (str(c1) + '-' + str(c2)):
                            self.values[c1][c2] = int(self.valuestring.get())
                            break
                        c2 += 1
                elif item == str(c1):
                    self.values[c1] = int(self.valuestring.get())
                    break
                c1 += 1
        else:
            # print('values is other: '+str(self.values))
            self.values = int(self.valuestring.get())

        # Populate into list
        valuess = self.Scrolledtreeview1.item(item)["values"]
        valuess[1] = self.valuestring.get()
        self.Scrolledtreeview1.item(item, text=item, values=valuess)

    def __populateValue(self, val, valtype=None):
        if valtype is not None:
            self.valuetype.set(valtype)
        else:
            valtype = self.valuetype.get()

        if self.__validate(val, valtype):
            if valtype == "int_8bit_unsigned":
                self.label1.set("Integer:")
                valhex = '{0:02x}'.format(int(val))
                valbin = '{0:08b}'.format(int(val))
                if self.valuehex.get() != valhex:
                    self.ignorehex.set(True)
                    self.valuehex.set(valhex)
                if self.valuebinary.get() != valbin:
                    self.ignorebinary.set(True)
                    self.valuebinary.set(valbin)
            elif valtype == "hex_8bit":
                self.label1.set("Hex:")
                valhex = '{0:02x}'.format(int(val, 16))
                valbin = '{0:08b}'.format(int(val, 16))
                if self.valuehex.get() != valhex:
                    self.ignorehex.set(True)
                    self.valuehex.set(valhex)
                if self.valuebinary.get() != valbin:
                    self.ignorebinary.set(True)
                    self.valuebinary.set(valbin)
            elif valtype == "int_8bit_signed":
                self.label1.set("Integer:")
                vali = int(val)
                if vali > 127:
                    vali -= 256
                valhex = '{0:02x}'.format(int(vali))
                valbin = '{0:08b}'.format(int(vali))
                if self.valuehex.get() != valhex:
                    self.ignorehex.set(True)
                    self.valuehex.set(valhex)
                if self.valuebinary.get() != valbin:
                    self.ignorebinary.set(True)
                    self.valuebinary.set(valbin)
            elif valtype == "int_16bit_signed":
                self.label1.set("Integer:")
                if self.valuehex.get() != '':
                    self.ignorehex.set(True)
                    self.valuehex.set('')
                if self.valuebinary.get() != '':
                    self.ignorebinary.set(True)
                    self.valuebinary.set('')
            elif valtype == "string":
                self.label1.set("String:")
                if self.valuehex.get() != '':
                    self.ignorehex.set(True)
                    self.valuehex.set('')
                if self.valuebinary.get() != '':
                    self.ignorebinary.set(True)
                    self.valuebinary.set('')

            self.__updateValues()

    def __showHide(self, widgets):
        if self.valuetype.get() in ["string", "int_16bit_signed"] and not self.isbinhidden.get():
            top = widgets["top"]
            for widget in widgets["hex"]:
                widget.lower(top)
            for widget in widgets["binary"]:
                widget.lower(top)
            self.isbinhidden.set(True)
        elif self.valuetype.get() in ["int_8bit_unsigned", "int_8bit_signed"] and self.isbinhidden.get():
            top = widgets["top"]
            for widget in widgets["hex"]:
                widget.lift(top)
            for widget in widgets["binary"]:
                widget.lift(top)
            self.isbinhidden.set(False)
        elif self.valuetype.get() == "hex_8bit" and self.isbinhidden.get():
            top = widgets["top"]
            for widget in widgets["hex"]:
                widget.lift(top)
            for widget in widgets["binary"]:
                widget.lift(top)
            self.isbinhidden.set(False)

        if self.valuetype.get() in ["string", "int_16bit_signed"] and self.isstringhidden.get():
            top = widgets["top"]
            for widget in widgets["string"]:
                widget.lift(top)
            self.isstringhidden.set(False)
        elif self.valuetype.get() in ["int_8bit_unsigned", "int_8bit_signed"] and self.isstringhidden.get():
            top = widgets["top"]
            for widget in widgets["string"]:
                widget.lift(top)
            self.isstringhidden.set(False)
        elif self.valuetype.get() == "hex_8bit" and not self.isstringhidden.get():
            top = widgets["top"]
            for widget in widgets["string"]:
                widget.lower(top)
            self.isstringhidden.set(True)

    def __valueStringChange(self):
        if self.ignorestring.get():
            self.ignorestring.set(False)
        else:
            self.__populateValue(self.valuestring.get())

    def __valueHexChange(self):
        self.infolabeltext.set("")

    def __applyHex(self):
        # Validate the value
        if self.valuetype.get() in ["int_8bit_signed", "int_8bit_unsigned", "hex_8bit"]:
            try:
                valint = int(self.valuehex.get(), 16)
                if valint > 255 or valint < 0:
                    self.infolabeltext.set("ERROR: Value must be between 0 and 255 (FF)")
                else:
                    if self.valuetype.get() == "hex_8bit":
                        self.valuestring.set('0x' + ('{0:02x}'.format(valint).upper()))
                    else:
                        self.valuestring.set(str(valint))
            except:
                self.infolabeltext.set("ERROR: Value must be a hexadecimal number")

    def __valueBinaryChange(self):
        self.infolabeltext.set("")

    def __applyBinary(self):
        # Validate the value
        if self.valuetype.get() in ["int_8bit_signed", "int_8bit_unsigned", "hex_8bit"]:
            try:
                valint = int(self.valuebinary.get(), 2)
                if valint > 255 or valint < 0:
                    self.infolabeltext.set("ERROR: Value must be between 0 and 255 (8 bit binary)")
                else:
                    self.valuestring.set(str(valint))
            except:
                self.infolabeltext.set("ERROR: Value must be a binary number")

    def __populateList(self):
        t = self.Scrolledtreeview1

        # Try to figure out what the value is
        if isinstance(self.values, str):
            # print('values is str: '+str(self.values))
            if self.values.startswith("0x") and len(self.values) <= 4:
                # print('str is hex')
                self.valuetype.set('hex_8bit')
            else:
                # print('str is string')
                self.valuetype.set('string')
            t.insert('', 'end', '0', text='0', values=[self.values, self.values])
        elif isinstance(self.values, list):
            # print('values is list: '+str(self.values))
            if 'attTrim' in self.item or 'axisTrim' in self.item:
                self.valuetype.set('int_16bit_signed')
            else:
                self.valuetype.set('int_8bit_unsigned')
            c1 = 0
            for v1 in self.values:
                if isinstance(v1, list):
                    c2 = 0
                    for v2 in v1:
                        t.insert('', 'end', str(c1) + '-' + str(c2), text=str(c1) + '-' + str(c2),
                                 values=[str(v2), str(v2)])
                        c2 += 1
                else:
                    t.insert('', 'end', str(c1), text=str(c1), values=[str(v1), str(v1)])
                c1 += 1
        else:
            # print('str is int')
            self.valuetype.set('int_8bit_unsigned')
            t.insert('', 'end', '0', text='0', values=[str(self.values), str(self.values)])

    def __tree_selection(self, event):
        item = self.Scrolledtreeview1.selection()[0]
        # print('item: '+str(item))
        vals = self.Scrolledtreeview1.item(item)["values"]

        self.valuestring.set(vals[1])

    def draw(self):
        self.top.geometry("700x400+150+150")
        self.top.title("RxEditor - "+self.item)
        self.top.configure(background="#d9d9d9")
        self.top.configure(highlightbackground="#d9d9d9")
        self.top.configure(highlightcolor="black")

        self.frame = Frame(self.top)
        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.configure(background="#d9d9d9")
        self.frame.configure(highlightbackground="#d9d9d9")
        self.frame.configure(highlightcolor="black")

        self.style.configure('Treeview.Heading',  font="TkDefaultFont")
        self.Scrolledtreeview1 = ScrolledTreeView.ScrolledTreeView(self.top)
        self.Scrolledtreeview1.place(relx=0.0, rely=0.0, relheight=0.4, relwidth=1.0)
        self.Scrolledtreeview1.configure(columns="Col1 Col2")
        self.Scrolledtreeview1.configure(selectmode=BROWSE)
        self.Scrolledtreeview1.heading("#0",text="Position")
        self.Scrolledtreeview1.heading("#0",anchor="center")
        self.Scrolledtreeview1.column("#0",width="50")
        self.Scrolledtreeview1.column("#0",minwidth="20")
        self.Scrolledtreeview1.column("#0",stretch="1")
        self.Scrolledtreeview1.column("#0",anchor="w")
        self.Scrolledtreeview1.heading("Col1",text="Old Value")
        self.Scrolledtreeview1.heading("Col1",anchor="center")
        self.Scrolledtreeview1.column("Col1",width="261")
        self.Scrolledtreeview1.column("Col1",minwidth="20")
        self.Scrolledtreeview1.column("Col1",stretch="1")
        self.Scrolledtreeview1.column("Col1",anchor="w")
        self.Scrolledtreeview1.heading("Col2",text="New Value")
        self.Scrolledtreeview1.heading("Col2",anchor="center")
        self.Scrolledtreeview1.column("Col2",width="261")
        self.Scrolledtreeview1.column("Col2",minwidth="20")
        self.Scrolledtreeview1.column("Col2",stretch="1")
        self.Scrolledtreeview1.column("Col2",anchor="w")

        self.TButton1 = ttk.Button(self.top)
        self.TButton1.place(relx=0.2, rely=0.9, height=35, width=120)
        self.TButton1.configure(command=self.__save)
        self.TButton1.configure(takefocus="")
        self.TButton1.configure(text='''Save''')

        self.TButton2 = ttk.Button(self.top)
        self.TButton2.place(relx=0.6, rely=0.9, height=35, width=120)
        self.TButton2.configure(command=self.__cancel)
        self.TButton2.configure(takefocus="")
        self.TButton2.configure(text='''Cancel''')

        self.TLabel1 = ttk.Label(self.top)
        self.TLabel1.place(relx=0.01, rely=0.45, height=29, width=65)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(relief=FLAT)
        self.TLabel1.configure(textvariable=self.label1)
        self.TLabel1.configure(anchor=E)

        self.TLabel3 = ttk.Label(self.top)
        self.TLabel3.place(relx=0.01, rely=0.55, height=29, width=65)
        self.TLabel3.configure(background="#d9d9d9")
        self.TLabel3.configure(foreground="#000000")
        self.TLabel3.configure(relief=FLAT)
        self.TLabel3.configure(text='''Hex:''')
        self.TLabel3.configure(anchor=E)

        self.TLabel4 = ttk.Label(self.top)
        self.TLabel4.place(relx=0.01, rely=0.65, height=29, width=65)
        self.TLabel4.configure(background="#d9d9d9")
        self.TLabel4.configure(foreground="#000000")
        self.TLabel4.configure(relief=FLAT)
        self.TLabel4.configure(text='''Binary:''')
        self.TLabel4.configure(anchor=E)

        self.infolabel = ttk.Label(self.top)
        self.infolabel.place(relx=0.01, rely=0.75, height=29, relwidth=.98)
        self.infolabel.configure(background="#d9d9d9")
        self.infolabel.configure(foreground="#ee3333")
        self.infolabel.configure(relief=SUNKEN)
        self.infolabel.configure(textvariable=self.infolabeltext)
        self.infolabel.configure(anchor=W)

        self.Entry1 = Entry(self.top)
        self.Entry1.place(relx=0.13, rely=0.45, relheight=0.06, relwidth=0.85)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")
        valuestring = self.valuestring
        self.Entry1.configure(textvariable=valuestring)
        valuestring.trace("w", lambda name, index, mode, valuestring=valuestring: self.__valueStringChange())

        self.Entry3 = Entry(self.top)
        self.Entry3.place(relx=0.13, rely=0.55, relheight=0.06, relwidth=0.73)
        self.Entry3.configure(background="white")
        self.Entry3.configure(disabledforeground="#a3a3a3")
        self.Entry3.configure(font="TkFixedFont")
        self.Entry3.configure(foreground="#000000")
        self.Entry3.configure(highlightbackground="#d9d9d9")
        self.Entry3.configure(highlightcolor="black")
        self.Entry3.configure(insertbackground="black")
        self.Entry3.configure(selectbackground="#c4c4c4")
        self.Entry3.configure(selectforeground="black")
        valuehex = self.valuehex
        self.Entry3.configure(textvariable=valuehex)
        valuehex.trace("w", lambda name, index, mode, valuehex=valuehex: self.__valueHexChange())

        self.TButton3 = ttk.Button(self.top)
        self.TButton3.place(relx=0.87, rely=0.55, height=29, width=80)
        self.TButton3.configure(command=self.__applyHex)
        self.TButton3.configure(takefocus="")
        self.TButton3.configure(text='''Apply''')

        self.Entry4 = Entry(self.top)
        self.Entry4.place(relx=0.13, rely=0.65, relheight=0.06, relwidth=0.73)
        self.Entry4.configure(background="white")
        self.Entry4.configure(disabledforeground="#a3a3a3")
        self.Entry4.configure(font="TkFixedFont")
        self.Entry4.configure(foreground="#000000")
        self.Entry4.configure(highlightbackground="#d9d9d9")
        self.Entry4.configure(highlightcolor="black")
        self.Entry4.configure(insertbackground="black")
        self.Entry4.configure(selectbackground="#c4c4c4")
        self.Entry4.configure(selectforeground="black")
        valuebinary = self.valuebinary
        self.Entry4.configure(textvariable=valuebinary)
        valuebinary.trace("w", lambda name, index, mode, valuebinary=valuebinary: self.__valueBinaryChange())

        self.TButton4 = ttk.Button(self.top)
        self.TButton4.place(relx=0.87, rely=0.65, height=29, width=80)
        self.TButton4.configure(command=self.__applyBinary)
        self.TButton4.configure(takefocus="")
        self.TButton4.configure(text='''Apply''')

        self.Scrolledtreeview1.bind('<ButtonRelease-1>', self.__treeSelection)

        self.__populateList()

    def __destroy_window(self):
        # Function which closes the window.
        self.top.destroy()
        self.top = None

    def __init__(self, top, style, item, fh, keys, values):
        self.top = top
        self.style = style
        self.item = item
        self.fh = fh
        self.keys = keys
        self.values = values
        # print('keys: '+str(keys)+' values: '+str(values))
        self.label1 = StringVar()
        self.label1.set("String:")
        self.infolabeltext = StringVar()
        self.infolabeltext.set("Select value to edit")
        self.valuestring = StringVar()
        self.valuehex = StringVar()
        self.valuebinary = StringVar()
        self.valuetype = StringVar()
        self.ignorestring = BooleanVar(False)
        self.ignorehex = BooleanVar(False)
        self.ignorebinary = BooleanVar(False)
        self.isusersave = BooleanVar(False)
        self.isstringhidden = BooleanVar(False)
        self.isbinhidden = BooleanVar(False)
