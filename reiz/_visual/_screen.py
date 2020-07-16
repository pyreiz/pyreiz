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
        # from pyglet import app
        # if app.event_loop.is_running:
        self.close()

    def on_key_press(self, symbol, modifiers):
        """Default on_key_press handler."""
        key = pyglet.window.key
        if symbol == key.ESCAPE and not (
            modifiers
            & ~(key.MOD_NUMLOCK | key.MOD_CAPSLOCK | key.MOD_SCROLLLOCK)
        ):
            self.dispatch_event("on_close")

        if symbol == key.F5:
            self.start_run = True

        if symbol == key.P:
            self.paused = not self.paused


class Canvas:
    def __init__(
        self,
        size: Tuple[int, int] = (640, 480),
        origin: Tuple[int, int] = (100, 100),
        antialias: bool = True,
    ):
        self.origin = origin
        self.start_width = size[0]
        self.start_height = size[1]
        self._create_window(antialias=antialias)

    @property
    def paused(self):
        return self.window.paused

    @property
    def start_run(self):
        return self.window.start_run

    @start_run.setter
    def start_run(self, value: bool):
        self.window.start_run = value

    def estimate_fps(self):
        pyglet.clock.tick()
        for i in range(0, 100, 1):
            self.window.flip()
            pyglet.clock.tick()
        return pyglet.clock.get_fps()

    def _create_window(self, antialias: bool):
        def default_window(kwargs={}):
            if kwargs == {}:
                # according to pyglet docs
                # https://pyglet.readthedocs.io/en/latest/programming_guide/context.html#opengl-configuration-options
                # Create separate front and back buffers. Without
                # double-buffering, drawing commands are immediately visible
                # on the screen, and the user will notice a visible flicker as
                # the image is redrawn in front of them.
                # It is recommended to set double_buffer=True, which creates a
                # separate hidden buffer to which drawing is performed. When
                # the Window.flip is called, the buffers are swapped, making
                # the new drawing visible virtually instantaneously.
                config = pyglet.gl.Config(double_buffer=True)
                kwargs = {"config": config}
            return ExperimentalWindow(
                visible=False,
                vsync=True,
                width=self.start_width,
                height=self.start_height,
                resizable=True,
                caption="Experimental Framework",
                **kwargs
            )

        if antialias:
            try:
                # Try to create a window with multisampling for anti-aliasing
                # see https://github.com/pyglet/pyglet/issues/247
                config = pyglet.gl.Config(
                    sample_buffers=1, samples=4, double_buffer=True
                )
                self.window = default_window(kwargs={"config": config})
                print(
                    "Multisampling available. Reiz will run with anti-aliasing"
                )

            except pyglet.window.NoSuchConfigException:
                # Fall back to no multisampling
                print(
                    "Multisampling not available. Reiz will run without anti-aliasing"
                )
                self.window = default_window()
        else:
            self.window = default_window()

        self.window.set_location(*self.origin)
        self.window.dispatch_events()
        self.window.has_exit = False

    def flip(self):
        "flip the backbuffer to front  and clear the old frontbuffer"
        if not hasattr(self, "window"):
            print("Window was closed")
            return
        try:
            self.window.switch_to()
        except AttributeError as e:
            print("Window was closed")
            return
        if self.window.has_exit:
            print("Window was closed")
            return
        try:
            self.window.dispatch_events()
            self.window.dispatch_event("on_draw")
            self.window.flip()  # flip front to backbuffer
            self.window.clear()  # clear the current backbuffer: was the old backbuffer
        except Exception as e:
            print(e)

    def open(self):
        if not hasattr(self, "window") or self.window.has_exit:
            self._create_window()
        self.window.set_visible(True)
        self.window.switch_to()
        self.window.dispatch_events()
        self.window.dispatch_event("on_draw")
        self.clear()

    def close(self):
        if hasattr(self, "window") and not self.window.has_exit:
            self.window.on_close()

    def clear(self):
        "clear both buffers and show a black screen"
        self.flip()
        self.flip()

    def show(self, visual):
        "after having rendered and drawn into the backbuffer, show this"
        try:
            self.window.switch_to()
            if visual is not None:
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
        return (self.height * self.width) ** 0.5

    width = property(get_width)
    height = property(get_height)
    diag = property(get_diag)

    @property
    def available(self):
        return (
            hasattr(self, "window")
            and not self.window.has_exit
            and self.window.visible
        )
