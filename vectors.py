from math import *
import random

def fromPolar(angle,mag):
    angle=radians(angle)
    return vec(sin(angle)*mag,cos(angle)*mag)

def toVec(pos):
    if type(pos)==vec:
        return pos
    elif type(pos)==float or type(pos)==int:
        return vec(pos,pos)
    else:
        return vec(pos[0],pos[1])

def randomVec(min,max):
    return vec(random.uniform(min,max), random.uniform(min,max))

class vec():
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y

    @property
    def pos(self): return (self.x,self.y)
    @pos.setter
    def pos(self,newpos): self.x,self.y = newpos

    @property
    def mag(self): return hypot(self.x,self.y)
    @mag.setter
    def mag(self,newmag): self.x,self.y = (self.normalized*newmag).pos

    @property
    def angle(self): return 90-degrees(atan2(self.y,self.x))
    @angle.setter
    def angle(self,newangle): self.x,self.y=fromPolar(newangle, self.mag).pos
    @property
    def normalized(self):
        try:
            return vec(self.x/self.mag, self.y/self.mag)
        except ZeroDivisionError:
            return vec()

    def rotateTo(self,newangle):
        return fromPolar(newangle, self.mag)


    def copy(self):
        return vec(self.x,self.y)

    def toInt(self):
        return vec(int(self.x),int(self.y))

    def angleTo(self,pos):
        pos=toVec(pos)
        return 90-degrees(atan2(pos.y-self.y,pos.x-self.x))

    def distanceTo(self,pos):
        pos=toVec(pos)
        return hypot(pos.x-self.x,pos.y-self.y)

    def __eq__(self,other):
        return toVec(other).pos == self.pos

    def __add__(self,pos):
        pos=toVec(pos)
        return vec(self.x+pos.x, self.y+pos.y)

    def __sub__(self,pos):
        pos=toVec(pos)
        return vec(self.x-pos.x, self.y-pos.y)

    def __mul__(self,pos):
        pos=toVec(pos)
        return vec(self.x*pos.x, self.y*pos.y)

    def __truediv__(self,pos):
        pos=toVec(pos)
        return vec(self.x/pos.x, self.y/pos.y)

    def __floordiv__(self,pos):
        pos=toVec(pos)
        return vec(int(self.x//pos.x), int(self.y//pos.y))

    def __mod__(self,pos):
        pos=toVec(pos)
        return vec(self.x%pos.x, self.y%pos.y)
