from collections import Counter
import math

def calculate_entropy(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
    except PermissionError:
        return None
    if not data:
        return 0.0
    count = Counter(data)
    length = len(data)
    entropy = 0.0
    for freq in count.values():
        p = freq / length
        entropy -= p * math.log2(p)
    return entropy