#!/usr/bin/env python3
"""Regenerate the card lists on both pages from JSON.

Adding a project: drop its image in images/, add an entry to projects.json,
run this. Adding a game: drop its screenshot in nspire/images/, add an entry
to nspire/games.json, run this — it also keeps the game count in the prose on
both pages in step with the list.

The cards are written into the HTML rather than built in the browser so the
pages keep working with JavaScript off, and so a search engine can read them —
the games page exists to hand out downloads. That costs this script being run;
nothing else here needs a build step.

    python3 build.py            # rewrite
    python3 build.py --check    # exit non-zero if a page is out of date

Run from anywhere; paths resolve against this file.
"""

import argparse
import json
import pathlib
import re
import struct
import sys
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent
RAW = "https://raw.githubusercontent.com/bobby-sills/tinspire-game/main/"

WORDS = """zero one two three four five six seven eight nine ten eleven twelve
thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty""".split()


def image_size(path):
    """Intrinsic size, so a card reserves the right box before the image
    loads instead of reflowing the grid under it."""
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":  # JPEG: walk the segments to the frame header
        i = 2
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3):
                height, width = struct.unpack(">HH", data[i + 5 : i + 9])
                return width, height
            if marker == 0xD8 or 0xD0 <= marker <= 0xD9:
                i += 2
                continue
            i += 2 + struct.unpack(">H", data[i + 2 : i + 4])[0]
    raise SystemExit(f"cannot read the size of {path}")


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(text, indent):
    """Hyphens are not break points: a line ending on "hand-" puts a space
    into the rendered sentence, because HTML folds the newline into one."""
    return "\n".join(
        textwrap.wrap(text, width=80, initial_indent=" " * indent,
                      subsequent_indent=" " * indent,
                      break_on_hyphens=False, break_long_words=False)
    )


def anchor(link, indent):
    """Anything leaving the site opens in a new tab; a link within it doesn't."""
    pad = " " * indent
    if link["href"].startswith("http"):
        return (f'{pad}<a\n{pad}  href="{link["href"]}"\n{pad}  target="_blank"\n'
                f'{pad}  rel="noopener"\n{pad}  >{esc(link["text"])}</a\n{pad}>')
    return f'{pad}<a href="{link["href"]}">{esc(link["text"])}</a>'


def project_card(project):
    image = ROOT / "images" / project["image"]
    if not image.exists():
        raise SystemExit(f"missing image: {image}")
    width, height = image_size(image)
    links = f"\n{' ' * 12}·\n".join(anchor(l, 12) for l in project["links"])
    return f"""        <li>
          <img
            src="images/{project["image"]}"
            alt="{esc(project["alt"])}"
            width="{width}"
            height="{height}"
          />
          <h3>{esc(project["name"])}</h3>
          <p class="project-links">
{links}
          </p>
          <p>
{wrap(project["description"], 12)}
          </p>
        </li>
"""


def game_card(game):
    image = ROOT / "nspire" / "images" / game["image"]
    if not image.exists():
        raise SystemExit(f"missing screenshot: {image}")
    width, height = image_size(image)
    return f"""        <li>
          <img
            src="images/{game["image"]}"
            alt="{esc(game["alt"])}"
            width="{width}"
            height="{height}"
            loading="lazy"
          />
          <h3>{esc(game["name"])}</h3>
          <p class="game-links">
            <a
              href="{RAW}{game["file"]}"
              >download</a
            >
          </p>
          <p>
{wrap(game["description"], 12)}
          </p>
        </li>
"""


def replace_list(text, ul, cards):
    opening = f'      <ul class="{ul}">\n'
    start = text.index(opening) + len(opening)
    end = text.index("      </ul>", start)
    return text[:start] + cards + text[end:]


def rewrite(projects, games):
    home = ROOT / "index.html"
    page = ROOT / "nspire" / "index.html"
    out = {
        home: replace_list(home.read_text(encoding="utf-8"), "projects",
                           "".join(project_card(p) for p in projects)),
        page: replace_list(page.read_text(encoding="utf-8"), "games",
                           "".join(game_card(g) for g in games)),
    }

    # The game count is written out in prose on both pages; keep it honest.
    count = WORDS[len(games)] if len(games) < len(WORDS) else str(len(games))
    pattern = re.compile(r"\b(%s|\d+)(\s+games for the ti-nspire cx ii)" % "|".join(WORDS))
    for path in (home, page):
        text, n = pattern.subn(lambda m: count + m.group(2), out[path])
        if not n:
            raise SystemExit(f"no game count found in {path}")
        out[path] = text

    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit non-zero if a page is out of date")
    args = ap.parse_args()

    projects = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))
    games = json.loads((ROOT / "nspire" / "games.json").read_text(encoding="utf-8"))
    if not projects or not games:
        raise SystemExit("projects.json and games.json must both have entries")

    stale = []
    for path, text in rewrite(projects, games).items():
        if path.read_text(encoding="utf-8") == text:
            continue
        stale.append(str(path.relative_to(ROOT)))
        if not args.check:
            path.write_text(text, encoding="utf-8")

    if args.check:
        print("out of date: " + ", ".join(stale) if stale else "up to date")
        sys.exit(1 if stale else 0)
    print(f"{len(projects)} projects, {len(games)} games -> "
          + (", ".join(stale) if stale else "no changes"))


if __name__ == "__main__":
    main()
