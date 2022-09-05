from vectors import *
from math import *
import pygame as p
from levels import *
import utils as ut
from player import *
import asepriteImport as ase
import random
p.init()
p.mixer.init()

class loop():
    def __init__(self,fps=60,scale=0.5,size=vec(256,256)):
        self.fps=fps
        self.clock=p.time.Clock()
        self.scale=scale
        self.size=size
        self.s=p.Surface(size.pos)
        self.screen = p.display.set_mode((size//scale).pos)
        self.quit=False
        self.palette = ut.palette('journey.png')
        ase.generateSheets()
        self.sprites = ase.loadSheets()
        self.dice=[]
        self.overlay=0
        self.music = {
        -1:[p.mixer.Sound('altgametheme.mp3'), p.mixer.Sound('gametheme.mp3')],
        0:[p.mixer.Sound('mainmenu.mp3')],
        1:[p.mixer.Sound('winningtheme.mp3')]
        }
        self.musicIndex=0
        self.musicChannel = self.music[self.overlay][self.musicIndex].play()

        self.swipeNoises = [p.mixer.Sound(f'swipe{i+1}.wav') for i in range(7)]
        self.startTransition()
        self.transitionX = 112

        self.offset=vec()
        self.shake = 0

        self.customEvents = {
        'musicEnd':p.USEREVENT+1
        }
        self.musicChannel.set_endevent(self.customEvents['musicEnd'])

    def win(self):
        self.overlay=1
        self.musicChannel.fadeout(1000)
        #self.music[self.overlay][self.musicIndex].play()


    def events(self):
        for e in p.event.get():
            if e.type == p.QUIT:
                self.quit=True
            elif e.type == p.KEYDOWN:
                if self.overlay==-1:
                    if e.key == p.K_r:
                        self.level.reset()
                        self.player.reset()
                    elif e.key == p.K_q:
                        self.level.level+=1
                        self.level.reset()
                        self.player.reset()
                elif self.overlay==0:
                    if e.key == p.K_RETURN:
                        self.startTransition()
                        self.overlay=-1
                        self.musicChannel.fadeout(1000)
                        self.musicIndex=0
                        #self.music[self.overlay][self.musicIndex].play()
                        self.musicChannel.set_endevent(self.customEvents['musicEnd'])
            elif e.type == self.customEvents['musicEnd']:
                self.musicIndex+=1
                self.musicIndex%=len(self.music[self.overlay])
                self.music[self.overlay][self.musicIndex].play()
                self.musicChannel.set_endevent(self.customEvents['musicEnd'])

    def startTransition(self):
        random.choice(self.swipeNoises).play()
        self.transitionX=-100

    def drawTransition(self):
        target = self.size.x*2
        if self.transitionX<target:
            self.transitionX += (target-self.transitionX)/10
            self.s.blit(self.sprites['overlays'].frames[2], (self.transitionX,0))
            self.s.blit(self.sprites['overlays'].frames[3], (self.transitionX-self.size.x, 0))

    def clear(self):
        self.s.fill(self.palette[1])
        self.screen.fill(self.palette[1])
        self.events()

    def update(self):
        if self.overlay!=-1:
            self.s.blit(self.sprites['overlays'].frames[self.overlay], (0,0))
        else:
            self.player.update()
            self.level.draw(self.s)
            self.player.draw(self.s)
            for e in self.dice:
                e.draw(self.s)

        self.drawTransition()

        if round(self.shake)!=0:
            self.offset = vec(random.uniform(-self.shake,self.shake), random.uniform(-self.shake,self.shake))
            self.shake*=0.9

    def loop(self):
        self.screen.blit(p.transform.scale(self.s, (self.size/self.scale).toInt().pos), self.offset.toInt().pos)
        p.display.update()
        self.clock.tick(self.fps)



loop=loop(size=vec(288,352))

loop.level = level(loop, vec(10,10), vec(16,16))
loop.player = player(loop)
while not loop.quit:
    loop.clear()
    #loop.level.draw(loop.s)
    #loop.player.update()
    #loop.player.draw(loop.s)
    loop.update()
    loop.loop()
