import json
import sys
from pathlib import Path
from .engine import analyze

def main() -> None:
    if len(sys.argv) != 3:
        print("usage: python -, oo.cli <work_a.txt> <work_b.txt>", file=sys.stderr)
        sys.exit(1)
    text_a=Path(sys.argv[1]).read_text(encoding="utf-8")
    text_b=Path(sys.argv[2]).read_text(encoding="utf-8")
    print(json.dumps(analyze(text_a, text_b), indent=2))

if __name__=="__main__":
    main()
