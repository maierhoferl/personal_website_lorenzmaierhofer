---
id: REQ-004
title: Grimasso interactive elements and animations
status: pending
created_at: 2026-02-07T12:00:00Z
user_request: UR-001
related: [REQ-001, REQ-002, REQ-003, REQ-005, REQ-006]
batch: grimasso-subsite
---

# Grimasso Interactive Elements and Animations

## What
Implement fun, engaging interactive elements and color animations throughout the Grimasso subsite to make it playful and delightful, matching the app's kid-friendly spirit.

## Detailed Requirements

- **Color animations** using the Grimasso palette:
  - Animated gradient backgrounds that shift between green, yellow, orange, pink
  - Pulsing/glowing effects on CTAs and badges
  - Color-transitioning section dividers (wave shapes, not straight lines)
  - Animated accent elements (floating dots, stars, or small frog silhouettes)

- **Scroll-triggered animations**:
  - Features cards animate in with bounce/spring effects (not just fade)
  - Statistics numbers count up when they scroll into view (51 exercises, 10 levels, etc.)
  - Staggered reveal of exercise category cards
  - Parallax-lite effects on background elements

- **Interactive elements**:
  - Grimasso mascot reacts to mouse hover or click (wobble, tongue out, wink)
  - Interactive exercise category cards that flip or expand on click to show details
  - Animated App Store download button with attention-grabbing effect
  - Fun cursor effects or hover states on interactive elements
  - Consider a mini "try it" interaction (e.g., click to hear a frog croak, or tap a sequence)

- **Micro-interactions**:
  - Button hover effects with playful bounce
  - Card tilt/3D effect on hover
  - Smooth transitions between sections
  - Loading animations with Grimasso theme

- **Performance**:
  - Use CSS animations where possible (GPU-accelerated)
  - JavaScript only for scroll-triggered and interaction-driven animations
  - Respect `prefers-reduced-motion` for accessibility
  - Keep page load fast despite animations

## Constraints

- Must not slow down page load or hurt Core Web Vitals
- Must work on mobile (touch interactions instead of hover where needed)
- Must respect `prefers-reduced-motion` media query
- Animations should enhance, not distract from the marketing message
- User explicitly said "uses color animations and visuals from the Grimasso app"

## Dependencies

- Depends on: REQ-001 (scaffolding), REQ-002 (visual design provides the canvas)
- Consider creating a dedicated `grimasso-script.js` or adding to main `script.js`

## Builder Guidance

- Certainty level: Exploratory - user wants "extra fun and engaging" but specific interactions are builder's choice
- Scope cue: Go creative here - the user explicitly asked for fun and engaging
- The main site already has particle effects (AI particle explosion on profile image click) - this site should have its own playful equivalent
- Think of sites like "makefrontendshitagain.party" for inspiration on fun web experiences
- The app itself has confetti celebrations for achievements - consider confetti on CTA click

## Full Context
See [user-requests/UR-001/input.md](./user-requests/UR-001/input.md) for complete verbatim input.

---
*Source: See UR-001/input.md for full verbatim input*
