import reiz


def test_beep():
    reiz.audio.Hertz(volume=0, duration_in_ms=100).play()


def test_audio_library():
    for item in reiz.audio.library.__dict__.values():
        item.volume = 0
        item.play_blocking()
