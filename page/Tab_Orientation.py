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

class Tab_Orientation:
    def __getFileHandle(self):
        if self.fh is None:
            self.fh = rxgui.rxeditorstate.getFileHandle()
        return self.fh

    def __rxOrientationChange(self):
        if self.ignorechange:
            return
        '''
        Pins Toward Nose, Label Toward Sky	axis2aircraft = 36, axisDirection = 4
        Pins Toward Nose, Label Toward Ground	axis2aircraft = 36, axisDirection = 2
        Pins Toward Nose, Label Toward Left	axis2aircraft = 24, axisDirection = 6
        Pins Toward Nose, Label Toward Right	axis2aircraft = 24, axisDirection = 0
        Pins Toward Tail, Label Toward Sky	axis2aircraft = 36, axisDirection = 7
        Pins Toward Tail, Label Toward Ground	axis2aircraft = 36, axisDirection = 1
        Pins Toward Tail, Label Toward Left	axis2aircraft = 24, axisDirection = 3
        Pins Toward Tail, Label Toward Right	axis2aircraft = 24, axisDirection = 5
        '''
        fh = self.__getFileHandle()
        if fh is not None:
            if self.rxorientation.get()==0:
                fh.setValue(["data", "system", "axisDirection"], 4)
                fh.setValue(["data", "system", "axis2aircraft"], 36)
                self.rxOrientImage.configure(image=self.rxPinsForwardLabelUpImg)
            elif self.rxorientation.get()==1:
                fh.setValue(["data", "system", "axisDirection"], 2)
                fh.setValue(["data", "system", "axis2aircraft"], 36)
                self.rxOrientImage.configure(image=self.rxPinsForwardLabelDownImg)
            elif self.rxorientation.get()==2:
                fh.setValue(["data", "system", "axisDirection"], 6)
                fh.setValue(["data", "system", "axis2aircraft"], 24)
                self.rxOrientImage.configure(image=self.rxPinsForwardLabelLeftImg)
            elif self.rxorientation.get()==3:
                fh.setValue(["data", "system", "axisDirection"], 0)
                fh.setValue(["data", "system", "axis2aircraft"], 24)
                self.rxOrientImage.configure(image=self.rxPinsForwardLabelRightImg)
            elif self.rxorientation.get()==4:
                fh.setValue(["data", "system", "axisDirection"], 7)
                fh.setValue(["data", "system", "axis2aircraft"], 36)
                self.rxOrientImage.configure(image=self.rxPinsAftLabelUpImg)
            elif self.rxorientation.get()==5:
                fh.setValue(["data", "system", "axisDirection"], 1)
                fh.setValue(["data", "system", "axis2aircraft"], 36)
                self.rxOrientImage.configure(image=self.rxPinsAftLabelDownImg)
            elif self.rxorientation.get()==6:
                fh.setValue(["data", "system", "axisDirection"], 3)
                fh.setValue(["data", "system", "axis2aircraft"], 24)
                self.rxOrientImage.configure(image=self.rxPinsAftLabelLeftImg)
            elif self.rxorientation.get()==7:
                fh.setValue(["data", "system", "axisDirection"], 5)
                fh.setValue(["data", "system", "axis2aircraft"], 24)
                self.rxOrientImage.configure(image=self.rxPinsAftLabelRightImg)
            elif self.rxorientation.get()==8:
                fh.setValue(["data", "system", "axisDirection"], 6)
                fh.setValue(["data", "system", "axis2aircraft"], 33)
                self.rxOrientImage.configure(image=self.rxPinsLeftLabelUpImg)
            else:
                self.rxOrientImage.configure(image=self.rxOtherImg)
            self.rxeditor.dataChange()

    def populate(self, fh):
        self.fh = fh
        self.ignorechange = True
        try:
            axisdir = fh.getValue(["data","system","axisDirection"], None)
            axis2 = fh.getValue(["data","system","axis2aircraft"], None)

            if axisdir == 4 and axis2 == 36:
                self.rxorientation.set(0)
                self.rxOrientImage.configure(image=self.rxPinsForwardLabelUpImg)
            elif axisdir == 2 and axis2 == 36:
                self.rxorientation.set(1)
                self.rxOrientImage.configure(image=self.rxPinsForwardLabelDownImg)
            elif axisdir == 6 and axis2 == 24:
                self.rxorientation.set(2)
                self.rxOrientImage.configure(image=self.rxPinsForwardLabelLeftImg)
            elif axisdir == 0 and axis2 == 24:
                self.rxorientation.set(3)
                self.rxOrientImage.configure(image=self.rxPinsForwardLabelRightImg)
            elif axisdir == 7 and axis2 == 36:
                self.rxorientation.set(4)
                self.rxOrientImage.configure(image=self.rxPinsAftLabelUpImg)
            elif axisdir == 1 and axis2 == 36:
                self.rxorientation.set(5)
                self.rxOrientImage.configure(image=self.rxPinsAftLabelDownImg)
            elif axisdir == 3 and axis2 == 24:
                self.rxorientation.set(6)
                self.rxOrientImage.configure(image=self.rxPinsAftLabelLeftImg)
            elif axisdir == 5 and axis2 == 24:
                self.rxorientation.set(7)
                self.rxOrientImage.configure(image=self.rxPinsAftLabelRightImg)
            elif axisdir == 6 and axis2 == 33:
                self.rxorientation.set(8)
                self.rxOrientImage.configure(image=self.rxPinsLeftLabelUpImg)
            else:
                self.rxorientation.set(-1)
                self.rxOrientImage.configure(image=self.rxOtherImg)
            self.ignorechange = False
        except:
            self.rxorientation.set(-1)
            self.ignorechange = False

    def draw(self):
        self.notebook_orientation = ttk.Frame(self.notebook)
        self.notebook.add(self.notebook_orientation, padding=3)
        self.notebook.tab(self.tab_num, text="Orientation",underline="-1",)

        self.rxorientframe = ttk.Labelframe(self.notebook_orientation)
        self.rxorientframe.place(x=5, y=5, height=280, width=500)
        self.rxorientframe.configure(relief=SUNKEN)
        self.rxorientframe.configure(text='''Receiver Orientation''')
        self.rxorientframe.configure(borderwidth="2")
        self.rxorientframe.configure(relief=SUNKEN)

        self.style.map('TRadiobutton',background=[('selected', self.gui_style.getBgColor()), ('active',self.gui_style.getBgColor())])

        rxorientation = self.rxorientation

        self.rxPinsForwardLabelUp = ttk.Radiobutton(self.rxorientframe, text='Pins Towards Nose, Label Up', variable=rxorientation, value=0, command=lambda:self.__rxOrientationChange())
        self.rxPinsForwardLabelDown = ttk.Radiobutton(self.rxorientframe, text='Pins Towards Nose, Label Down', variable=rxorientation, value=1, command=lambda:self.__rxOrientationChange())
        self.rxPinsForwardLabelLeft = ttk.Radiobutton(self.rxorientframe, text='Pins Towards Nose, Label Left', variable=rxorientation, value=2, command=lambda:self.__rxOrientationChange())
        self.rxPinsForwardLabelRight = ttk.Radiobutton(self.rxorientframe, text='Pins Towards Nose, Label Right', variable=rxorientation, value=3, command=lambda:self.__rxOrientationChange())
        self.rxPinsAftLabelUp = ttk.Radiobutton(self.rxorientframe, text='Pins Towards Tail, Label Up', variable=rxorientation, value=4, command=lambda:self.__rxOrientationChange())
        self.rxPinsAftLabelDown = ttk.Radiobutton(self.rxorientframe, text='Pins Towards Tail, Label Down', variable=rxorientation, value=5, command=lambda:self.__rxOrientationChange())
        self.rxPinsAftLabelLeft = ttk.Radiobutton(self.rxorientframe, text='Pins Towards Tail, Label Left', variable=rxorientation, value=6, command=lambda:self.__rxOrientationChange())
        self.rxPinsAftLabelRight = ttk.Radiobutton(self.rxorientframe, text='Pins Towards Tail, Label Right', variable=rxorientation, value=7, command=lambda:self.__rxOrientationChange())

        self.rxPinsLeftLabelUp = ttk.Radiobutton(self.rxorientframe, text='Pins Left, Label Up', variable=rxorientation, value=8, command=lambda:self.__rxOrientationChange())

        self.rxOrientOther = ttk.Radiobutton(self.rxorientframe, text='Other', variable=rxorientation, value=-1, command=lambda:self.__rxOrientationChange())

        self.rxPinsForwardLabelUp.place(x=5, y=0, width=230, height=25)
        self.rxPinsForwardLabelDown.place(x=5, y=21, width=230, height=25)
        self.rxPinsForwardLabelLeft.place(x=5, y=42, width=230, height=25)
        self.rxPinsForwardLabelRight.place(x=5, y=63, width=230, height=25)
        self.rxPinsAftLabelUp.place(x=5, y=84, width=230, height=25)
        self.rxPinsAftLabelDown.place(x=5, y=105, width=230, height=25)
        self.rxPinsAftLabelLeft.place(x=5, y=126, width=230, height=25)
        self.rxPinsAftLabelRight.place(x=5, y=147, width=230, height=25)

        self.rxPinsLeftLabelUp.place(x=5, y=189, width=230, height=25)

        self.rxOrientOther.place(x=5, y=231, width=230, height=25)

        # rx orientation image
        self.rxOrientImage = ttk.Label(self.rxorientframe)
        self.rxOrientImage.place(x=240, y=0, width=250, height=250)
        self.rxOrientImage.configure(image = self.rxOtherImg)
        self.rxOrientImage.configure(relief=SUNKEN)

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
        self.rxorientation = IntVar()
        self.rxorientation.set(-1)

        # Load the orientation images
        self.rxPinsForwardLabelUpImg = PhotoImage(file="images/rx-orientation/rx-labeluppinsforward.png")
        self.rxPinsForwardLabelDownImg = PhotoImage(file="images/rx-orientation/rx-labeldownpinsforward.png")
        self.rxPinsForwardLabelLeftImg = PhotoImage(file="images/rx-orientation/rx-labelleftpinsforward.png")
        self.rxPinsForwardLabelRightImg = PhotoImage(file="images/rx-orientation/rx-labelrightpinsforward.png")
        self.rxPinsAftLabelUpImg = PhotoImage(file="images/rx-orientation/rx-labeluppinsaft.png")
        self.rxPinsAftLabelDownImg = PhotoImage(file="images/rx-orientation/rx-labeldownpinsaft.png")
        self.rxPinsAftLabelLeftImg = PhotoImage(file="images/rx-orientation/rx-labelleftpinsaft.png")
        self.rxPinsAftLabelRightImg = PhotoImage(file="images/rx-orientation/rx-labelrightpinsaft.png")

        self.rxPinsLeftLabelUpImg = PhotoImage(file="images/rx-orientation/rx-labeluppinsleft.png")

        self.rxOtherImg = PhotoImage(file="images/rx-orientation/rx-other.png")
