# Structured data (JSON-LD)

Structured data helps Google understand a page and makes it eligible for rich results. It never compensates for weak content, and markup that does not match visible content can trigger a manual action.

## Which types to use

| Page | Types | Rich result today? |
|---|---|---|
| Every page (once, site-wide) | `Organization` (name, url, logo, `sameAs` social profiles, contactPoint), `WebSite` (name, url) | Organization logo and knowledge panel signals; site name in results |
| Tool / web app | `WebApplication` or `SoftwareApplication` with `applicationCategory`, `operatingSystem`, `offers` (price 0) | Software app rich result needs `aggregateRating` or `review` from **real** users. Never fabricate ratings |
| Article / blog post | `Article` or `BlogPosting` with `headline`, `image`, `datePublished`, `dateModified`, `author` (**Person** with `url` to an author page), `publisher` | Article enhancements in Top stories/Discover |
| Any nested page | `BreadcrumbList` | Breadcrumb trail in results |
| Listing / hub | `CollectionPage` + `ItemList` | No rich result; helps understanding |
| FAQ section | `FAQPage` | Rich result only for authoritative government/health sites since 2023; keep it for semantics, do not promise rich snippets |
| How-to content | `HowTo` | Rich result deprecated (2023); optional |
| Product | `Product` with `offers`, `aggregateRating`, `review` | Yes: price, availability, ratings |
| Local business | `LocalBusiness` subtype, address, geo, hours | Supports local panel; use the `seo-local` skill |
| Video | `VideoObject` | Video rich results / key moments |
| Event, Recipe, JobPosting, Course | Their own types | Yes, with strict required fields |

The `WebSite` → `SearchAction` (sitelinks search box) markup no longer produces a search box; Google retired the feature in 2024. It is harmless but unnecessary.

Google simplified its supported types further in 2025. Check the current list in the Search Gallery (developers.google.com/search/docs/appearance/structured-data/search-gallery) before promising a rich result.

## Rules

- JSON-LD in `<script type="application/ld+json">`, rendered on the server.
- Only mark up what is visible on the page. FAQ answers in JSON-LD must also be in the HTML.
- Absolute URLs everywhere.
- One canonical `Organization` with a stable `@id` (`https://example.com/#organization`); reference it from other nodes (`publisher: { "@id": ".../#organization" }`) instead of repeating it with different values.
- Prefer `Person` authors with an author page for articles; Organization-only authorship is weak for E-E-A-T.
- Keep `dateModified` honest; it should change only when content changes.
- Never add `aggregateRating` or `review` that is not backed by real, visible user reviews collected by the site itself. Ratings from App Store, Play Store, G2, Trustpilot or any other site must not be copied into your markup; Google's review-snippet guidelines forbid aggregating third-party ratings. Link to those profiles instead.
- **Escape JSON-LD output.** `JSON.stringify` does not escape `<`, so a CMS title containing `</script>` breaks out of the tag. Replace `<` with `<` when serialising:

```ts
const json = JSON.stringify(schema).replace(/</g, '\\u003c');
<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: json }} />
```

## Example: tool page graph

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebApplication",
      "@id": "https://example.com/tools/json-formatter#app",
      "name": "JSON Formatter",
      "url": "https://example.com/tools/json-formatter",
      "applicationCategory": "DeveloperApplication",
      "operatingSystem": "Any",
      "isAccessibleForFree": true,
      "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
      "featureList": ["Validate JSON with line-level errors", "Prettify and minify", "Runs in the browser"],
      "publisher": { "@id": "https://example.com/#organization" }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/" },
        { "@type": "ListItem", "position": 2, "name": "Tools", "item": "https://example.com/tools" },
        { "@type": "ListItem", "position": 3, "name": "JSON Formatter", "item": "https://example.com/tools/json-formatter" }
      ]
    }
  ]
}
```

## Validate

- Rich Results Test (search.google.com/test/rich-results) for eligible types.
- Schema Markup Validator (validator.schema.org) for general correctness.
- Search Console → Enhancements reports after deploy.
- The `seo-schema` skill for detection, validation and generation across many pages.
