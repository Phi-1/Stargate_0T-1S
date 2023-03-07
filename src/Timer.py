
# for static use with tick_all and add_timer, as instance with constructor and tick
class Timer:
    TIMERS = []

    @staticmethod
    def add_timer(time_ns, callback):
        Timer.TIMERS.append(Timer(time_ns, callback))

    @staticmethod
    def tick_all(time_ns):
        finished_timers = []
        for timer in Timer.TIMERS:
            timer.tick(time_ns)
            if not timer.is_ticking():
                finished_timers.append(timer)
        if len(finished_timers) > 0:
            for timer in finished_timers:
                Timer.TIMERS.pop(Timer.TIMERS.index(timer))

    def __init__(self, time_ns, callback):
        self._time = time_ns
        self._callback = callback
        self._ticking = True

    def tick(self, time_ns):
        if not self._ticking:
            return
        self._time -= time_ns
        if self._time <= 0:
            self._ticking = False
            self._callback()

    def is_ticking(self):
        return self._ticking

    def get_time(self):
        return self._time
