import reiz
import time
# %%

# start the MarkerServer which distributes markerstrings over LSL
reiz.marker.start()

# create a window
canvas = reiz.Canvas()

# initialize Cues
# each Cue reveices information about
# the Window where it will be shown -> canvas
# auditory and visual stimuli, e.g. a tone (Hertz) or text (Mural)
# and a markerstring to be send via LSL when .show() is called
hello = reiz.Cue(canvas,
                 audiostim=reiz.audio.Hertz(
                     frequency=400, duration_in_ms=1000),
                 visualstim=reiz.visual.Mural('Hello World!'),
                 markerstr='hello')

# there is also a library of typical auditory and visual stimuli and
# we can for example, take the visual "los" and the auditory "beep" stimuli
# for convenience, we use the text of the go stimulus as marker message
los = reiz.Cue(canvas,
               audiostim=reiz.audio.library.beep,
               visualstim=reiz.visual.library.go,
               markerstr=reiz.visual.library.go.text)

# here we show a fixation cross but don't want to play an auditory stimulus.
# we can therefore either set it to None or just leave it out (defaults to None)
fix = reiz.Cue(canvas,
               visualstim=reiz.visual.library.fixation,
               markerstr='Fixation')

shape = reiz.Cue(canvas,
                 visualstim=reiz.visual.Trapezoid(xpos=(-.25, -.33, .33, .25),
                                                  ypos=(-.25, .25), color='red'),
                 markerstr='Shape')

# we can also use an iterable for the visual stimuli, and they are overlayed
# from left to right
farewell = reiz.audio.Message("Auf Wiedersehen!")
overlay = reiz.Cue(canvas,
                   audiostim=farewell,
                   visualstim=[reiz.visual.library.logo,                                   reiz.visual.Mural('Good Bye', fontsize=1),
                               ],
                   markerstr='Overlayed')

# we create a named variable for a visual stimulus to allow later updating
# because we will repeatedly call ball.show(), we don't use the markerstr
# as these would be otherwise send everytime we .show()
dynamic_ball = reiz.visual.Circle(zoom=1, color='red')
ball = reiz.Cue(canvas, visualstim=dynamic_ball)

# we open a window, show the cues and close the window again
canvas.open()

# we can either add a sleep function afterwards
fix.show()
time.sleep(1)
# or use the duration parameter. this has the advantage that the window stays
# responsive under Win10 and can e.g. be moved around or resized
hello.show(duration=1)
los.show(duration=1)
shape.show(duration=1)
# we continually update the size of the visualstim of the cue
# because the Cue has a reference to the dynamic_ball, it takes
# over any changes
for i in range(0, 100, 1):
    t0 = time.time()
    # we update the size of the ball
    dynamic_ball.zoom = i/20
    # and show it
    ball.show()
    # if the show duration is slower than the framerate of your graphics card
    # and screen, expect that not all frames can be drawn, i.e. some will be
    # dropped. 60 Hz is ~16ms, so showing the Cue for 50ms  should be fine
    # generally, when you use dynamic cues, e.g. for feedback, consider that
    # there might be a variable amount of time spend for calculation.
    # therefore, it is best practice to wait instead of sleep the remainder of
    # the time
    while (time.time()-t0) < 0.017:
        pass


# we present the cue as long as the audio is playing
overlay.show(duration=farewell.duration)

canvas.close()

reiz.marker.stop()
