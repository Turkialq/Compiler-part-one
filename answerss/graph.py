class GraphNode:
    def __init__(self, data):
        self.data = data
        self.a = None
        self.b = None

    def getData(self):
        return self.data

    def addData(self, data):
        self.data.append(data)

    def getA(self):
        return self.a

    def addA(self, data):
        self.a = data

    def getB(self):
        return self.b

    def addB(self, data):
        self.b = data
