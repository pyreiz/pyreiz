from pytest import fixture
import reiz
import logging

logging.basicConfig(level=1)


@fixture
def rmarker(capsys):
    # set up
    assert reiz.marker.available(verbose=True) is False
    out, err = capsys.readouterr()
    assert "is not available" in out
    assert "Connection refused" in out
    reiz.clock.reset()
    reiz.marker.start()
    assert reiz.clock.now() < 10  # create within 10 secs
    # interrupt
    yield True
    # tear down
    reiz.marker.start()
    reiz.clock.sleep(0.5)
    out, err = capsys.readouterr()
    assert "A marker-server is already running" in out

    reiz.clock.reset()
    reiz.marker.stop()
    assert reiz.clock.now() < 10  # kill within 10 secs

    reiz.marker.stop()
    reiz.clock.sleep(0.5)
    out, err = capsys.readouterr()
    assert "No marker-server is currently running" in out


def test_sanitization(rmarker, capsys):
    assert rmarker
    out, err = capsys.readouterr()
    reiz.marker.push("ä ö ü")
    out, err = capsys.readouterr()
    assert "Sending ae_oe_ue " in out
    out, err = capsys.readouterr()
    reiz.marker.push("ping")
    out, err = capsys.readouterr()
    assert 'Sending {"msg": "ping"}' in out
    out, err = capsys.readouterr()
    reiz.marker.push("poison-pill")
    out, err = capsys.readouterr()
    assert 'Sending {"msg": "poison-pill"}' in out

    c = reiz.Canvas((10, 10))
    reiz.audio.library.beep.volume = 0
    cue = reiz.Cue(
        canvas=c,
        audiostim=reiz.audio.library.beep,
        visualstim=reiz.visual.library.go,
        markerstr="test",
    )

    out, err = capsys.readouterr()
    cue.show()
    out, err = capsys.readouterr()
    assert "Sending test at" in out
