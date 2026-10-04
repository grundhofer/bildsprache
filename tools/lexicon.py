#!/usr/bin/env python3
"""Beispielbilder für das Lexikon: ein kleines Bild pro Stil, erzeugt aus seinem Prompt-Baustein.

    python3 tools/lexicon.py plan jobs.json --pilot           # drei Stile pro Kategorie
    python3 tools/lexicon.py plan jobs.json --category cinema # alle offenen Stile einer Kategorie
    python3 tools/lexicon.py plan jobs.json --reroll          # Neuversuch für durchgefallene Bilder
    python3 tools/generate.py jobs.json                       # erzeugt originals/lexicon/<slug>-<n>.png
    python3 tools/lexicon.py manifest                         # wählt pro Stil die geprüfte Fassung
    python3 tools/lexicon.py optimize                         # WebP-Dateien in images/lexicon/

Der Prompt ist wie im Katalog gebaut: 'Style: <prompt_fragment>', dann ein Lexikonmotiv aus
data/lexicon_motifs.json, dann die Leitplanken. Leitstile haben eigene Bilder im Katalog, Stile mit
verdict 'restrict' bekommen keinen Prompt und deshalb auch kein Bild. Geprüft wird leichter als im
Katalog (data/lexicon_qa.json): ein Bild pro Stil, bei 'fail' höchstens ein Neuversuch.
"""
import argparse, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.plan import attempts  # noqa: E402
from tools.prompts import compose  # noqa: E402
from tools import optimize  # noqa: E402

TYPE = "lexicon"
LM = json.loads((ROOT / "data" / "lexicon_motifs.json").read_text())
MOTIFS = {m["id"]: m for m in LM["motifs"]}
QA_FILE = ROOT / "data" / "lexicon_qa.json"
MANIFEST = ROOT / "images" / TYPE / "manifest.json"
RANK = {"pass": 2, "flawed": 1, "fail": 0}
# Erster Versuch plus ein Neuversuch; danach wird auch ein Fehlversuch gezeigt, sichtbar markiert.
MAX_ATTEMPTS = 2
SIZES = {"": (768, 76), ".thumb": (320, 70)}
FEAS = {"high": 0, "medium": 1, "low": 2}


def styles():
    """Alle Lexikonstile, die ein Beispielbild bekommen: ohne verworfene, ohne gesperrte, ohne Leitstile."""
    lead = {p.stem for p in (ROOT / "styles").glob("*.json")}
    lex = json.loads((ROOT / "data" / "lexicon.json").read_text())["styles"]
    return [s for s in lex if s.get("verdict") not in ("drop", "restrict") and s["slug"] not in lead]


def motif_id(s):
    return LM["categories"].get(s["category_id"], LM["default"])


def prompt(s):
    return compose(motif_id(s), s["prompt_fragment"], "en", motifs=MOTIFS)


def pilot(items):
    """Drei Stile pro Kategorie, quer über die Machbarkeit: je der auffälligste aus hoch, mittel, niedrig."""
    out = []
    by = {}
    for s in items:
        by.setdefault(s["category_id"], []).append(s)
    for cat, ss in by.items():
        ss = sorted(ss, key=lambda s: (FEAS.get(s["feasibility"], 1), -s["distinctiveness"], s["slug"]))
        picked = []
        for f in ("high", "medium", "low"):
            pick = next((s for s in ss if s["feasibility"] == f and s not in picked), None)
            if pick:
                picked.append(pick)
        picked += [s for s in ss if s not in picked][: 3 - len(picked)]
        out += picked
    return out


def plan(items, qa=None):
    jobs = []
    for s in items:
        p, _ = prompt(s)
        tries = attempts(TYPE, s["slug"], "en")
        current = [a for a in tries if a[1]["prompt"] == p and a[2].exists()]
        nxt = (tries[-1][0] + 1) if tries else 1
        job = {"type": TYPE, "style": s["slug"], "attempt": nxt, "size": MOTIFS[motif_id(s)]["size"], "prompt": p, "lang": "en"}
        if not current:
            jobs.append(job)
        elif qa is not None:
            verdicts = [qa.get(f"{TYPE}/{a[2].stem}", {}).get("verdict") for a in current]
            if all(v == "fail" for v in verdicts) and len(current) < MAX_ATTEMPTS:
                jobs.append(job)
    return jobs


def build_manifest(qa):
    old = {}
    if MANIFEST.exists():
        old = {e["slug"]: e for e in json.loads(MANIFEST.read_text())["images"]}
    images, missing = [], []
    for s in styles():
        p, parts = prompt(s)
        best, tries = None, 0
        for n, meta, png in attempts(TYPE, s["slug"], "en"):
            q = qa.get(f"{TYPE}/{png.stem}")
            if meta["prompt"] != p or not png.exists() or not q or q.get("verdict") not in RANK:
                continue
            tries += 1
            if best is None or (RANK[q["verdict"]], n) >= (RANK[best[2]["verdict"]], best[0]):
                best = (n, meta, q, png)
        if not best:
            continue
        if best[2]["verdict"] == "fail" and tries < MAX_ATTEMPTS:
            missing.append(s["slug"])
            continue
        n, meta, q, png = best
        discarded = sum(1 for k, mm, pp in attempts(TYPE, s["slug"], "en")
                        if k < n and mm["prompt"] == p and qa.get(f"{TYPE}/{pp.stem}", {}).get("verdict") == "fail")
        e = {"slug": s["slug"], "motif": motif_id(s), "file": png.name, "attempt": n, "discarded": discarded,
             "prompt": p, "parts": {k: v for k, v in parts},
             "size": meta["size"], "generated_at": meta["generated_at"], "tool": meta["tool"],
             "codex_version": meta.get("codex_version", ""),
             "qa": {"verdict": q["verdict"], "note_de": q.get("note_de", ""), "note_en": q.get("note_en", "")},
             "alt_de": q.get("alt_de", ""), "alt_en": q.get("alt_en", "")}
        o = old.get(s["slug"])
        if o and o.get("file") == e["file"]:
            e["width"], e["height"] = o.get("width"), o.get("height")
        images.append(e)
    return images, missing


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    pl = sub.add_parser("plan")
    pl.add_argument("out")
    pl.add_argument("--pilot", action="store_true")
    pl.add_argument("--category")
    pl.add_argument("--slugs", help="kommagetrennt")
    pl.add_argument("--limit", type=int)
    pl.add_argument("--reroll", action="store_true", help="nur Neuversuche für durchgefallene Bilder")
    sub.add_parser("manifest")
    op = sub.add_parser("optimize")
    op.add_argument("--force", action="store_true")
    a = ap.parse_args()
    qa = json.loads(QA_FILE.read_text()) if QA_FILE.exists() else {}

    if a.cmd == "plan":
        items = styles()
        if a.pilot:
            items = pilot(items)
        if a.category:
            items = [s for s in items if s["category_id"] == a.category]
        if a.slugs:
            want = set(a.slugs.split(","))
            items = [s for s in items if s["slug"] in want]
        jobs = plan(items, qa if a.reroll else None)
        if a.reroll:
            jobs = [j for j in jobs if attempts(TYPE, j["style"], "en")]
        if a.limit:
            jobs = jobs[: a.limit]
        pathlib.Path(a.out).write_text(json.dumps(jobs, ensure_ascii=False, indent=1))
        print(len(jobs), "Aufträge")
    elif a.cmd == "manifest":
        images, missing = build_manifest(qa)
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        stats = {"styles": len(styles()), "images": len(images),
                 "calls": sum(1 for p in (optimize.ORIG / TYPE).glob("*.json")) if (optimize.ORIG / TYPE).exists() else 0}
        MANIFEST.write_text(json.dumps({"stats": stats, "images": images}, ensure_ascii=False, indent=1) + "\n")
        print(f"{len(images)} Lexikonbilder im Manifest, {len(missing)} warten auf einen Neuversuch")
    elif a.cmd == "optimize":
        optimize.DONE = json.loads(optimize.DONE_FILE.read_text()) if optimize.DONE_FILE.exists() else {}
        man = json.loads(MANIFEST.read_text())
        n = 0
        for e in man["images"]:
            src = optimize.ORIG / TYPE / e["file"]
            if not src.exists():
                print("fehlt:", src, file=sys.stderr)
                continue
            (w, h), made = optimize.convert(src, ROOT / "images" / TYPE / e["slug"], a.force, sizes=SIZES)
            e["width"], e["height"] = w, h
            n += len(made)
        # Dateien von Stilen, die nicht mehr im Manifest stehen (Prompt geändert, gesperrt, Leitstil geworden), entfernen.
        keep = {e["slug"] for e in man["images"]}
        removed = 0
        for f in sorted((ROOT / "images" / TYPE).glob("*.webp")):
            if f.name.removesuffix(".webp").removesuffix(".thumb") not in keep:
                f.unlink()
                optimize.DONE.pop(str(f.relative_to(ROOT)), None)
                removed += 1
        MANIFEST.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
        optimize.DONE_FILE.write_text(json.dumps(optimize.DONE, indent=1))
        print(f"{n} WebP-Dateien erzeugt, {removed} verwaiste entfernt")


if __name__ == "__main__":
    main()
