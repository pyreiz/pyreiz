import reiz


def test_beep():
    reiz.audio.Hertz(volume=0, duration_in_ms=100).play()


def test_clock_sleep():
    limit = 1.5 * 10**(-4)  # exact within a millisecond
    desired = 1
    actual = reiz.clock.sleep(desired)
    deviance = abs(desired-actual)
    print(actual)
    assert deviance


def test_clock_sleep_debiased():
    import random
    import time
    limit = 1.5 * 10**(-4)  # exact within a millisecond
    desired = .1
    reiz.clock.reset()
    for i in range(0, 10):
        time.sleep(random.random()*0.05)
        reiz.clock.sleep_debiased(desired)

    actual = reiz.clock.now()
    deviance = abs(1-reiz.clock.now())
    print(actual)
    assert deviance < limit
