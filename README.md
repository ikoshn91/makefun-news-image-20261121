# makefun-news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/ikoshn91/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/ikoshn91/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-page atlas dashboard summing up Saturday 21 November 2026's
world news, for make.fun's "Sum up 21 November's world news in one
image" bounty ($100 in USDC, 50 places paid).

## The image

`entry.png` (1024×1024) is "THE WORLD TODAY — Saturday 21 November
2026": three lead stories (Iran strikes Bahrain, COP31 overtime in
Antalya, the M6.7 Peru quake) over eight colour-coded region panels
holding 27 more dated stories — 30 stories in 8 regions — plus an
"Also today" ticker. It is drawn programmatically with Python
Pillow (`gen_image.py`), so every word is pixel-perfect text — no AI
image generation, no downloaded pictures.

- **Lead — Iran/Bahrain:** the IRGC claims hits on two US bases;
  Bahrain reports a civilian industrial site ablaze, no one hurt.
- **Lead — COP31:** talks run into overtime in Antalya; the draft
  drops the fossil-fuel phase-out and ~200 nations are deadlocked.
- **Lead — Peru:** M6.7 quake, 108 km deep near Junín, at 00:09 UTC;
  felt in Lima; 152 homes uninhabitable, no deaths reported.
- **Regions:** Middle East, Europe, Asia, Americas, Markets & Tech,
  Science & Health, Africa, Sport — from the Kryvyi Rih triple-tap
  and the Sparta II fire to the Wolbachia dengue result and Harden's
  51 points passing Kobe.

Sources: CNN, Reuters, AP, WSJ and same-day roundups — reports
published 21 November 2026.

## The program

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`. No network, no randomness: two runs write the
same bytes. Regenerate the image with `python3 gen_image.py` (needs
Pillow); verify determinism with `sha256sum` across two runs.

## License

MIT — see LICENSE.
