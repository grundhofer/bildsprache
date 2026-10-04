"""Datenprüfungen vor dem Build. Jede Funktion liefert eine Liste von Fehlermeldungen.

Die wichtigste Prüfung ist check_prompts: Die Website behauptet, dass der Motivblock pro Motiv
und der Stilblock pro Stil wortgleich sind. Das wird hier für jedes veröffentlichte Bild gegen
data/motifs.json und styles/<slug>.json nachgerechnet.
"""
import json, pathlib, re

SIZES = {"1536x1024", "1024x1536", "1024x1024"}
SHEET_FIELDS = ("name", "summary", "era", "origin", "markers", "escapes", "pitfalls", "tip")
BASELINES = ("baseline", "baseline-2")


def _load(root, rel):
    return json.loads((root / rel).read_text(encoding="utf-8"))


def _text_in_block(text, block):
    """Ein erlaubter Bildtext muss wörtlich im Motivblock stehen: als 'Text', als Schritt 1 'Sow'
    oder als Wert hinter einer Beschriftung wie 'JUN' 12."""
    if f"'{text}'" in block:
        return True
    if text.isdigit():
        return re.search(rf"'[^']+' {text}\b", block) is not None
    num, _, label = text.partition(" ")
    return num.isdigit() and f"{num} '{label}'" in block


def check_motifs(motifs):
    errs, ids = [], set()
    for m in motifs:
        mid = m.get("id", "?")
        if mid in ids:
            errs.append(f"Motiv doppelt: {mid}")
        ids.add(mid)
        for f in ("name_de", "name_en", "summary_de", "summary_en", "tests_de", "tests_en", "motif_en", "size", "tier", "text"):
            if f not in m or m[f] in ("", None):
                errs.append(f"Motiv {mid}: Feld {f} fehlt")
        if m.get("size") not in SIZES:
            errs.append(f"Motiv {mid}: ungültiges Format {m.get('size')}")
        for key, block in (("text", "motif_en"), ("text_de", "motif_de")):
            if m.get(key) and not m.get(block):
                errs.append(f"Motiv {mid}: {key} ohne {block}")
                continue
            for t in m.get(key, []):
                if not _text_in_block(t, m.get(block, "")):
                    errs.append(f"Motiv {mid}: Text '{t}' steht nicht wörtlich in {block}")
        if m.get("text_de") and len(m["text_de"]) != len(m["text"]):
            errs.append(f"Motiv {mid}: text_de und text sind unterschiedlich lang")
    return errs


def check_lexicon(lex):
    errs = []
    fams = {f["id"] for c in lex["categories"] for f in c["families"]}
    cats = {c["id"] for c in lex["categories"]}
    slugs = set()
    for s in lex["styles"]:
        if s["slug"] in slugs:
            errs.append(f"Lexikon: Slug doppelt {s['slug']}")
        slugs.add(s["slug"])
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s["slug"]):
            errs.append(f"Lexikon: ungültiger Slug {s['slug']}")
        if s.get("family_id") not in fams:
            errs.append(f"Lexikon {s['slug']}: unbekannte Familie {s.get('family_id')}")
        if s.get("category_id") not in cats:
            errs.append(f"Lexikon {s['slug']}: unbekannte Kategorie {s.get('category_id')}")
        for f in ("name_de", "name_en", "prompt_fragment", "feasibility", "distinctiveness"):
            if not s.get(f):
                errs.append(f"Lexikon {s['slug']}: Feld {f} fehlt")
    return errs


def check_sheets(sheets, lex_slugs):
    errs = []
    for slug, st in sheets.items():
        if st.get("slug") != slug:
            errs.append(f"Faktenblatt {slug}: slug-Feld passt nicht zum Dateinamen")
        if slug not in lex_slugs:
            errs.append(f"Faktenblatt {slug}: kein Lexikoneintrag")
        if not st.get("style_block") or len(st["style_block"].split()) < 40:
            errs.append(f"Faktenblatt {slug}: Stilblock fehlt oder ist kürzer als 40 Wörter")
        for lang in ("de", "en"):
            d = st.get(lang) or {}
            for f in SHEET_FIELDS:
                if not d.get(f):
                    errs.append(f"Faktenblatt {slug}/{lang}: Feld {f} fehlt")
            if len(d.get("markers", [])) < 3:
                errs.append(f"Faktenblatt {slug}/{lang}: weniger als drei Merkmale")
        if st.get("de", {}).get("markers") and st.get("en", {}).get("markers") and \
                len(st["de"]["markers"]) != len(st["en"]["markers"]):
            errs.append(f"Faktenblatt {slug}: Merkmale de/en unterschiedlich viele")
    return errs


def check_matrix(matrix, motifs, sheets):
    errs = []
    ids = {m["id"] for m in motifs}
    for t, slugs in matrix["cells"].items():
        if t not in ids:
            errs.append(f"Matrix: unbekanntes Motiv {t}")
        if len(slugs) != len(set(slugs)):
            errs.append(f"Matrix {t}: Stil doppelt")
        for s in slugs:
            if s not in sheets:
                errs.append(f"Matrix {t}: Stil {s} ohne Faktenblatt")
    for s in matrix["flagships"]:
        if s not in sheets:
            errs.append(f"Matrix: Leitstil {s} ohne Faktenblatt")
    return errs


def check_prompts(root, manifest, motifs, sheets):
    import sys
    sys.path.insert(0, str(root))
    from tools.prompts import compose
    errs = []
    seen = set()
    for e in manifest:
        key = (e["type"], e["style"], e.get("lang", "en"))
        if key in seen:
            errs.append(f"Manifest: doppelt {key}")
        seen.add(key)
        if e["type"] not in {m["id"] for m in motifs}:
            errs.append(f"Manifest: unbekanntes Motiv {e['type']}")
            continue
        if e["style"] not in BASELINES and e["style"] not in sheets:
            errs.append(f"Manifest {key}: Stil ohne Faktenblatt")
            continue
        block = None if e["style"] in BASELINES else sheets[e["style"]]["style_block"]
        expected, parts = compose(e["type"], block, e.get("lang", "en"))
        if e["prompt"] != expected:
            errs.append(f"Manifest {key}: Prompt weicht vom aktuellen Motiv-/Stilblock ab (neu erzeugen oder Daten prüfen)")
        if {k: v for k, v in parts} != e.get("parts"):
            errs.append(f"Manifest {key}: Prompt-Teile passen nicht zum Prompt")
        lang = ".de" if e.get("lang") == "de" else ""
        for suffix in ("", ".thumb"):
            f = root / "images" / e["type"] / f"{e['style']}{lang}{suffix}.webp"
            if not f.exists():
                errs.append(f"Manifest {key}: Datei fehlt {f.relative_to(root)}")
        for f in ("generated_at", "width", "height", "attempt"):
            if not e.get(f):
                errs.append(f"Manifest {key}: Feld {f} fehlt")
        size = next(m["size"] for m in motifs if m["id"] == e["type"])
        if e.get("width") and e.get("height"):
            want = int(size.split("x")[0]) / int(size.split("x")[1])
            if abs(e["width"] / e["height"] - want) > 0.08:
                errs.append(f"Manifest {key}: Seitenverhältnis {e['width']}x{e['height']} passt nicht zum Format {size}")
    return errs


def check_texts(tells, levers):
    errs = []
    for i, t in enumerate(tells):
        for f in ("tell_de", "tell_en", "why_de", "why_en", "fix_de", "fix_en", "applies_de", "applies_en"):
            if not t.get(f):
                errs.append(f"KI-Merkmal {i + 1}: Feld {f} fehlt")
    axes = {a["id"] for a in levers["axes"]}
    for a in levers["axes"]:
        for f in ("name_de", "name_en", "description_de", "description_en"):
            if not a.get(f):
                errs.append(f"Hebelbereich {a.get('id')}: Feld {f} fehlt")
    for x in levers["levers"]:
        if x.get("axis") not in axes:
            errs.append(f"Hebel {x.get('name_en')}: unbekannter Bereich {x.get('axis')}")
        for f in ("name_de", "name_en", "effect_de", "effect_en", "prompt_phrase"):
            if not x.get(f):
                errs.append(f"Hebel {x.get('name_en')}: Feld {f} fehlt")
    return errs


def check_lexicon_images(root, lex, sheets):
    """Lexikon-Beispielbilder: Prompt = Baustein + Lexikonmotiv + Leitplanken, Dateien vorhanden, keine gesperrten Stile."""
    path = root / "images" / "lexicon" / "manifest.json"
    lm = _load(root, "data/lexicon_motifs.json")
    motifs = {m["id"]: m for m in lm["motifs"]}
    errs = []
    for m in lm["motifs"]:
        if m.get("size") not in SIZES:
            errs.append(f"Lexikonmotiv {m['id']}: ungültiges Format {m.get('size')}")
        for t in m.get("text", []):
            if not _text_in_block(t, m["motif_en"]):
                errs.append(f"Lexikonmotiv {m['id']}: Text '{t}' steht nicht im Motivblock")
    if lm["default"] not in motifs or any(v not in motifs for v in lm["categories"].values()):
        errs.append("Lexikonmotive: Zuordnung verweist auf ein unbekanntes Motiv")
    if not path.exists():
        return errs
    import sys
    sys.path.insert(0, str(root))
    from tools.prompts import compose
    styles = {s["slug"]: s for s in lex["styles"]}
    entries = json.loads(path.read_text(encoding="utf-8"))["images"]
    for e in entries:
        slug = e["slug"]
        s = styles.get(slug)
        if not s or s.get("verdict") in ("drop", "restrict") or slug in sheets:
            errs.append(f"Lexikonbild {slug}: Stil darf kein Lexikonbild haben")
            continue
        mid = lm["categories"].get(s["category_id"], lm["default"])
        if e.get("motif") != mid:
            errs.append(f"Lexikonbild {slug}: falsches Motiv {e.get('motif')}")
            continue
        expected, parts = compose(mid, s["prompt_fragment"], "en", motifs=motifs)
        if e["prompt"] != expected:
            errs.append(f"Lexikonbild {slug}: Prompt weicht von Baustein und Motiv ab (neu erzeugen)")
        if {k: v for k, v in parts} != e.get("parts"):
            errs.append(f"Lexikonbild {slug}: Prompt-Teile passen nicht zum Prompt")
        for suffix in ("", ".thumb"):
            f = root / "images" / "lexicon" / f"{slug}{suffix}.webp"
            if not f.exists():
                errs.append(f"Lexikonbild {slug}: Datei fehlt {f.relative_to(root)}")
        # Maße fehlen, solange die gewählte Fassung nicht umgewandelt ist; sonst läge noch die alte WebP-Datei bereit.
        for f in ("generated_at", "width", "height", "attempt"):
            if not e.get(f):
                errs.append(f"Lexikonbild {slug}: Feld {f} fehlt (tools/lexicon.py optimize ausführen)")
        size = motifs[mid]["size"]
        if e.get("width") and e.get("height"):
            want = int(size.split("x")[0]) / int(size.split("x")[1])
            if abs(e["width"] / e["height"] - want) > 0.08:
                errs.append(f"Lexikonbild {slug}: Seitenverhältnis {e['width']}x{e['height']} passt nicht zum Format {size}")
    known = {e["slug"] for e in entries}
    for f in sorted((root / "images" / "lexicon").glob("*.webp")):
        slug = f.name.removesuffix(".webp").removesuffix(".thumb")
        if slug not in known:
            errs.append(f"Lexikonbild-Datei ohne Manifesteintrag: {f.relative_to(root)} (löschen)")
    return errs


def check_all(root):
    root = pathlib.Path(root)
    motifs = _load(root, "data/motifs.json")["motifs"]
    lex = _load(root, "data/lexicon.json")
    sheets = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((root / "styles").glob("*.json"))}
    matrix = _load(root, "data/matrix.json")
    manifest = _load(root, "images/manifest.json")["images"]
    errs = check_motifs(motifs) + check_lexicon(lex)
    errs += check_sheets(sheets, {s["slug"] for s in lex["styles"]})
    errs += check_matrix(matrix, motifs, sheets)
    errs += check_prompts(root, manifest, motifs, sheets)
    errs += check_texts(_load(root, "data/tells.json")["tells"], _load(root, "data/levers.json"))
    errs += check_lexicon_images(root, lex, sheets)
    return errs
