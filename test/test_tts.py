from pytest import fixture
from reiz._audio.primitives import Sound
from reiz._audio.tts import Silent_Mixin


@fixture
def msg():
    import reiz.api as reiz

    msg = reiz.audio.Message("test")
    msg.volume = 0
    return msg


@fixture
def silence():
    class Silence(Silent_Mixin, Sound):
        pass

    return Silence()


def test_silence(silence):
    assert silence.duration == 0.1


def test_play_blocking(msg):
    assert msg.volume == 0
    played_time = msg.play_blocking()
    assert played_time == 0
