from adafruit_macropad import MacroPad

class Macropad_manager:
    MACROPAD = MacroPad()
    DISPLAY_CONTEXT = MACROPAD.display_text()
    KEY_EVENT = None

    @staticmethod
    def get_macropad():
        return Macropad_manager.MACROPAD

    @staticmethod
    def get_display_context():
        return Macropad_manager.DISPLAY_CONTEXT

    @staticmethod
    def set_brightness(amount):
        Macropad_manager.MACROPAD.pixels.brightness = amount

    @staticmethod
    def clear_pixels():
        Macropad_manager.MACROPAD.pixels.fill((0,0,0))

    @staticmethod
    def set_pixel(number, color):
        if number < 0 or number >= 12:
            print(f"ERROR: pixel {number} is out of bounds")
            return
        Macropad_manager.MACROPAD.pixels[number] = color

    @staticmethod
    def poll_events():
        Macropad_manager.KEY_EVENT = Macropad_manager.MACROPAD.keys.events.get()

    @staticmethod
    def key_pressed():
        if not Macropad_manager.KEY_EVENT:
            return None
        if Macropad_manager.KEY_EVENT.pressed:
            return Macropad_manager.KEY_EVENT.key_number
        return None

    @staticmethod
    def key_released():
        if not Macropad_manager.KEY_EVENT:
            return None
        if Macropad_manager.KEY_EVENT.released:
            return Macropad_manager.KEY_EVENT.key_number
        return None

    @staticmethod
    def get_encoder_value():
        return Macropad_manager.MACROPAD.encoder

    @staticmethod
    def get_encoder_switch():
        return Macropad_manager.MACROPAD.encoder_switch

    @staticmethod
    def play_tone(freq, duration):
        Macropad_manager.MACROPAD.play_tone(freq, duration)