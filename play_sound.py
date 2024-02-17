import numpy as np
import pyaudio


def play_sound(frequency, duration):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(2 * np.pi * frequency * t)

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=sample_rate,
        output=True)

    stream.write(wave.astype(np.float32).tostring())

    stream.stop_stream()
    stream.close()
    p.terminate()


play_sound(6000, 3)
