'''
Play sound easily.
TODO:
[x] support windwos
[ ] support linux
'''
import time
import threading
import ctypes

class WindowsBeeper:
    """Beep Player in WindowsOS"""
    def __init__(self, freq=1000) -> None:
        self.player = ctypes.windll.kernel32
        self.freq = freq

    def play(self, duration):
        """Play Beep"""
        self.player.Beep(self.freq, duration)


class Beeper:
    """Player Manager"""
    def __init__(self, freq=1000) -> None:
        self.__player = WindowsBeeper(freq)

    def play(self, duration=500):
        """Sound Player Cross-Platform"""
        self.__player.play(duration)

def beep(freq, duration, count=1, gap=1000, in_new_thread=False):
    """make beep"""
    def _fn():
        for _ in range(count):
            player = Beeper(freq)
            player.play(duration)
            time.sleep(gap / 1000)
    if in_new_thread:
        _thread = threading.Thread(target=_fn)
        _thread.start()
    else:
        _fn()
