notes = {
    "C4": 261.63,
    "D4": 293.66,
    "E4": 329.63,
    "F4": 349.23,
    "G4": 392.00,
    "A4": 440.00,
    "B4": 493.88,
    "C5": 523.25
}

tabs: list[dict[str, int]] = [
    ['D4'], ['E4'], ['F4'], ['G4'], ['A4'], ['B4'], ['C5']
]

def play_tabs():
    while True:
        for note_ in tabs:
            if note_ == {}:
                yield []
                continue

            freqs = []
            for note in note_:
                frequency = notes[note]
                freqs.append(frequency)

            yield freqs

        # for _ in range(3):
        #     yield []
