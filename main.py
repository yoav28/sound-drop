import threading, pyaudio
import numpy as np


class Listener:

    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024

        # Will be bytes later
        self.history: list[int] = []
        self.file: list[int] = []


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
        byte = self.freq_to_byte(freq)

        if byte == -1:
            return

        self.history.append(byte)

        if len(self.history) >= 3 and self.history[-1] == self.history[-2] == self.history[-3]:
            byte_ = self.history[-1]
            print(f"Byte: {byte_}")
            self.history = []
            self.file.append(byte_)


    def find_freq(self, data: np.ndarray) -> int:
        fft = np.abs(np.fft.rfft(data))
        i = np.argmax(fft)
        freq = i * self.RATE / self.CHUNK
        return int(freq)


    def freq_to_byte(self, freq: int) -> int:
        MAX_FREQ = 7000
        MIN_FREQ = 3000

        if freq < MIN_FREQ or freq > MAX_FREQ:
            return -1

        x = (freq - MIN_FREQ) / (MAX_FREQ - MIN_FREQ)
        return int(x * 255)
        # TODO: convert to byte here


if __name__ == '__main__':
    listener = Listener()
    listener.listen_to_microphone()
