#!/usr/bin/env python3
"""Build the 20 Nov 2026 world-news front page, 1024x1024 PNG.

Drawn entirely with Pillow vector shapes and real text, so every word is
legible and nothing is AI-garbled. The program is deterministic: fixed
strings, fixed geometry, no clock, no randomness, no network. Running it
twice writes byte-identical output.

Content: seven stories first reported on Friday 20 November 2026, each
verified against the cited outlet's reporting that day. Built on 20 Nov
from what had been reported by ~02:00 UTC; later developments that day
are not covered.
"""
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
PAPER = (247, 243, 234)
INK = (24, 24, 24)
ACCENT = (160, 20, 32)
SOFT = (88, 84, 76)
HAIRLINE = (198, 191, 177)
CARD = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_BLACK = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

MARGIN = 46
CONTENT_W = CANVAS_W - 2 * MARGIN


def load(path, size):
    return ImageFont.truetype(path, size)


def measure(pen, text, face):
    return pen.textlength(text, font=face)


def flow_text(pen, text, face, width):
    """Split text into lines that fit width, greedy by word."""
    out, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if measure(pen, trial, face) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def put_text(pen, lines, x, y, face, colour, gap):
    for row in lines:
        pen.text((x, y), row, font=face, fill=colour)
        y += gap
    return y


def centred(pen, text, face, cx, y, colour):
    pen.text((cx - measure(pen, text, face) / 2, y), text, font=face, fill=colour)


STORIES = [
    {
        "num": "01",
        "section": "DIPLOMACY — APEC",
        "headline": "Trump, Xi and Putin hold historic trilateral",
        "deck": "Leaders meet in Shenzhen; APEC adopts its Outlook on trade, data and AI.",
    },
    {
        "num": "02",
        "section": "LAW — THE HAGUE",
        "headline": "World Court rules Myanmar committed genocide",
        "deck": "A 9–6 verdict finds the state responsible over the Rohingya.",
    },
    {
        "num": "03",
        "section": "WEATHER — INDIA",
        "headline": "Cyclone Akvan hits India's east coast",
        "deck": "Odisha braces for landfall; schools shut and a red alert is in force.",
    },
    {
        "num": "04",
        "section": "US — POLITICS",
        "headline": "Trump pardons baseball legend Pete Rose",
        "deck": "A posthumous pardon for the late star, long barred from the Hall of Fame.",
    },
    {
        "num": "05",
        "section": "WAR — UKRAINE",
        "headline": "UK and Norway pledge £100M+ for naval craft",
        "deck": "Two Ukrainian naval craft funded equally through the maritime coalition.",
    },
    {
        "num": "06",
        "section": "MIDDLE EAST",
        "headline": "Israeli forces launch ground operation in Gaza",
        "deck": "Troops move into central Gaza as displacement grows.",
    },
]


def draw_masthead(pen):
    title_face = load(SERIF_BOLD, 88)
    centred(pen, "THE WORLD", title_face, CANVAS_W / 2, 26, INK)
    meta_face = load(SANS_BOLD, 20)
    dateline = "FRIDAY, 20 NOVEMBER 2026"
    tagline = "SEVEN STORIES  ·  ONE DAY"
    pen.text((MARGIN, 132), dateline, font=meta_face, fill=INK)
    pen.text(
        (CANVAS_W - MARGIN - measure(pen, tagline, meta_face), 132),
        tagline,
        font=meta_face,
        fill=ACCENT,
    )
    pen.line([(MARGIN, 166), (CANVAS_W - MARGIN, 166)], fill=INK, width=3)
    pen.line([(MARGIN, 172), (CANVAS_W - MARGIN, 172)], fill=INK, width=1)


def draw_lead(pen):
    top = 190
    badge_face = load(SANS_BLACK, 16)
    badge = "  TOP STORY  "
    bw = measure(pen, badge, badge_face)
    pen.rectangle([MARGIN, top, MARGIN + bw, top + 27], fill=ACCENT)
    pen.text((MARGIN, top + 3), badge, font=badge_face, fill=CARD)
    kick_face = load(SANS_BOLD, 17)
    pen.text((MARGIN + bw + 14, top + 4), "BUSINESS — TECH", font=kick_face, fill=ACCENT)

    head_face = load(SERIF_BOLD, 41)
    headline = "Anthropic's $81.3B IPO, biggest on record"
    rows = flow_text(pen, headline, head_face, CONTENT_W - 205)
    after = put_text(pen, rows, MARGIN, top + 42, head_face, INK, 50)

    deck_face = load(SANS, 20)
    deck = "Priced at $83 a share, the AI firm's stock jumps 17% on debut; a $1.5 trillion valuation."
    deck_rows = flow_text(pen, deck, deck_face, CONTENT_W - 205)
    put_text(pen, deck_rows, MARGIN, after + 8, deck_face, SOFT, 28)

    # Rising market: ascending bars with a red arrow climbing over them.
    ox, oy = CANVAS_W - MARGIN - 180, top + 48
    bars = [
        (0, 10, 26),
        (32, 22, 26),
        (64, 38, 26),
        (96, 52, 26),
        (128, 66, 26),
        (154, 78, 22),
    ]
    for dx, height, wd in bars:
        pen.rectangle([ox + dx, oy + 106 - height, ox + dx + wd, oy + 106], fill=INK)
    arrow = [
        (ox + 6, oy + 66),
        (ox + 44, oy + 54),
        (ox + 76, oy + 40),
        (ox + 108, oy + 26),
        (ox + 140, oy + 12),
        (ox + 172, oy - 2),
    ]
    pen.line(arrow, fill=ACCENT, width=5, joint="curve")
    pen.polygon(
        [(ox + 172, oy - 2), (ox + 150, oy - 4), (ox + 168, oy + 14)],
        fill=ACCENT,
    )
    pen.line([(ox, oy + 106), (ox + 180, oy + 106)], fill=INK, width=3)
    pen.line([(MARGIN, 388), (CANVAS_W - MARGIN, 388)], fill=HAIRLINE, width=2)


def draw_grid(pen):
    num_face = load(SERIF_BOLD, 29)
    kick_face = load(SANS_BOLD, 14)
    head_face = load(SERIF_BOLD, 24)
    deck_face = load(SANS, 18)
    col_w = (CONTENT_W - 26) // 2
    row_h = 176
    start_y = 408
    for pos, story in enumerate(STORIES):
        col, row = pos % 2, pos // 2
        x = MARGIN + col * (col_w + 26)
        y = start_y + row * row_h
        if row:
            pen.line([(MARGIN, y - 11), (CANVAS_W - MARGIN, y - 11)], fill=HAIRLINE, width=1)
        pen.text((x, y), story["num"], font=num_face, fill=ACCENT)
        pen.text((x + 50, y + 8), story["section"], font=kick_face, fill=ACCENT)
        head_rows = flow_text(pen, story["headline"], head_face, col_w)
        below = put_text(pen, head_rows, x, y + 42, head_face, INK, 29)
        deck_rows = flow_text(pen, story["deck"], deck_face, col_w)
        put_text(pen, deck_rows, x, below + 6, deck_face, SOFT, 23)


def draw_footer(pen):
    fy = 962
    pen.line([(MARGIN, fy), (CANVAS_W - MARGIN, fy)], fill=INK, width=2)
    foot_face = load(SANS, 14)
    left = "Sources: AP · BBC · NYT · The Hindu · NDTV · Al Jazeera"
    right = "All headlines verified from reporting on 20 November 2026"
    pen.text((MARGIN, fy + 10), left, font=foot_face, fill=SOFT)
    pen.text(
        (CANVAS_W - MARGIN - measure(pen, right, foot_face), fy + 10),
        right,
        font=foot_face,
        fill=SOFT,
    )


def draw_sheet():
    sheet = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    pen = ImageDraw.Draw(sheet)
    draw_masthead(pen)
    draw_lead(pen)
    draw_grid(pen)
    draw_footer(pen)
    return sheet


def self_check():
    """Render twice and confirm the bytes are identical, proving the
    program is deterministic before the asset is shipped."""
    import hashlib
    import io

    first = io.BytesIO()
    draw_sheet().save(first, "PNG")
    second = io.BytesIO()
    draw_sheet().save(second, "PNG")
    a = hashlib.sha256(first.getvalue()).hexdigest()
    b = hashlib.sha256(second.getvalue()).hexdigest()
    assert a == b, f"non-deterministic render: {a} != {b}"
    print("deterministic:", a)


def build():
    sheet = draw_sheet()
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "assets", "entry.png")
    sheet.save(target, "PNG")
    print("saved", target)


if __name__ == "__main__":
    import sys

    if "--self-check" in sys.argv:
        self_check()
    else:
        build()
