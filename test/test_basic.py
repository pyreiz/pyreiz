import pytest
import time
from pyglet.window import key
import reiz
import reiz.api


def test_canvas_keypress():
    canvas = reiz.api.Canvas()
    canvas.open()
    assert canvas.start_run == False
    canvas.window.dispatch_event("on_key_press", key.F5, 0)
    canvas.flip()
    assert canvas.start_run == True
    canvas.window.dispatch_event("on_key_press", key.P, 0)
    canvas.flip()
    assert canvas.paused == True
    canvas.window.dispatch_event("on_key_press", key.P, 0)
    canvas.flip()
    assert canvas.paused == False
    canvas.window.dispatch_event("on_key_press", key.ESCAPE, 0)
    canvas.flip()
    assert canvas.available == False


def test_canvas_available(capsys):
    canvas = reiz.api.Canvas(size=(5, 5))
    assert canvas.available == False
    canvas.open()
    assert canvas.available == True
    canvas.close()
    assert canvas.available == False
    canvas.open()
    assert canvas.available == True
    canvas.close()
    canvas.flip()
    out, err = capsys.readouterr()
    assert "Window was closed" in out
    canvas.open()
    del canvas.window
    canvas.flip()
    out, err = capsys.readouterr()
    assert "Window was closed" in out


def test_canvas_properties(capsys):
    w, h = (1, 1)
    canvas = reiz.api.Canvas(size=(w, h))
    canvas.open()
    canvas.clear()
    canvas.get_diag()
    canvas.estimate_fps()
    canvas.set_fullscreen()
    assert h < canvas.height
    assert w < canvas.width
    canvas.set_windowed()
    assert h == canvas.height
    assert w == canvas.width
    canvas.close()
    canvas.show(reiz.visual.library.fixation)
    out, err = capsys.readouterr()
    assert "Window was closed" in out
    canvas.open()


def test_clock_sleep():
    import reiz.api

    limit = 1.5 * 10 ** (-4)  # exact within a millisecond
    desired = 0.1
    actual = reiz.api.clock.sleep(desired)
    deviance = abs(desired - actual)
    assert deviance < limit


def test_clock_sleep_debiased():
    import random
    import time
    import reiz.api

    limit = 1.5 * 10 ** (-4)  # exact within a millisecond
    desired = 0.1
    reiz.api.clock.reset()
    for i in range(1, 11):
        time.sleep(random.random() * 0.05)
        reiz.api.clock.sleep_debiased(desired)
    actual = reiz.api.clock.now()
    deviance = abs(desired * i - actual)
    assert deviance < limit
