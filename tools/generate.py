#!/usr/bin/env python3
"""Erzeugt Bilder über das eingebaute image_gen-Werkzeug von Codex CLI.

Jeder Auftrag läuft als `codex exec --json` in einer read-only-Sandbox. Das erste JSONL-Ereignis
nennt die Thread-ID, und Codex legt das Bild unter $CODEX_HOME/generated_images/<thread>/ ab.
Dadurch laufen parallele Aufträge ohne Rätselraten, welches Bild zu welchem Prompt gehört.

    python3 tools/generate.py jobs.json --workers 4

jobs.json: [{"type": "people", "style": "risograph", "attempt": 1, "size": "1536x1024",
             "prompt": "...", "lang": "en"}]
Ergebnis: originals/<type>/<style>[.de]-<attempt>.png plus .json mit Prompt und Metadaten.
originals/ ist nicht eingecheckt; tools/optimize.py erzeugt daraus die WebP-Dateien der Website.
"""
import argparse, concurrent.futures as cf, datetime, json, os, pathlib, shutil, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
ORIG = ROOT / "originals"
CODEX_HOME = pathlib.Path(os.environ.get("CODEX_HOME", pathlib.Path.home() / ".codex"))
SHAPE = {"1024x1024": "square (1:1)", "1536x1024": "landscape (3:2)", "1024x1536": "portrait (2:3)"}

INSTRUCTION = """Call your built-in image generation tool exactly once with the prompt below, \
as a {shape} image ({size}). Pass the prompt through verbatim; do not rewrite, shorten or embellish it. \
Do not run shell commands. When the image exists, reply only OK.

PROMPT:
{prompt}"""


def stem(job):
    lang = ".de" if job.get("lang") == "de" else ""
    return ORIG / job["type"] / f"{job['style']}{lang}-{job.get('attempt', 1)}"


def run(job, timeout):
    base = stem(job)
    # Nicht with_suffix: bei "woodcut.de-1" hielte pathlib ".de-1" für die Endung.
    png, meta = base.parent / (base.name + ".png"), base.parent / (base.name + ".json")
    if png.exists():
        return job, "skip", 0.0
    base.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    text = INSTRUCTION.format(shape=SHAPE.get(job["size"], job["size"]), size=job["size"], prompt=job["prompt"])
    try:
        p = subprocess.run(
            ["codex", "exec", "--json", "--skip-git-repo-check", "--ephemeral", "-s", "read-only",
             "-C", str(base.parent), text],
            stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return job, "timeout", time.time() - t0
    thread, reply = None, ""
    for line in p.stdout.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "thread.started":
            thread = ev["thread_id"]
        item = ev.get("item") or {}
        if item.get("type") == "agent_message":
            reply = item.get("text", "")
    if not thread:
        return job, "no-thread: " + p.stderr[-300:].replace("\n", " "), time.time() - t0
    pngs = sorted((CODEX_HOME / "generated_images" / thread).glob("*.png"), key=lambda f: f.stat().st_mtime)
    if not pngs:
        return job, "no-image: " + reply[:200].replace("\n", " "), time.time() - t0
    shutil.copy2(pngs[-1], png)
    secs = time.time() - t0
    meta.write_text(json.dumps({
        **job,
        "thread_id": thread,
        "seconds": round(secs, 1),
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "tool": "Codex CLI built-in image_gen",
        "codex_version": CODEX_VERSION,
        "pngs_in_thread": len(pngs),
    }, ensure_ascii=False, indent=1))
    return job, "ok", secs


def main():
    global CODEX_VERSION
    ap = argparse.ArgumentParser()
    ap.add_argument("jobs")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=480)
    a = ap.parse_args()
    CODEX_VERSION = subprocess.run(["codex", "--version"], capture_output=True, text=True).stdout.strip()
    jobs = json.loads(pathlib.Path(a.jobs).read_text())
    fails = 0
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for job, status, secs in ex.map(lambda j: run(j, a.timeout), jobs):
            fails += status not in ("ok", "skip")
            print(f"{status[:60]:24} {secs:6.1f}s  {job['type']}/{job['style']}"
                  f"{'.de' if job.get('lang') == 'de' else ''}-{job.get('attempt', 1)}", flush=True)
    print(f"{len(jobs) - fails}/{len(jobs)} ok", flush=True)
    return 1 if fails else 0


CODEX_VERSION = ""

if __name__ == "__main__":
    sys.exit(main())
