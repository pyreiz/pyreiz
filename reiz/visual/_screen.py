# -*- coding: utf-8 -*-
"""
Pyglet based screen and frame drawing

    
"""
import pyglet
from pylsl import local_clock
from typing import Tuple
# %%


def get_screens():
    return pyglet.canvas.Display().get_screens()

# %%


class ExperimentalWindow(pyglet.window.Window):
    start_run = False
    paused = False

    def on_close(self):
        """Default on_close handler, but closing even without vent loop"""
        self.has_exit = True
        #from pyglet import app
        # if app.event_loop.is_running:
        self.close()

    def on_key_press(self, symbol, modifiers):
        """Default on_key_press handler."""
        key = pyglet.window.key
        if symbol == key.ESCAPE and not (modifiers & ~(key.MOD_NUMLOCK |
                                                       key.MOD_CAPSLOCK |
                                                       key.MOD_SCROLLLOCK)):
            self.dispatch_event('on_close')

        if symbol == key.F5:
            self.start_run = True

        if symbol == key.P:
            self.paused = ~self.paused

    def _on_mouse_press_log(self, x, y, button, modifiers):
        from reiz.marker import push
        from pylsl import local_clock
        tstamp = local_clock()
        if button == pyglet.window.mouse.LEFT:
            push('LEFT_MOUSE_BUTTON',  tstamp=tstamp)
        elif button == pyglet.window.mouse.RIGHT:
            push('RIGHT_MOUSE_BUTTON', tstamp=tstamp)
        elif button == pyglet.window.mouse.MIDDLE:
            push('MIDDLE_MOUSE_BUTTON', tstamp=tstamp)

    def _on_mouse_press_log_to_queue(self, x, y, button, modifiers):

        tstamp = local_clock()

        def push(label, tstamp):
            print(f"Pushing to queue: {label} at {tstamp}")
            self.queue.put((label, tstamp))

        if button == pyglet.window.mouse.LEFT:
            push('LEFT_MOUSE_BUTTON',  tstamp=tstamp)
        elif button == pyglet.window.mouse.RIGHT:
            push('RIGHT_MOUSE_BUTTON', tstamp=tstamp)
        elif button == pyglet.window.mouse.MIDDLE:
            push('MIDDLE_MOUSE_BUTTON', tstamp=tstamp)

    def _on_mouse_press_log_to_queue_and_lsl(self, x, y, button, modifiers):
        def push(label, tstamp):
            from reiz.marker import push
            print(f"Pushing to queue: {label} at {tstamp}")
            self.queue.put((label, tstamp))
            print(f"Pushing to LSL: {label} at {tstamp}")
            push(label, tstamp)

        tstamp = local_clock()
        if button == pyglet.window.mouse.LEFT:
            push('LEFT_MOUSE_BUTTON',  tstamp=tstamp)
        elif button == pyglet.window.mouse.RIGHT:
            push('RIGHT_MOUSE_BUTTON', tstamp=tstamp)
        elif button == pyglet.window.mouse.MIDDLE:
            push('MIDDLE_MOUSE_BUTTON', tstamp=tstamp)

    def enable_mouse_logging_to_queue(self, queue):
        self.queue = queue
        self.on_mouse_press = self._on_mouse_press_log_to_queue

    def enable_mouse_logging_to_queue_and_lsl(self, queue):
        self.queue = queue
        self.on_mouse_press = self._on_mouse_press_log_to_queue_and_lsl

    def _on_mouse_press_swallow(self, x, y, button, modifiers):
        pass

    def enable_mouse_logging(self):
        self.on_mouse_press = self._on_mouse_press_log

    def disable_mouse_logging(self):
        self.on_mouse_press = self._on_mouse_press_swallow


class Canvas():

    def set_mouse_logging(self, state=True):
        if state == "queue":
            from queue import Queue
            queue = Queue()
            self.window.enable_mouse_logging_to_queue(queue=queue)
            return queue
        if state == "both":
            from queue import Queue
            queue = Queue()
            self.window.enable_mouse_logging_to_queue_and_lsl(queue=queue)
            return queue
        elif state == True or state == "lsl":
            self.window.enable_mouse_logging()
        elif state == False:
            self.window.disable_mouse_logging()

    def __init__(self, size: Tuple[int, int] = (640, 480),
                 origin: Tuple[int, int] = (100, 100)):
        maxsize = (get_screens()[0].width, get_screens()[0].height)
        if size == 'full':
            self.size = maxsize
        else:
            self.size = size

        # check whether origin is outside of window
        # outside = [o<0 for o in origin]
        # self.origin = [o*(1-c) for o,c in zip(origin, outside)]
        self.origin = origin

        self.start_width = size[0]
        self.start_height = size[1]
        self._create_window()

    @property
    def paused(self):
        return self.window.paused

    @property
    def start_run(self):
        return self.window.start_run

    @start_run.setter
    def start_run(self, value: bool):
        self.window.start_run = value

    def is_fps_feasible(self, fps, throw=True):
        if fps >= .9*self.get_fps():
            if throw:
                raise ResourceWarning(
                    'Framerate to high for monitor: decrease fps')
            else:
                return False
        return True

    def get_fps(self):
        pyglet.clock.tick()
        for i in range(0, 100, 1):
            self.window.flip()
            pyglet.clock.tick()
        return pyglet.clock.get_fps()

    def _create_window(self):
        self.window = ExperimentalWindow(visible=False,
                                         vsync=True,
                                         width=self.start_width,
                                         height=self.start_height,
                                         resizable=True,
                                         caption='Experimental Framework')

        self.window.set_location(*self.origin)
        self.window.dispatch_events()
        self.window.has_exit = False

    def _on_key_press(symbol, modifiers):
        pass

    def flip(self):
        "flip the backbuffer to front  and clear the old frontbuffer"
        try:
            self.window.switch_to()
            self.window.dispatch_events()
            self.window.dispatch_event('on_draw')
            self.window.flip()  # flip front to backbuffer
            self.window.clear()  # clear the current backbuffer: was the old backbuffer
        except AttributeError as e:
            if not hasattr(self, 'window') or self.window.has_exit:
                print("Window was closed during flipping")
                return
            else:
                print(__name__, e)
                raise Exception('Window was closed')

    def open(self):
        if not hasattr(self, 'window') or self.window.has_exit:
            self._create_window()
        self.window.set_visible(True)
        self.window.switch_to()
        self.window.dispatch_events()
        self.window.dispatch_event('on_draw')
        self.clear()

    def close(self):
        if hasattr(self, 'window') and not self.window.has_exit:
            self.window.close()

    def clear(self):
        "clear both buffers and show a black screen"
        self.flip()
        self.flip()

    def show(self, visual):
        "after having rendered and drawn into the backbuffer, show this"
        try:
            self.window.switch_to()
            for v in visual:
                if v is not None:
                    v.draw(canvas=self)
        # except TypeError: #visual is not iterable
        #    visual.draw(canvas=self)
        except AttributeError:  # window was closed
            print("Window was closed")
            return
        self.flip()

    def set_fullscreen(self):
        self.window.set_fullscreen(fullscreen=True)
        self.flip()

    def set_windowed(self):
        self.window.set_fullscreen(fullscreen=False)
        self.flip()

    def get_width(self):
        return self.window.width

    def get_height(self):
        return self.window.height

    def get_diag(self):
        return (self.height * self.width)**0.5

    width = property(get_width)
    height = property(get_height)
    diag = property(get_diag)

    @property
    def available(self):
        return (hasattr(self, "window") and not self.window.has_exit)
