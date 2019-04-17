# -*- coding: utf-8 -*-
"""
Reiz examples
"""
import reiz
import time
# %%
canvas = reiz.visual.Canvas()

cue = reiz.Cue(canvas, 
               audiostim=reiz.audio.library.button,
               visualstim=reiz.visual.Mural('Hallo Welt!'),
               markerstr='test')

cue = reiz.Cue(canvas, 
               audiostim=reiz.audio.library.button,
               visualstim=reiz.visual.Mural('Hallo Welt!'),
               markerstr='test')

# %%
canvas.open()
canvas.set_fullscreen()
cue.show()
time.sleep(1)
canvas.close()