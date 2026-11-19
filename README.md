# The World Today — 19 November 2026

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
- **Fifteen more stories** in three columns — Voyager 1 crossing one
  light-day, India–Japan 2+2 talks in Tokyo, Russian oil refining down
  45%, Bitcoin, Asian markets, oil, the US House Democratic Caucus chair
  election, Spain's general strike, a drug seizure in Libya, a new
  Knesset speaker, the Women's Champions League, and more.
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
