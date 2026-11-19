# The World Today — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/nemesisbug/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/nemesisbug/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for [make.fun's "Sum up 19 November's world news in one image"](https://make.fun/bounty/news-image-20261119) bounty ($250 in USDC, top 50 paid).

A one-page newspaper front page that sums up the world's news of
**Thursday 19 November 2026** in a single image. Every story on the page
happened, or was first reported, on that day.

## What the image shows

- **Masthead** — the paper's name and the date, front and centre.
- **Lead story** — Grand Theft Auto VI begins its worldwide rollout after
  13 years: a 99 on Metacritic, tying the site's all-time high, with
  pre-sales estimated at $1.65 billion.
- **The day around the world** — a lon/lat world map with six numbered pins
  for the other lead stories: Anthropic's Nasdaq debut as ANT, the
  International Court of Justice delivering its Myanmar judgment in The
  Hague, the first-ever Trump–Xi–Putin trilateral in Shenzhen, Cyclone
  Akvan bearing down on India's east coast, and the Coalition of the
  Willing meeting in Berlin.
- **Twelve more stories** in three columns — Voyager 1's confirmation a
  light-day out, India–Japan 2+2 talks in Tokyo, Bitcoin, the Nikkei's
  open, oil, South Korea's exam-day market delay, the Women's Champions
  League, Ondo's Anthropic tracker, cricket in Nepal and Abu Dhabi, and
  two more from launch day itself.
- **By the numbers** — the day's figures at a glance, and a sources line.

## How it is made

`build_image.py` draws the whole page with Pillow (deterministic — the
same bytes on every run) from the story list in the same file. `main.ts`
(Node 22, standard library only) copies the resulting `entry.png` to
`$MAKEFUN_OUTPUT_DIR` (default `/output`). No network is used at run time.

```sh
python3 build_image.py   # writes entry.png (1024x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources

Reuters, AP, BBC, Nasdaq, India Meteorological Department, NASA, Sensor
Tower, CNBC, The Hindu.

## Licence

MIT — see `LICENSE`.

## Referral

https://make.fun/?ref=w642jqgx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119
