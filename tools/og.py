#!/usr/bin/env python3
"""Baut das Social-Preview-Bild og.png (1280x640) aus echten Katalogbildern.

    python3 tools/og.py          # schreibt og.html und rendert og.png mit Chrome (headless)

Gezeigt werden fünf Anwendungen in je einem Leitstil, im Seitenstil Swiss (Schwarz-Weiß, Rot als Signalfarbe).
Die Zahlen kommen aus build.py, damit sie mit der Website übereinstimmen.
og.png liegt im Repo, weil der CI-Runner keinen Browser hat; build.py kopiert es nach docs/.
"""
import html, json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TILES = [("infographic", "infographic", "isotype"), ("poster", "poster", "swiss-international-typographic-style"),
         ("charts", "chart", "du-bois-data-portraits"), ("icons", "icons", "engraved-postage-stamp"),
         ("people", "portrait", "fayum-mummy-portrait")]


def main():
    manifest = {(e["type"], e["style"]) for e in json.loads((ROOT / "images" / "manifest.json").read_text())["images"]
                if e.get("lang", "en") == "en"}
    n_img = len(json.loads((ROOT / "images" / "manifest.json").read_text())["images"])
    n_lex = len(build.LEX_PUBLIC)
    imgs = []
    for uc, motif, slug in TILES:
        if (motif, slug) not in manifest:
            sys.exit(f"Bild fehlt: {motif}/{slug}")
        label = f'{build.UC[uc]["name_de"]} · {build.STYLES[slug]["de"]["name"]}'
        src = (ROOT / "images" / motif / f"{slug}.webp").as_uri()
        imgs.append(f'<figure><img src="{src}" alt=""><figcaption>{html.escape(label)}</figcaption></figure>')
    page = f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap">
<style>
html,body{{margin:0;width:1280px;height:640px;overflow:hidden;background:#FFFFFF;color:#0B0B0B;font-family:Inter,Helvetica,Arial,sans-serif}}
.wrap{{display:grid;grid-template-columns:430px 1fr;height:640px}}
.txt{{padding:44px 36px 40px 48px;display:flex;flex-direction:column;justify-content:space-between}}
.brand{{display:flex;align-items:center;gap:10px;font:700 15px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}}
.brand i{{width:22px;height:22px;background:#C8050F;display:block}}
.eb{{font:500 13px Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;margin-top:44px}}
h1{{font:700 58px/0.98 Inter,sans-serif;letter-spacing:-.045em;margin:14px 0 0}}
h1 em{{font-style:normal;font-weight:400;color:#5E5E5E}}
.ucs{{font:500 15px/1.5 Inter,sans-serif;color:#3A3A3A;margin-top:22px}}
.facts{{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid #0B0B0B}}
.facts div{{padding:12px 10px 0 0}}
.facts b{{display:block;font:700 30px/1.1 Inter,sans-serif;letter-spacing:-.02em}}
.facts span{{display:block;font:500 10.5px Inter,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#5E5E5E;margin-top:3px}}
.grid{{display:grid;grid-template-columns:1.2fr 1fr 1fr;grid-template-rows:minmax(0,1fr) minmax(0,1fr);gap:10px;padding:28px 28px 28px 0;height:640px;box-sizing:border-box}}
figure{{margin:0;position:relative;overflow:hidden;background:#F2F2F2;min-height:0}}
figure:first-child{{grid-row:span 2}}
figure:nth-child(-n+2) img{{object-position:50% 0}}
img{{width:100%;height:100%;object-fit:cover;display:block}}
figcaption{{position:absolute;left:0;bottom:0;background:#0B0B0B;color:#fff;font:500 12px Inter,sans-serif;padding:5px 8px}}
</style></head><body><div class="wrap">
<div class="txt"><div><div class="brand"><i></i>Bildsprache</div><div class="eb">Bildstile für KI-Bilder</div>
<h1>Was willst du <em>erstellen?</em></h1>
<div class="ucs">Infografik, Diagramm, Icons, Porträt,<br>Plakat, Karte und mehr.<br>Prompt, Stil oder Vorlage kopieren.</div></div>
<div class="facts"><div><b>{len(build.USECASES)}</b><span>Anwendungen</span></div><div><b>{n_img}</b><span>Bilder</span></div>
<div><b>{n_lex}</b><span>Stile im Lexikon</span></div></div></div>
<div class="grid">{''.join(imgs)}</div></div></body></html>"""
    out = ROOT / "og.html"
    out.write_text(page, encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=8000",
                    "--allow-file-access-from-files", f"--screenshot={ROOT / 'og.png'}", "--window-size=1280,640",
                    out.as_uri()], check=True, capture_output=True)
    print("og.png geschrieben")


if __name__ == "__main__":
    main()
