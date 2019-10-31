'''Root module for the pyreiz stimulus presentation toolbox
'''
from reiz.time import clock
from reiz._visual._screen import Canvas
from reiz.cue import Cue
import reiz.marker as marker
import reiz.audio as audio
import reiz.visual as visual
import pyglet
from sys import platform
if platform == 'linux':
    pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')
del pyglet, platform
# %%
