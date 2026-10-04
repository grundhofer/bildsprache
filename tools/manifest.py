#!/usr/bin/env python3
"""Baut images/manifest.json aus den Originalen und den Prüfergebnissen.

    python3 tools/manifest.py            # liest data/qa.json

Pro Zelle wird die neueste Fassung mit aktuellem Prompt gewählt, die die Prüfung bestanden hat
(verdict "pass"); gibt es keine, die neueste mit kleineren Abweichungen ("flawed", wird markiert).
Ein Fehlversuch ("fail") erscheint nur, wenn nach drei Versuchen nichts Besseres vorliegt, und ist
dann als Fehlversuch markiert. data/qa.json enthält das Prüfergebnis jeder Fassung, auch der
verworfenen: {"<type>/<datei-stem>": {verdict, note_de, note_en, alt_de, alt_en, ...}}.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.plan import cells, attempts  # noqa: E402
from tools.prompts import compose  # noqa: E402

RANK = {"pass": 2, "flawed": 1, "fail": 0}
# Nach so vielen Versuchen wird auch ein Fehlversuch veröffentlicht, sichtbar markiert, statt die Zelle leer zu lassen.
MAX_ATTEMPTS = 3


def build(qa):
    matrix = json.loads((ROOT / "data" / "matrix.json").read_text())
    ai_default = {(c["type"], c["slug"]) for c in matrix.get("ai_default", [])}
    images, missing = [], []
    for t, s, lang, block in cells():
        prompt, parts = compose(t, block, lang)
        best, tries = None, 0
        for n, meta, png in attempts(t, s, lang):
            if meta["prompt"] != prompt or not png.exists():
                continue
            q = qa.get(f"{t}/{png.stem}")
            if not q or q.get("verdict") not in RANK:
                continue
            tries += 1
            if best is None or (RANK[q["verdict"]], n) >= (RANK[best[2]["verdict"]], best[0]):
                best = (n, meta, q, png)
        if not best or (best[2]["verdict"] == "fail" and tries < MAX_ATTEMPTS):
            missing.append(f"{t}/{s}{'.de' if lang == 'de' else ''}")
            continue
        n, meta, q, png = best
        # Verworfen heißt: frühere Fassung mit demselben Prompt, die die Prüfung nicht bestanden hat.
        # Bilder älterer Blockfassungen zählen nicht dazu (siehe stats.superseded).
        discarded = sum(1 for k, mm, pp in attempts(t, s, lang)
                        if k < n and mm["prompt"] == prompt and qa.get(f"{t}/{pp.stem}", {}).get("verdict") == "fail")
        images.append({
            "type": t, "style": s, "lang": lang, "file": png.name, "attempt": n, "discarded": discarded,
            "prompt": prompt, "parts": {k: v for k, v in parts},
            "size": meta["size"], "generated_at": meta["generated_at"], "tool": meta["tool"],
            "codex_version": meta.get("codex_version", ""),
            "qa": {"verdict": q["verdict"], "note_de": q.get("note_de", ""), "note_en": q.get("note_en", ""),
                   "text_exact": q.get("text_exact")},
            "alt_de": q.get("alt_de", ""), "alt_en": q.get("alt_en", ""),
            "ai_default": (t, s) in ai_default,
        })
    return images, missing


def stats(images):
    """Zahlen für die Methodenseite. Die Originale liegen nicht im Repo, deshalb stehen die Summen im Manifest."""
    orig = ROOT / "originals"
    # originals/lexicon/ enthält die Lexikon-Beispielbilder (tools/lexicon.py), nicht Teil der Katalogzahlen.
    metas = [p for p in orig.rglob("*.json") if not p.name.startswith(".") and p.relative_to(orig).parts[0] != "lexicon"]
    v1 = sum(1 for p in metas if "_v1" in p.parts)
    current = set()
    for t, s, lang, block in cells():
        prompt, _ = compose(t, block, lang)
        for n, meta, png in attempts(t, s, lang):
            if meta["prompt"] == prompt:
                current.add(str(png.with_suffix(".json")))
    superseded = sum(1 for p in metas if "_v1" not in p.parts and str(p) not in current)
    return {"calls": len(metas), "pilot_v1": v1, "superseded": superseded,
            "current": len(current), "rerolls": sum(e["discarded"] for e in images)}


def main():
    qa = json.loads(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "data" / "qa.json").read_text())
    images, missing = build(qa)
    path = ROOT / "images" / "manifest.json"
    old = {}
    if path.exists():
        for e in json.loads(path.read_text())["images"]:
            old[(e["type"], e["style"], e.get("lang", "en"))] = e
    for e in images:  # Maße aus dem letzten optimize-Lauf übernehmen, wenn dieselbe Datei gewählt ist
        o = old.get((e["type"], e["style"], e["lang"]))
        if o and o.get("file") == e["file"]:
            e["width"], e["height"] = o.get("width"), o.get("height")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps({"stats": stats(images), "images": images}, ensure_ascii=False, indent=1) + "\n")
    print(f"{len(images)} Bilder im Manifest, {len(missing)} Zellen ohne veröffentlichbares Bild")
    for m in missing:
        print("  fehlt:", m)


if __name__ == "__main__":
    main()
