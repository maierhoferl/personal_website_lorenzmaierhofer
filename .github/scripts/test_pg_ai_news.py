"""Validator self-check: python3 .github/scripts/test_pg_ai_news.py"""
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pg_ai_news import find_span, paragraphs, validate  # noqa: E402

TEXT = " ".join(paragraphs(
    "<p>As Cohen put it, “AI without data is simply ‘A’…artificial.”</p>"
    "<p>Using AI, they were able to rapidly develop the Pantene Sunkiss Glow Spray,\n"
    "moving from insight to product concept in just days instead of weeks.</p>"))
TODAY = dt.date(2026, 11, 3)
CAND = {"url": "https://us.pg.com/blogs/x/", "prefix": "https://us.pg.com/blogs/",
        "source": "P&G Blog", "channel": "blog"}
META = {"title": "T", "date": "2026-10-20", "author": "Procter & Gamble"}
GOOD = "Using AI, they were able to rapidly develop the Pantene Sunkiss Glow Spray, moving from insight to product concept in just days instead of weeks."


def run(cand=CAND, meta=META, excerpts=(GOOD,), existing=(), max_age=60):
    return validate(cand, meta, {"is_ai": True, "excerpts": list(excerpts)}, TEXT,
                    set(existing), TODAY, max_age)


item, why = run()
assert item and item["excerpts"] == [GOOD], why
# straight quotes from the model map back to the page's curly quotes, page glyphs published
assert find_span('As Cohen put it, "AI', TEXT) == "As Cohen put it, “AI"
assert not run(excerpts=["Using AI, they quickly developed the Pantene Sunkiss Glow Spray."])[0]  # paraphrase
assert not run(excerpts=["Using AI, they were able to ... Glow Spray"])[0]  # elided
assert not run(meta={**META, "author": ""})[0]  # missing metadata
assert not run(cand={**CAND, "url": "https://evil.example/blogs/x/"})[0]  # wrong domain
assert not run(meta={**META, "date": "2026-12-01"})[0]  # future
assert not run(meta={**META, "date": "2026-01-01"})[0]  # too old
assert run(meta={**META, "date": "2026-01-01"}, max_age=None)[0]  # manual seed: no age limit
assert not run(existing=[CAND["url"]])[0]  # duplicate
assert not validate(CAND, META, {"is_ai": False, "excerpts": []}, TEXT, set(), TODAY, 60)[0]
# related-post teaser cards are not part of the article
assert paragraphs('<main><p>Body.</p><a href="/blogs/y/" class="blog-item event_internal_link">'
                  '<p>Teaser about AI.</p></a></main><p>Footer.</p>') == ["Body."]
print("ok")
