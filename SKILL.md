---
name: seo-playbook
description: Hands-on SEO implementation playbook for building and changing real websites — keyword research that finds winnable queries, mapping one keyword set per page, writing titles/meta/H1/content/FAQs/internal links, structured data, technical indexability checks (canonicals, soft 404s, server-rendered HTML, sitemaps), off-page link earning and launch distribution, and Search Console follow-up. Use this skill whenever you are creating or editing any public web page, landing page, tool page, blog post, or programmatic page set and it should rank on Google; whenever the user mentions SEO, keywords, ranking, organic traffic, meta tags, titles, backlinks, off-page, "get indexed", "why isn't this page ranking", or Search Console; and whenever you add routes, metadata, sitemaps or robots rules in a web framework — even if the user did not say "SEO" explicitly. Prefer this skill for doing the work in the codebase; the narrower seo-* skills are for deep single-topic audits and paid data APIs.
---

# SEO Playbook

This skill turns SEO into a repeatable engineering workflow: find queries the site can actually win, give every page one clear job, put the right words in the right HTML elements, make sure Google can crawl, render and index the result, earn links, then measure and iterate.

It distils what worked (and what silently broke) while taking a young Next.js tools site from zero to page-one rankings on long-tail queries. The lessons generalise to any stack.

## The mindset, in five sentences

1. **Rankings follow winnability, not wishes.** A young domain will not reach the top 5 for a head term like "qr code generator" this year; it can rank in weeks for "free qr code generator no sign up" or "birthday wish link with name". Target the long tail first and let topical authority lift the head term later.
2. **One page, one search intent, one primary keyword.** Two pages targeting the same query split signals (cannibalisation); one page targeting two intents serves neither.
3. **Google ranks the HTML it receives, not the app the user sees.** If the content, H1, FAQ answers or links only appear after JavaScript runs, assume they do not exist. Check the raw server response every time.
4. **Indexability bugs outweigh copywriting.** A soft 404, a stray canonical or a `noindex` inherited from a layout can erase months of content work without any error. Verify status codes, canonicals and robots on every page type you touch.
5. **Measure with Search Console, not intuition.** Impressions at position 8–20 are the cheapest wins; position 50+ means an authority or intent problem that more on-page tweaks will not fix.

Set the user's expectations honestly: first impressions for long-tail pages usually appear in 2–6 weeks; head terms take months and backlinks. "Fast" SEO means picking fights the site can win.

## Workflow

Run the phases in order for a new site or page set. For a single-page change, do phases 3, 4 and 6 at minimum. Read the linked reference file when you reach a phase — each one holds the detailed checklist and templates.

**Scale the work to the request.** A page review is a page review; a keyword map is a keyword map. Do the asked-for job thoroughly, and put adjacent opportunities (keywords, off-page ideas) in a short "Also worth doing" list rather than producing full extra plans nobody asked for. Extra deliverables dilute the one the user needs and cost time.

**Verify before you assert.** Check facts you can check (the live SERP, whether the brand name is already taken, what a page actually contains, what a feature actually does). When you cannot check something — a page you only know by URL, a site that does not load, a feature you have not seen — say it is an assumption and tell the user what to confirm. Confident guesses about someone's site are the most common way SEO advice goes wrong.

**The scripts are for you.** Run `scripts/*.py` yourself. In instructions written for the user, describe the check in plain terms or give a command they can run without this skill (curl, Search Console steps). Reference the skill's script paths only when you know the user has the skill installed.

### Phase 1 — Recon (before changing anything)

- Identify the stack and how pages are rendered (SSR, SSG, SPA, hybrid). For framework traps read the relevant section of `references/technical-seo.md` (Next.js App Router has its own section).
- Inventory what exists: how metadata is set, where page copy lives, sitemap and robots generation, structured-data components, analytics. Reuse existing patterns rather than adding parallel ones.
- Fetch a representative page of each type as Googlebot and record the baseline:
  `python3 <skill-dir>/scripts/seo_check.py <url> [<url> ...]`
  It reports status, title/description lengths, canonical, robots meta and `X-Robots-Tag`, H1 count, visible word count, JSON-LD types, OG image and red flags like a "Loading…" main element.
- If Search Console data is available (an export, an API helper, or the `seo-google` skill if installed), pull 90 days of query+page rows and run `scripts/gsc_opportunities.py` (see Phase 6). Existing impressions tell you what Google already associates with the site.
- Look for project SEO docs or memory notes from earlier audits and build on them.

### Phase 2 — Keyword research and the keyword map

Read `references/keyword-research.md`. In short:

1. Seed from the product: what the page does, who uses it, the words users type when they want exactly that.
2. Expand with free signals: Google autocomplete and "People also ask", related searches, competitor titles, GSC queries, Reddit/Quora phrasing. Use paid APIs only if the project has them (e.g. the `seo-dataforseo` or `seo-ahrefs` skills, if installed).
3. Classify intent (do / know / go / buy) and **look at the live SERP** for each candidate. If page one is all big brands or all a different page type (e.g. listicles when you have a tool), the keyword is not winnable for this page yet.
4. Score winnability: weak competitors (thin indie pages, forums, GitHub repos, `*.vercel.app` sites) on page one is the strongest signal.
5. Check the brand name: search it bare, plus npm/PyPI/GitHub/app stores where relevant. If it is taken, recommend using the domain form ("Brand.app") consistently.
6. Produce a **keyword map**: one row per URL with primary keyword, 3–8 secondary/long-tail terms, intent, and where each term goes (title, H1, H2, intro, FAQ). No primary keyword appears on two rows, and every row in every table has an intent.

Volumes without a paid tool are directional tiers (very high / high / medium / low). Say so in your output instead of inventing numbers.

### Phase 3 — On-page implementation

Read `references/on-page.md` for the full checklist and the page content model. The essentials for every indexable page:

- **Title**: unique, primary keyword first, ideally ≤ 60 characters including any brand suffix, and written to win the click.
- **Meta description**: unique, 120–160 characters, states what the user gets and the differentiator ("free, no sign-up, runs in your browser") only when it is true.
- **Exactly one H1** in the server HTML, matching the page's primary intent (a close variant of the title, not a copy).
- **Body**: answer the query in the first paragraph, then add depth a competitor page lacks: how-to steps, worked examples, common problems with fixes, limitations, FAQs. Each section exists because a searcher needs it, not to hit a word count.
- **FAQs** visible in the HTML (not only in collapsed, unmounted accordions and not only in JSON-LD), phrased as real queries.
- **Internal links**: 3–5 contextual links to related pages and at least one link *into* the page from a relevant hub or article. No orphan pages.
- **Structured data** that matches visible content: see `references/structured-data.md` for which types still earn rich results.
- **Trust**: real author or organisation, accurate claims, last-reviewed date that changes when content changes, sources for numbers. Never publish placeholder reviews or testimonials — Google treats them as misrepresentation.

Store page SEO content as data (a typed config object or CMS fields) rather than scattering strings through JSX. That makes uniqueness checks, length tests and bulk reviews possible.

### Phase 4 — Technical gates (do not skip)

Read `references/technical-seo.md`. Before calling any page done, confirm in the **built or deployed HTML**:

- Status 200 for real pages and a real 404 (not a 200 with "not found" text) for unknown URLs.
- Self-referencing absolute canonical, and no canonical/robots inherited by accident from a parent layout.
- Indexable pages are in the sitemap with an honest `lastmod`; noindex pages are not.
- Pages you want hidden use `noindex` (meta or `X-Robots-Tag`) and are **not** blocked in robots.txt, otherwise Google can never read the noindex.
- Main content, H1, FAQ answers and internal links are present in the raw HTML (`seo_check.py` word count and H1 check).
- One preferred host (https, www or apex) with single-hop 301s from the others.
- Core Web Vitals are not regressed (LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1). For field data use PageSpeed Insights / CrUX, or the `seo-performance` / `seo-google` skills if installed.

### Phase 5 — Off-page and distribution

Read `references/off-page.md`. On-page work makes a page eligible; links and brand demand decide how high it goes for anything competitive. Plan link earning alongside the page, not after:

- Build one **linkable asset** per cluster (free tool, template repo, data table, original guide).
- Submit to the few directories and launch platforms that fit the audience, written as genuine posts.
- Use visual platforms (Pinterest, YouTube Shorts) for visual niches; GitHub for developer audiences.
- Set up Bing Webmaster Tools and IndexNow (Bing's index feeds ChatGPT search and Copilot).
- Never buy links, join link schemes, or mass-submit to junk directories.

When you cannot do off-page work yourself, produce a ready-to-run kit for the user: target list, post drafts, outreach email drafts, and a calendar.

### Phase 6 — Verify, ship, monitor

Read `references/measurement.md`.

- Re-run `seo_check.py` against the built or deployed pages and diff against the Phase 1 baseline. For changes to shared layouts or components, diff **every** page type, not just the one you edited — a site-wide change can quietly alter pages that already rank.
- After deploy: resubmit the sitemap, request indexing only for the handful of most important new URLs, ping IndexNow.
- After 2–4 weeks: run `python3 <skill-dir>/scripts/gsc_opportunities.py <gsc-export.json|csv>` to list striking-distance queries, low-CTR pages and cannibalisation, then iterate on titles, sections and internal links for those.

## Hard-won rules

These came from real regressions. Each one cost rankings or indexing before it was found.

- **Check what crawlers actually receive.** A route-level loading spinner, `ssr: false` dynamic imports, or a fade-in that starts at `opacity: 0` can leave the server HTML with only "Loading…" while the browser looks perfect. AI crawlers do not run JavaScript at all.
- **Entrance animations hide the hero.** Animation libraries (framer-motion `initial={{ opacity: 0 }}`, AOS, GSAP) server-render their start state, so the H1 and intro ship invisible until hydration, delaying LCP. Use `initial={false}` or CSS-only animation for anything above the fold; grep the built HTML for `opacity:0`.
- **CMS bodies add a second H1.** Markdown that starts with `# Title` under a page-level H1 duplicates it. Demote body H1s to H2 in the renderer.
- **Soft 404s from streaming SSR.** Once a streamed response has started, a later `notFound()` cannot change the 200. Reject unknown slugs before rendering (static params with dynamic params disabled), or return an explicit `noindex` from the metadata miss branch.
- **Inherited canonicals.** A canonical in a root layout leaks into every page that does not set its own. A soft 404 that inherits it becomes an indexable duplicate of a real page.
- **"API down" is not "no results".** Code that decides `notFound()` or `noindex` must distinguish a failed fetch from an empty result, or one outage deindexes real pages.
- **Hidden content.** Accordions that unmount closed panels remove FAQ answers from the HTML. Keep them mounted (`hidden="until-found"` or CSS) so they are crawlable and findable by in-page search.
- **Shared components are blast radius.** When one page ranks well, change shared SEO components behind opt-in props and diff the built HTML of the other pages before and after.
- **Fabricated social proof is a policy violation.** Sample reviews left in production, hardcoded testimonials as a loading fallback, and claims like "runs in your browser" for server-processed tools all hurt trust and ad-network approval.
- **Ratings must be your own.** Never add `aggregateRating`/`review` markup that is not backed by reviews collected and shown on the page itself — and never copy ratings from App Store, Play Store, G2 or other sites into structured data. Google's review-snippet rules forbid both.
- **Roll out page sets gradually.** Launch the two or three variant pages (per profession, currency, city…) with the most distinct content, then add more once those earn impressions. Launching dozens of near-identical pages on a new domain looks like scaled thin content.
- **Thin taxonomy pages.** Tag or category pages with very few posts should be `noindex` and out of the sitemap until they have enough unique content.
- **Dates that lie.** A sitemap `lastmod` that never changes, or a visible "last reviewed" date months older than the latest edit, wastes freshness signals. Update both whenever content changes.
- **Titles truncate.** A brand suffix template pushes most titles past 60 characters. Front-load the keyword so truncation only cuts the brand, or drop the suffix on high-value pages.
- **Seasonal copy expires.** Year-stamped titles ("Eid Wishes 2027") need a dated reminder to roll them forward.

## Output formats

Match the deliverable to the request:

- **Implementation work**: make the code changes, then report what changed per page, the before/after `seo_check.py` results, and anything the user must do outside the code (Search Console, off-page posts).
- **Keyword research**: the keyword map table from `references/keyword-research.md`, with the live-SERP winnability notes and an honest volume caveat.
- **Audit**: use this structure:

```
# <Site/page> SEO audit — <date>
## Verdict (3–5 sentences: what is working, the single biggest blocker, the fastest win)
## Ranking data (GSC: clicks/impressions/top pages, striking-distance queries) — or "no GSC data available"
## Findings by priority
### P0 — indexing/rendering blockers
### P1 — on-page and keyword targeting
### P2 — enhancements
(each finding: what, evidence (URL/file:line/command output), why it matters, fix)
## Off-page plan
## Next steps checklist (owner: agent / user)
```

Save audits and keyword maps as Markdown in the project's docs folder when one exists, so the next agent can build on them.

## Related skills

Use these for depth when they are installed; this playbook tells you when you need them:

- `seo-google` — Search Console, URL Inspection, CrUX, GA4 data.
- `seo-technical`, `seo-schema`, `seo-sitemap`, `seo-performance` — deep single-area audits.
- `seo-cluster`, `seo-content-brief` — SERP-overlap clustering and per-page briefs.
- `seo-backlinks`, `seo-bing` — link profile data and IndexNow.
- `seo-geo` — AI Overviews / ChatGPT / Perplexity visibility.
- `seo-programmatic` — template pages at scale.
