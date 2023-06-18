"""Package books.

```bash
python package_books.py \
    --books_folder ../books \
    --index_file ../index.csv \
    --output_folder ./books_dataset
```
"""

import os
import sys
import argparse
import json
import csv
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser("Package books.")
    parser.add_argument("--books_folder", required=True)
    parser.add_argument("--index_file", default=None)
    parser.add_argument("--output_folder", default="./books_dataset")
    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    index = {}
    if args.index_file:
        with open(args.index_file, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                index[row["书名"]] = row

    os.mkdir(args.output_folder)

    # Output dataset
    data_file = open(os.path.join(args.output_folder, "books.jsonl"), "w")
    for root, _, files in os.walk(args.books_folder, topdown=False):
        print(f"Process folder {root}...")
        for filename in tqdm(files):
            if not filename.endswith(".txt"):
                continue

            book_name = filename[:-len(".txt")]
            if args.index_file:
                if book_name not in index:
                    continue

            file_path = os.path.join(root, filename)
            try:
                j = {
                    "name": book_name,
                    "text": open(file_path, encoding="utf-8").read(),
                }
            except:
                print(f"Parsing {file_path} failed, skipped", file=sys.stderr)
            print(json.dumps(j, ensure_ascii=False), file=data_file)
            if not args.index_file:
                index[book_name] = {"书名", book_name}

    # Output dataset index file
    fields = ["书名", "Book Title", "Author", "Publication Date"]
    csvfile = open(os.path.join(args.output_folder, "index.csv"), "w")
    writer = csv.DictWriter(csvfile, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(index.values())


if __name__ == "__main__":
    main()
