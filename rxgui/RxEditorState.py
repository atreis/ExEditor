class State:
    def setFileHandle(self, fh):
        self.fh = fh

    def getFileHandle(self):
        return self.fh

    def clearFileHandle(self):
        self.fh = None

    def __init__(self):
        self.fh = None
