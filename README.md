# Wednesday 25 November 2026 — The World in One Page

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/bangfadli121-arch/news-image-20261125-entry/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/bangfadli121-arch/news-image-20261125-entry/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-page newspaper front page that sums up the world's news of
**Wednesday 25 November 2026** in a single 1024×1024 image.

## What is on the page

- **Full-width hero** — Pakistan's first astronaut, Muhammad Zeeshan Ali,
  launches aboard China's Shenzhou-24 to the Tiangong space station: the
  first Pakistani in orbit and the first foreign astronaut on Tiangong.
- **Three secondary stories** — Kyiv confirms a drone strike on a Russian
  cargo ship in the Gulf of Finland; the AI sell-off (Nvidia -6%, Micron
  -11%, Nasdaq -1.5%) as a Trump tariff-hike plan is reported; Hamas
  internal-security chief Naeem Abu Nahel is killed in a Gaza airstrike.
- **Six big numbers** — -6% Nvidia, -11% Micron, 11 wounded in Riyadh,
  13 killed in a UAE crash, 6,500 Rohingya returns, 570,000 AIDS deaths
  in 2025 (the lowest in 20+ years).
- **Ten small cards** with mini illustrations — Riyadh tower hit, Huawei
  found guilty, a CIA breach, tankers mined in Hormuz, Hasina to return,
  Rohingya returns, a Nepal quake, Giuliani honoured, a China probe,
  NATO to Poland.
- **Where it happened** — a structured table of the places in today's news.
- **Also on Wednesday** — 21 more stories, numbered, for a total of 35.
- **Date check** — the COP31 collapse and the Nvidia +31% surge were
  Monday's news, not today's, so they are deliberately left out.

Every story happened, or was first reported, on Wednesday 25 November 2026.
All drawings are original, drawn procedurally with Pillow. No photos.

## How it runs

`draw.py` draws `entry.png` at build time (Pillow, 4x supersampling
downscaled with LANCZOS for smooth HD edges). `main.py` is the
entrypoint: it copies `entry.png` to `/output/entry.png`. Standard library only, no network,
so two runs write byte-identical output.

```sh
python3 draw.py            # redraw entry.png
python3 main.py            # writes /output/entry.png
```

## Sources

Reuters and AP digests dated 25 November 2026.
Attributions are printed on the page itself.
