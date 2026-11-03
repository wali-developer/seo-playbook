# Technical SEO: crawl, render, index

## Contents
1. The indexability checklist
2. Status codes and soft 404s
3. Canonicals
4. robots.txt vs noindex
5. Sitemaps
6. Rendering: what crawlers see
7. Hosts, redirects, HTTPS
8. Core Web Vitals
9. International (hreflang)
10. Framework notes: Next.js App Router
11. Framework notes: SPAs (React/Vue/Vite) and others
12. Verification commands

---

## 1. The indexability checklist

For each page type (home, listing, detail, article, taxonomy, legal, private):

| Check | Expected |
|---|---|
| Status | 200 for real pages; 404/410 for unknown URLs; 301 for moved |
| Canonical | Absolute, self-referencing, on the preferred host |
| Robots | `index, follow` for public pages; `noindex` for private/thin pages |
| Sitemap | Present iff indexable |
| Server HTML | Contains H1, main copy, FAQ answers, internal links |
| Title/description | Page-specific, not the site default |

## 2. Status codes and soft 404s

A soft 404 is a page that says "not found" but returns 200. Google either drops it or, worse, indexes it.

Common causes:
- Catch-all dynamic routes that render a "not found" component without setting the status.
- **Streaming SSR**: once the response has started streaming, the status is committed. Calling `notFound()` after the shell has streamed renders 404 UI under a 200.
- SPA fallbacks that serve `index.html` with 200 for every path.

Fixes:
- When the valid set is known at build time, reject unknown params before rendering (static params plus disabled dynamic params, or a router-level check).
- When the set is only known at runtime, make the miss branch return explicit `robots: noindex, nofollow`, and do not let it inherit a canonical.
- Test with junk URLs: `curl -s -o /dev/null -w '%{http_code}' https://site.com/tools/does-not-exist`.

## 3. Canonicals

- Every indexable page sets its own absolute canonical. Do not rely on inheritance.
- A canonical declared in a root/layout metadata object applies to every child that does not override it. New pages that forget to set one silently canonicalise to the home page.
- Filtered and search URLs (`?q=`, `?category=`) canonicalise to the clean listing unless they are deliberate landing pages with unique content.
- Paginated pages canonicalise to themselves, not page 1.
- Canonical, sitemap URL, internal links and redirects must all agree on the same host and trailing-slash form.

## 4. robots.txt vs noindex

- `robots.txt` controls crawling. `noindex` controls indexing. They do not combine: if robots.txt blocks a URL, Google cannot read its `noindex`, and the URL can still be indexed from links (shown without a snippet).
- To keep pages out of the index (admin, private share links, thank-you pages), allow crawling and send `noindex` via meta tag or `X-Robots-Tag` header.
- Block in robots.txt only what should never be fetched at all (API endpoints, infinite faceted spaces).
- Reference the sitemap in robots.txt.
- Decide deliberately about AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended). Blocking them removes the site from those assistants' answers.

## 5. Sitemaps

- Include only canonical, indexable, 200-status URLs. Exclude noindex, redirected and thin taxonomy pages.
- `lastmod` must reflect the last meaningful content change. Google uses it only when it is consistently accurate; a value that never changes, or changes on every request, is ignored. `changefreq` and `priority` are ignored by Google.
- Drive `lastmod` from content data (a per-page `updatedAt` or `lastReviewed`) rather than one hardcoded date for everything.
- Split above 50,000 URLs or 50 MB; use a sitemap index.
- After significant changes, resubmit in Search Console and ping IndexNow.

## 6. Rendering: what crawlers see

Google renders JavaScript, but later and not always fully; most AI crawlers and many social scrapers do not run JavaScript at all. Treat the raw HTML as the source of truth.

Patterns that empty the server HTML while the browser looks fine:
- Route-level loading states (a spinner in `<main>` with the real content streamed into a hidden container).
- Page templates that start content at `opacity: 0` until hydration.
- Entrance animations (framer-motion `initial`, AOS, GSAP) whose start state is server-rendered as `style="opacity:0"`. The text is in the HTML but invisible until JavaScript runs, which delays LCP and can read as hidden text. Count occurrences: `curl -s URL | grep -o 'opacity:0' | wc -l`.
- Components loaded with `ssr: false` / client-only dynamic imports. Acceptable for the interactive widget itself, but the H1, intro, explanation and FAQs around it must be server-rendered.
- Reading query parameters during render in a way that forces the whole page to client-render.
- Accordions and tabs that unmount inactive panels.
- Content fetched in `useEffect` after mount.

Check: fetch the page with a plain HTTP client, strip tags, and confirm the main copy is there (`scripts/seo_check.py` reports a visible word count and flags "Loading…" mains). Some frameworks stream metadata, so a plain client may receive the layout's default `<title>` while Googlebot gets the real one; fetch with a Googlebot user agent to compare.

## 7. Hosts, redirects, HTTPS

- One canonical origin (`https://example.com` or `https://www.example.com`). Every other variant 301s to it in a single hop.
- HTTPS everywhere, HSTS once stable, certificate auto-renewal monitored.
- When changing URLs: 301 old → new, update internal links and the sitemap, keep redirects indefinitely.
- No redirect chains; no 302 for permanent moves.

## 8. Core Web Vitals

Thresholds at the 75th percentile of real users: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1. CWV is a modest ranking factor but affects every page.

Common fixes:
- LCP: server-render the hero, preload the LCP image, avoid client-only rendering of above-the-fold content, self-host fonts with `font-display: swap`.
- INP: break up long tasks, defer non-critical third-party scripts (tag managers, chat widgets, ads), avoid heavy work in input handlers.
- CLS: dimensions on images/ads/embeds, reserve space for late content, avoid inserting banners above content.

Lab tools (Lighthouse) catch regressions; field data (CrUX, Search Console CWV report) is what Google uses. Use `seo-performance`, `seo-google` or `seo-unlighthouse` for measurement.

## 9. International (hreflang)

Only when the site serves the same content in multiple languages or regions: reciprocal `hreflang` annotations on every variant, plus `x-default`, with each variant self-canonical. Use the `seo-hreflang` skill.

## 10. Framework notes: Next.js App Router

Read the project's installed Next.js docs before writing metadata code; APIs change between majors.

- **Metadata inheritance**: `metadata` and `generateMetadata` merge down the tree. A root `alternates.canonical` or `robots` reaches every page that does not override it. Set canonical per page.
- **`generateMetadata` miss branch**: return a complete object with `robots: { index: false, follow: false }`, never a partial object that inherits the parent's canonical.
- **Unknown dynamic params**: with `generateStaticParams`, set `export const dynamicParams = false` so unknown slugs 404 at the router before streaming starts.
- **Runtime collections** (CMS posts, tags): a 200 is unavoidable once streaming starts, so the noindex miss branch is the safety net. Use fetchers that throw on network/API failure; only a confirmed "not found" response should trigger `notFound()` or noindex.
- **`loading.tsx`** at a route level puts a fallback into `<main>` and streams the content separately. Avoid it on SEO pages; use small Suspense boundaries around slow widgets instead.
- **`template.tsx`** animations that start at `opacity: 0` hide content until hydration. Use CSS-only animations that do not depend on JS.
- **`useSearchParams()`** in a client component without a Suspense boundary bails the tree out to client rendering. Read `searchParams` in the server page and pass values down as props. Check the build's route table after changes (static vs dynamic).
- **`next/dynamic` with `ssr: false`**: keep it to the interactive widget; render headings and explanatory content in server components.
- **Streamed metadata**: verify titles with a Googlebot user agent.
- **Third-party scripts that must be in raw HTML** (verification snippets, ad tags) belong in a plain `<script>` in `<head>`; `next/script` defaults inject after hydration.
- **`NEXT_PUBLIC_*` variables** are inlined at build time. If they gate SEO-relevant output (analytics, verification), they must exist in the build environment.
- **Files**: `app/sitemap.ts`, `app/robots.ts`, `app/manifest.ts`, `opengraph-image.tsx` per route. Use `headers()` in `next.config` for `X-Robots-Tag` on private paths.
- **Verifying a shared-component change**: build before and after, then diff the prerendered HTML under `.next/server/app/**/*.html` after normalising chunk hashes and build IDs.

## 11. Framework notes: SPAs (React/Vue/Vite) and others

- A pure client-rendered SPA ships an empty `<div id="root">`. For pages that need to rank, use SSR/SSG (Next, Nuxt, Astro, Remix/React Router framework mode, SvelteKit) or prerender those routes at build time.
- Set per-route title/meta/canonical in the server output, not only via client-side head managers.
- Configure the host so unknown routes return 404, not the SPA shell with 200.
- WordPress/CMS: one SEO plugin, no duplicate meta output, noindex tag/date/author archives unless they are curated, check the theme's heading structure.

## 12. Verification commands

```bash
# Status, redirects and headers
curl -sI https://example.com/page
curl -sIL http://www.example.com/ | grep -iE '^(HTTP|location)'

# What Googlebot gets
UA='Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
curl -s -A "$UA" https://example.com/page | grep -oE '<title>[^<]*|rel="canonical"[^>]*|name="robots"[^>]*'

# Soft-404 probe
curl -s -o /dev/null -w '%{http_code}\n' https://example.com/blog/this-does-not-exist-123

# Full per-page report
python3 <skill-dir>/scripts/seo_check.py https://example.com/ https://example.com/page

# Every URL in the sitemap
python3 <skill-dir>/scripts/seo_check.py --sitemap https://example.com/sitemap.xml --limit 200
```
