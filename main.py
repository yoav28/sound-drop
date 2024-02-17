from utills import *
import numpy as np
import pyaudio
import threading


class Listener:

    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = RATE
        self.CHUNK = 1024 * 2
        self.last_sound = -1
        self.file: list[int] = []
        self.bm1 = None
        self.bm2 = None


    def listen_to_microphone(self):
        p = pyaudio.PyAudio()

        stream = p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK)

        while True:
            data = np.fromstring(stream.read(self.CHUNK), dtype=np.int16)
            threading.Thread(target=self.process_data, args=(data,)).start()

    def process_data(self, data: np.ndarray):
        freq = self.find_freq(data)
        byte = freq_to_num(freq)

        if freq == self.last_sound:
            return

        self.last_sound = freq

        bms = (self.bm1, self.bm2)

        sd = 100

        if benchmark_1 - sd < freq < benchmark_1 + sd:
            self.bm1 = benchmark_1 / freq
            return

        if benchmark_2 - sd < freq < benchmark_2 + sd:
            self.bm2 = benchmark_2 / freq
            return

        if None in bms:
            return

        if byte < 0:
            if byte == -4:
                self.on_finish()

            return

        self.file.append(byte)

    def find_freq(self, data: np.ndarray) -> int:
        fft = np.abs(np.fft.rfft(data))
        i = np.argmax(fft)
        freq = i * self.RATE / self.CHUNK
        return freq

    def on_finish(self):
        with open("test.zip", "wb") as f:
            for byte in self.file:
                f.write(byte.to_bytes(1, "big"))

        unzip_files("file.zip", "unzipped")
        print("Unzipped")

        self.bm1, self.bm2 = None, None
        self.file = []


if __name__ == '__main__':
    listener = Listener()
    listener.listen_to_microphone()
