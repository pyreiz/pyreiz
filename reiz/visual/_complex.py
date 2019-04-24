# -*- coding: utf-8 -*-
"""
Pyglet based api to shapes and murals
    
"""
import pyglet            
from ._primitives import Polygon as _Polygon
from ._primitives import Circle as _Circle
from typing import Tuple
# %%
COLORS = {
        "red": [0.9, 0.1, 0.1],
        "pink": [0.9, 0.5, 0.9],
        "green": [.25, .8, .25],
        "blue": [0, 0, 1],
        "white": [1, 1, 1],
        "black": [0, 0, 0],        
        "gray": [0.25, 0.25, 0.25],
        "light": [0.5, 0.5, 0.5],
        "dark": [0.1, 0.1, 0.1],
        }  #: A dictionary of color strings encoding a tuple in RGB
        
# %% Complex

class Mural():
    
    def __init__(self, text:str='Hello World', font='Times New Roman', 
                 fontsize=36, position:Tuple[float, float]=(0,0)):
        self.text = text
        self.font = font
        self.fontsize = fontsize
        self.pos = position
        
    def adapt(self, window):
        x0 = window.width//2
        y0 = window.height//2        
        y = (y0*self.pos[0]) + y0
        x = (x0*self.pos[1]) + x0
        
        self.label = pyglet.text.Label(self.text, font_name=self.font, 
                           font_size=self.fontsize,
                           x=x, y=y,
                           anchor_x='center', anchor_y='center')
    
    def draw(self):
        self.label.draw()

    def __repr__(self):
        return f"Mural('{self.text}')"


class Circle():
    
    def __init__(self, zoom=1, color='red', position:Tuple[float, float]=(0,0)):
        self.pos = position
        if type(color) is tuple or type(color) is list:
            self.color = color
        elif type(color) is str:
            self.color = COLORS[color].copy()
        self.color.append(1)        
        self.zoom = zoom
        
    
    def adapt(self, window):
        x0 = window.width//2
        y0 = window.height//2
        width = int(0.1*min([window.height, window.width]) * self.zoom)
        
        y = (y0*self.pos[0]) + y0
        x = (x0*self.pos[1]) + x0
        self.drawing = _Circle(x=x, y=y, z=0, width=width, color=self.color) 
        
    def draw(self):
        self.drawing.render()
        
    def __repr__(self):
        return (f"Circle(zoom={self.zoom}, color={self.color}, " +
               f"position={self.pos})")

class Cross():
    
    def __init__(self, zoom=1, color='white'):
        try:
            self.color = COLORS[color]
        except KeyError:
            self.color = color
        self.zoom = zoom
        
    def adapt(self, window):        
        x0 = window.width//2
        y0 = window.height//2
        armlen = int(self.zoom * 100)
        armwid = int(self.zoom * 15)
        
        y1 = y0-armlen
        y2 = y0-armwid
        y3 = y0+armwid                
        y4 = y0+armlen
        
        x1 = x0-armlen        
        x2 = x0-armwid        
        x3 = x0+armwid        
        x4 = x0+armlen            
    
        v = [(x1, y2), (x1, y3), (x4, y3), (x4, y2)]                 
        self.ho = _Polygon(v=v, z=0, color=(*self.color,1), stroke=0, rotation=0)
        v = [(x2, y1), (x2, y4), (x3, y4), (x3, y1)]                 
        self.ve = _Polygon(v=v, z=0, color=(*self.color,1), stroke=0, rotation=0)        
    
    def draw(self):
        self.ho.render()
        self.ve.render()

    def __repr__(self):
        return f"Cross(zoom='{self.zoom}', color={self.color})"


# %% File-based classes
class Image():
    
    def __init__(self, imgpath:str):
        self.imgpath = imgpath
        self.img = pyglet.image.load(imgpath)
        
    def adapt(self, window):        
        x0 = window.width//2 - self.img.width//2
        y0 = window.height//2 - self.img.height//2
        self.sprite = pyglet.sprite.Sprite(img=self.img, x=x0, y=y0,
                                           usage='static')
    
    def draw(self):
        self.sprite.draw()
        
    def __repr__(self):
        return f"Image(imgpath='{self.imgpath}')"
        
