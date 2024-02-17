import zipfile

RATE = 40100
# RATE = 80100

min_freq = 3000
interval = 30
total_bytes = 255
max_freq = min_freq + interval * total_bytes

start_byte = min_freq - 100
end_byte = min_freq - 200
finish_byte = min_freq - 300
benchmark_1 = min_freq - 400
benchmark_2 = min_freq + 500


def freq_to_num(freq: int) -> int:
    sd = 45

    if finish_byte - sd < freq < finish_byte + sd:
        return -4

    if start_byte - sd < freq < start_byte + sd:
        return -3

    if end_byte - sd < freq < end_byte + sd:
        return -2

    if freq < min_freq - sd or freq > max_freq + sd:
        return -1

    above_min = freq - min_freq
    number = above_min / interval

    # round to the nearest number
    if number - int(number) > 0.5:
        return int(number) + 1

    return int(number)



def num_to_freq(num: int) -> int:
    return min_freq + num * interval


def zip_files(files: list[str], name: str):
    with zipfile.ZipFile(name, "w") as z:
        for file in files:
            z.write(file)

def unzip_files(name: str, path: str):
    with zipfile.ZipFile(name, "r") as z:
        z.extractall(path)
