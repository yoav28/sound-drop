import numpy as np
import pyaudio
import time
import threading
import os
from play_sound import Player
from Byte import Byte
from utills import RATE, lowest_freq, highest_freq, interval, octave_interval, octaves, START, STOP


class Listener:
    def __init__(self):
        self.low_freq = lowest_freq
        self.high_freq = highest_freq
        self.chunk = 2048
        self.file: list[Byte] = []
        self.last_id = 0
        self.run = True
        self.same_id = False
        self.started = False

    def plot_rounded_spectrum(self, data: np.ndarray) -> dict[int, list[float]]:
        n = len(data)
        k = np.arange(n)
        T = n / RATE
        frq = k / T
        frq = frq[range(n // 2)]

        Y = np.fft.fft(data) / n
        Y = Y[range(n // 2)]

        low_idx = int(np.round(self.low_freq * n / RATE))
        high_idx = int(np.round(self.high_freq * n / RATE))

        round_by = int(np.log10(100)) * -1
        rounded_frq = np.round(frq[low_idx:high_idx], round_by)
        unique_rounded_frq = np.unique(rounded_frq)
        rounded_Y = np.zeros_like(unique_rounded_frq)

        for i, freq in enumerate(unique_rounded_frq):
            idx = np.where(rounded_frq == freq)
            rounded_Y[i] = np.mean(abs(Y[low_idx:high_idx][idx]))

        rounded_spectrum = {}
        for freq, amplitude in zip(frq[low_idx:high_idx], abs(Y[low_idx:high_idx])):
            rounded_freq = int(np.round(freq, round_by))
            if rounded_freq in rounded_spectrum:
                rounded_spectrum[rounded_freq].append(amplitude)
            else:
                rounded_spectrum[rounded_freq] = [amplitude]

        return rounded_spectrum

    @staticmethod
    def find_peaks(data: dict[int, float]) -> list[int]:
        peaks: list[int] = []

        for start in [lowest_freq + x * octave_interval for x in range(octaves)]:
            lst = [int(data[key] * 1000000) for key in range(start, start + octave_interval, interval)]
            highest = max(lst)
            median = np.median(lst)
            average = np.average(lst)

            if highest > 3 * median and highest > 3 * average and highest > 0.03:
                adding = start + lst.index(highest) * interval
                peaks.append(adding)

        return peaks

    def listen(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=self.chunk
        )

        for _ in range(3):
            stream.read(self.chunk)

        while self.run:
            data = stream.read(self.chunk)

            if self.same_id:
                self.same_id = False
                continue

            audio = np.frombuffer(data, dtype=np.float32)
            self.process(audio)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def process(self, audio: np.ndarray, flat: bool = True):
        if flat:
            rounded_freqs = self.plot_rounded_spectrum(audio.flatten())
            d = {key: np.mean(value) for key, value in rounded_freqs.items()}
        else:
            d = audio

        peaks = self.find_peaks(d)

        if all(x in peaks for x in START):
            self.started = True
            return

        if all(x in peaks for x in STOP):
            return self.stop()

        if len(peaks) != 5:
            return

        id_ = peaks[0]
        if id_ == self.last_id:
            self.same_id = True
            return

        try:
            byte = Byte().set_from_freq(peaks[1:])
        except ValueError:
            return

        self.last_id = id_
        self.file.append(byte)
        print(f"Byte: {byte}")

    def stop(self):
        self.run = False

        with open("output.txt", "wb") as file:
            for byte in self.file:
                print(byte, end="")
                file.write(bytes(byte))

        print("\nFile saved as output.txt")

        time.sleep(1)
        self.started = False
        self.file = []
        self.last_id = 0
        self.same_id = False


if __name__ == '__main__':
    player = Player()

    filename = 'x'
    while not os.path.exists(filename):
        filename = input("Enter path of file to play: ")

    listener = Listener()
    threading.Thread(target=listener.listen).start()

    player.play_file(filename)
