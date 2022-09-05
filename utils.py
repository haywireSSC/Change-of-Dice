from vectors import *
import pygame as p
from math import *

def arrows():
    arrows=vec(0,0)
    k=p.key.get_pressed()
    if k[p.K_RIGHT] or k[p.K_d] or k[p.K_l]:
        arrows.x+=1
    elif k[p.K_LEFT] or k[p.K_a] or k[p.K_h]:
        arrows.x-=1
    elif k[p.K_UP] or k[p.K_w] or k[p.K_k]:
        arrows.y-=1
    elif k[p.K_DOWN] or k[p.K_s] or k[p.K_j]:
        arrows.y+=1
    return arrows

class palette:
    def __init__(self,path):
        self.surf = p.image.load(path).convert()
    def __getitem__(self,key):
        return self.surf.get_at((key,0))

    def toIndex(self,colour):
        for x in range(self.surf.get_width()):
            if self.surf.get_at((x,0)) == colour:
                return x
        return False
