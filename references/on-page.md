# On-page SEO checklist and page content model

## Contents
1. Per-page checklist (definition of done)
2. Titles
3. Meta descriptions
4. Headings
5. The page content model (tool / product / landing pages)
6. Blog articles
7. FAQs
8. Internal linking
9. Images and social previews
10. E-E-A-T and trust
11. Programmatic and spoke pages
12. Automated content tests

---

## 1. Per-page checklist (definition of done)

An indexable page is done when all of these hold in the server-rendered HTML:

- [ ] Unique `<title>`, primary keyword first, ≤ 60 chars including any suffix (or keyword front-loaded so truncation only cuts the brand)
- [ ] Unique meta description, 120–160 chars
- [ ] Exactly one `<h1>`, visible (not `sr-only` unless a visible heading is impossible)
- [ ] Logical H2/H3 outline; no skipped levels used for styling
- [ ] Main content present without JavaScript
- [ ] Self-referencing absolute canonical
- [ ] Indexable (no stray `noindex`), in the sitemap
- [ ] 3–5 contextual internal links out; at least one link in from a hub or related page
- [ ] Structured data matching visible content, valid in the Rich Results Test
- [ ] OG title, description and 1200×630 image
- [ ] Images have dimensions, alt text and modern formats; LCP image not lazy-loaded
- [ ] Trust elements: author/publisher, last-reviewed date, sources where numbers or advice appear
- [ ] Claims are true (privacy, "free", "no sign-up", supported formats)

## 2. Titles

- Pattern for tools: `{Primary keyword} — {Differentiator or second keyword}`. Example: `JSON Formatter — Validate & Prettify JSON Online, Free`.
- Pattern for articles: the question or outcome the searcher wants. Example: `QR Code Not Scanning? 10 Causes and How to Fix Them`.
- Pattern for hubs/categories: `{Topic} Tools` or `{Topic} Guides`.
- Google shows about 600 px (~55–60 characters). Longer titles are not penalised, but the tail is cut and Google rewrites titles it finds unhelpful. Put the keyword and the reason to click in the first 50 characters.
- A global template suffix like `%s | Brand` adds 10–20 characters to every title. Either budget for it or use an absolute title on high-value pages.
- Every page title is unique. Test this in CI when titles are data.
- Check the live SERP before writing the title: if competitors promise "100+ wishes" or "50 examples", a title offering "24" loses the click even at position 3. Match or beat the SERP's promise, but only with numbers the page actually delivers.
- When a page already ranks, title changes are experiments. Change one high-traffic title at a time, note the date, and compare 28 days of GSC CTR and position before and after.

## 3. Meta descriptions

- 120–160 characters; Google rewrites many descriptions, but a good one still wins clicks when it matches the query.
- Include the primary keyword (Google bolds matching terms) and a concrete promise: what the user gets, how fast, what makes it different.
- Mention "free", "no sign-up", "private" only when they are true for this page.
- Never duplicate across pages; never leave it to a generic site-wide default.

## 4. Headings

- One H1 per page describing the page's main topic. If a client component renders the visible heading, make sure that heading is in the server HTML, or render a server H1 and avoid a duplicate.
- H2s are the page's table of contents and the place for secondary keywords. A searcher skimming only the H2s should know what the page covers.
- Choose heading tags for meaning; keep the visual style with CSS classes. Changing an `<h3>` to an `<h2>` should not change the design.

## 5. The page content model (tool / product / landing pages)

Store page content as typed data so every page has the same complete structure and can be tested. A model that worked well for a tools site:

```ts
interface PageSeoContent {
  primaryKeyword: string;
  keywordCluster: string[];        // secondary + long-tail, used for metadata and review — not rendered as chips
  seoTitle: string;
  seoDescription: string;
  intro: string;                   // direct answer in the first 2–3 sentences
  features: string[];
  steps: string[];                 // how to use it
  example: { title: string; body: string };
  useCases?: { title: string; body: string }[];
  guides?: { title: string; paragraphs: string[]; examples?: { label: string; code: string }[] }[];
  commonProblems?: { problem: string; fix: string }[];
  methodology: string;             // how it works / how results are calculated
  privacy: string;                 // what happens to user data — must match reality
  limitations: string;             // honest boundaries; builds trust
  faqs: { question: string; answer: string }[];   // 5+
  relatedToolSlugs?: string[];
  relatedArticles?: { title: string; slug: string }[];
  lastReviewed: string;            // update when the content changes
  ogImage?: string;
}
```

Render order that works for "do" intent pages: H1 + one-line value proposition → the tool/product (above the fold) → intro → how to use → features/use cases → example → guides and common problems → methodology, privacy, limitations → FAQs → related tools and articles → last reviewed.

Depth guidance: the pages that ranked had roughly 800–1,100 words of genuinely tool-specific content (guides, real error messages with fixes, worked examples). Word count is a side effect of covering what searchers need, not a target. A generic paragraph repeated across 30 pages with the tool name swapped adds nothing and can drag the site down.

## 6. Blog articles

- One informational intent per article, matching a keyword-map row.
- Answer the question in the opening paragraph, then expand. Use descriptive H2s, numbered steps, tables and real screenshots.
- Link to the relevant tool or product page at least twice (once early, once in the conclusion) with descriptive anchors, and add the article to that page's related-articles list so the link goes both ways.
- Byline a real person with a short bio and an author page where possible; Organization-only authorship is the weakest E-E-A-T signal.
- Show published and updated dates and keep `dateModified` honest.
- Categories and tags are navigation, not landing pages. Noindex them until they hold several posts and an introduction.

## 7. FAQs

- Use real questions from People Also Ask, autocomplete and support emails, phrased the way users type them.
- Answer in 40–80 words, self-contained (AI Overviews and assistants quote passages like these).
- Keep the answers in the HTML. Many accordion components unmount closed panels; use `hidden="until-found"` or CSS-only collapse so the text is crawlable and findable with Ctrl+F.
- FAQPage markup no longer produces rich results for most sites (Google limited it to authoritative government and health sites in 2023), but it is harmless and still describes the content. The visible answers are what matter.

## 8. Internal linking

- Each page links to 3–5 closely related pages with descriptive anchor text ("validate JSON before converting it to XML"), not "click here".
- Each page receives links from a hub (category page, tools index) and from at least one contextual source (an article, a related tool).
- Hub-and-spoke: the hub targets the broad term and links to every spoke; each spoke links back to the hub and to 2–3 sibling spokes.
- New pages need links from pages Google already crawls often (home page, top-traffic pages). Header/footer links alone are weak; contextual body links count more.
- Find orphans: compare the sitemap URL list with URLs linked from crawled HTML.
- Breadcrumbs: visible and in BreadcrumbList JSON-LD.

## 9. Images and social previews

- Explicit `width`/`height` (or aspect-ratio) to prevent layout shift.
- WebP/AVIF, responsive `srcset`, lazy-load below the fold only; the LCP image gets priority/eager loading.
- Alt text describes the image for someone who cannot see it.
- Descriptive file names (`wifi-qr-code-guest-sign.webp`).
- Unique OG image per important page (1200×630). A generic site-wide image is fine for long-tail pages but costs clicks on shared high-value pages.

## 10. E-E-A-T and trust

Google's quality systems reward pages that show experience, expertise, authoritativeness and trust, especially on money and health topics (tax, finance, legal).

- About page that says who runs the site and why; Contact page with a working address.
- Named authors with bios for articles; reviewer names for finance/health content when possible.
- Sources and "last reviewed" dates for calculations, rates, rules.
- Accurate privacy statements: if the tool sends data to a server, do not say it runs in the browser.
- Real reviews only. Never seed sample testimonials into production, and never hardcode testimonials as a loading fallback.
- Organization JSON-LD with `logo` and `sameAs` links to real social profiles.

## 11. Programmatic and spoke pages

Spoke pages (e.g. `/wishes/birthday/for-sister`, `/tools/wifi-qr-code-generator`) work when each has a distinct search intent and unique substance: its own examples, messages, tips and FAQs. They fail when they are the same template with a word swapped.

- Each spoke gets a unique title, H1, intro, at least 3 unique FAQs and its own preview/example data.
- Enforce uniqueness in tests (no duplicated messages or descriptions across pages).
- Link spokes from the hub and to each other.
- For large page sets, use the `seo-programmatic` skill and its thin-content safeguards.

## 12. Automated content tests

When SEO content is data, add tests that fail the build on:
- duplicate titles or descriptions across pages
- titles over the character budget, descriptions outside 110–160
- fewer than N FAQs on priority pages
- repeated paragraphs or messages across pages
- `relatedToolSlugs` or `relatedArticles` pointing at non-existent pages
- stale `lastReviewed` older than the last content change, if you track that
