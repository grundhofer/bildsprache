#!/usr/bin/env python3
"""Baut die Website Bildsprache nach docs/.

    python3 build.py

Quellen:
  data/motifs.json      16 Referenzmotive: Motivblock, Texte, Format
  data/matrix.json      welche Stile auf welchem Motiv gezeigt werden
  data/lexicon.json     alle Stile mit Prompt-Baustein, 14 Kategorien, 119 Familien
  data/tells.json       KI-Merkmale und Gegenhebel
  data/levers.json      Stilhebel
  styles/<slug>.json    Faktenblätter der Leitstile (de + en, Stilblock)
  images/manifest.json  jedes veröffentlichte Bild mit Prompt und Metadaten
  web/                  Seitenstil, Seitenskript, Theme

Der Build bricht ab, wenn Daten fehlen oder nicht zusammenpassen (tools/checks.py),
statt eine halbe Seite auszuliefern.

Build the bilingual Bildsprache site. See README.md.
"""
import html, json, pathlib, shutil, sys

from web import theme
from tools.checks import check_all

ROOT = pathlib.Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE_URL = "https://grundhofer.github.io/bildsprache"
REPO_URL = "https://github.com/grundhofer/bildsprache"
SIBLING_URL = "https://grundhofer.github.io/designsprache/"
LANGS = ("de", "en")
SEG = {
    "motifs": {"de": "motive", "en": "motifs"},
    "styles": {"de": "stile", "en": "styles"},
    "lexicon": {"de": "lexikon", "en": "lexicon"},
    "levers": {"de": "hebel", "en": "levers"},
    "method": {"de": "methode", "en": "method"},
}
AR = {"1536x1024": "ar-landscape", "1024x1536": "ar-portrait", "1024x1024": "ar-square"}
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600'
         '&family=IBM+Plex+Sans+Condensed:wght@400;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;'
         '1,6..72,400&display=swap">')
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' fill='%238A3324'/%3E%3Crect x='6' y='6' width='9' height='20' fill='%23F7F5F0'/%3E"
           "%3Ccircle cx='22' cy='11' r='5' fill='%23F7F5F0'/%3E%3Cpath d='M17 26l5-9 5 9z' fill='%23F7F5F0'/%3E%3C/svg%3E")
LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" fill="var(--accent)"/>'
        '<rect x="6" y="6" width="9" height="20" fill="var(--surface)"/><circle cx="22" cy="11" r="5" fill="var(--surface)"/>'
        '<path d="M17 26l5-9 5 9z" fill="var(--surface)"/></svg>')


def asset_version(name):
    """Kurzer Inhalts-Hash, damit Browser und Pages-Cache nach einer Änderung die neue Datei laden."""
    import hashlib
    return hashlib.sha1((ROOT / "web" / name).read_bytes()).hexdigest()[:10]


def jload(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def h(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def jscript(obj, id_):
    text = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/json" id="{id_}">{text}</script>'


# ---------------------------------------------------------------------------
# Daten
# ---------------------------------------------------------------------------
MOTIFS = jload("data/motifs.json")["motifs"]
MOTIF = {m["id"]: m for m in MOTIFS}
LEXDATA = jload("data/lexicon.json")
CATS = LEXDATA["categories"]
CAT = {c["id"]: c for c in CATS}
FAM = {f["id"]: (c, f) for c in CATS for f in c["families"]}
LEX = {s["slug"]: s for s in LEXDATA["styles"]}
LEX_PUBLIC = [s for s in LEXDATA["styles"] if s.get("verdict") != "drop"]
MATRIX = jload("data/matrix.json")
STYLES = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "styles").glob("*.json"))}
_MANIFEST = jload("images/manifest.json")
MANIFEST = _MANIFEST["images"]
STATS = _MANIFEST.get("stats", {})
IMG = {(e["type"], e["style"], e.get("lang", "en")): e for e in MANIFEST}
TELLS = jload("data/tells.json")["tells"]
LEVERS = jload("data/levers.json")["levers"]
AXES = jload("data/levers.json")["axes"]

AI_DEFAULT_STYLES = {c["slug"] for c in MATRIX.get("ai_default", [])}
N_IMAGES = len(MANIFEST)
N_LEX = len(LEX_PUBLIC)
LEAD = [s for s in STYLES]                       # Leitstile mit Faktenblatt
N_LEAD = len(LEAD)


def pub_images(type_id, lang=None):
    """Veröffentlichte Stilbilder eines Motivs in der Reihenfolge der Matrix."""
    out = []
    for slug in MATRIX["cells"].get(type_id, []):
        e = IMG.get((type_id, slug, "en"))
        if e:
            out.append(e)
    return out


def style_images(slug):
    return [IMG[(m["id"], slug, "en")] for m in MOTIFS if (m["id"], slug, "en") in IMG]


# ---------------------------------------------------------------------------
# Texte der Oberfläche
# ---------------------------------------------------------------------------
UI = {
 "de": {
  "brand_tag": "Ein Motiv, viele Bildsprachen",
  "nav_home": "Start", "nav_motifs": "Motive", "nav_styles": "Leitstile", "nav_lexicon": "Lexikon",
  "nav_levers": "KI-Look & Hebel", "nav_method": "Methode", "other_lang": "English", "skip": "Zum Inhalt springen",
  "baseline": "Ohne Stilangabe", "baseline_2": "Ohne Stilangabe, zweiter Lauf",
  "images": "Bilder", "image": "Bild", "styles_n": "Stile", "lead_styles": "Leitstile", "motifs_n": "Motive",
  "in_lexicon": "Stile im Lexikon", "categories": "Kategorien", "all": "Alle",
  "copy_prompt": "Prompt kopieren", "copy_style": "Nur Stilblock kopieren", "copy_motif": "Motivblock kopieren",
  "copy_block": "Stilblock kopieren", "compare": "Neben „Ohne Stilangabe“ legen", "prev": "Vorheriges Bild", "next": "Nächstes Bild",
  "close": "Schließen", "download": "Bild öffnen",
  "part_style": "Stil", "part_motif": "Motiv (bei allen Bildern dieses Motivs gleich)", "part_guards": "Leitplanken",
  "legend_style": "Stilblock", "legend_motif": "Motivblock", "legend_guards": "Leitplanken",
  "tool": "Werkzeug", "date": "Erzeugt", "format": "Format", "attempt": "Versuch", "lang_in_image": "Text im Bild",
  "tier1": "Kernmotiv", "tier2": "Weiteres Motiv", "tier3": "Ergänzung",
  "ai_label": "Alle Bilder sind KI-generiert (OpenAI-Bildgenerierung über Codex CLI).",
  "license": "Code MIT · Texte CC BY 4.0 · Bilder CC0",
  "sibling": "Schwesterprojekt: Designsprache",
  "feas_high": "hoch", "feas_medium": "mittel", "feas_low": "niedrig",
  "flawed": "Abweichung", "failed": "Fehlversuch", "ai_default": "KI-Standard",
 },
 "en": {
  "brand_tag": "One motif, many visual languages",
  "nav_home": "Home", "nav_motifs": "Motifs", "nav_styles": "Lead styles", "nav_lexicon": "Lexicon",
  "nav_levers": "AI look & levers", "nav_method": "Method", "other_lang": "Deutsch", "skip": "Skip to content",
  "baseline": "No style given", "baseline_2": "No style given, second run",
  "images": "images", "image": "image", "styles_n": "styles", "lead_styles": "lead styles", "motifs_n": "motifs",
  "in_lexicon": "styles in the lexicon", "categories": "categories", "all": "All",
  "copy_prompt": "Copy prompt", "copy_style": "Copy style block only", "copy_motif": "Copy motif block",
  "copy_block": "Copy style block", "compare": "Compare with “No style given”", "prev": "Previous image", "next": "Next image",
  "close": "Close", "download": "Open image",
  "part_style": "Style", "part_motif": "Motif (identical for every image of this motif)", "part_guards": "Guards",
  "legend_style": "Style block", "legend_motif": "Motif block", "legend_guards": "Guards",
  "tool": "Tool", "date": "Generated", "format": "Format", "attempt": "Attempt", "lang_in_image": "Text in image",
  "tier1": "Core motif", "tier2": "Further motif", "tier3": "Addition",
  "ai_label": "All images are AI-generated (OpenAI image generation via Codex CLI).",
  "license": "Code MIT · texts CC BY 4.0 · images CC0",
  "sibling": "Sibling project: Designsprache",
  "feas_high": "high", "feas_medium": "medium", "feas_low": "low",
  "flawed": "Deviation", "failed": "Failed attempt", "ai_default": "AI default",
 },
}
JS_TEXT = {
 "de": {"copied": "Kopiert", "copyFailed": "Kopieren fehlgeschlagen", "image": "Bild", "images": "Bilder",
        "baseline": "Ohne Stilangabe", "compareSlider": "Vergleich: Stil und Bild ohne Stilangabe",
        "part_style": "Stil", "part_motif": "Motiv", "part_guards": "Leitplanken",
        "copyFragment": "Baustein kopieren", "feasibility": "Machbarkeit", "distinct": "Abstand zum KI-Look",
        "feas_high": "hoch", "feas_medium": "mittel", "feas_low": "niedrig", "withImages": "Leitstil mit Bildern", "noFragment": "Kein Prompt-Baustein: Diese Tradition ist an eine Gemeinschaft oder an religiöse Bedeutung gebunden. Der Eintrag dient nur zur Information.",
        "style": "Stil", "styles": "Stile", "showMore": "{n} weitere anzeigen", "loadFailed": "Lexikon konnte nicht geladen werden."},
 "en": {"copied": "Copied", "copyFailed": "Copy failed", "image": "image", "images": "images",
        "baseline": "No style given", "compareSlider": "Comparison: style and image without a style",
        "part_style": "Style", "part_motif": "Motif", "part_guards": "Guards",
        "copyFragment": "Copy fragment", "feasibility": "Feasibility", "distinct": "Distance from the AI look",
        "feas_high": "high", "feas_medium": "medium", "feas_low": "low", "withImages": "Lead style with images", "noFragment": "No prompt fragment: this tradition is bound to a community or to religious meaning. The entry is for information only.",
        "style": "style", "styles": "styles", "showMore": "Show {n} more", "loadFailed": "The lexicon could not be loaded."},
}


def num(n, lang):
    return f"{n:,}".replace(",", "." if lang == "de" else ",")


# ---------------------------------------------------------------------------
# Pfade
# ---------------------------------------------------------------------------
def path(lang, kind, ident=None):
    """Pfad relativ zu docs/, immer mit abschließendem Schrägstrich."""
    if kind == "home":
        return f"{lang}/"
    base = f"{lang}/{SEG[{'motif': 'motifs', 'style': 'styles'}.get(kind, kind)][lang]}/"
    return base + (f"{ident}/" if ident else "")


def rel(src, dst):
    return "../" * src.count("/") + dst


def other(lang):
    return "en" if lang == "de" else "de"


def style_name(slug, lang):
    if slug in ("baseline", "baseline-2"):
        return UI[lang][slug.replace("-", "_")]
    if slug in STYLES:
        return STYLES[slug][lang]["name"]
    s = LEX[slug]
    return s["name_de"] if lang == "de" else s["name_en"]


def style_cat(slug, lang):
    s = LEX.get(slug)
    if not s:
        return ""
    c, f = FAM[s["family_id"]]
    return c[f"name_{lang}"]


def img_src(e, page, thumb=False):
    lang = ".de" if e.get("lang") == "de" else ""
    return rel(page, f"images/{e['type']}/{e['style']}{lang}{'.thumb' if thumb else ''}.webp")


def thumb_dims(e):
    w, hgt = e.get("width") or 1536, e.get("height") or 1024
    k = 560 / max(w, hgt)
    return round(w * k), round(hgt * k)


def alt(e, lang):
    a = e.get(f"alt_{lang}")
    if a:
        return a
    return f"{style_name(e['style'], lang)}: {MOTIF[e['type']][f'summary_{lang}']}"


def cell_data(e, lang, page):
    """Daten für die Lightbox."""
    m = MOTIF[e["type"]]
    ui = UI[lang]
    parts = [[k, e["parts"][k]] for k in ("style", "motif", "guards") if e["parts"].get(k)]
    is_base = e["style"].startswith("baseline")
    base = None if is_base else (IMG.get((e["type"], "baseline", e.get("lang", "en"))) or IMG.get((e["type"], "baseline", "en")))
    disc = e.get("discarded", 0)
    att_txt = (f"{disc + 1}" + (f" ({disc} verworfen)" if lang == "de" else f" ({disc} discarded)")) if disc else "1"
    meta = [[ui["tool"], "Codex CLI · image_gen (OpenAI)"],
            [ui["date"], e["generated_at"][:10]],
            [ui["format"], f"{e.get('width')}×{e.get('height')}"],
            [ui["attempt"], att_txt]]
    if m["text"]:
        names = {"de": {"de": "Deutsch", "en": "Englisch"}, "en": {"de": "German", "en": "English"}}[lang]
        meta.append([ui["lang_in_image"], names[e.get("lang", "en")]])
    qa = e.get("qa") or {}
    href = None if is_base else rel(page, path(lang, "style", e["style"]))
    if e["style"] in STYLES or is_base:
        pass
    else:
        href = None
    return {
        "src": img_src(e, page), "alt": alt(e, lang), "w": e.get("width"), "h": e.get("height"), "ar": AR[m["size"]],
        "title": style_name(e["style"], lang), "href": href,
        "eyebrow": m[f"name_{lang}"] + (" · " + style_cat(e["style"], lang) if not is_base else ""),
        "sub": "", "parts": parts, "prompt": e["prompt"],
        "styleBlock": e["parts"].get("style", "").removeprefix("Style: ") or None,
        "meta": meta,
        "note": (UI[lang]["failed" if qa.get("verdict") == "fail" else "flawed"] + ": " + qa[f"note_{lang}"])
                if qa.get(f"note_{lang}") and qa.get("verdict") in ("fail", "flawed") else "",
        "base": img_src(base, page) if base else None, "baseAlt": alt(base, lang) if base else "",
    }


# ---------------------------------------------------------------------------
# Seitenrahmen
# ---------------------------------------------------------------------------
def head(lang, page, title, desc, kind):
    alt_page = PAGE_TWIN(lang, page)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{h(title)}</title>
<meta name="description" content="{h(desc)}">
<meta name="author" content="Sebastian Grundhöfer">
<link rel="canonical" href="{SITE_URL}/{page}">
<link rel="alternate" hreflang="{lang}" href="{SITE_URL}/{page}">
<link rel="alternate" hreflang="{other(lang)}" href="{SITE_URL}/{alt_page}">
<meta property="og:type" content="website">
<meta property="og:title" content="{h(title)}">
<meta property="og:description" content="{h(desc)}">
<meta property="og:url" content="{SITE_URL}/{page}">
<meta property="og:locale" content="{'de_DE' if lang == 'de' else 'en_US'}">
<meta property="og:image" content="{SITE_URL}/og.png">
<meta property="og:image:width" content="1280">
<meta property="og:image:height" content="640">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{FAVICON}">
{FONTS}
{theme.script()}<style>{theme.css()}</style>
<link rel="stylesheet" href="{rel(page, 'assets/site.css')}?v={asset_version('site.css')}">
</head>
<body data-page="{kind}">
<a class="skip" href="#main">{UI[lang]['skip']}</a>
{topbar(lang, page, kind)}
<main id="main">
"""


def topbar(lang, page, kind):
    ui = UI[lang]
    items = [("home", "nav_home"), ("motifs", "nav_motifs"), ("styles", "nav_styles"),
             ("lexicon", "nav_lexicon"), ("levers", "nav_levers"), ("method", "nav_method")]
    nav = "".join(
        f'<a href="{rel(page, path(lang, k))}"{" aria-current=\"page\"" if k == kind or (kind == "motif" and k == "motifs") or (kind == "style" and k == "styles") else ""}>{ui[l]}</a>'
        for k, l in items if k != "home")
    twin = PAGE_TWIN(lang, page)
    return f"""<header class="topbar"><div class="wrap topbar-in">
<a class="tb-brand" href="{rel(page, path(lang, 'home'))}">{LOGO}Bildsprache</a>
<nav class="tb-nav" aria-label="{'Hauptnavigation' if lang == 'de' else 'Main navigation'}">{nav}</nav>
<div class="tb-end"><span class="tb-lang"><a href="{rel(page, twin)}" hreflang="{other(lang)}" lang="{other(lang)}">{ui['other_lang']}</a></span>{theme.controls(lang)}</div>
</div></header>"""


def foot(lang, page):
    ui = UI[lang]
    return f"""</main>
<footer class="foot"><div class="wrap foot-in">
<span>© Sebastian Grundhöfer</span>
<span class="ai-label">{ui['ai_label']}</span>
<span>{ui['license']}</span>
<a href="{REPO_URL}" rel="noopener">GitHub</a>
<a href="{SIBLING_URL}{lang}/" rel="noopener">{ui['sibling']}</a>
</div></footer>
<p class="sr-only" role="status" id="status"></p>
{jscript(JS_TEXT[lang], 'i18n')}
<script src="{rel(page, 'assets/site.js')}?v={asset_version('site.js')}" defer></script>
</body>
</html>
"""


def lightbox(lang):
    ui = UI[lang]
    return f"""<dialog class="lb" id="lb" aria-labelledby="lb-title">
<div class="lb-in">
<figure class="lb-fig"></figure>
<div class="lb-side">
<div class="lb-top"><div class="lb-nav">
<button type="button" class="btn" data-lb-prev aria-label="{ui['prev']}">←</button>
<button type="button" class="btn" data-lb-next aria-label="{ui['next']}">→</button></div>
<button type="button" class="btn" data-lb-close>{ui['close']}</button></div>
<div><div class="eyebrow lb-eyebrow"></div><h2 class="lb-title" id="lb-title"></h2><p class="lb-sub muted"></p>
<p class="sr-only lb-live" aria-live="polite"></p></div>
<div class="actions">
<button type="button" class="btn primary" data-lb-copy-all>{ui['copy_prompt']}</button>
<button type="button" class="btn" data-lb-copy-style>{ui['copy_style']}</button>
<button type="button" class="btn" data-lb-compare aria-pressed="false">{ui['compare']}</button>
<a class="btn" data-lb-download href="#" target="_blank" rel="noopener">{ui['download']}</a></div>
<p class="note lb-note" hidden></p>
<div class="anat"></div>
<dl class="lb-meta"></dl>
</div></div>
</dialog>"""


def fact(value, label):
    """Kennzahl; Text und lange Werte in kleinerer Schrift, damit nichts in die Nachbarzelle läuft."""
    v = str(value)
    small = len(v) > 5 or not v[:1].isdigit()
    return f'<div><b{" class=\"t\"" if small else ""}>{h(v)}</b><span>{h(label)}</span></div>'


def card(e, idx, lang, page, show="style", link=True):
    """Eine Bildkarte. show='style' zeigt den Stilnamen, show='motif' den Motivnamen."""
    m = MOTIF[e["type"]]
    tw, th = thumb_dims(e)
    is_base = e["style"].startswith("baseline")
    if show == "motif":
        title = h(m[f"name_{lang}"])
        sub = h(style_name(e["style"], lang)) if is_base else ""
        title_html = f'<a href="{rel(page, path(lang, "motif", m["id"]))}">{title}</a>' if link else title
    else:
        title = h(style_name(e["style"], lang))
        sub = h(UI[lang]["baseline"] if is_base else style_cat(e["style"], lang))
        title_html = (f'<a href="{rel(page, path(lang, "style", e["style"]))}">{title}</a>'
                      if link and e["style"] in STYLES else title)
    flag = ""
    if e.get("ai_default"):
        flag = f'<span class="flag warn">{UI[lang]["ai_default"]}</span>'
    elif (e.get("qa") or {}).get("verdict") == "fail":
        flag = f'<span class="flag warn">{UI[lang]["failed"]}</span>'

    cat = LEX[e["style"]]["category_id"] if e["style"] in LEX else "baseline"
    return (f'<figure class="card {AR[m["size"]]}{" base" if is_base else ""}" data-cat="{cat}">'
            f'<button type="button" data-cell="{idx}">'
            f'<img src="{img_src(e, page, True)}" width="{tw}" height="{th}" loading="lazy" decoding="async" alt="{h(alt(e, lang))}">{flag}</button>'
            f'<figcaption><b>{title_html}</b><span>{sub}</span></figcaption></figure>')


def anatomy(parts, lang):
    ui = UI[lang]
    segs = "".join(f'<div class="seg seg-{k}"><i>{ui["part_" + k]}</i><span lang="en">{h(t)}</span></div>' for k, t in parts)
    return (f'<div class="anat-legend"><span class="k-style">{ui["legend_style"]}</span>'
            f'<span class="k-motif">{ui["legend_motif"]}</span><span class="k-guards">{ui["legend_guards"]}</span></div>'
            f'<div class="anat">{segs}</div>')


# ---------------------------------------------------------------------------
# Seiteninhalte (Texte in COPY, Aufbau hier)
# ---------------------------------------------------------------------------
from web.copy import COPY  # noqa: E402  (Fließtexte der Seiten, zweisprachig)


def PAGE_TWIN(lang, page):
    """Gegenstück einer Seite in der anderen Sprache."""
    o = other(lang)
    parts = page.split("/")
    parts[0] = o
    if len(parts) > 2 and parts[1]:
        for key, seg in SEG.items():
            if parts[1] == seg[lang]:
                parts[1] = seg[o]
    return "/".join(parts)


def write(page, text):
    out = DOCS / page / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return out


def page_home(lang):
    page = path(lang, "home")
    c = COPY[lang]["home"]
    ui = UI[lang]
    cells, idx = [], 0
    out = [head(lang, page, c["title"], c["desc"], "home")]
    facts = [(len(MOTIFS), ui["motifs_n"]), (N_IMAGES, ui["images"]), (N_LEAD, ui["lead_styles"]), (N_LEX, ui["in_lexicon"])]
    out.append(f"""<section class="mast"><div class="wrap mast-in">
<div><p class="eyebrow">{c['eyebrow']}</p><h1>{c['h1']}</h1><p class="lede">{c['lede']}</p></div>
<div class="facts">{''.join(f'<div><b>{num(n, lang)}</b><span>{h(l)}</span></div>' for n, l in facts)}</div>
</div></section>""")

    # Vergleichsregler: Szene mit Menschen, Leitstile gegen die Basislinie
    hero_type = "people"
    base = IMG.get((hero_type, "baseline", "en"))
    picks = [IMG[(hero_type, s, "en")] for s in MATRIX["flagships"] if (hero_type, s, "en") in IMG]
    if base and picks:
        first = picks[0]
        chips = "".join(
            f'<button type="button" class="chip" data-hero-pick="hero" aria-pressed="{str(i == 0).lower()}" '
            f'data-src="{img_src(e, page)}" data-alt="{h(alt(e, lang))}" data-label="{h(style_name(e["style"], lang))}" '
            f'data-href="{rel(page, path(lang, "style", e["style"]))}">{h(style_name(e["style"], lang))}</button>'
            for i, e in enumerate(picks))
        out.append(f"""<section class="sec"><div class="wrap hero">
<div class="cmp ar-landscape" id="hero"><img src="{img_src(base, page)}" alt="{h(alt(base, lang))}" width="{base.get('width')}" height="{base.get('height')}">
<div class="cmp-top"><img src="{img_src(first, page)}" alt="{h(alt(first, lang))}"></div>
<input type="range" min="0" max="100" value="50" aria-label="{h(c['hero_slider'])}"><span class="cmp-line"></span>
<span class="cmp-lab l">{h(style_name(first['style'], lang))}</span><span class="cmp-lab r">{ui['baseline']}</span></div>
<div class="hero-side"><h2>{c['hero_h']}</h2><p class="muted">{c['hero_p']}</p>
<div class="chips" role="group" aria-label="{h(c['hero_pick'])}">{chips}</div>
<p class="mono muted">{c['hero_more']} <a id="hero-link" href="{rel(page, path(lang, 'style', first['style']))}">{h(style_name(first['style'], lang))}</a></p>
</div></div></section>""")

    # Basislinien
    bases = [IMG[(m["id"], "baseline", "en")] for m in MOTIFS if (m["id"], "baseline", "en") in IMG]
    items = []
    for e in bases:
        cells.append(cell_data(e, lang, page)); items.append(card(e, idx, lang, page, show="motif")); idx += 1
    out.append(f"""<section class="sec"><div class="wrap">
<div class="sec-head"><h2>{c['base_h']}</h2><p>{c['base_p']} <a href="{rel(page, path(lang, 'levers'))}">{c['base_link']}</a></p></div>
<div class="grid mixed">{''.join(items)}</div></div></section>""")

    # Motive
    out.append(f"""<section class="sec"><div class="wrap">
<div class="sec-head"><h2>{c['motifs_h']}</h2><p>{c['motifs_p']}</p></div>
{motif_cards(lang, page)}</div></section>""")

    # Leitstile über alle Motive
    rows = []
    for slug in MATRIX["flagships"]:
        imgs = style_images(slug)
        if not imgs:
            continue
        items = []
        for e in imgs:
            cells.append(cell_data(e, lang, page)); items.append(card(e, idx, lang, page, show="motif")); idx += 1
        rows.append(f'<div class="flag-row"><h3><a href="{rel(page, path(lang, "style", slug))}">{h(style_name(slug, lang))}</a> '
                    f'<span class="mono muted">· {h(style_cat(slug, lang))} · {len(imgs)} {ui["images"]}</span></h3>'
                    f'<div class="row">{"".join(items)}</div></div>')
    out.append(f"""<section class="sec"><div class="wrap">
<div class="sec-head"><h2>{c['flag_h']}</h2><p>{c['flag_p']}</p></div>
<div class="flag-rows">{''.join(rows)}</div></div></section>""")

    # Anatomie
    ex = IMG.get(tuple(MATRIX.get("anatomy_example", ["people", MATRIX["flagships"][0]])) + ("en",))
    if ex:
        parts = [[k, ex["parts"][k]] for k in ("style", "motif", "guards") if ex["parts"].get(k)]
        cells.append(cell_data(ex, lang, page))
        out.append(f"""<section class="sec"><div class="wrap">
<div class="sec-head"><h2>{c['anat_h']}</h2><p>{c['anat_p']}</p></div>
<div class="sheet"><div>{anatomy(parts, lang)}
<div class="actions" style="margin-top:12px"><button type="button" class="btn primary" data-copy="{h(ex['prompt'])}">{ui['copy_prompt']}</button></div></div>
<div>{card(ex, idx, lang, page)}<div class="prose" style="margin-top:16px">{c['anat_side']}</div></div></div>
</div></section>""")
        idx += 1

    # Kategorien
    counts = {}
    for s in LEX_PUBLIC:
        counts[s["category_id"]] = counts.get(s["category_id"], 0) + 1
    lex_page = path(lang, "lexicon")
    cats = "".join(
        f'<a class="tell" href="{rel(page, lex_page)}?cat={c_["id"]}" style="text-decoration:none;color:inherit">'
        f'<span class="lab">{num(counts.get(c_["id"], 0), lang)} {ui["styles_n"]}</span><h3>{h(c_["name_" + lang])}</h3>'
        f'<p class="muted" style="font-size:14.5px">{h(c_["description_" + lang])}</p></a>' for c_ in CATS)
    out.append(f"""<section class="sec"><div class="wrap">
<div class="sec-head"><h2>{c['cats_h'].replace('{n}', num(N_LEX, lang))}</h2><p>{c['cats_p']}</p></div>
<div class="tells">{cats}</div></div></section>""")

    out.append(lightbox(lang) + jscript(cells, "cells-data"))
    out.append(foot(lang, page))
    return write(page, "".join(out))


def motif_cards(lang, page):
    ui = UI[lang]
    out = []
    for m in MOTIFS:
        imgs = pub_images(m["id"])
        base = IMG.get((m["id"], "baseline", "en"))
        pics = ([imgs[0]] if imgs else []) + ([base] if base else []) + imgs[1:2]
        pics = [p for p in pics if p][:3]
        mos = "".join(f'<img src="{img_src(p, page, True)}" alt="" loading="lazy" width="{thumb_dims(p)[0]}" height="{thumb_dims(p)[1]}">' for p in pics)
        out.append(f'<a class="mcard" href="{rel(page, path(lang, "motif", m["id"]))}"><div class="mos">{mos}</div>'
                   f'<div class="mt"><span class="tier">{ui["tier" + str(m["tier"])]} · {len(imgs)} {ui["styles_n"]}</span>'
                   f'<h3>{h(m["name_" + lang])}</h3><p>{h(m["summary_" + lang])}</p></div></a>')
    return f'<div class="motifs">{"".join(out)}</div>'


def page_motifs(lang):
    page = path(lang, "motifs")
    c = COPY[lang]["motifs"]
    out = [head(lang, page, c["title"], c["desc"], "motifs"),
           f'<section class="mast"><div class="wrap mast-in"><div><p class="eyebrow">{c["eyebrow"]}</p><h1>{c["h1"]}</h1>'
           f'<p class="lede">{c["lede"]}</p></div></div></section>',
           f'<section class="sec"><h2 class="sr-only">{c["h1"]}</h2><div class="wrap">{motif_cards(lang, page)}</div></section>',
           foot(lang, page)]
    return write(page, "".join(out))


def page_motif(lang, m):
    page = path(lang, "motif", m["id"])
    c = COPY[lang]["motif"]
    ui = UI[lang]
    name = m[f"name_{lang}"]
    imgs = pub_images(m["id"])
    cells, idx = [], 0
    out = [head(lang, page, f"{name} – Bildsprache", m[f"summary_{lang}"], "motif")]
    texts = m["text"]  # Motivblock und Raster sind englisch; deutsche Fassung steht im Abschnitt der Zwillinge
    facts = [(len(imgs), ui["styles_n"]), (m["size"].replace("x", "×"), c["format"]),
             (len(m["text"]) or "–", c["strings"]), (ui["tier" + str(m["tier"])], c["tier"])]
    out.append(f"""<section class="mast"><div class="wrap mast-in">
<div><p class="crumbs"><a href="{rel(page, path(lang, 'motifs'))}">{ui['nav_motifs']}</a> /</p><h1>{h(name)}</h1>
<p class="lede">{h(m['summary_' + lang])}</p></div>
<div class="facts">{''.join(fact(v, l) for v, l in facts)}</div>
</div></section>""")
    motif_text = "Subject: " + (m["motif_en"])
    out.append(f"""<section class="sec"><div class="wrap sheet">
<div class="box"><h2>{c['block_h']}</h2><p class="muted" style="font-size:14.5px;margin-bottom:10px">{c['block_p']}</p>
<div class="anat"><div class="seg seg-motif"><i>{ui['legend_motif']}</i><span lang="en">{h(motif_text)}</span></div></div>
<div class="actions" style="margin-top:10px"><button type="button" class="btn" data-copy="{h(motif_text)}">{ui['copy_motif']}</button></div></div>
<div><div class="box"><h2>{c['tests_h']}</h2><p>{h(m['tests_' + lang])}</p></div>
{f'<div class="box"><h2>{c["text_h"]}</h2><p class="mono">{" · ".join(h(t) for t in texts)}</p></div>' if m["text"] else ''}
</div></div></section>""")

    # Basislinien
    bl = [IMG[(m["id"], s, "en")] for s in ("baseline", "baseline-2") if (m["id"], s, "en") in IMG]
    items = []
    for e in bl:
        cells.append(cell_data(e, lang, page)); items.append(card(e, idx, lang, page)); idx += 1
    out.append(f"""<section class="sec"><div class="wrap">
<div class="sec-head"><h2>{c['base_h']}</h2><p>{c['base_p']}</p></div>
<div class="grid wide">{''.join(items)}</div></div></section>""")

    # Stilraster mit Filter
    present = []
    for e in imgs:
        cid = LEX[e["style"]]["category_id"]
        if cid not in present:
            present.append(cid)
    chips = (f'<button type="button" class="chip" data-filter="*" aria-pressed="true">{ui["all"]} <small>{len(imgs)}</small></button>' +
             "".join(f'<button type="button" class="chip" data-filter="{cid}" aria-pressed="false">{h(CAT[cid]["name_" + lang])} '
                     f'<small>{sum(1 for e in imgs if LEX[e["style"]]["category_id"] == cid)}</small></button>'
                     for cid in sorted(present, key=lambda x: [c_["id"] for c_ in CATS].index(x))))
    items = []
    for e in imgs:
        cells.append(cell_data(e, lang, page)); items.append(card(e, idx, lang, page)); idx += 1
    out.append(f"""<section class="sec"><div class="wrap">
<div class="sec-head"><h2>{c['grid_h'].replace('{n}', str(len(imgs)))}</h2><p>{c['grid_p']}</p></div>
<div class="bar"><div class="chips" role="group" aria-label="{c['filter']}" data-filter-for="grid">{chips}</div>
<span class="tally" id="grid-tally" aria-live="polite">{len(imgs)} {ui['images']}</span></div>
<div class="grid" id="grid">{''.join(items)}</div></div></section>""")

    # Deutsche Textfassungen
    twins = [IMG[(m["id"], s, "de")] for s in ["baseline"] + MATRIX["cells"].get(m["id"], []) if (m["id"], s, "de") in IMG]
    if twins:
        items = []
        for e in twins:
            cells.append(cell_data(e, lang, page)); items.append(card(e, idx, lang, page)); idx += 1
        out.append(f"""<section class="sec"><div class="wrap">
<div class="sec-head"><h2>{c['de_h']}</h2><p>{c['de_p']}</p></div>
<div class="grid">{''.join(items)}</div></div></section>""")

    out.append(lightbox(lang) + jscript(cells, "cells-data"))
    out.append(foot(lang, page))
    return write(page, "".join(out))


def page_styles(lang):
    page = path(lang, "styles")
    c = COPY[lang]["styles"]
    ui = UI[lang]
    shown = sum(1 for s in STYLES if style_images(s))
    out = [head(lang, page, c["title"], c["desc"], "styles"),
           f'<section class="mast"><div class="wrap mast-in"><div><p class="eyebrow">{c["eyebrow"]}</p><h1>{c["h1"]}</h1>'
           f'<p class="lede">{c["lede"].replace("{n}", str(shown))}</p></div></div></section>']
    for cat in CATS:
        slugs = [s for s in STYLES if LEX[s]["category_id"] == cat["id"]]
        if not slugs:
            continue
        cards = []
        for s in sorted(slugs, key=lambda x: style_name(x, lang)):
            imgs = style_images(s)
            if not imgs:
                continue
            e = imgs[0]
            tw, th = thumb_dims(e)
            cards.append(f'<figure class="card {AR[MOTIF[e["type"]]["size"]]}"><a class="cimg" href="{rel(page, path(lang, "style", s))}">'
                         f'<img src="{img_src(e, page, True)}" width="{tw}" height="{th}" loading="lazy" alt="{h(alt(e, lang))}"></a>'
                         f'<figcaption><b><a href="{rel(page, path(lang, "style", s))}">{h(style_name(s, lang))}</a></b>'
                         f'<span>{len(imgs)} {ui["images"] if len(imgs) != 1 else ui["image"]} · {h(STYLES[s][lang].get("era", ""))}</span></figcaption></figure>')
        if not cards:
            continue
        out.append(f'<section class="sec"><div class="wrap"><div class="sec-head"><h2>{h(cat["name_" + lang])}</h2>'
                   f'<p>{h(cat["description_" + lang])}</p></div><div class="grid mixed">{"".join(cards)}</div></div></section>')
    out.append(foot(lang, page))
    return write(page, "".join(out))


def page_style(lang, slug):
    page = path(lang, "style", slug)
    st = STYLES[slug]
    d = st[lang]
    c = COPY[lang]["style"]
    ui = UI[lang]
    lx = LEX[slug]
    cat, fam = FAM[lx["family_id"]]
    imgs = style_images(slug)
    cells, idx = [], 0
    out = [head(lang, page, f"{d['name']} – Bildsprache", d["summary"], "style")]
    facts = [(len(imgs), ui["images"]), (cat["name_" + lang], c["category"]),
             (ui["feas_" + lx["feasibility"]], c["feasibility"]), (f"{lx['distinctiveness']}/5", c["distinct"])]
    out.append(f"""<section class="mast"><div class="wrap mast-in">
<div><p class="crumbs"><a href="{rel(page, path(lang, 'styles'))}">{ui['nav_styles']}</a> / {h(cat['name_' + lang])} / {h(fam['name_' + lang])}</p>
<h1>{h(d['name'])}</h1><p class="lede">{h(d['summary'])}</p></div>
<div class="facts">{''.join(fact(v, l) for v, l in facts)}</div>
</div></section>""")
    items = []
    for e in imgs:
        cells.append(cell_data(e, lang, page)); items.append(card(e, idx, lang, page, show="motif")); idx += 1
    out.append(f"""<section class="sec"><div class="wrap">
<div class="sec-head"><h2>{c['row_h'].replace('{n}', str(len(imgs)))}</h2><p>{c['row_p']}</p></div>
<div class="grid mixed">{''.join(items)}</div></div></section>""")
    markers = "".join(f"<li>{h(x)}</li>" for x in d.get("markers", []))
    srcs = "".join(f'<li><a href="{h(s["url"])}" rel="noopener">{h(s["title"])}</a></li>' for s in st.get("sources", []))
    related = [s for s in LEX_PUBLIC if s["family_id"] == lx["family_id"] and s["slug"] != slug and s["slug"] not in STYLES][:14]
    rel_links = "".join(f'<a class="tag" href="{rel(page, path(lang, "lexicon"))}#{s["slug"]}">{h(s["name_" + lang])}</a>' for s in related)
    aka = ", ".join(d.get("aka", []))
    out.append(f"""<section class="sec"><h2 class="sr-only">{c['sheet_h']}</h2><div class="wrap sheet">
<div>
<div class="box"><h3>{c['block_h']}</h3><p class="muted" style="font-size:14.5px;margin-bottom:10px">{c['block_p']}</p>
<div class="anat"><div class="seg seg-style"><i>{ui['legend_style']}</i><span lang="en">{h(st['style_block'])}</span></div></div>
<div class="actions" style="margin-top:10px"><button type="button" class="btn primary" data-copy="{h(st['style_block'])}">{ui['copy_block']}</button></div></div>
<div class="box"><h3>{c['origin_h']}</h3><p>{h(d.get('origin', ''))}</p></div>
<div class="box"><h3>{c['markers_h']}</h3><ul class="markers">{markers}</ul></div>
</div>
<div>
<dl class="kv box">{f'<dt>{c["aka"]}</dt><dd>{h(aka)}</dd>' if aka else ''}<dt>{c['family']}</dt><dd>{h(cat['name_' + lang])} · {h(fam['name_' + lang])}</dd>
<dt>{c['era']}</dt><dd>{h(d.get('era', ''))}</dd></dl>
<div class="box"><h3>{c['escapes_ai_h'] if slug in AI_DEFAULT_STYLES else c['escapes_h']}</h3><p>{h(d.get('escapes', ''))}</p></div>
<div class="box"><h3>{c['pitfalls_h']}</h3><p>{h(d.get('pitfalls', ''))}</p></div>
<div class="box"><h3>{c['tip_h']}</h3><p>{h(d.get('tip', ''))}</p></div>
{f'<div class="box"><h3>{c["sens_h"]}</h3><p>{h(d["sensitivity"])}</p></div>' if d.get('sensitivity') else ''}
{f'<div class="box"><h3>{c["sources_h"]}</h3><ul class="markers">{srcs}</ul></div>' if srcs else ''}
</div></div></section>""")
    if rel_links:
        out.append(f"""<section class="sec"><div class="wrap"><div class="sec-head"><h2>{c['related_h']}</h2><p>{c['related_p']}</p></div>
<div class="tags">{rel_links}</div></div></section>""")
    out.append(lightbox(lang) + jscript(cells, "cells-data"))
    out.append(foot(lang, page))
    return write(page, "".join(out))


def lexicon_rows(lang):
    rows = []
    for s in LEXDATA["styles"]:
        if s.get("verdict") == "drop":
            continue
        cat, fam = FAM[s["family_id"]]
        o = "en" if lang == "de" else "de"
        sheet = STYLES.get(s["slug"])
        name = sheet[lang]["name"] if sheet else s[f"name_{lang}"]
        other_names = [sheet[o]["name"]] if sheet else [s[f"name_{o}"]]
        extra = [n for n in [s[f"name_{lang}"], s[f"name_{o}"]] + s.get("aliases", [])[:3] if n not in other_names + [name]]
        rows.append({
            "slug": s["slug"], "name": name,
            "alt": " · ".join(dict.fromkeys(other_names + extra)),
            "catId": cat["id"], "cat": cat[f"name_{lang}"], "fam": fam[f"name_{lang}"],
            "era": s.get(f"era_{lang}") or (s["era_origin"] if lang == "en" else ""),
            "desc": s.get(f"short_{lang}", ""),
            "markers": s.get(f"markers_{lang}") or (s["visual_markers"] if lang == "en" else []),
            "frag": "" if s.get("verdict") == "restrict" else s["prompt_fragment"],
            "feas": s["feasibility"], "dist": s["distinctiveness"],
            "sens": s[f"sensitivity_{lang}"] if f"sensitivity_{lang}" in s else (s["sensitivity_note"] if lang == "en" else ""),
            "page": ("../" + SEG["styles"][lang] + "/" + s["slug"] + "/") if s["slug"] in STYLES else None,
        })
    return rows


def page_lexicon(lang):
    page = path(lang, "lexicon")
    c = COPY[lang]["lexicon"]
    ui = UI[lang]
    data_rel = rel(page, f"data/lexicon.{lang}.json")
    (DOCS / "data").mkdir(parents=True, exist_ok=True)
    (DOCS / "data" / f"lexicon.{lang}.json").write_text(
        json.dumps(lexicon_rows(lang), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    chips = (f'<button type="button" class="chip" data-lex-cat="*" aria-pressed="true">{ui["all"]}</button>' +
             "".join(f'<button type="button" class="chip" data-lex-cat="{c_["id"]}" aria-pressed="false">{h(c_["name_" + lang])}</button>'
                     for c_ in CATS))
    out = [head(lang, page, c["title"].replace("{n}", num(N_LEX, lang)), c["desc"].replace("{n}", num(N_LEX, lang)), "lexicon"),
           f'<section class="mast"><div class="wrap mast-in"><div><p class="eyebrow">{c["eyebrow"]}</p>'
           f'<h1>{c["h1"].replace("{n}", num(N_LEX, lang))}</h1><p class="lede">{c["lede"]}</p></div></div></section>',
           f"""<section class="sec" id="lexicon" data-src="{data_rel}"><div class="wrap">
<h2 class="sr-only">{c['entries_h']}</h2>
<div class="bar"><label class="ctl-label" for="lex-q">{c['search_label']}</label>
<input type="search" id="lex-q" placeholder="{c['search']}" autocomplete="off">
<label class="mono" style="font-size:12px"><input type="checkbox" id="lex-lead"> {c['only_lead']}</label>
<span class="tally" id="lex-tally" aria-live="polite"></span>
<div class="chips" role="group" aria-label="{ui['categories']}" style="flex-basis:100%">{chips}</div></div>
<ul class="lex" id="lex-list" style="list-style:none;padding:0;margin:0"></ul>
<button type="button" class="btn more" id="lex-more" hidden></button>
<noscript><p>{c['noscript']}</p></noscript>
</div></section>""",
           foot(lang, page)]
    return write(page, "".join(out))


def page_levers(lang):
    page = path(lang, "levers")
    c = COPY[lang]["levers"]
    out = [head(lang, page, c["title"], c["desc"], "levers"),
           f'<section class="mast"><div class="wrap mast-in"><div><p class="eyebrow">{c["eyebrow"]}</p><h1>{c["h1"]}</h1>'
           f'<p class="lede">{c["lede"]}</p></div></div></section>']
    tells = "".join(
        f'<article class="tell" id="tell-{i + 1}"><span class="lab">{h(t["applies_" + lang])}</span><h3>{h(t["tell_" + lang])}</h3>'
        f'<p class="muted" style="font-size:14.5px"><b>{c["why"]}</b> {h(t["why_" + lang])}</p>'
        f'<p class="fix" style="font-size:14.5px"><b>{c["fix"]}</b> {h(t["fix_" + lang])}</p>'
        + (f'<p class="dots"><a href="{h(t["source"])}" rel="noopener">{c["source"]}</a></p>' if t.get("source", "").startswith("http") else "")
        + '</article>' for i, t in enumerate(TELLS))
    out.append(f'<section class="sec"><div class="wrap"><div class="sec-head"><h2>{c["tells_h"].replace("{n}", str(len(TELLS)))}</h2>'
               f'<p>{c["tells_p"]}</p></div><div class="tells">{tells}</div></div></section>')
    for ax in AXES:
        lv = [x for x in LEVERS if x["axis"] == ax["id"]]
        cards = "".join(
            f'<div class="lever"><h3>{h(x["name_" + lang])}</h3><p>{h(x["effect_" + lang])}</p><code lang="en">{h(x["prompt_phrase"])}</code>'
            f'<div class="actions"><button type="button" class="btn" data-copy="{h(x["prompt_phrase"])}">{c["copy"]}</button></div></div>'
            for x in lv)
        out.append(f'<section class="sec"><div class="wrap"><div class="sec-head"><h2>{h(ax["name_" + lang])}</h2>'
                   f'<p>{h(ax["description_" + lang])}</p></div><div class="levers">{cards}</div></div></section>')
    out.append(foot(lang, page))
    return write(page, "".join(out))


def page_method(lang):
    page = path(lang, "method")
    c = COPY[lang]["method"]
    stats = method_stats()
    body = c["body"]
    for k, v in stats.items():
        body = body.replace("{" + k + "}", num(v, lang) if isinstance(v, int) else str(v))
    cells, idx, extra = [], 0, ""
    flawed = [e for e in MANIFEST if (e.get("qa") or {}).get("verdict") == "fail"]
    if flawed:
        items = []
        for e in flawed:
            cells.append(cell_data(e, lang, page)); items.append(card(e, idx, lang, page)); idx += 1
        extra = (f'<section class="sec"><div class="wrap"><div class="sec-head"><h2>{c["flawed_h"]}</h2><p>{c["flawed_p"]}</p></div>'
                 f'<div class="grid mixed">{"".join(items)}</div></div></section>')
    pilot = ""
    pics = sorted((ROOT / "images" / "method").glob("v*.webp"))
    if pics:
        rows = []
        for v in ("v1", "v2"):
            figs = "".join(
                f'<figure class="card ar-portrait"><img src="{rel(page, "images/method/" + p.name)}" width="373" height="560" '
                f'loading="lazy" alt="{h(c["pilot_alt"].format(v=v[1], style=pilot_label(p.stem, lang)))}">'
                f'<figcaption><b>{h(pilot_label(p.stem, lang))}</b></figcaption></figure>'
                for p in pics if p.stem.startswith(v + "-"))
            rows.append(f'<h3>{h(c["pilot_" + v])}</h3><div class="grid">{figs}</div>')
        pilot = (f'<section class="sec"><div class="wrap"><div class="sec-head"><h2>{c["pilot_h"]}</h2><p>{c["pilot_p"]}</p></div>'
                 f'{"".join(rows)}</div></section>')
    out = [head(lang, page, c["title"], c["desc"], "method"),
           f'<section class="mast"><div class="wrap mast-in"><div><p class="eyebrow">{c["eyebrow"]}</p><h1>{c["h1"]}</h1>'
           f'<p class="lede">{c["lede"]}</p></div></div></section>',
           f'<section class="sec"><div class="wrap prose">{body}</div></section>', pilot, extra,
           lightbox(lang) + jscript(cells, "cells-data") if cells else "",
           foot(lang, page)]
    return write(page, "".join(out))


def pilot_label(stem, lang):
    slug = stem.split("-", 1)[1]
    names = {"watercolor": "watercolor-wet-in-wet", "claymation": "clay-animation"}
    slug = names.get(slug, slug)
    return style_name(slug, lang) if slug in STYLES or slug == "baseline" else slug


def method_stats():
    dates = [e["generated_at"][:10] for e in MANIFEST] or ["–"]
    versions = sorted({e.get("codex_version", "") for e in MANIFEST if e.get("codex_version")}) or ["Codex CLI"]
    return {
        "images": N_IMAGES, "calls": STATS.get("calls", N_IMAGES), "v1": STATS.get("pilot_v1", 0),
        "superseded": STATS.get("superseded", 0), "rerolls": STATS.get("rerolls", 0),
        "flawed": sum(1 for e in MANIFEST if (e.get("qa") or {}).get("verdict") == "flawed"),
        "failed": sum(1 for e in MANIFEST if (e.get("qa") or {}).get("verdict") == "fail"),
        "passed": sum(1 for e in MANIFEST if (e.get("qa") or {}).get("verdict") == "pass"),
        "lead": N_LEAD, "lex": N_LEX, "motifs": len(MOTIFS),
        "first": min(dates), "last": max(dates), "codex": versions[-1],
    }


def landing():
    """Eingangsseite: leitet nach Browsersprache oder gemerkter Wahl weiter."""
    text = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bildsprache – Ein Motiv, viele Bildsprachen</title>
<meta name="description" content="{h(COPY['de']['home']['desc'])}">
<link rel="canonical" href="{SITE_URL}/">
<link rel="alternate" hreflang="de" href="{SITE_URL}/de/">
<link rel="alternate" hreflang="en" href="{SITE_URL}/en/">
<link rel="alternate" hreflang="x-default" href="{SITE_URL}/">
<meta property="og:type" content="website">
<meta property="og:title" content="Bildsprache – Ein Motiv, viele Bildsprachen">
<meta property="og:description" content="{h(COPY['de']['home']['desc'])}">
<meta property="og:url" content="{SITE_URL}/">
<meta property="og:image" content="{SITE_URL}/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{FAVICON}">
{theme.script()}<script>
(function () {{
  var lang = null;
  try {{ lang = localStorage.getItem('bildsprache.language'); }} catch (e) {{}}
  if (lang !== 'de' && lang !== 'en') {{
    lang = 'en';
    var prefs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language];
    for (var i = 0; i < prefs.length; i++) {{
      var p = String(prefs[i] || '').slice(0, 2).toLowerCase();
      if (p === 'de' || p === 'en') {{ lang = p; break; }}
    }}
  }}
  location.replace(lang + '/' + location.search + location.hash);
}})();
</script>
<style>{theme.css()}body{{margin:0;font:17px/1.6 Georgia,serif;background:var(--ground);color:var(--ink);display:grid;place-items:center;min-height:100vh}}a{{color:var(--accent)}}</style>
</head>
<body><main><h1>Bildsprache</h1><p><a href="de/" hreflang="de" lang="de">Deutsch</a> · <a href="en/" hreflang="en" lang="en">English</a></p></main></body>
</html>
"""
    (DOCS / "index.html").write_text(text, encoding="utf-8")
    remember = "<script>document.addEventListener('click',function(e){var a=e.target.closest('.tb-lang a');if(a){try{localStorage.setItem('bildsprache.language',a.hreflang)}catch(x){}}});</script>"
    return remember


def not_found():
    (DOCS / "404.html").write_text(
        f'<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>404 – Bildsprache</title>{theme.script()}<style>{theme.css()}body{{margin:0;font:17px/1.6 Georgia,serif;background:var(--ground);'
        f'color:var(--ink);display:grid;place-items:center;min-height:100vh}}a{{color:var(--accent)}}</style></head>'
        f'<body><main><h1>404</h1><p>Seite nicht gefunden · Page not found</p>'
        f'<p><a href="/bildsprache/de/">Deutsch</a> · <a href="/bildsprache/en/">English</a></p></main></body></html>',
        encoding="utf-8")


def copy_assets():
    (DOCS / "assets").mkdir(parents=True, exist_ok=True)
    for f in ("site.css", "site.js"):
        shutil.copyfile(ROOT / "web" / f, DOCS / "assets" / f)
    n = 0
    for e in MANIFEST:
        lang = ".de" if e.get("lang") == "de" else ""
        for suffix in ("", ".thumb"):
            src = ROOT / "images" / e["type"] / f"{e['style']}{lang}{suffix}.webp"
            dst = DOCS / "images" / e["type"] / src.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            n += 1
    for p in (ROOT / "images" / "method").glob("*.webp"):
        dst = DOCS / "images" / "method" / p.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, dst)
    og = ROOT / "og.png"
    if og.exists():
        shutil.copyfile(og, DOCS / "og.png")
    else:
        print("  WARNUNG: og.png fehlt – Link-Vorschauen bleiben ohne Bild", file=sys.stderr)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    return n


def write_readmes():
    """README.md und README.de.md aus den Vorlagen in web/, mit denselben Zahlen wie die Website."""
    values = {"__N_MOTIFS__": str(len(MOTIFS)), "__N_LEAD__": str(N_LEAD), "__N_IMAGES__": str(N_IMAGES)}
    for src, dst, lang in (("readme.en.md", "README.md", "en"), ("readme.de.md", "README.de.md", "de")):
        text = (ROOT / "web" / src).read_text(encoding="utf-8")
        for k, v in values.items():
            text = text.replace(k, v)
        text = text.replace("__N_LEX__", num(N_LEX, lang))
        (ROOT / dst).write_text(text, encoding="utf-8")


def main():
    problems = check_all(ROOT)
    if problems:
        for p in problems:
            print("  FEHLER ", p, file=sys.stderr)
        sys.exit(f"{len(problems)} Datenfehler – Build abgebrochen")
    # In ein Zwischenverzeichnis bauen und erst am Ende tauschen: ein Fehler lässt kein halbes docs/ zurück.
    global DOCS
    final, DOCS = DOCS, ROOT / "docs.tmp"
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir()
    n_img = copy_assets()
    remember = landing()
    not_found()
    pages = []
    for lang in LANGS:
        pages += [page_home(lang), page_motifs(lang), page_styles(lang), page_lexicon(lang), page_levers(lang), page_method(lang)]
        pages += [page_motif(lang, m) for m in MOTIFS]
        pages += [page_style(lang, s) for s in STYLES]
    for p in pages:  # Sprachwahl merken, wenn jemand umschaltet
        p.write_text(p.read_text(encoding="utf-8").replace("</body>", remember + "\n</body>"), encoding="utf-8")
    if final.exists():
        shutil.rmtree(final)
    DOCS.rename(final)
    DOCS = final
    write_readmes()
    print(f"  {len(pages)} Seiten, {n_img} Bilddateien, {N_IMAGES} Bilder, {N_LEAD} Leitstile, {N_LEX} Lexikoneinträge -> docs/")


if __name__ == "__main__":
    main()
