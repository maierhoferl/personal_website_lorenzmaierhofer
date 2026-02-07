---
id: REQ-002
title: Grimasso hero section and visual design
status: pending
created_at: 2026-02-07T12:00:00Z
user_request: UR-001
related: [REQ-001, REQ-003, REQ-004, REQ-005, REQ-006]
batch: grimasso-subsite
---

# Grimasso Hero Section and Visual Design

## What
Design and implement a compelling, fun hero section and overall visual design for the Grimasso marketing subsite that captures the playful, kid-friendly spirit of the app.

## Detailed Requirements

- Eye-catching hero section with the Grimasso frog mascot as the centerpiece
- Use the Grimasso app icon (`Grimasso_Main.png`) prominently
- Animated gradient backgrounds using Grimasso's signature lime green (#33C759) palette
- Bright, colorful sections that transition between Grimasso's brand colors (green, yellow, orange, pink)
- Kid-friendly design aesthetic: rounded corners, bouncy feel, playful typography
- Hero tagline in each language (e.g., "Fun Tongue Exercises with Grimasso the Frog!")
- Prominent App Store download button with Apple icon (link: https://apps.apple.com/ch/app/grimasso/id6758241652)
- The page should feel distinctly different from the main site's cyberpunk aesthetic - it's a kids' app
- Use playful fonts appropriate for a children's app while maintaining readability
- Consider animated elements in the hero: floating bubbles, bouncing mascot, tongue-themed playful motifs
- Responsive design that works beautifully on all devices (parents browse on phones)
- Dark/light theme support inherited from main site, but with Grimasso color overrides

## Constraints

- Must use existing `Grimasso_Main.png` asset (1.6MB - consider optimization)
- Keep CSS animations performant (prefer transform/opacity, avoid layout thrashing)
- Must look great on mobile first (many parents will find this on their phones)
- Must feel "extra fun and engaging" per user's explicit request

## Dependencies

- Depends on: REQ-001 (page scaffolding must exist first)
- Related to: REQ-004 (interactive animations build on the visual foundation)

## Builder Guidance

- Certainty level: Firm on "fun and engaging", flexible on specific visual implementation
- User explicitly said "Make it extra fun and engaging!" - this is the primary design directive
- The app itself uses SF Rounded font family; consider Google Fonts equivalents (Nunito, Quicksand, etc.)
- Think app landing pages like those on Apple's App Store featured pages
- The Grimasso frog has multiple emotional states - consider showing different expressions

## Full Context
See [user-requests/UR-001/input.md](./user-requests/UR-001/input.md) for complete verbatim input.

---
*Source: See UR-001/input.md for full verbatim input*
