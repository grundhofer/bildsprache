"""Prüft Daten, Theme-Kontraste und die gebaute Website (python3 build.py vorher ausführen)."""
import html.parser, json, pathlib, re, sys, unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DOCS = ROOT / "docs"

from tools.checks import check_all  # noqa: E402
from web.theme import PALETTES  # noqa: E402


def luminance(hexcolor):
    rgb = [int(hexcolor[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


class Collector(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.imgs_without_alt, self.ids, self.html_lang = [], 0, [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.html_lang = a.get("lang")
        if tag == "img":
            self.refs.append(a.get("src"))
            if a.get("alt") is None:
                self.imgs_without_alt += 1
        if tag in ("a", "link") and a.get("href"):
            self.refs.append(a["href"])
        if tag == "script" and a.get("src"):
            self.refs.append(a["src"])
        if a.get("id"):
            self.ids.append(a["id"])


class TestData(unittest.TestCase):
    def test_checks_pass(self):
        self.assertEqual(check_all(ROOT), [])

    def test_readmes_have_no_placeholders(self):
        for name in ("README.md", "README.de.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertNotIn("__N_", text, name)

    def test_theme_contrast(self):
        for mode, p in PALETTES.items():
            for fg in ("ink", "ink-2", "ink-3", "accent", "brass"):
                for bg in ("ground", "surface", "surface-2"):
                    with self.subTest(mode=mode, fg=fg, bg=bg):
                        self.assertGreaterEqual(contrast(p[fg], p[bg]), 4.5)
            self.assertGreaterEqual(contrast(p["accent-ink"], p["accent"]), 4.5)
            for tag in ("tag-style", "tag-motif", "tag-guard"):
                self.assertGreaterEqual(contrast(p["ink"], p[tag]), 4.5)
                self.assertGreaterEqual(contrast(p["ink-3"], p[tag]), 3.0)


@unittest.skipUnless((DOCS / "de" / "index.html").exists(), "docs/ fehlt – erst python3 build.py")
class TestSite(unittest.TestCase):
    pages = sorted(DOCS.rglob("index.html"))

    def test_both_languages_have_the_same_pages(self):
        de = len(list((DOCS / "de").rglob("index.html")))
        en = len(list((DOCS / "en").rglob("index.html")))
        self.assertEqual(de, en)
        self.assertGreater(de, 20)

    def test_internal_links_and_images_resolve(self):
        missing = []
        for page in self.pages:
            c = Collector()
            c.feed(page.read_text(encoding="utf-8"))
            for ref in c.refs:
                if not ref or re.match(r"^(https?:|mailto:|data:|#)", ref):
                    continue
                target = (page.parent / ref.split("#")[0].split("?")[0]).resolve()
                if target.is_dir():
                    target = target / "index.html"
                if not target.exists():
                    missing.append(f"{page.relative_to(DOCS)} -> {ref}")
        self.assertEqual(missing[:20], [])

    def test_lightbox_images_resolve(self):
        missing = []
        for page in self.pages:
            text = page.read_text(encoding="utf-8")
            m = re.search(r'<script type="application/json" id="cells-data">(.*?)</script>', text, re.S)
            if not m:
                continue
            for cell in json.loads(m.group(1)):
                for src in (cell["src"], cell.get("base")):
                    if src and not (page.parent / src).resolve().exists():
                        missing.append(f"{page.relative_to(DOCS)} -> {src}")
        self.assertEqual(missing[:20], [])

    def test_every_page_has_lang_title_alt_and_unique_ids(self):
        for page in self.pages:
            with self.subTest(page=str(page.relative_to(DOCS))):
                text = page.read_text(encoding="utf-8")
                c = Collector()
                c.feed(text)
                if page.parent.name in ("de", "en") or "/de/" in str(page) or "/en/" in str(page):
                    self.assertIn(c.html_lang, ("de", "en"))
                self.assertRegex(text, r"<title>[^<]{5,}</title>")
                self.assertEqual(c.imgs_without_alt, 0)
                self.assertEqual(len(c.ids), len(set(c.ids)), "doppelte id")

    def test_lexicon_json(self):
        for lang in ("de", "en"):
            rows = json.loads((DOCS / "data" / f"lexicon.{lang}.json").read_text(encoding="utf-8"))
            self.assertGreater(len(rows), 1000)
            self.assertTrue(all(r["name"] and r["cat"] for r in rows))


if __name__ == "__main__":
    unittest.main()
