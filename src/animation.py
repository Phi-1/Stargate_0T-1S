from src.Timer import Timer

class Frame:

    def __init__(self, function, length_s):
        self.function = function
        self.length = length_s


def animate(frames):
    time = 0
    for frame in frames:
        Timer.add_timer(time*1E9, frame.function)
        time += frame.length