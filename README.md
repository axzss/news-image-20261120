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
too — it copies the same bundled bytes.

## Bounty

Built for the make.fun bounty: https://make.fun/bounty/news-image-20261120

Optional: earn referral rewards, a second way to make money — join
make.fun with referral code `1409h78a`: https://make.fun/r/1409h78a
