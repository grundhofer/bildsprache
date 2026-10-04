#!/usr/bin/env python3
"""Plant Bildaufträge: jede Zelle der Matrix, deren aktueller Prompt noch kein brauchbares Bild hat.

    python3 tools/plan.py jobs.json                 # fehlende Zellen
    python3 tools/plan.py jobs.json --reroll data/qa.json  # zusätzlich Zellen ohne bestandene Fassung (max. 3 Versuche)

Ein Bild zählt nur, wenn sein gespeicherter Prompt exakt dem aktuellen Prompt entspricht. Ändert sich
ein Motiv- oder Stilblock, plant das Werkzeug die betroffenen Zellen deshalb automatisch neu.
"""
import argparse, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.prompts import compose, MOTIFS  # noqa: E402

ORIG = ROOT / "originals"


def cells(include_baselines=True, de_twins=None):
    matrix = json.loads((ROOT / "data" / "matrix.json").read_text())
    sheets = {p.stem: json.loads(p.read_text()) for p in (ROOT / "styles").glob("*.json")}
    out = []
    for t in MOTIFS:
        if include_baselines:
            out += [(t, "baseline", "en", None), (t, "baseline-2", "en", None)]
        for s in matrix["cells"].get(t, []):
            if s in sheets:
                out.append((t, s, "en", sheets[s]["style_block"]))
    for t, s in (de_twins or matrix.get("de_twins", [])):
        block = None if s.startswith("baseline") else sheets.get(s, {}).get("style_block")
        if s.startswith("baseline") or block:
            out.append((t, s, "de", block))
    return out


def attempts(t, s, lang):
    tag = ".de" if lang == "de" else ""
    found = []
    for meta in sorted((ORIG / t).glob(f"{s}{tag}-*.json")):
        stem = meta.stem
        n = stem.rsplit("-", 1)[-1]
        if not n.isdigit() or stem[: -len(n) - 1] != f"{s}{tag}":
            continue
        found.append((int(n), json.loads(meta.read_text()), meta.with_suffix(".png")))
    return sorted(found, key=lambda x: x[0])


def plan(reroll_qa=None):
    qa = json.loads(pathlib.Path(reroll_qa).read_text()) if reroll_qa else {}
    jobs = []
    for t, s, lang, block in cells():
        prompt, _ = compose(t, block, lang)
        tries = attempts(t, s, lang)
        current = [a for a in tries if a[1]["prompt"] == prompt and a[2].exists()]
        nxt = (tries[-1][0] + 1) if tries else 1
        if not current:
            jobs.append({"type": t, "style": s, "attempt": nxt, "size": MOTIFS[t]["size"], "prompt": prompt, "lang": lang})
            continue
        if qa:
            verdicts = [qa.get(f"{t}/{a[2].stem}", {}).get("verdict") for a in current]
            if verdicts and all(v == "fail" for v in verdicts) and len(current) < 3:
                jobs.append({"type": t, "style": s, "attempt": nxt, "size": MOTIFS[t]["size"], "prompt": prompt, "lang": lang})
    return jobs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--reroll")
    a = ap.parse_args()
    jobs = plan(a.reroll)
    pathlib.Path(a.out).write_text(json.dumps(jobs, ensure_ascii=False, indent=1))
    by = {}
    for j in jobs:
        by[j["type"]] = by.get(j["type"], 0) + 1
    print(len(jobs), "Aufträge", by)


if __name__ == "__main__":
    main()
