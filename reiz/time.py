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
        delta_t = ts - self.last_ts
        self.cumulative_time += delta_t
        self.last_ts = ts
        return delta_t

    def pause(self):
        """pass time as idle

        returns
        -------
        delta_t: float
            time passed in seconds since the last call of :meth:`~.tick` or
            :meth:`~.pause`. This is time not being added to the cumulative time
        """
        ts = self.time()
        delta_t = ts - self.last_ts
        self.last_ts = ts
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

        sometimes, you execute some other commands, and these commands have a variable runtime. If we would naively sleep everytime for n seconds afterwards, we would inherit this jitter. By using :meth:`~.tick` before these commands, and :meth:`~.sleep_since_tick` after these commands, we can normalize the runtime to a fixed period (as long as the sleep duration is longer than the runtime of the commands).

        Additionally, this function keeps track of any oversleeping or undersleeping, and will minimize the temporal error asymptotically

        returns
        -------
        duration: float
            the time in seconds spent sleeping since the last call
            of :meth:`~.tick` or :meth:`~.sleep_debiased`.


        Example
        -------

        This examkle shows how we can regularize the time spent in each cycle to 200ms in spite of there being an element of random runtime  

        .. code-block:: python

            import time
            import random
            clock = Clock()
            clock.reset()
            clock.tick()
            for i in range(1, 11):
                time.sleep(random.random()/10)
                dt = clock.sleep_debiased(0.2)
                print(i, clock.now(), dt)
            print(i*.2, clock.now())
        """
        bias = self.tick()
        dt = clock.sleep(duration - bias - self._error)
        self._error += dt + bias - duration
       # self.tick()
        return dt + bias

    def reset(self):
        """reset the clock

        resets the counter keeping track of the cumulative time spend since the last call to :meth:`~.reset` to 0
        """
        self.cumulative_time = 0
        self.next_ts = self.last_ts = self.time()

    def now(self):
        """return the cumulative time passed since the last call of :meth:`reset`

        this cumulative time has ignored any time spent with :meth:`pause`.
        """
        self.tick()
        return self.cumulative_time


clock = Clock()  #: a default :class:`.Clock` instance ready for your experiment
