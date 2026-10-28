# Tara Menu

Tara’s learning menu, duplicated from `ariamenu`, with independent Supabase data.

- Timeline: October 26, 2026 through January 5, 2027, with weekly Monday columns and the January 5 endpoint. Uses the existing teacher editor account.
- Timeline rows: Page 1–Page 13, followed by Torah Blessing · Before, Torah Blessing · After, Haftarah Blessing · Before, and Haftarah Blessing · After.
- Torah: Exodus 8:1–15, divided into aliyot 1–3, 4–5, 6–8, 9–11, 12–13, and 14–15. Includes cached Hebrew, trope and script controls.
- Service: all 13 PDF pages in order, beginning with “As I wrap myself in the talit…”. Each Page button corresponds to the PDF page with that number.
- English: Vaera, Exodus 6:2–9:35. Exodus 8:1–15 is transcribed from the supplied photos and highlighted yellow. Remaining text uses the matching JPS edition, checked against the photos; Sefaria fills cropped text. Footnotes are omitted.
- Homework and service recordings retain the original menu’s behavior and use Tara’s separate tables.
- Haftorah: Ezekiel 28:25–26 and 29:1, with trope and script controls.
- Elohai retains the original menu’s link. The Zoom link is removed.

## Run

Run `python -m http.server 8765` from this folder and open http://localhost:8765. Static files are served directly by GitHub Pages. Microphone recording requires localhost or HTTPS.

## Timeline build

```powershell
cd timeline-src
npm ci
npm run build
```

The build writes to `timeline/`, which is committed for GitHub Pages. Frontend dependencies are pinned in the lockfile.

## Data

`supabase/tara_setup.sql` records the applied schema setup. All Tara tables have RLS enabled. Progress is publicly readable and writable only by the existing teacher account. Homework follows the original shared-edit model. Individual recording access uses the original per-recording UUID capability model.

## Sources and verification

- [Original service PDF](https://drive.google.com/file/d/1qxrMtbRMuusya7_LPaZGc2fQ8aPCUNTS/view)
- [Vaera on Sefaria](https://www.sefaria.org/Exodus.6.2-9.35?lang=bi)
- English edition: *Tanakh: The Holy Scriptures*, JPS; Hebrew: Sefaria’s Masoretic text.
- Hebrew font licenses are included under `torah/fonts/`.
- `tools/customize.py` documents customization from the sibling `ariamenu`, `aria-torah`, and `bmtimelinear` source folders.
- `tools/verify.cjs` checks all service pages, the six aliyot, English highlighting, timeline bounds, and homework persistence in a browser. Install Playwright under `tools/` to run it; set `CHROME_PATH` if needed.
