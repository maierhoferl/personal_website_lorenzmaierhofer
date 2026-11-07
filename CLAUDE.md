# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal website for Lorenz Maierhofer, Senior Director and Global Lead for AI Factory, Agentic AI Products & AI Governance at Procter & Gamble. Static site hosted on GitHub Pages at lorenzmaierhofer.com.

## Architecture

**Static HTML/CSS/JS site with multilingual support (English/German/French/Chinese)**

- Root level: English pages (`index.html`, `news.html`, `projects.html`)
- `/de/` folder: German pages (same structure)
- `/grimasso/` folder: Quadrilingual Grimasso app subsite (EN, DE `/de/`, FR `/fr/`, ZH `/zh/`)
- `/offgridmedia/` folder: 10-locale Offgrid Media app subsite — see below
- Single shared `styles.css` and `script.js` (German/French pages reference via `../`)
- `grimasso/grimasso-styles.css` and `grimasso/grimasso-script.js` for Grimasso branding
- `linkedin_posts.json`: Configuration for dynamically loaded LinkedIn post embeds

**SEO Implementation**
- Canonical URLs and hreflang tags on all pages for proper multilingual indexing
- x-default points to English version
- Structured data (JSON-LD) for Person schema

**Key Design Elements**
- Cyberpunk aesthetic with P&G brand color (#003DA5)
- Dark/light theme toggle (localStorage persisted)
- CSS variables for theming in `:root` and `[data-theme="light"]`
- Scroll animations via Intersection Observer
- AI particle explosion effect on profile image click

## Deployment

Automatically deploys to GitHub Pages on push to `main` branch via `.github/workflows/static.yml`.

## Development

No build step required. Open HTML files directly in browser or use a local server:
```bash
python3 -m http.server 8000
```

Local server needed for `linkedin_posts.json` fetch to work (CORS).

## Grimasso Subsite

**Quadrilingual Tongue-Training App Landing Page** (EN, DE, FR, ZH)

**Structure**
- `/grimasso/index.html` - English landing page
- `/grimasso/de/index.html` - German landing page
- `/grimasso/fr/index.html` - French landing page
- `/grimasso/zh/index.html` - Chinese (Simplified) landing page
- `/grimasso/grimasso-styles.css` - Custom styling (kid-friendly, bright palette #33C759 primary)
- `/grimasso/grimasso-script.js` - Interactive features (animations, confetti, count-ups)
- `/grimasso/Grimasso_Welcome.mov` - Hero video (with image fallback)

**Key Features**
- Playful, kid-friendly aesthetic with bright green primary color (#33C759)
- Animated hero with floating bubbles, decorative emojis, wavy SVG dividers
- 100 scientifically-designed exercises across 5 categories
- Gamification elements: 20 levels, 29 achievement badges, streak tracking
- Comprehensive app features section (12 features with emoji icons)
- "By the Numbers" statistics section with count-up animations
- Parent-focused benefits messaging
- Confetti burst animations on CTA clicks
- Card tilt/3D hover effects with bounce scroll animations
- Scroll progress indicator bar
- Accessibility: respects prefers-reduced-motion

**Chinese (ZH) Cultural Adaptation**
- `<body class="zh">` enables CSS overrides scoped to `.zh` in `grimasso-styles.css`
- Red/gold color palette: CTA buttons #E53935 (Chinese red), hover #FFD700 (gold), gold stat numbers and hero text
- Chinese font stack: `'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei'` with 1.8 line-height
- Noto Sans SC loaded from Google Fonts in the ZH page `<head>`
- Chinese App Store link (`/cn/`), CNY currency in JSON-LD
- Content tone: 您 (formal) for parents, 你 (casual) for kids
- Key terminology: 口腔肌肉训练 (oral muscle training), 关卡 (game levels), 连续打卡 (streaks), 成就徽章 (badges)
- Back-to-main link points to `/` (no Chinese main site)

**Universal Commerce Protocol (UCP)**
- Enhanced JSON-LD structured data on all 4 pages
- MobileApplication schema with Offer details (free, InStock availability)
- AggregateRating, seller info, keywords for agent discoverability
- Localized offers (USD for US, EUR for CH/DE/FR, CNY for CN)
- Makes Grimasso discoverable to commerce agents and platforms

**SEO & Navigation**
- Quadrilingual hreflang tags in sitemap.xml (EN, DE, FR, ZH)
- Canonical URLs for each language version
- Back-to-main links with proper localization (/de/ for German, /fr/ for French, / for Chinese)
- Language switcher with active state highlighting (EN/FR/DE/ZH)

## Offgrid Media Subsite

**10-locale landing page for the Offgrid Media iOS app** (`/offgridmedia/`)

- App source: `../share_to_save/` (directory name predates two renames: Share2Save → Kept → Offgrid Media). The former `/share2save/` subsite has been removed from this repo.
- The app hardcodes `lorenzmaierhofer.com/offgridmedia/` and `/offgridmedia/privacy` in its App Store metadata and in-app Settings, so **neither URL may change**
- Locales: EN at the root plus `ar de es fr hi id pt ru zh`, each with `index.html`, `privacy/index.html` and `age-rating/index.html`; `ar` is `dir="rtl"`
- The app is rated **16+**, driven solely by `unrestrictedWebAccess: true` in `../share_to_save/fastlane/metadata/app_rating_config.json`; every content descriptor there is `NONE`. `/offgridmedia/age-rating/` explains that, states the app ships no adult material, and states plainly that it does not stop anyone storing or playing such material (no content filter, age gate or parental mode). Copy lives in `_build/strings_age.py`; keep it in sync with that JSON
- `offgridmedia-styles.css` (deep navy + `#5CC8F7` icon-sky token layer, `--ogm-sky` / `--ogm-sky-dim`) and `offgridmedia-script.js`; both loaded after the shared `styles.css` / `script.js`. Palette is sampled from the app icon (navy field `#0A1631`–`#1B2E52`, sky strokes `#5CC8F7`, UI blue `#2F6FEC`); the `.offgridmedia-nav` spotlight badge in the root `styles.css` uses the same sky
- Signature interaction: the hero "airplane mode" switch toggles `body.is-online`, which fades the connectivity grid while the library card stays lit
- Scroll reveals are gated on `.ogm-anim` (added by JS) so content stays visible without JavaScript
- `APP_STORE_URL` at the top of `offgridmedia-script.js` is `null`; set it to `https://apps.apple.com/us/app/offgrid-media` once that listing is published and every "coming soon" badge turns into a real App Store button. Do **not** point it at the old Share2Save listing (`id6766317237`)

**Regenerating the pages**

All 20 HTML files are generated, not hand-edited. The generator and its per-locale UI strings live in `offgridmedia/_build/` (`build.py`, `strings.py`, `strings_b.py`; run `python3 build.py` from that directory, or `python3 build.py age` to regenerate only the age-rating pages — the deploy workflow excludes `**/*.py` and `**/*.sh`); marketing copy (hero lede, the seven feature cards, the rights notice) is read at build time from `../share_to_save/fastlane/metadata/<locale>/description.txt` and `fastlane/framing/titles/<locale>.strings` so the site never claims more than the reviewed App Store description. Small edits can be made directly in the HTML, but apply them to all 10 locales.

`build.py`'s `app_copy()` currently asserts on the English description (`expected 10 blocks, got 12`) because the store description grew — fix `N_BLOCKS` and the per-locale `feature_heads` before regenerating the landing or privacy pages. `build.py age` is unaffected.

**Regenerating the images**

`offgridmedia/_build/make_assets.sh` (needs `magick` + `ffmpeg`) rebuilds every image asset from the app repo: `icon.png` from `OffgridMedia/Assets.xcassets/AppIcon.appiconset/icon-1024.png`, the per-locale `screenshots/<loc>/{iphone,ipad}-*.webp` from fastlane's `*_framed.png` (iPhone 17 Pro Max → 660×1434, iPad Pro 13 → 720×960), `preview.mp4` + `preview-poster.webp` as a crossfade of the unframed English shots, and the `og-offgridmedia.jpg` social card. Locale mapping is in the script (`zh` → `zh-Hans`, `pt` → `pt-BR`, …). The app's `fastlane/previews/` screen recordings are not used — they go stale faster than the screenshots.

**Accuracy constraints**

- Never claim playback speed, sleep timer, subtitles, iCloud/cross-device sync, or a macOS version — none exist
- Never lead with downloading or "save from any link"; that framing caused an App Review 5.2.3 rejection. Import is the primary path, links are secondary, and the notice "only add content you have the right to keep" stays on the page
- The app has no analytics; the website does (Plausible). The privacy page states both

## P&G AI News (news.html)

Weekly auto-published section of **verbatim excerpts** from official P&G sources, rendered on `news.html`, `de/news.html`, `zh/news.html` by `loadPgAiNews()` in `script.js` from `/pg_ai_news.json`.

News page layout (all three locales): a TOC row (`.page-toc`) under the title. Then `.feeds`, two columns at ≥1100px and stacked below: `#my-posts` on the left (LinkedIn embeds) and `#pg-ai-news` on the right. Each column has a sticky `.feed-head` whose left edge colour marks the source (LinkedIn blue vs P&G blue). After that come Topics (`#topics`) and, last, Role changes (`#role-changes`, the former news cards). Anchor IDs carry `scroll-margin-top` to clear the fixed navbar.

- `.github/workflows/pg-ai-news.yml` runs Mondays 06:00 UTC, plus a Thursday catch-up for pages an outage skipped (and on demand). It runs `.github/scripts/pg_ai_news.py`, commits, then triggers `static.yml`, because a `GITHUB_TOKEN` push doesn't fire `on: push`
- Approved sources: `.github/pg_ai_sources.json` (`pg-blog` = us.pg.com/blogs, `sec-edgar` = P&G 8-K Exhibit 99 / 10-K). Only URLs under a source's `allowed_url_prefix` can publish. pginvestor.com blocks bots (403), so earnings releases come via SEC. Earnings calls: P&G publishes no transcript (its IR "Script and Slides" PDFs are only financial reconciliations), so `earnings-transcripts` uses StockAnalysis (data by Quartr). It's free, plain HTML, allowed by robots.txt, and only quarterly calls are taken (newest 4). Only speaker turns whose role contains "Procter & Gamble" are quotable, never analysts, the operator or the page's generated summary. The author is the executive who spoke the excerpt; an excerpt crossing two speakers is rejected LinkedIn is manual-only (no feed, scraping against its terms)
- Gemini (free tier; default `gemini-flash-latest`, the alias Google moves to the newest Flash release; fallback `gemini-flash-lite-latest`; repo variable `GEMINI_MODEL` takes a comma-separated chain) only decides "is AI a core message" and **selects** passages. It never writes text. Title/author/date come from page JSON-LD or SEC filing metadata. Every excerpt must be an exact span of the page (only whitespace and quote/dash glyphs may differ), and the page's own span is what gets published. Nothing is summarised, so there is no AI label. Every card links to the full original
- Resilience: page fetches retry 5xx/429/timeouts (3 tries) and refuse off-site redirects; each model in the chain gets 3 tries; 401/402/403 or 3 failed pages in a row stop model calls for the run; no new page starts after 12 min. Skipped pages are not marked seen, so the next run retries them. Actions are SHA-pinned and `google-genai` is pinned exactly; checkout keeps no token, only the push step gets it
- Limits: items no older than 60 days, at most 5 new per run. Rejected URLs go to `.github/pg_ai_news_seen.json` and aren't retried. Model/quota errors skip the page without marking it seen, so it is retried next run. A source failing two runs in a row turns the run red
- Add items by hand from an approved source: put `{url: [excerpt, ...]}` in a JSON file, then run `python3 .github/scripts/pg_ai_news.py --manual file.json`. It goes through the same verbatim checks, with no age limit. To remove an item, delete it from `pg_ai_news.json` and add its URL to `rejected` in the seen file. LinkedIn items can't be fetched or checked, so add them straight to `pg_ai_news.json` with `"channel": "linkedin", "added": "manual"`, copying the post text verbatim
- Repo secret `GEMINI_API_KEY` (Google AI Studio) and variable `SEC_USER_AGENT` (`lorenzmaierhofer.com`; the script appends ` news-bot`, because SEC rejects a bare domain)
- When a run publishes something, the workflow opens a GitHub issue assigned to the repo owner that lists the new items. GitHub emails the assignee; that is the notification, with no SMTP or secrets involved. No issue is opened on no-change runs
- RSS: `/news.xml` is generated from `pg_ai_news.json` plus Lorenz's own posts in `linkedin_posts.json` (date decoded from the post ID, no text, links to the post; channel `my-posts`) by `.github/scripts/news_feed.py` (stdlib, self-checks well-formedness and order). The workflow runs it before committing; after a hand edit of the JSON, run it yourself. `static.yml` also rebuilds it on every deploy, so adding a post to `linkedin_posts.json` is enough. News pages link it via `<link rel="alternate">` and the `.feed-rss` button in the P&G feed head
- Self-check: `python3 .github/scripts/test_pg_ai_news.py`

## File Conventions

- When updating content, ensure changes are made to all relevant language versions (EN, DE, FR, ZH for Grimasso)
- German translations should use proper umlauts (ä, ö, ü) not ASCII substitutes (ae, oe, ue)
- Chinese translations should use Simplified Chinese characters, address parents with 您 (formal)
- Image assets and videos go in root directory or `/grimasso/`, referenced with proper paths
- Link styling in project cards (`.project-card h2 a`, `.project-card p a`) uses theme colors with hover effects
- When formatting headings with links: inherit text color, add cyan accent on hover with underline
