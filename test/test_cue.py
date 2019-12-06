import reiz
from pytest import fixture


@fixture
def stimuli(canvas):
    cue = reiz.Cue(
        canvas=canvas,
        audiostim=reiz.audio.library.beep,
        visualstim=reiz.visual.library.go,
    )
    N = reiz.Cue(canvas=canvas, audiostim=None, visualstim=None)
    return cue, N


def test_cue(canvas, stimuli):
    cue, N = stimuli
    reiz.audio.library.beep.volume = 0
    cue.show(0.5)
    N.show(canvas=canvas)
    N.show()
    cue.show(None)


def test_collection(stimuli):
    cue, N = stimuli
    lib = reiz.cue.collect(**{"N": N, "C": cue})
    assert "N" in lib.__dict__
    assert "C" in lib.__dict__
    assert lib.N is N
