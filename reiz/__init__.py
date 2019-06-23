'''Root module for the pyreiz stimulus presentation toolbox
'''
import pyglet
from sys import platform
if platform == 'linux':
    pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')
del pyglet, platform
#%%
import reiz.visual as visual
import reiz.audio as audio
import reiz.marker as marker
from reiz.time import clock 
from reiz.cue import Cue
from reiz.visual._screen import Canvas
