# -*- coding: utf-8 -*-
"""
resting state
"""

def start(trials=5):
    import reiz
    import time
    # %%
    def count_down():
        for i in range(0,3):
            time.sleep(0.5)
            reiz.audio.library.hint.play()
            
    canvas = reiz.visual.Canvas()

    pre = reiz.Cue(canvas, visualstim=reiz.visual.library.pre)
    post = reiz.Cue(canvas, visualstim=reiz.visual.library.post)
    f5 = reiz.Cue(canvas, visualstim=reiz.visual.Mural('Press F5 to start'))
    augen_auf = reiz.Cue(canvas,
                         audiostim=reiz.audio.library.hint,
                         visualstim=[reiz.visual.Background(color='light'),
                               reiz.visual.library.fixation],
                         markerstr='augen_auf')

    augen_zu = reiz.Cue(canvas,
                         audiostim=reiz.audio.library.relax,
                         visualstim=[reiz.visual.Background(color='light'),
                               reiz.visual.library.fixation],
                         markerstr='augen_zu')
    # %%
    canvas.open()
    #canvas.set_fullscreen()
    while not canvas.start_run:
        f5.show(duration=0.1)
  
    pre.show(duration=3)
    for trl_num in range(trials):
        augen_auf.show(duration=30)
        augen_zu.show(duration=30)    
    post.show(duration=5)
    canvas.close()


if __name__ == '__main__':
    start()
