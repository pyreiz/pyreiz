from pytest import fixture
import reiz


@fixture
def rmarker():
    # set up
    assert reiz.marker.available() is False
    reiz.clock.reset()
    reiz.marker.start()
    assert reiz.clock.now() < 10  # create within 10 secs
    # interrupt
    yield True
    # tear down
    reiz.clock.reset()
    reiz.marker.stop()
    assert reiz.clock.now() < 10  # kill within 10 secs


def test_sanitization(rmarker, capsys):
    assert rmarker
    out, err = capsys.readouterr()
    reiz.marker.push("ä ö ü")
    out, err = capsys.readouterr()
    assert "Sending ae_oe_ue " in out
    out, err = capsys.readouterr()
    reiz.marker.push("ping")
    out, err = capsys.readouterr()
    assert 'Sending {\"msg": "ping"}' in out
    out, err = capsys.readouterr()
    reiz.marker.push("poison-pill")
    out, err = capsys.readouterr()
    assert 'Sending {\"msg": "poison-pill"}' in out

    c = reiz.Canvas((10, 10))

    cue = reiz.Cue(canvas=c,
                   audiostim=reiz.audio.library.beep, visualstim=reiz.visual.library.go,
                   markerstr="test")

    out, err = capsys.readouterr()
    cue.show()
    out, err = capsys.readouterr()
    assert 'Sending test at' in out
