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

## 3. Missing assets

| File | Referenced from | Status |
|---|---|---|
| `Allen_Bautista_Resume.pdf` | nav, hero, closing CTA, footer (4 links) | **Pending — author is exporting a fresh PDF.** Links are wired and will resolve the moment this file is dropped in the repo root. Until then these four links 404. Note `Allen_Bautista_Career_Resume.docx` was modified 2026-08-25, 19 days after `Allen_Bautista_Career_Resume.pdf` (2026-08-06) — export from the `.docx` to avoid shipping a stale résumé. |
| `Grammys_Campaign_Deck.pdf` | Grammys campaign card | **Not on disk anywhere.** The link block is commented out in `index.html` (markup preserved, not deleted). Restore it once the file is added to the repo root. |

## 4. Supply-Chain Contagion — no repository link, deliberately

`supply-chain-contagion/` has no `.git` directory, so there is no remote to cite. The
card therefore ships with **no GitHub link** rather than a guessed URL. Add one only
after the repo exists and the remote is read from `.git/config`.
