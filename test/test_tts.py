from pytest import fixture
import reiz
from reiz._audio.primitives import Sound
from reiz._audio.tts import Silent_Mixin


@fixture
def msg():
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


def test_properties(msg):
    assert msg.volume == 0


def test_play_stop(msg):
    dur = msg.duration
    played_time = msg.play()
    msg.stop()
    assert played_time < dur


def test_play_blocking(msg):
    played_time = msg.play_blocking()
    assert played_time == 0
