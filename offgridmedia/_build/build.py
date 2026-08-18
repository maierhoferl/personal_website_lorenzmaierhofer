#!/usr/bin/env python3
"""Generate the /offgridmedia/ landing + privacy pages for all 10 locales.

Marketing copy (lede, the seven feature blocks, the rights notice) is taken
verbatim from the app's App Store metadata in ../share_to_save/fastlane so the
site never claims something the reviewed description does not.
"""
import os
import re
import html

APP = "/Users/lorenzmaierhofer/claude-projects/share_to_save/fastlane"
OUT = "/Users/lorenzmaierhofer/claude-projects/Personal_Website/offgridmedia"

# site locale -> (metadata dir, framing titles file, hreflang, og:locale, html dir)
LOCALES = {
    "en": ("en-US",   "en-US",   "en",      "en_US", "ltr"),
    "ar": ("ar-SA",   "ar-SA",   "ar",      "ar_SA", "rtl"),
    "de": ("de-DE",   "de-DE",   "de",      "de_DE", "ltr"),
    "es": ("es-ES",   "es-ES",   "es",      "es_ES", "ltr"),
    "fr": ("fr-FR",   "fr-FR",   "fr",      "fr_FR", "ltr"),
    "hi": ("hi",      "hi-IN",   "hi",      "hi_IN", "ltr"),
    "id": ("id",      "id-ID",   "id",      "id_ID", "ltr"),
    "pt": ("pt-BR",   "pt-BR",   "pt-BR",   "pt_BR", "ltr"),
    "ru": ("ru",      "ru-RU",   "ru",      "ru_RU", "ltr"),
    "zh": ("zh-Hans", "zh-Hans", "zh-Hans", "zh_CN", "ltr"),
}
ORDER = ["en", "ar", "de", "es", "fr", "hi", "id", "pt", "ru", "zh"]
N_BLOCKS = 10  # feature sections in the store description
SHOTS = ["01_library", "02_import", "03_folders", "04_player", "05_actions", "06_settings"]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def app_copy(loc):
    """Pull lede, the 7 feature blocks and the rights notice from the store description."""
    meta = LOCALES[loc][0]
    paras = [p.strip() for p in read(f"{APP}/metadata/{meta}/description.txt").split("\n\n") if p.strip()]
    blocks = []
    for p in paras[2:-1]:
        p = p.rstrip("—").strip()
        if not p:
            continue
        head, _, body = p.partition("\n")
        blocks.append((head.strip(), body.strip()))
    assert len(blocks) == N_BLOCKS, f"{loc}: expected {N_BLOCKS} blocks, got {len(blocks)}"
    # The store description shouts its section headings in caps; the page uses
    # sentence case instead (per-locale, because casing rules differ).
    heads = STRINGS[loc].get("feature_heads")
    if heads:
        assert len(heads) == N_BLOCKS, f"{loc}: need {N_BLOCKS} feature headings"
        blocks = [(heads[i], blocks[i][1]) for i in range(N_BLOCKS)]
    rights = paras[-1]
    promo = read(f"{APP}/metadata/{meta}/promotional_text.txt")
    return {
        "lede": paras[1],
        "blocks": blocks,
        "rights": rights,
        "promo": promo,
        "subtitle": read(f"{APP}/metadata/{meta}/subtitle.txt"),
        "keywords": read(f"{APP}/metadata/{meta}/keywords.txt"),
    }


def framing(loc):
    txt = read(f"{APP}/framing/titles/{LOCALES[loc][1]}.strings")
    out = {}
    for m in re.finditer(r'"([^"]+)"\s*=\s*"((?:[^"\\]|\\.)*)"\s*;', txt):
        out[m.group(1)] = m.group(2).replace('\\"', '"')
    return out


def e(s):
    return html.escape(s, quote=True)


APPLE_SVG = ('<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true">'
             '<path d="M17.05 20.28c-.98.95-2.05.88-3.08.4-1.09-.5-2.08-.48-3.24 0-1.44.62-2.2.44-3.06-.4C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09l.01-.01zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>')

THEME_SVG = ('<svg class="sun-icon" viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 17.5a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zm0 1.5a7 7 0 1 1 0-14 7 7 0 0 1 0 14zm0-17a.75.75 0 0 1 .75.75v1.5a.75.75 0 0 1-1.5 0v-1.5A.75.75 0 0 1 12 2zm0 18a.75.75 0 0 1 .75.75v1.5a.75.75 0 0 1-1.5 0v-1.5A.75.75 0 0 1 12 20zM4.22 4.22a.75.75 0 0 1 1.06 0l1.06 1.06a.75.75 0 0 1-1.06 1.06L4.22 5.28a.75.75 0 0 1 0-1.06zm13.44 13.44a.75.75 0 0 1 1.06 0l1.06 1.06a.75.75 0 0 1-1.06 1.06l-1.06-1.06a.75.75 0 0 1 0-1.06zM2 12a.75.75 0 0 1 .75-.75h1.5a.75.75 0 0 1 0 1.5h-1.5A.75.75 0 0 1 2 12zm18 0a.75.75 0 0 1 .75-.75h1.5a.75.75 0 0 1 0 1.5h-1.5A.75.75 0 0 1 20 12zM5.28 17.66a.75.75 0 0 1 0 1.06l-1.06 1.06a.75.75 0 1 1-1.06-1.06l1.06-1.06a.75.75 0 0 1 1.06 0zm13.44-13.44a.75.75 0 0 1 0 1.06l-1.06 1.06a.75.75 0 1 1-1.06-1.06l1.06-1.06a.75.75 0 0 1 1.06 0z"/></svg>'
             '<svg class="moon-icon" viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 3a9 9 0 1 0 9 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 0 1-4.4 2.26 5.403 5.403 0 0 1-3.14-9.8c-.44-.06-.9-.1-1.36-.1z"/></svg>')

FEATURE_ICONS = [
    '<path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M4 20h16"/>',
    '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    '<rect x="5" y="2" width="14" height="20" rx="3"/><path d="M9 18h6"/>',
    '<path d="m6 4 12 8-12 8z"/>',
    '<path d="M9 18V6l10-2v12"/><circle cx="6" cy="18" r="3"/><circle cx="16" cy="16" r="3"/>',
    '<path d="M5 3v18"/><path d="M12 8v13"/><path d="M19 3v18"/><circle cx="5" cy="8" r="2"/><circle cx="12" cy="16" r="2"/><circle cx="19" cy="10" r="2"/>',
    '<path d="M4 6h10"/><path d="M4 12h10"/><path d="M4 18h10"/><path d="M18 4v16"/><circle cx="18" cy="12" r="2"/>',
    '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M7 12h10"/><path d="M7 16h6"/>',
    '<path d="M6 5h12"/><rect x="4" y="9" width="16" height="11" rx="2"/><path d="M10 13h4"/>',
    '<path d="M12 3 4 6v6c0 4.5 3.4 8.3 8 9 4.6-.7 8-4.5 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
]

LANG_LABELS = {"en": "EN", "ar": "AR", "de": "DE", "es": "ES", "fr": "FR",
               "hi": "HI", "id": "ID", "pt": "PT", "ru": "RU", "zh": "ZH"}


def lang_select(cur, suffix):
    """suffix is '' for the landing page, 'privacy' for the policy page."""
    opts = []
    for loc in ORDER:
        base = "/offgridmedia/" if loc == "en" else f"/offgridmedia/{loc}/"
        sel = " selected" if loc == cur else ""
        opts.append(f'<option value="{base}{suffix}"{sel}>{LANG_LABELS[loc]}</option>')
    return "\n                        ".join(opts)


def hreflangs(suffix):
    rows = []
    for loc in ORDER:
        base = "https://lorenzmaierhofer.com/offgridmedia/" if loc == "en" else f"https://lorenzmaierhofer.com/offgridmedia/{loc}/"
        rows.append(f'<link rel="alternate" hreflang="{LOCALES[loc][2]}" href="{base}{suffix}">')
    rows.append(f'<link rel="alternate" hreflang="x-default" href="https://lorenzmaierhofer.com/offgridmedia/{suffix}">')
    return "\n    ".join(rows)


def nav(loc, t, root, active):
    """Shared navbar. `active` is 'index' or 'privacy'."""
    home = "/offgridmedia/" if loc == "en" else f"/offgridmedia/{loc}/"
    back = {"de": "/de/", "zh": "/zh/"}.get(loc, "/")
    if active == "index":
        links = (f'<li><a href="#library" class="nav-link">{e(t["nav_library"])}</a></li>\n'
                 f'                <li><a href="#features" class="nav-link">{e(t["nav_features"])}</a></li>\n'
                 f'                <li><a href="{home}privacy" class="nav-link">{e(t["nav_privacy"])}</a></li>\n'
                 f'                <li><a href="#faq" class="nav-link">{e(t["nav_faq"])}</a></li>')
        sel = lang_select(loc, "")
    else:
        links = (f'<li><a href="{home}" class="nav-link">{e(t["nav_overview"])}</a></li>\n'
                 f'                <li><a href="{home}#features" class="nav-link">{e(t["nav_features"])}</a></li>\n'
                 f'                <li><a href="{home}privacy" class="nav-link active">{e(t["nav_privacy"])}</a></li>')
        sel = lang_select(loc, "privacy")
    return f'''<nav class="navbar">
        <div class="nav-container">
            <a href="{home}" class="nav-logo">
                <img src="{root}icon.png" alt="" class="logo-mark" width="26" height="26">
                <span class="logo-text">Offgrid Media</span>
            </a>
            <ul class="nav-menu" id="navMenu">
                {links}
                <li><a href="{back}" class="nav-link back-to-main">&#8592; lorenzmaierhofer.com</a></li>
            </ul>
            <div class="nav-social">
                <div class="ogm-lang-switcher">
                    <select class="lang-select" aria-label="Language" onchange="localStorage.setItem('langChosen','1');window.location.href=this.value">
                        {sel}
                    </select>
                </div>
                <button class="theme-toggle" id="themeToggle" aria-label="{e(t["theme_toggle"])}">
                    {THEME_SVG}
                </button>
            </div>
            <button class="hamburger" id="hamburgerToggle" aria-label="{e(t["nav_toggle"])}" aria-expanded="false">
                <span class="ham-bar"></span><span class="ham-bar"></span><span class="ham-bar"></span>
            </button>
        </div>
    </nav>'''


def footer(loc, t, root):
    home = "/offgridmedia/" if loc == "en" else f"/offgridmedia/{loc}/"
    return f'''<footer class="ogm-footer">
        <div class="ogm-footer-inner">
            <div class="ogm-footer-brand">
                <img src="{root}icon.png" alt="" width="30" height="30">
                <span>Offgrid Media<small>{e(t["subtitle"])}</small></span>
            </div>
            <nav class="ogm-footer-links" aria-label="{e(t["footer_nav"])}">
                <a href="{home}privacy">{e(t["nav_privacy"])}</a>
                <a href="/offgridmedia/llms.txt">llms.txt</a>
                <a href="{"/de/" if loc == "de" else "/zh/" if loc == "zh" else "/"}">lorenzmaierhofer.com</a>
            </nav>
        </div>
    </footer>'''


def head(loc, t, root, site, page):
    """page: 'index' | 'privacy'"""
    hl, og, direction = LOCALES[loc][2], LOCALES[loc][3], LOCALES[loc][4]
    if page == "index":
        url = "https://lorenzmaierhofer.com/offgridmedia/" if loc == "en" else f"https://lorenzmaierhofer.com/offgridmedia/{loc}/"
        title, desc = t["meta_title"], t["meta_desc"]
        ogt, ogd = t["og_title"], t["og_desc"]
        suffix = ""
        extra = f'<meta name="keywords" content="{e(t["keywords"])}">'
    else:
        url = ("https://lorenzmaierhofer.com/offgridmedia/privacy" if loc == "en"
               else f"https://lorenzmaierhofer.com/offgridmedia/{loc}/privacy")
        title, desc = t["privacy_title"], t["privacy_desc"]
        ogt, ogd = t["privacy_title"], t["privacy_desc"]
        suffix = "privacy"
        extra = ""
    return f'''    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/png" href="/offgridmedia/icon.png">
    <title>{e(title)}</title>

    <meta name="description" content="{e(desc)}">
    {extra}
    <meta name="author" content="Lorenz Maierhofer">
    <meta name="robots" content="index, follow">

    <meta property="og:type" content="{'website' if page == 'index' else 'article'}">
    <meta property="og:title" content="{e(ogt)}">
    <meta property="og:description" content="{e(ogd)}">
    <meta property="og:image" content="https://lorenzmaierhofer.com/offgridmedia/og-offgridmedia.jpg">
    <meta property="og:image:alt" content="{e(t["og_image_alt"])}">
    <meta property="og:locale" content="{og}">
    <meta property="og:url" content="{url}">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{e(ogt)}">
    <meta name="twitter:description" content="{e(ogd)}">
    <meta name="twitter:image" content="https://lorenzmaierhofer.com/offgridmedia/og-offgridmedia.jpg">

    <link rel="canonical" href="{url}">
    {hreflangs(suffix)}
'''


def jsonld(loc, t, copy):
    import json
    url = "https://lorenzmaierhofer.com/offgridmedia/" if loc == "en" else f"https://lorenzmaierhofer.com/offgridmedia/{loc}/"
    app = {
        "@context": "https://schema.org",
        "@type": "MobileApplication",
        "name": "Offgrid Media",
        "alternateName": f"Offgrid Media – {copy['subtitle']}",
        "applicationCategory": "EntertainmentApplication",
        "applicationSubCategory": "Media Library",
        "operatingSystem": "iOS 16.1 or later",
        "softwareVersion": "1.0",
        "description": copy["lede"],
        "image": "https://lorenzmaierhofer.com/offgridmedia/icon.png",
        "screenshot": f"https://lorenzmaierhofer.com/offgridmedia/screenshots/{loc}/iphone-01_library.webp",
        "url": url,
        "offers": {
            "@type": "Offer", "price": "0", "priceCurrency": t["currency"],
            "availability": "https://schema.org/PreOrder",
            "seller": {"@type": "Organization", "name": "Apple App Store"},
        },
        "author": {"@type": "Person", "name": "Lorenz Maierhofer", "url": "https://lorenzmaierhofer.com"},
        "featureList": [b[0] for b in copy["blocks"]],
        "keywords": copy["keywords"],
        "contentRating": "4+",
        "inLanguage": LOCALES[loc][2],
        "isFamilyFriendly": True,
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in t["faq"]
        ],
    }
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Lorenz Maierhofer", "item": "https://lorenzmaierhofer.com/"},
            {"@type": "ListItem", "position": 2, "name": "Offgrid Media", "item": url},
        ],
    }
    dump = lambda o: json.dumps(o, ensure_ascii=False, indent=8)
    return "\n".join(f'    <script type="application/ld+json">\n{dump(o)}\n    </script>\n' for o in (app, faq, crumbs))


def build_index(loc):
    t = STRINGS[loc]
    copy = app_copy(loc)
    t = dict(t, subtitle=copy["subtitle"], keywords=copy["keywords"])
    fr = framing(loc)
    root = "./" if loc == "en" else "../"
    site = "../" if loc == "en" else "../../"
    lang, direction = LOCALES[loc][2], LOCALES[loc][4]
    dir_attr = ' dir="rtl"' if direction == "rtl" else ""

    steps = "\n".join(
        f'''                    <div class="ogm-step ogm-reveal">
                        <span class="ogm-step-n">0{i + 1}</span>
                        <h3>{e(fr[key])}</h3>
                    </div>''' for i, key in enumerate(["02_import", "03_folders", "04_player"]))

    features = "\n".join(
        f'''                    <div class="ogm-feature ogm-reveal">
                        <span class="ogm-feature-icon" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{FEATURE_ICONS[i]}</svg></span>
                        <h3>{e(head_)}</h3>
                        <p>{e(body)}</p>
                    </div>''' for i, (head_, body) in enumerate(copy["blocks"]))

    def shots(device, w, h):
        return "\n".join(
            f'                    <img src="{root}screenshots/{loc}/{device}-{s}.webp" alt="{e(fr[s])}" loading="lazy" width="{w}" height="{h}">'
            for s in SHOTS)

    privacy_items = "\n".join(
        f'''                    <div class="ogm-privacy-item ogm-reveal">
                        <strong>{e(ti)}</strong>
                        <span>{e(bo)}</span>
                    </div>''' for ti, bo in t["privacy_items"])

    faq_items = "\n".join(
        f'''                    <div class="ogm-faq-item">
                        <button class="ogm-faq-q" aria-expanded="false">{e(q)}<span class="ogm-faq-icon" aria-hidden="true">+</span></button>
                        <div class="ogm-faq-a"><p>{e(a)}</p></div>
                    </div>''' for q, a in t["faq"])

    h1_main, _, h1_accent = t["h1"].partition("|")
    home = "/offgridmedia/" if loc == "en" else f"/offgridmedia/{loc}/"
    video = f'''<video autoplay muted loop playsinline preload="metadata" poster="{root}preview-poster.webp"
                               aria-label="{e(t["video_label"])}">
                            <source src="{root}preview.mp4" type="video/mp4">
                        </video>''' if loc == "en" else (
        f'<img src="{root}screenshots/{loc}/iphone-01_library.webp" alt="{e(fr["01_library"])}" width="660" height="1434">')

    return f'''<!DOCTYPE html>
<html lang="{lang}"{dir_attr}>
<head>
{head(loc, t, root, site, "index")}
{jsonld(loc, t, copy)}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{site}styles.css">
    <link rel="stylesheet" href="{root}offgridmedia-styles.css">
</head>
<body>
    {nav(loc, t, root, "index")}

    <main class="main-content">

        <section class="ogm-hero">
            <div class="ogm-grid" aria-hidden="true"></div>
            <div class="ogm-hero-inner">
                <div class="ogm-hero-copy">
                    <p class="ogm-eyebrow">Offgrid Media &middot; {e(copy["subtitle"])}</p>
                    <h1>{e(h1_main)}<br><em>{e(h1_accent)}</em></h1>
                    <p class="ogm-lede">{e(copy["lede"])}</p>

                    <div class="ogm-cta-row">
                        <span class="ogm-soon" data-live-label="{e(t["cta_live"])}">
                            {APPLE_SVG}
                            <span><b>{e(t["cta_soon"])}</b><small>{e(t["cta_meta"])}</small></span>
                        </span>
                        <a href="#how" class="ogm-btn ogm-btn-ghost">{e(t["cta_secondary"])}</a>
                    </div>

                    <div class="ogm-switch-row">
                        <button class="ogm-switch" id="ogmSwitch" aria-pressed="true"
                                data-label-offline="{e(t["switch_off"])}" data-label-online="{e(t["switch_on"])}">
                            <span class="ogm-switch-track"><span class="ogm-switch-knob"></span></span>
                            <span class="ogm-switch-text">{e(t["switch_off"])}</span>
                        </button>
                        <p class="ogm-switch-hint" id="ogmSwitchHint"
                           data-hint-offline="{e(t["hint_off"])}"
                           data-hint-online="{e(t["hint_on"])}">{e(t["hint_off"])}</p>
                    </div>
                </div>

                <div class="ogm-stage">
                    <div class="ogm-phone">
                        {video}
                    </div>
                    <div class="ogm-readout" aria-hidden="true">
                        <div class="ogm-chip ogm-chip-network">
                            <span class="ogm-chip-label">{e(t["chip_network"])}</span>
                            <span class="ogm-chip-value ogm-offline-only"><span class="ogm-dot ogm-dot-dead"></span>{e(t["chip_no_conn"])}</span>
                            <span class="ogm-chip-value ogm-online-only"><span class="ogm-dot ogm-dot-dead"></span>{e(t["chip_conn"])}</span>
                        </div>
                        <div class="ogm-chip">
                            <span class="ogm-chip-label">{e(t["chip_library"])}</span>
                            <span class="ogm-chip-value"><span class="ogm-dot ogm-dot-live"></span>{e(t["chip_playing"])}</span>
                        </div>
                        <p class="ogm-chip-caption">{e(t["chip_caption"])}</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="ogm-section ogm-section-alt" id="library">
            <div class="ogm-shell">
                <div class="ogm-head ogm-head-center ogm-reveal">
                    <span class="ogm-label">{e(t["lbl_library"])}</span>
                    <h2 class="ogm-h2">{e(t["h2_library"])}</h2>
                    <p class="ogm-sub">{e(t["sub_library"])}</p>
                </div>

                <div class="ogm-device-tabs" role="tablist" aria-label="{e(t["device"])}">
                    <button class="ogm-device-tab active" role="tab" aria-selected="true" data-device="iphone">iPhone</button>
                    <button class="ogm-device-tab" role="tab" aria-selected="false" data-device="ipad">iPad</button>
                </div>

                <div class="ogm-shots" data-device="iphone" role="region" aria-label="iPhone" tabindex="0">
{shots("iphone", 660, 1434)}
                </div>

                <div class="ogm-shots hidden" data-device="ipad" role="region" aria-label="iPad" tabindex="0">
{shots("ipad", 720, 960)}
                </div>
            </div>
        </section>

        <section class="ogm-section" id="how">
            <div class="ogm-shell">
                <div class="ogm-head ogm-reveal">
                    <span class="ogm-label">{e(t["lbl_how"])}</span>
                    <h2 class="ogm-h2">{e(t["h2_how"])}</h2>
                </div>
                <div class="ogm-steps">
{steps}
                </div>
            </div>
        </section>

        <section class="ogm-section ogm-section-alt" id="features">
            <div class="ogm-shell">
                <div class="ogm-head ogm-head-center ogm-reveal">
                    <span class="ogm-label">{e(t["lbl_features"])}</span>
                    <h2 class="ogm-h2">{e(t["h2_features"])}</h2>
                    <p class="ogm-sub">{e(t["sub_features"])}</p>
                </div>
                <div class="ogm-features">
{features}
                </div>
            </div>
        </section>

        <section class="ogm-section">
            <div class="ogm-shell">
                <div class="ogm-stats">
                    <div class="ogm-stat">
                        <span class="ogm-stat-n" data-count="11">11</span>
                        <span class="ogm-stat-l">{e(t["stat_langs"])}</span>
                    </div>
                    <div class="ogm-stat">
                        <span class="ogm-stat-n" data-count="0">0</span>
                        <span class="ogm-stat-l">{e(t["stat_zero"])}</span>
                    </div>
                    <div class="ogm-stat">
                        <span class="ogm-stat-n" data-count="100" data-suffix="%">100%</span>
                        <span class="ogm-stat-l">{e(t["stat_device"])}</span>
                    </div>
                    <div class="ogm-stat">
                        <span class="ogm-stat-n">16.1+</span>
                        <span class="ogm-stat-l">{e(t["stat_ios"])}</span>
                    </div>
                </div>
            </div>
        </section>

        <section class="ogm-section ogm-section-alt" id="privacy">
            <div class="ogm-shell">
                <div class="ogm-head ogm-reveal">
                    <span class="ogm-label">{e(t["nav_privacy"])}</span>
                    <h2 class="ogm-h2">{e(t["h2_privacy"])}</h2>
                    <p class="ogm-sub">{e(t["sub_privacy"])}</p>
                </div>
                <div class="ogm-privacy-grid">
{privacy_items}
                </div>
                <a class="ogm-link" href="{home}privacy">{e(t["privacy_link"])} &rarr;</a>
            </div>
        </section>

        <section class="ogm-section" id="faq">
            <div class="ogm-shell-narrow">
                <div class="ogm-head ogm-reveal">
                    <span class="ogm-label">{e(t["lbl_faq"])}</span>
                    <h2 class="ogm-h2">{e(t["h2_faq"])}</h2>
                </div>
                <div class="ogm-faq">
{faq_items}
                </div>
                <p class="ogm-note" style="margin-top:2.5rem;">{e(copy["rights"])}</p>
            </div>
        </section>

        <section class="ogm-close">
            <h2>{e(t["close_h2"])}</h2>
            <p>{e(t["close_p"])}</p>
            <div class="ogm-cta-row">
                <span class="ogm-soon" data-live-label="{e(t["cta_live"])}">
                    {APPLE_SVG}
                    <span><b>{e(t["cta_soon"])}</b><small>{e(t["cta_meta2"])}</small></span>
                </span>
            </div>
            <p class="ogm-close-meta">{e(t["close_meta"])}</p>
        </section>

    </main>

    {footer(loc, t, root)}

    <script src="{site}script.js"></script>
    <script src="{root}offgridmedia-script.js"></script>
</body>
</html>
'''


def build_privacy(loc):
    t = STRINGS[loc]
    copy = app_copy(loc)
    t = dict(t, subtitle=copy["subtitle"])
    root = "../" if loc == "en" else "../../"
    site = "../../" if loc == "en" else "../../../"
    lang, direction = LOCALES[loc][2], LOCALES[loc][4]
    dir_attr = ' dir="rtl"' if direction == "rtl" else ""
    home = "/offgridmedia/" if loc == "en" else f"/offgridmedia/{loc}/"

    body = []
    for item in t["policy"]:
        kind, text = item[0], item[1:]
        if kind == "h2":
            body.append(f"            <h2>{e(text[0])}</h2>")
        elif kind == "p":
            body.append(f"            <p>{text[0]}</p>")
        elif kind == "ul":
            lis = "\n".join(f"                <li>{x}</li>" for x in text[0])
            body.append(f"            <ul>\n{lis}\n            </ul>")
    body = "\n".join(body)

    return f'''<!DOCTYPE html>
<html lang="{lang}"{dir_attr}>
<head>
{head(loc, t, root, site, "privacy")}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{site}styles.css">
    <link rel="stylesheet" href="{root}offgridmedia-styles.css">
</head>
<body>
    {nav(loc, t, root, "privacy")}

    <main class="main-content ogm-doc">
        <div class="ogm-shell-narrow">
            <h1>{e(t["privacy_h1"])}</h1>
            <p class="ogm-doc-meta">Offgrid Media &middot; {e(t["privacy_updated"])}</p>
{body}
            <p style="margin-top:2.5rem;"><a href="{home}">&larr; {e(t["privacy_back"])}</a></p>
        </div>
    </main>

    {footer(loc, t, root)}

    <script src="{site}script.js"></script>
    <script src="{root}offgridmedia-script.js"></script>
</body>
</html>
'''


if __name__ == "__main__":
    from strings import STRINGS
    for loc in ORDER:
        d = OUT if loc == "en" else f"{OUT}/{loc}"
        os.makedirs(f"{d}/privacy", exist_ok=True)
        with open(f"{d}/index.html", "w", encoding="utf-8") as f:
            f.write(build_index(loc))
        with open(f"{d}/privacy/index.html", "w", encoding="utf-8") as f:
            f.write(build_privacy(loc))
        print(f"built {loc}")
