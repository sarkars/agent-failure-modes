# Missing Self-Reflection for High-Stakes Output

## Issue: Agent skips a beneficial critique/revise pass on a high-stakes output, going straight to a single-shot answer where a reflection round would demonstrably have caught an error.

**Frequency**: Occasional

**Symptoms**
- High-stakes or irreversible-action-adjacent outputs ship from a single generation pass with no critique/verification step, even though the task type has a track record of benefiting from one
- Errors that a second reflection pass would typically catch (arithmetic mistakes, unchecked edge cases, contradicted earlier statements within the same output) reach the end user or downstream system unflagged
- Pipeline configuration applies the same fixed number of generation passes (usually one) to both routine, low-stakes requests and flagged high-stakes ones, with no branch based on stakes classification
- Post-incident review of a shipped error shows that a straightforward "review your answer for X" prompt, when run retroactively, would have caught the mistake before it shipped
- No task-type or output-category in the system is ever routed to a critique/revise step, even for categories explicitly documented elsewhere (runbooks, risk policy) as high-stakes

**Root Cause**
Agent skips a beneficial critique/revise pass on a high-stakes output, going straight to a single-shot answer where a reflection round would demonstrably have caught an error.

**Example**
```
An agent that drafts customer-facing legal notices for a subscription-billing product
generates a cancellation-and-refund notice in a single pass and sends it directly to the
templating system that emails customers, with no critique or review step regardless of notice
type. For a batch of enterprise accounts undergoing a contract-mandated pro-rated refund, the
agent's single-pass draft states an incorrect refund calculation basis (full-month proration
instead of the contractually specified daily proration), a category of error a second pass
explicitly prompted to "recheck the calculation against the referenced contract clause" would
likely have caught, since the contract clause was already present in the agent's context. The
notices go out to over a dozen enterprise customers before a customer's finance team flags the
discrepancy. Legal and support then have to issue corrected notices and manually verify refund
amounts for every affected account, and one customer escalates a formal complaint over the
inconsistency.
```

**Contributing Factors**
- No difficulty/stakes classifier routes high-stakes outputs into a mandatory reflection pass; reflection (where it exists at all) is applied uniformly or not at all rather than being stakes-aware
- Added latency and token cost of a reflection pass is treated as a strict pipeline cost to minimize everywhere, without weighing it against the cost of an error in the specific high-stakes category
- No catalog exists mapping output categories (legal notices, financial calculations, irreversible account actions) to their documented error rate reduction from reflection, so there's no data-driven basis for deciding where to apply it
- Team conflates "we tried self-reflection once and it added cost with unclear benefit" (measured on low-stakes traffic) with "self-reflection isn't worth it," never re-testing it specifically on the high-stakes subset

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Flagged-high-stakes output routing | An input tagged as high-stakes by the stakes classifier (e.g., financial notice, irreversible account action) | Pipeline invokes a critique/revise pass before finalizing output | Output is finalized after a single generation pass with no reflection step logged |
| Reflection catch-rate benchmark | A set of high-stakes tasks with known, injected errors that a review pass should catch (miscalculation, contract-clause mismatch) | Reflection pass identifies and corrects the injected error before output ships | Single-pass and reflected output are identical; injected error ships uncorrected |
| Stakes-classifier coverage audit | Full catalog of output categories the agent produces | Every category documented as high-stakes in policy/runbooks maps to a mandatory reflection step | A high-stakes category exists with no corresponding reflection routing rule |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| High-stakes reflection coverage | 100% of classifier-flagged high-stakes outputs go through a critique/revise pass | Audit pipeline logs for reflection-step invocation on outputs tagged high-stakes |
| Reflection catch rate on injected-error benchmark | >=70% of injected errors caught and corrected | Run the reflection pass on a benchmark of high-stakes tasks with known injected errors; measure correction rate |
| Escaped high-stakes defects post-reflection-rollout | Reduction of >=50% vs. pre-rollout baseline | Compare error rate in production high-stakes categories before and after mandatory reflection is enabled |

---

## Mitigation Strategies

### Prevention
1. **Stakes classifier with mandatory reflection routing**: Classify each output request by stakes/reversibility before generation, and hard-wire a critique/revise pass as a non-optional pipeline stage for anything above the stakes threshold.
2. **Targeted critique prompts, not generic review**: For each high-stakes category, write a critique prompt that checks the specific failure modes known for that category (e.g., "recheck the refund calculation against the cited contract clause") rather than a generic "review this for errors" pass, since targeted critique catches more than generic critique at similar cost.
3. **Cost/benefit re-evaluation per category**: Re-test whether reflection helps specifically on the high-stakes subset of each output category rather than relying on an aggregate test across all traffic, since aggregate results can mask a large benefit concentrated in a small high-stakes slice.

### Detection & Response
1. **Reflection-bypass audit**: Log every high-stakes-classified output alongside whether a reflection pass ran; alert when any ships without one.
2. **Retroactive reflection replay on incidents**: When a high-stakes output error reaches production, replay it through the category's critique prompt retroactively to confirm (and document) whether reflection would have caught it, closing the loop on whether the mitigation is correctly scoped.

### Architecture Patterns
1. **Stakes-gated generate-critique-revise loop**: A pipeline stage that classifies stakes, then conditionally runs generate -> critique -> revise for flagged categories and a single generate pass for everything else.
2. **Category-specific critique templates**: A registry of critique prompts keyed by output category, each encoding the known failure modes for that category, invoked automatically once a request is classified into it.
3. **Reflection audit trail**: Persist the pre-reflection draft, critique output, and post-reflection final output together so catch-rate and false-negative rate can be measured after the fact.

### Metrics
1. **high_stakes_reflection_coverage_pct**: Target: 100%; Alert threshold: <95%
2. **reflection_catch_rate_benchmark**: Target: >=70%; Alert threshold: <40%
3. **high_stakes_escaped_defect_rate**: Target: reduction of >=50% vs. baseline; Alert threshold: no improvement or regression vs. baseline

### Alerts
1. **High-Stakes Output Shipped Without Reflection** (P1 - Critical): Condition - an output classified as high-stakes is finalized with no reflection-step log entry. Action: block release of that output and page the pipeline owner to fix the routing gap.
2. **Reflection Catch Rate Below Benchmark** (P2 - Warning): Condition - catch rate on the injected-error benchmark drops below 40% after a prompt or model change. Action: review and revise the category's critique prompt before continuing rollout.
3. **High-Stakes Defect Recurrence** (P1 - Critical): Condition - a defect of a type the reflection pass was specifically designed to catch escapes to production despite reflection running. Action: treat as a critique-prompt gap; update the template and add the case to the benchmark.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| High-stakes reflection coverage | <95% |
| Reflection catch rate on benchmark | <40% |
| High-stakes escaped defects vs. baseline | No reduction or regression |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Reflection skipped on high-stakes output | Flagged output ships with no reflection-step log | High |
| Catch rate degradation | Benchmark catch rate falls below 40% | Medium |
| Defect recurs despite reflection | A targeted-critique-covered error type still escapes | High |

---

## Related Patterns

- [Redundant Self-Reflection Passes](../../../../operations/goals/cost-optimization/failures/redundant-self-reflection-passes.md) - the inverse failure of running reflection when it isn't needed; this pattern is the case of a stakes-aware gate being absent in the other direction, skipping reflection where it was warranted
- [Under-Planning Costly Rework](../../../../operations/goals/cost-optimization/failures/under-planning-costly-rework.md) - a related planning-level (rather than output-critique-level) failure to invest upfront effort proportional to task risk

## References

- [Evaluating LLM Self-Reflection Loops: The 3 Metrics That Matter (2026)](https://futureagi.com/blog/evaluating-llm-self-reflection-loops-2026/) - reflection's quality benefit is real but task-dependent, and most production systems never measure whether it's engaged where it should be
- [Reflection-Driven Control for Trustworthy Code Agents](https://arxiv.org/pdf/2512.21354) - stakes-aware reflection control for trustworthy agent output
