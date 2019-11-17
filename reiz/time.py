# -*- coding: utf-8 -*-
"""A clock based on LSL local_clock
"""
from pylsl import local_clock


class Clock():
    """allows to keep track of time

    reset the clock with :meth:`~.reset`, and get the time since this reset with :meth:`~.now`. Measure intermediate times with :meth:`~.tick`, which return time since last call of :meth:`tick`, or

    each call of :meth:`~.tick` updates the cumulative time since the last call of :meth:`reset`. If you don't want to add the time measured, use :meth:`~.pause`
    """

    def __init__(self):
        "create a new instance requiring no arguments"
        self._error = 0.
        self.reset()

    def time(self):
        "time in seconds (usually since computer boot) according to LSL"
        return local_clock()

    def tick(self) -> float:
        """time since last call of :meth:`~.tick`

        returns
        -------
        delta_t: float
            time passed in seconds since the last call of :meth:`~.tick` or
            :meth:`~.pause`. This is time counting into the cumulative time


        """
        ts = self.time()
        delta_t = ts - self.last_tick
        self.last_tick = ts
        return delta_t

    def sleep(self, duration: float):
        """Sleep for duration in seconds

        blocking is slightly more accurate than non-blocking sleep, e.g. as available with :meth:`time.sleep` from the stdlib. There is one disadvantage of this kind of busy sleep: it can cause slight oversleeping, as there is an overhead of the function being called and returning, which is not accounted for. See :meth:`~.sleep_debiased` for an alternative sleep with asymptotic minimisation of the error.

        args
        ----
        duration: float
            how many seconds to sleep blocking

        returns
        -------
        duration: float
            the time in seconds spent sleeping
        """
        t1 = t0 = self.time()
        dt = 0
        while dt <= duration:
            t1 = self.time()
            dt = t1-t0
        return dt

    def sleep_debiased(self, duration: float):
        """Sleep for duration in seconds with attempts for debiasing`

        sometimes, you execute some other commands, and these commands have a variable runtime. If we would naively sleep everytime for n seconds afterwards, we would inherit this jitter. By using :meth:`~.tick` before these commands, and :meth:`~.sleep_debiased` after these commands, we can normalize the runtime to a fixed period (as long as the sleep duration is longer than the runtime of the commands).

        Additionally, this function keeps track of any oversleeping or undersleeping, and will minimize the temporal error asymptotically

        returns
        -------
        duration: float
            the time in seconds spent sleeping since the last call
            of :meth:`~.tick` or :meth:`~.sleep_debiased`.


        Example
        -------

        This example shows how we can regularize the time spent in each cycle to 200ms in spite of there being an element of random runtime

        .. code-block:: python

            import time
            import random
            from reiz.time import Clock
            clock = Clock()
            t = 0.
            msg = "{0:3.5f}, {1:3.5f}, {2:3.5f}, slept for {3:3.5f}s"
            for i in range(1, 11):
                time.sleep(random.random()/10)
                dt = clock.sleep_debiased(0.2)
                t += dt
                print(msg.format(i*0.2, clock.now(), t, dt))
        """
        bias = self.tick()
        dt = self.sleep(duration - bias - self._error)
        self._error += dt + bias - duration
        tick_bias = self.tick()-dt
        self._error += tick_bias
        return dt + bias + tick_bias

    def reset(self):
        """reset the clock

        resets the counter keeping track of the cumulative time spend since instantiaion or the last call of :meth:`~.reset`
        """
        self._t0 = self.last_tick = self.time()

    def now(self):
        """return the cumulative time passed since the last call of :meth:`reset`
        """
        return self.time()-self._t0


clock = Clock()  #: a default :class:`.Clock` instance ready for your experiment
