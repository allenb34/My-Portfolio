# TODO — unverified links & missing assets

Everything below is either **live on the site but not independently verified**, or
**referenced by the site but missing from the repo**. Nothing here should be treated
as confirmed until the "How to verify" step is completed.

Rule in force for this repo: **never invent a URL.** GitHub URLs are taken only from a
project folder's `.git/config` `[remote "origin"]`; deployment URLs only from a repo's
README or an explicit statement from the author.

---

## 1. Unverified deployment URLs (live on the site)

These are currently linked from project cards. They were inherited from the previous
version of the site and could not be confirmed against any repo file.

| URL | Card | Why it is unverified | How to verify |
|---|---|---|---|
| `https://nfl-signing-roi-analyzer.streamlit.app` | NFL Marquee Player Signing ROI Analyzer | Appears in no file in `nfl_signing_roi/`. README records no deployment URL. | Open the Streamlit Cloud dashboard and copy the real app URL, or confirm the app is not deployed and remove the "Live app" link. |
| `https://madden-2k-forecaster.streamlit.app` | Sports Price Forecaster | README confirms a deployment exists but records no URL. Folder is `sports-price-forecaster/`, repo is `madden-2k-forecaster`. | Same — read the true URL off Streamlit Cloud. |
| `https://fab-pressure-atlas.lovable.app/` | FabPressure Risk Atlas | No local repo exists for this project, so nothing on disk corroborates it. | Confirm from the Lovable dashboard. |

## 2. Unverified GitHub URLs (live on the site)

| URL | Card | Why it is unverified | How to verify |
|---|---|---|---|
| `https://github.com/allenb34/fab-pressure-atlas` | FabPressure Risk Atlas | No local repo — no `.git/config` to read. | `git ls-remote <url>` should exit 0, or check github.com/allenb34?tab=repositories. |
| `https://github.com/allenb34/console-economics` | Console Economics | `console-economics/` has no `.git` directory at all. | Same. |
| `https://github.com/allenb34/path-water-maze` | Path: Water. | `path-water-maze/.git` exists but has **no remote configured**. | Add the remote locally, or read the true repo name off GitHub. |

Quick check for all six at once:

```bash
for u in nfl-signing-roi-analyzer.streamlit.app madden-2k-forecaster.streamlit.app fab-pressure-atlas.lovable.app; do echo "== $u"; curl -sSI "https://$u" | head -1; done
for r in fab-pressure-atlas console-economics path-water-maze; do echo "== $r"; git ls-remote "https://github.com/allenb34/$r" >/dev/null 2>&1 && echo OK || echo "404 / no access"; done
```

## 3. Assets

| File | Referenced from | Status |
|---|---|---|
| `Allen_Bautista_Resume.pdf` | nav, hero, closing CTA, footer (4 links) | **Shipped 2026-08-26.** Author-supplied export with the personal phone number removed from the contact line (116,159 bytes, single page). All four links return 200. **Open item — see below.** |
| `Grammys_Campaign_Deck.pdf` | Grammys campaign card | **Not on disk anywhere.** The link block is commented out in `index.html` (markup preserved, not deleted). Restore it once the file is added to the repo root. |

## 4. Supply-Chain Contagion — no repository link, deliberately

`supply-chain-contagion/` has no `.git` directory, so there is no remote to cite. The
card therefore ships with **no GitHub link** rather than a guessed URL. Add one only
after the repo exists and the remote is read from `.git/config`.

## 5. Résumé source document — phone number will come back

The phone number was removed by editing the **PDF** directly, because the only
`.docx` in the projects folder (`Allen_Bautista_Career_Resume.docx`) is an older draft
— it has no Costco entry, no supply-chain entry and no summary section, so re-exporting
from it would have regressed the résumé.

That means **the real source document still contains `(425) 622-3131`**. The next export
from it will reintroduce the number to the site. Remove it at the source, then either
re-export over `Allen_Bautista_Resume.pdf` or re-run the same edit.

Check any future replacement before committing it:

```bash
python -c "import pymupdf,sys; t=pymupdf.open(sys.argv[1])[0].get_text(); print('phone present:', any(x in t for x in ['622-3131','(425)']))" Allen_Bautista_Resume.pdf
```
