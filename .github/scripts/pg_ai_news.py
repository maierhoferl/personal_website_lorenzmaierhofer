#!/usr/bin/env python3
"""Weekly P&G AI News collector.

Finds new pages on the approved official P&G sources (.github/pg_ai_sources.json),
asks Gemini only to *select* verbatim passages about AI, verifies every passage is
an exact span of the source page, and appends passing items to pg_ai_news.json.
Nothing published is written by the model: title/author/date come from page or
filing metadata, excerpts are the matched spans cut from the page text itself.

  python3 pg_ai_news.py                 # weekly run (writes files)
  python3 pg_ai_news.py --dry-run       # print decisions, write nothing
  python3 pg_ai_news.py --manual F.json # {url: [excerpt, ...]}: skip the LLM and
                                        # the age limit, still verified verbatim
"""
import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NEWS = ROOT / "pg_ai_news.json"
SOURCES = ROOT / ".github" / "pg_ai_sources.json"
SEEN = ROOT / ".github" / "pg_ai_news_seen.json"

# Google-maintained alias for the newest Flash release, so model deprecations need no change here.
# Pin a concrete model via repo variable GEMINI_MODEL if the alias ever misbehaves.
MODEL = os.environ.get("GEMINI_MODEL") or "gemini-flash-latest"
MAX_AGE_DAYS = 60
MAX_NEW = 5
MAX_EXCERPT = 600
MAX_PROMPT_CHARS = 60_000
SEC_CIK = "80424"
SEC_AUTHOR = "The Procter & Gamble Company"
WEB_UA = "Mozilla/5.0 (compatible; lorenzmaierhofer.com news-bot)"
# ponytail: SEC rejects a bare domain as User-Agent; " news-bot" passes. Add a
# contact email to SEC_USER_AGENT if SEC ever tightens this.
SEC_UA = (os.environ.get("SEC_USER_AGENT") or "lorenzmaierhofer.com") + " news-bot"
AI_RE = re.compile(
    r"\b(AI|A\.I\.|artificial intelligence|machine learning|generative|GenAI|agentic|"
    r"AI agents?|algorithms?|automat\w+|digitiz\w+|digitaliz\w+|data science|chatPG)\b",
    re.I,
)


# ---------- fetching & parsing ----------

def fetch(url: str) -> str:
    ua = SEC_UA if "sec.gov" in url else WEB_UA
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode(r.headers.get_content_charset() or "utf-8", errors="replace")


def paragraphs(page_html: str) -> list[str]:
    """Visible text, one entry per block element."""
    main = re.search(r"<main\b.*?</main>", page_html, re.S | re.I)
    t = main.group(0) if main else page_html
    # drop "related posts" teaser cards: verbatim, but not part of this article
    t = re.sub(r'<a\b[^>]*class="[^"]*blog-item[^"]*"[^>]*>.*?</a>', " ", t, flags=re.S | re.I)
    t = re.sub(r"<(script|style|noscript|svg|head)\b.*?</\1>", " ", t, flags=re.S | re.I)
    t = re.sub(r"\s+", " ", t)  # source line breaks are not paragraph breaks
    t = re.sub(r"</?(p|div|br|li|h[1-6]|tr|td|section|article|blockquote|figcaption)\b[^>]*>", "\n", t, flags=re.I)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return [p for p in (re.sub(r"\s+", " ", line).strip() for line in t.split("\n")) if p]


def blog_meta(page_html: str) -> dict:
    for block in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', page_html, re.S):
        try:
            d = json.loads(block)
        except ValueError:
            continue
        if d.get("@type") == "BlogPosting":
            author = d.get("author") or {}
            return {
                "title": re.sub(r"\s*\|\s*P&G\s*$", "", d.get("headline", "")).strip(),
                "date": (d.get("datePublished") or "")[:10],
                "author": author.get("name", "") if isinstance(author, dict) else "",
            }
    return {}


def transcript_turns(page_html: str) -> list[tuple[str, str, list[str]]]:
    """(speaker, role, paragraphs) per speaker turn of a StockAnalysis transcript.
    Reads only transcript paragraphs, never the page's generated call summary."""
    name_re = r'<div class="text-lg font-bold text-default md:text-xl">([^<]+)</div>'
    parts = re.split(name_re, page_html)
    turns = []
    for name, seg in zip(parts[1::2], parts[2::2]):
        role = re.search(r'^\s*(?:<!--[^>]*-->\s*)*<div class="text-sm italic text-muted">([^<]*)</div>', seg)
        paras = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", p))).strip()
                 for p in re.findall(r'<p class="text-default[^"]*">(.*?)</p>', seg, re.S)]
        turns.append((html.unescape(name).strip(), html.unescape(role.group(1)).strip() if role else "",
                      [x for x in paras if x]))
    return turns


def transcript_meta(page_html: str) -> dict:
    title = ""
    for block in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', page_html, re.S):
        try:
            d = json.loads(block)
        except ValueError:
            continue
        if d.get("@type") == "WebPage":
            title = re.sub(r"\s*&\s*Audio\s*$", "", d.get("name", "")).strip()
    # StockAnalysis names AGMs and conferences "FY 2026 Earnings Call Transcript"; the h1 has the event
    h1 = re.search(r"<h1[^>]*>([^<]+)</h1>", page_html)
    if h1 and re.search(r"\bFY \d{4} Earnings Call\b", title):
        title = f"Procter & Gamble (PG) Transcript: {html.unescape(h1.group(1)).strip()}"
    m = re.search(r'eventDate:"(\d{4}-\d{2}-\d{2})"', page_html)
    return {"title": title, "date": m.group(1) if m else ""}


PG_ROLE = r",?\s*(?:The )?(?:Procter & Gamble|P&G)(?: Company)?$"


def parse_page(kind: str, page: str, cand: dict) -> tuple[list[str], dict, object]:
    """-> (paragraphs eligible for quoting, metadata, attribute(spans) or None)."""
    if kind != "transcript":
        return paragraphs(page), cand.get("meta") or blog_meta(page), None
    # P&G executives only: analysts and the operator are never quoted
    # roles end ", Procter & Gamble", ", The Procter & Gamble Company" or ", P&G"
    pg_role = PG_ROLE
    turns = [t for t in transcript_turns(page) if re.search(pg_role, t[1])]

    def attribute(spans: list[str]) -> str:
        names = []
        for sp in spans:
            who = next((f"{n}, {re.sub(pg_role, '', r)}" for n, r, ps in turns
                        if find_span(sp, " ".join(ps))), None)
            if not who:
                return ""  # excerpt crosses speaker turns: cannot attribute it
            names.append(who)
        return "; ".join(dict.fromkeys(names))

    return [p for _, _, ps in turns for p in ps], transcript_meta(page), attribute


# ---------- collectors (one per source type) ----------

def collect_pg_blog(src: dict, cutoff: dt.date) -> list[dict]:
    index = fetch(src["url"])
    out = []
    pat = r'<a href="(/blogs/[^"]+/)"[^>]*class="blog-item[ "](?:(?!</a>).)*?blog-item__date">(\d{1,2}/\d{1,2}/\d{4})<'
    for path, mdy in re.findall(pat, index, re.S):
        if dt.datetime.strptime(mdy, "%m/%d/%Y").date() >= cutoff:
            out.append({"url": "https://us.pg.com" + path})
    return out


def collect_sec(src: dict, cutoff: dt.date) -> list[dict]:
    recent = json.loads(fetch(src["url"]))["filings"]["recent"]
    out = []
    for form, filed, acc, primary, items in zip(
        recent["form"], recent["filingDate"], recent["accessionNumber"],
        recent["primaryDocument"], recent["items"]
    ):
        if dt.date.fromisoformat(filed) < cutoff:
            continue
        is_8k = form == "8-K" and any(i in items for i in ("2.02", "7.01", "8.01"))
        if not (is_8k or form == "10-K"):
            continue
        base = f"https://www.sec.gov/Archives/edgar/data/{SEC_CIK}/{acc.replace('-', '')}/"
        names = [primary] if form == "10-K" else [
            x["name"] for x in json.loads(fetch(base + "index.json"))["directory"]["item"]
            if re.search(r"ex(hibit)?-?99", x["name"], re.I) and x["name"].lower().endswith(".htm")
        ]
        for name in names:
            label = "Annual Report" if form == "10-K" else "Exhibit 99"
            out.append({"url": base + name, "meta": {
                "title": f"P&G Form {form}, {label} (filed {filed})",
                "date": filed, "author": SEC_AUTHOR}})
    return out


def collect_transcripts(src: dict, cutoff: dt.date) -> list[dict]:
    """Quarterly earnings calls only (no AGM/conference talks), newest first; the call
    date is on the transcript page, so cap to the newest few to save model quota."""
    index = fetch(src["url"])
    links = sorted(set(re.findall(r'href="(/stocks/pg/transcripts/(\d+)-q[1-4]-\d{4}/)"', index)),
                   key=lambda x: int(x[1]), reverse=True)
    return [{"url": "https://stockanalysis.com" + path} for path, _ in links[:4]]


COLLECTORS = {"pg-blog": collect_pg_blog, "sec-edgar": collect_sec, "transcript": collect_transcripts}


# ---------- LLM: select, never write ----------

SCHEMA = {
    "type": "object",
    "properties": {
        "is_ai": {"type": "boolean"},
        "excerpts": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["is_ai", "excerpts"],
    "additionalProperties": False,
}

RULES = {
    "page": ("one official Procter & Gamble page",
             "artificial intelligence (AI, machine learning, generative or agentic AI, AI-driven "
             "automation) is a core message of this page, not a passing mention, a list of "
             "buzzwords, or legal/risk-factor boilerplate"),
    "transcript": ("the remarks of P&G executives on a quarterly earnings call",
                   "the executives make at least one substantive statement about artificial "
                   "intelligence (AI, machine learning, generative or agentic AI, AI-driven "
                   "automation): what P&G does with it or what it delivers, not a passing mention"),
}

PROMPT = """You curate a "P&G AI News" list on a personal website. Below are numbered \
paragraphs from {what} ({url}).

1. Set is_ai to true only if {rule}.
2. If is_ai is true, choose 1 to 3 passages that best carry the AI message, preferring \
statements by named P&G leaders and concrete outcomes. Copy each passage character for \
character from a single paragraph: whole sentences, no ellipses, no merging, no \
rewording, no added words, at most {max_chars} characters each. Each passage must make \
sense on its own to a reader who sees nothing else from the page: do not start with \
words like "This", "That", "These", "It" or "They" that point back to an earlier \
sentence. Pick a passage that names its subject, or start one sentence earlier; keep \
passages short.
3. If is_ai is false, return an empty excerpts list.

Paragraphs:
{paras}"""


def select_excerpts(url: str, paras: list[str], kind: str = "page") -> dict:
    from google import genai  # only needed for live runs
    from google.genai import types

    hits = [p for p in paras if AI_RE.search(p) and len(p) > 40]
    if not hits:
        return {"is_ai": False, "excerpts": [], "no_call": True}
    body, used = [], 0
    for i, p in enumerate(hits, 1):
        if used + len(p) > MAX_PROMPT_CHARS:
            break  # ponytail: keyword paragraphs only, capped; enough for blog posts and 8-K exhibits
        body.append(f"[{i}] {p}")
        used += len(p)
    # reads GEMINI_API_KEY; free tier often answers 503 "high demand", so back off and retry
    client = genai.Client(http_options=types.HttpOptions(timeout=120_000, retry_options=types.HttpRetryOptions(
        attempts=6, initial_delay=10, max_delay=120, http_status_codes=[429, 500, 503, 504])))
    resp = client.models.generate_content(
        model=MODEL,
        contents=PROMPT.format(what=RULES[kind][0], rule=RULES[kind][1], url=url,
                               max_chars=MAX_EXCERPT, paras="\n\n".join(body)),
        config=types.GenerateContentConfig(
            response_mime_type="application/json", response_json_schema=SCHEMA),
    )
    print(f"  model: {resp.model_version}")  # what the alias resolved to
    if not resp.text:  # blocked or empty: treat as not publishable
        return {"is_ai": False, "excerpts": []}
    return json.loads(resp.text)


# ---------- validation (deterministic; the real safety net) ----------

QUOTES = "\"'‘’“”«»"
DASHES = "-‐‑‒–—"


def find_span(excerpt: str, text: str) -> str | None:
    """Return the exact substring of `text` that `excerpt` denotes, tolerating only
    whitespace and quote/dash glyph differences. The returned span is published."""
    parts = []
    for ch in excerpt.strip():
        if ch.isspace():
            if parts and parts[-1] != r"\s+":
                parts.append(r"\s+")
        elif ch in QUOTES:
            parts.append(f"[{re.escape(QUOTES)}]")
        elif ch in DASHES:
            parts.append(f"[{re.escape(DASHES)}]")
        else:
            parts.append(re.escape(ch))
    m = re.search("".join(parts), text) if parts else None
    return m.group(0) if m else None


# Opening words that point back to an earlier sentence the reader cannot see.
DANGLING_RE = re.compile(
    r"(?:This|That|These|Those|It|Its|They|Their|Such|He|She|Here|Both|And|But|So|Also)\b")


def with_context(span: str, text: str) -> str | None:
    """If `span` opens by pointing back ("This is critical..."), prepend the previous
    sentence of the same paragraph (paragraphs are "\n"-separated in `text`). Still one
    contiguous, verbatim span. None if there is no such sentence or it stays dangling."""
    for _ in range(2):  # ponytail: at most two sentences of lead-in, then give up
        if not DANGLING_RE.match(span):
            return span
        i = text.find(span)
        before = text[text.rfind("\n", 0, i) + 1:i]
        ends = list(re.finditer(r'[.!?][\"”’)]?\s+(?=\S)', before.rstrip() + " "))
        if not before.strip():
            return None
        start = ends[-2].end() if len(ends) > 1 else 0
        span = before[start:] + span
    return None if DANGLING_RE.match(span) else span


def validate(cand: dict, meta: dict, picked: dict, text: str, existing: set,
             today: dt.date, max_age: int | None, attribute=None) -> tuple[dict | None, str]:
    url = cand["url"]
    if not url.startswith("https://") or not url.startswith(cand["prefix"]):
        return None, "url outside approved prefix"
    if url in existing:
        return None, "duplicate url"
    if not picked.get("is_ai"):
        return None, "not AI-focused"
    excerpts = picked.get("excerpts") or []
    if not 1 <= len(excerpts) <= 3:
        return None, f"{len(excerpts)} excerpts"
    spans = []
    for e in excerpts:
        if len(e) > MAX_EXCERPT or "..." in e or "…" in e:
            return None, "excerpt too long or elided"
        span = find_span(e, text)
        if not span:
            return None, f"excerpt not verbatim: {e[:60]!r}"
        span = with_context(span, text)  # dangling excerpt without context: dropped
        if span and len(span) <= MAX_EXCERPT:
            spans.append(span)
    if not spans:
        return None, "no excerpt makes sense on its own"
    if attribute:  # transcripts: author is whoever spoke the quoted words
        meta = {**meta, "author": attribute(spans)}
    if not all(meta.get(k) for k in ("title", "date", "author")):
        return None, "missing title/date/author metadata"
    try:
        date = dt.date.fromisoformat(meta["date"])
    except ValueError:
        return None, f"bad date {meta['date']!r}"
    if date > today or (max_age is not None and (today - date).days > max_age):
        return None, f"date {date} out of range"
    return {
        "date": date.isoformat(), "title": meta["title"], "excerpts": spans,
        "source": cand["source"], "author": meta["author"], "channel": cand["channel"],
        "url": url, "added": cand.get("added", "auto"), "added_on": today.isoformat(),
    }, "ok"


# ---------- main ----------

def load(path: Path, default):
    return json.loads(path.read_text()) if path.exists() else default


def summary(line: str):
    print(line)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
            f.write(line + "\n")


def report(items: list[dict]) -> str:
    """Markdown listing exactly what was published (emailed via a GitHub issue)."""
    out = [f"The weekly run published {len(items)} new item(s) to "
           "https://lorenzmaierhofer.com/news.html\n"]
    for i in items:
        out.append(f"### [{i['title']}]({i['url']})\n"
                   f"{i['date']} · {i['source']} · {i['author']}\n")
        out += [f"> {x}\n" for x in i["excerpts"]]
    out.append("---\nTo take an item down: delete it from `pg_ai_news.json`, add its URL to "
               "`rejected` in `.github/pg_ai_news_seen.json`, push.")
    # zero-width space after "@" so quoted handles/emails never ping GitHub users
    return "\n".join(out).replace("@", "@\u200b")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--manual", type=Path, help="JSON {url: [excerpts]} picked by a human")
    args = ap.parse_args()

    sources = load(SOURCES, {"sources": []})["sources"]
    news = load(NEWS, {"items": []})
    seen = load(SEEN, {"rejected": {}, "errors": {}})
    existing = {i["url"] for i in news["items"]}
    today = dt.date.today()
    cutoff = today - dt.timedelta(days=MAX_AGE_DAYS)

    manual = json.loads(args.manual.read_text()) if args.manual else None
    cands = []
    if manual:
        for url in manual:
            src = next((s for s in sources if url.startswith(s["allowed_url_prefix"])), None)
            if not src:
                summary(f"- REJECT {url}: not under an approved source")
                continue
            cands.append({"url": url, "src": src, "added": "manual"})
    else:
        for src in sources:
            try:
                found = COLLECTORS[src["type"]](src, cutoff)
                seen["errors"][src["id"]] = 0
            except Exception as e:  # one broken source must not stop the others
                seen["errors"][src["id"]] = seen["errors"].get(src["id"], 0) + 1
                summary(f"- WARN source {src['id']}: {e}")
                continue
            cands += [dict(c, src=src) for c in found
                      if c["url"] not in existing and c["url"] not in seen["rejected"]]

    added, model_ok, model_failed = [], 0, 0
    for c in cands:
        if not manual and len(added) >= MAX_NEW:
            break
        src = c["src"]
        c.update(prefix=src["allowed_url_prefix"], source=src["name"], channel=src["channel"])
        if src["type"] == "transcript" and not re.search(r"-q[1-4]-\d{4}/$", c["url"]):
            # AGM / investor conference (manual runs only; the collector takes quarterly calls)
            c.update(channel="investor-event",
                     source="Investor event transcript (StockAnalysis, data by Quartr)")
        try:
            page = fetch(c["url"])
        except Exception as e:
            summary(f"- SKIP {c['url']}: fetch failed ({e})")
            continue
        kind = "transcript" if src["type"] == "transcript" else "page"
        paras, meta, attribute = parse_page(kind, page, c)
        text = "\n".join(paras)  # "\n" marks paragraph ends for with_context
        if not manual and meta.get("date") and meta["date"] < cutoff.isoformat():
            seen["rejected"][c["url"]] = f"{today}: date {meta['date']} too old"
            summary(f"- REJECT {c['url']}: date {meta['date']} too old (no model call)")
            continue
        try:
            picked = ({"is_ai": True, "excerpts": manual[c["url"]]} if manual
                      else select_excerpts(c["url"], paras, kind))
            model_ok += not picked.get("no_call")
        except Exception as e:  # quota/API error: not marked seen, retried next run
            model_failed += 1
            summary(f"- SKIP {c['url']}: model call failed ({str(e)[:200]})")
            continue
        item, why = validate(c, meta, picked, text, existing, today,
                             None if manual else MAX_AGE_DAYS, attribute)
        if item:
            added.append(item)
            existing.add(item["url"])
            summary(f"- ADD {item['date']} {item['title']} ({item['url']})")
        else:
            seen["rejected"][c["url"]] = f"{today}: {why}"
            summary(f"- REJECT {c['url']}: {why}")

    summary(f"{len(added)} item(s) added.")
    if not args.dry_run:
        if added:
            news["items"] = sorted(news["items"] + added, key=lambda i: i["date"], reverse=True)
            NEWS.write_text(json.dumps(news, indent=2, ensure_ascii=False) + "\n")
            if os.environ.get("PG_NEWS_REPORT"):  # body of the notification issue
                Path(os.environ["PG_NEWS_REPORT"]).write_text(report(added))
        if not manual:
            SEEN.write_text(json.dumps(seen, indent=2, ensure_ascii=False) + "\n")
    if model_failed and not model_ok:
        summary("FAIL: every model call failed (check GEMINI_API_KEY / GEMINI_MODEL / quota)")
        return 1
    broken = [k for k, v in seen["errors"].items() if v >= 2]
    if broken:
        summary(f"FAIL: sources erroring two runs in a row: {', '.join(broken)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
