import json
import sys
from pathlib import Path

from oo.pipeline import full_analysis

def main() -> None:
    if len(sys.argv)!=3:
        print("usage: python -m scripts.analyze <suspect.txt> <original.txt>", file=sys.stderr)
        sys.exit(1)
    suspect=Path(sys.argv[1]).read_text(encoding="utf-8")
    orignal=Path(sys.argv[2]).read_text(encoding="utf-8")

    result=full_analysis(suspect, orignal)
    risk=result["risk"]

    print(f"\nRisk: {risk["tier"]} (score {risk["score"]})\n")
    print(result["legal"]["ordinary_observer_narrative"], "\n")
    print("Full result:")
    print(json.dumps(result, indent=2))

if __name__=="__main__":
    main()