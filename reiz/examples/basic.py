import reiz
import time
# %%

# start the MarkerServer which distributes markerstrings over LSL
reiz.marker.start()

# create a window
canvas = reiz.Canvas()

# initialize Cues
hello = reiz.Cue(canvas,
                 audiostim=reiz.audio.Hertz(duration_in_ms=1000),
                 visualstim=reiz.visual.Mural('Hallo Welt!'),
                 markerstr='hello')

los = reiz.Cue(canvas,
               audiostim=reiz.audio.library.los_laut,
               visualstim=reiz.visual.library.los,
               markerstr=reiz.visual.library.los.text)

fix = reiz.Cue(canvas,
               audiostim=None,
               visualstim=reiz.visual.library.fixation,
               markerstr='Fixation')

shape = reiz.Cue(canvas,
                 audiostim=None,
                 visualstim=reiz.visual.Trapezoid(
                     xpos=(-.25, -.33, .17, .66),
                     ypos=(-.25, .25), color='red'),
                 markerstr='Shape')

# open a window, show the cues and close the window again
canvas.open()
fix.show()
time.sleep(1)
hello.show()
time.sleep(1)
los.show()
time.sleep(1)
shape.show()
time.sleep(1)
canvas.close()

reiz.marker.stop()
