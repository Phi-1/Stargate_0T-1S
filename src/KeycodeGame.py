from src.macropad_manager import Macropad_manager as MM
from src.Timer import Timer
from src.animation import Frame, animate
import random


class KEY_STATES:
    BLANK = 0
    NEXT = 1
    RIGHT = 2
    WRONG = 3
    GOLD = 4

class COLORS:
    NEXT = (255, 255, 255)
    RIGHT = (0, 255, 0)
    WRONG = (255, 0, 0)
    GOLD = (255, 100, 0)

class KeycodeGame:   

    def __init__(self, n_numbers):
        if n_numbers > 12:
            print("ERROR: game only generates codes up to 12 numbers long")
            return None
        self.KEYCODE = self._generate_code(n_numbers)
        self._key_states = [KEY_STATES.BLANK for i in range(12)]
        self.game_solved = False
        self._key_states[self._get_next_key()] = KEY_STATES.NEXT
        MM.clear_pixels()
        MM.set_pixel(self._get_next_key(), COLORS.NEXT)


    def update(self, *args):
        if self.game_solved:
            return None
        key = MM.key_pressed()
        if key is not None:
            self._process_input(key)
        return self


    def _generate_code(self, n_numbers):
        code = []
        for i in range(n_numbers):
            while True:
                key = random.randint(0, 11)
                if key in code:
                    continue
                code.append(key)
                break
        return code

    def _get_next_key(self):
        return self.KEYCODE[0]

    def _play_wrong_key_animation(self, key_n):
        # colors
        f1 = Frame(lambda: MM.set_pixel(key_n, COLORS.WRONG), 0.1)
        f2 = Frame(lambda: MM.set_pixel(key_n, (0,0,0)), 0.1)
        def fEnd():
            state = self._key_states[key_n]
            if state == KEY_STATES.BLANK:
                MM.set_pixel(key_n, (0,0,0))
            elif state == KEY_STATES.NEXT:
                MM.set_pixel(key_n, COLORS.NEXT)
            elif state == KEY_STATES.RIGHT:
                MM.set_pixel(key_n, COLORS.RIGHT)
        animate([f1, f2, f1, f2, f1, f2, Frame(fEnd, 0)])
        # sound
        animate([Frame(lambda: MM.play_tone(600, 0.1), 0.1), Frame(lambda: MM.play_tone(600, 0.1), 0.1)])

    def _play_win_animation(self):
        # TODO: just found out play tone is blocking so fix animation timing
        # colors
        def get_frame(key_n):
            def f():
                MM.set_pixel(key_n, COLORS.GOLD)
            return f

        frames = [Frame(get_frame(i), 0.05) for i in range(12)]
        def finish_frame():
            for i in range(12):
                MM.set_pixel(i, COLORS.GOLD)
        frames.append(Frame(finish_frame, 0))
        animate(frames)
        # sound
        animate([Frame(lambda: MM.play_tone(261.63, 0.1), 0.1), Frame(lambda: MM.play_tone(329.63, 0.1), 0.1), Frame(lambda: MM.play_tone(392, 0.1), 0.1), Frame(lambda: MM.play_tone(493.88, 0.1), 0.1), Frame(lambda: MM.play_tone(523.25, 0.5), 0.1)])

    def _process_input(self, key):
        if self._key_states[key] == KEY_STATES.NEXT:
            self._key_states[key] = KEY_STATES.RIGHT
            MM.set_pixel(key, COLORS.RIGHT)
            self.KEYCODE.pop(0)
            if len(self.KEYCODE) == 0:
                self.game_solved = True
                self._play_win_animation()
                self._process_game_end()
                return
            animate([Frame(lambda: MM.play_tone(900, 0.1), 0.1), Frame(lambda: MM.play_tone(1200, 0.1), 0.1)])
            self._key_states[self._get_next_key()] = KEY_STATES.NEXT
            MM.set_pixel(self._get_next_key(), COLORS.NEXT)
        elif self._key_states[key] == KEY_STATES.BLANK:
            self._play_wrong_key_animation(key)
            


    def _process_game_end(self):
        print("congrats")