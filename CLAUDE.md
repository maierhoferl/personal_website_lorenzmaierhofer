# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal website for Lorenz Maierhofer, Senior Director and Global Lead for AI Factory, Agentic AI Products & AI Governance at Procter & Gamble. Static site hosted on GitHub Pages at lorenzmaierhofer.com.

## Architecture

**Static HTML/CSS/JS site with bilingual support (English/German)**

- Root level: English pages (`index.html`, `news.html`, `projects.html`)
- `/de/` folder: German pages (same structure)
- Single shared `styles.css` and `script.js` (German pages reference via `../`)
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

## File Conventions

- When updating content, ensure changes are made to both English and German versions
- German translations should use proper umlauts (ä, ö, ü) not ASCII substitutes (ae, oe, ue)
- Image assets go in root directory, referenced from `/de/` pages with `../` prefix
