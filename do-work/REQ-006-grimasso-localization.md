---
id: REQ-006
title: Grimasso full localization (EN/FR/DE)
status: pending
created_at: 2026-02-07T12:00:00Z
user_request: UR-001
related: [REQ-001, REQ-002, REQ-003, REQ-004, REQ-005]
batch: grimasso-subsite
---

# Grimasso Full Localization (EN/FR/DE)

## What
Fully localize the Grimasso marketing subsite into English, French, and German, ensuring all content, UI text, meta tags, and marketing copy is properly translated.

## Detailed Requirements

- **Three complete language versions**:
  - English (`/grimasso/index.html`) - primary/source language
  - German (`/grimasso/de/index.html`) - German translation
  - French (`/grimasso/fr/index.html`) - French translation

- **Content to localize**:
  - All marketing copy (headlines, descriptions, feature lists, CTAs)
  - Navigation labels and UI text
  - Meta tags (title, description, Open Graph)
  - Image alt text
  - Button text (e.g., "Download on App Store" → "Im App Store laden" / "Télécharger sur l'App Store")
  - Footer text and links

- **Language-specific app terminology**:
  - The app itself uses these exercise category names:
    - EN: Tongue Tip, Tongue Strength, Tongue Control, Swallowing, Jaw Muscles
    - DE: Zungenspitze, Zungenkraft, Zungensteuerung, Schlucken, Kiefermuskeln
    - FR: Pointe de la langue, Force de la langue, Contrôle de la langue, Déglutition, Muscles de la mâchoire
  - Use the app's own terminology to maintain consistency

- **Language switcher**:
  - Visible on all pages
  - Shows current language highlighted
  - Links to the equivalent page in other languages
  - Use language names in their own language: English, Deutsch, Français

- **German-specific requirements**:
  - Use proper umlauts (ä, ö, ü) not ASCII substitutes (ae, oe, ue) - per CLAUDE.md convention
  - German translation should feel natural, not machine-translated
  - App tagline in German: "Zungenübungen mit Spaß!"

- **French-specific requirements**:
  - This is the first French content on the site
  - App tagline in French: "Exercices de langue amusants!"
  - Use proper French punctuation (spaces before colons, semicolons, etc.)
  - Proper accents on all French characters (é, è, ê, ë, à, ç, etc.)

- **App Store link**:
  - Same URL for all languages: https://apps.apple.com/ch/app/grimasso/id6758241652
  - The App Store itself handles language display

## Constraints

- User explicitly said "Ensure that it is localized into all 3 supported languages, english, french and german"
- Must match the app's own language support (the app supports EN/FR/DE)
- German translations must use proper umlauts per CLAUDE.md
- French is new for this site - no existing French patterns to follow, but follow the EN/DE pattern

## Dependencies

- Depends on: REQ-003 (English content must be written first as source for translation)
- Depends on: REQ-001 (page structure must support 3 languages)
- Related to: REQ-005 (SEO meta tags need localized versions)

## Builder Guidance

- Certainty level: Firm - 3 languages are required, no ambiguity
- Write English first, then translate to DE and FR
- The app's own Localizable.strings files at ../LogoApp/ contain authoritative translations for app-specific terms
- Consider the audience: parents of children with speech therapy needs - use warm, encouraging, accessible language
- French translations should be natural European French (not Canadian French)

## Full Context
See [user-requests/UR-001/input.md](./user-requests/UR-001/input.md) for complete verbatim input.

---
*Source: See UR-001/input.md for full verbatim input*
