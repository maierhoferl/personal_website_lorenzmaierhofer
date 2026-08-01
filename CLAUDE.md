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
- Locales: EN at the root plus `ar de es fr hi id pt ru zh`, each with `index.html` and `privacy/index.html`; `ar` is `dir="rtl"`
- `offgridmedia-styles.css` (deep navy + `#F2A93B` amber token layer) and `offgridmedia-script.js`; both loaded after the shared `styles.css` / `script.js`
- Signature interaction: the hero "airplane mode" switch toggles `body.is-online`, which fades the connectivity grid while the library card stays lit
- Scroll reveals are gated on `.ogm-anim` (added by JS) so content stays visible without JavaScript
- `APP_STORE_URL` at the top of `offgridmedia-script.js` is `null`; set it to `https://apps.apple.com/us/app/offgrid-media` once that listing is published and every "coming soon" badge turns into a real App Store button. Do **not** point it at the old Share2Save listing (`id6766317237`)

**Regenerating the pages**

All 20 HTML files are generated, not hand-edited. The generator and its per-locale UI strings live in `offgridmedia/_build/` (`build.py`, `strings.py`, `strings_b.py`; run `python3 build.py` from that directory — the deploy workflow excludes `**/*.py`); marketing copy (hero lede, the seven feature cards, the rights notice) is read at build time from `../share_to_save/fastlane/metadata/<locale>/description.txt` and `fastlane/framing/titles/<locale>.strings` so the site never claims more than the reviewed App Store description. Small edits can be made directly in the HTML, but apply them to all 10 locales.

**Accuracy constraints**

- Never claim playback speed, sleep timer, subtitles, iCloud/cross-device sync, or a macOS version — none exist
- Never lead with downloading or "save from any link"; that framing caused an App Review 5.2.3 rejection. Import is the primary path, links are secondary, and the notice "only add content you have the right to keep" stays on the page
- The app has no analytics; the website does (Plausible). The privacy page states both

## File Conventions

- When updating content, ensure changes are made to all relevant language versions (EN, DE, FR, ZH for Grimasso)
- German translations should use proper umlauts (ä, ö, ü) not ASCII substitutes (ae, oe, ue)
- Chinese translations should use Simplified Chinese characters, address parents with 您 (formal)
- Image assets and videos go in root directory or `/grimasso/`, referenced with proper paths
- Link styling in project cards (`.project-card h2 a`, `.project-card p a`) uses theme colors with hover effects
- When formatting headings with links: inherit text color, add cyan accent on hover with underline
