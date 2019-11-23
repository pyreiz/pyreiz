import reiz
import unittest


class Test_Marker(unittest.TestCase):

    def setUp(self):
        assert reiz.marker.available() is False
        reiz.clock.reset()
        reiz.marker.start()
        assert reiz.clock.now() < 5  # create within 5 secs

    def test_marker_sending(self):
        c = reiz.Canvas((10, 10))
        N = reiz.Cue(canvas=c,
                     audiostim=None,
                     visualstim=None,
                     markerstr="test")
        reiz.audio.library.beep.volume = 0
        c.open()
        N.show(0.05)
        c.close()

    def tearDown(self):
        reiz.clock.reset()
        reiz.marker.stop()
        assert reiz.clock.now() < 5  # ä kill within 5 secs
