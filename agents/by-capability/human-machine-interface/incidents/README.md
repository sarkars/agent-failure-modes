# Incidents: Real Cases Behind the Patterns

**Each page here describes one dated, public case of an assistant failing people, what happened, and which pattern it matches.** Incident pages are evidence, not commentary: every fact has a source we opened.

## Check the site first
The published site already has incident pages (for example Air Canada's invented refund policy and McDonald's AI drive-thru shutdown) in its `src/content/incidents/` folder. **Before writing a new incident, check that folder and link to the existing page.** Add a new one only for a case the site does not have.

## Format (matches the site's incident collection)
Each page is `<short-name>.md` with this front matter, which the site's Astro content schema requires:

```
---
title: "Short, factual title"
date: 2024-02-14            # date of the event or ruling
source: "https://..."       # the primary source (ruling, regulator notice, report)
summary: "One or two sentences."
categories: [Governance]    # existing site categories
patterns: [pattern-slug]    # site slugs of the patterns it matches
---
```

The body has three short parts: what happened (two or three sentences with dates as the source reports them), **Pattern match** (which written patterns it matches and why), and **The fix** (one sentence).

## Rules
- Never describe an incident you did not read about in a source you opened. Mark each source *opened* or *read through a summary* in the review note, not in the page.
- Prefer the original filing, ruling, regulator notice, or report over news coverage.
- Do not name or quote private individuals beyond what the source publishes.
- Do not guess at causes. Say "the source does not explain why."
- If no good source exists, there is no page.

## Related
- [Content program](../roadmap/content-program.md)
