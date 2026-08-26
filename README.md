# allenb34.github.io

Allen Bautista's analytics portfolio: a single static page served by GitHub Pages.

## Structure

```
index.html                 the entire site: markup, CSS, and JS inline
DiD_Dividend_Study.xlsx    downloadable workbook linked from the DiD card
.nojekyll                  tells GitHub Pages to serve files as-is, no Jekyll build
TODO-links.md              unverified URLs and missing assets, read before deploying
```

No build step, no bundler, no framework, no dependencies beyond the Google Fonts
stylesheet. Edit `index.html` directly.

## Local preview

```bash
python -m http.server 8080
```

Then open http://localhost:8080. Serving over HTTP matters: the scroll-reveal
animation starts every card at `opacity: 0` and relies on an IntersectionObserver,
so the page is intentionally blank until that script runs.

## Conventions

- **Never invent a URL.** GitHub links come from a project folder's `.git/config`
  `[remote "origin"]`; deployment links come from a repo README or the author.
  Anything unconfirmed goes in `TODO-links.md`, not into the page as a live link.
- **Do not strengthen the project copy.** Several cards report null or exploratory
  results on purpose: n=24 for FabPressure, p=0.86 for the DiD study, p≈0.21 for
  Console Economics, 65.0% held-out for Supply-Chain Contagion, 0 months scored for
  the Costco ledger. The restraint is deliberate.
- Category accent colors are set per-section with `style="--c:var(--<domain>)"`.

## Deploy

Push to `main`, then **Settings → Pages → Source: `main` / root**.
