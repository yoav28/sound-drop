import numpy as np, pyaudio, time
from piano import play_tabs
from Byte import Byte
from utills import *


class Player:

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                output=True)

    def play_sounds(self, freqs: list[int], duration: float = 0.5, add_hz: bool = True):
        wave = np.zeros(int(RATE * duration))
        t = np.linspace(0, duration, int(RATE * duration))

        if type(freqs) in [int, float]:
            freqs = [freqs]

        for freq in freqs:
            wave = self.add_freq(freq, wave, t, add_hz)

        self.stream.write(wave.astype(np.float32).tobytes())

    @staticmethod
    def add_freq(freq: int, wave: np.ndarray, t: float, add_hz: bool) -> np.ndarray:
        if add_hz and freq >= lowest_freq:
            freq += 30

        wave += np.sin(2 * np.pi * freq * t)
        return wave

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    @staticmethod
    def file_gen(filename: str):
        with open(filename, "rb") as file:
            for byte in file.read():
                yield Byte(byte).freq

    def play_file(self, filename: str):
        time.sleep(1)

        tabs_gen = play_tabs()
        file_gen = self.file_gen(filename)
        random_id = lowest_freq

        self.play_sounds(next(tabs_gen) + START, 0.25)

        for freqs in file_gen:
            freqs_to_play = [random_id] + freqs + next(tabs_gen)
            self.play_sounds(freqs_to_play, 0.22)
            time.sleep(0.02)

            if random_id == lowest_freq + 9 * interval:
                random_id = lowest_freq

            else:
                random_id += interval

        time.sleep(0.1)
        self.play_sounds(next(tabs_gen) + STOP, 0.25)
