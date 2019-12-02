import reiz
from pytest import fixture


@fixture
def stimuli():
    c = reiz.Canvas((10, 10))
    cue = reiz.Cue(canvas=c,
                   audiostim=reiz.audio.library.beep,  visualstim=reiz.visual.library.go)
    N = reiz.Cue(canvas=c,
                 audiostim=None,
                 visualstim=None)
    return c, cue, N


def test_cue(stimuli):
    c, cue, N = stimuli
    reiz.audio.library.beep.volume = 0
    c.open()
    cue.show(0.5)
    N.show(canvas=c)
    N.show()
    cue.show(None)
    c.close()


def test_collection(stimuli):
    c, cue, N = stimuli
    lib = reiz.cue.collect(**{"N": N, "C": cue})
    assert "N" in lib.__dict__
    assert "C" in lib.__dict__
    assert lib.N is N
