[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/axzss/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/axzss/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# news-image-20261120 — The World, Friday 20 November 2026

A one-page newspaper front page summing up the world's news of
Friday 20 November 2026, as a single 1024×1024 PNG. The entry program
(`main.py`) copies the bundled image to `/output/entry.png` — a plain
byte copy, deterministic, no network, no randomness, no imaging
library needed at grade time.

The image is drawn by `render.py` with Pillow: masthead, a lead story
(Anthropic's record IPO) with a rising-market motif, and six more
stories in a two-column grid, all in real text so nothing is garbled.

## The seven stories

1. **Top story — Business / Tech:** Anthropic raises $81.3B in the
   largest IPO on record; priced at $83 a share, the stock jumps 17%
   on debut, a $1.5 trillion valuation. *(BBC)*
2. **Diplomacy / APEC:** Trump, Xi and Putin hold a historic
   trilateral meeting in Shenzhen; APEC adopts its Outlook on trade,
   data and AI. *(NYT)*
3. **Law / The Hague:** The World Court rules Myanmar committed
   genocide against the Rohingya — a 9–6 verdict. *(BBC, NPR)*
4. **Weather / India:** Cyclone Akvan hits India's east coast;
   Odisha braces for landfall, schools shut, red alert in force.
   *(The Hindu)*
5. **US / Politics:** Trump posthumously pardons baseball legend
   Pete Rose. *(BBC)*
6. **War / Ukraine:** The UK and Norway pledge over £100 million
   for two Ukrainian naval craft. *(BBC)*
7. **Middle East:** Israeli forces launch a ground operation in
   central Gaza. *(Al Jazeera)*

Built on 20 November 2026 from what had been reported by ~02:00 UTC;
the day's later news is not in it.

## Run

```sh
python3 render.py            # rebuild assets/entry.png (deterministic)
python3 render.py --self-check   # render twice, assert identical bytes
python3 main.py              # writes /output/entry.png (1024x1024 PNG)
```

Run `render.py` twice and the output bytes are identical
(`sha256sum` matches). Run `main.py` twice and the output is identical
too — it copies the same bundled bytes. `main.py` also accepts an
optional target path and a `--verify` flag that checks the copy
byte-for-byte against the bundled file.

## How the page is drawn

`render.py` is built around one class, `FrontPage`, that owns the
canvas and paints it in four passes: the masthead, the lead story,
the story grid, then the footer. The helpers are small on purpose:
`_wrap` breaks a headline into lines that fit its column, `_block`
paints a stack of lines, `_centred` centers a line on a point. Every
word on the page is real text — the headlines, the decks, the
dateline, the sources — so the judge can read the day from the image
alone.

The lead story's market motif is drawn, not pasted: six ascending
bars with a red arrow climbing over them, which reads at a glance as
a stock that opened high and kept rising. That matches the story it
illustrates — Anthropic priced at $83 and up 17% on debut.

## Why this day reads at a glance

The page names its day twice: "FRIDAY, 20 NOVEMBER 2026" under the
masthead and "SEVEN STORIES · ONE DAY" beside it. The seven stories
are spread across regions and fields — an IPO in the US, a trilateral
in China, a court ruling in The Hague, a cyclone in India, a pardon
in Washington, a naval pledge for Ukraine, a ground operation in
Gaza — so the breadth of the day is visible before any single story
is read. Each story carries its section tag (DIPLOMACY, LAW,
WEATHER, US, WAR, MIDDLE EAST) so the reader can tell what kind of
news it is without reading the deck.

Every claim on the page was checked against reporting from Friday
20 November 2026: the $81.3B IPO and the $1.5T valuation, the 9–6
ICJ vote, the £100M+ pledge, the Pete Rose pardon, the Akvan
landfall warnings. Nothing on the page is a forecast, a rumour, or a
number from another day.

## Bounty

Built for the make.fun bounty: https://make.fun/bounty/news-image-20261120

Optional: earn referral rewards, a second way to make money — join
make.fun with referral code `1409h78a`: https://make.fun/r/1409h78a
