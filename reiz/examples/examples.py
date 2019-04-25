# -*- coding: utf-8 -*-
"""
Reiz examples
"""
import reiz
import time
# %%
canvas = reiz.visual.Canvas()

hello = reiz.Cue(canvas, 
               audiostim=reiz.audio.library.button,
               visualstim=reiz.visual.Mural('Hallo Welt!'),
               markerstr='hello')

los = reiz.Cue(canvas, 
                audiostim=reiz.audio.library.los_laut,
                visualstim=reiz.visual.library.los,
                markerstr=reiz.visual.library.los.text)

rate = reiz.Cue(canvas, 
                audiostim=reiz.audio.Hertz(duration_in_ms=1000),
                visualstim=reiz.visual.library.rating,
                markerstr=reiz.visual.library.rating.text)

fix = reiz.Cue(canvas,
               audiostim=None,
               visualstim=[reiz.visual.Background(color='light'),
                           reiz.visual.library.fixation],
               markerstr='Fixation')

ball = reiz.Cue(canvas,
               audiostim=None,
               visualstim=[reiz.visual.Circle(zoom=1, color='red', position=(0.25, 0)),
                           reiz.visual.Circle(zoom=1, color='blue', position=(-.25, 0)),
                           reiz.visual.Mural('Two Balls!', position=(0, .5))],
               markerstr='Circle')

line = reiz.Cue(canvas, 
                visualstim=[reiz.visual.Line(a=(0,0), b=(-1, -1), color='red'),
                            reiz.visual.Polygon(positions=[(0,0),(0,.5),(.5,0)], color='red')]
                )
# %%
canvas.open()
#canvas.set_fullscreen()
line.show()
time.sleep(1)
# %%
ball.show()
time.sleep(1)
fix.show()
time.sleep(1)
hello.show()
time.sleep(1)
los.show()
time.sleep(1)
rate.show()
time.sleep(1)
canvas.close()