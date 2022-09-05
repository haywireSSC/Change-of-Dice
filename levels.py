import pygame as p
import numpy as np
from math import *
from vectors import *
from tileset import *

class dice:
    def __init__(self,root,scale, pos,value):
        self.scale = scale
        self.pos = pos
        self.value = value
        self.sprites = root.sprites['dice'].frames
        self.selectedSprites = root.sprites['currentDice'].frames
        self.current = False

    def draw(self,s):
        if not self.current:
            s.blit(self.sprites[self.value], (self.pos*self.scale).pos)
        else:
            s.blit(self.selectedSprites[self.value], (self.pos*self.scale).pos)

class level:
    def __init__(self,root, size,scale):
        self.root=root
        self.palette = root.palette
        self.scale=scale
        self.specials = {i:dice for i in range(6)}

        self.levels=root.sprites['levels'].frames
        self.level=0
        bitmask = p.image.load('bitmask.png').convert()


        self.autotiles={}
        walls = p.image.load('tileset.png').convert()
        self.autotiles[25] = autotiler(walls, bitmask)

        greenImg = p.image.load('tilesetGreenFilled.png').convert()
        greenOffImg = p.image.load('tilesetGreenEmpty.png').convert()
        self.autotiles[46] = autotiler(greenImg, bitmask)
        self.autotiles[45] = autotiler(greenOffImg, bitmask)

        purpleImg = p.image.load('tilesetPurpleFilled.png').convert()
        purpleOffImg = p.image.load('tilesetPurpleEmpty.png').convert()
        self.autotiles[56] = autotiler(purpleImg, bitmask)
        self.autotiles[57] = autotiler(purpleOffImg, bitmask)

        self.imgs = {i+36:v for i,v in enumerate(root.sprites['numbers'].frames)}
        self.imgs[35] = p.image.load('emptyTile.png').convert()
        spikes = p.image.load('spikes.png').convert()
        spikes.set_colorkey((0,0,0))
        self.imgs[18] = spikes
        self.toggles={56:57, 45:46}
        self.togglesInverted = {value:key for key,value in self.toggles.items()}

        self.reset()

    def reset(self):
        self.root.startTransition()
        if self.level==len(self.levels):
            self.root.win()
            return False
        while len(self.root.dice)>0:
            self.root.dice.pop(0)
        self.grid = self.surfToGrid(self.levels[self.level])
        self.size = vec(self.grid.shape[0], self.grid.shape[1])
        self.surf = p.Surface((self.size*self.scale).pos)
        self.updateAutotile(25)

        self.updateAutotile(46)
        self.updateAutotile(45)
        self.updateAutotile(57)
        self.updateAutotile(56)
        self.renderGrids()
        return True

    def surfToGrid(self,surf):
        grid = np.zeros(surf.get_size(), dtype=np.int8)
        for x in range(surf.get_width()):
            for y in range(surf.get_height()):
                cell = self.palette.toIndex(surf.get_at((x,y)))
                if cell in self.specials:
                    self.root.dice.append(dice(self.root,self.scale, vec(x,y), cell))
                    grid[x][y] = 35#empty
                else:
                    grid[x][y] = cell
        return grid

    def draw(self,s):
        s.blit(self.surf, (0,0))

    def renderGrids(self):
        self.surf.fill(self.palette[1])
        for x in range(self.size.x):
            for y in range(self.size.y):
                cell = self.grid[x][y]
                if cell in self.imgs.keys():
                    self.surf.blit(self.imgs[cell], (self.scale*(x,y)).pos)
        for i in self.autotiles.values():
            i.draw(self.surf)

    def updateAutotile(self,index):
        newgrid = self.grid.copy()
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                newgrid[x][y] = 1 if self.grid[x][y]==index else 0

        self.autotiles[index].setGrid(newgrid)

    def toggle(self,toggle):
        for x in range(self.size.x):
            for y in range(self.size.y):
                cell = self.grid[x][y]
                if cell in list(self.toggles.items())[toggle]:
                    if cell in self.toggles.keys():
                        self.grid[x][y] = self.toggles[cell]
                    elif cell in self.togglesInverted:
                        self.grid[x][y] = self.togglesInverted[cell]
        if toggle==1:
            self.updateAutotile(46)
            self.updateAutotile(45)
            self.autotiles[46].draw(self.surf)
            self.autotiles[45].draw(self.surf)
        else:
            self.updateAutotile(57)
            self.updateAutotile(56)
            self.autotiles[57].draw(self.surf)
            self.autotiles[56].draw(self.surf)
