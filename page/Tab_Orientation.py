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
        Ping left - label up=33,6
        Pins left - label down=33,3
        Pins left - label forward=18,2
        Pins left - label rear=18,7
        
        Pins right - label up=33,5
        Pins right - label down=33,0
        Pins right - label forward=18,4
        Pins right - label rear=18,1
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
            elif self.rxorientation.get() == 9:
                fh.setValue(["data", "system", "axisDirection"], 3)
                fh.setValue(["data", "system", "axis2aircraft"], 33)
                self.rxOrientImage.configure(image=self.rxPinsLeftLabelDownImg)
            elif self.rxorientation.get() == 10:
                fh.setValue(["data", "system", "axisDirection"], 2)
                fh.setValue(["data", "system", "axis2aircraft"], 18)
                self.rxOrientImage.configure(image=self.rxPinsLeftLabelForwardImg)
            elif self.rxorientation.get() == 11:
                fh.setValue(["data", "system", "axisDirection"], 7)
                fh.setValue(["data", "system", "axis2aircraft"], 18)
                self.rxOrientImage.configure(image=self.rxPinsLeftLabelAftImg)
            elif self.rxorientation.get() == 12:
                fh.setValue(["data", "system", "axisDirection"], 5)
                fh.setValue(["data", "system", "axis2aircraft"], 33)
                self.rxOrientImage.configure(image=self.rxPinsRightLabelUpImg)
            elif self.rxorientation.get() == 13:
                fh.setValue(["data", "system", "axisDirection"], 0)
                fh.setValue(["data", "system", "axis2aircraft"], 33)
                self.rxOrientImage.configure(image=self.rxPinsRightLabelDownImg)
            elif self.rxorientation.get() == 14:
                fh.setValue(["data", "system", "axisDirection"], 4)
                fh.setValue(["data", "system", "axis2aircraft"], 18)
                self.rxOrientImage.configure(image=self.rxPinsRightLabelForwardImg)
            elif self.rxorientation.get() == 15:
                fh.setValue(["data", "system", "axisDirection"], 1)
                fh.setValue(["data", "system", "axis2aircraft"], 18)
                self.rxOrientImage.configure(image=self.rxPinsRightLabelAftImg)
            else:
                self.rxOrientImage.configure(image=self.rxOtherImg)
            self.rxeditor.dataChange()

    def __attTrim0ValueChange(self):
        if self.ignorechange:
            return
        fh = self.__getFileHandle()
        atttrim = fh.getValue(["data","model","attTrim"], None)
        try:
            atttrim[0] = int(self.atttrim0.get())
        except:
            # Ignore
            return
        fh.setValue(["data","model","attTrim"], atttrim)

        # Set the text description
        degrees = round(self.atttrim0.get()/100, 2)
        if degrees == 0.0:
            self.rxattlabeldesc0.configure(text=('0 degrees'))
        elif degrees > 0:
            degstr = str(degrees)
            self.rxattlabeldesc0.configure(text=(degstr+' degrees, rx right raised'))
        else:
            degstr = str(-1.0*degrees)
            self.rxattlabeldesc0.configure(text=(degstr+' degrees, rx left raised'))
        self.rxeditor.dataChange()

    def __attTrim1ValueChange(self):
        if self.ignorechange:
            return
        fh = self.__getFileHandle()
        atttrim = fh.getValue(["data","model","attTrim"], None)
        try:
            atttrim[1] = int(self.atttrim1.get())
        except:
            # ignore
            return
        fh.setValue(["data","model","attTrim"], atttrim)

        # Set the text description
        degrees = round(self.atttrim1.get()/100, 2)
        if degrees == 0.0:
            self.rxattlabeldesc1.configure(text=('0 degrees'))
        elif degrees > 0:
            degstr = str(degrees)
            self.rxattlabeldesc1.configure(text=(degstr+' degrees, rx tail raised'))
        else:
            degstr = str(-1.0*degrees)
            self.rxattlabeldesc1.configure(text=(degstr+' degrees, rx nose raised'))
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
            elif axisdir == 3 and axis2 == 33:
                self.rxorientation.set(9)
                self.rxOrientImage.configure(image=self.rxPinsLeftLabelDownImg)
            elif axisdir == 2 and axis2 == 18:
                self.rxorientation.set(10)
                self.rxOrientImage.configure(image=self.rxPinsLeftLabelForwardImg)
            elif axisdir == 7 and axis2 == 18:
                self.rxorientation.set(11)
                self.rxOrientImage.configure(image=self.rxPinsLeftLabelAftImg)
            elif axisdir == 5 and axis2 == 33:
                self.rxorientation.set(12)
                self.rxOrientImage.configure(image=self.rxPinsRightLabelUpImg)
            elif axisdir == 0 and axis2 == 33:
                self.rxorientation.set(13)
                self.rxOrientImage.configure(image=self.rxPinsRightLabelDownImg)
            elif axisdir == 4 and axis2 == 18:
                self.rxorientation.set(14)
                self.rxOrientImage.configure(image=self.rxPinsRightLabelForwardImg)
            elif axisdir == 1 and axis2 == 18:
                self.rxorientation.set(15)
                self.rxOrientImage.configure(image=self.rxPinsRightLabelAftImg)
            else:
                self.rxorientation.set(-1)
                self.rxOrientImage.configure(image=self.rxOtherImg)

            atttrim = fh.getValue(["data","model","attTrim"], None)
            self.atttrim0.set(atttrim[0])
            self.atttrim1.set(atttrim[1])

            # Set the text description
            degrees = round(self.atttrim0.get() / 100, 2)
            if degrees == 0.0:
                self.rxattlabeldesc0.configure(text=('0 degrees'))
            elif degrees > 0:
                degstr = str(degrees)
                self.rxattlabeldesc0.configure(text=(degstr + ' degrees, rx right raised'))
            else:
                degstr = str(-1.0 * degrees)
                self.rxattlabeldesc0.configure(text=(degstr + ' degrees, rx left raised'))
            degrees = round(self.atttrim1.get() / 100, 2)
            if degrees == 0.0:
                self.rxattlabeldesc1.configure(text=('0 degrees'))
            elif degrees > 0:
                degstr = str(degrees)
                self.rxattlabeldesc1.configure(text=(degstr + ' degrees, rx tail raised'))
            else:
                degstr = str(-1.0 * degrees)
                self.rxattlabeldesc1.configure(text=(degstr + ' degrees, rx nose raised'))

            self.ignorechange = False
        except:
            self.rxorientation.set(-1)
            self.ignorechange = False

    def draw(self):
        self.notebook_orientation = ttk.Frame(self.notebook)
        self.notebook.add(self.notebook_orientation, padding=3)
        self.notebook.tab(self.tab_num, text="Orientation",underline="-1",)

        self.rxorientframe = ttk.Labelframe(self.notebook_orientation)
        self.rxorientframe.place(x=5, y=5, height=430, width=500)
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
        self.rxPinsLeftLabelDown = ttk.Radiobutton(self.rxorientframe, text='Pins Left, Label Down', variable=rxorientation, value=9, command=lambda:self.__rxOrientationChange())
        self.rxPinsLeftLabelForward = ttk.Radiobutton(self.rxorientframe, text='Pins Left, Label Towards Nose', variable=rxorientation, value=10, command=lambda:self.__rxOrientationChange())
        self.rxPinsLeftLabelAft = ttk.Radiobutton(self.rxorientframe, text='Pins Left, Label Towards Tail', variable=rxorientation, value=11, command=lambda:self.__rxOrientationChange())
        self.rxPinsRightLabelUp = ttk.Radiobutton(self.rxorientframe, text='Pins Right, Label Up', variable=rxorientation, value=12, command=lambda:self.__rxOrientationChange())
        self.rxPinsRightLabelDown = ttk.Radiobutton(self.rxorientframe, text='Pins Right, Label Down', variable=rxorientation, value=13, command=lambda:self.__rxOrientationChange())
        self.rxPinsRightLabelForward = ttk.Radiobutton(self.rxorientframe, text='Pins Right, Label Towards Nose', variable=rxorientation, value=14, command=lambda:self.__rxOrientationChange())
        self.rxPinsRightLabelAft = ttk.Radiobutton(self.rxorientframe, text='Pins Right, Label Towards Tail', variable=rxorientation, value=15, command=lambda:self.__rxOrientationChange())

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
        self.rxPinsLeftLabelDown.place(x=5, y=210, width=230, height=25)
        self.rxPinsLeftLabelForward.place(x=5, y=231, width=230, height=25)
        self.rxPinsLeftLabelAft.place(x=5, y=252, width=230, height=25)
        self.rxPinsRightLabelUp.place(x=5, y=273, width=230, height=25)
        self.rxPinsRightLabelDown.place(x=5, y=294, width=230, height=25)
        self.rxPinsRightLabelForward.place(x=5, y=315, width=230, height=25)
        self.rxPinsRightLabelAft.place(x=5, y=336, width=230, height=25)

        self.rxOrientOther.place(x=5, y=378, width=230, height=25)

        # rx orientation image
        self.rxOrientImage = ttk.Label(self.rxorientframe)
        self.rxOrientImage.place(x=240, y=0, width=250, height=250)
        self.rxOrientImage.configure(image = self.rxOtherImg)
        self.rxOrientImage.configure(relief=SUNKEN)

        # ------------------------------ attTrim settings
        self.rxattframe = ttk.Labelframe(self.notebook_orientation)
        self.rxattframe.place(x=510, y=5, height=90, width=300)
        self.rxattframe.configure(relief=SUNKEN)
        self.rxattframe.configure(text='''Receiver Trim''')
        self.rxattframe.configure(borderwidth="2")
        self.rxattframe.configure(relief=SUNKEN)

        atttrim0 = self.atttrim0
        atttrim1 = self.atttrim1

        self.rxattlabel = ttk.Label(self.rxattframe)
        self.rxattlabel.place(x=5, y=0, width=150, height=21)
        self.rxattlabel.configure(text = 'Attitude Trim')

        self.rxattlabel0 = ttk.Label(self.rxattframe)
        self.rxattlabel0.place(x=5, y=21, width=50, height=25)
        self.rxattlabel0.configure(text = 'Aileron: ')

        self.rxattentry0 = Entry(self.rxattframe)
        self.rxattentry0.place(x=55, y=21, height=21, width=50)
        self.rxattentry0.configure(background="white")
        self.rxattentry0.configure(disabledforeground="#a3a3a3")
        self.rxattentry0.configure(font="TkFixedFont")
        self.rxattentry0.configure(foreground="#000000")
        self.rxattentry0.configure(highlightbackground="#d9d9d9")
        self.rxattentry0.configure(highlightcolor="black")
        self.rxattentry0.configure(insertbackground="black")
        self.rxattentry0.configure(selectbackground="#c4c4c4")
        self.rxattentry0.configure(selectforeground="black")
        self.rxattentry0.configure(textvariable=atttrim0)
        atttrim0.trace("w", lambda name, index, mode, atttrim0=atttrim0: self.__attTrim0ValueChange())

        self.rxattlabel1 = ttk.Label(self.rxattframe)
        self.rxattlabel1.place(x=5, y=42, width=50, height=25)
        self.rxattlabel1.configure(text = 'Elevator: ')

        self.rxattentry1 = Entry(self.rxattframe)
        self.rxattentry1.place(x=55, y=42, height=21, width=50)
        self.rxattentry1.configure(background="white")
        self.rxattentry1.configure(disabledforeground="#a3a3a3")
        self.rxattentry1.configure(font="TkFixedFont")
        self.rxattentry1.configure(foreground="#000000")
        self.rxattentry1.configure(highlightbackground="#d9d9d9")
        self.rxattentry1.configure(highlightcolor="black")
        self.rxattentry1.configure(insertbackground="black")
        self.rxattentry1.configure(selectbackground="#c4c4c4")
        self.rxattentry1.configure(selectforeground="black")
        self.rxattentry1.configure(textvariable=atttrim1)
        atttrim1.trace("w", lambda name, index, mode, atttrim1=atttrim1: self.__attTrim1ValueChange())

        self.rxattlabeldesc0 = ttk.Label(self.rxattframe)
        self.rxattlabeldesc0.place(x=110, y=21, width=160, height=25)
        self.rxattlabeldesc0.configure(text = '0 degrees')

        self.rxattlabeldesc1 = ttk.Label(self.rxattframe)
        self.rxattlabeldesc1.place(x=110, y=42, width=160, height=25)
        self.rxattlabeldesc1.configure(text = '0 degrees')

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
        self.rxorientation = IntVar()
        self.rxorientation.set(-1)
        self.atttrim0 = IntVar()
        self.atttrim0.set(0)
        self.atttrim1 = IntVar()
        self.atttrim1.set(0)
        self.axistrim0 = IntVar()
        self.axistrim0.set(-1)
        self.axistrim1 = IntVar()
        self.axistrim1.set(-1)
        self.axistrim2 = IntVar()
        self.axistrim2.set(-1)

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
        self.rxPinsLeftLabelDownImg = PhotoImage(file="images/rx-orientation/rx-labeldownpinsleft.png")
        self.rxPinsLeftLabelForwardImg = PhotoImage(file="images/rx-orientation/rx-labelforwardpinsleft.png")
        self.rxPinsLeftLabelAftImg = PhotoImage(file="images/rx-orientation/rx-labelaftpinsleft.png")
        self.rxPinsRightLabelUpImg = PhotoImage(file="images/rx-orientation/rx-labeluppinsright.png")
        self.rxPinsRightLabelDownImg = PhotoImage(file="images/rx-orientation/rx-labeldownpinsright.png")
        self.rxPinsRightLabelForwardImg = PhotoImage(file="images/rx-orientation/rx-labelforwardpinsright.png")
        self.rxPinsRightLabelAftImg = PhotoImage(file="images/rx-orientation/rx-labelaftpinsright.png")

        self.rxOtherImg = PhotoImage(file="images/rx-orientation/rx-other.png")
