#!/usr/bin/env python3
"""Wandelt die ausgewählten Originale in WebP für die Website um.

    python3 tools/optimize.py            # alle in images/manifest.json gewählten Bilder
    python3 tools/optimize.py --force    # vorhandene WebP-Dateien neu erzeugen

Quelle: originals/<type>/<file>.png (nicht eingecheckt). Ziel: images/<type>/<style>[.de].webp
(lange Kante 1280 px) und .thumb.webp (lange Kante 560 px). Braucht cwebp und sips (macOS);
der CI-Build braucht beides nicht, weil die WebP-Dateien eingecheckt sind.
"""
import argparse, json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ORIG, IMG = ROOT / "originals", ROOT / "images"
SIZES = {"": (1280, 78), ".thumb": (560, 72)}
# Merkt sich, aus welchem Original jede WebP-Datei stammt; wechselt die gewählte Fassung, wird neu umgewandelt.
DONE_FILE = ORIG / ".converted.json"
DONE = {}


def dims(png):
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(png)],
                         capture_output=True, text=True, check=True).stdout.split()
    return int(out[out.index("pixelWidth:") + 1]), int(out[out.index("pixelHeight:") + 1])


def convert(png, dest_base, force, sizes=SIZES):
    w, h = dims(png)
    made = []
    for suffix, (edge, q) in sizes.items():
        dest = dest_base.with_name(dest_base.name + suffix + ".webp")
        key = str(dest.relative_to(ROOT))
        if dest.exists() and not force and DONE.get(key) == png.name:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        rw, rh = (edge, 0) if w >= h else (0, edge)
        if max(w, h) <= edge:
            rw, rh = 0, 0
        subprocess.run(["cwebp", "-quiet", "-q", str(q), "-m", "6", "-metadata", "none",
                        "-resize", str(rw), str(rh), str(png), "-o", str(dest)], check=True)
        DONE[key] = png.name
        made.append(dest)
    return (w, h), made


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    global DONE
    DONE = json.loads(DONE_FILE.read_text()) if DONE_FILE.exists() else {}
    manifest_path = IMG / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    n = 0
    for entry in manifest["images"]:
        src = ORIG / entry["type"] / entry["file"]
        lang = ".de" if entry.get("lang") == "de" else ""
        dest = IMG / entry["type"] / f"{entry['style']}{lang}"
        if not src.exists():
            if not dest.with_name(dest.name + ".webp").exists():
                print("fehlt:", src, file=sys.stderr)
            continue
        (w, h), made = convert(src, dest, a.force)
        entry["width"], entry["height"] = w, h
        n += len(made)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n")
    DONE_FILE.write_text(json.dumps(DONE, indent=1))
    print(f"{n} WebP-Dateien erzeugt")


if __name__ == "__main__":
    sys.exit(main())
