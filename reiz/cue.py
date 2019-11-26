"""Cues bind stimuli and a marker for synchronous presentation
"""
import reiz.marker as marker
from reiz.time import Clock as _Clock
from types import SimpleNamespace


class Cue():
    """bind stimuli and a marker for synchronous presentation


    This class binds auditory and visual stimuli together with a canvas
    for presentation and sends markers.


    args
    ----

    canvas: :class:`reiz.Canvas`
        a canvas for presentation of the visual stimuli. Create with
    audiostim: :class:`reiz._audio.primitives.Sound`
        a single auditory stimulus to be presented once at the start
        of :meth:`~.show`.
    visualstim: :class:`reiz._visual.complex.Visual`
        a list or a single visual stimulus. Will be presented on the canvas during the whole duration when :meth:`~.show`. was called. If you use more than one visual stimulus, they will be overlayed and are plotted from left to right. That means the first is at the bottom layer, the last at the top.
    markerstr: str
        a string encapsulating the meaning of the cue. This string will be forwarded to the marker-server, and published with LSL. By default,
        strings are sanitized for easier parsing, so do not use case-sensitive
        information, and try to limit yourself to ascii.

    """

    def __init__(self, canvas=None, audiostim=None,
                 visualstim=None, markerstr=None):
        self.canvas = canvas
        self.audio = audiostim
        self.visual = visualstim
        self.marker = markerstr

    def show(self, duration: float = 0, canvas=None, safetime=.2):
        """present all stimuli stored in the cue

        args
        ----
        duration: float
            how many seconds you want to present the visual stimuli on the canvas. Defaults to zero.
            Using zero will result in the function returning immediatly, while
            keeping the visual stimulus maintained on the canvas. In that regard, it resembles presentation forever, (or until another cue is presented). This can confuse Windows 10 if the canvas is moved or resized, as the OS thinks the canvas is `unresponsive`. Any other positive values cause the function to not return and block for the whole duration.
        canvas: :class:`reiz.Canvas`
            In case you decide to present the Cue on a different canvas instead to the one assigned during instantiation. Will be ignored otherwise.
        safetime: float
            continuous presentation causes the canvas to be updated at the flip rate of your screen and grapics cards (usually aroung 60Hz). This hardware limitation means that the duration of presentation
            will be quantizised, i.e. the duration of presentation will be a multiple of 16.6ms for a 60Hz screen. To achieve more accurate duration, the safetime parameters sets how long to the end of the duration we will no longer flip the screen. By default, we won't flip the screen during the last 200ms. This can cause the OS to consider the screen `unresponsive` (see duration above). Please note that this does not improve the timing of the actual drawing on the screen, it just allows the :meth:`~.show` to return at a more accurate time.

        """

        if canvas is not None:
            self.canvas = canvas
        if self.audio is not None:
            self.audio.play()
        if self.marker is not None:
            marker.push(self.marker)

        if duration is not None and self.visual is not None:
            if duration == 0:  # show "forever"
                self.canvas.show(self.visual)
                return 0
            else:  # show for duration
                clk = _Clock()
                dt = clk.now()
                clk.tick()
                self.canvas.show(self.visual)
                while dt <= duration and self.canvas.available:
                    # flipping quantizises the sleep duration, therefore we
                    # don't flip anymore if that would become relevant
                    # we only repeat presentation of the visual stimulus
                    # as audio and markers would be senseless and overlays
                    if abs(duration-dt) > safetime:
                        self.canvas.show(self.visual)
                        clk.sleep_debiased(.1)
                    dt = clk.now()
                return dt


def collect(**lib) -> SimpleNamespace:
    lib = SimpleNamespace(**lib)
    return lib
