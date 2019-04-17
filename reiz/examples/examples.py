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
               markerstr='hello')

prep = reiz.Cue(canvas, 
                audiostim=reiz.audio.library.los_laut,
                visualstim=reiz.visual.library.los,
                markerstr=reiz.visual.library.los.text)
# %%
canvas.open()
canvas.set_fullscreen()
cue.show()
time.sleep(1)
prep.show()
time.sleep(1)
canvas.close()