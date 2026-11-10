import argparse
import sys
from pathlib import Path
from mismatch import compute_status, detect_type
from entropy import calculate_entropy

EXPECTED_TYPE = {
    ".png":  "PNG",
    ".jpg":  "JPEG",
    ".jpeg": "JPEG",
    ".pdf":  "PDF",
    ".zip":  "ZIP",
    ".docx": "ZIP",
    ".xlsx": "ZIP",
    ".pptx": "ZIP",
    ".jar":  "ZIP",
    ".exe":  "EXE",
    ".dll":  "EXE",
    ".sys":  "EXE",
    ".gif":  "GIF",
    ".gz":   "GZIP",
}

# Above this many bits per byte, data looks compressed or encrypted.
HIGH_ENTROPY = 7.5
# These formats are compressed by design, so high entropy is normal for them.
NATURALLY_COMPRESSED = {"PNG", "JPEG", "GIF", "ZIP", "GZIP", "PDF"}
# Entropy of tiny files isn't meaningful (a 100-byte file can't reach 8.0).
MIN_ENTROPY_SIZE = 1024


def is_high_entropy(entropy, detected, size):
    return (entropy >= HIGH_ENTROPY
            and size >= MIN_ENTROPY_SIZE
            and detected not in NATURALLY_COMPRESSED)


def inspect(item):
    """Print one line for one file. Returns False if the file couldn't be read."""
    try:
        detected = detect_type(item)
        entropy = calculate_entropy(item)
        size = item.stat().st_size
    except OSError as e:
        print(f"[ERROR] {item} -> can't read file ({e.strerror or e})")
        return False

    expected = EXPECTED_TYPE.get(item.suffix.lower())
    status = compute_status(detected, expected)
    ext = f"'{item.suffix}'" if item.suffix else "(no extension)"

    if status is True:
        line = f"[MATCH] {item} -> {detected}"
    elif status is False:
        line = f"[MISMATCH] {item} -> detected : {detected}, expected : {expected}"
    elif detected is None and expected is None:
        line = f"[UNKNOWN] {item} -> no known signature, no expected type for {ext}"
    elif detected is None:
        line = f"[UNKNOWN] {item} -> no known signature, expected : {expected}"
    else:
        line = f"[UNKNOWN] {item} -> detected : {detected}, no expected type for {ext}"

    line += f", entropy : {entropy:.4f}"
    if is_high_entropy(entropy, detected, size):
        line += "  [HIGH ENTROPY: possibly packed or encrypted]"
    print(line)
    return True


def main():
    parser = argparse.ArgumentParser(description="Scan a directory for suspicious files")
    parser.add_argument("directory", help="Directory to inspect")
    args = parser.parse_args()
    target = Path(args.directory)
    if not target.exists():
        print(f"Error: {target} does not exist", file=sys.stderr)
        sys.exit(1)
    if not target.is_dir():
        print(f"Error: {target} is not a directory", file=sys.stderr)
        sys.exit(1)

    errors = 0
    for item in target.rglob("*"):
        if item.is_file() and not inspect(item):
            errors += 1
    if errors:
        print(f"\n{errors} file(s) could not be read", file=sys.stderr)


if __name__ == "__main__":
    main()
