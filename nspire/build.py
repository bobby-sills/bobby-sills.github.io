#!/usr/bin/env python3
"""Regenerate the games page from games.json.

Adding a game is: drop its screenshot in nspire/images/, add an entry to
nspire/games.json, run this. It rewrites the card list on the games page and
the count in the prose on both pages.

The cards are written into the HTML rather than built in the browser so the
page keeps working with JavaScript off — the downloads are the whole point of
it, and a search engine should be able to read them. That costs this script
being run; nothing else here needs a build step.

    python3 nspire/build.py            # rewrite
    python3 nspire/build.py --check    # fail if the files are out of date

Run from anywhere; paths resolve against this file.
"""

import argparse
import json
import pathlib
import re
import struct
import sys
import textwrap

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = "https://raw.githubusercontent.com/bobby-sills/tinspire-game/main/"

WORDS = """zero one two three four five six seven eight nine ten eleven twelve
thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty""".split()


def png_size(path):
    """Width and height from a PNG header, so the card carries the real
    intrinsic size and the browser reserves the right box before it loads."""
    header = path.read_bytes()[:24]
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"{path} is not a PNG")
    return struct.unpack(">II", header[16:24])


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def card(game):
    image = HERE / "images" / game["image"]
    if not image.exists():
        raise SystemExit(f"missing screenshot: {image}")
    width, height = png_size(image)

    # Wrapped to the width the rest of the file uses; textwrap counts the
    # indent within it. Hyphens must not be break points — a line ending on
    # "hand-" puts a space into the rendered sentence, because HTML folds the
    # newline into one. Long tokens stay whole for the same reason.
    body = "\n".join(
        textwrap.wrap(game["description"], width=80,
                      initial_indent=" " * 12, subsequent_indent=" " * 12,
                      break_on_hyphens=False, break_long_words=False)
    )
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
{body}
          </p>
        </li>
"""


def rewrite(games):
    """Return {path: new text} for every file this script owns a part of."""
    out = {}

    page = HERE / "index.html"
    text = page.read_text(encoding="utf-8")
    start = text.index('      <ul class="games">\n') + len('      <ul class="games">\n')
    end = text.index("      </ul>", start)
    out[page] = text[:start] + "".join(card(g) for g in games) + text[end:]

    # The count is written out in prose on both pages; keep it honest.
    count = WORDS[len(games)] if len(games) < len(WORDS) else str(len(games))
    pattern = re.compile(r"\b(%s|\d+)(\s+games for the ti-nspire cx ii)" % "|".join(WORDS))
    for path in (page, ROOT / "index.html"):
        text = out.get(path, path.read_text(encoding="utf-8"))
        text, n = pattern.subn(lambda m: count + m.group(2), text)
        if not n:
            raise SystemExit(f"no game count found in {path}")
        out[path] = text

    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit non-zero if any file is out of date")
    args = ap.parse_args()

    games = json.loads((HERE / "games.json").read_text(encoding="utf-8"))
    if not games:
        raise SystemExit("games.json is empty")

    stale = []
    for path, text in rewrite(games).items():
        if path.read_text(encoding="utf-8") == text:
            continue
        stale.append(path)
        if not args.check:
            path.write_text(text, encoding="utf-8")

    rel = [str(p.relative_to(ROOT)) for p in stale]
    if args.check:
        print("out of date: " + ", ".join(rel) if rel else "up to date")
        sys.exit(1 if rel else 0)
    print(f"{len(games)} games -> " + (", ".join(rel) if rel else "no changes"))


if __name__ == "__main__":
    main()
