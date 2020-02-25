import reiz
from pytest import fixture, raises
from tempfile import TemporaryDirectory, NamedTemporaryFile
import wave
import random
import struct
from pathlib import Path


def test_beep():
    reiz.audio.Hertz(volume=0, duration_in_ms=100).play()


def test_audio_library():
    for item in reiz.audio.library.__dict__.values():
        item.volume = 0
        item.play_blocking()


@fixture
def mock_wavfiles():
    SAMPLE_LEN = 44100
    with TemporaryDirectory() as fld:
        wf = (Path(fld) / "tmp").with_suffix(".wav")
        with wave.open(str(wf), "wb") as wfile:
            wfile.setparams((2, 2, 44100, 0, "NONE", "not compressed"))
            for i in range(0, SAMPLE_LEN):
                value = random.randint(-32767, 32767)
                packed_value = struct.pack("h", value)
                wfile.writeframes(packed_value)
                wfile.writeframes(packed_value)
            wfile.close()
            yield fld, Path(wf.name).stem
        wf.unlink()


def test_read_folder(mock_wavfiles):
    fld, fname = mock_wavfiles
    lib = reiz.audio.read_folder(fld)
    assert fname in lib.__dict__.keys()


def test_noise():
    b = reiz.audio.Noise(100, "brown")
    w = reiz.audio.Noise(100, "white")
    with raises(NotImplementedError):
        reiz.audio.Noise(100, "notimplemented")
