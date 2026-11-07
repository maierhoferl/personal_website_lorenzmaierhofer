"""Validator self-check: python3 .github/scripts/test_pg_ai_news.py"""
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pg_ai_news import PG_ROLE, find_span, paragraphs, parse_page, validate, with_context  # noqa: E402

TEXT = "\n".join(paragraphs(
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
# transcripts: only P&G speakers are quotable, and quotes are credited to who said them
T = ''.join(f'<div class="text-lg font-bold text-default md:text-xl">{n}</div> <!--[0-->'
            f'<div class="text-sm italic text-muted">{r}</div><p class="text-default mt-2">{x}</p>'
            for n, r, x in [("Ann Analyst", "Analyst, Big Bank", "Is AI driving savings?"),
                            ("Jane Exec", "CFO, Procter &amp; Gamble", "AI cut our planning time in half."),
                            ("Operator", "", "Next question.")])
T += '<script>eventDate:"2026-10-22"</script>'
paras, meta, attribute = parse_page("transcript", T, {})
assert paras == ["AI cut our planning time in half."] and meta["date"] == "2026-10-22"
TC = {**CAND, "url": "https://stockanalysis.com/stocks/pg/transcripts/1-q1-2027/",
      "prefix": "https://stockanalysis.com/stocks/pg/transcripts/"}
TM = {"title": "PG Q1 2027 Earnings Call Transcript", "date": "2026-10-22"}
item, why = validate(TC, TM, {"is_ai": True, "excerpts": ["AI cut our planning time in half."]},
                     "\n".join(paras), set(), TODAY, 60, attribute)
assert item and item["author"] == "Jane Exec, CFO", why
assert not validate(TC, TM, {"is_ai": True, "excerpts": ["Is AI driving savings?"]},
                    "\n".join(paras), set(), TODAY, 60, attribute)[0]  # analyst words

# dangling opener gets the previous sentence of its paragraph; none available -> dropped
CTX = "Old news.\nWe built agent tools for retailers. This is critical as agents shop.\nThis stands alone."
assert with_context("This is critical as agents shop.", CTX) == "We built agent tools for retailers. This is critical as agents shop."
assert with_context("This stands alone.", CTX) is None
assert with_context("We built agent tools for retailers.", CTX) == "We built agent tools for retailers."
import re  # noqa: E402
for role in ("CFO, Procter & Gamble", "CFO, The Procter & Gamble Company", "CEO, P&G"):
    assert re.sub(PG_ROLE, "", role) == role.split(",")[0], role
assert not re.search(PG_ROLE, "Analyst, Barclays")

# ---------- resilience: fetch retries, redirect guard, model fallback ----------
import io, types as _t, urllib.error  # noqa: E401,E402
import pg_ai_news as m  # noqa: E402
m.time.sleep = lambda s: None


class Resp(io.BytesIO):
    def __init__(self, body, url):
        super().__init__(body); self.url = url
        self.headers = _t.SimpleNamespace(get_content_charset=lambda: "utf-8")
    def geturl(self): return self.url
    def __enter__(self): return self
    def __exit__(self, *a): pass


def urlopen_seq(*outcomes):
    it = iter(outcomes)
    def fake(req, timeout):
        o = next(it)
        if isinstance(o, Exception): raise o
        return Resp(b"page", o)
    m.urllib.request.urlopen = fake


U = "https://us.pg.com/blogs/x/"
urlopen_seq(urllib.error.HTTPError(U, 503, "busy", {}, None), TimeoutError(), U)
assert m.fetch(U) == "page"  # two transient failures, then success
urlopen_seq(urllib.error.HTTPError(U, 404, "gone", {}, None))
try: m.fetch(U); raise AssertionError("404 must not retry")
except urllib.error.HTTPError: pass
urlopen_seq("https://evil.example/x")
try: m.fetch(U); raise AssertionError("off-site redirect accepted")
except ValueError: pass


class APIError(Exception):
    def __init__(self, code): super().__init__(f"{code}"); self.code = code


def fake_genai(behaviour):  # behaviour: model -> exception or response text
    calls = []
    class Models:
        def generate_content(self, model, contents, config):
            calls.append(model); b = behaviour[model]
            if isinstance(b, Exception): raise b
            return _t.SimpleNamespace(text=b, model_version=model)
    ns = _t.SimpleNamespace
    gtypes = ns(HttpOptions=lambda **k: None, HttpRetryOptions=lambda **k: None,
                GenerateContentConfig=lambda **k: None)
    genai = ns(Client=lambda **k: ns(models=Models()), types=gtypes, errors=ns(APIError=APIError))
    sys.modules.update({"google": ns(genai=genai), "google.genai": genai})
    return calls


m.MODELS = ["a", "b"]
P = ["We use AI to plan every launch across all categories."]
calls = fake_genai({"a": APIError(503), "b": '{"is_ai": true, "excerpts": ["x", 3]}'})
assert m.select_excerpts(U, P) == {"is_ai": True, "excerpts": ["x"]} and calls == ["a", "b"]
calls = fake_genai({"a": "", "b": '{"is_ai": false, "excerpts": []}'})
assert m.select_excerpts(U, P)["is_ai"] is False and calls == ["a", "b"]  # empty output falls through
calls = fake_genai({"a": APIError(402), "b": "{}"})
try: m.select_excerpts(U, P); raise AssertionError("402 must stop the run")
except m.ModelDown: assert calls == ["a"]
calls = fake_genai({"a": APIError(500), "b": "[]"})
try: m.select_excerpts(U, P); raise AssertionError("bad output accepted")
except ValueError: pass
print("ok")
