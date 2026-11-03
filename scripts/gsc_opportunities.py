#!/usr/bin/env python3
"""Find quick SEO wins in Search Console query+page data (stdlib only).

Input, either:
  - JSON from the Search Analytics API, or a helper that wraps it:
      {"rows": [{"keys": [query, page], "clicks": n, "impressions": n, "ctr": x, "position": x}, ...]}
    (ctr may be a fraction or a percentage; it is recomputed from clicks/impressions anyway)
  - CSV (--csv) with columns named like Query, Page/Landing page/URL, Clicks, Impressions, Position.
    The plain "Queries" export from the UI has no page column; cannibalisation is then skipped.

Usage:
  gsc_opportunities.py export.json [--min-impr 50] [--site https://example.com]
  gsc_opportunities.py queries.csv --csv
"""
import argparse
import csv
import json
from collections import defaultdict

# Rough expected CTR by rounded position; used only to flag outliers.
EXPECTED_CTR = {1: 0.28, 2: 0.15, 3: 0.10, 4: 0.07, 5: 0.055, 6: 0.04, 7: 0.035,
                8: 0.03, 9: 0.025, 10: 0.02}


def expected_ctr(pos):
    return EXPECTED_CTR.get(round(pos), 0.01 if pos <= 20 else 0.003)


def load(path, is_csv):
    rows = []
    if is_csv:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh):
                low = {k.strip().lower(): v for k, v in r.items()}
                q = low.get("query") or low.get("top queries") or low.get("queries")
                page = low.get("page") or low.get("landing page") or low.get("url") or low.get("top pages")
                rows.append({
                    "query": q, "page": page,
                    "clicks": float(str(low.get("clicks", 0)).replace(",", "") or 0),
                    "impressions": float(str(low.get("impressions", 0)).replace(",", "") or 0),
                    "position": float(low.get("position", 0) or 0),
                })
    else:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        for r in data.get("rows", data if isinstance(data, list) else []):
            keys = r.get("keys") or [r.get("query"), r.get("page")]
            rows.append({
                "query": keys[0] if keys else None,
                "page": keys[1] if len(keys) > 1 else r.get("page"),
                "clicks": r.get("clicks", 0),
                "impressions": r.get("impressions", 0),
                "position": r.get("position", 0),
            })
    return [r for r in rows if r["impressions"]]


def short(url, site):
    return url.replace(site, "") or "/" if site and url else url


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--csv", action="store_true")
    ap.add_argument("--min-impr", type=int, default=50, help="minimum impressions to report a query")
    ap.add_argument("--site", default="", help="origin to strip from URLs in the output")
    ap.add_argument("--top", type=int, default=25)
    args = ap.parse_args()

    rows = load(args.path, args.csv)
    has_pages = any(r["page"] for r in rows)
    total_c = sum(r["clicks"] for r in rows)
    total_i = sum(r["impressions"] for r in rows)
    print(f"{len(rows)} rows | {total_c:.0f} clicks | {total_i:.0f} impressions | "
          f"CTR {100 * total_c / max(total_i, 1):.2f}%")

    # Aggregate per query (impression-weighted position)
    q = defaultdict(lambda: {"c": 0, "i": 0, "pw": 0, "pages": defaultdict(float)})
    for r in rows:
        a = q[r["query"]]
        a["c"] += r["clicks"]
        a["i"] += r["impressions"]
        a["pw"] += r["position"] * r["impressions"]
        if r["page"]:
            a["pages"][r["page"]] += r["impressions"]
    for a in q.values():
        a["pos"] = a["pw"] / a["i"]

    def qline(k, a):
        top_page = max(a["pages"], key=a["pages"].get) if a["pages"] else ""
        return (f"  {a['c']:5.0f} {a['i']:7.0f}  pos {a['pos']:5.1f}  ctr {100 * a['c'] / a['i']:5.2f}%  "
                f"{k}" + (f"  -> {short(top_page, args.site)}" if top_page else ""))

    print("\n## Striking distance (avg position 8-20): strengthen the section, H2/FAQ wording, internal links, title")
    sd = [(k, a) for k, a in q.items() if 8 <= a["pos"] <= 20 and a["i"] >= args.min_impr]
    for k, a in sorted(sd, key=lambda x: -x[1]["i"])[:args.top]:
        print(qline(k, a))
    if not sd:
        print("  (none)")

    print("\n## Page one, CTR well below expected: rewrite title/description to match these queries")
    low = [(k, a) for k, a in q.items()
           if a["pos"] <= 10 and a["i"] >= args.min_impr and a["c"] / a["i"] < 0.5 * expected_ctr(a["pos"])]
    for k, a in sorted(low, key=lambda x: -x[1]["i"])[:args.top]:
        print(qline(k, a) + f"  (expected ~{100 * expected_ctr(a['pos']):.1f}%)")
    if not low:
        print("  (none)")

    print("\n## High impressions, position 40+: authority or intent gap; links or a long-tail retarget, not more copy")
    deep = [(k, a) for k, a in q.items() if a["pos"] >= 40 and a["i"] >= args.min_impr]
    for k, a in sorted(deep, key=lambda x: -x[1]["i"])[:args.top]:
        print(qline(k, a))
    if not deep:
        print("  (none)")

    if has_pages:
        print("\n## Cannibalisation: one query, several of your URLs with >=20% of its impressions each")
        found = False
        for k, a in sorted(q.items(), key=lambda x: -x[1]["i"]):
            if a["i"] < args.min_impr:
                continue
            big = {p: i for p, i in a["pages"].items() if i >= 0.2 * a["i"]}
            if len(big) > 1:
                found = True
                print(f"  {k} ({a['i']:.0f} impr): " +
                      ", ".join(f"{short(p, args.site)} {100 * i / a['i']:.0f}%" for p, i in big.items()))
        if not found:
            print("  (none)")

        print("\n## Pages by impressions (query vocabulary per page, top 5 queries)")
        pages = defaultdict(lambda: {"c": 0, "i": 0, "pw": 0, "q": []})
        for r in rows:
            if not r["page"]:
                continue
            p = pages[r["page"]]
            p["c"] += r["clicks"]
            p["i"] += r["impressions"]
            p["pw"] += r["position"] * r["impressions"]
            p["q"].append((r["impressions"], r["query"]))
        for url, p in sorted(pages.items(), key=lambda x: -x[1]["i"])[:15]:
            qs = ", ".join(x[1] for x in sorted(p["q"], reverse=True)[:5])
            print(f"  {p['c']:5.0f} {p['i']:7.0f}  pos {p['pw'] / p['i']:5.1f}  {short(url, args.site)}\n         {qs}")


if __name__ == "__main__":
    main()
