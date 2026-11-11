# lorenzmaierhofer.com

Personal website of Lorenz Maierhofer, Senior Director and Global Lead for Decision Engine, AI Factory, Agentic AI Products & AI Governance at Procter & Gamble.

Live at **[lorenzmaierhofer.com](https://lorenzmaierhofer.com)**. Static HTML/CSS/JS, no build step, hosted on GitHub Pages.

## What's in here

| Path | What it is |
|------|------------|
| `index.html`, `news.html`, `projects.html` | Main site (English) |
| `de/`, `zh/` | German and Simplified Chinese versions of the main site |
| `styles.css`, `script.js` | Shared styling and behaviour for all main-site pages |
| `grimasso/` | Landing page for the Grimasso tongue-training app (EN, DE, FR, ZH) |
| `offgridmedia/` | Landing, privacy and age-rating pages for the Offgrid Media iOS app (10 locales, generated) |
| `linkedin_posts.json` | LinkedIn posts embedded on the news page |
| `pg_ai_news.json`, `news.xml` | P&G AI News feed data and its RSS feed |
| `llms.txt`, `robots.txt`, `sitemap.xml` | Crawler and agent metadata |
| `.github/workflows/` | Deploy (`static.yml`) and weekly news update (`pg-ai-news.yml`) |
| `.github/scripts/` | P&G AI News fetcher, RSS generator and self-check |

## Run locally

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>. A local server is needed (not `file://`) because the news page fetches JSON.

## Deploy

Every push to `main` deploys to GitHub Pages via `.github/workflows/static.yml`. The custom domain is configured in the repository's Pages settings.

## P&G AI News

`news.html` shows verbatim excerpts about AI from official P&G sources (P&G blog, SEC filings, earnings calls). A scheduled workflow runs every Monday (with a Thursday catch-up):

1. `.github/scripts/pg_ai_news.py` fetches new pages from the sources in `.github/pg_ai_sources.json`.
2. Gemini decides whether AI is a core message and picks passages. It never writes text: every excerpt must match the source page word for word, and each card links to the original.
3. `.github/scripts/news_feed.py` regenerates `news.xml`.
4. The workflow commits, redeploys and opens a GitHub issue listing what was published.

Needs repo secret `GEMINI_API_KEY` and repo variable `SEC_USER_AGENT`.

```bash
python3 .github/scripts/test_pg_ai_news.py                  # self-check
python3 .github/scripts/pg_ai_news.py --manual items.json   # add items by hand: {url: [excerpt, ...]}
python3 .github/scripts/news_feed.py                        # rebuild news.xml after editing the JSON
```

## Offgrid Media pages

The 30 HTML files under `offgridmedia/` are generated. Edit `offgridmedia/_build/` and regenerate:

```bash
cd offgridmedia/_build
python3 build.py        # all pages
python3 build.py age    # age-rating pages only
./make_assets.sh        # images and preview video (needs magick + ffmpeg)
```

The generator reads app copy from the sibling app repo (`../share_to_save/`), which must be checked out next to this one.

## Conventions

- Change content in every language version of a page.
- German uses real umlauts (ä, ö, ü). Chinese uses Simplified characters and the formal 您 for parents.
- Every page carries a canonical URL and hreflang tags. `x-default` points to English.
- `/offgridmedia/` and `/offgridmedia/privacy` are referenced by the shipped app and must not move.

See [`CLAUDE.md`](CLAUDE.md) for detailed notes on design, SEO and each subsite.

## License

© Lorenz Maierhofer. All rights reserved. Content, images and branding may not be reused without permission.
