---
id: REQ-001
title: Grimasso subsite structure and page scaffolding
status: completed
created_at: 2026-02-07T12:00:00Z
claimed_at: 2026-02-07T21:45:00Z
route: C
completed_at: 2026-02-07T21:58:00Z
user_request: UR-001
related: [REQ-002, REQ-003, REQ-004, REQ-005, REQ-006]
batch: grimasso-subsite
---

# Grimasso Subsite Structure and Page Scaffolding

## What
Create the directory structure and HTML page scaffolding for the Grimasso marketing subsite with support for 3 languages (English, French, German).

## Detailed Requirements

- Create `/grimasso/index.html` (English landing page)
- Create `/grimasso/de/index.html` (German landing page)
- Create `/grimasso/fr/index.html` (French landing page)
- Each page needs proper navigation with language switcher (EN/FR/DE)
- Include a "back to main site" link in the header
- Create `/grimasso/grimasso-styles.css` for Grimasso-specific styles that layer on top of the main site's design system
- Reference shared `styles.css` and `script.js` from the main site for base functionality (theme toggle, mobile menu)
- Maintain the existing `/grimasso/privacy.txt` (convert to privacy.html later if needed)
- The subsite should feel like a cohesive part of lorenzmaierhofer.com while having its own Grimasso identity
- Use the Grimasso color palette as CSS custom properties: Primary Green #33C759, Dark Green #26A647, Light Green #66E080, Yellow #FFD933, Orange #FF9933, Pink #FF8099, Blue #66B3FF, Purple #B380FF, Background #FAFAF2, Text #333340

## Constraints

- Must work as static HTML (no build step) - consistent with existing site architecture
- German pages use `/grimasso/de/` path (matching site convention)
- French pages use `/grimasso/fr/` path (new for this site - first French content)
- Must be deployable via existing GitHub Pages workflow (no changes needed)
- Reference main site assets with appropriate relative paths

## Dependencies

- Blocks: REQ-002 (hero/visuals), REQ-003 (content), REQ-004 (interactions), REQ-005 (SEO), REQ-006 (localization) - all need the scaffolding first

## Builder Guidance

- Certainty level: Firm on structure, flexible on exact page sections
- User wants a "compelling marketing website" - this should be more than a simple landing page
- Look at existing site structure in `/de/` for patterns to follow
- The Grimasso app icon already exists at `/Grimasso_Main.png` in the site root

## Full Context
See [user-requests/UR-001/input.md](./user-requests/UR-001/input.md) for complete verbatim input.

---
*Source: See UR-001/input.md for full verbatim input*

---

## Triage

**Route: C** - Complex

**Reasoning:** New subsite requiring trilingual page scaffolding, custom CSS layer, language switcher, and directory structure. This is the foundational REQ that blocks all 5 other Grimasso REQs. Architectural decisions needed for path structure, CSS layering, and shared asset referencing.

**Planning:** Required

## Plan

### Directory Structure
```
grimasso/
├── index.html          (English landing page)
├── grimasso-styles.css (Grimasso-specific CSS layer)
├── grimasso-script.js  (Grimasso-specific JS - language switcher, interactions)
├── privacy.txt         (existing - keep as-is)
├── de/
│   └── index.html      (German landing page)
└── fr/
    └── index.html      (French landing page)
```

### Architecture Decisions

1. **CSS Layering**: `grimasso-styles.css` loads AFTER main `styles.css` to override variables and add Grimasso-specific styles. Uses CSS custom properties to override the main site's palette with Grimasso colors.

2. **Asset References**:
   - English page (`/grimasso/index.html`): `../styles.css`, `../script.js`, `./grimasso-styles.css`
   - German page (`/grimasso/de/index.html`): `../../styles.css`, `../../script.js`, `../grimasso-styles.css`
   - French page (`/grimasso/fr/index.html`): `../../styles.css`, `../../script.js`, `../grimasso-styles.css`
   - App icon: `../Grimasso_Main.png` from EN, `../../Grimasso_Main.png` from DE/FR

3. **Navigation**: Simplified nav with Grimasso branding instead of "LM" logo. Includes:
   - Grimasso logo/name as home link
   - "Back to main site" link (arrow + text)
   - Language switcher (EN | FR | DE) with active state
   - Theme toggle (reusing main site's script.js functionality)

4. **Page Sections** (scaffold with placeholder content for REQ-002/003/004/006 to fill):
   - Hero section (app showcase with CTA)
   - Features section (exercise categories)
   - How it works section
   - Benefits for parents section
   - App Store CTA section
   - Footer with privacy link and back-to-main-site

5. **Color Palette CSS Variables**:
   ```css
   --grimasso-primary: #33C759;
   --grimasso-dark: #26A647;
   --grimasso-light: #66E080;
   --grimasso-yellow: #FFD933;
   --grimasso-orange: #FF9933;
   --grimasso-pink: #FF8099;
   --grimasso-blue: #66B3FF;
   --grimasso-purple: #B380FF;
   --grimasso-bg: #FAFAF2;
   --grimasso-text: #333340;
   ```

6. **Grimasso-specific JS**: A small `grimasso-script.js` for the language switcher active state logic (the main `script.js` handles theme toggle and other shared functionality).

### Implementation Order
1. Create `grimasso/grimasso-styles.css` with Grimasso color overrides and layout styles
2. Create `grimasso/grimasso-script.js` for Grimasso-specific interactions
3. Create `grimasso/index.html` (English) with full page structure
4. Create `grimasso/de/index.html` (German) - adapted from English
5. Create `grimasso/fr/index.html` (French) - adapted from English

*Generated by orchestrator (inline plan)*

## Exploration

### Existing Patterns Found
- **Main site nav**: Uses `.navbar`, `.nav-container`, `.nav-menu`, `.nav-social`, `.lang-switch` classes
- **Language switcher**: Simple `<a>` tag with `.lang-switch` class, stores preference in `localStorage`
- **Theme toggle**: `#themeToggle` button in `.nav-social`, persisted via `localStorage`
- **CSS variables**: Defined in `:root` and `[data-theme="light"]` selector
- **Font stack**: `Space Grotesk` (headings), `Space Mono` (mono), `Orbitron` (display)
- **Google Fonts**: Loaded via preconnect + stylesheet link
- **German pattern**: `/de/index.html` references `../styles.css` and `../script.js`
- **Grimasso app icon**: `Grimasso_Main.png` in site root (1.6MB)
- **Existing grimasso dir**: Only contains `privacy.txt`
- **App Store link**: `https://apps.apple.com/ch/app/grimasso/id6758241652` (Swiss store) or `/us/app/` variant
- **Grimasso description**: "Tongue-training for Kids" - iPhone/iPad app for speech and tongue training

### Key Concerns
- The main `script.js` has a language switch listener that expects only DE/EN toggle - the Grimasso subsite needs its own 3-way language switcher
- The Grimasso pages should NOT include the main site's nav menu items (About/News/Projects) - only Grimasso-relevant navigation
- The `Grimasso_Main.png` is 1.6MB - may want to reference it carefully for performance

*Generated by orchestrator (inline exploration)*

## Implementation Summary

- Created `grimasso/grimasso-styles.css` (16.6KB) - Full CSS layer with Grimasso color palette, light-by-default theme, dark mode support, responsive breakpoints
- Created `grimasso/grimasso-script.js` (1.8KB) - Light theme default, Intersection Observer for card animations
- Created `grimasso/index.html` (16.4KB) - English landing page with hero, features, how-it-works, benefits, CTA sections
- Created `grimasso/de/index.html` (16.9KB) - Complete German translation with proper umlauts
- Created `grimasso/fr/index.html` (17.3KB) - Complete French translation with proper accents
- Existing `grimasso/privacy.txt` untouched
- No files outside `grimasso/` were modified

*Completed by work action (Route C)*

## Testing

**Tests run:** N/A
**Result:** No testing infrastructure detected - static HTML site

*Verified by work action*
