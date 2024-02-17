from utills import *
import numpy as np
import pyaudio


class Player:

    def __init__(self):
        self.last_sound = -1
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                output=True)

    def play_sounds(self, frequencies: list[int], duration: float):
        for freq in frequencies:
            self.play_sound(freq, duration)

    def play_sound(self, freq: int, duration: float):
        if freq == self.last_sound:
            freq += 3

        self.last_sound = freq
        t = np.linspace(0, duration, int(RATE * duration), endpoint=False)
        wave = 0.5 * np.sin(2 * np.pi * freq * t)
        self.stream.write(wave.astype(np.float32).tobytes())

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


player = Player()


player.play_sounds([benchmark_1, benchmark_2], 0.5)

time_to_play = 0.15

path = "hello.txt"
path_to_zip = "hello.zip"
zip_files([path], path_to_zip)

with open(path_to_zip, "rb") as f:
    data = f.read()

    for byte in data:
        player.play_sound(num_to_freq(byte), time_to_play)

player.play_sound(finish_byte, 0.5)
