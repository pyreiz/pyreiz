import reiz


def test_canvas_keypress():
    from pyglet.window import key
    canvas = reiz.Canvas()
    canvas.open()
    assert canvas.start_run == False
    canvas.window.dispatch_event('on_key_press', key.F5, 0)
    canvas.flip()
    assert canvas.start_run == True
    canvas.close()


def test_canvas_available():
    canvas = reiz.Canvas(size=(5, 5))
    assert canvas.available == False
    canvas.open()
    assert canvas.available == True
    canvas.close()
    assert canvas.available == False


def test_canvas_properties():
    w, h = (10, 9)
    canvas = reiz.Canvas(size=(w, h))
    canvas.open()
    canvas.clear()
    canvas.get_diag()
    canvas.estimate_fps()
    assert h == canvas.height
    assert w == canvas.width
    canvas.close()


def test_clock_sleep():
    limit = 1.5 * 10**(-4)  # exact within a millisecond
    desired = .1
    actual = reiz.clock.sleep(desired)
    deviance = abs(desired-actual)
    assert deviance < limit


def test_clock_sleep_debiased():
    import random
    import time
    limit = 1.5 * 10**(-4)  # exact within a millisecond
    desired = .1
    reiz.clock.reset()
    for i in range(1, 11):
        time.sleep(random.random()*0.05)
        reiz.clock.sleep_debiased(desired)
    actual = reiz.clock.now()
    deviance = abs(desired*i-actual)
    assert deviance < limit
