import pyaudio, threading
import numpy as np
from utills import freq_to_num


class Listener:

    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024

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
        byte = freq_to_num(freq)

        if byte == -1:
            return

        self.history.append(byte)

        if len(self.history) >= 3 and self.history[-1] == self.history[-2] == self.history[-3]:
            byte_ = self.history[-1]
            self.history = []
            self.file.append(byte_)

            print(self.file, len(self.file))

    def find_freq(self, data: np.ndarray) -> int:
        fft = np.abs(np.fft.rfft(data))
        i = np.argmax(fft)
        freq = i * self.RATE / self.CHUNK
        return int(freq)



if __name__ == '__main__':
    listener = Listener()
    listener.listen_to_microphone()
