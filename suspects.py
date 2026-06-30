import argparse
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
    ".gz":  "GZIP",
}

def main():
    parser = argparse.ArgumentParser(description="Tool that inspects a directory")
    parser.add_argument("directory", help="Directory to inspect")
    args = parser.parse_args()
    target = Path(args.directory)
    if not target.exists():
        print(f"Error: {target} does not exist")
        return
    if not target.is_dir():
        print(f"Error: {target} is not a directory")
        return
    for item in target.rglob("*"):
        if item.is_file():
            detected = detect_type(item)
            expected = EXPECTED_TYPE.get(item.suffix.lower())
            status = compute_status(detected, expected)
            entropy = calculate_entropy(item)
            if status is None:
                print(f"[UNKNOWN] {item} -> no signature match, expected : {expected}, detected : {detected}, {entropy:.4f}")
            elif status is True:
                print(f"[MATCH] {item} -> {detected}, {entropy:.4f}")
            else:
                print(f"[MISMATCH] {item} -> {detected}, expected : {expected}, {entropy:.4f}")

if __name__ == "__main__":
    main()