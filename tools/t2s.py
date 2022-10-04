"""Traditional Chinese to Simplified Chinese.

Instructions:
```bash
cat books.jsonl | python t2s.py > books_in_simplified_chinese.jsonl
```
"""

import sys
import json

import opencc
from tqdm import tqdm


def main():
    t2s = opencc.OpenCC('t2s')
    conversions = 0
    for line in tqdm(sys.stdin):
        j = json.loads(line)
        simplified_text = t2s.convert(j["text"])
        conversions += sum(1 for a, b in zip(simplified_text, j["text"]) if a != b)
        j["text"] = simplified_text
        print(json.dumps(j, ensure_ascii=False))
    print(f"Traditional Chinese to Simplified Chinese. Conversions: {conversions}", file=sys.stderr)


if __name__ == "__main__":
    main()
