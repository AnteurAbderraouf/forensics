import argparse
from pathlib import Path

MAGIC_BYTES = {
    b'\x89PNG\r\n\x1a\n': 'PNG',
    b'\xff\xd8\xff':       'JPEG',
    b'%PDF':               'PDF',
    b'PK\x03\x04':         'ZIP',
    b'MZ':                 'MZ',
    b'GIF8':               'GIF',
    b'\x7fELF':            'ELF',
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
            print(item, "->", detect_type(item) or "unknown")

if __name__ == "__main__":
    main()