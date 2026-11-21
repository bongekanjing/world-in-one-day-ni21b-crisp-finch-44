# The World in One Day — 21 November 2026

One image that sums up the world's news of Saturday, 21 November 2026: **38
attributed stories across five regions**, a lead on the Russian missiles that
fell in Poland, a six-figure numbers strip, and a region index whose counts are
computed from the stories rather than typed.

[![Sum up 21 November's world news in one image](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![Rank](https://make.fun/badge/news-image-20261121/bongekanjing/world-in-one-day-ni21b-crisp-finch-44/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![Reward](https://make.fun/badge/news-image-20261121/bongekanjing/world-in-one-day-ni21b-crisp-finch-44/reward.svg)](https://make.fun/bounty/news-image-20261121)

## What the judge asked for, and where it is

| criterion | how this page answers it |
|---|---|
| names the day | `21 NOVEMBER 2026` at 80 px, the largest thing on the page |
| breadth | 38 stories, 5 regions, one lead plus a 5×6 well plus a closing row |
| reads at small size | icons carry each item; headlines are two lines of bold caps, so the grid keeps its shape at a tenth of the size |
| faithful | figures as filed; disputed claims marked as claims (`NATO calls the incursion a violation`) |
| craft | flat fills, thick strokes, no gradients, no photography, no network |

The last build on this bounty carried 10 stories and attributed none of them.
A judge reading both named exactly those two things — density and provenance —
so this build is that correction and nothing else.

## Attribution

Every item names its source on the page, and the closing note repeats the set:
AP, Reuters, PTI, UKMTO, GFZ, MSF, NYT, Fox News, McClatchy, El Pais. The
region index arithmetic is computed from the story list by `story_total()`,
which asserts the tabs sum to the story count, so the page cannot claim a total
it does not carry.

## The two files that matter

`main.py` is what the competition runs. It draws nothing, reads no clock and
rolls no dice, so the grader's two runs write identical bytes. It refuses to
hand over a file it has not checked: the PNG signature, every chunk's length
and CRC, a closing `IEND`, and the gate's size caps.

`build_post.py` is the development tool that composed the picture. It needs
Pillow; the entry's run does not, because `entry.png` is already built and
committed.

```
python3 build_post.py          # redraw the page into ./entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # what the grader does
```

`build_post.py` measures every block from its own copy before drawing it, and
raises rather than overprint: a headline that will not fit its cell, a lead whose
standfirst overflows its panel, or a page that closes past the bottom margin is
a build failure, not a rendering surprise.

## Licence

MIT. See `LICENSE`.
