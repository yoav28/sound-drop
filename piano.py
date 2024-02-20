from mingus.containers import Note


# Für Elise
tabs = [
    ['E5'], ['D#5'], ['E5'], ['D#5'], ['E5'], ['B4'], ['D5'], ['C5'], ['A4'], ['C4'], ['E4'], ['A4'], ['B4'],
    ['E4'], ['G#4'], ['B4'], ['C5'], ['E4'], ['E5'], ['D#5'], ['E5'], ['D#5'], ['E5'], ['B4'], ['D5'], ['C5'],
    ['A4'], ['C4'], ['E4'], ['A4'], ['B4'], ['E4'], ['C5'], ['B4'], ['A4'], ['G#4'], ['E5'], ['G#5'], ['A5'],
    ['F5'], ['A5'], ['G#5'], ['E5'], ['A4'], ['D5'], ['E5'], ['F5'], ['E5'], ['D5'], ['C5'], ['E4'], ['A4'],
    ['G4'], ['F4'], ['E4'], ['C5'], ['E4'], ['A4'], ['G4'], ['F4'], ['E4'], ['B4'], ['D5'], ['C5'], ['A4'],
    ['C4'], ['E4'], ['A4'], ['B4'], ['E4'], ['G#4'], ['B4'], ['C5'], ['E4'], ['E5'], ['D#5'], ['E5'], ['D#5'],
    ['E5'], ['B4'], ['D5'], ['C5'], ['A4'], ['C4'], ['E4'], ['A4'], ['B4'], ['E4'], ['C5'], ['B4'], ['A4'],
    ['G#4'], ['E5'], ['G#5'], ['A5'], ['F5'], ['A5'], ['G#5'], ['E5'], ['A4'], ['D5'], ['E5'], ['F5'], ['E5'],
    ['D5'], ['C5'], ['E4'], ['A4'], ['G4'], ['F4'], ['E4'], ['C5'], ['E4'], ['A4'], ['G4'], ['F4'], ['E4'],
    ['B4'], ['D5'], ['C5'], ['A4'], ['C4'], ['E4'], ['A4'], ['B4'], ['E4'], ['C5'], ['B4'], ['A4'], ['G#4']
]



def play_tabs():
    while True:
        for note_ in tabs:
            if note_ == {}:
                yield []
                continue

            freqs = []
            for note in note_:
                note, octave = note[:-1], int(note[-1])
                notedata = Note(name=f"{note}-{octave}")
                freqs.append(notedata.to_hertz())

            yield freqs

        for _ in range(3):
            yield []


if __name__ == '__main__':
    from play_sound import Player
    player = Player()

    play = play_tabs()
    while True:
        notes = next(play)
        if not notes:
            break

        player.play_sounds(notes, 0.1)
        # time.sleep(0.5)

