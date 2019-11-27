'''Root module for the pyreiz stimulus presentation toolbox
'''


from sys import platform
import pyglet
import reiz.visual as visual
import reiz.audio as audio
import reiz.marker as marker
from reiz.cue import Cue
from reiz._visual._screen import Canvas
from reiz.time import clock, Clock


if platform == 'linux':
    pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')

del pyglet, platform
