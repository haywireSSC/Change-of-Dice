from pathlib import Path
from os import system
from json import load
import pygame as p


path=Path('assets')

def generateSheets():
    files = [i.with_suffix('') for i in path.glob('*.aseprite')]
    for file in files:
        system(f"aseprite -b {file}.aseprite --sheet {file}.png --data {file}.json --format json-array --list-tags")

def loadSheet(name):
    with open(path / f'{name}.json', 'r') as f:
        data = load(f)
    img = p.image.load(path / f'{name}.png').convert()
    frames=[]
    durations=[]
    x,y=0,0
    for frame in data['frames']:
        rect=frame['frame']
        surf=img.subsurface((rect['x'],rect['y'],rect['w'],rect['h'])).convert()
        surf.set_colorkey((0,0,0))
        frames.append(surf)
        durations.append(frame['duration'])
    anims={i['name']:(i['from'],i['to']) for i in data['meta']['frameTags']}

    return sprite(frames, durations, anims)

def loadSheets():
    files = [i.stem for i in path.glob('*.aseprite')]
    sprites={}
    for name in files:
        sprites[name] = loadSheet(name)
    return sprites


class sprite:
    def __init__(self, frames, durations, anims):
        self.frames, self.durations, self.anims = frames, durations, anims
