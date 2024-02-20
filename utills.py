
RATE = 44100

lowest_freq = 8_000
interval = 100
freqs_per_octave = 16
octave_interval = interval * freqs_per_octave + interval
octaves = 6
highest_freq = lowest_freq + (octaves * octave_interval)
STOP = [lowest_freq + i * octave_interval + interval for i in range(4)]
START = [lowest_freq + interval * 3 + i * octave_interval + interval for i in range(1, 5)]
