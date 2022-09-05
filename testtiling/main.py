from vectors import *
from math import *
import pygame as p
from tileset import *
p.init()

class loop():
    def __init__(self,fps=60,scale=2,bg=(0,0,0),size=vec(256,256)):
        self.fps=fps
        self.clock=p.time.Clock()
        self.bg=bg
        self.scale=scale
        self.size=size
        self.screenSize=size*scale
        self.s=p.Surface(size.pos)
        self.screen = p.display.set_mode(self.screenSize.pos)
        self.quit=False

    def arrows(self):
        arrows=vec()
        k=p.key.get_pressed()
        if k[K_RIGHT]:
            arrows.x+=1
        if k[K_LEFT]:
            arrows.x-=1
        if k[K_UP]:
            arrows.y+=1
        if k[K_DOWN]:
            arrows.y-=1
        return arrows


    def events(self):
        for e in p.event.get():
            if e.type == p.QUIT:
                self.quit=True

    def clear(self):
        self.s.fill(self.bg)
        self.events()

    def loop(self):
        self.screen.blit(p.transform.scale(self.s, self.screenSize.pos), (0,0))
        p.display.update()
        self.clock.tick(self.fps)


loop=loop(bg=(255,255,255))
tileset = autotiler()
while not loop.quit:
    loop.clear()
    tileset.draw(loop.s)
    loop.loop()
