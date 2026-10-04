"""Fließtexte der Seiten, Deutsch und Englisch. Platzhalter in {geschweiften Klammern} setzt build.py ein.

Redaktionelle Texte stehen unter CC BY 4.0 (siehe LICENSE-CONTENT.md).
"""

COPY = {
 "de": {
  "home": {
   "title": "Bildsprache – Ein Motiv, viele Bildsprachen",
   "desc": "16 feste Motive in vielen Bildstilen, jedes Bild mit kopierbarem Prompt. Gegen den austauschbaren KI-Look: "
           "Fotografie, Malerei, Druckgrafik, Infografik, Plakat, Pixel-Art und mehr.",
   "eyebrow": "Stilkatalog für KI-Bildgenerierung",
   "h1": "Ein Motiv,<br><em>viele Bildsprachen.</em>",
   "lede": "KI-Bilder sehen oft gleich aus: warmes Gegenlicht, glatte Haut, Bildmitte, Infografiken aus denselben "
           "bunten Kacheln. Das liegt oft weniger am Modell als am Prompt. Hier läuft <strong>dasselbe Motiv durch "
           "viele Stile</strong>, und jedes Bild zeigt den Prompt, der es erzeugt hat.",
   "hero_slider": "Regler: links der Stil, rechts dasselbe Motiv ohne Stilangabe",
   "hero_h": "Gleicher Inhalt, anderer Prompt",
   "hero_p": "Beide Bilder beschreiben dieselbe Szene Wort für Wort. Rechts fehlt nur der Stilblock. Zieh den Regler "
             "und wähle einen Stil.",
   "hero_pick": "Stil wählen",
   "hero_more": "Zum Faktenblatt:",
   "base_h": "Ohne Stilangabe sieht vieles gleich aus",
   "base_p": "Diese 16 Bilder entstanden aus vollständigen, genauen Motivbeschreibungen, nur ohne Angabe zu Medium, "
             "Epoche, Licht oder Technik. Was dabei herauskommt, ist der Standardlook des Modells.",
   "base_link": "Woran man ihn erkennt →",
   "motifs_h": "16 Motive",
   "motifs_p": "Jedes Motiv legt den Inhalt fest, nicht die Anordnung. Alle spielen auf der erfundenen Insel Lornholm. "
               "Menschen, Infografik, Plakat, Karte, Datendiagramm und weitere Grafiktypen prüfen jeweils etwas anderes.",
   "flag_h": "Leitstile über alle Motive",
   "flag_p": "Ein Stil ist kein Filter, sondern ein System aus Entscheidungen zu Linie, Fläche, Schrift und Aufbau. "
             "Diese Stile laufen durch alle 16 Motive.",
   "anat_h": "So ist jeder Prompt gebaut",
   "anat_p": "Drei Teile, immer in derselben Reihenfolge. Der Motivblock ist für alle Bilder eines Motivs wortgleich, "
             "der Stilblock für alle Bilder eines Stils. Was sich zwischen zwei Bildern unterscheidet, steht also nur im "
             "Stilblock.",
   "anat_side": "<p>Der <b>Stilblock</b> beschreibt Medium und Technik, aber auch Komposition, Schrift und Aufbau von "
                "Informationen. Ohne diese Angaben übernimmt das Modell seine Standardkomposition und legt den Stil nur "
                "wie einen Filter darüber.</p><p>Die <b>Leitplanken</b> nennen Format, erlaubten Text und was nicht "
                "geschönt werden darf.</p>",
   "cats_h": "{n} Stile in 14 Kategorien",
   "cats_p": "Das Lexikon enthält jeden Stil mit Merkmalen und einem Prompt-Baustein, auch die ohne Beispielbild. "
             "Vom Daguerreotypie-Porträt bis zum Frutiger-Aero-Wallpaper.",
  },
  "motifs": {
   "title": "16 Motive – Bildsprache", "desc": "Die 16 Referenzmotive von Bildsprache, jedes in vielen Stilen.",
   "eyebrow": "Referenzmotive", "h1": "16 Motive",
   "lede": "Jedes Motiv ist ein fester Text, der den Inhalt beschreibt: wer, was, wo, welche Gegenstände. Farbe, Licht, "
           "Optik, Medium und Anordnung bleiben dem Stil überlassen. So lassen sich Stile vergleichen, ohne dass alle "
           "Bilder gleich gebaut sind.",
  },
  "motif": {
   "format": "Format", "strings": "Texte im Bild", "tier": "Rang",
   "block_h": "Motivblock", "block_p": "Dieser Text steht wortgleich in jedem Prompt dieses Motivs. Er ist englisch, "
                                      "weil das Modell englische Prompts am verlässlichsten umsetzt.",
   "tests_h": "Was das Motiv prüft", "text_h": "Exakter Text im Bild",
   "base_h": "Ohne Stilangabe", "base_p": "Zweimal derselbe Prompt ohne Stilblock. Die Ähnlichkeit der beiden Läufe "
                                         "zeigt, wie stabil der Standardlook ist.",
   "grid_h": "In {n} Stilen", "grid_p": "Klick auf ein Bild öffnet den vollständigen Prompt, aufgeteilt in Stil, Motiv "
                                        "und Leitplanken, und den Vergleich mit der Basislinie.",
   "filter": "Nach Kategorie filtern",
   "de_h": "Mit deutschem Text im Bild", "de_p": "Dieselben Stile mit deutscher Beschriftung. Umlaute und das "
                                                "Gradzeichen sind ein guter Härtetest für die Textdarstellung.",
  },
  "styles": {
   "title": "Leitstile – Bildsprache", "desc": "Die Leitstile von Bildsprache mit Faktenblatt, Stilblock und Beispielbildern.",
   "eyebrow": "Leitstile", "h1": "Stile mit Bildern",
   "lede": "{n} Stile mit Faktenblatt, kopierbarem Stilblock und Beispielbildern. Weitere Stile ohne Bild stehen im Lexikon.",
  },
  "style": {
   "era": "Zeit", "category": "Kategorie", "feasibility": "Machbarkeit", "distinct": "Abstand zum KI-Look",
   "block_h": "Stilblock", "block_p": "Diesen Block vor deine Motivbeschreibung setzen. Er ist in allen Bildern dieses "
                                    "Stils wortgleich.",
   "origin_h": "Herkunft", "markers_h": "Erkennungsmerkmale", "aka": "Auch genannt", "family": "Einordnung",
   "escapes_h": "Warum er nicht nach KI aussieht", "escapes_ai_h": "Warum er nach KI aussieht", "pitfalls_h": "Wo es schiefgeht", "tip_h": "Tipp",
   "sens_h": "Zu beachten", "sources_h": "Quellen", "sheet_h": "Faktenblatt",
   "row_h": "Auf {n} Motiven", "row_p": "Derselbe Stilblock, unterschiedliche Motivblöcke.",
   "related_h": "Verwandte Stile im Lexikon", "related_p": "Weitere Stile derselben Familie im Lexikon, ohne eigenes Faktenblatt.",
  },
  "lexicon": {
   "title": "Lexikon: {n} Bildstile – Bildsprache", "desc": "{n} Bildstile mit Merkmalen und Prompt-Baustein, durchsuchbar.",
   "eyebrow": "Lexikon", "h1": "{n} Bildstile",
   "lede": "Jeder Eintrag nennt Herkunft, Merkmale und einen englischen Prompt-Baustein, den du an eine eigene "
           "Motivbeschreibung anhängen kannst. Machbarkeit und Abstand zum KI-Look sind redaktionelle Einschätzungen. "
           "Nur die Leitstile wurden mit Bildern geprüft.",
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
wurden anschließend einzeln auf Plausibilität geprüft, aber nur die {lead} Leitstile auch im Bild. Machbarkeit und
Abstand zum KI-Look sind redaktionelle Einschätzungen, keine Messwerte.</p>
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
   "title": "Bildsprache – One motif, many visual languages",
   "desc": "16 fixed motifs in many image styles, each image with a copyable prompt. Against the interchangeable AI look: "
           "photography, painting, printmaking, infographics, posters, pixel art and more.",
   "eyebrow": "Style catalogue for AI image generation",
   "h1": "One motif,<br><em>many visual languages.</em>",
   "lede": "AI images often look alike: warm backlight, smooth skin, centred subjects, infographics built from the same "
           "colourful tiles. That is often less the model's doing than the prompt's. Here <strong>the same motif runs "
           "through many styles</strong>, and every image shows the prompt that made it.",
   "hero_slider": "Slider: the style on the left, the same motif without a style on the right",
   "hero_h": "Same content, different prompt",
   "hero_p": "Both images describe the same scene word for word. The right one only lacks the style block. Drag the "
             "slider and pick a style.",
   "hero_pick": "Pick a style",
   "hero_more": "Fact sheet:",
   "base_h": "Without a style, much looks the same",
   "base_p": "These 16 images come from complete, precise motif descriptions, only without any mention of medium, era, "
             "light or technique. What comes out is the model's default look.",
   "base_link": "How to recognise it →",
   "motifs_h": "16 motifs",
   "motifs_p": "Each motif fixes the content, not the arrangement. All of them are set on the fictional island of "
               "Lornholm. People, infographic, poster, map, data chart and the other graphic types each test something else.",
   "flag_h": "Lead styles across all motifs",
   "flag_p": "A style is not a filter but a system of decisions about line, surface, lettering and structure. These "
             "styles run through all 16 motifs.",
   "anat_h": "How every prompt is built",
   "anat_p": "Three parts, always in the same order. The motif block is identical for every image of a motif, the style "
             "block for every image of a style. Whatever differs between two images therefore sits in the style block only.",
   "anat_side": "<p>The <b>style block</b> covers medium and technique, and also composition, lettering and the way the "
                "style organises information. Without that, the model keeps its default composition and lays the style "
                "on top like a filter.</p><p>The <b>guards</b> state the format, the allowed text and what must not be "
                "prettified.</p>",
   "cats_h": "{n} styles in 14 categories",
   "cats_p": "The lexicon lists every style with its markers and a prompt fragment, including those without an example "
             "image. From the daguerreotype portrait to the Frutiger Aero wallpaper.",
  },
  "motifs": {
   "title": "16 motifs – Bildsprache", "desc": "The 16 reference motifs of Bildsprache, each in many styles.",
   "eyebrow": "Reference motifs", "h1": "16 motifs",
   "lede": "Each motif is a fixed text that describes the content: who, what, where, which objects. Colour, light, optics, "
           "medium and arrangement are left to the style. That keeps styles comparable without every image being built "
           "the same way.",
  },
  "motif": {
   "format": "Format", "strings": "Strings in image", "tier": "Rank",
   "block_h": "Motif block", "block_p": "This text appears word for word in every prompt for this motif.",
   "tests_h": "What the motif tests", "text_h": "Exact text in the image",
   "base_h": "No style given", "base_p": "The same prompt twice, without a style block. How similar the two runs are "
                                        "shows how stable the default look is.",
   "grid_h": "In {n} styles", "grid_p": "Click an image to see the full prompt, split into style, motif and guards, "
                                        "and to compare it with the baseline.",
   "filter": "Filter by category",
   "de_h": "With German text in the image", "de_p": "The same styles with German labels. Umlauts and the degree sign "
                                                   "are a good stress test for text rendering.",
  },
  "styles": {
   "title": "Lead styles – Bildsprache", "desc": "The lead styles of Bildsprache with fact sheet, style block and example images.",
   "eyebrow": "Lead styles", "h1": "Styles with images",
   "lede": "{n} styles with a fact sheet, a copyable style block and example images. More styles without images are in the lexicon.",
  },
  "style": {
   "era": "Period", "category": "Category", "feasibility": "Feasibility", "distinct": "Distance from AI look",
   "block_h": "Style block", "block_p": "Put this block in front of your motif description. It is identical in every image of this style.",
   "origin_h": "Origin", "markers_h": "Markers", "aka": "Also known as", "family": "Classification",
   "escapes_h": "Why it does not look like AI", "escapes_ai_h": "Why it looks like AI", "pitfalls_h": "Where it goes wrong", "tip_h": "Tip",
   "sens_h": "Keep in mind", "sources_h": "Sources", "sheet_h": "Fact sheet",
   "row_h": "On {n} motifs", "row_p": "The same style block with different motif blocks.",
   "related_h": "Related styles in the lexicon", "related_p": "More styles of the same family in the lexicon, without their own fact sheet.",
  },
  "lexicon": {
   "title": "Lexicon: {n} image styles – Bildsprache", "desc": "{n} image styles with markers and a prompt fragment, searchable.",
   "eyebrow": "Lexicon", "h1": "{n} image styles",
   "lede": "Each entry gives the origin, the markers and an English prompt fragment you can append to your own motif "
           "description. Feasibility and distance from the AI look are editorial judgements. Only the lead styles were "
           "tested with images.",
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
checked one by one for plausibility, but only the {lead} lead styles were also tested with images. Feasibility and
distance from the AI look are editorial judgements, not measurements.</p>
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
