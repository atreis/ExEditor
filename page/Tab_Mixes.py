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

    def __disableThrottleToElevatorMix(self):
        if self.ignorechange:
            return
        self.thr2pitchangle0.set(-1)
        self.thr2pitchthreshold0.set(255)
        self.thr2pitchangle1.set(-1)
        self.thr2pitchthreshold1.set(255)

    def __thr2PitchAngle0Change(self):
        if self.ignorechange:
            return
        fh = self.__getFileHandle()
        try:
            fh.setValue(["data","autopilot","thr2pitch","0","angle"], int(self.thr2pitchangle0.get()))
        except:
            # Ignore
            return
        self.__setDescriptions()
        self.rxeditor.dataChange()

    def __thr2PitchThreshold0Change(self):
        if self.ignorechange:
            return
        fh = self.__getFileHandle()
        try:
            fh.setValue(["data","autopilot","thr2pitch","0","threshold"], int(self.thr2pitchthreshold0.get()))
        except:
            # Ignore
            return
        self.__setDescriptions()
        self.rxeditor.dataChange()

    def __thr2PitchAngle1Change(self):
        if self.ignorechange:
            return
        fh = self.__getFileHandle()
        try:
            fh.setValue(["data","autopilot","thr2pitch","1","angle"], int(self.thr2pitchangle1.get()))
        except:
            # Ignore
            return
        self.__setDescriptions()
        self.rxeditor.dataChange()

    def __thr2PitchThreshold1Change(self):
        if self.ignorechange:
            return
        fh = self.__getFileHandle()
        try:
            fh.setValue(["data","autopilot","thr2pitch","1","threshold"], int(self.thr2pitchthreshold1.get()))
        except:
            # Ignore
            return
        self.__setDescriptions()
        self.rxeditor.dataChange()

    def __thr2PitchLinearChange(self):
        if self.ignorechange:
            return
        fh = self.__getFileHandle()
        try:
            fh.setValue(["data","autopilot","thr2pitchLinear"], int(self.thr2pitchlinear.get()))
        except:
            # Ignore
            return
        self.rxeditor.dataChange()

    def __setDescription(self, value, label):
        if value == 0:
            label.configure(text='No Mix')
        elif value > 0:
            label.configure(text='Degrees Down Elevator')
        else:
            label.configure(text='Degrees Up Elevator')

    def __setDescriptions(self):
        self.__setDescription(self.thr2pitchangle0.get(), self.thr2pitchangledesclabel0)
        self.__setDescription(self.thr2pitchangle1.get(), self.thr2pitchangledesclabel1)

    def populate(self, fh):
        self.fh = fh
        self.ignorechange = True

        try:
            # Get the current values
            self.thr2pitchangle0.set(fh.getValue(["data","autopilot","thr2pitch","0","angle"], None))
            self.thr2pitchthreshold0.set(fh.getValue(["data","autopilot","thr2pitch","0","threshold"], None))
            self.thr2pitchangle1.set(fh.getValue(["data","autopilot","thr2pitch","1","angle"], None))
            self.thr2pitchthreshold1.set(fh.getValue(["data","autopilot","thr2pitch","1","threshold"], None))
            self.thr2pitchlinear.set(fh.getValue(["data","autopilot","thr2pitchLinear"], None))
            self.__setDescriptions()
        except:
            pass

        self.ignorechange = False

    def draw(self):
        self.notebook_mixes = ttk.Frame(self.notebook)
        self.notebook.add(self.notebook_mixes, padding=3)
        self.notebook.tab(self.tab_num, text="Mixes",underline="-1",)

        self.rxthrottletoelevatorframe = ttk.Labelframe(self.notebook_mixes)
        self.rxthrottletoelevatorframe.place(x=5, y=5, height=230, width=260)
        self.rxthrottletoelevatorframe.configure(relief=SUNKEN)
        self.rxthrottletoelevatorframe.configure(text='''Throttle to Elevator''')
        self.rxthrottletoelevatorframe.configure(borderwidth="2")
        self.rxthrottletoelevatorframe.configure(relief=SUNKEN)

        self.style.map('TRadiobutton',background=[('selected', self.gui_style.getBgColor()), ('active',self.gui_style.getBgColor())])

        # Button to turn off throttle to elevator mix entirely
        self.TButton1 = ttk.Button(self.rxthrottletoelevatorframe)
        self.TButton1.place(x=5, y=0, height=25, width=200)
        self.TButton1.configure(command=self.__disableThrottleToElevatorMix)
        self.TButton1.configure(takefocus="")
        self.TButton1.configure(text='''Disable Throttle to Elevator Mix''')

        # Settings for throttle to elevator mix
        thr2pitchangle0 = self.thr2pitchangle0
        thr2pitchangle1 = self.thr2pitchangle1
        thr2pitchthreshold0 = self.thr2pitchthreshold0
        thr2pitchthreshold1 = self.thr2pitchthreshold1

        self.thr2pitchlabel = ttk.Label(self.rxthrottletoelevatorframe)
        self.thr2pitchlabel.place(x=5, y=40, width=170, height=21)
        self.thr2pitchlabel.configure(text = 'Low Throttle Elevator Mix')

        self.thr2pitchanglelabel0 = ttk.Label(self.rxthrottletoelevatorframe)
        self.thr2pitchanglelabel0.place(x=5, y=61, width=70, height=25)
        self.thr2pitchanglelabel0.configure(text = 'Angle: ')

        self.thr2pitchangle0entry = Entry(self.rxthrottletoelevatorframe)
        self.thr2pitchangle0entry.place(x=75, y=61, height=21, width=50)
        self.thr2pitchangle0entry.configure(background="white")
        self.thr2pitchangle0entry.configure(disabledforeground="#a3a3a3")
        self.thr2pitchangle0entry.configure(font="TkFixedFont")
        self.thr2pitchangle0entry.configure(foreground="#000000")
        self.thr2pitchangle0entry.configure(highlightbackground="#d9d9d9")
        self.thr2pitchangle0entry.configure(highlightcolor="black")
        self.thr2pitchangle0entry.configure(insertbackground="black")
        self.thr2pitchangle0entry.configure(selectbackground="#c4c4c4")
        self.thr2pitchangle0entry.configure(selectforeground="black")
        self.thr2pitchangle0entry.configure(textvariable=thr2pitchangle0)
        thr2pitchangle0.trace("w", lambda name, index, mode, thr2pitchangle0=thr2pitchangle0: self.__thr2PitchAngle0Change())

        self.thr2pitchangledesclabel0 = ttk.Label(self.rxthrottletoelevatorframe)
        self.thr2pitchangledesclabel0.place(x=125, y=61, width=130, height=25)
        self.thr2pitchangledesclabel0.configure(text = 'No Mix')

        self.thr2pitchthresholdlabel0 = ttk.Label(self.rxthrottletoelevatorframe)
        self.thr2pitchthresholdlabel0.place(x=5, y=82, width=70, height=25)
        self.thr2pitchthresholdlabel0.configure(text = 'Threshold: ')

        self.thr2pitchthreshold0entry = Entry(self.rxthrottletoelevatorframe)
        self.thr2pitchthreshold0entry.place(x=75, y=82, height=21, width=50)
        self.thr2pitchthreshold0entry.configure(background="white")
        self.thr2pitchthreshold0entry.configure(disabledforeground="#a3a3a3")
        self.thr2pitchthreshold0entry.configure(font="TkFixedFont")
        self.thr2pitchthreshold0entry.configure(foreground="#000000")
        self.thr2pitchthreshold0entry.configure(highlightbackground="#d9d9d9")
        self.thr2pitchthreshold0entry.configure(highlightcolor="black")
        self.thr2pitchthreshold0entry.configure(insertbackground="black")
        self.thr2pitchthreshold0entry.configure(selectbackground="#c4c4c4")
        self.thr2pitchthreshold0entry.configure(selectforeground="black")
        self.thr2pitchthreshold0entry.configure(textvariable=thr2pitchthreshold0)
        thr2pitchthreshold0.trace("w", lambda name, index, mode, thr2pitchthreshold0=thr2pitchthreshold0: self.__thr2PitchThreshold0Change())

        self.thr2pitchthresholddesclabel0 = ttk.Label(self.rxthrottletoelevatorframe)
        self.thr2pitchthresholddesclabel0.place(x=125, y=82, width=130, height=25)
        self.thr2pitchthresholddesclabel0.configure(text = 'Percent Throttle')

        self.thr2pitchlabel1 = ttk.Label(self.rxthrottletoelevatorframe)
        self.thr2pitchlabel1.place(x=5, y=110, width=170, height=21)
        self.thr2pitchlabel1.configure(text = 'High Throttle Elevator Mix')

        self.thr2pitchanglelabel1 = ttk.Label(self.rxthrottletoelevatorframe)
        self.thr2pitchanglelabel1.place(x=5, y=131, width=70, height=25)
        self.thr2pitchanglelabel1.configure(text = 'Angle: ')

        self.thr2pitchangle1entry = Entry(self.rxthrottletoelevatorframe)
        self.thr2pitchangle1entry.place(x=75, y=131, height=21, width=50)
        self.thr2pitchangle1entry.configure(background="white")
        self.thr2pitchangle1entry.configure(disabledforeground="#a3a3a3")
        self.thr2pitchangle1entry.configure(font="TkFixedFont")
        self.thr2pitchangle1entry.configure(foreground="#000000")
        self.thr2pitchangle1entry.configure(highlightbackground="#d9d9d9")
        self.thr2pitchangle1entry.configure(highlightcolor="black")
        self.thr2pitchangle1entry.configure(insertbackground="black")
        self.thr2pitchangle1entry.configure(selectbackground="#c4c4c4")
        self.thr2pitchangle1entry.configure(selectforeground="black")
        self.thr2pitchangle1entry.configure(textvariable=thr2pitchangle1)
        thr2pitchangle1.trace("w", lambda name, index, mode, thr2pitchangle1=thr2pitchangle1: self.__thr2PitchAngle1Change())

        self.thr2pitchangledesclabel1 = ttk.Label(self.rxthrottletoelevatorframe)
        self.thr2pitchangledesclabel1.place(x=125, y=131, width=130, height=25)
        self.thr2pitchangledesclabel1.configure(text = 'No Mix')

        self.thr2pitchthresholdlabel1 = ttk.Label(self.rxthrottletoelevatorframe)
        self.thr2pitchthresholdlabel1.place(x=5, y=152, width=70, height=25)
        self.thr2pitchthresholdlabel1.configure(text = 'Threshold: ')

        self.thr2pitchthreshold1entry = Entry(self.rxthrottletoelevatorframe)
        self.thr2pitchthreshold1entry.place(x=75, y=152, height=21, width=50)
        self.thr2pitchthreshold1entry.configure(background="white")
        self.thr2pitchthreshold1entry.configure(disabledforeground="#a3a3a3")
        self.thr2pitchthreshold1entry.configure(font="TkFixedFont")
        self.thr2pitchthreshold1entry.configure(foreground="#000000")
        self.thr2pitchthreshold1entry.configure(highlightbackground="#d9d9d9")
        self.thr2pitchthreshold1entry.configure(highlightcolor="black")
        self.thr2pitchthreshold1entry.configure(insertbackground="black")
        self.thr2pitchthreshold1entry.configure(selectbackground="#c4c4c4")
        self.thr2pitchthreshold1entry.configure(selectforeground="black")
        self.thr2pitchthreshold1entry.configure(textvariable=thr2pitchthreshold1)
        thr2pitchthreshold1.trace("w", lambda name, index, mode, thr2pitchthreshold1=thr2pitchthreshold1: self.__thr2PitchThreshold1Change())

        self.thr2pitchthresholddesclabel1 = ttk.Label(self.rxthrottletoelevatorframe)
        self.thr2pitchthresholddesclabel1.place(x=125, y=152, width=130, height=25)
        self.thr2pitchthresholddesclabel1.configure(text = 'Percent Throttle')

        self.thr2pitchblendlabel = ttk.Label(self.rxthrottletoelevatorframe)
        self.thr2pitchblendlabel.place(x=5, y=180, width=150, height=25)
        self.thr2pitchblendlabel.configure(text = 'Low to High Transition: ')

        thr2pitchlinear = self.thr2pitchlinear
        self.thr2pitchblendlinear = ttk.Radiobutton(self.rxthrottletoelevatorframe, text='Linear', variable=thr2pitchlinear, value=252, command=lambda:self.__thr2PitchLinearChange())
        self.thr2pitchblendstep = ttk.Radiobutton(self.rxthrottletoelevatorframe, text='Step', variable=thr2pitchlinear, value=255, command=lambda:self.__thr2PitchLinearChange())
        self.thr2pitchblendlinear.place(x=135, y=180, width=60, height=25)
        self.thr2pitchblendstep.place(x=195, y=180, width=60, height=25)

    def replaceFh(self):
        self.fh = rxgui.rxeditorstate.getFileHandle()

    def __init__(self, rxeditor, tab_num):
        self.top = rxeditor.getTop()
        self.notebook = rxeditor.getNotebook()
        self.rxeditor = rxeditor
        self.tab_num = tab_num
        self.gui_style = rxeditor.getStyle()
        self.style = self.gui_style.getStyle()
        self.fh = rxgui.rxeditorstate.getFileHandle()
        self.ignorechange = False

        self.thr2pitchangle0 = IntVar()
        self.thr2pitchangle0.set(0)
        self.thr2pitchthreshold0 = IntVar()
        self.thr2pitchthreshold0.set(0)
        self.thr2pitchangle1 = IntVar()
        self.thr2pitchangle1.set(0)
        self.thr2pitchthreshold1 = IntVar()
        self.thr2pitchthreshold1.set(0)

        self.thr2pitchlinear = IntVar()
        self.thr2pitchlinear.set(255)