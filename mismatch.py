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

def compute_status(detected, expected):
    if detected is None or expected is None:
        return None
    elif expected == detected:
        return True
    else:
        return False