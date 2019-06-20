# -*- coding: utf-8 -*-
"""Repeat runs at will
"""
from collections import Counter
def start(trials=5):
    import reiz
    import time
    # %%
    def count_down():
        for i in range(0,3):
            time.sleep(0.5)
            reiz.audio.library.hint.play()
            
    def generate_info(counter):
        run_num = counter["runs"]
        trl_num = counter["trials"]
        tlr_goal = run_num*trials
        visual = reiz.visual.Mural(text=f'{run_num}: {trl_num} / {tlr_goal}',
                                   position=(-.9, .9),
                                   fontsize=.3)
        return visual
     
    counter = Counter()
    canvas = reiz.visual.Canvas()

    pre = reiz.Cue(canvas, visualstim=reiz.visual.library.pre)
    post = reiz.Cue(canvas, visualstim=reiz.visual.library.post)
    decision = reiz.Cue(canvas, visualstim=reiz.visual.Mural("F5 to start. ESC to quit."))
    augen_auf_visual = [reiz.visual.Background(color='light'),
                        reiz.visual.library.fixation,
                        generate_info(counter)]
    augen_auf = reiz.Cue(canvas,
                         audiostim=reiz.audio.library.hint,
                         visualstim=augen_auf_visual,
                         markerstr='augen_auf')

    # %%

    canvas.open()

    counter = Counter()
    while True:
        canvas.start_run = False #reset the decision screen
        while not canvas.start_run: #wait for decision
            decision.show(duration = 0.1)
        counter["runs"] += 1
        # start and run a trial
        pre.show(duration = 3)
        for trl_num in range(trials):
            counter["trials"] += 1
            # update the trial-info
            augen_auf.visual[-1] = generate_info(counter)
            # and show 
            augen_auf.show(duration = 5) 
        post.show(duration = 3)
    
    canvas.close()

def main():
    from reiz.marker.__main__ import subprocess
    subprocess()
    start()
    
if __name__ == '__main__':
    main()
