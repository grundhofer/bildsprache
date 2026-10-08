"""Fließtexte der Seiten, Deutsch und Englisch. Platzhalter in {geschweiften Klammern} setzt build.py ein.

Redaktionelle Texte stehen unter CC BY 4.0 (siehe LICENSE-CONTENT.md).
"""

COPY = {
 "de": {
  "home": {
   "title": "Bildsprache – Bildstile für Infografik, Porträt, Icons und mehr",
   "desc": "Bildstile für KI-Bilder nach Anwendung: Infografik, Diagramm, Icons, Porträt, Produkt, Plakat, Illustration, "
           "Karte und Stimmungsbild. Jedes Bild mit kopierbarem Prompt, Stilblock und Vorlage für eigene Inhalte.",
   "eyebrow": "Bildstile für KI-Bilder",
   "h1": "Was willst du<br><em>erstellen?</em>",
   "lede": "Wähl eine Anwendung, such dir einen Look aus und kopier, was du brauchst: <strong>den ganzen Prompt, nur den "
           "Stil oder eine Vorlage</strong>, in die du deine eigenen Inhalte einsetzt. Jedes Bild hier ist mit genau dem "
           "Prompt entstanden, der daneben steht.",
   "uc_h": "Anwendungen",
   "uc_p": "Jede Anwendung zeigt dieselbe Aufgabe in vielen Stilen, dazu das Bild ohne Stilangabe zum Vergleich und eine "
           "Vorlage zum Ausfüllen.",
   "how_h": "So benutzt du einen Stil",
   "how_p": "Jeder Prompt hat drei Teile: Stil, Inhalt und Leitplanken. Der Stil ist austauschbar, der Inhalt ist deiner.",
   "how_steps": [
    ["Ganzer Prompt:", "genau dieses Bild noch einmal erzeugen, als Ausgangspunkt."],
    ["Nur Stil:", "den Stilblock vor deine eigene Beschreibung oder deine Daten setzen, etwa „Mach daraus eine Infografik in diesem Stil“."],
    ["Vorlage:", "Stil, Inhalt mit Platzhaltern in [ECKIGEN KLAMMERN] und passende Leitplanken. Platzhalter ersetzen, fertig."],
   ],
   "why_h": "Warum überhaupt einen Stil angeben?",
   "why_p": "Ohne Stilangabe liefert das Modell seinen Standardlook: warmes Gegenlicht, glatte Haut, Bildmitte, bunte Kacheln.",
   "base_link": "Woran man ihn erkennt →",
   "hero_slider": "Regler: links der Stil, rechts dasselbe Motiv ohne Stilangabe",
   "hero_h": "Gleicher Inhalt, anderer Prompt",
   "hero_p": "Beide Bilder beschreiben dieselbe Szene Wort für Wort. Rechts fehlt nur der Stilblock. Zieh den Regler "
             "und wähle einen Stil.",
   "hero_pick": "Stil wählen",
   "hero_more": "Zum Faktenblatt:",
   "more_h": "Weiter stöbern",
   "more_p": "Für alle, die einen Stil genauer kennenlernen oder nach etwas Bestimmtem suchen.",
   "more_styles": ["Stile mit Faktenblatt", "Herkunft, Erkennungsmerkmale, Stolperfallen und der Stilblock zum Kopieren, mit Bildern aus allen Anwendungen."],
   "more_lexicon": ["Lexikon", "Ausgewählte Stile mit Prompt-Baustein, durchsuchbar, vom Daguerreotypie-Porträt bis zum Frutiger-Aero-Wallpaper."],
   "more_levers": ["KI-Look erkennen", "Woran man KI-Bilder erkennt und mit welchen Formulierungen man gegensteuert."],
  },
  "usecase": {
   "lede_more": "Klick auf ein Bild zeigt den ganzen Prompt; unter jedem Bild kopierst du Prompt oder Stil direkt.",
   "examples": "Beispielmotive", "format": "Format",
   "grid_h": "In {n} Stilen",
   "grid_p": "Am Ende steht dasselbe Motiv ohne Stilangabe.",
   "motif_h": "Beispielmotiv: so ist der Inhalt beschrieben",
   "b_h": "Deinen eigenen Prompt bauen",
   "b_p": "Stil wählen, Inhalt eintragen, kopieren. Bleibt ein Feld leer, steht im Prompt ein Platzhalter in [ECKIGEN KLAMMERN]. "
          "Prompts funktionieren auf Englisch am verlässlichsten; den Inhalt kannst du aber auch auf Deutsch schreiben.",
   "b_style": "Stil", "b_subject": "Inhalt: was soll zu sehen sein?",
   "b_subject_hint": "Der Platzhalter zeigt, was eine gute Beschreibung enthält. Anordnung und Gestaltung überlässt du dem Stil.",
   "b_text": "Text im Bild, eine Zeile pro Textstück", "b_text_ph": "Vom Korn zum Brot\n1 Säen\n2 Ernten",
   "b_format": "Format",
  },
  "motif": {
   "block_p": "Dieser Text steht wortgleich in jedem Prompt dieses Motivs. Er ist englisch, "
              "weil das Modell englische Prompts am verlässlichsten umsetzt.",
   "de_h": "Mit deutschem Text im Bild", "de_p": "Dieselben Stile mit deutscher Beschriftung. Umlaute und das "
                                                "Gradzeichen sind ein guter Härtetest für die Textdarstellung.",
  },
  "styles": {
   "title": "Leitstile – Bildsprache", "desc": "Die Leitstile von Bildsprache mit Faktenblatt, Stilblock und Beispielbildern.",
   "eyebrow": "Leitstile", "h1": "Stile mit Bildern",
   "lede": "{n} Stile mit Faktenblatt, kopierbarem Stilblock und Beispielbildern. Weitere Stile ohne Bild stehen im Lexikon.",
   "filter": "Nach Anwendung filtern",
  },
  "style": {
   "era": "Zeit", "category": "Kategorie", "feasibility": "Machbarkeit", "distinct": "Abstand zum KI-Look",
   "block_h": "Stilblock", "block_p": "Diesen Block vor deine Motivbeschreibung setzen. Er ist in allen Bildern dieses "
                                    "Stils wortgleich.",
   "tpl_p": "Oder als Vorlage für eine Anwendung kopieren: Stilblock, Inhalt mit Platzhaltern und passende Leitplanken.",
   "origin_h": "Herkunft", "markers_h": "Erkennungsmerkmale", "aka": "Auch genannt", "family": "Einordnung",
   "escapes_h": "Warum er nicht nach KI aussieht", "escapes_ai_h": "Warum er nach KI aussieht", "pitfalls_h": "Wo es schiefgeht", "tip_h": "Tipp",
   "sens_h": "Zu beachten", "sources_h": "Quellen", "sheet_h": "Faktenblatt",
   "row_h": "Auf {n} Motiven", "row_p": "Derselbe Stilblock, unterschiedliche Motivblöcke.",
   "related_h": "Verwandte Stile im Lexikon", "related_p": "Weitere Stile derselben Familie im Lexikon, ohne eigenes Faktenblatt.",
  },
  "lexicon": {
   "title": "Lexikon: {n} Bildstile – Bildsprache", "desc": "{n} ausgewählte Bildstile mit Merkmalen und Prompt-Baustein, durchsuchbar.",
   "eyebrow": "Lexikon", "h1": "{n} Bildstile",
   "lede": "Eine Auswahl aus {all} recherchierten Stilen: die Leitstile und alle, die sich deutlich vom KI-Look abheben "
           "und sich verlässlich erzeugen lassen. Jeder Eintrag nennt Herkunft, Merkmale und einen englischen "
           "Prompt-Baustein, den du an eine eigene Beschreibung anhängen kannst. Zu {m} Stilen gibt es ein kleines "
           "Beispielbild, kurz geprüft, bei Fehlschlag ein Neuversuch.",
   "search": "Stil, Epoche, Material …", "search_label": "Suchen", "entries_h": "Einträge", "only_lead": "nur Leitstile mit Bildern",
   "noscript": "Das Lexikon braucht JavaScript. Die Daten liegen auch als JSON im Repository (data/lexicon.json).",
  },
  "levers": {
   "title": "KI-Look und Stilhebel – Bildsprache", "desc": "Woran man KI-Bilder erkennt und welche Prompt-Hebel dagegen helfen.",
   "eyebrow": "KI-Look & Hebel", "h1": "Woran man KI-Bilder erkennt",
   "lede": "Die typischen Merkmale entstehen, wenn der Prompt etwas offenlässt: Dann füllt das Modell die Lücke mit "
           "seinem Durchschnitt. Für die meisten Merkmale gibt es einen Gegenhebel. Darunter stehen Hebel nach Bereich, jeweils mit "
           "einer Formulierung zum Kopieren.",
   "tells_h": "{n} typische Merkmale",
   "tells_p": "Gesammelt aus Fachartikeln, Studien und OpenAIs eigener Prompt-Anleitung. Quellen stehen am jeweiligen Eintrag.",
   "why": "Warum:", "fix": "Gegenhebel:", "source": "Quelle", "copy": "Kopieren",
  },
  "method": {
   "title": "Methode – Bildsprache", "desc": "Wie die Bilder und das Lexikon von Bildsprache entstanden sind und wo die Grenzen liegen.",
   "eyebrow": "Methode", "h1": "Wie der Katalog entstand",
   "lede": "Alle Bilder sind mit KI erzeugt, alle Texte von KI-Agenten recherchiert und redaktionell geprüft. Hier steht, "
           "wie das ablief, was gemessen wurde und was nicht.",
   "pilot_h": "Fassung 1 und Fassung 2 im Vergleich",
   "pilot_p": "Dieselben Plakatmotive vor und nach der Umstellung. In Fassung 1 legte der Motivblock die Bildanlage fest, der "
              "Stilblock beschrieb nur die Oberfläche: Jedes Plakat bekam denselben Sonnenkreis über dem Horizont. In Fassung 2 "
              "beschreibt der Motivblock nur noch den Inhalt, der Stilblock auch Komposition und Schrift.",
   "pilot_v1": "Fassung 1: Stil als Oberfläche", "pilot_v2": "Fassung 2: Stil als Bildordnung",
   "pilot_alt": "Festivalplakat aus Fassung {v}, Stil: {style}",
   "flawed_h": "Fehlversuche",
   "flawed_p": "Bei diesen Zellen hat auch der dritte Versuch die Prüfung nicht bestanden. Sie bleiben sichtbar, weil sie zeigen, "
               "wo ein Stil-Prompt an Grenzen stößt. Der Grund steht jeweils in der Bildansicht.",
   "body": """
<h2>Motive</h2>
<p>{motifs} Motive, jedes als fester englischer Text. Ein Motiv legt den Inhalt fest: Personen, Handlung, Ort,
Gegenstände und bei Infografik, Plakat, Karte und Diagramm den exakten Text. Licht, Farbe, Optik, Medium und Anordnung
bleiben offen. Alle Motive spielen auf der erfundenen Insel Lornholm, damit keine realen Orte, Personen oder Marken
im Bild landen.</p>
<h2>Prompts</h2>
<p>Jeder Prompt besteht aus Stilblock, Motivblock und Leitplanken. Der Motivblock ist pro Motiv wortgleich, der
Stilblock pro Stil. Die Bilder „ohne Stilangabe“ entstehen aus demselben Prompt ohne Stilblock. Die Leitplanken nennen das Format, den erlaubten
Text und bei Menschen die Anweisung, nichts zu schönen.</p>
<h2>Was der Pilotlauf gezeigt hat</h2>
<p>In der ersten Fassung legten die Motivblöcke auch Bildausschnitt und Anordnung fest, und die Stilblöcke beschrieben
nur Medium und Oberfläche. Das Ergebnis sah aus wie ein Filter: Jede Infografik hatte dasselbe Zwei-mal-drei-Raster,
jedes Plakat denselben Sonnenkreis über dem Horizont. Seit der zweiten Fassung beschreibt der Motivblock nur noch den
Inhalt, und der Stilblock enthält auch Komposition, Schrift und Informationsaufbau des Stils. Außerdem steht das Format
jetzt im Prompt, weil die Größenangabe allein in 21 von 46 Fällen nicht ankam.</p>
<h2>Erzeugung</h2>
<p>Alle Bilder stammen aus dem eingebauten Bildwerkzeug von Codex CLI ({codex}), aufgerufen im Zeitraum {first} bis
{last}. Laut OpenAI-Dokumentation nutzt es gpt-image-2; welches Modell im Einzelfall antwortete, lässt sich von außen
nicht prüfen. Jedes Bild ist ein eigener Aufruf ohne Seed. Derselbe Prompt liefert also beim nächsten Mal ein anderes
Bild.</p>
<h2>Prüfung</h2>
<p>Jedes Bild hat ein Prüfagent angesehen: Ist der Stil erkennbar? Sind die festen Motivteile da? Ist die Anatomie stimmig? Ein zweiter Agent hat jeden Text Buchstabe für Buchstabe gegengelesen. Bei groben Fehlern wurde
neu erzeugt, mit höchstens drei Versuchen je Zelle. Insgesamt gab es {calls} Bildaufrufe: {v1} im ersten Pilotlauf,
{superseded} mit älteren Fassungen von Stilblöcken, die danach überarbeitet wurden, und {rerolls} Neuversuche nach
durchgefallener Prüfung. Veröffentlicht sind {images} Bilder. {passed} Bilder haben die Prüfung ohne Einwand bestanden, bei {flawed} ist eine Abweichung
dokumentiert, {failed} sind als Fehlversuch markiert. Die Abweichung steht in der Bildansicht, zusammen mit Datum,
Format und Versuchsnummer. Die Prüfer waren streng: Ein Pflaster am falschen Finger oder vier statt zwei Kochstellen zählen
schon als Abweichung.</p>
<h2>Lexikon</h2>
<p>Das Lexikon mit {lex} Einträgen entstand in einer Recherche mit 32 KI-Agenten: 14 Fachgebiete von Fotografie bis
Internetästhetik, danach Zusammenführung von Dubletten und drei Runden Lückensuche aus vier Blickwinkeln. Die Einträge
wurden anschließend einzeln auf Plausibilität geprüft, gründlich im Bild aber nur die {lead} Leitstile. Machbarkeit und
Abstand zum KI-Look sind redaktionelle Einschätzungen, keine Messwerte. Auf der Website stehen davon {lex_pub}: die
Leitstile und alle Einträge mit großem Abstand zum KI-Look (4 oder 5 von 5) und hoher Machbarkeit. Die übrigen bleiben im
Repository (data/lexicon.json).</p>
<p>Zu {lex_images} der übrigen Stile gibt es ein kleines Beispielbild. Es entsteht aus dem Prompt-Baustein des Eintrags
und einem von zwei einfachen Motiven: einer Leuchtturmwärterin mit Besen oder, bei Grafikdesign und Infografik, einem
Infoblatt mit drei Punkten. Ein Prüfagent hat jedes Bild kurz angesehen: Ist der Stil erkennbar, ist das Motiv da, gibt
es Logos oder erfundenen Text? Fiel ein Bild durch, gab es einen Neuversuch. {lex_flawed} Bilder zeigen eine dokumentierte
Abweichung, {lex_failed} sind als Fehlversuch markiert; insgesamt waren es {lex_calls} Bildaufrufe. Davon gehören
{lex_images_pub} zu Stilen, die auf der Website stehen. Die {lex_restricted}
Einträge zu gemeinschaftsgebundenen Traditionen zeigen auf der Website weder Prompt-Baustein noch Bild.</p>
<h2>Grenzen</h2>
<ul>
<li>Die Bilder sind nicht reproduzierbar. Der Katalog zeigt, was ein Prompt typischerweise bewirkt, nicht, was er garantiert.</li>
<li>Stilnamen beschreiben Techniken, Epochen und Bewegungen. Lebende Künstlerinnen und Künstler und Studios werden
bewusst nicht genannt. Markennamen erscheinen nur, wo sie ein technisches Verfahren bezeichnen, etwa Tri-X oder
Technicolor.</li>
<li>Heilige oder kulturell geschützte Bildtraditionen sind ausgeschlossen oder im Lexikon mit Hinweis versehen.</li>
<li>Die WebP-Dateien der Website enthalten keine C2PA-Herkunftsdaten mehr. Die Originale mit Metadaten liegen als
Release im Repository.</li>
</ul>
<h2>Kennzeichnung und Lizenz</h2>
<p>Alle Bilder sind als KI-generiert gekennzeichnet. Die Bilder stehen unter CC0: Rein KI-generierte Bilder sind in
vielen Rechtsordnungen ohnehin nicht urheberrechtlich geschützt. Texte stehen unter CC BY 4.0, der Code unter MIT.</p>
<h2>Verwandte Projekte</h2>
<p>Ähnliche Sammlungen zeigen eine einzelne Szene in vielen Stilen, etwa gpt-image-style-atlas mit 116 Stilen.
Bildsprache setzt auf mehrere Grafiktypen, weil sich ein Stil an einer Infografik oder einem Plakat anders bewährt als
an einem Porträt. Das Schwesterprojekt <a href="https://grundhofer.github.io/designsprache/de/">Designsprache</a> macht
dasselbe für Benutzeroberflächen.</p>
""",
  },
 },
 "en": {
  "home": {
   "title": "Bildsprache – Image styles for infographics, portraits, icons and more",
   "desc": "Image styles for AI images by use case: infographic, chart, icons, portrait, product, poster, illustration, "
           "map and mood image. Every image with a copyable prompt, style block and a template for your own content.",
   "eyebrow": "Image styles for AI images",
   "h1": "What do you want<br><em>to make?</em>",
   "lede": "Pick a use case, choose a look and copy what you need: <strong>the full prompt, the style only or a "
           "template</strong> to fill with your own content. Every image here was made with exactly the prompt shown "
           "next to it.",
   "uc_h": "Use cases",
   "uc_p": "Each use case shows the same task in many styles, the image without a style for comparison and a template to fill in.",
   "how_h": "How to use a style",
   "how_p": "Every prompt has three parts: style, content and constraints. The style is interchangeable, the content is yours.",
   "how_steps": [
    ["Full prompt:", "make exactly this image again, as a starting point."],
    ["Style only:", "put the style block in front of your own description or data, e.g. 'Turn this into an infographic in this style'."],
    ["Template:", "style, content with placeholders in [SQUARE BRACKETS] and matching constraints. Replace the placeholders and you are done."],
   ],
   "why_h": "Why give a style at all?",
   "why_p": "Without a style the model delivers its default look: warm backlight, smooth skin, centred subjects, colourful tiles.",
   "base_link": "How to recognise it →",
   "hero_slider": "Slider: the style on the left, the same motif without a style on the right",
   "hero_h": "Same content, different prompt",
   "hero_p": "Both images describe the same scene word for word. The right one only lacks the style block. Drag the "
             "slider and pick a style.",
   "hero_pick": "Pick a style",
   "hero_more": "Fact sheet:",
   "more_h": "Keep exploring",
   "more_p": "For getting to know a style in depth or looking for something specific.",
   "more_styles": ["Styles with fact sheets", "Origin, markers, pitfalls and the style block to copy, with images from every use case."],
   "more_lexicon": ["Lexicon", "Selected styles with a prompt fragment, searchable, from the daguerreotype portrait to the Frutiger Aero wallpaper."],
   "more_levers": ["Spotting the AI look", "How to recognise AI images and which phrases counter it."],
  },
  "usecase": {
   "lede_more": "Click an image for the full prompt; the buttons under each image copy the prompt or the style directly.",
   "examples": "example motifs", "format": "Format",
   "grid_h": "In {n} styles",
   "grid_p": "The same motif without a style comes last.",
   "motif_h": "Example motif: how the content is described",
   "b_h": "Build your own prompt",
   "b_p": "Pick a style, enter your content, copy. Any field left empty becomes a placeholder in [SQUARE BRACKETS].",
   "b_style": "Style", "b_subject": "Content: what should the image show?",
   "b_subject_hint": "The placeholder shows what a good description contains. Leave layout and design to the style.",
   "b_text": "Text in the image, one line per string", "b_text_ph": "From Grain to Bread\n1 Sow\n2 Harvest",
   "b_format": "Format",
  },
  "motif": {
   "block_p": "This text appears word for word in every prompt for this motif.",
   "de_h": "With German text in the image", "de_p": "The same styles with German labels. Umlauts and the degree sign "
                                                   "are a good stress test for text rendering.",
  },
  "styles": {
   "title": "Lead styles – Bildsprache", "desc": "The lead styles of Bildsprache with fact sheet, style block and example images.",
   "eyebrow": "Lead styles", "h1": "Styles with images",
   "lede": "{n} styles with a fact sheet, a copyable style block and example images. More styles without images are in the lexicon.",
   "filter": "Filter by use case",
  },
  "style": {
   "era": "Period", "category": "Category", "feasibility": "Feasibility", "distinct": "Distance from AI look",
   "block_h": "Style block", "block_p": "Put this block in front of your motif description. It is identical in every image of this style.",
   "tpl_p": "Or copy it as a template for a use case: style block, content with placeholders and matching constraints.",
   "origin_h": "Origin", "markers_h": "Markers", "aka": "Also known as", "family": "Classification",
   "escapes_h": "Why it does not look like AI", "escapes_ai_h": "Why it looks like AI", "pitfalls_h": "Where it goes wrong", "tip_h": "Tip",
   "sens_h": "Keep in mind", "sources_h": "Sources", "sheet_h": "Fact sheet",
   "row_h": "On {n} motifs", "row_p": "The same style block with different motif blocks.",
   "related_h": "Related styles in the lexicon", "related_p": "More styles of the same family in the lexicon, without their own fact sheet.",
  },
  "lexicon": {
   "title": "Lexicon: {n} image styles – Bildsprache", "desc": "{n} selected image styles with markers and a prompt fragment, searchable.",
   "eyebrow": "Lexicon", "h1": "{n} image styles",
   "lede": "A selection from {all} researched styles: the lead styles and every style that stands clearly apart from the "
           "AI look and renders reliably. Each entry gives the origin, the markers and an English prompt fragment you can "
           "append to your own description. {m} styles have a small example image, briefly reviewed, with one retry if it failed.",
   "search": "Style, period, material …", "search_label": "Search", "entries_h": "Entries", "only_lead": "lead styles with images only",
   "noscript": "The lexicon needs JavaScript. The data is also in the repository as JSON (data/lexicon.json).",
  },
  "levers": {
   "title": "AI look and style levers – Bildsprache", "desc": "How to recognise AI images and which prompt levers counter it.",
   "eyebrow": "AI look & levers", "h1": "How to recognise AI images",
   "lede": "The typical markers appear when a prompt leaves something open: the model fills the gap with its average. "
           "Most markers have a counter-lever. Below are levers by area, each with a phrase to copy.",
   "tells_h": "{n} typical markers",
   "tells_p": "Collected from articles, studies and OpenAI's own prompting guide. Sources are given on each entry.",
   "why": "Why:", "fix": "Counter-lever:", "source": "Source", "copy": "Copy",
  },
  "method": {
   "title": "Method – Bildsprache", "desc": "How the images and the lexicon of Bildsprache were made, and where the limits are.",
   "eyebrow": "Method", "h1": "How the catalogue was made",
   "lede": "Every image is AI-generated; every text was researched by AI agents and edited. This page explains how that "
           "worked, what was measured and what was not.",
   "pilot_h": "Version 1 and version 2 compared",
   "pilot_p": "The same poster motif before and after the change. In version 1 the motif block fixed the layout and the style "
              "block only described the surface, so every poster got the same sun disc above the horizon. In version 2 the "
              "motif block only describes the content, and the style block also covers composition and lettering.",
   "pilot_v1": "Version 1: style as surface", "pilot_v2": "Version 2: style as structure",
   "pilot_alt": "Festival poster from version {v}, style: {style}",
   "flawed_h": "Failed attempts",
   "flawed_p": "For these cells even the third attempt did not pass the review. They stay visible because they show where a "
               "style prompt hits its limits. The reason is given in the image view.",
   "body": """
<h2>Motifs</h2>
<p>{motifs} motifs, each a fixed English text. A motif fixes the content: people, action, place, objects and, for the
infographic, poster, map and chart, the exact text. Light, colour, optics, medium and arrangement stay open. All motifs
are set on the fictional island of Lornholm so that no real places, people or brands end up in the images.</p>
<h2>Prompts</h2>
<p>Every prompt consists of a style block, a motif block and guards. The motif block is identical per motif, the style
block per style. The images with "no style given" come from the same prompt without a style block. The guards state the format, the allowed text
and, for people, the instruction not to prettify anyone.</p>
<h2>What the pilot run showed</h2>
<p>In the first version the motif blocks also fixed framing and arrangement, and the style blocks only described medium
and surface. The result looked like a filter: every infographic had the same two-by-three grid, every poster the same
sun disc above the horizon. Since the second version the motif block describes content only, and the style block also
covers the style's composition, lettering and information layout. The format is now part of the prompt as well, because
the size setting alone was ignored in 21 of 46 cases.</p>
<h2>Generation</h2>
<p>All images come from the built-in image tool of Codex CLI ({codex}), called between {first} and {last}. According to
OpenAI's documentation it uses gpt-image-2; which model answered in a given case cannot be verified from outside. Every
image is a separate call without a seed, so the same prompt gives a different image next time.</p>
<h2>Review</h2>
<p>A review agent looked at every image: is the style recognisable, are the fixed motif elements there, is the anatomy
plausible? A second agent proofread every text letter by letter. Images with major errors were regenerated,
with at most three attempts per cell. In total there were {calls} image calls: {v1} in the first pilot run,
{superseded} with older versions of style blocks that were revised afterwards, and {rerolls} retries after a failed
review. {images} images are published.
{passed} images passed without objection, {flawed} have a documented deviation, {failed} are marked as failed attempts.
The deviation is named in the image view, together with the date, format and attempt number. The reviewers were strict:
a plaster on the wrong finger or four burners instead of two already count as a deviation.</p>
<h2>Lexicon</h2>
<p>The lexicon of {lex} entries comes from research with 32 AI agents: 14 fields from photography to internet
aesthetics, followed by merging duplicates and three rounds of gap-finding from four perspectives. The entries were then
checked one by one for plausibility, but only the {lead} lead styles were tested thoroughly with images. Feasibility and
distance from the AI look are editorial judgements, not measurements. The site shows {lex_pub} of them: the lead
styles and every entry with a large distance from the AI look (4 or 5 out of 5) and high feasibility. The rest stay in
the repository (data/lexicon.json).</p>
<p>{lex_images} of the other styles have a small example image. It is made from the entry's prompt fragment and one of
two simple motifs: a lighthouse keeper with a broom or, for graphic design and infographics, an information sheet with
three items. A review agent looked at each image briefly: is the style recognisable, is the motif there, are there logos
or invented text? If an image failed, it got one retry. {lex_flawed} images show a documented deviation, {lex_failed}
are marked as failed attempts; there were {lex_calls} image calls in total. {lex_images_pub} of these images belong
to styles shown on the site. The {lex_restricted} entries on
community-bound traditions show neither a prompt fragment nor an image on the site.</p>
<h2>Limits</h2>
<ul>
<li>The images cannot be reproduced. The catalogue shows what a prompt typically does, not what it guarantees.</li>
<li>Style names describe techniques, periods and movements. Living artists and studios are deliberately not named.
Brand names appear only where they denote a technical process, such as Tri-X or Technicolor.</li>
<li>Sacred or culturally protected traditions are excluded or carry a note in the lexicon.</li>
<li>The site's WebP files no longer carry C2PA provenance data. The originals with metadata are attached to a release
in the repository.</li>
</ul>
<h2>Labelling and licence</h2>
<p>All images are labelled as AI-generated. The images are released under CC0: purely AI-generated images are not
protected by copyright in many jurisdictions anyway. Texts are under CC BY 4.0, the code under MIT.</p>
<h2>Related projects</h2>
<p>Similar collections show a single scene in many styles, for example gpt-image-style-atlas with 116 styles.
Bildsprache uses several graphic types, because a style that works for a portrait may fail on an infographic or a
poster. The sibling project <a href="https://grundhofer.github.io/designsprache/en/">Designsprache</a> does the same
for user interfaces.</p>
""",
  },
 },
}
