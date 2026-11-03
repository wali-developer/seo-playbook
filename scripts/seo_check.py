#!/usr/bin/env python3
"""On-page SEO check of the raw HTML a crawler receives (stdlib only).

Usage:
  seo_check.py URL [URL ...]
  seo_check.py --sitemap https://example.com/sitemap.xml [--limit 100]
  seo_check.py --file built.html --url https://example.com/page   # check a local build output
  options: --ua googlebot|browser|"custom UA"   --json

Reports status, redirects, title/description length, canonical, robots meta and
X-Robots-Tag, H1 count, visible word count, JSON-LD types, OG tags, internal link
count, and flags common problems.
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

UAS = {
    "googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "browser": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0 Safari/537.36",
}

TITLE_MAX = 60
DESC_MIN, DESC_MAX = 110, 160
THIN_WORDS = 300
# Elements that separate words visually; without a space, "Tools<br>Built" reads as "ToolsBuilt".
BLOCK_TAGS = {"br", "p", "div", "li", "td", "th", "tr", "section", "article",
              "h1", "h2", "h3", "h4", "h5", "h6", "header", "footer", "nav", "main"}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self._in_title = False
        self.metas = []
        self.links = []
        self.h1s = []
        self._h1_depth = 0
        self._h1_buf = []
        self.headings = []
        self.anchors = []
        self.jsonld = []
        self._script_type = None
        self._script_buf = []
        self._skip = 0
        self.text = []
        self.main_text = []
        self._main_depth = 0
        self.html_lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in BLOCK_TAGS:
            self.handle_data(" ")
        if tag == "html":
            self.html_lang = a.get("lang")
        elif tag == "title" and self.title is None:
            self._in_title = True
            self.title = ""
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag == "a" and a.get("href"):
            self.anchors.append(a)
        elif tag == "script":
            self._script_type = (a.get("type") or "").lower()
            self._script_buf = []
            self._skip += 1
        elif tag in ("style", "noscript", "template", "svg"):
            self._skip += 1
        elif tag == "main":
            self._main_depth += 1
        if tag == "h1":
            self._h1_depth += 1
            self._h1_buf = []
        if tag in ("h1", "h2", "h3"):
            self.headings.append([tag, ""])

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script":
            if self._script_type == "application/ld+json":
                self.jsonld.append("".join(self._script_buf))
            self._script_type = None
            self._skip = max(0, self._skip - 1)
        elif tag in ("style", "noscript", "template", "svg"):
            self._skip = max(0, self._skip - 1)
        elif tag == "main":
            self._main_depth = max(0, self._main_depth - 1)
        elif tag == "h1" and self._h1_depth:
            self._h1_depth -= 1
            self.h1s.append(" ".join("".join(self._h1_buf).split()))

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._script_type is not None:
            self._script_buf.append(data)
            return
        if self._skip:
            return
        self.text.append(data)
        if self._main_depth:
            self.main_text.append(data)
        if self._h1_depth:
            self._h1_buf.append(data)
        if self.headings:
            self.headings[-1][1] += data


def fetch(url, ua):
    hops = []
    opener = urllib.request.build_opener(NoRedirect)
    current = url
    for _ in range(10):
        req = urllib.request.Request(current, headers={"User-Agent": ua, "Accept": "text/html,*/*"})
        try:
            resp = opener.open(req, timeout=30)
            body = resp.read().decode(resp.headers.get_content_charset() or "utf-8", "replace")
            return resp.status, dict(resp.headers), body, hops, current
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308) and e.headers.get("Location"):
                nxt = urljoin(current, e.headers["Location"])
                hops.append((e.code, nxt))
                current = nxt
                continue
            body = e.read().decode("utf-8", "replace")
            return e.code, dict(e.headers), body, hops, current
    return None, {}, "", hops, current


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def meta(p, *, name=None, prop=None):
    for m in p.metas:
        if name and (m.get("name") or "").lower() == name:
            return m.get("content")
        if prop and (m.get("property") or "").lower() == prop:
            return m.get("content")
    return None


def jsonld_types(blocks):
    types, errors = [], 0

    def walk(node):
        if isinstance(node, dict):
            t = node.get("@type")
            if t:
                types.extend(t if isinstance(t, list) else [t])
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    for b in blocks:
        try:
            walk(json.loads(b))
        except json.JSONDecodeError:
            errors += 1
    top = [t for t in types if t not in ("ListItem", "Offer", "EntryPoint", "Answer", "Question",
                                         "ContactPoint", "ImageObject", "PropertyValueSpecification")]
    return sorted(set(top)), errors


def analyse(url, status, headers, body, hops, final_url):
    p = PageParser()
    p.feed(body)
    words = len(" ".join(p.text).split())
    main_words = len(" ".join(p.main_text).split())
    canonical = next((l.get("href") for l in p.links if "canonical" in (l.get("rel") or "").lower()), None)
    hreflangs = [l.get("hreflang") for l in p.links if l.get("hreflang")]
    robots = meta(p, name="robots")
    xrobots = next((v for k, v in headers.items() if k.lower() == "x-robots-tag"), None)
    desc = meta(p, name="description")
    title = " ".join((p.title or "").split()) or None
    types, ld_errors = jsonld_types(p.jsonld)
    host = urlparse(final_url).netloc
    internal = {urljoin(final_url, a["href"]).split("#")[0] for a in p.anchors
                if urlparse(urljoin(final_url, a["href"])).netloc == host}

    flags = []
    if status != 200:
        flags.append(f"status {status}")
        if status and status >= 400:
            # An error page only needs its status checked; content checks would be noise.
            return result(url, final_url, status, hops, title, desc, p, canonical, robots, xrobots,
                          hreflangs, words, main_words, internal, types, flags)
    if len(hops) > 1:
        flags.append(f"redirect chain ({len(hops)} hops)")
    if not title:
        flags.append("missing <title>")
    elif len(title) > TITLE_MAX:
        flags.append(f"title {len(title)} chars (> {TITLE_MAX}, will truncate)")
    if not desc:
        flags.append("missing meta description")
    elif not DESC_MIN <= len(desc) <= DESC_MAX:
        flags.append(f"description {len(desc)} chars (aim {DESC_MIN}-{DESC_MAX})")
    if len(p.h1s) != 1:
        flags.append(f"{len(p.h1s)} H1 elements (want 1)")
    if not canonical:
        flags.append("no canonical")
    elif canonical.rstrip("/") != final_url.split("?")[0].split("#")[0].rstrip("/"):
        flags.append(f"canonical points elsewhere: {canonical}")
    noindex = any("noindex" in (v or "").lower() for v in (robots, xrobots))
    if noindex:
        flags.append("NOINDEX")
    if words < THIN_WORDS:
        flags.append(f"only {words} visible words in server HTML")
    if p.main_text and main_words < 50:
        flags.append(f"<main> has only {main_words} words (client-rendered or loading state?)")
    if re.search(r"<main[^>]*>\s*(<[^>]+>\s*)*Loading", body, re.I):
        flags.append('"Loading" placeholder inside <main>')
    hidden = len(re.findall(r"opacity:\s*0(?![.\d])", body))
    if re.search(r"<h1[^>]*style=\"[^\"]*opacity:\s*0(?![.\d])", body):
        flags.append("H1 server-rendered with opacity:0 (entrance animation hides it until hydration)")
    elif hidden >= 10:
        flags.append(f"{hidden} elements server-rendered with opacity:0 (entrance animations?)")
    if ld_errors:
        flags.append(f"{ld_errors} invalid JSON-LD block(s)")
    if re.search(r"not found|page doesn.t exist|404", title or "", re.I) and status == 200:
        flags.append("SOFT 404: not-found title with status 200")
    if not meta(p, prop="og:image"):
        flags.append("no og:image")
    if not p.html_lang:
        flags.append("no <html lang>")

    return result(url, final_url, status, hops, title, desc, p, canonical, robots, xrobots,
                  hreflangs, words, main_words, internal, types, flags)


def result(url, final_url, status, hops, title, desc, p, canonical, robots, xrobots,
           hreflangs, words, main_words, internal, types, flags):
    return {
        "url": url,
        "final_url": final_url,
        "status": status,
        "redirects": hops,
        "title": title,
        "title_len": len(title or ""),
        "description": desc,
        "description_len": len(desc or ""),
        "h1": p.h1s,
        "h2_count": sum(1 for h in p.headings if h[0] == "h2"),
        "canonical": canonical,
        "robots_meta": robots,
        "x_robots_tag": xrobots,
        "hreflang": hreflangs,
        "visible_words": words,
        "main_words": main_words,
        "internal_links": len(internal),
        "jsonld_types": types,
        "og_title": meta(p, prop="og:title"),
        "og_image": meta(p, prop="og:image"),
        "flags": flags,
    }


def sitemap_urls(url, ua, limit):
    _, _, body, _, _ = fetch(url, ua)
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body)
    if "<sitemapindex" in body:
        out = []
        for child in locs:
            out += sitemap_urls(child, ua, limit - len(out))
            if len(out) >= limit:
                break
        return out[:limit]
    return locs[:limit]


def print_report(r):
    print(f"\n== {r['url']}")
    if r["redirects"]:
        for code, to in r["redirects"]:
            print(f"   {code} -> {to}")
    print(f"   status {r['status']} | words {r['visible_words']} (main {r['main_words']}) | "
          f"internal links {r['internal_links']} | H2s {r['h2_count']}")
    print(f"   title ({r['title_len']}): {r['title']}")
    print(f"   desc  ({r['description_len']}): {r['description']}")
    print(f"   h1: {r['h1']}")
    print(f"   canonical: {r['canonical']} | robots: {r['robots_meta']} | x-robots: {r['x_robots_tag']}")
    print(f"   json-ld: {', '.join(r['jsonld_types']) or '-'} | og:image: {'yes' if r['og_image'] else 'no'}"
          + (f" | hreflang: {', '.join(r['hreflang'])}" if r["hreflang"] else ""))
    for f in r["flags"]:
        print(f"   ! {f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--sitemap")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--file", help="local HTML file (e.g. prerendered build output)")
    ap.add_argument("--url", help="URL the --file represents (for canonical/link checks)")
    ap.add_argument("--ua", default="googlebot")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    ua = UAS.get(args.ua, args.ua)

    results = []
    if args.file:
        with open(args.file, encoding="utf-8", errors="replace") as fh:
            body = fh.read()
        u = args.url or "https://example.invalid/"
        results.append(analyse(u, 200, {}, body, [], u))
    urls = list(args.urls)
    if args.sitemap:
        urls += sitemap_urls(args.sitemap, ua, args.limit)
    def check(u):
        try:
            return analyse(u, *fetch(u, ua))
        except Exception as e:  # network errors should not stop a batch
            return {"url": u, "error": str(e), "flags": [f"fetch failed: {e}"]}

    # Modest concurrency: fast enough for a few hundred URLs without hammering the site.
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results += list(pool.map(check, urls))
    if not results:
        ap.error("give at least one URL, --sitemap or --file")

    if args.json:
        json.dump(results, sys.stdout, indent=2)
        print()
        return
    for r in results:
        if "error" in r:
            print(f"\n== {r['url']}\n   ! {r['error']}")
        else:
            print_report(r)
    if len(results) > 1:
        titles = [r.get("title") for r in results if r.get("title")]
        dupes = {t for t in titles if titles.count(t) > 1}
        descs = [r.get("description") for r in results if r.get("description")]
        ddupes = {d for d in descs if descs.count(d) > 1}
        flagged = sum(1 for r in results if r.get("flags"))
        print(f"\n-- {len(results)} pages, {flagged} with flags, "
              f"{len(dupes)} duplicate titles, {len(ddupes)} duplicate descriptions")
        for t in dupes:
            print(f"   duplicate title: {t}")
        for d in ddupes:
            print(f"   duplicate description: {d[:90]}...")


if __name__ == "__main__":
    main()
