# Measurement and iteration (Search Console first)

## Contents
1. Setup
2. After every deploy
3. The 2–4 week review
4. Reading positions
5. CTR benchmarks
6. Cannibalisation
7. Indexing problems
8. Cadence

---

## 1. Setup

- Search Console: prefer a **Domain property** (`sc-domain:example.com`), which covers every protocol and subdomain. API calls must use that exact string.
- Submit the sitemap. Add Bing Webmaster Tools (import from GSC).
- Analytics (GA4 or a privacy-friendly alternative) with organic landing pages and conversions.
- If the `seo-google` skill or another API helper is configured, use it to pull Search Analytics and URL Inspection data; otherwise ask the user for a CSV export from the Performance report (Queries and Pages tabs) and the Page indexing report (the indexing report has no API; it must be exported from the UI).

## 2. After every deploy

1. Run `scripts/seo_check.py` on the changed pages (and one page of every other type if shared code changed).
2. Resubmit the sitemap if URLs were added.
3. Request indexing via URL Inspection for the 3–5 most important new or changed URLs only. The quota is small (about 10/day in the UI) and the rest will be found through the sitemap and links. The Indexing API is only for job postings and livestreams; do not use it for normal pages.
4. Ping IndexNow for Bing.
5. Note the date and what changed (a changelog in the project docs), so later ranking moves can be attributed.

## 3. The 2–4 week review

Pull 90 days of query+page data and run:

```bash
python3 <skill-dir>/scripts/gsc_opportunities.py export.json            # JSON from the GSC API (rows with keys [query, page])
python3 <skill-dir>/scripts/gsc_opportunities.py queries.csv --csv      # CSV export with Query/Page/Clicks/Impressions/Position columns
```

It prints:
- **Striking distance**: queries at average position 8–20 with meaningful impressions. Act first: strengthen the matching section, add the exact phrasing to an H2 or FAQ, add internal links with that anchor, improve the title.
- **Low CTR for position**: pages whose CTR is far below the expected curve. Rewrite the title and description to match the dominant queries and promise a clear benefit.
- **Cannibalisation**: queries where two or more of your URLs collect impressions. Consolidate (merge and 301), differentiate the intents, or point internal links at the intended page.
- **Deep positions with high impressions** (50+): the page is relevant but lacks authority or matches the wrong intent. More on-page copy rarely helps; plan links, or retarget the page at a winnable long-tail variant.

### Estimating upside honestly

- One search can show two of your URLs, and Search Console counts an impression for each. When two pages share a query, their impressions are the **same searches**: never add them up. Use the larger page's impressions as the baseline for the consolidated page (the sum is an upper bound at most).
- Base CTR uplift on the expected-CTR band for the *target* position, label it an estimate, and give a range.
- When you only know a page by its URL and its queries, say what you are assuming about it (single recipe vs category page, tool vs article) and ask the user to confirm before recommending a retitle or merge.

### "Traffic is flat" questions

A 90-day total cannot show a trend. Ask for the Performance report's **Dates** tab (12–16 months) and compare periods: last 28 days against the previous 28 days and against the same period last year. Look for seasonality, drops that line up with known Google core updates, and changes in indexed page counts. Do the prioritised plan from the data you have anyway, and say what the extra export would add.

## 4. Reading positions

| Average position | Meaning | Typical action |
|---|---|---|
| 1–3 | Winning | Protect: do not churn the page; refresh facts and dates |
| 4–7 | Page one | CTR work, featured-snippet formatting, a few internal links |
| 8–20 | Striking distance | Content depth for the exact query, internal links, title |
| 21–50 | Relevant but weak | Intent check against the SERP, depth, links |
| 50+ | Not competitive | Authority (off-page), or target a long-tail variant instead |

Averages hide spread: a page at "position 17" may rank 6 for one query and 60 for another. Always analyse at query+page level.

## 5. CTR benchmarks

Rough organic CTR by position (varies with SERP features, AI Overviews and brand): 1 ≈ 25–35%, 2 ≈ 12–18%, 3 ≈ 8–11%, 4–5 ≈ 5–7%, 6–10 ≈ 2–4%, 11–20 ≈ 1%. A page well below its band has a snippet problem (title, description, or a mismatch with the query) — or the SERP is crowded with AI Overviews, ads or video carousels. Check the live SERP before rewriting.

## 6. Cannibalisation

Two URLs ranking for the same query at alternating positions usually rank worse than one consolidated page. Fix by deciding which URL owns the query, then:
- move the competing content into the owner and 301 the other URL, or
- retarget the other page at a distinct intent and change its title/H1, and
- point internal links for that query at the owner.

## 7. Indexing problems

| GSC status | Usual cause | Fix |
|---|---|---|
| Discovered – currently not indexed | Low priority or crawl budget; weak internal links | Link from strong pages, improve uniqueness |
| Crawled – currently not indexed | Thin or duplicative content | Add unique substance or noindex/merge |
| Soft 404 | "Not found" or empty content under 200 | See technical-seo.md §2; check server HTML is not just a spinner |
| Duplicate, Google chose different canonical | Near-duplicate pages or conflicting canonicals | Make pages distinct or consolidate; align canonical signals |
| Excluded by noindex | Intended, or an inherited/miss-branch noindex | Confirm intent; check layouts and API-failure paths |
| Blocked by robots.txt | Disallow rule | Remove unless truly never-crawl |

Use URL Inspection (UI or API, ~2,000/day per property via API) to confirm the rendered HTML and the Google-selected canonical for specific URLs.

## 8. Cadence

- Weekly in the first month after launch: indexing status of new URLs.
- Monthly: striking-distance and CTR review, Links report, CWV report, one or two targeted page improvements.
- Quarterly: refresh the keyword map, prune or merge pages with no impressions after 6 months, update year-stamped titles and "last reviewed" dates.
- Seasonal content: publish and link 6–8 weeks before the peak.
