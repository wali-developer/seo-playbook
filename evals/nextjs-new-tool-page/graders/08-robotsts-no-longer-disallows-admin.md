---
type: llm
focus: trace
weight: 1
---

robots.ts no longer disallows /admin/ (relying on the page's noindex), or the response explicitly flags the conflict that a robots.txt disallow prevents crawlers from reading noindex.
