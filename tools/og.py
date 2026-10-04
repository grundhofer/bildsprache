#!/usr/bin/env python3
"""Baut das Social-Preview-Bild og.png (1280x640) aus echten Katalogbildern.

    python3 tools/og.py          # schreibt og.html und rendert og.png mit Chrome (headless)

Gezeigt wird dieselbe Szene ohne Stilangabe und in vier Leitstilen, dazu der Prompt-Aufbau.
og.png liegt im Repo, weil der CI-Runner keinen Browser hat; build.py kopiert es nach docs/.
"""
import html, json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MOTIF = "people"
STYLES = ["ancient-egyptian-wall-painting", "woodcut", "cyanotype", "16-bit-pixel-art"]


def main():
    manifest = {(e["type"], e["style"]): e for e in json.loads((ROOT / "images" / "manifest.json").read_text())["images"]
                if e.get("lang", "en") == "en"}
    sheets = {s: json.loads((ROOT / "styles" / f"{s}.json").read_text()) for s in STYLES}
    lex = json.loads((ROOT / "data" / "lexicon.json").read_text())["styles"]
    n_lex = sum(1 for s in lex if s.get("verdict") != "drop")
    n_img = len(manifest) + sum(1 for e in json.loads((ROOT / "images" / "manifest.json").read_text())["images"]
                                if e.get("lang") == "de")
    tiles = [("baseline", "Ohne Stilangabe")] + [(s, sheets[s]["de"]["name"]) for s in STYLES]
    imgs = []
    for slug, label in tiles:
        e = manifest.get((MOTIF, slug))
        if not e:
            sys.exit(f"Bild fehlt: {MOTIF}/{slug}")
        src = (ROOT / "images" / MOTIF / f"{slug}.webp").as_uri()
        imgs.append(f'<figure><img src="{src}" alt=""><figcaption>{html.escape(label)}</figcaption></figure>')
    page = f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans+Condensed:wght@700&family=Newsreader:ital,opsz,wght@1,6..72,400&display=swap">
<style>
html,body{{margin:0;width:1280px;height:640px;overflow:hidden;background:#ECE9E2;color:#1B1A17}}
.wrap{{display:grid;grid-template-columns:400px 1fr;height:640px}}
.txt{{padding:48px 36px 40px 48px;display:flex;flex-direction:column;justify-content:space-between}}
.eb{{font:500 13px 'IBM Plex Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:#7A5C22}}
h1{{font:700 62px/0.95 'IBM Plex Sans Condensed',sans-serif;letter-spacing:-.02em;margin:14px 0 0}}
h1 em{{display:block;font:italic 400 40px/1.1 'Newsreader',serif;color:#524E47;letter-spacing:0;margin-top:10px}}
.anat{{display:grid;gap:6px;font:500 13px 'IBM Plex Mono',monospace}}
.anat span{{padding:7px 10px;border-left:4px solid}}
.s{{background:#F3DED6;border-color:#8A3324}} .m{{background:#E4E1DA;border-color:#5A554D}} .g{{background:#EDE3C9;border-color:#7A5C22}}
.facts{{font:500 13px 'IBM Plex Mono',monospace;color:#5A554D}}
.grid{{display:grid;grid-template-columns:1.25fr 1fr 1fr;grid-template-rows:1fr 1fr;gap:8px;padding:24px 24px 24px 0}}
figure{{margin:0;position:relative;overflow:hidden;background:#F7F5F0}}
figure:first-child{{grid-row:span 2}}
figure:first-child img{{object-position:22% 50%}}
img{{width:100%;height:100%;object-fit:cover;display:block}}
figcaption{{position:absolute;left:8px;bottom:8px;background:rgba(27,26,23,.82);color:#fff;font:500 12px 'IBM Plex Mono',monospace;padding:4px 7px;letter-spacing:.04em}}
</style></head><body><div class="wrap">
<div class="txt"><div><div class="eb">Stilkatalog für KI-Bilder</div><h1>Bildsprache<em>Ein Motiv, viele Bildsprachen.</em></h1></div>
<div class="anat"><span class="s">Stilblock</span><span class="m">Motivblock, immer gleich</span><span class="g">Leitplanken</span></div>
<div class="facts">16 Motive · {n_img} Bilder · {n_lex:,} Stile im Lexikon</div></div>
<div class="grid">{''.join(imgs)}</div></div></body></html>"""
    page = page.replace(f"{n_lex:,}", f"{n_lex:,}".replace(",", "."))
    out = ROOT / "og.html"
    out.write_text(page, encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=8000",
                    "--allow-file-access-from-files", f"--screenshot={ROOT / 'og.png'}", "--window-size=1280,640",
                    out.as_uri()], check=True, capture_output=True)
    print("og.png geschrieben")


if __name__ == "__main__":
    main()
