#pyreiz

pyReiz is a low-level auditory and visual stimulus presentation suite wrapping
pyglet, sending markers via a pylsl outlet.

It comes with a library of default visual and auditory cues. They can be found in
reiz.visual.library and reiz.audio.library

### Libraries

The visual library is filled based on the images files and the ini file in /media/img.
All images are aggregated, with their filename as key. The ini-file is being 
parsed. The section title defines the type of the visual stimulus (e.g. Mural or Cross...), the key will be the key for the library and the following json value
will be exploded as keyword arguments in the creation of respective visual object.


The auditory library is filled based on the auditory files in /media/wav. All images are aggregated, with their filename as key.

This allows a global configuration of your stimuli library.

### Example of Cue construction and presentation

A cue usually consists of at least a visual stimulus and an auditory stimulus. This can be selected from the library or constructed on the fly. Additionally, a marker string is useful. Any visual stimulation requires information about which canvas it should be shown on. This can be given during object creation ```cue = Cue(canvas=canvas)``` or set at any later time ```cue.show(canvas=other_canvas)```

For example:

```
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
               visualstim=reiz.visual.library.fixation,
               markerstr='Fixation')

canvas.open()
canvas.set_fullscreen()
fix.show()
time.sleep(1)
hello.show()
time.sleep(1)
los.show()
time.sleep(1)
rate.show()
time.sleep(1)
canvas.close()

```

If you want a cue that does not send a marker, show a visual stimulus or play 
an audio for any reason, just omit the respective argument or set it to None.

### Recording

Because all markers are send via lsl, i suggest recording with Labrecorder from
https://github.com/labstreaminglayer/App-LabRecorder/releases Use at least 1.13,
as this version supports BIDS-conform recording, offers a remote interface and
has a critical timing bugfix included.

### Acknowledgment

I used code from Cocos2d at https://github.com/los-cocos/cocos for generation
of the openGL primitives. 


