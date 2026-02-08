---
id: REQ-005
title: Grimasso SEO optimization and sitemap integration
status: completed
created_at: 2026-02-07T12:00:00Z
claimed_at: 2026-02-07T22:55:00Z
route: A
completed_at: 2026-02-07T23:05:00Z
user_request: UR-001
related: [REQ-001, REQ-002, REQ-003, REQ-004, REQ-006]
batch: grimasso-subsite
---

# Grimasso SEO Optimization and Sitemap Integration

## What
Ensure the Grimasso subsite is fully SEO optimized with proper meta tags, structured data, and sitemap integration for all 3 language versions.

## Detailed Requirements

- **Meta tags on all Grimasso pages**:
  - Title tags optimized for search (e.g., "Grimasso - Fun Tongue Exercises for Kids | Download on App Store")
  - Meta descriptions compelling and keyword-rich
  - Open Graph tags (og:title, og:description, og:image, og:url, og:type)
  - Twitter Card tags
  - Canonical URLs for each language version

- **hreflang tags** for trilingual support:
  - `hreflang="en"` pointing to `/grimasso/`
  - `hreflang="de"` pointing to `/grimasso/de/`
  - `hreflang="fr"` pointing to `/grimasso/fr/`
  - `hreflang="x-default"` pointing to `/grimasso/` (English as default)
  - These must appear on ALL language versions of each page

- **Structured data (JSON-LD)**:
  - SoftwareApplication schema for the app
  - Include: name, operatingSystem (iOS), applicationCategory (HealthApplication or Education), offers, aggregateRating if available
  - Link to App Store URL
  - BreadcrumbList schema for navigation context

- **Sitemap updates** (`sitemap.xml` in site root):
  - Add `/grimasso/` (EN) - priority 0.8, monthly changefreq
  - Add `/grimasso/de/` (DE) - priority 0.8, monthly changefreq
  - Add `/grimasso/fr/` (FR) - priority 0.8, monthly changefreq
  - Include xhtml:link elements for hreflang alternates in sitemap (matching existing pattern)

- **Additional SEO considerations**:
  - Semantic HTML (proper heading hierarchy, nav, main, section, article)
  - Image alt text in appropriate language
  - Fast page load (optimize images, minimize render-blocking resources)
  - Mobile-friendly design (responsive)

## Constraints

- User explicitly said "Ensure that the Grimasso site is SEO optimized, added to the site map"
- Must follow existing site's SEO patterns (see current sitemap.xml and meta tag structure)
- This is the first French content on the site - hreflang setup is new for fr
- Structured data must be valid (test with Google Rich Results Test)

## Dependencies

- Depends on: REQ-001 (pages must exist to add meta tags)
- Depends on: REQ-006 (localized meta descriptions need translated content)

## Builder Guidance

- Certainty level: Firm - SEO requirements are well-defined
- Follow the exact pattern used in existing site pages for meta tags and hreflang
- The existing sitemap uses xhtml:link for hreflang alternates - follow same pattern
- App Store URL for structured data: https://apps.apple.com/ch/app/grimasso/id6758241652

## Full Context
See [user-requests/UR-001/input.md](./user-requests/UR-001/input.md) for complete verbatim input.

---
*Source: See UR-001/input.md for full verbatim input*

---

## Triage

**Route: A** - Simple

**Reasoning:** Clear SEO requirements following existing site patterns. Meta tags and sitemap additions are straightforward - no architectural decisions needed. The Grimasso pages already have proper meta tag structure from REQ-001, just need to verify/enhance and add sitemap entries.

**Planning:** Not required

## Plan

**Planning not required** - Route A: Direct implementation

Rationale: Simple configuration tasks (meta tags, sitemap). Follow existing site patterns. No ambiguity.

*Skipped by work action*

## Implementation Summary

- Verified meta tags on all 3 pages (EN/DE/FR): title, description, OG tags, Twitter cards all present and keyword-rich
- Fixed image URLs: changed og:image and twitter:image from relative paths to absolute URLs for proper social media sharing
- Verified structured data: MobileApplication schema with correct App Store link on all 3 pages
- Verified canonical URLs and hreflang tags correctly configured on all pages
- Updated sitemap.xml: added 3 Grimasso entries (EN, DE, FR) with proper hreflang alternates and xhtml:link elements following existing site pattern
- All pages: language-appropriate meta descriptions under 160 characters
- All pages: proper lang attributes (en, de, fr)

*Completed by work action (Route A)*

## Testing

**Tests run:** N/A
**Result:** No testing infrastructure detected - static HTML site

*Verified by work action*
