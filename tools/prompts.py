"""Setzt Prompts aus drei Teilen zusammen: Stilblock, Motivblock, Leitplanken.

Der Motivblock ist je Grafiktyp wortgleich, der Stilblock je Stil über alle Typen wortgleich.
Die Basislinie ist derselbe Prompt ohne Stilblock: Sie zeigt, was das Modell ohne Stilangabe tut.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MOTIFS = {m["id"]: m for m in json.loads((ROOT / "data" / "motifs.json").read_text())["motifs"]}


FORMAT = {"1536x1024": "landscape, 3:2", "1024x1536": "portrait, 2:3", "1024x1024": "square, 1:1"}


def guards(motif, lang="en"):
    text = motif.get("text_de") if lang == "de" and motif.get("text_de") else motif["text"]
    # Codex reicht die Größe nicht zuverlässig an das Bildwerkzeug weiter (Pilot v1: 21 von 46
    # Bildern im falschen Format). Im Prompt selbst genannt, wird das Format eingehalten.
    out = [f"Image format: {FORMAT[motif['size']]}."]
    if motif["figurative"]:
        out.append("Keep every person's age, build and imperfections exactly as described; "
                   "do not beautify, retouch or glamorize anyone.")
    if text:
        quoted = ", ".join(f"'{t}'" for t in text)
        out.append(f"The only text in the image is exactly: {quoted}. Spell every string exactly as given; "
                   "add no other words, numbers or small print.")
    else:
        out.append("No text, letters or numbers anywhere in the image.")
    out.append("No logos, brand names, signatures or watermarks.")
    return " ".join(out)


def motif_block(motif, lang="en"):
    return motif.get("motif_de") if lang == "de" and motif.get("motif_de") else motif["motif_en"]


def compose(motif_id, style_block=None, lang="en", motifs=None):
    """Liefert (prompt, teile). teile dient der farbigen Prompt-Anatomie auf der Website.
    motifs: andere Motivliste, etwa die der Lexikon-Beispielbilder (data/lexicon_motifs.json)."""
    m = (motifs or MOTIFS)[motif_id]
    parts = []
    if style_block:
        parts.append(("style", "Style: " + style_block.strip()))
    parts.append(("motif", "Subject: " + motif_block(m, lang)))
    parts.append(("guards", "Constraints: " + guards(m, lang)))
    return "\n\n".join(p for _, p in parts), parts
