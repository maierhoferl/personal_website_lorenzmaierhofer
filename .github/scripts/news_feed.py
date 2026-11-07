#!/usr/bin/env python3
"""Write news.xml (RSS 2.0) from pg_ai_news.json. Run after any change to the JSON."""
import json
from datetime import datetime, timezone
from email.utils import format_datetime
from html import escape
from pathlib import Path
from xml.sax.saxutils import escape as x
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
SITE = "https://lorenzmaierhofer.com"


def rfc822(day: str) -> str:
    return format_datetime(datetime.strptime(day, "%Y-%m-%d").replace(hour=12, tzinfo=timezone.utc))


def build(items: list) -> str:
    items = sorted(items, key=lambda i: (i["date"], i.get("added_on", "")), reverse=True)
    out = []
    for i in items:
        body = "".join(f"<blockquote><p>{escape(e)}</p></blockquote>" for e in i["excerpts"])
        body += f'<p>— {escape(i["author"])}, {escape(i["source"])}. <a href="{escape(i["url"])}">Read the original</a></p>'
        out.append(
            "<item>"
            f"<title>{x(i['title'])}</title>"
            f"<link>{x(i['url'])}</link>"
            f'<guid isPermaLink="true">{x(i["url"])}</guid>'
            f"<pubDate>{rfc822(i['date'])}</pubDate>"
            f"<dc:creator>{x(i['author'])}</dc:creator>"
            f"<category>{x(i['channel'])}</category>"
            f"<description>{x(body)}</description>"
            "</item>"
        )
    last = rfc822(items[0]["date"]) if items else format_datetime(datetime.now(timezone.utc))
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        "<channel>"
        "<title>P&amp;G AI News | Lorenz Maierhofer</title>"
        f"<link>{SITE}/news.html#pg-ai-news</link>"
        f'<atom:link href="{SITE}/news.xml" rel="self" type="application/rss+xml"/>'
        "<description>Excerpts of official P&amp;G references to the impact of AI, "
        "illustrating what P&amp;G&#8217;s AI platform and transformation drive.</description>"
        "<language>en</language>"
        f"<lastBuildDate>{last}</lastBuildDate>\n"
        + "\n".join(out)
        + "\n</channel>\n</rss>\n"
    )


if __name__ == "__main__":
    feed = build(json.loads((ROOT / "pg_ai_news.json").read_text())["items"])
    # self-check: well-formed, one <item> per entry, newest first
    ch = ET.fromstring(feed).find("channel")
    dates = [datetime.strptime(d.text, "%a, %d %b %Y %H:%M:%S %z") for d in ch.iter("pubDate")]
    assert dates == sorted(dates, reverse=True)
    (ROOT / "news.xml").write_text(feed)
    print(f"news.xml: {len(dates)} items")
