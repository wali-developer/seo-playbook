# Keyword research and the keyword map

Goal: for every page, choose the queries it can realistically rank for, and decide exactly where each word goes. A keyword map is the contract between research and implementation.

## Contents
1. Seed list
2. Expansion with free sources
3. Intent classification
4. Reading the SERP (winnability)
5. Prioritising
6. The keyword map template
7. Placement rules
8. Worked examples
9. Common mistakes

---

## 1. Seed list

Start from the product, not from a keyword tool:

- What does the page let someone *do* or *learn*? ("format JSON", "make a birthday surprise link")
- Who is searching, and what words do they use? Developers say "prettify", "beautify", "format"; non-technical users say "make", "create", "free", "online", "with name".
- Which modifiers express this product's real advantages? `free`, `no sign up`, `no watermark`, `never expires`, `online`, `with logo`, `in Urdu`, `for <audience>`, `2027`.
- What problems bring people here? "qr code not scanning", "invalid json unexpected token".

Write 5–15 seeds per page type.

## 2. Expansion with free sources

Use whichever the environment allows (WebSearch/WebFetch, a browser, or the user pasting results):

| Source | How | What it gives |
|---|---|---|
| Google autocomplete | Type seed + a, b, c…; seed + "for", "with", "without", "vs", "how to" | Real long-tail phrasing with demand |
| People Also Ask | Expand PAA boxes on the SERP | FAQ questions and H2 ideas |
| Related searches | Bottom of SERP | Adjacent intents, spoke-page ideas |
| Competitor titles/H2s | Fetch top 5 results | The vocabulary Google currently rewards |
| Search Console | Queries report, 90 days, query+page | What Google already associates with the site — the best source for an existing site |
| Reddit/Quora/forums | `site:reddit.com <topic>` | How real users phrase problems |
| Bing Webmaster Tools keyword research | Free, needs a verified site | Volume estimates without a paid tool |
| Google Keyword Planner | Free with an Ads account | Volume ranges |

Paid sources (DataForSEO, Ahrefs, Semrush) give real volume and difficulty. Use them through the `seo-dataforseo` or `seo-ahrefs` skills when configured. Without them, report volume as tiers (Very high / High / Medium / Low) and say they are directional.

## 3. Intent classification

Every query has a dominant intent; the page type must match it.

| Intent | Example | Page type that ranks |
|---|---|---|
| Do (transactional tool) | "json formatter", "qr code generator with logo" | Working tool above the fold, then explanation |
| Know (informational) | "static vs dynamic qr code", "what is a jwt" | Article/guide |
| Buy/compare (commercial) | "best invoice generator", "X alternative" | Comparison, listicle, alternatives page |
| Go (navigational) | "acme json formatter" | Brand/home page |
| Local | "plumber near me" | Location page + Google Business Profile |

Mixed intent is common: "qr code size for print" wants a short answer plus a table. Check the SERP to see which format wins.

**Homonym traps.** A keyword that looks perfect can mean something else to most searchers: "receipt generator" is dominated by fake-receipt intent, "quote generator" by inspirational quotes, "template" by Canva designs rather than tools. Always look at what actually ranks before mapping a page to it, and list such keywords under "rejected, and why".

**Format intent.** The SERP also tells you the format searchers want. If "invoice template for photographers" ranks Word/Excel/PDF downloads, a page targeting it must offer those downloads (alongside your tool), or you should not target it. Keep this consistent: do not reject a keyword for its format intent and then map a sibling page with the same intent but without that format.

## 4. Reading the SERP (winnability)

Before committing to a keyword, open the live SERP (or fetch it) and look at the top 10:

**Signs it is winnable for a young site:**
- Thin single-purpose sites, indie projects, `*.vercel.app`/`*.netlify.app`, GitHub repos, forum threads or Pinterest pins in the top 10.
- Results that only partly match the query (a "birthday wishes" text listicle ranking for "birthday wish link maker").
- Old pages (dated years ago) or pages that are clearly worse than what you can build.

**Signs it is not winnable yet:**
- Page one is entirely major brands (Adobe, Canva, Shutterfly) or high-authority publishers.
- Every result is a different page type from yours (all articles when you have a tool).
- Massive head terms with millions of searches.

Do not abandon unwinnable head terms. Place them in the title/H1 of the hub page as a long-term goal while the long tail does the near-term work.

## 5. Prioritising

Score each candidate quickly:

| Factor | High | Low |
|---|---|---|
| Demand | Autocomplete suggests it unprompted; GSC impressions | Only you would type it |
| Winnability | Weak competitors on page one | Brands only |
| Fit | The page fully satisfies it | Partial match |
| Business value | Leads to use/sign-up/revenue | Vanity traffic |

Do the high-fit, winnable, medium-demand queries first. For an existing site, **striking-distance queries** (position 8–20 with impressions) come before everything, because they need the smallest change.

## 6. The keyword map template

One row per URL. A primary keyword appears on exactly one row.

```markdown
| URL | Primary keyword | Secondary / long-tail | Intent | Winnability note | Placement |
|---|---|---|---|---|---|
| /tools/qr-code-generator | free qr code generator | qr code generator with logo, no sign up, never expires, svg | Do | Head term = brands; modifiers have indie competitors | Title + H1: primary; H2 "Customize": with logo; trust strip: no sign up / never expires |
| /tools/wifi-qr-code-generator | wifi qr code generator | qr code for wifi, share wifi password qr | Do | Medium competition, few dedicated pages | Title, H1, intro, FAQ |
| /blog/static-vs-dynamic-qr-codes | static vs dynamic qr code | qr code that doesn't expire, free lifetime qr | Know | Weak, mostly vendor blogs | Title, H1, H2s; links to tool twice |
```

Every row in every table carries an intent, including later-phase and tool rows. Mapping intent is how you catch a page that cannot rank for its keyword.

Also record:
- **Spoke pages to create**: a distinct intent with enough demand gets its own URL (e.g. "wifi qr code generator" deserves a page; "qr code generator blue" does not).
- **Rollout order for page families**: for variants such as per-profession templates or per-currency/country pages, launch the two or three with the most distinct content first, give each genuinely different substance (examples, fields, rules, FAQs), and add more after the first ones collect impressions. A brand-new domain launching ten near-identical variants at once looks like scaled thin content.
- **Blog posts to support each tool**: informational queries that link back to the tool.
- **Rejected keywords and why**: so the next agent does not re-research them.

## 7. Placement rules

| Element | What goes there |
|---|---|
| Title | Primary keyword first, then the strongest modifier/differentiator |
| H1 | Primary keyword or close variant (not identical to the title) |
| Meta description | Primary + one secondary, written as a promise |
| First 100 words | Primary keyword naturally, plus the direct answer |
| H2s | Secondary keywords phrased as the section's real topic ("How to add a logo to a QR code") |
| FAQ questions | PAA questions and long-tail queries, verbatim when natural |
| Image alt text | Describe the image; include a keyword only if it genuinely describes it |
| Anchor text of internal links into the page | Varied, descriptive, includes the primary keyword sometimes |
| URL slug | Short, primary keyword, hyphenated, stable (never change a ranking URL without a 301) |

Write for the reader. Repeating the exact keyword in every paragraph is unnecessary; Google understands synonyms and related terms, and stuffing reads as spam.

## 8. Worked examples

**Tool site, young domain.** "qr code generator" had millions of searches and a page one of Adobe, Canva and established QR vendors. The plan targeted modifiers instead: "free qr code generator no sign up", "never expires", "with logo", plus spoke pages for wifi, vCard and WhatsApp QR codes and five supporting blog posts ("QR code not scanning? 10 causes"). The blog posts started collecting impressions within weeks while the head term stayed out of reach — as expected.

**Greeting-card product.** Pages originally targeted "birthday wishes for sister", which greeting-card brands own. SERP review showed that the product-intent queries ("birthday wish link", "birthday surprise website for girlfriend", "Eid Mubarak card with name") had weak indie competitors and zero usage on the site. Retitling the hub and occasion pages and adding nine relationship spokes produced the site's top page: "birthday wishes for best friend" at position ~8 with thousands of impressions.

**Developer tool already ranking.** A code beautifier ranked on page one for "code formatter online" even though its title said "Code Beautifier". The GSC query report revealed the vocabulary users actually type ("code formatter", "format code online", "prettify code"), which is the cheapest input for the next title/H2 test.

## 9. Common mistakes

- Targeting only head terms because they look impressive.
- Picking keywords without looking at the SERP.
- Two pages with the same primary keyword (hub and spoke both titled "Birthday Wishes"). Give the hub the broad term and each spoke a distinct modifier.
- Inventing search volumes. Use tiers and say where they came from.
- Ignoring the page-type match: an article will not outrank tools for a "do" query, and vice versa.
- Keyword lists rendered as visible "chips" or tag clouds instead of prose. They read as stuffing; turn them into use-case sentences.
