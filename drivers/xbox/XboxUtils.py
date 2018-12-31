import time


# FIXME Make a competent debouncing mecanism
class ButtonDebouncer:

    def __init__(self, tolerance):
        self.prev_time = time.time()
        self.delta = 0
        self.tolerance = tolerance

    def update(self):
        self.delta = time.time() - self.prev_time
        self.prev_time = self.delta

    def should_filter(self):
        return self.delta <= self.tolerance
