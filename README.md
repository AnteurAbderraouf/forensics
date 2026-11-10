# Forensics: suspicious file scanner

> A Python script that scans a folder for suspicious files.

Built as a learning project for the digital-forensics discipline, not as a production tool.

## What it checks

For every file in the folder (and its subfolders):

- **Extension mismatch.** It reads the file's first bytes (its *magic bytes*) to find its real type, then compares that with what the extension claims. An `invoice.pdf` that is really a Windows executable is reported as a `MISMATCH`.
- **Entropy.** It computes the file's Shannon entropy, from 0 to 8 bits per byte. Above **7.5**, data looks compressed or encrypted, which can mean a packed executable or encrypted payload. Formats that are compressed by design (PNG, JPEG, GIF, ZIP/Office, GZIP, PDF) and files under 1 KiB are not flagged.

Recognized signatures: PNG, JPEG, GIF, PDF, ZIP (incl. `.docx` `.xlsx` `.pptx` `.jar`), EXE/DLL, ELF, GZIP.

## Usage

Requires Python 3.8+, no dependencies.

```bash
python suspects.py <directory>
```

Example output:

```
[MATCH] samples/photo.png -> PNG, entropy : 7.9812
[MISMATCH] samples/invoice.pdf -> detected : EXE, expected : PDF, entropy : 6.1043
[UNKNOWN] samples/blob.bin -> no known signature, no expected type for '.bin', entropy : 7.9969  [HIGH ENTROPY: possibly packed or encrypted]
[ERROR] samples/locked.db -> can't read file (Permission denied)
```

| Status | Meaning |
| --- | --- |
| `MATCH` | Real type matches the extension |
| `MISMATCH` | Real type differs from the extension: worth a look |
| `UNKNOWN` | Signature not recognized, or no expected type for this extension |
| `ERROR` | File couldn't be read. The scan continues. |

## Status

Work in progress.
