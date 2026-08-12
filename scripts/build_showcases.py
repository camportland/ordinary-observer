import json
from pathlib import Path

from oo.cases import CASES
from oo.pipeline import full_analysis

def main() -> None:
    out=[]
    for case in CASES:
        print(f"Analyzing: {case["id"]} ...")
        result=full_analysis(case["work_a"], case["work_b"])
        out.append({
            "id": case["id"],
            "title": case["title"],
            "expected": case["expected"],
            "work_a": case["work_a"],
            "work_b": case["work_b"],
            "analysis": result
        })
    Path("data/showcases.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote data/showcases.json ({len(out)} cases)")

if __name__=="__main__":
    main()