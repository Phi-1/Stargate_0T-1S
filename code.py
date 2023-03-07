from src.macropad_manager import Macropad_manager as MM
from src.Timer import Timer
from src.Menu import Menu
from src.SimonSaysGame import SimonSaysGame
import time


def loop():
    MM.set_brightness(0.4)

    scene = Menu()

    currentTime = time.monotonic_ns()
    lastTime = 0
    deltaTime = 0
    frameTime = 0
    iterCount = 0
    FPS = 0

    while True:
        lastTime = currentTime
        currentTime = time.monotonic_ns()
        deltaTime = currentTime - lastTime
        frameTime += currentTime - lastTime 
        iterCount += 1

        if frameTime >= 1E9:
            FPS = iterCount
            frameTime = 0
            iterCount = 0

        Timer.tick_all(deltaTime)
        MM.poll_events()

        if scene == None:
            scene = Menu()
        scene = scene.update(FPS)
        


loop()