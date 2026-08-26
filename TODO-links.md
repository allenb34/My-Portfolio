# Link state of truth

> **A URL being correct and a URL being publicly reachable are different properties.**
> Earlier verification confirmed only the first. Every entry here was checked
> anonymously, using a real browser User-Agent, redirects followed, the *final* URL judged,
> and no git credentials in play, because cached credentials are what made
> `madden-2k-forecaster` look public when it was private.

Regenerate this table with:

```bash
python verify_links.py
```

It exits non-zero if anything fails, so it can gate a deploy. Run it against the live
site with `python verify_links.py --base https://allenb34.github.io/My-Portfolio/`.

Last full pass: **2026-08-26, all 18 checks passed.**

---

## External links

| URL | Type | Anonymous status | Final URL | Verified how | Date |
|---|---|---|---|---|---|
| `nfl-signing-roi-analyzer.streamlit.app` | deployment | **200** (303→200) | app root | anonymous GET, browser UA, cookie jar; lands on the app | 2026-08-26 |
| `github.com/allenb34/nfl-signing-roi-analyzer` | repo | **200** | same | remote read from `nfl_signing_roi/.git/config` | 2026-08-26 |
| `seahawks-homefield-analytics.streamlit.app/12th_Man_Value` | deployment | **200** (303→200) | app root | anonymous GET; page path resolves | 2026-08-26 |
| `github.com/allenb34/seahawks-homefield-analytics` | repo | **200** | same | remote read from `seahawks-sql-analytics/.git/config` | 2026-08-26 |
| `madden-2k-forecaster.streamlit.app` | deployment | **200** (303→200) | app root | anonymous GET; made public by author | 2026-08-26 |
| `github.com/allenb34/madden-2k-forecaster` | repo | **200** | same | remote from `sports-price-forecaster/.git/config`; **folder name ≠ repo name**; was private until 2026-08-26 | 2026-08-26 |
| `fab-pressure-atlas.lovable.app/` | deployment | **200** | same | anonymous GET | 2026-08-26 |
| `github.com/allenb34/fab-pressure-atlas` | repo | **200** | same | no local clone; repo existed but was private until 2026-08-26 | 2026-08-26 |
| `path-water-mazezip--allenb34.replit.app/` | deployment | **200** | same | anonymous GET | 2026-08-26 |
| `github.com/allenb34/path-water-maze` | repo | **200** | same | local `.git` has **no remote**; confirmed by anonymous fetch, not inferred | 2026-08-26 |
| `social-proof-badge-readout-we8mad64gry9vbs3ajslyr.streamlit.app/` | deployment | **200** (303→200) | app root | anonymous GET; author-confirmed URL | 2026-08-26 |
| `github.com/allenb34/social-proof-badge-readout` | repo | **200** | same | remote read from `social-proof-badge-readout/.git/config` | 2026-08-26 |
| `github.com/allenb34/console-economics` | repo | **200** | same | published 2026-08-26 from local folder that had no `.git`; README renders | 2026-08-26 |
| `github.com/allenb34/costco-comp-ledger` | repo | **200** | same | remote read from `costco-comp-ledger/.git/config` | 2026-08-26 |
| `linkedin.com/in/allen-bautista-279778323/` | profile | **200** | same | anonymous GET | 2026-08-26 |
| `github.com/allenb34` | profile | **200** | same | anonymous GET | 2026-08-26 |

## Relative assets

| File | Type | Status | Verified how | Date |
|---|---|---|---|---|
| `Allen_Bautista_Resume.pdf` | asset | **present**, 117,621 bytes | author's source re-export, phone number removed at source; 1 page, text extracted and checked | 2026-08-26 |
| `DiD_Dividend_Study.xlsx` | asset | **present**, 1,438,724 bytes | SHA256 identical to source; opens as a valid 36-member workbook | 2026-08-26 |

---

## Known gaps, deliberate

**`Grammys_Campaign_Deck.pdf` not shipped.** The supplied file is the course
worksheet with its template scaffolding intact: "delete the options that you do not
choose" with all four options still listed, "read the instructions on the previous
slide", two slides headed "LevelUp (Extra Credit)", and a filename of "Copy of Copy of
Grammys Social Media Project.pptx". Every figure on the Grammys card was checked against
it and is correct: $150,000 budget, 1,800,000 impressions, CPA $30 vs $15 benchmark,
CTR 0.25% vs 2% (−87.5%), CPC $2.00 at benchmark, 400% traffic lift against 2.3%
conversion. The card therefore stands on its own; only the deck button is withheld. The
anchor is commented out in `index.html` with a restore note. Restore it if a cleaned
deck is produced.

**Supply-Chain Contagion: no repository link, by design.** `supply-chain-contagion/`
has no `.git`, so there is no remote to cite and the card ships with no GitHub button
rather than a guessed URL. Add one only after the repo exists and the remote is read
from `.git/config`.

---

## Two failure modes this file exists to prevent

1. **Cached git credentials.** `git ls-remote` succeeds against a private repo when the
   caller is authenticated. It is not evidence of public reachability. `madden-2k-forecaster`
   and `fab-pressure-atlas` both passed that check while returning 404 to everyone else.

2. **Judging the first hop.** Streamlit routes even public apps through a
   `share.streamlit.io/-/auth` handshake that sets a session cookie before returning to
   the app. A checker without a cookie jar never completes that chain and reports a
   public app as a sign-in wall. `verify_links.py` carries a per-URL cookie jar and
   judges only where the chain comes to rest.
