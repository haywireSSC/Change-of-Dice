import numpy as np
import pygame as p
from math import *
from vectors import *

class autotiler:
    def __init__(self,tileset,bitmask):
        self.size=vec(16,16)

        tileset.set_colorkey((0,0,0))
        self.tileset = self.loadTileset(tileset, self.size)
        self.bitmask = self.loadTileset(bitmask, vec(3,3))

        self.states = {
        (255,65,125):1,
        (198,216,49):0,
        (0,0,0):'ignore',
        (120,215,255):'skip'
        }

    def setGrid(self,grid):
        self.grid = grid
        self.fancyGrid = np.copy(self.grid)
        self.applyBitmask()

    def findTile(self,grid):
        for i,v in enumerate(self.bitmask):
            valid=True
            for x in range(3):
                for y in range(3):
                    state = self.states[tuple(v.get_at((x,y)))[:3]]
                    if state!='ignore':
                        if state!=grid[x][y]:
                            valid=False
                            break
                else:
                    continue
                break
            if valid:
                return i
        return -1 if grid[1][1]==0 else 16

    def getInnerGrid(self,X,Y):
        return [[self.grid[x+X][y+Y] if ( x+X in range(self.grid.shape[0]) and y+Y in range(self.grid.shape[1])) else 0 for y in range(-1,2,1)] for x in range(-1,2,1)]

    def applyBitmask(self):
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if self.grid[x][y]==1:
                    grid=self.getInnerGrid(x,y)
                    self.fancyGrid[x][y] = self.findTile(self.getInnerGrid(x,y))
                else:
                    self.fancyGrid[x][y] = -1


    def loadTileset(self,img,size):
        tiles=[]
        for x in range(img.get_width()//size.x):
            for y in range(img.get_height()//size.y):
                tiles.append(img.subsurface(p.Rect((vec(x,y)*size).pos, size.pos)))
        return tiles

    def draw(self,s):
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                cell = self.fancyGrid[x][y]
                if cell != -1:
                    s.blit(self.tileset[cell], (vec(x,y)*self.size).pos)

class autotiler2x(autotiler):
    def __init__(self,tilesets,bitmask):
        self.size=vec(16,16)
        for tileset in tilesets:
            tileset.set_colorkey((0,0,0))
        self.tilesets = [self.loadTileset(tileset, self.size) for tileset in tilesets]
        self.bitmask = self.loadTileset(bitmask, vec(3,3))

        self.states = {
        (255,65,125):1,
        (198,216,49):0,
        (0,0,0):'ignore',
        (120,215,255):'skip'
        }

    def setGrid(self,grid):
        self.grid = grid
        self.fancyGrid = np.copy(self.grid)
        self.applyBitmask()

    def draw(self,s,index):
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                cell = self.fancyGrid[x][y]
                if cell != -1:
                    s.blit(self.tilesets[index][cell], (vec(x,y)*self.size).pos)
