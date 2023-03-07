from src.macropad_manager import Macropad_manager as MM
from src.KeycodeGame import KeycodeGame
from src.SimonSaysGame import SimonSaysGame
from src.animation import Frame, animate

menu_options = [
    "Keycode",
    "Interstellar Nav",
    "Space Defense"
]

class Menu:

    def __init__(self):
        self.display = MM.get_display_context()
        self.current_submenu = 0
        self.handled_press = False
        self.clear_screen()
        self.display.show()

    def update(self, *args):
        encoder = MM.get_encoder_value()

        if self.handled_press and not MM.get_encoder_switch():
            self.handled_press = False

        if not self.handled_press and MM.get_encoder_switch():
             return self.process_input(encoder)
        
        if self.current_submenu == 0:
            self.display_main_menu(encoder)
        elif self.current_submenu == 1:
            self.display_keycode_menu(encoder)
        elif self.current_submenu == 2:
            self.display_simonsays_menu(encoder)
        elif self.current_submenu == 3:
            self.display_spacedefense_menu(encoder)

        return self

    def display_main_menu(self, encoder):
        option = encoder % 3
        self.display[0].text = " > STARGATE 0T-1S <"
        for line in range(1, 4):
            if option == line-1:
                self.display[line].text = "> " + menu_options[line-1]
                continue
            self.display[line].text = menu_options[line-1]

    def display_keycode_menu(self, encoder):
        vortex_level = encoder % 12 + 1
        self.display[0].text = " > STARGATE 0T-1S <"
        self.display[2].text = "Vortex level: " + str(vortex_level)
        self.display[3].text = "X" * vortex_level

    def display_simonsays_menu(self, encoder):
        map_sizes = ["x2y2", "x3y2", "x3y3", "x3y4"]
        map_size = map_sizes[encoder % 4]
        self.display[0].text = " > STARGATE 0T-1S <"
        self.display[2].text = "Star region: " + map_size

    def display_spacedefense_menu(self, encoder):
        pass

    def process_input(self, encoder):
        self.handled_press = True
        if self.current_submenu == 0:
            self.current_submenu = encoder % 3 + 1
            self.clear_screen()
            return self
        if self.current_submenu == 1:
            vortex_level = encoder % 12 + 1
            self.clear_screen()
            animate([Frame(lambda: MM.play_tone(250, 0.2), 0.2), Frame(lambda: MM.play_tone(150, 0.2), 0.2)])
            return KeycodeGame(vortex_level)
        if self.current_submenu == 2:
            map_size = encoder % 4
            self.clear_screen()
            return SimonSaysGame(map_size)
        if self.current_submenu == 3:
            # TODO: space defense
            self.clear_screen()
            return self
        
    def clear_screen(self):
        for line in range(4):
            self.display[line].text = ""