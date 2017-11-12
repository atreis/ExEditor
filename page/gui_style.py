class gui_style:
    def getBgColor(self):
        return self.__bgcolor

    def getFgColor(self):
        return self.__fgcolor

    def getCompColor(self):
        return self.__compcolor

    def getAna1Color(self):
        return self.__ana1color

    def getAna2Color(self):
        return self.__ana2color

    def getStyle(self):
        return self.__style

    def __init__(self, style):
        self.__bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        self.__fgcolor = '#000000'  # X11 color: 'black'
        self.__compcolor = '#d9d9d9'  # X11 color: 'gray85'
        self.__ana1color = '#d9d9d9'  # X11 color: 'gray85'
        self.__ana2color = '#d9d9d9'  # X11 color: 'gray85'
        self.__style = style
