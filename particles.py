import pygame as p
from math import *
from vectors import *
import random
from dataclasses import dataclass

@dataclass
class particle:
    pos:vec
    size:float
    life:float
    vel:vec
    sprite:p.Surface
    dir:vec

class particleSystem:
    def __init__(self,root):
        self.sprites = root.sprites['confetti'].frames
        self.particles=[]
        self.gravity=0.25
        self.gap=1000
        self.lastEmission=0
        self.burstSize=80

    # def update(self):
    #     if p.time.get_ticks()-self.lastEmission > self.gap:
    #         for i in range(self.burstSize):
    #             self.particles.append(particle(self.pos, 4, 100, vec(random.uniform(-5,5), random.uniform(0,-5)), random.choice(self.sprites)))
    #         self.lastEmission=p.time.get_ticks()

    def burst(self,pos):
        for i in range(self.burstSize):
            self.particles.append(particle(pos, 4, 100, vec(random.uniform(-5,5), random.uniform(0,-5)), random.choice(self.sprites), vec()))

    def draw(self,s):
        for i in range(len(self.particles)-1, -1, -1):
            v=self.particles[i]
            #p.draw.circle(s, (255,0,0), v.pos.pos, v.size)
            s.blit(v.sprite, v.pos.pos)
            v.life-=1
            v.vel.y+=self.gravity
            v.vel.x*=0.95
            v.pos+=v.vel
            if v.life<0:
                self.particles.pop(i)

class starParticles:
    def __init__(self,root):
        self.sprite = p.image.load('star.png').convert()
        self.sprite.set_colorkey((0,0,0))
        self.particles=[]
        self.gravity=0.25
        self.burstSize=20
        self.maxLife=30

    def burst(self,pos):
        self.pos=pos
        for i in range(self.burstSize):
            progress = i/(self.burstSize-1)
            angle = progress*360
            self.particles.append(particle(pos, 4, self.maxLife, vec(random.uniform(-5,5), random.uniform(0,-5)), self.sprite, fromPolar(angle, 1)))

    def draw(self,s):
        for i in range(len(self.particles)-1, -1, -1):
            v=self.particles[i]
            v.sprite.set_alpha((v.life/self.maxLife)*255)
            s.blit(v.sprite, v.pos.pos)
            v.life-=1
            v.pos+= ((self.pos+v.dir*50)-v.pos)/5
            if v.life<0:
                self.particles.pop(i)
