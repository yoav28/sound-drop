# Sound Drop

Sound Drop is a Python project that encodes and decodes data into audio signals. It can represent data as a series of frequencies, play them as sound, and listen for these sounds to reconstruct the original data.

## How it Works

The core idea is to map bytes of data to specific audio frequencies. Each byte is converted into a set of frequencies that are then played. A listener module captures the audio, identifies the dominant frequencies, and converts them back into bytes.

This project was never fully completed due to inaccuracies encountered when trying to reliably transmit data via sound waves.

## Files

### `Byte.py`

This class represents a single byte of data and handles its conversion to and from audio frequencies.

- **`__init__(self, byte: int = 0)`**: Initializes a `Byte` object from an integer.
- **`freq`**: A property that returns a list of four frequencies representing the byte.
- **`set_from_freq(self, freqs: list[int])`**: Sets the byte's value from a list of four frequencies.
- **`set_from_str(self, string: str)`**: Sets the byte's value from a string character.

### `play_sound.py`

This script is responsible for playing the audio signals.

- **`Player` class**:
  - **`play_sounds(self, freqs: list[int], duration: float = 0.5)`**: Plays a combination of frequencies for a given duration.
  - **`generator(filename: str)`**: A generator that yields frequency sets for each byte in a file or string.
  - **`play(self, filename: str)`**: Plays an entire file or string as a sequence of sounds. It includes `START` and `STOP` signals and can optionally overlay a piano melody.

### `listener.py`

This script listens for the audio signals and decodes them back into data.

- **`Listener` class**:
  - **`listen(self)`**: Listens for audio from the microphone and processes it in real-time.
  - **`plot_rounded_spectrum(self, data: np.ndarray)`**: Analyzes the frequency spectrum of the incoming audio.
  - **`find_peaks(self, data: dict[int, float])`**: Identifies the dominant frequencies (peaks) in the spectrum.
  - **`process(self, audio: np.ndarray)`**: Processes the audio data to identify bytes, handling `START` and `STOP` signals.
  - **`stop(self)`**: Stops the listener and prints the received data.

### `piano.py`

This script provides a simple melody that can be played in the background during data transmission.

- **`play_tabs()`**: A generator that yields notes from the "Für Elise" melody by Beethoven.

## How to Run

1.  **Run `listener.py`**: This will start the listener, which will wait for audio signals.
2.  **Run `play_sound.py`**: This will encode the content of a file into sound and play it.
