#!/usr/bin/env python3
"""Regenerate the card lists on every page from JSON.

Adding a project: drop its image in images/, add an entry to projects.json,
run this. Adding a game: drop its screenshot in ti-nspire-games/images/,
add an entry to ti-nspire-games/games.json, run this — it also keeps the game
count in the prose on both pages in step with the list. Adding a photo: drop it
in photography/images/ (about 2000px on the long edge is plenty), add an entry
to photography/photos.json, run this — it makes the collage thumbnail in
photography/thumbs/ itself, using macOS's sips, and reads the camera from the
photo's EXIF unless its entry sets "camera". A photo's tile in the mosaic
follows its shape unless its entry sets "size" to one of SIZES.

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
import subprocess
import sys
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent
RAW = "https://raw.githubusercontent.com/bobby-sills/tinspire-game/main/"

WORDS = """zero one two three four five six seven eight nine ten eleven twelve
thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty""".split()

# The phrases the spelled-out game count leads, one per page. Reword either
# sentence and its phrase has to be reworded here too — otherwise the count
# goes unfound and the run fails rather than quietly drifting.
COUNT_PHRASES = ("games for the ti-nspire cx ii", "games to play on your calculator",
                 "games</a")


EXIF_ORIENTATION, EXIF_MAKE, EXIF_MODEL = 0x0112, 0x010F, 0x0110


def exif_tags(data):
    """The main EXIF directory of a JPEG as {tag: value}, empty if it has
    none. Only text and short-integer values are read; that covers the
    orientation and the camera, which is all this script asks for."""
    start = data.find(b"Exif\x00\x00", 0, 0x10000)
    if start < 0:
        return {}
    tiff = start + 6
    order = "<" if data[tiff : tiff + 2] == b"II" else ">"
    (ifd,) = struct.unpack(order + "I", data[tiff + 4 : tiff + 8])
    (count,) = struct.unpack(order + "H", data[tiff + ifd : tiff + ifd + 2])
    tags = {}
    for n in range(count):
        entry = tiff + ifd + 2 + n * 12
        tag, kind, length = struct.unpack(order + "HHI", data[entry : entry + 8])
        if kind == 3:  # SHORT, stored in place
            (tags[tag],) = struct.unpack(order + "H", data[entry + 8 : entry + 10])
        elif kind == 2:  # ASCII, in place if it fits in four bytes
            if length <= 4:
                raw = data[entry + 8 : entry + 8 + length]
            else:
                (offset,) = struct.unpack(order + "I", data[entry + 8 : entry + 12])
                raw = data[tiff + offset : tiff + offset + length]
            tags[tag] = raw.rstrip(b"\x00").decode("utf-8", "replace").strip()
    return tags


def exif_orientation(data):
    """The Orientation tag, or 1 (upright) if none."""
    return exif_tags(data).get(EXIF_ORIENTATION, 1)


def exif_camera(path):
    """The camera a photo was taken on, as the site writes it: lowercase, no
    brackets, and without the maker repeated where the model name already
    starts with it ("Nothing" + "Nothing Phone (2a)" -> "nothing phone 2a").
    None when editing apps have stripped it — set "camera" in photos.json for
    those."""
    tags = exif_tags(path.read_bytes())
    make, model = tags.get(EXIF_MAKE, ""), tags.get(EXIF_MODEL, "")
    if not model:
        return None
    if make and not model.lower().startswith(make.lower()):
        model = f"{make} {model}"
    return model.lower().replace("(", "").replace(")", "")


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
                # Browsers draw the photo turned by its EXIF orientation, so a
                # camera's portrait shot stored sideways has to be measured
                # turned too, or the collage gives it a landscape-shaped slot.
                if exif_orientation(data) in (5, 6, 7, 8):
                    width, height = height, width
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
    image = ROOT / "ti-nspire-games" / "images" / game["image"]
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
          <div class="game-head">
            <h3>{esc(game["name"])}</h3>
            ·
            <a
              href="{RAW}{game["file"]}"
              >download</a
            >
          </div>
        </li>
"""


# Tile shapes in the photo mosaic, matching .photos classes in the stylesheet.
SIZES = ("portrait", "landscape", "small", "panorama", "big", "big-portrait")

THUMB_EDGE = 800  # px on the long edge; the collage never shows them wider


def thumbnail(name):
    """The collage loads every photo at once, so it gets small copies and only
    the viewer fetches the full files. Made once and then left alone — delete a
    thumb to have it remade after replacing its photo."""
    src = ROOT / "photography" / "images" / name
    thumb = ROOT / "photography" / "thumbs" / name
    if not src.exists():
        raise SystemExit(f"missing photo: {src}")
    if not thumb.exists():
        thumb.parent.mkdir(exist_ok=True)
        try:
            subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions",
                            "75", "-Z", str(THUMB_EDGE), str(src), "--out",
                            str(thumb)], check=True, capture_output=True)
        except (OSError, subprocess.CalledProcessError) as e:
            raise SystemExit(f"cannot make a thumbnail of {src}: {e}")
    return thumb


def photo_card(photo):
    width, height = image_size(thumbnail(photo["image"]))
    size = photo.get("size", "portrait" if height > width else "landscape")
    if size not in SIZES:
        raise SystemExit(f"{photo['image']}: size must be one of {', '.join(SIZES)}")
    camera = photo.get("camera") or exif_camera(
        ROOT / "photography" / "images" / photo["image"])
    camera_attr = f' data-camera="{esc(camera)}"' if camera else ""
    return f"""        <li class="{size}">
          <a href="images/{photo["image"]}" data-title="{esc(photo["title"])}"{camera_attr}>
            <img
              src="thumbs/{photo["image"]}"
              alt="{esc(photo["alt"])}"
              width="{width}"
              height="{height}"
              loading="lazy"
            />
          </a>
        </li>
"""


def replace_list(text, ul, cards):
    opening = f'      <ul class="{ul}">\n'
    start = text.index(opening) + len(opening)
    end = text.index("      </ul>", start)
    return text[:start] + cards + text[end:]


def rewrite(projects, games, photos):
    home = ROOT / "index.html"
    page = ROOT / "ti-nspire-games" / "index.html"
    gallery = ROOT / "photography" / "index.html"
    out = {
        home: replace_list(home.read_text(encoding="utf-8"), "projects",
                           "".join(project_card(p) for p in projects)),
        page: replace_list(page.read_text(encoding="utf-8"), "games",
                           "".join(game_card(g) for g in games)),
        gallery: replace_list(gallery.read_text(encoding="utf-8"), "photos",
                              "".join(photo_card(p) for p in photos)),
    }

    # The game count is written out in prose on both pages; keep it honest.
    count = WORDS[len(games)] if len(games) < len(WORDS) else str(len(games))
    pattern = re.compile(r"\b(%s|\d+)(\s+(?:%s))"
                         % ("|".join(WORDS), "|".join(COUNT_PHRASES)))
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
    games_json = ROOT / "ti-nspire-games" / "games.json"
    games = json.loads(games_json.read_text(encoding="utf-8"))
    photos_json = ROOT / "photography" / "photos.json"
    photos = json.loads(photos_json.read_text(encoding="utf-8"))
    if not projects or not games or not photos:
        raise SystemExit("projects.json, games.json and photos.json must all "
                         "have entries")

    stale = []
    for path, text in rewrite(projects, games, photos).items():
        if path.read_text(encoding="utf-8") == text:
            continue
        stale.append(str(path.relative_to(ROOT)))
        if not args.check:
            path.write_text(text, encoding="utf-8")

    if args.check:
        print("out of date: " + ", ".join(stale) if stale else "up to date")
        sys.exit(1 if stale else 0)
    print(f"{len(projects)} projects, {len(games)} games, "
          f"{len(photos)} photos -> "
          + (", ".join(stale) if stale else "no changes"))


if __name__ == "__main__":
    main()
