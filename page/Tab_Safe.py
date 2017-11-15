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

class Tab_Safe:
    def __getFileHandle(self):
        if self.fh is None:
            self.fh = rxgui.rxeditorstate.getFileHandle()
        return self.fh

    def __safeModeChange(self):
        fh = self.__getFileHandle()
        if fh is not None:
            fh.setValue(["data", "autopilot", "safeEnabled"], self.safemode.get())
            self.rxeditor.dataChange()

    def __safeLimitedFlightModeEnabledChange(self):
        fh = self.__getFileHandle()
        if fh is not None:
            fh.setValue(["data", "system", "safeLimitedFlightModesDisabled"], self.safelimitedflightmodeenabled.get())
            self.rxeditor.dataChange()

    def __defaultSafeLimitedFlightModeChange(self):
        fh = self.__getFileHandle()
        if fh is not None:
            fh.setValue(["data", "system", "defaultSafeLimitedFlightMode"], self.defaultsafelimitedflightmode.get())
            self.rxeditor.dataChange()

    def __safeLimitedFlightModeSwitchValueChange(self):
        # Validate the value
        try:
            intval = int(self.safelimitedflightmodeswitchvalue.get())
            if intval <= 255 and intval >= 0:
                fh = self.__getFileHandle()
                if fh is not None:
                    fh.setValue(["data", "system", "safeLimitedFlightModeSwitch"], intval)
                    self.rxeditor.dataChange()
            else:
                self.safeinfotext.set("Error: Value must be an integer between 0 and 255.")
        except:
            self.safeinfotext.set("Error: Value must be an integer between 0 and 255.")

    def populate(self, fh):
        self.fh = fh
        try:
            self.safemode.set(fh.getValue(["data", "autopilot", "safeEnabled"], None))
            self.safelimitedflightmodeenabled.set(fh.getValue(["data", "system", "safeLimitedFlightModesDisabled"], None))
            self.defaultsafelimitedflightmode.set(fh.getValue(["data", "system", "defaultSafeLimitedFlightMode"], None))
            self.safelimitedflightmodeswitchvalue.set(
                int(fh.getValue(["data", "system", "safeLimitedFlightModeSwitch"], None)))
            self.safeinfotext.set('')
        except:
            self.safemode.set(0)
            self.safelimitedflightmodeenabled.set(1)
            self.defaultsafelimitedflightmode.set(-1)
            self.safelimitedflightmodeswitchvalue.set(255)
            self.safeinfotext.set("This might not be a SAFE receiver.")

    def draw(self):
        self.notebook_safe = ttk.Frame(self.notebook)
        self.notebook.add(self.notebook_safe, padding=3)
        self.notebook.tab(self.tab_num, text="Safe",underline="-1",)

        self.safe = ttk.Labelframe(self.notebook_safe)
        self.safe.place(x=5, y=5, height=65, width=65)
        self.safe.configure(relief=SUNKEN)
        self.safe.configure(text='''SAFE®''')
        self.safe.configure(borderwidth="2")
        self.safe.configure(relief=SUNKEN)

        safemode = self.safemode

        self.style.map('TRadiobutton',background=[('selected', self.gui_style.getBgColor()), ('active',self.gui_style.getBgColor())])
        self.safeOn = ttk.Radiobutton(self.safe, text='On', variable=safemode, value=1, command=lambda:self.__safeModeChange())
        self.safeOn.place(x=5, y=0, width=50, height=25)

        self.safeOff = ttk.Radiobutton(self.safe, text='Off', variable=safemode, value=0, command=lambda:self.__safeModeChange())
        self.safeOff.place(x=5, y=21, width=50, height=25)

        self.safeLim = ttk.Labelframe(self.notebook_safe)
        self.safeLim.place(x=75, y=5, height=175, width=200)
        self.safeLim.configure(relief=SUNKEN)
        self.safeLim.configure(text='''SAFE® Limited Flight Mode''')
        self.safeLim.configure(borderwidth="2")
        self.safeLim.configure(relief=SUNKEN)

        safelimitedflightmodeenabled = self.safelimitedflightmodeenabled

        self.SFMOn = ttk.Radiobutton(self.safeLim, text='Enabled', variable=safelimitedflightmodeenabled, value=0, command=lambda:self.__safeLimitedFlightModeEnabledChange())
        self.SFMOn.place(x=5, y=0, width=100, height=25)

        self.SFMOff = ttk.Radiobutton(self.safeLim, text='Disabled', variable=safelimitedflightmodeenabled, value=1, command=lambda:self.__safeLimitedFlightModeEnabledChange())
        self.SFMOff.place(x=5, y=21, width=100, height=25)

        defaultsafelimitedflightmode = self.defaultsafelimitedflightmode

        self.defaultSFMOne = ttk.Radiobutton(self.safeLim, text='Switch Position 1', variable=defaultsafelimitedflightmode, value=-1, command=lambda:self.__defaultSafeLimitedFlightModeChange())
        self.defaultSFMOne.place(x=5, y=50, width=130, height=25)

        self.defaultSFMTwo = ttk.Radiobutton(self.safeLim, text='Switch Position 2', variable=defaultsafelimitedflightmode, value=-2, command=lambda:self.__defaultSafeLimitedFlightModeChange())
        self.defaultSFMTwo.place(x=5, y=71, width=130, height=25)

        self.defaultSFMThree = ttk.Radiobutton(self.safeLim, text='Switch Position 3', variable=defaultsafelimitedflightmode, value=-3, command=lambda:self.__defaultSafeLimitedFlightModeChange())
        self.defaultSFMThree.place(x=5, y=92, width=130, height=25)

        safelimitedflightmodeswitchvalue = self.safelimitedflightmodeswitchvalue

        self.SFLMSwitchLabel = ttk.Label(self.safeLim)
        self.SFLMSwitchLabel.place(x=5, y=120, height=29, width=80)
        self.SFLMSwitchLabel.configure(background=self.gui_style.getBgColor())
        self.SFLMSwitchLabel.configure(foreground=self.gui_style.getFgColor())
        self.SFLMSwitchLabel.configure(relief=FLAT)
        self.SFLMSwitchLabel.configure(text='''Switch Value:''')
        self.SFLMSwitchLabel.configure(anchor=W)

        self.SFLMSwitchEntry = Entry(self.safeLim)
        self.SFLMSwitchEntry.place(x=90, y=120, height=29, width=50)
        self.SFLMSwitchEntry.configure(background="white")
        self.SFLMSwitchEntry.configure(disabledforeground="#a3a3a3")
        self.SFLMSwitchEntry.configure(font="TkFixedFont")
        self.SFLMSwitchEntry.configure(foreground=self.gui_style.getFgColor())
        self.SFLMSwitchEntry.configure(insertbackground="black")
        self.SFLMSwitchEntry.configure(textvariable=safelimitedflightmodeswitchvalue)
        safelimitedflightmodeswitchvalue.trace("w", lambda name, index, mode, safelimitedflightmodeswitchvalue=safelimitedflightmodeswitchvalue: self.__safeLimitedFlightModeSwitchValueChange())

        self.safeInfoLabel = ttk.Label(self.notebook_safe)
        self.safeInfoLabel.place(x=5, y=190, height=29, relwidth=.98)
        self.safeInfoLabel.configure(background=self.gui_style.getBgColor())
        self.safeInfoLabel.configure(foreground="#ee3333")
        self.safeInfoLabel.configure(relief=SUNKEN)
        self.safeInfoLabel.configure(textvariable=self.safeinfotext)
        self.safeInfoLabel.configure(anchor=W)

        self.trademark = ttk.Label(self.notebook_safe)
        self.trademark.place(x=5, rely=0.95, height=29, relwidth=.98)
        self.trademark.configure(background=self.gui_style.getBgColor())
        self.trademark.configure(foreground=self.gui_style.getFgColor())
        self.trademark.configure(relief=SUNKEN)
        self.trademark.configure(text="SAFE® - Sensor Assisted Flight Envelope technology - is a registered trademark of Horizon Hobby, Inc.")
        self.trademark.configure(anchor=W)


    def __init__(self, rxeditor, tab_num):
        self.rxeditor = rxeditor
        self.top = rxeditor.getTop()
        self.notebook = rxeditor.getNotebook()
        self.tab_num = tab_num
        self.gui_style = rxeditor.getStyle()
        self.style = self.gui_style.getStyle()
        self.safemode = IntVar()
        self.safelimitedflightmodeenabled = IntVar()
        self.defaultsafelimitedflightmode = IntVar()
        self.safelimitedflightmodeswitchvalue = StringVar()
        self.safeinfotext = StringVar()
        self.fh = rxgui.rxeditorstate.getFileHandle()
