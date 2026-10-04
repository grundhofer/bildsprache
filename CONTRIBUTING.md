# Mitmachen / Contributing

*Deutsch unten, English below.*

---

## Deutsch

Willkommen sind **Korrekturen** an Faktenblättern und Lexikoneinträgen sowie **neue Stile**.

### Korrekturen

Falsche Jahreszahlen, falsch zugeschriebene Techniken, ungenaue Begriffe: gern per Issue oder Pull Request, bei
strittigen Fakten mit Quelle. Machbarkeit und „Abstand zum KI-Look“ sind redaktionelle Einschätzungen; Änderungen
bitte begründen.

### Einen Stil ergänzen

1. Faktenblatt `styles/<slug>.json` anlegen, mit `style_block` (Englisch, 90–150 Wörter) und den Feldern `de` und `en`
   (`name`, `aka`, `era`, `summary`, `origin`, `markers`, `escapes`, `pitfalls`, `tip`, `sensitivity`) sowie `sources`.
   Der Slug muss im Lexikon (`data/lexicon.json`) existieren.
2. Der Stilblock ist motivneutral und beschreibt Medium, **Komposition**, **Schrift** und, wo nötig, den
   **Informationsaufbau** des Stils, zum Schluss was zu vermeiden ist. Ein Block, der nur die Oberfläche beschreibt,
   wirkt wie ein Filter (siehe Methodenseite).
3. Keine lebenden Künstlerinnen und Künstler, keine Studios, keine Marken als Stilangabe. Markennamen nur, wo sie ein
   technisches Verfahren bezeichnen. Heilige oder gemeinschaftsgebundene Traditionen werden nicht als Prompt angeboten.
4. Den Stil in `data/matrix.json` den passenden Motiven zuordnen.
5. Bilder erzeugen und prüfen:
   ```sh
   python3 tools/plan.py jobs.json
   python3 tools/generate.py jobs.json     # braucht ein angemeldetes Codex CLI
   ```
   Jedes Bild bekommt in `data/qa.json` ein Prüfergebnis (`pass`, `flawed` oder `fail`) mit Notiz und Alt-Text auf
   Deutsch und Englisch. Danach `python3 tools/manifest.py`, `python3 tools/optimize.py` und `python3 build.py`.

Der Build prüft, dass jeder veröffentlichte Prompt genau aus dem aktuellen Motiv- und Stilblock besteht. Wer einen
Stilblock ändert, muss dessen Bilder neu erzeugen; `tools/plan.py` findet sie automatisch.

### Motive

Die Motivblöcke in `data/motifs.json` sind fest. Eine Änderung macht alle Bilder des Motivs ungültig und sollte nur
mit gutem Grund vorgeschlagen werden.

---

## English

**Corrections** to fact sheets and lexicon entries and **new styles** are welcome.

### Corrections

Wrong dates, misattributed techniques, imprecise terms: please open an issue or pull request, with a source for
disputed facts. Feasibility and "distance from the AI look" are editorial judgements; please explain proposed changes.

### Adding a style

1. Create `styles/<slug>.json` with a `style_block` (English, 90–150 words), the `de` and `en` fields (`name`, `aka`,
   `era`, `summary`, `origin`, `markers`, `escapes`, `pitfalls`, `tip`, `sensitivity`) and `sources`. The slug must
   exist in the lexicon (`data/lexicon.json`).
2. The style block is motif-agnostic and covers the medium, the **composition**, the **lettering** and, where needed,
   the **information layout** of the style, ending with what to avoid. A block that only describes the surface acts
   like a filter (see the method page).
3. No living artists, studios or brands as style references. Brand names only where they denote a technical process.
   Sacred or community-bound traditions are not offered as prompts.
4. Assign the style to suitable motifs in `data/matrix.json`.
5. Generate and review the images:
   ```sh
   python3 tools/plan.py jobs.json
   python3 tools/generate.py jobs.json     # needs a logged-in Codex CLI
   ```
   Every image gets a review result in `data/qa.json` (`pass`, `flawed` or `fail`) with a note and alt text in German
   and English. Then run `python3 tools/manifest.py`, `python3 tools/optimize.py` and `python3 build.py`.

The build checks that every published prompt consists exactly of the current motif and style block. Changing a style
block means regenerating its images; `tools/plan.py` finds them automatically.

### Motifs

The motif blocks in `data/motifs.json` are fixed. Changing one invalidates every image of that motif, so please only
propose it for a good reason.
