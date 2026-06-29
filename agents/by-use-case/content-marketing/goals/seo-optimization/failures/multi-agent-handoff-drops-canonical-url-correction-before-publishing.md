# Multi-Agent Handoff Drops Canonical-URL Correction Before Publishing

## Issue: An SEO-Review Agent's Free-Text Notes Flagging and Correcting a Duplicate-Content Canonical-Tag Error Are Not Captured in the Structured Deploy Schema Passed to the Publishing Agent, Which Pushes the Page Live with the Original, Uncorrected Canonical Tag

**Frequency**: Occasional

**Symptoms**
- A page is published with a canonical tag pointing to a different, lower-priority URL, even though the SEO-review agent's review notes explicitly flagged the duplicate-content issue and specified the correct canonical target before handoff to publishing
- The structured deploy schema passed to the publishing agent includes fields for page slug, meta title, and meta description, but has no field for a canonical-tag correction noted only in the SEO-review agent's free-text review comments
- Asking the publishing agent why the correction was not applied shows it received only the standard structured deploy fields and had no input describing the canonical-tag fix from the SEO-review agent's notes
- The miss concentrates on canonical corrections identified during ad hoc SEO review rather than during the standard page-template configuration, since those are exactly the corrections that fall outside the deploy schema's predefined fields
- Search-console reporting showing duplicate-content cannibalization between the two URLs is typically how the gap is discovered, well after the page has been live and indexed with the incorrect canonical tag

**Root Cause**
The handoff between the SEO-review agent, which reviews a draft page and produces free-text notes flagging issues like a duplicate-content canonical-tag error, and the publishing agent, which deploys the page from a fixed structured schema, has no mechanism for surfacing a correction that does not map to one of the schema's predefined fields. The SEO-review agent's notes record the flagged issue and the correct canonical target, but nothing in the handoff forces a check for "does this page's SEO-review notes contain a canonical-tag correction not represented in the structured deploy fields" before the publishing agent proceeds, so a real, search-ranking-affecting correction is silently dropped at the agent-to-agent boundary.

**Example**
```
SEO-review agent reviews a new product-comparison page and notes: "This page duplicates content already covered by /products/comparison-guide -- canonical tag should point to that URL, not self-reference"
SEO-review agent hands off to the publishing agent using the standard structured deploy schema: page slug, meta title, meta description -- no field exists for "canonical-tag override"
Publishing agent deploys the page with the default self-referencing canonical tag, since the correction was never represented in the structured fields it received
Search console later reports both URLs competing for the same query terms, with ranking diluted across both, discovered only when an organic-traffic review flags the cannibalization weeks after the page went live
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems show a recurring failure mode where information established in one agent's reasoning or review process is not correctly specified or transferred to a downstream agent operating on a fixed schema | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Generalist multi-agent systems require explicit mechanisms for passing task-relevant context between agents with different input schemas, and gaps in this transfer are identified as a common source of downstream task failure | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |
| Audits of agentic workflow failures in production platforms identify schema mismatches at agent-to-agent handoff boundaries as a recurring root cause of dropped task-relevant information | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- The deploy schema passed between the SEO-review and publishing agents has no field for a canonical-tag override flagged during ad hoc review
- No check runs before publishing to compare the SEO-review agent's notes against the structured deploy fields for an unrepresented correction
- Canonical-tag issues identified during ad hoc review are especially likely to fall outside the schema, since the schema's canonical-tag default is set by page template rather than by per-page review

---

## Mitigation Strategies

1. **Canonical-Override Field in Deploy Schema**: Add a structured "canonical-tag override" field to the SEO-review-to-publishing handoff schema that the SEO-review agent is required to populate whenever its review notes flag a duplicate-content or canonical-correction issue
2. **Pre-Publish Review-Notes Reconciliation Check**: Before publishing, require a check that compares the SEO-review agent's notes against the structured deploy fields and flags any canonical-tag correction not represented in the schema
3. **Human SEO-Lead Review Gate for Flagged Corrections**: Route any page with a populated canonical-override field to human SEO-lead confirmation before publishing, rather than allowing the publishing agent to resolve it automatically
4. **Review-to-Publish Traceability Log**: Maintain a log linking each published page to the SEO-review notes it was derived from, so a missing canonical correction can be caught by audit before it affects search rankings

### Metrics
- Rate of published pages later found, on audit, to omit a canonical-tag correction present in the SEO-review notes
- Rate of deploy handoffs with a populated "canonical-tag override" field versus handoffs where a downstream audit found a correction that should have been populated but wasn't
- Average time between page publishing and canonical-tag-gap detection via search-console cannibalization reporting

### Alerts
- A page is published with a canonical-tag correction present in the SEO-review notes but absent from the structured deploy fields → P2
- Search-console reporting flags duplicate-content cannibalization between two URLs where one page's SEO-review notes had flagged the correct canonical target → P2
- Rate of pages requiring post-publish canonical-tag correction exceeds the defined threshold for a rolling window → P3

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
