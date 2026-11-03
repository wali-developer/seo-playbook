---
type: llm
focus: trace
weight: 1
---

FaqAccordion keeps FAQ answers in the DOM when closed (e.g. hidden attribute, hidden="until-found", <details>, or CSS), instead of `{open === i && <p>}` unmounting them.
