#!/usr/bin/env python3
"""Render the 20 Nov 2026 world-news front page as a 1024x1024 PNG.

A FrontPage object owns the canvas, the drawing context and the fonts,
and paints the sheet in four passes: masthead, lead story, story grid,
footer. Every word is real text drawn with Pillow vector shapes, so
nothing is garbled. The build is deterministic: fixed strings, fixed
geometry, no clock, no randomness, no network. Two runs write
byte-identical output.

The seven stories are the ones first reported on Friday 20 November
2026, each verified against the cited outlet's reporting that day.
Built on 20 Nov from what had been reported by ~02:00 UTC; the day's
later news is not in it.
"""
import os

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1024, 1024
BACKGROUND = (247, 243, 234)
FOREGROUND = (24, 24, 24)
HIGHLIGHT = (160, 20, 32)
MUTED = (88, 84, 76)
RULE = (198, 191, 177)
CARD = (255, 255, 255)

SERIF_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_BLACK_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

EDGE = 46
INNER = WIDTH - 2 * EDGE

ITEMS = [
    (
        "01",
        "DIPLOMACY — APEC",
        "Trump, Xi and Putin hold historic trilateral",
        "Leaders meet in Shenzhen; APEC adopts its Outlook on trade, data and AI.",
    ),
    (
        "02",
        "LAW — THE HAGUE",
        "World Court rules Myanmar committed genocide",
        "A 9–6 verdict finds the state responsible over the Rohingya.",
    ),
    (
        "03",
        "WEATHER — INDIA",
        "Cyclone Akvan hits India's east coast",
        "Odisha braces for landfall; schools shut and a red alert is in force.",
    ),
    (
        "04",
        "US — POLITICS",
        "Trump pardons baseball legend Pete Rose",
        "A posthumous pardon for the late star, long barred from the Hall of Fame.",
    ),
    (
        "05",
        "WAR — UKRAINE",
        "UK and Norway pledge £100M+ for naval craft",
        "Two Ukrainian naval craft funded equally through the maritime coalition.",
    ),
    (
        "06",
        "MIDDLE EAST",
        "Israeli forces launch ground operation in Gaza",
        "Troops move into central Gaza as displacement grows.",
    ),
]


class FrontPage:
    """Paints one newspaper front page onto a Pillow canvas."""

    def __init__(self):
        self.sheet = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
        self.dc = ImageDraw.Draw(self.sheet)

    def _font(self, path, size):
        return ImageFont.truetype(path, size)

    def _width(self, text, face):
        return self.dc.textlength(text, font=face)

    def _wrap(self, text, face, width):
        """Greedy word wrap: split text into lines that fit width."""
        rows, current = [], ""
        for word in text.split():
            trial = f"{current} {word}".strip()
            if self._width(trial, face) <= width:
                current = trial
            else:
                if current:
                    rows.append(current)
                current = word
        if current:
            rows.append(current)
        return rows

    def _block(self, rows, x, y, face, colour, leading):
        for row in rows:
            self.dc.text((x, y), row, font=face, fill=colour)
            y += leading
        return y

    def _centred(self, text, face, cx, y, colour):
        self.dc.text(
            (cx - self._width(text, face) / 2, y), text, font=face, fill=colour
        )

    def masthead(self):
        title = self._font(SERIF_BOLD_PATH, 88)
        self._centred("THE WORLD", title, WIDTH / 2, 26, FOREGROUND)
        meta = self._font(SANS_BOLD_PATH, 20)
        self.dc.text((EDGE, 132), "FRIDAY, 20 NOVEMBER 2026", font=meta, fill=FOREGROUND)
        tag = "SEVEN STORIES  ·  ONE DAY"
        self.dc.text(
            (WIDTH - EDGE - self._width(tag, meta), 132),
            tag,
            font=meta,
            fill=HIGHLIGHT,
        )
        self.dc.line([(EDGE, 166), (WIDTH - EDGE, 166)], fill=FOREGROUND, width=3)
        self.dc.line([(EDGE, 172), (WIDTH - EDGE, 172)], fill=FOREGROUND, width=1)

    def lead_story(self):
        top = 190
        badge_face = self._font(SANS_BLACK_PATH, 16)
        label = "  TOP STORY  "
        badge_w = self._width(label, badge_face)
        self.dc.rectangle([EDGE, top, EDGE + badge_w, top + 27], fill=HIGHLIGHT)
        self.dc.text((EDGE, top + 3), label, font=badge_face, fill=CARD)
        kicker = self._font(SANS_BOLD_PATH, 17)
        self.dc.text(
            (EDGE + badge_w + 14, top + 4), "BUSINESS — TECH", font=kicker, fill=HIGHLIGHT
        )

        headline_face = self._font(SERIF_BOLD_PATH, 41)
        headline = "Anthropic's $81.3B IPO, biggest on record"
        rows = self._wrap(headline, headline_face, INNER - 205)
        after = self._block(rows, EDGE, top + 42, headline_face, FOREGROUND, 50)

        deck_face = self._font(SANS_PATH, 20)
        deck = (
            "Priced at $83 a share, the AI firm's stock jumps 17% on debut; "
            "a $1.5 trillion valuation."
        )
        deck_rows = self._wrap(deck, deck_face, INNER - 205)
        self._block(deck_rows, EDGE, after + 8, deck_face, MUTED, 28)

        # Rising market: ascending bars with a red arrow climbing over them.
        ox, oy = WIDTH - EDGE - 180, top + 48
        bars = [
            (0, 10, 26),
            (32, 22, 26),
            (64, 38, 26),
            (96, 52, 26),
            (128, 66, 26),
            (154, 78, 22),
        ]
        for dx, height, wd in bars:
            self.dc.rectangle(
                [ox + dx, oy + 106 - height, ox + dx + wd, oy + 106], fill=FOREGROUND
            )
        arrow = [
            (ox + 6, oy + 66),
            (ox + 44, oy + 54),
            (ox + 76, oy + 40),
            (ox + 108, oy + 26),
            (ox + 140, oy + 12),
            (ox + 172, oy - 2),
        ]
        self.dc.line(arrow, fill=HIGHLIGHT, width=5, joint="curve")
        self.dc.polygon(
            [(ox + 172, oy - 2), (ox + 150, oy - 4), (ox + 168, oy + 14)],
            fill=HIGHLIGHT,
        )
        self.dc.line([(ox, oy + 106), (ox + 180, oy + 106)], fill=FOREGROUND, width=3)
        self.dc.line([(EDGE, 388), (WIDTH - EDGE, 388)], fill=RULE, width=2)

    def story_grid(self):
        number_face = self._font(SERIF_BOLD_PATH, 29)
        kicker_face = self._font(SANS_BOLD_PATH, 14)
        headline_face = self._font(SERIF_BOLD_PATH, 24)
        deck_face = self._font(SANS_PATH, 18)
        column_w = (INNER - 26) // 2
        row_h = 176
        start_y = 408
        for pos, (num, section, headline, deck) in enumerate(ITEMS):
            col, row = pos % 2, pos // 2
            x = EDGE + col * (column_w + 26)
            y = start_y + row * row_h
            if row:
                self.dc.line(
                    [(EDGE, y - 11), (WIDTH - EDGE, y - 11)], fill=RULE, width=1
                )
            self.dc.text((x, y), num, font=number_face, fill=HIGHLIGHT)
            self.dc.text((x + 50, y + 8), section, font=kicker_face, fill=HIGHLIGHT)
            head_rows = self._wrap(headline, headline_face, column_w)
            below = self._block(head_rows, x, y + 42, headline_face, FOREGROUND, 29)
            deck_rows = self._wrap(deck, deck_face, column_w)
            self._block(deck_rows, x, below + 6, deck_face, MUTED, 23)

    def footer(self):
        fy = 962
        self.dc.line([(EDGE, fy), (WIDTH - EDGE, fy)], fill=FOREGROUND, width=2)
        foot = self._font(SANS_PATH, 14)
        left = "Sources: AP · BBC · NYT · The Hindu · NDTV · Al Jazeera"
        right = "All headlines verified from reporting on 20 November 2026"
        self.dc.text((EDGE, fy + 10), left, font=foot, fill=MUTED)
        self.dc.text(
            (WIDTH - EDGE - self._width(right, foot), fy + 10),
            right,
            font=foot,
            fill=MUTED,
        )

    def render(self):
        self.masthead()
        self.lead_story()
        self.story_grid()
        self.footer()
        return self.sheet


def draw_sheet():
    return FrontPage().render()


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
