# Off-page SEO: links, mentions and distribution

On-page work makes a page eligible to rank. For anything with real competition, links from relevant sites, brand searches and genuine mentions decide the order. Young sites stuck at positions 40–80 for head terms despite good pages almost always have an authority problem, not a copy problem.

## Contents
1. Principles and what to avoid
2. Tactics ranked by effort vs payoff for small sites
3. Linkable assets
4. Launch platforms and communities
5. Directories
6. Outreach
7. Visual and video platforms
8. Search engines beyond Google
9. Brand signals
10. The off-page kit deliverable
11. Tracking

---

## 1. Principles and what to avoid

- Earn links by making things worth linking to, then telling the right people.
- Relevance beats raw authority: one link from a developer newsletter is worth more to a dev-tools site than ten from generic directories.
- Natural anchor text: mostly brand and URL, some descriptive; exact-match keyword anchors in bulk look manipulative.
- Mark paid or sponsored placements `rel="sponsored"` and user-generated links `rel="ugc"`.
- Know which links pass ranking value. Links in GitHub READMEs, Reddit, Hacker News, Product Hunt, dev.to, Stack Overflow, Quora and most forums and social sites are `nofollow`/`ugc`. They are still worth having, because they bring referral visitors, get the product discovered, and lead to the editorial links (blog posts, roundups, docs) that do pass value. Do not tell the user a README badge or a Reddit post will lift rankings directly.
- Before any public post, fact-check every claim about the product (what runs client-side, supported formats, pricing). One wrong claim in a Show HN thread does more damage than no launch. Give the user a short "confirm these facts" table when you could not verify them yourself.

Do not: buy links, join private blog networks, do large-scale link exchanges, spam comments or forums, mass-submit to hundreds of directories, or publish scaled AI content on other sites for links. These violate Google's spam policies, and penalties are slow to undo.

## 2. Tactics ranked by effort vs payoff for small sites

| Tactic | Effort | Payoff | Fits |
|---|---|---|---|
| Search Console + Bing Webmaster Tools + IndexNow setup | Low | Indexing speed, Bing/Copilot/ChatGPT visibility | Everyone |
| Built-in viral loop ("Made with X" on shared output) | Low (once) | Brand searches, referral traffic | Products whose output gets shared |
| Curated directories and "alternatives" sites | Low | A few relevant links, referral traffic | SaaS, tools |
| Open-source repo or template linking back | Medium | Discovery, referral traffic, GitHub topic rankings (README links are nofollow) | Dev audiences |
| Launch posts (Show HN, Reddit, Product Hunt, Indie Hackers) | Medium | Spike plus follow-on links from people who write about it | New products/features |
| Genuinely helpful answers in communities | Medium, ongoing | Referral traffic, mentions | Everyone |
| Original data or a definitive guide (linkable asset) | High | The most durable links | Sites with a niche |
| Guest posts and podcasts on relevant sites | High | Strong contextual links | Founders with expertise |
| Journalist requests (Qwoted, Featured, Help a B2B Writer, Source of Sources) | Medium | High-authority mentions | Experts with quotable opinions |
| Broken-link and resource-page outreach | Medium | Contextual links | Sites with strong reference content |
| Unlinked brand mentions → ask for a link | Low | Easy links | Sites already being talked about |

## 3. Linkable assets

Content other sites cite:
- Free tools that solve a recurring task (calculators, formatters, generators).
- Templates and starter repos (with a README link back).
- Original data: surveys, benchmarks, aggregated public data with charts.
- Definitive references (size charts, error-code lists, cheat sheets).
- Embeddable widgets or badges with an attribution link.

Every cluster in the keyword map should have one asset designed to attract links, which then passes authority to the commercial pages through internal links.

## 4. Launch platforms and communities

Write each post for that community's norms. Lead with the interesting problem or build story, disclose that you made it, and answer every comment.

- **Hacker News (Show HN)**: technical angle, plain title, link to the product, no marketing language.
- **Reddit**: r/SideProject, r/InternetIsBeautiful, niche subreddits that allow self-promotion; read each subreddit's rules first.
- **Product Hunt**: schedule a launch, prepare gallery images and a maker comment; time it ahead of seasonal demand.
- **Indie Hackers, dev.to, Hashnode, Medium**: build logs and tutorials with a canonical link back where the platform allows it.
- **Stack Overflow, Quora, forums**: answer the question fully; link only when the tool genuinely solves it.
- **LinkedIn, X**: build-in-public posts; they create brand searches more than links.

## 5. Directories

Pick a handful of curated, relevant ones; skip "submit to 500 directories" services.
- Software/SaaS: AlternativeTo, SaaSHub, Product Hunt, G2/Capterra (B2B), There's An AI For That (AI tools), awesome-lists on GitHub (via pull request).
- Developer tools: GitHub awesome-lists, devhunt, free-for.dev style lists.
- Local businesses: Google Business Profile, Bing Places, Apple Business Connect, Yelp, industry and city directories with consistent NAP (use the `seo-local` skill).

## 6. Outreach

When reaching out (to bloggers listing tools, resource pages, journalists):
- Personalise the first line to their specific page.
- Say what you made and why it is useful to their readers, in two sentences.
- Make the ask easy (exact page, suggested placement).
- One polite follow-up after a week, then stop.

Template:

```
Subject: A free <tool> for your "<their article title>" list

Hi <name>,

Your list of <topic> tools helped me when <genuine detail>. I built <product>, a free <what it does> with <the one differentiator>: <url>.

If you update the list, it might be useful to your readers next to <similar tool they already list>. Happy to answer any questions.

<name>
```

## 7. Visual and video platforms

- **Pinterest** ranks in Google for visual queries (cards, designs, recipes, decor, quotes). One pin per page, using the OG image, page title as pin title, URL as link; bulk-upload by CSV, then add 3–5 pins a week.
- **YouTube / Shorts / Reels / TikTok**: 15–60 s screen recordings of the product doing something delightful. Video results appear for many "how to" queries.

## 8. Search engines beyond Google

- **Bing Webmaster Tools**: import from Search Console, submit the sitemap. Bing's index powers Copilot and feeds ChatGPT search, and it offers free backlink and keyword data.
- **IndexNow**: host a key file at the site root and POST changed URLs on deploy. Bing, Yandex, Seznam and Naver use it; Google does not. Use the `seo-bing` skill.
- **AI assistants**: being cited depends on crawlable HTML, clear self-contained answers, and brand mentions across the web. Use the `seo-geo` skill. An `llms.txt` file is optional; Google ignores it.

## 9. Brand signals

Brand searches ("<brand> json formatter") show Google that people seek the site out.

**Check for name collisions first.** Search the bare brand name on Google, GitHub, npm, PyPI, crates.io, app stores and Product Hunt. If an established package or product already owns it, brand queries will land on them. Recommend writing the full domain ("mdpdf.dev", "InvoiceKit.app") in every post, profile and anchor, and track the domain-form query in Search Console.
- Consistent brand name across the site, social profiles and directories.
- `Organization` JSON-LD with `sameAs` to every official profile.
- Share features that put the brand in front of new people (attribution on exported or shared output).
- Watch brand query impressions in Search Console as a health metric.

## 10. The off-page kit deliverable

When the agent cannot post or email on the user's behalf, hand over a kit (save it in the project docs):

1. **Target list**: platform/site, URL, why it fits, owner, status column.
2. **Post drafts** per platform, written to that platform's norms.
3. **Outreach drafts** for the top 10 link targets.
4. **Assets**: pin images, screenshots, demo GIFs, a GitHub template repo if relevant.
5. **Calendar**: dates tied to seasonal demand (links take weeks to be discovered; seasonal pages need them 1–2 months before the peak).

Ask before posting anything publicly or sending email; those actions are outward-facing and the user should approve them.

## 11. Tracking

- Search Console → Links report (top linking sites and anchors) monthly.
- Bing Webmaster Tools backlinks (free).
- Referral traffic in analytics per platform.
- Brand query impressions trend.
- For deeper profiles, `seo-backlinks` (Moz, Common Crawl, Bing) or `seo-ahrefs`/`seo-dataforseo` if configured.
