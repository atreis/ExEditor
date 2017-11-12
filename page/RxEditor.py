import traceback
import rxgui
import rxfile

from page import Tab_Safe
from page import Tab_Orientation
from page import Tab_Advanced
from page import gui_style

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    from tkinter import filedialog
    py3 = 1

class RxEditor:
    def __menu_open(self):
        options = {}
        options['title'] = "Open Rx SRM..."
        options['filetypes'] = [('srm', '*.srm'), ('any', '*.*')]
        filename = filedialog.askopenfile(mode="r", **options)
        if filename is not None:
            # print(filename.name)
            try:
                fh = rxfile.RxFileHandler.RxFileWrapper(filename.name)
                rxgui.rxeditorstate.setFileHandle(fh)
                rxgui.PopulateSettings.clear(self.advanced.getAdvancedTree())
                rxgui.PopulateSettings.populateAdvancedTree(fh, self.advanced.getAdvancedTree())
                self.advanced.setFilterString('')
                rxgui.PopulateSettings.populateSafeTab(fh, self.safe.getComponents())
            except:
                traceback.print_exc()

    def __menu_save(self):
        fh = rxgui.rxeditorstate.getFileHandle()
        if fh is not None:
            fh.save()

    def __menu_saveAs(self):
        fh = rxgui.rxeditorstate.getFileHandle()
        if fh is not None:
            options = {}
            options['title'] = "Save Rx SRM..."
            options['filetypes'] = [('srm', '*.srm'), ('any', '*.*')]
            options['defaultextension'] = '.srm'
            filename = filedialog.asksaveasfile(mode="w", **options)
            if filename is not None:
                fh.saveAs(filename.name)

    def __menu_exit(self):
        fh = rxgui.rxeditorstate.getFileHandle()
        if fh is not None and fh.isDirty():
            self.__menu_saveAs()
        self.__destroy_window()

    def __destroy_window(self):
        # Function which closes the window.
        self.top.destroy()
        self.top = None

    def getTop(self):
        return self.top

    def getNotebook(self):
        return self.notebook

    def getStyle(self):
        return self.gui_style

    def dataChange(self):
        # Refresh data on other tabs
        self.advanced.dataChange()

    def draw(self):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#d9d9d9'  # X11 color: 'gray85'
        self.style = ttk.Style()
        self.gui_style = gui_style.gui_style(self.style)

        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        self.top.geometry("1000x700+100+100")
        self.top.title("RxEditor (v0.8.5)")
        self.top.configure(background="#d9d9d9")
        self.top.configure(highlightbackground="#e9e9e9")
        self.top.configure(highlightcolor="#191919")

        self.menubar = Menu(self.top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        self.top.configure(menu=self.menubar)

        self.file = Menu(self.top, tearoff=0)
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
            command=self.__menu_open,
            font="TkMenuFont",
            foreground="#000000",
            label="Open...")
        self.file.add_command(
            activebackground="#d8d8d8",
            activeforeground="#000000",
            accelerator="s",
            background="#d9d9d9",
            command=self.__menu_save,
            font="TkMenuFont",
            foreground="#000000",
            label="Save")
        self.file.add_command(
            activebackground="#d8d8d8",
            activeforeground="#000000",
            accelerator="a",
            background="#d9d9d9",
            command=self.__menu_saveAs,
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
            command=self.__menu_exit,
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
        [('selected', _compcolor), ('active', _ana2color)])
        self.notebook = ttk.Notebook(self.top)
        self.notebook.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.notebook.configure(width=300)
        self.notebook.configure(takefocus="")

        # -----------------------------------------------------------------------------------
        # SAFE Tab

        tab_num = 0
        self.safe = Tab_Safe.Tab_Safe(self, tab_num)
        self.safe.draw()

        # -----------------------------------------------------------------------------------
        # Orientation Tab

        tab_num += 1
        self.orientation = Tab_Orientation.Tab_Orientation(self, tab_num)
        self.orientation.draw()

        # -----------------------------------------------------------------------------------
        # Advanced Tab

        tab_num += 1
        self.advanced = Tab_Advanced.Tab_Advanced(self, tab_num)
        self.advanced.draw()

    def __init__(self, top=None):
        self.top = top
