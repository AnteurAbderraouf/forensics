from collections import Counter
import math

CHUNK_SIZE = 1024 * 1024  # read 1 MiB at a time so big files don't fill memory


def calculate_entropy(path):
    """
    Shannon entropy of the file, in bits per byte (0.0 to 8.0).
    Raises OSError if the file can't be read.
    """
    count = Counter()
    length = 0
    with open(path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            count.update(chunk)
            length += len(chunk)
    if length == 0:
        return 0.0
    entropy = 0.0
    for freq in count.values():
        p = freq / length
        entropy -= p * math.log2(p)
    return entropy
