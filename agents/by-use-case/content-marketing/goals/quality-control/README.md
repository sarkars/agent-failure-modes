# What Are the Most Common Quality Control Failures in AI Agents?

**Quality control fails when a content-generation pipeline skips fact-checking for statistical claims, treats a previously-approved similar claim as confirming evidence for a new claim with different underlying numbers, approximates QC policy thresholds from stale knowledge rather than querying the live policy tool, or drops a statistical caveat (time window, population scope, expiration date) at a multi-agent handoff.** Quality-control failures are distinct from compliance failures in that they involve internal accuracy and substantiation standards rather than external regulatory requirements, but they operate through the same mechanisms: claims that sound right without being verified, retrieval that confuses similarity with relevance, and handoff schemas that lose conditional information.

## Key Takeaways

- 5 patterns are documented, spanning four distinct failure mechanisms: skipped fact-checking on statistical claims, similarity-based confirmation confusion, stale-knowledge override of live policy, and caveat loss at handoffs.
- [Fact-check skipped on statistical claims](failures/fact-check-skipped-on-statistical-claims.md) shows that quality-control checklists often prioritize comparative-claim substantiation (usually legally mandated) over general statistical fact-checking, leaving a gap where non-comparative figures (adoption rates, growth percentages, research citations) pass through without source verification.
- [Embedding retrieval treats mismatched prior claim as confirming precedent](failures/embedding-retrieval-treats-mismatched-prior-claim-as-confirming-precedent.md) documents that claim templates reused across reporting periods (year-over-year growth statements) produce near-identical embeddings despite different underlying numbers, so a precedent-similarity check confirms the new claim's structure but not its current accuracy.
- [Stale training-corpus quality threshold overrides live QC policy tool](failures/stale-training-corpus-quality-threshold-overrides-live-qc-policy-tool.md) and [AI-generated content disclosure omission](failures/ai-generated-content-disclosure-omission.md) show QC gates requiring live tool calls or updated reference tables — a static prompt or generic best-practice is not a substitute for current policy.

## Scope

- **Fact-Checking Gaps** — [fact-check-skipped-on-statistical-claims](failures/fact-check-skipped-on-statistical-claims.md), [embedding-retrieval-treats-mismatched-prior-claim-as-confirming-precedent](failures/embedding-retrieval-treats-mismatched-prior-claim-as-confirming-precedent.md). Both involve statistical accuracy without legal mandates, where QC often treats them as lower-priority than substantiation-for-comparative-claims checks.
- **Policy and Requirement Updates** — [stale-training-corpus-quality-threshold-overrides-live-qc-policy-tool](failures/stale-training-corpus-quality-threshold-overrides-live-qc-policy-tool.md), [ai-generated-content-disclosure-omission](failures/ai-generated-content-disclosure-omission.md). Both require live policy queries or maintained reference tables that reflect current rules, not generic best-practices or older guidance.
- **Handoff and Caveat Loss** — [multi-agent-handoff-drops-fact-checkers-statistical-caveat-before-publishing](failures/multi-agent-handoff-drops-fact-checkers-statistical-caveat-before-publishing.md). A fact-checking agent's caveat (time window, population scope) is dropped because the handoff schema has no field for it.

## When Quality Control Matters

- Multi-stage content pipelines where fact-checked content may be transformed by later stages (SEO optimization, formatting) that don't re-verify facts, so an earlier stage's caveat can be lost or altered
- Campaigns reusing claim templates across multiple reporting periods (quarterly earnings content, annual state-of-business reports), where year-over-year claim phrasing can mask different underlying numbers
- Content marketing in data-heavy industries (business intelligence, enterprise software, financial services) where statistical claims and adoption metrics are a primary form of persuasion and require rigorous fact-checking

## Cross-Pattern Insight

All five quality-control patterns center on the same architectural gap: QC is treated as a static text-check or a similarity-based confirmation when it is actually a cross-verification problem requiring three distinct steps: (1) a current tool call to live policy or a verification call to a current source (not a memory of an old rule), (2) scope-matching or numerical validation (not just topical similarity), and (3) caveat and condition tracking across multi-stage handoffs. A statistical claim can look fluent without being verified; a similar prior claim can be used as confirming precedent without checking that the underlying data actually applies; and a time-scoped or population-scoped caveat can be dropped silently at a handoff unless the schema explicitly carries it. The recurring mitigation is making verification explicit: mandatory source calls, numerical diff checks, and extended handoff schemas that carry conditional information.

## Frequently Asked Questions

### Should general statistical fact-checking be as rigorous as comparative-claim substantiation?
[Fact-check skipped on statistical claims](failures/fact-check-skipped-on-statistical-claims.md) argues yes. While comparative and superiority claims are legally mandated to be substantiated in regulated industries, general statistical claims carry comparable reputational risk if wrong — a false adoption metric or misattributed research propagates as freely as a false comparative claim. A fact-checking gate that prioritizes comparative claims only is leaving a documented quality gap.

### Can a previously-approved similar claim be used to confirm a new claim?
No. [Embedding retrieval treats mismatched prior claim as confirming precedent](failures/embedding-retrieval-treats-mismatched-prior-claim-as-confirming-precedent.md) shows that confirming a new claim based on similarity to a prior approved claim only verifies the structure and phrasing are correct; it does not verify the underlying numbers are current or applicable. Recurring claim templates (year-over-year statements) produce near-identical embeddings despite year-over-year number changes, so a precedent check is no substitute for an independent source-data verification of the new claim.

### If a quality-control policy tool is available, should it always be called?
Yes. [Stale training-corpus quality threshold overrides live QC policy tool](failures/stale-training-corpus-quality-threshold-overrides-live-qc-policy-tool.md) shows agents often substitute their own understanding (absorbed from training or from an earlier project phase) for a fresh tool call, applying thresholds the live policy has since tightened. The only reliable fix is to make the policy-tool call mandatory and non-optional, logged and auditable, for every QC judgment.

### What happens to a statistical caveat that was approved conditionally?
[Multi-agent handoff drops fact-checkers statistical caveat before publishing](failures/multi-agent-handoff-drops-fact-checkers-statistical-caveat-before-publishing.md) documents exactly this failure: a fact-check approves a statistic only with a caveat (time window, population scope), but the handoff schema has no field for caveats, so the publishing agent never sees it. The fix is extending the schema to carry caveat information explicitly, with a human review gate on any handoff with a populated caveat field.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Fact-Check Skipped on Statistical Claims](failures/fact-check-skipped-on-statistical-claims.md) | Quantitative claim is approved without verifying a source or checking the claim's accuracy |
| [Embedding Retrieval Treats Mismatched Prior Claim as Confirming Precedent](failures/embedding-retrieval-treats-mismatched-prior-claim-as-confirming-precedent.md) | New claim is treated as confirmed by a similar prior-approved claim with different underlying data |
| [AI-Generated Content Disclosure Omission](failures/ai-generated-content-disclosure-omission.md) | Content published without required AI-disclosure label because QC checklist had no gate for disclosure-requirement applicability |
| [Multi-Agent Handoff Drops Fact-Checker's Statistical Caveat Before Publishing](failures/multi-agent-handoff-drops-fact-checkers-statistical-caveat-before-publishing.md) | Fact-checker approves a claim only with a caveat (scope, time window, expiration); the caveat is not represented in the handoff schema so is dropped downstream |
| [Stale Training-Corpus Quality Threshold Overrides Live QC Policy Tool](failures/stale-training-corpus-quality-threshold-overrides-live-qc-policy-tool.md) | QC agent applies quality standards from stale knowledge rather than calling a live policy tool that has since been updated |

**Total: 5 patterns**

## Related Goals

- [Compliance](../compliance/) — both involve verification and substantiation, but compliance checks against external regulations while quality control enforces internal standards
- [Brand Consistency](../brand-consistency/) — both support content quality overall, but consistency checks voice and tone while quality control checks factual accuracy
