import argparse
from pathlib import Path

MAGIC_BYTES = {
    b'\x89PNG\r\n\x1a\n': 'PNG',
    b'\xff\xd8\xff':       'JPEG',
    b'%PDF':               'PDF',
    b'PK\x03\x04':         'ZIP',
    b'MZ':                 'EXE',
    b'GIF8':               'GIF',
    b'\x7fELF':            'ELF',
    b'\x1f\x8b':           'GZIP',
}

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

def detect_type(path):
    try:
        with open(path, "rb") as f:
            first_bytes = f.read(8)
    except PermissionError:
        return "Can't open file"
    for magic, filetype in MAGIC_BYTES.items():
        if first_bytes.startswith(magic):
            return filetype
    return None

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
            if detected is None or expected is None:
                print("[UNKNOWN]", item, "-> no signature match", "expected:", expected, "detected:", detected)
            elif expected == detected:
                print("[OK]", item, "->", detected)
            else:
                print("[MISMATCH]", item, "->", detected, "expected:", expected)

if __name__ == "__main__":
    main()