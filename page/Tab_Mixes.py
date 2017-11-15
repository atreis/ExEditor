import sys
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

class Tab_Mixes:
    def __getFileHandle(self):
        if self.fh is None:
            self.fh = rxgui.rxeditorstate.getFileHandle()
        return self.fh

    def populate(self, fh):
        self.fh = fh

    def draw(self):
        self.notebook_mixes = ttk.Frame(self.notebook)
        self.notebook.add(self.notebook_mixes, padding=3)
        self.notebook.tab(self.tab_num, text="Mixes",underline="-1",)


    def __init__(self, rxeditor, tab_num):
        self.top = rxeditor.getTop()
        self.notebook = rxeditor.getNotebook()
        self.rxeditor = rxeditor
        self.tab_num = tab_num
        self.gui_style = rxeditor.getStyle()
        self.style = self.gui_style.getStyle()
        self.fh = rxgui.rxeditorstate.getFileHandle()
