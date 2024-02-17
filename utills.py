min_freq = 3000
interval = 15
total_bytes = 255
max_freq = min_freq + interval * total_bytes


def freq_to_num(freq: int) -> int:
    sd = 5

    if freq < min_freq - sd or freq > max_freq + sd:
        return -1

    above_min = freq - min_freq
    return above_min // interval


def num_to_freq(num: int) -> int:
    return min_freq + num * interval
