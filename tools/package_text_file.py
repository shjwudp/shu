"""Package text files in jsonl.

Instructions:
```bash
python package_text_file.py --text_file_folders TEXT_FILE_PATH_A TEXT_FILE_PATH_B > books.jsonl
```
"""

import os
import sys
import argparse
import json
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser("Package text files in jsonl.")
    parser.add_argument("--text_file_folders", nargs="+", required=True)
    parser.add_argument("--skip_list_file", type=str)

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    skip_books = {}
    if args.skip_list_file:
        for filename in open(args.skip_list_file):
            skip_books[filename] = True

    for folder in args.text_file_folders:
        print(f"Processing on folder {folder}...", file=sys.stderr)
        for root, _, files in os.walk(folder, topdown=False):
            for filename in tqdm(files):
                if not filename.endswith(".txt"):
                    continue

                if filename in skip_books:
                    continue

                file_path = os.path.join(root, filename)
                try:
                    j = {
                        "name": filename,
                        "text": open(file_path, encoding="utf-8").read(),
                    }
                except:
                    print(f"{file_path} failed parse", file=sys.stderr)
                    raise
                print(json.dumps(j, ensure_ascii=False))


if __name__ == "__main__":
    main()
