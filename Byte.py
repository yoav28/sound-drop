from utills import interval, lowest_freq, octave_interval


class Byte:
    def __init__(self, byte: int = 0):
        self._interval = interval
        self._floor = lowest_freq + 2 * octave_interval
        self._x = byte

    def __bytes__(self):
        return self._x.to_bytes(1, "big")

    def __str__(self):
        return bytes(self).decode("utf-8")

    def __int__(self):
        return self._x

    def _freq(self, floor: int) -> list[int]:
        number = self._x
        hexed = hex(number)[2:].zfill(2).upper()
        split1, split2 = int(hexed[0], 16), int(hexed[1], 16)
        split1 = split1 * self._interval + floor
        split2 = split2 * self._interval + floor + octave_interval
        return [split1, split2]

    @property
    def freq(self) -> list[int]:
        base0 = self._freq(self.floor(0))
        base1 = self._freq(self.floor(2))
        return base0 + base1

    def set_from_freq(self, freqs: list[int]):
        if len(freqs) != 4:
            raise ValueError("Byte must be set from 4 frequencies")

        f1l, f1h, f2l, f2h = freqs

        def get_from_pair(f1: int, f2: int) -> int:
            octave = self.get_octave(f1)
            f2 -= octave_interval

            if octave != self.get_octave(f2):
                raise ValueError("Frequencies must be in the same octave")

            f1 = (f1 - self.floor(octave)) // self._interval
            f2 = (f2 - self.floor(octave)) // self._interval
            return f1 * 16 + f2

        n1, n2 = get_from_pair(f1l, f1h), get_from_pair(f2l, f2h)
        if n1 != n2:
            raise ValueError("Byte is invalid")

        self._x = n1
        return self

    def set_from_str(self, string: str):
        self._x = int.from_bytes(string.encode("utf-8"), "big")
        return self

    def floor(self, octave: int) -> int:
        return self._floor + octave * octave_interval

    def get_octave(self, freq: int) -> int:
        return (freq - self._floor) // octave_interval


if __name__ == '__main__':
    a = 'א'
    b = Byte().set_from_str(a)
    print(b.freq)
    print(str(b))
