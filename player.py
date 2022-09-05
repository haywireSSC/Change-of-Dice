import pygame as p
from math import *
from vectors import *
import utils as ut
import random
import particles as par

class roller:
    def __init__(self,value):
        self.y=[3,4,2,1]
        self.x=[0,4,5,1]
        self.rollTo(value)

    @property
    def current(self): return self.x[1]

    def addX(self):
        self.x.append(self.x.pop(0))
        self.y[1] = self.x[1]
        self.y[-1] = self.x[-1]

    def addY(self):
        self.y.append(self.y.pop(0))
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

    def rollVec(self,pos):
        if pos.x>0:
            self.addX()
        elif pos.x<0:
            self.minusX()

        if pos.y>0:
            self.addY()
        elif pos.y<0:
            self.minusY()

    def rollVecCopy(self,pos):
        if pos.x!=0:
            return self.x[1+pos.x]
        elif pos.y!=0:
            return self.y[1+pos.y]
        else:
            return self.current


    def rollTo(self,value):
        if value in self.x:
            while self.x[1]!=value:
                self.addX()
        elif value in self.y:
            while self.y[1]!=value:
                self.addY()

class trail:
    def __init__(self,pos,duration,sprite, brightness=0):
        self.pos=pos
        self.sprite=sprite.copy()

        self.duration = duration
        self.startTime = p.time.get_ticks()

    def draw(self,s):
        progress = (p.time.get_ticks()-self.startTime)/self.duration + 0.5

        if progress>1:
            return False

        self.sprite.set_alpha(255*(1-progress))
        s.blit(self.sprite, self.pos.pos)
        return True

class player:
    def __init__(self,root):
        self.dice=root.dice
        self.clock=root.clock
        self.level = root.level
        self.root=root
        self.pos=vec()
        self.prevArrows=vec()
        self.sprites = root.sprites['dice'].frames
        self.altSprites = root.sprites['currentDice'].frames
        self.uiBack = p.image.load('diceui.png').convert()
        self.uiBack.set_colorkey((0,0,0))
        self.reset()
        self.prevSpace = False

        self.empty=[35,57,45,18,32]

        #self.noises=[p.mixer.Sound(f'dice_tap_{i+1}.mp3') for i in range(6)]
        self.noises=[p.mixer.Sound(f'dice{i+1}.wav') for i in range(3)]
        for i in self.noises:
            i.set_volume(0.5)

        self.switchNoise = p.mixer.Sound('dice_roll_1.mp3')
        self.winNoise = p.mixer.Sound('win.wav')

        self.trail=[]

        self.particles=par.particleSystem(root)
        self.starParticles=par.starParticles(root)

    def draw(self,s):
        count=0
        for i in range(len(self.trail)):
            if not self.trail[count].draw(s):
                self.trail.pop(count)
                count-=1
            count+=1

        # offset=vec(0,s.get_height()-self.uiBack.get_height())
        # s.blit(self.uiBack, offset.pos)
        # offset+=self.level.scale+(1,1)
        # s.blit(self.sprites[self.roller.x[1]], offset.pos)
        # s.blit(self.sprites[self.roller.y[0]], vec(offset.x, offset.y-self.level.scale.y).pos)
        # s.blit(self.sprites[self.roller.y[2]], vec(offset.x, offset.y+self.level.scale.y).pos)
        #
        # s.blit(self.sprites[self.roller.x[0]], vec(offset.x-self.level.scale.y, offset.y).pos)
        # s.blit(self.sprites[self.roller.x[2]], vec(offset.x+self.level.scale.y, offset.y).pos)

        self.particles.draw(s)
        self.starParticles.draw(s)

    def reset(self):
        self.prev = []
        self.die=None
        self.swap()

        #self.roller=roller(self.die.value)

    def addtrail(self,pos):
        self.trail.append(trail(pos*self.level.scale, 1000,self.sprites[self.die.value]))

    def addtrailLine(self,start,end):
        gap=1
        delta=end-start
        count=0
        while (count+1)*gap < delta.mag:
            count+=1
            self.trail.append(trail((start+delta.normalized*count*gap)*self.level.scale, 15*count,self.sprites[self.die.value]))

    def update(self):
        if self.die:
            arrows = ut.arrows()

            k=p.key.get_pressed()
            if k[p.K_SPACE] and not self.prevSpace:
                self.prevPos=self.pos.copy()
                if self.swap():
                    self.starParticles.burst(self.pos*self.level.scale)
                    self.root.shake = 5
                    self.addtrailLine(self.prevPos,self.pos)
                    self.switchNoise.play()
                    self.level.toggle(1)

            self.prevSpace=k[p.K_SPACE]


            if arrows != self.prevArrows:
                self.pos+=arrows
                self.pos%=self.level.size
                cell=self.level.grid[self.pos.x][self.pos.y]
                if (cell not in self.empty or True in [e.pos==self.pos for e in self.dice]) and not cell-36 == (self.die.value+1)%6:
                    self.pos-=arrows
                else:
                    if cell==18:
                        self.level.reset()
                        self.reset()
                    elif cell==32:
                        self.particles.burst(self.pos*self.level.scale)
                        self.root.shake = 10
                        self.winNoise.play()
                        self.dice.remove(self.die)
                        if len(self.dice)==0:
                            self.level.level+=1
                            if self.level.reset():
                                self.reset()
                        else:
                            self.reset()
                    else:
                        self.addtrail(self.pos-arrows)
                        random.choice(self.noises).play()
                        self.level.toggle(0)
                        self.die.value +=1
                        self.die.value %= 6


            self.prevArrows = arrows

            self.die.pos=self.pos.copy()

    def swap(self):
        swap = self.swapLower()
        if not swap:
            self.prev=[]
            swap = self.swapLower()
        return swap

    def swapLower(self):
        for e in self.dice:
            if e.value==self.die.value and not e in self.prev and not e == self.die if self.die else True:
                if self.die:
                    self.die.current=False
                self.die=e
                self.die.current=True
                self.pos=self.die.pos.copy()
                self.prev.append(self.die)
                return True
        return False
