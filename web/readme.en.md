[Deutsch lesen → README.de.md](README.de.md)

# Bildsprache

**One motif, many visual languages: AI images need not look alike.**

Image styles by use case (infographic, chart, icons, portrait, product, poster, illustration, map, mood image):
__N_IMAGES__ images in __N_LEAD__ lead styles, each with the prompt that made it, the style block on its own and a
template for your own content. Plus a lexicon of __N_LEX__ selected image styles and an overview of how to recognise AI images.

**[Open the catalogue](https://grundhofer.github.io/bildsprache/)** ·
[English](https://grundhofer.github.io/bildsprache/en/) ·
[Deutsch](https://grundhofer.github.io/bildsprache/de/)

![The same scene without a style and in four styles, next to the prompt structure.](og.png)

## What this is about

AI images often look alike: warm backlight, smooth skin, centred subjects, infographics built from the same
colourful tiles. That is usually the prompt's doing. Describe medium, technique, period, composition and lettering
precisely and you get very different images.

Bildsprache shows this on __N_MOTIFS__ graphic types, all set on the fictional island of Lornholm: people in a scene,
portrait, infographic, landscape, product, poster, editorial, street, food, animal, character, map, icon set, data
chart, interior and botanical study. Every motif runs through many styles, from ancient Egyptian wall painting via
cyanotype and the Polish School of Posters to pixel art.

## How a prompt is built

```
Style: <style block – medium, composition, lettering, information layout, things to avoid>

Subject: <motif block – identical for every image of a motif>

Constraints: <guards – format, allowed text, do not prettify, no logos>
```

The motif block fixes the content, not the arrangement. The style block is identical for every image of a style.
The baseline is the same prompt without a style block and shows the model's default look. The build verifies for every
published image that its prompt is assembled exactly this way.

## Contents

- **[Use cases](https://grundhofer.github.io/bildsprache/en/):** the entry point. Each use case groups one or more of the __N_MOTIFS__ motifs, shows them in every style with copy buttons (full prompt, style only) and has a template builder for your own content.
- **[Lead styles](https://grundhofer.github.io/bildsprache/en/styles/):** __N_LEAD__ fact sheets with origin, markers, a copyable style block and sources.
- **[Lexicon](https://grundhofer.github.io/bildsprache/en/lexicon/):** __N_LEX__ selected styles in 14 categories (lead styles plus every entry with high distance from the AI look and high feasibility), each with a prompt fragment, some with a small example image. `data/lexicon.json` holds all researched entries.
- **[AI look & levers](https://grundhofer.github.io/bildsprache/en/levers/):** typical markers of AI images, each with a counter-lever, and style levers for light, optics, composition, colour and lettering.
- **[Method](https://grundhofer.github.io/bildsprache/en/method/):** how images and texts were made, how they were checked and where the limits are.

## Build locally

Requires Python 3.12+. No package installation.

```sh
python3 build.py
python3 -m http.server 8000 --directory docs
python3 -m unittest discover -s tests -v
```

## Generate images

Images come from the built-in image tool of [Codex CLI](https://github.com/openai/codex) and need a logged-in Codex.
`cwebp` converts them for the site.

```sh
python3 tools/plan.py jobs.json          # cells without an image for the current prompt
python3 tools/generate.py jobs.json      # writes originals/<motif>/<style>-<n>.png
python3 tools/manifest.py                # picks the reviewed version per cell (data/qa.json)
python3 tools/optimize.py                # WebP files in images/
```

The lexicon example images use the same tool:

```sh
python3 tools/lexicon.py plan jobs.json  # lexicon styles without an example (--pilot, --category, --reroll)
python3 tools/generate.py jobs.json      # writes originals/lexicon/<style>-<n>.png
python3 tools/lexicon.py manifest        # picks the reviewed version per style (data/lexicon_qa.json)
python3 tools/lexicon.py optimize        # WebP files in images/lexicon/
```

## Project structure

| Path | Contents |
| --- | --- |
| `data/usecases.json` | The use cases: which motifs belong to them, template with placeholders |
| `data/motifs.json` | The motifs with motif block, format and allowed text |
| `data/matrix.json` | Which style appears on which motif |
| `data/lexicon.json` | All styles with category, markers and prompt fragment |
| `data/qa.json` | Review result for every image version, including discarded ones |
| `data/lexicon_motifs.json`, `data/lexicon_qa.json` | Motifs and review results of the lexicon example images |
| `styles/*.json` | Bilingual fact sheets of the lead styles with style block |
| `images/` | Published images (WebP) and `manifest.json` with prompt and metadata per image |
| `tools/` | Prompt builder, generator, planner, checks |
| `web/`, `build.py` | Page style, page script, copy and static generator |
| `docs/` | Generated site; not committed |

GitHub Actions checks the data and deploys `main` to GitHub Pages. [CONTRIBUTING.md](CONTRIBUTING.md) explains how to
add a style.

## Labelling and licence

All images are AI-generated (OpenAI image generation via Codex CLI) and labelled as such.
Code: [MIT](LICENSE). Texts: [CC BY 4.0](LICENSE-CONTENT.md). Images: [CC0](LICENSE-CONTENT.md).
Style names describe techniques, periods and movements; living artists, studios and brands are not used as styles.

Sibling project: [Designsprache](https://github.com/grundhofer/designsprache), a catalogue of UI design languages.

© Sebastian Grundhöfer
