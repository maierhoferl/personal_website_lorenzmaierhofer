# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal website for Lorenz Maierhofer, Senior Director and Global Lead for AI Factory, Agentic AI Products & AI Governance at Procter & Gamble. Static site hosted on GitHub Pages at lorenzmaierhofer.com.

## Architecture

**Static HTML/CSS/JS site with multilingual support (English/German/French)**

- Root level: English pages (`index.html`, `news.html`, `projects.html`)
- `/de/` folder: German pages (same structure)
- `/grimasso/` folder: Trilingual Grimasso app subsite (EN, DE `/de/`, FR `/fr/`)
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

**Trilingual Tongue-Training App Landing Page** (EN, DE, FR)

**Structure**
- `/grimasso/index.html` - English landing page
- `/grimasso/de/index.html` - German landing page
- `/grimasso/fr/index.html` - French landing page
- `/grimasso/grimasso-styles.css` - Custom styling (kid-friendly, bright palette #33C759 primary)
- `/grimasso/grimasso-script.js` - Interactive features (animations, confetti, count-ups)
- `/grimasso/Grimasso_Welcome.mov` - Hero video (with image fallback)

**Key Features**
- Playful, kid-friendly aesthetic with bright green primary color (#33C759)
- Animated hero with floating bubbles, decorative emojis, wavy SVG dividers
- 51 scientifically-designed exercises across 5 categories
- Gamification elements: 10 levels, 25+ achievement badges, streak tracking
- Comprehensive app features section (12 features with emoji icons)
- "By the Numbers" statistics section with count-up animations
- Parent-focused benefits messaging
- Confetti burst animations on CTA clicks
- Card tilt/3D hover effects with bounce scroll animations
- Scroll progress indicator bar
- Accessibility: respects prefers-reduced-motion

**Universal Commerce Protocol (UCP)**
- Enhanced JSON-LD structured data on all 3 pages
- MobileApplication schema with Offer details (free, InStock availability)
- AggregateRating, seller info, keywords for agent discoverability
- Localized offers (USD for US, EUR for CH/DE/FR)
- Makes Grimasso discoverable to commerce agents and platforms

**SEO & Navigation**
- Trilingual hreflang tags in sitemap.xml
- Canonical URLs for each language version
- Back-to-main links with proper localization (/de/ for German, /fr/ for French)
- Language switcher with active state highlighting

## File Conventions

- When updating content, ensure changes are made to all relevant language versions (EN, DE, FR)
- German translations should use proper umlauts (ä, ö, ü) not ASCII substitutes (ae, oe, ue)
- Image assets and videos go in root directory or `/grimasso/`, referenced with proper paths
- Link styling in project cards (`.project-card h2 a`, `.project-card p a`) uses theme colors with hover effects
- When formatting headings with links: inherit text color, add cyan accent on hover with underline
