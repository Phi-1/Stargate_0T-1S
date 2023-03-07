from src.macropad_manager import Macropad_manager as MM
import src.util as util
from src.animation import Frame, animate
import random
import time

color_options = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 40, 0),
    (255, 0, 40),
    (0, 255, 40),
    (40, 255, 0),
    (0, 40, 255),
    (40, 0, 255)
]

# double pentatonic + G3 and A5
tone_options = [
    192.43,

    216,
    256.87,
    288.33,
    323.63,
    384.87,

    432,
    513.74,
    576.65,
    647.27,
    769.74,

    864
]

# keys available to pattern per difficulty
difficulty_options = [
    [0, 1, 3, 4],
    [i for i in range(6)],
    [i for i in range(9)],
    [i for i in range(12)]
]


class SimonSaysGame:
    # TODO: little startup animation that lights up all the keys in a snake pattern
    # TODO: difficulty setting to use only part of the keypad, 2x2, 3x2, 3x3, 3x4
    # TODO: display score
    def __init__(self, difficulty):
        self.available_keys = difficulty_options[difficulty]
        self.pattern = []
        self.input = []
        self.score = 0

        self.colors = util.shuffle(color_options)
        self.tones = util.shuffle(tone_options)

        self.should_clear_input_buffer = 2
        
        self.expand_pattern()
        self.show_pattern()

    def update(self, *args):
        input = MM.key_pressed()
        # clear queued inputs, I don't fucking know why it's this weird, see comment after show_pattern
        if self.should_clear_input_buffer > 0:
            if input == None:
                self.should_clear_input_buffer -= 1
            return self

        if input == None:
            return self
        
        if input == self.pattern[len(self.input)]:
            MM.set_pixel(input, self.colors[input])
            MM.play_tone(self.tones[input], 0.3)
            MM.clear_pixels()
            # check if full pattern is completed
            if len(self.input) + 1 == len(self.pattern):
                # TODO: sound and colors
                self.score += len(self.pattern)
                MM.get_display_context()[1].text = "Score: " + str(self.score)
                self.input = []
                self.expand_pattern()
                self.show_pattern()
                # for some fucking reason it queues inputs followed by a None input event, so to clear all of them we need twice as many
                self.should_clear_input_buffer = len(self.pattern) * 2
                return self
            # if pattern is still incomplete
            self.input.append(input)
            return self
        # wrong input
        print("you suck")
            
    def expand_pattern(self):
        next_key = self.available_keys[random.randrange(0, len(self.available_keys))]
        self.pattern.append(next_key)

    def show_pattern(self):
        time.sleep(1)
        for key in self.pattern:
            MM.clear_pixels()
            time.sleep(0.5)
            MM.set_pixel(key, self.colors[key])
            MM.play_tone(self.tones[key], 0.3) # play tone is blocking for the duration of the tone
            time.sleep(0.7)
        MM.clear_pixels()