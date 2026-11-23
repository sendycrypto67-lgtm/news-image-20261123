[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/sendycrypto67-lgtm/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/sendycrypto67-lgtm/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
# The World Today: Monday 23 November 2026

A one-image newspaper front page summing up the world news of Monday
23 November 2026, built for the make.fun bounty
[news-image-20261123](https://make.fun/bounty/news-image-20261123)
("Sum up 23 November's world news in one image").

The image is a cream broadsheet page, masthead **THE WORLD TODAY**,
dated **MONDAY 23 NOVEMBER 2026**, with six stories in a 3 by 2 grid.
Each story has a flat editorial illustration, a red topic tag, a bold
headline and a one-line sub-caption. The six stories were verified
against real reporting from 20-23 November 2026 (AP, Reuters, CNN,
WSJ, Le Monde, UKMTO, IANS, Korea JoongAng Daily). No casualty
figures appear anywhere in the image, and no unverified claim is
presented as fact.

## The six stories

1. **CLIMATE TALKS COLLAPSE IN ANTALYA** (Climate) - COP31 in
   Antalya ends with no deal, the longest COP ever, after the EU and
   its allies reject the Antalya Pact, which mentions no fossil
   fuels; the first failed COP since COP15 in 2009.
2. **TANKERS HIT OFF OMAN** (Hormuz) - Two tankers are struck by
   unknown projectiles in the Strait of Hormuz near Khasab, Oman,
   one at the stern and one in the engine room; no casualties are
   reported. Claims about mines are unverified and not stated.
3. **RUSSIAN MISSILES LAND IN POLAND** (Poland) - Two missiles and a
   jet drone come down in south-eastern Poland during a barrage on
   Ukraine, near Nowy Lipowiec, with no casualties; Poland calls it
   a deliberate provocation and NATO meets in Brussels today.
4. **MINISTER QUITS OVER AI EXAM CHEATING** (Korea) - Education
   Minister Choi Kyo-jin resigns after last-minute anti-cheating
   changes sow confusion ahead of the CSAT; the trigger was a
   top exam scorer admitting to cheating with a mini camera and AI.
5. **NEPAL PM MEETS MODI IN DELHI** (India) - Nepal's Prime
   Minister Balendra Shah holds his first foreign bilateral talks
   since taking office in March 2026, with energy and trade on the
   agenda, during a state visit on 22-23 November.
6. **LISBON MARCHES OVER LIVING COSTS** (Lisbon) - Thousands march
   in the rain through Lisbon, called by the CGTP union, demanding
   higher wages and pensions, controlled prices and affordable
   housing.

## How main.py works

`main.py` is Python 3, standard library only. It finds `entry.png`
next to itself and validates it: PNG magic bytes, an IHDR chunk of
length 13 with non-zero dimensions of at most 1024 on each side, a
valid bit depth and colour type, a file size of at most 1048576
bytes, and a well-formed IEND chunk at the end of the file. It then
copies the file byte for byte to `$MAKEFUN_OUTPUT_DIR` (or `/output`
when unset), re-reads the copy, and asserts that the copy's sha256,
size and dimensions equal the source's. On success it prints the
source path, dimensions, byte size, sha256 and destination; on
failure it exits 1 with an error naming the file. No network, no
randomness, so both runs write identical bytes.

## How to run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `entry.png` - the front page image, 1024x1024, 606966 bytes,
  sha256 `8b1d4996417598fd8047c6e1d67578ce0ab38e640ffb0a28412762f9709e9a21`
- `main.py` - validator and copier described above
- `README.md` - this file
- `LICENSE` - MIT license
- `BUILD_LOG.md` - research, generation and test notes

Referral: https://make.fun/r/y8skhesk
