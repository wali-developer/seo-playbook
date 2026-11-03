# seo-playbook

A hands-on SEO skill for Claude Code (and other agents that read `SKILL.md` skills). It gives an agent one repeatable workflow for making pages rank:

1. **Find winnable keywords**: it reads the live SERP before committing, prioritises the long tail on young domains, and builds a keyword map with one primary keyword per URL.
2. **Implement on-page SEO**: titles, descriptions, H1s, a page content model, FAQs, internal links, structured data and trust signals.
3. **Pass the technical checks**: real 404s instead of soft 404s, per-page canonicals, server-rendered content, honest sitemaps, and `noindex` without contradictory robots rules.
4. **Earn links**: a zero-budget off-page playbook (linkable assets, launches, directories, outreach templates, Bing and IndexNow).
5. **Measure and iterate** in Search Console: striking-distance queries, low CTR, cannibalisation.

The rules come from a real production site that went from zero to page-one rankings on long-tail queries. They include the bugs that quietly cost it rankings: soft 404s from streaming SSR, canonicals inherited from a layout, loading spinners and entrance animations that hide content from crawlers, and fabricated reviews.

## Install

```bash
# Personal skill (available in every project)
git clone https://github.com/wali-developer/seo-playbook.git ~/.claude/skills/seo-playbook

# Or per project
git clone https://github.com/wali-developer/seo-playbook.git .claude/skills/seo-playbook
```

Keep the target folder name `seo-playbook` so that it matches the skill's `name` field.

Claude Code picks the skill up automatically. It triggers when you build or edit public pages, touch routes, metadata, sitemaps or robots rules, or mention SEO, keywords, ranking, backlinks or Search Console. You can also invoke it explicitly with `/seo-playbook`.

## Quick mode and full mode

The skill picks a depth before it starts, because most SEO requests are small.

- **Quick mode** covers one or two pages where the keyword is known: retitling a page, writing a meta description, adding FAQs, fixing a flagged issue. The agent follows the project's existing SEO pattern and runs a five-point checklist without reading the reference files or researching live search results. Any bigger problem it notices is flagged and offered, not silently fixed.
- **Full mode** covers new sites and page sets, unclear keyword choices, "why isn't this ranking?", pre-launch audits and off-page plans. It runs the six-phase workflow with live SERP checks.

## What's inside

```
seo-playbook/
├── SKILL.md                      # workflow, hard-won rules, output formats
├── references/
│   ├── keyword-research.md       # free research sources, SERP winnability, keyword-map template
│   ├── on-page.md                # definition of done, titles, content model, FAQs, linking, E-E-A-T
│   ├── technical-seo.md          # indexability, soft 404s, canonicals, rendering, Next.js & SPA notes
│   ├── structured-data.md        # which schema types still earn rich results, JSON-LD rules
│   ├── off-page.md               # link earning ranked by effort/payoff, outreach templates
│   └── measurement.md            # Search Console workflow, position/CTR interpretation
├── scripts/
│   ├── seo_check.py              # crawl URLs, a sitemap or a local HTML file as Googlebot
│   └── gsc_opportunities.py      # quick wins from a Search Console export
└── evals/                        # test cases (see below)
```

Both scripts use only the Python 3 standard library.

```bash
python3 scripts/seo_check.py https://example.com/ https://example.com/pricing
python3 scripts/seo_check.py --sitemap https://example.com/sitemap.xml --limit 200
python3 scripts/seo_check.py --file dist/index.html --url https://example.com/
python3 scripts/gsc_opportunities.py export.json            # Search Analytics API rows (keys: [query, page])
python3 scripts/gsc_opportunities.py queries.csv --csv      # CSV with Query, Page, Clicks, Impressions, Position
```

## Optional companion skills

The playbook works on its own. If you also have narrower SEO skills installed (for example `seo-google` for Search Console and CrUX data, `seo-schema`, `seo-backlinks` or `seo-dataforseo`), it points the agent to them for deep single-topic audits and paid data sources.

## Tests

`evals/` holds six test cases in the format `claude plugin eval` reads:

| Case | What it checks |
|---|---|
| `nextjs-new-tool-page` | Adding a page to a Next.js project with nine planted SEO traps |
| `landing-page-review` | Reviewing a static landing page that has a leftover staging `noindex`, fake ratings and hidden FAQ schema |
| `gsc-export-prioritise` | Turning a Search Console CSV into a prioritised plan |
| `new-site-keyword-map` | Keyword research and a keyword map for a new domain |
| `offpage-launch-plan` | A zero-budget backlink and launch plan |
| `quick-title-update` | A one-page title and description change that should stay small and cheap (quick mode) |

Results from the last benchmark: one run per configuration, with the same model with and without the skill, against 61 graded checks.

| Case | With skill | Without skill |
|---|---|---|
| nextjs-new-tool-page | 14/14 | 11/14 |
| new-site-keyword-map | 12/12 | 10/12 |
| offpage-launch-plan | 12/12 | 10/12 |
| landing-page-review | 13/13 | 12/13 |
| gsc-export-prioritise | 10/10 | 9/10 |
| **Overall** | **100%** | **85%** |

A capable model without the skill already catches most textbook SEO problems. The skill closes the gaps where advice goes wrong in practice:
- robots.txt disallow rules that hide a page's `noindex`
- third-party ratings copied into structured data
- treating nofollow community links as ranking boosts
- double-counted impressions
- unverified claims about the user's own site
- keywords whose search intent doesn't match the product
- launching dozens of near-identical pages at once

**Cost.** Full-mode tasks use about 1.6× the tokens and time of the same model without the skill, mostly reading references and checking live search results. Quick mode brings small edits close to baseline. In a single-page title and description change (`quick-title-update`), both configurations passed 5/5: 57k tokens and 98 s with the skill against 46k tokens and 64 s without, about 1.25×. Several checks were written after a first round of runs, to target differences seen there, and each configuration ran once, so read the scores as directional.

To run them with Claude Code (these are real, billed model runs):

```bash
cd ~/.claude/skills/seo-playbook
claude plugin eval . --allow-tools Write,Edit,Bash --scaffold
```

## License

MIT. See [LICENSE](LICENSE).
