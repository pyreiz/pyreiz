# -*- coding: utf-8 -*-
"""
Dynamic reiz examples
"""

if __name__ == '__main__':
    import reiz
    import time
    # %%
    left_ball = reiz.visual.Circle(zoom=1, color='blue', position=(0, -0.25))
    right_ball = reiz.visual.Circle(zoom=1, color='red', position=(0, 0.25))
    canvas = reiz.visual.Canvas()
    ball = reiz.Cue(canvas,
                   audiostim=None,
                   visualstim=[left_ball, right_ball],
                   markerstr='Circle')

    # %%
    canvas.open()
    #canvas.set_fullscreen()
    for i in range(0, 100, 1):
        left_ball.zoom = i/20
        ball.show()    
        right_ball.zoom = 5 - i/20
        ball.show()
        time.sleep(.05)
    for i in range(0, 100, 1):
        left_ball.zoom = 5 - i/20
        right_ball.zoom = i/20
        ball.show()
        time.sleep(.05)
    canvas.close()
