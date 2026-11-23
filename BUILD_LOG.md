# Build log: news-image-20261123

## The six stories (verified by the coordinator against AP, Reuters, CNN, WSJ, Le Monde, UKMTO, IANS, Korea JoongAng Daily, 20-23 Nov 2026)

1. COP31 climate talks collapse in Antalya on Sunday 22 Nov; the EU,
   UK, Panama, the Marshall Islands and Norway reject the Antalya
   Pact, which mentions no fossil fuels. Longest COP ever, first
   failed COP since COP15 in 2009.
2. Two tankers struck by unknown projectiles in the Strait of Hormuz
   near Khasab, Oman, on Saturday (UKMTO): one at the stern, one in
   the engine room; no casualties reported. Unverified claims about
   mines are not stated as fact.
3. Two missiles and a jet drone come down in south-eastern Poland
   on 20 Nov during a barrage on Ukraine (Kh-101 near Nowy
   Lipowiec), no casualties; Poland calls it a deliberate
   provocation; NATO meets in emergency session in Brussels today,
   Monday 23 Nov.
4. Education Minister Choi Kyo-jin resigns on Sunday, accepted by
   President Lee Jae Myung within the hour, after last-minute
   anti-cheating changes sow confusion ahead of the CSAT; the
   trigger was a top accounting-exam scorer admitting to cheating
   with a mini camera and AI.
5. Nepal PM Balendra Shah makes a state visit to India on 22-23
   Nov, his first trip abroad since taking office in March 2026;
   delegation talks with PM Modi and a joint press conference on
   Monday 23 Nov, energy and trade on the agenda.
6. Thousands march in the rain in Lisbon on Saturday 21 Nov, called
   by the CGTP union, demanding higher wages and pensions,
   controlled prices and affordable housing.

No casualty figures appear anywhere in the image. No speculation is
presented as fact.

## Generation notes

- Six fresh flat editorial illustrations were generated with the
  media image tool, each prompted with NO text, NO words, NO letters,
  NO numbers. Each was read back visually before composing.
- The entry was composed with Python + Pillow in a build-time script
  kept in /tmp/ni23/compose.py (not in the repo): cream page, serif
  masthead "THE WORLD TODAY", date line "MONDAY 23 NOVEMBER 2026",
  double rule, one-line deck, 3 by 2 grid of panels (illustration,
  red tag, bold headline, sub-caption directly under the headline),
  footer line with sources. Headlines and captions use adaptive font
  sizing (shrink until they fit, wrap to at most 3 lines) so nothing
  overflows or is cut off.

## Self-review defects found and fixed

- Defect 1 (factual, illustration): the first India illustration
  showed two identical Indian flags behind the handshake. Fixed by
  regenerating with the Nepal flag (crimson double-pennon with sun
  and moon) on the left and the Indian tricolour on the right; the
  new image was read back visually and is correct.
- Defect 2 (layout, checked): the Korea headline wraps to 3 lines
  while the others take 2. Verified it still fits inside its panel
  with even whitespace below; no change needed.
- After the fixes, the final read-back confirmed: every headline and
  sub-caption spelled exactly, nothing garbled or cut off, nothing
  overflows its panel, every illustration matches its story, the
  date, deck and footer are correct, and there are no large empty
  gaps (only even newspaper whitespace at panel bottoms).

## main.py

Python 3, standard library only, written fresh in this session. It
validates entry.png (PNG magic bytes, IHDR length 13 with non-zero
dimensions at most 1024 per side, valid bit depth and colour type,
file at most 1048576 bytes, well-formed IEND chunk at the end),
copies it to $MAKEFUN_OUTPUT_DIR (or /output), then re-reads the
copy and asserts sha256, size and dimensions equal the source.
Prints source path, dimensions, byte size, sha256 and destination;
exits 1 naming the file on failure.

## Test results

- `python3 -m py_compile main.py`: pass.
- `MAKEFUN_OUTPUT_DIR=/tmp/ni23/out1 python3 main.py`: pass,
  1024x1024, 606966 bytes,
  sha256 8b1d4996417598fd8047c6e1d67578ce0ab38e640ffb0a28412762f9709e9a21.
- `MAKEFUN_OUTPUT_DIR=/tmp/ni23/out2 python3 main.py`: pass,
  identical sha256 matching the source.
- Negative test, non-PNG file as entry.png: rejected, exit 1,
  "is not a PNG file (bad magic bytes)".
- Negative test, 1200x1200 PNG as entry.png: rejected, exit 1,
  "is 1200x1200, over the 1024x1024 limit".
- Original entry.png restored after the negative tests, sha256
  re-verified identical.

## Final entry

- entry.png: 1024x1024, 606966 bytes,
  sha256 8b1d4996417598fd8047c6e1d67578ce0ab38e640ffb0a28412762f9709e9a21
- Referral code used: y8skhesk (https://make.fun/r/y8skhesk).

- Coordinator revision: IEND CRC32 is now verified too (in addition to the IEND length/type position check).
