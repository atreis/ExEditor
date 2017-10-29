import json

class RxFile:
    def getData(self):
        return self.data

    def load(self):
        with open(self.filename, 'r') as fin:
            self.data = json.load(fin)

    def save(self):
        self.saveAs(self.filename)

    def saveAs(self, filename):
        with open(filename, 'w') as fout:
            json.dump(self.data, fout, indent=4, sort_keys=False)
        self.filename = filename

    def __init__(self, filename):
        self.filename = filename
        self.data = None
