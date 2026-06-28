import argparse
from pathlib import Path

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
            print(item)

if __name__ == "__main__":
    main()