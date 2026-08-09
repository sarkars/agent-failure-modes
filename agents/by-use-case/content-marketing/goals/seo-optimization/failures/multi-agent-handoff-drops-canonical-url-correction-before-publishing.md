# Multi-Agent Handoff Drops Canonical-URL Correction Before Publishing

## Issue: An SEO-Review Agent's Free-Text Notes Flagging and Correcting a Duplicate-Content Canonical-Tag Error Are Not Captured in the Structured Deploy Schema Passed to the Publishing Agent, Which Pushes the Page Live with the Original, Uncorrected Canonical Tag

**Frequency**: Occasional

**Symptoms**
- A newly published product-comparison page keeps its self-referencing canonical tag even though the SEO-review agent's own notes, minutes earlier, named the exact competing URL it should point to instead
- Every field in the deploy schema (slug, meta title, meta description) traces back to a per-page decision the template already anticipated; canonical tag is the one field the template assumes never varies per page, so no slot exists for an override once one is actually needed
- Pages whose SEO review surfaces a template-level exception show a consistently higher post-publish correction rate than pages whose review simply confirms the template defaults are fine
- The publishing agent, asked why it didn't apply the correction, reports it received a complete and valid deploy payload by its own schema's standard -- nothing in that payload indicated a correction existed
- Duplicate-content cannibalization in search-console reporting is typically the first anyone notices, arriving weeks after the page went live, long after the review agent's original note would have been easy to find

**Root Cause**
The deploy schema treats the canonical tag as a template-level default rather than a per-page attribute, because for the overwhelming majority of pages the template's self-referencing default is correct and no per-page override is ever needed. The SEO-review step was layered on afterward as a quality gate over an already-fixed publishing pipeline, so when that gate produces a genuine per-page exception, there is no field left in the schema to write it into -- extending the schema for a case the template was explicitly designed not to need was never part of either system's original scope.

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
