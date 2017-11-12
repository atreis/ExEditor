import sys
import json
import traceback
import rxgui
import rxfile

from page import ScrolledTreeView
from page import Dialog_AdvancedEdit

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

class Tab_Advanced:
    def __getFileHandle(self):
        if self.fh is None:
            self.fh = rxgui.rxeditorstate.getFileHandle()
        return self.fh

    def __tree_doubleclick(self):
        item = self.advancedtree.selection()[0]
        # print('item: '+str(item))
        keys = item.split('-')
        # print('keys: '+str(keys))
        values = self.advancedtree.item(item)["values"]
        # print('values: '+str(values))
        if len(values) > 0:
            # We have a value - prevents an error from clicking parent elements in the tree
            value = values[0]
            # print('value: '+str(value))
            if isinstance(value, str) and value.startswith('['):
                # Value is really a list
                value = json.loads(value)
            elif isinstance(value, str) and value.startswith('0x'):
                # Value in hex
                pass
            else:
                try:
                    value = int(value)
                except ValueError:
                    # Just go with a string
                    pass

            return item, keys, value, self.__getFileHandle()

    def __tree_updatevalues(self, item, keys, newvalues, fh):
        self.advancedtree.item(item, values=[str(newvalues)])
        fh.setValue(keys, newvalues)

    def __create_DialogAdvancedEdit(self, parent, item, keys, values, fh):
        ae_rt = parent
        advancedEdit = Toplevel(parent)
        ae_top = Dialog_AdvancedEdit.Dialog_AdvancedEdit(advancedEdit, self.style, item, fh, keys, values)
        ae_top.draw()
        self.notebook.wait_window(advancedEdit)
        return ae_top.getValues()

    def __doubleClickAdvancedTree(self, event):
        item, keys, value, fh = self.__tree_doubleclick()
        newvalues = self.__create_DialogAdvancedEdit(self.top, item, keys, value, fh)
        # print('newvalues: '+str(newvalues))
        if newvalues is not None:
            self.__tree_updatevalues(item, keys, newvalues, fh)

    def __filterStringChange(self):
        if len(self.filterstring.get()) > 0:
            fh = self.__getFileHandle()
            rxgui.PopulateSettings.clear(self.advancedtree)
            rxgui.PopulateSettings.populateAdvancedTreeFiltered(fh, self.advancedtree, self.filterstring.get().lower())
        else:
            fh = self.__getFileHandle()
            rxgui.PopulateSettings.clear(self.advancedtree)
            rxgui.PopulateSettings.populateAdvancedTree(fh, self.advancedtree)

    def getAdvancedTree(self):
        return self.advancedtree

    def setFilterString(self, s):
        self.filterstring.set(s)

    def dataChange(self):
        self.__filterStringChange()

    def draw(self):
        self.notebook_advanced = ttk.Frame(self.notebook)
        self.notebook.add(self.notebook_advanced, padding=3)
        self.notebook.tab(self.tab_num, text="Advanced",underline="-1",)

        self.FilterLabel = ttk.Label(self.notebook_advanced)
        self.FilterLabel.place(relx=0.0, rely=0.0, height=29, width=32)
        self.FilterLabel.configure(background="#d9d9d9")
        self.FilterLabel.configure(foreground="#000000")
        self.FilterLabel.configure(relief=FLAT)
        self.FilterLabel.configure(text='''Filter:''')
        self.FilterLabel.configure(anchor=E)

        self.Filter = Entry(self.notebook_advanced)
        self.Filter.place(relx=0.04, rely=0.0, height=29, relwidth=0.95)
        self.Filter.configure(background="white")
        self.Filter.configure(disabledforeground="#a3a3a3")
        self.Filter.configure(font="TkFixedFont")
        self.Filter.configure(foreground="#000000")
        self.Filter.configure(insertbackground="black")
        filterstring = self.filterstring
        self.Filter.configure(textvariable=filterstring)
        filterstring.trace("w", lambda name, index, mode, filterstring=filterstring: self.__filterStringChange())

        self.style.configure('Treeview.Heading', font="TkDefaultFont")
        self.advancedtree = ScrolledTreeView.ScrolledTreeView(self.notebook_advanced)
        self.advancedtree.place(relx=0.0, y=30, relheight=0.95, relwidth=1.0)
        self.advancedtree.configure(columns="Col1", selectmode="browse")
        self.advancedtree.heading("#0", text="Options")
        self.advancedtree.heading("#0", anchor="center")
        self.advancedtree.heading("#0", command="advancedselect")
        self.advancedtree.column("#0", width="250")
        self.advancedtree.column("#0", minwidth="20")
        self.advancedtree.column("#0", stretch="1")
        self.advancedtree.column("#0", anchor="w")

        self.advancedtree.heading("Col1", text="Value")
        self.advancedtree.heading("Col1", anchor="center")
        self.advancedtree.column("Col1", width="714")
        self.advancedtree.column("Col1", minwidth="20")
        self.advancedtree.column("Col1", stretch="1")
        self.advancedtree.column("Col1", anchor="w")

        self.advancedtree.bind("<Double-1>", self.__doubleClickAdvancedTree)

    def __init__(self, rxeditor, tab_num):
        self.top = rxeditor.getTop()
        self.notebook = rxeditor.getNotebook()
        self.rxeditor = rxeditor
        self.tab_num = tab_num
        self.gui_style = rxeditor.getStyle()
        self.style = self.gui_style.getStyle()
        self.fh = rxgui.rxeditorstate.getFileHandle()
        self.filterstring = StringVar()
