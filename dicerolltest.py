class roller:
    def __init__(self,value):
        self.y=[4,5,3,2]
        self.x=[1,5,6,2]
        self.rollTo(value)

    @property
    def current(self): return self.x[1]-1

    def addX(self):
        self.x.insert(-1, self.x.pop(0))
        self.y[1] = self.x[1]
        self.y[-1] = self.x[-1]

    def addY(self):
        self.y.insert(-1, self.y.pop(0))
        self.x[1] = self.y[1]
        self.x[-1] = self.y[-1]

    def minusX(self):
        self.x.insert(0, self.x.pop(-1))
        self.y[1] = self.x[1]
        self.y[-1] = self.x[-1]

    def minusY(self):
        self.y.insert(0, self.y.pop(-1))
        self.x[1] = self.y[1]
        self.x[-1] = self.y[-1]

    def rollTo(self,value):
        if value in self.x:
            while self.x[1]!=value:
                self.addX()
        elif value in self.y:
            while self.y[1]!=value:
                self.addY()
