# Fact Generalization Error

## Issue
An agent takes a fact that is true only under narrow, specific conditions — a particular study population, a specific product configuration, a specific regulatory jurisdiction — and presents it as a general truth applicable broadly. The source fact isn't misquoted; the error is in stripping away the scope that made it narrowly true and applying it as if it held universally.

**Frequency**: Very Common

**Symptoms**
- Agent output states a narrowly-scoped fact without any of its original qualifying conditions
- The fact is technically sourced correctly, but the source explicitly limits it to a subset the agent's answer doesn't mention
- Errors increase when the query is phrased in general terms even though the best-matching retrieved source is narrow
- Users apply the generalized claim to cases the original narrow finding never covered, with predictably worse-than-expected results

## Root Cause
Retrieval and summarization compress source text, and specificity markers — sample descriptions, population definitions, configuration prerequisites — are exactly the kind of detail that gets trimmed first when a passage is condensed to fit a response, because they read as secondary to the "headline" claim. Generation models are also trained on a strong prior toward confident, general-sounding statements, since hedged and narrowly-scoped claims are less common and less rewarded in typical training distributions. The combination — compression that strips scope markers plus a generation bias toward unqualified statements — means narrow findings default to sounding general unless something actively preserves and asserts the boundary.

## Example
```
A source study finds: "Among trial participants aged 65+ with prior
cardiovascular history, Drug X reduced recurrence risk by 34% over 24
months." The study explicitly did not enroll or draw conclusions about
patients under 65 or without prior cardiovascular history.

A user without cardiovascular history, age 40, asks a health-information
agent whether Drug X reduces recurrence risk. The agent retrieves the
study and answers: "Yes, studies show Drug X reduces recurrence risk by
34% over 24 months" — generalizing a finding specific to an older,
cardiovascular-history population to the general population, dropping
both qualifying conditions in the process.

The user's actual risk-reduction from the drug, given their different
risk profile, may be substantially different from the cited figure,
which was never established for someone in their situation.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 25-40% of statistics cited from population-specific or condition-specific studies are presented without their scoping population/condition in agent-generated summaries | Estimated from summarization-fidelity audits of scientific/medical source material |
| General-phrased user queries produce a higher rate of unscoped generalization than queries that explicitly name the population/condition of interest | Typical pattern observed in retrieval-QA evaluation |
| Explicit scope-preservation instructions in the summarization step reduce generalization errors substantially in tested pipelines | Reported range across teams that added scope-preservation prompting/checks |

## Mitigations
1. **Scope-marker extraction and forced retention**: At ingestion, explicitly extract population/condition/configuration scope markers from source facts as structured metadata, and require the generation step to include them whenever the fact is cited, rather than treating them as droppable prose.
2. **Scope-mismatch flagging at query time**: Compare the scope of the best-matching source fact against the scope implied by the user's query, and explicitly flag when they don't match (e.g. "this finding is specific to patients 65+ with cardiovascular history — is that your situation?").
3. **Anti-generalization prompting**: Instruct the generation step to preserve rather than compress scope qualifiers, and to explicitly state "this is specific to X" rather than defaulting to unqualified phrasing for narrow findings.
4. **Scope-aware confidence calibration**: Lower the agent's confidence framing when citing a narrowly-scoped fact for a query outside that scope, rather than presenting the extrapolation with the same confidence as an in-scope citation.
5. **Post-generation scope audit**: Automatically compare generated claims against source scope metadata and flag mismatches for review before the response is finalized, particularly in health/financial/legal domains.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| scope_qualifier_retention_rate | Share of cited narrow-scope facts whose scope qualifier survives into the final response | Alert if < 85% |
| out_of_scope_citation_rate | Rate at which narrowly-scoped facts are cited for queries outside their documented scope, without a scope mismatch flag | Alert if > 5% |
| generalization_correction_rate | Rate of expert/user corrections identifying an over-generalized claim | Track trend; alert on sustained increase |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unscoped citation in high-stakes domain | A narrowly-scoped medical/financial/legal fact is cited without its qualifier for an out-of-scope query | High | Retract/correct the response, add case to scope-audit test set |
| Scope qualifier retention drop | scope_qualifier_retention_rate falls below threshold after a summarization pipeline change | Medium | Review recent summarization prompt/pipeline changes for scope-stripping regressions |

## Related Patterns
- [Fact Partial Truth](./fact-partial-truth.md) - closely related; generalization error is the specific case where the dropped qualifier is the fact's applicable scope
- [Knowledge Scope Assumption Wrong](./knowledge-scope-assumption-wrong.md) - shares the scope-mismatch mechanism, framed at the level of jurisdiction/version rather than population/condition
- [Fact Probabilistic Mismatch](./fact-probabilistic-mismatch.md) - a related over-confidence failure where a conditional/probabilistic finding is stated as a flat certainty
