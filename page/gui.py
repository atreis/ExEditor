#! /usr/bin/env python
#
# GUI module generated by PAGE version 4.9
# In conjunction with Tcl version 8.6
#    Oct 28, 2017 12:01:46 PM
import sys

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

from page import gui_support
from page import dialog_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    gui_support.set_Tk_var()
    top = RxEditor (root)
    gui_support.init(root, top)
    root.mainloop()

w = None
def create_RxEditor(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    gui_support.set_Tk_var()
    top = RxEditor (w)
    gui_support.init(w, top, *args, **kwargs)
    return (w, top)

advancedEdit = None
def create_DialogAdvancedEdit(parent, item, keys, values, fh):
    global advancedEdit, ae_win, ae_rt, root
    ae_rt = parent
    advancedEdit = Toplevel(parent)
    dialog_support.set_Tk_var()
    ae_top = DialogAdvancedEdit(advancedEdit, item)
    dialog_support.init(advancedEdit, ae_top, fh, keys, values)
    root.wait_window(advancedEdit)
    return dialog_support.getValues()

def destroy_RxEditor():
    global w
    w.destroy()
    w = None


class RxEditor:
    def getAdvancedTree(self):
        return self.advancedtree

    def getTop(self):
        return self.top

    def __doubleClickAdvancedTree(self, event):
        item, keys, value, fh = gui_support.tree_doubleclick(event)
        newvalues = create_DialogAdvancedEdit(self.top, item, keys, value, fh)
        if newvalues is not None:
            gui_support.tree_updatevalues(item, keys, newvalues, fh)

    def __init__(self, top=None):
        self.top = top
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("1000x700+100+100")
        top.title("RxEditor (v0.8.4)")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#e9e9e9")
        top.configure(highlightcolor="#191919")

        self.menubar = Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.file = Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.file,
                activebackground="#d9d9d9",
                activeforeground="#000000",
                accelerator="f",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="File")
        self.file.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                accelerator="o",
                background="#d9d9d9",
                command=gui_support.menu_open,
                font="TkMenuFont",
                foreground="#000000",
                label="Open...")
        self.file.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                accelerator="s",
                background="#d9d9d9",
                command=gui_support.menu_save,
                font="TkMenuFont",
                foreground="#000000",
                label="Save")
        self.file.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                accelerator="a",
                background="#d9d9d9",
                command=gui_support.menu_saveAs,
                font="TkMenuFont",
                foreground="#000000",
                label="SaveAs...")
        self.file.add_separator(
                background="#d9d9d9")
        self.file.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                accelerator="x",
                background="#d9d9d9",
                command=gui_support.menu_exit,
                font="TkMenuFont",
                foreground="#000000",
                label="Exit")
        # self.view = Menu(top,tearoff=0)
        # self.menubar.add_cascade(menu=self.view,
        #         activebackground="#d9d9d9",
        #         activeforeground="#000000",
        #         accelerator="v",
        #         background="#d9d9d9",
        #         font="TkMenuFont",
        #         foreground="#000000",
        #         label="View")
        # self.view.add_command(
        #         activebackground="#d8d8d8",
        #         activeforeground="#000000",
        #         accelerator="b",
        #         background="#d9d9d9",
        #         command=gui_support.TODO,
        #         font="TkMenuFont",
        #         foreground="#000000",
        #         label="Basic View")
        # self.view.add_command(
        #         activebackground="#d8d8d8",
        #         activeforeground="#000000",
        #         accelerator="d",
        #         background="#d9d9d9",
        #         command=gui_support.TODO,
        #         font="TkMenuFont",
        #         foreground="#000000",
        #         label="Advanced View")


        self.style.configure('TNotebook.Tab', background=_bgcolor)
        self.style.configure('TNotebook.Tab', foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=
            [('selected', _compcolor), ('active',_ana2color)])
        self.notebook = ttk.Notebook(top)
        self.notebook.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.notebook.configure(width=300)
        self.notebook.configure(takefocus="")
        self.notebook_basic = ttk.Frame(self.notebook)
        self.notebook.add(self.notebook_basic, padding=3)
        self.notebook.tab(0, text="Safe",underline="-1",)
        self.notebook_t2 = ttk.Frame(self.notebook)
        self.notebook.add(self.notebook_t2, padding=3)
        self.notebook.tab(1, text="Mixes",underline="-1",)
        self.notebook_t2 = ttk.Frame(self.notebook)
        self.notebook.add(self.notebook_t2, padding=3)
        self.notebook.tab(2, text="Advanced",underline="-1",)

        # -----------------------------------------------------------------------------------
        # SAFE Tab

        self.safe = ttk.Labelframe(self.notebook_basic)
        self.safe.place(x=5, y=5, height=65, width=65)
        self.safe.configure(relief=SUNKEN)
        self.safe.configure(text='''SAFE®''')
        self.safe.configure(borderwidth="2")
        self.safe.configure(relief=SUNKEN)

        safemode = gui_support.safemode

        self.style.map('TRadiobutton',background=[('selected', _bgcolor), ('active',_bgcolor)])
        self.safeOn = ttk.Radiobutton(self.safe, text='On', variable=safemode, value=1, command=lambda:gui_support.safeModeChange())
        self.safeOn.place(x=5, y=0, width=50, height=25)

        self.safeOff = ttk.Radiobutton(self.safe, text='Off', variable=safemode, value=0, command=lambda:gui_support.safeModeChange())
        self.safeOff.place(x=5, y=21, width=50, height=25)

        self.safeLim = ttk.Labelframe(self.notebook_basic)
        self.safeLim.place(x=75, y=5, height=175, width=200)
        self.safeLim.configure(relief=SUNKEN)
        self.safeLim.configure(text='''SAFE® Limited Flight Mode''')
        self.safeLim.configure(borderwidth="2")
        self.safeLim.configure(relief=SUNKEN)

        safelimitedflightmodeenabled = gui_support.safelimitedflightmodeenabled

        self.SFMOn = ttk.Radiobutton(self.safeLim, text='Enabled', variable=safelimitedflightmodeenabled, value=0, command=lambda:gui_support.safeLimitedFlightModeEnabledChange())
        self.SFMOn.place(x=5, y=0, width=100, height=25)

        self.SFMOff = ttk.Radiobutton(self.safeLim, text='Disabled', variable=safelimitedflightmodeenabled, value=1, command=lambda:gui_support.safeLimitedFlightModeEnabledChange())
        self.SFMOff.place(x=5, y=21, width=100, height=25)

        defaultsafelimitedflightmode = gui_support.defaultsafelimitedflightmode

        self.defaultSFMOne = ttk.Radiobutton(self.safeLim, text='Switch Position 1', variable=defaultsafelimitedflightmode, value=-1, command=lambda:gui_support.defaultSafeLimitedFlightModeChange())
        self.defaultSFMOne.place(x=5, y=50, width=130, height=25)

        self.defaultSFMTwo = ttk.Radiobutton(self.safeLim, text='Switch Position 2', variable=defaultsafelimitedflightmode, value=-2, command=lambda:gui_support.defaultSafeLimitedFlightModeChange())
        self.defaultSFMTwo.place(x=5, y=71, width=130, height=25)

        self.defaultSFMThree = ttk.Radiobutton(self.safeLim, text='Switch Position 3', variable=defaultsafelimitedflightmode, value=-3, command=lambda:gui_support.defaultSafeLimitedFlightModeChange())
        self.defaultSFMThree.place(x=5, y=92, width=130, height=25)

        safelimitedflightmodeswitchvalue = gui_support.safelimitedflightmodeswitchvalue

        self.SFLMSwitchLabel = ttk.Label(self.safeLim)
        self.SFLMSwitchLabel.place(x=5, y=120, height=29, width=80)
        self.SFLMSwitchLabel.configure(background="#d9d9d9")
        self.SFLMSwitchLabel.configure(foreground="#000000")
        self.SFLMSwitchLabel.configure(relief=FLAT)
        self.SFLMSwitchLabel.configure(text='''Switch Value:''')
        self.SFLMSwitchLabel.configure(anchor=W)

        self.SFLMSwitchEntry = Entry(self.safeLim)
        self.SFLMSwitchEntry.place(x=90, y=120, height=29, width=50)
        self.SFLMSwitchEntry.configure(background="white")
        self.SFLMSwitchEntry.configure(disabledforeground="#a3a3a3")
        self.SFLMSwitchEntry.configure(font="TkFixedFont")
        self.SFLMSwitchEntry.configure(foreground="#000000")
        self.SFLMSwitchEntry.configure(insertbackground="black")
        self.SFLMSwitchEntry.configure(textvariable=safelimitedflightmodeswitchvalue)
        safelimitedflightmodeswitchvalue.trace("w", lambda name, index, mode, safelimitedflightmodeswitchvalue=safelimitedflightmodeswitchvalue: gui_support.safeLimitedFlightModeSwitchValueChange())

        self.safeInfoLabel = ttk.Label(self.notebook_basic)
        self.safeInfoLabel.place(x=5, y=190, height=29, relwidth=.98)
        self.safeInfoLabel.configure(background="#d9d9d9")
        self.safeInfoLabel.configure(foreground="#ee3333")
        self.safeInfoLabel.configure(relief=SUNKEN)
        self.safeInfoLabel.configure(textvariable=gui_support.safeinfolabel)
        self.safeInfoLabel.configure(anchor=W)

        self.trademark = ttk.Label(self.notebook_basic)
        self.trademark.place(x=5, rely=0.95, height=29, relwidth=.98)
        self.trademark.configure(background="#d9d9d9")
        self.trademark.configure(foreground="#000000")
        self.trademark.configure(relief=SUNKEN)
        self.trademark.configure(text="SAFE® - Sensor Assisted Flight Envelope technology - is a registered trademark of Horizon Hobby, Inc.")
        self.trademark.configure(anchor=W)

        # -----------------------------------------------------------------------------------
        # Mixes Tab

        # -----------------------------------------------------------------------------------
        # Advanced Tab

        self.FilterLabel = ttk.Label(self.notebook_t2)
        self.FilterLabel.place(relx=0.0, rely=0.0, height=29, width=32)
        self.FilterLabel.configure(background="#d9d9d9")
        self.FilterLabel.configure(foreground="#000000")
        self.FilterLabel.configure(relief=FLAT)
        self.FilterLabel.configure(text='''Filter:''')
        self.FilterLabel.configure(anchor=E)

        self.Filter = Entry(self.notebook_t2)
        self.Filter.place(relx=0.04, rely=0.0, height=29, relwidth=0.95)
        self.Filter.configure(background="white")
        self.Filter.configure(disabledforeground="#a3a3a3")
        self.Filter.configure(font="TkFixedFont")
        self.Filter.configure(foreground="#000000")
        self.Filter.configure(insertbackground="black")
        filterstring = gui_support.filterstring
        self.Filter.configure(textvariable=filterstring)
        filterstring.trace("w", lambda name, index, mode, filterstring=filterstring: gui_support.filterStringChange())

        self.style.configure('Treeview.Heading',  font="TkDefaultFont")
        self.advancedtree = ScrolledTreeView(self.notebook_t2)
        self.advancedtree.place(relx=0.0, y=30, relheight=0.95, relwidth=1.0)
        self.advancedtree.configure(columns="Col1", selectmode="browse")
        self.advancedtree.heading("#0",text="Options")
        self.advancedtree.heading("#0",anchor="center")
        self.advancedtree.heading("#0",command="advancedselect")
        self.advancedtree.column("#0",width="250")
        self.advancedtree.column("#0",minwidth="20")
        self.advancedtree.column("#0",stretch="1")
        self.advancedtree.column("#0",anchor="w")

        self.advancedtree.heading("Col1",text="Value")
        self.advancedtree.heading("Col1",anchor="center")
        self.advancedtree.column("Col1",width="714")
        self.advancedtree.column("Col1",minwidth="20")
        self.advancedtree.column("Col1",stretch="1")
        self.advancedtree.column("Col1",anchor="w")

        self.advancedtree.bind("<Double-1>", self.__doubleClickAdvancedTree)

class DialogAdvancedEdit:
    def getTree(self):
        return self.Scrolledtreeview1

    def __treeSelection(self, event):
        dialog_support.tree_selection(event)
        dialog_support.showHide({"top":self.frame,"string":[self.TLabel1,self.Entry1],"hex":[self.TLabel3,self.Entry3,self.TButton3],"binary":[self.TLabel4,self.Entry4,self.TButton4]})

    def __init__(self, top, item):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#d9d9d9'  # X11 color: 'gray85'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        top.geometry("700x400+150+150")
        top.title("RxEditor - "+item)
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        self.top = top

        self.frame = Frame(top)
        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.configure(background="#d9d9d9")
        self.frame.configure(highlightbackground="#d9d9d9")
        self.frame.configure(highlightcolor="black")

        self.style.configure('Treeview.Heading',  font="TkDefaultFont")
        self.Scrolledtreeview1 = ScrolledTreeView(top)
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

        self.TButton1 = ttk.Button(top)
        self.TButton1.place(relx=0.2, rely=0.9, height=35, width=120)
        self.TButton1.configure(command=dialog_support.__save)
        self.TButton1.configure(takefocus="")
        self.TButton1.configure(text='''Save''')

        self.TButton2 = ttk.Button(top)
        self.TButton2.place(relx=0.6, rely=0.9, height=35, width=120)
        self.TButton2.configure(command=dialog_support.__cancel)
        self.TButton2.configure(takefocus="")
        self.TButton2.configure(text='''Cancel''')

        self.TLabel1 = ttk.Label(top)
        self.TLabel1.place(relx=0.01, rely=0.45, height=29, width=65)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(relief=FLAT)
        self.TLabel1.configure(textvariable=dialog_support.label1)
        self.TLabel1.configure(anchor=E)

        self.TLabel3 = ttk.Label(top)
        self.TLabel3.place(relx=0.01, rely=0.55, height=29, width=65)
        self.TLabel3.configure(background="#d9d9d9")
        self.TLabel3.configure(foreground="#000000")
        self.TLabel3.configure(relief=FLAT)
        self.TLabel3.configure(text='''Hex:''')
        self.TLabel3.configure(anchor=E)

        self.TLabel4 = ttk.Label(top)
        self.TLabel4.place(relx=0.01, rely=0.65, height=29, width=65)
        self.TLabel4.configure(background="#d9d9d9")
        self.TLabel4.configure(foreground="#000000")
        self.TLabel4.configure(relief=FLAT)
        self.TLabel4.configure(text='''Binary:''')
        self.TLabel4.configure(anchor=E)

        self.infolabel = ttk.Label(top)
        self.infolabel.place(relx=0.01, rely=0.75, height=29, relwidth=.98)
        self.infolabel.configure(background="#d9d9d9")
        self.infolabel.configure(foreground="#ee3333")
        self.infolabel.configure(relief=SUNKEN)
        self.infolabel.configure(textvariable=dialog_support.infolabel)
        self.infolabel.configure(anchor=W)

        self.Entry1 = Entry(top)
        self.Entry1.place(relx=0.13, rely=0.45, relheight=0.06, relwidth=0.85)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")
        valuestring = dialog_support.valuestring
        self.Entry1.configure(textvariable=valuestring)
        valuestring.trace("w", lambda name, index, mode, valuestring=valuestring: dialog_support.valueStringChange())

        self.Entry3 = Entry(top)
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
        valuehex = dialog_support.valuehex
        self.Entry3.configure(textvariable=valuehex)
        valuehex.trace("w", lambda name, index, mode, valuehex=valuehex: dialog_support.valueHexChange())

        self.TButton3 = ttk.Button(top)
        self.TButton3.place(relx=0.87, rely=0.55, height=29, width=80)
        self.TButton3.configure(command=dialog_support.__applyHex)
        self.TButton3.configure(takefocus="")
        self.TButton3.configure(text='''Apply''')

        self.Entry4 = Entry(top)
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
        valuebinary = dialog_support.valuebinary
        self.Entry4.configure(textvariable=valuebinary)
        valuebinary.trace("w", lambda name, index, mode, valuebinary=valuebinary: dialog_support.valueBinaryChange())

        self.TButton4 = ttk.Button(top)
        self.TButton4.place(relx=0.87, rely=0.65, height=29, width=80)
        self.TButton4.configure(command=dialog_support.__applyBinary)
        self.TButton4.configure(takefocus="")
        self.TButton4.configure(text='''Apply''')

        self.Scrolledtreeview1.bind('<ButtonRelease-1>', self.__treeSelection)


# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = Pack.__dict__.keys() | Grid.__dict__.keys() \
                  | Place.__dict__.keys()
        else:
            methods = Pack.__dict__.keys() + Grid.__dict__.keys() \
                  + Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        return func(cls, container, **kw)
    return wrapped

class ScrolledTreeView(AutoScroll, ttk.Treeview):
    '''A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


if __name__ == '__main__':
    vp_start_gui()



