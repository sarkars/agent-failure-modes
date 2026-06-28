# Herbal & Supplement Interaction Blindness

## Issue: Agent Checks Prescription-Drug Interactions but Ignores Patient-Reported Supplements and Herbal Products

**Frequency**: Common

**Symptoms**
- Patient-reported "vitamins" or "natural supplements" are recorded as free text and excluded from structured interaction checks
- St. John's Wort, ginkgo, and other herbs with well-documented pharmacokinetic interactions are not cross-checked against new prescriptions
- Agent's interaction summary states "no interactions found" while only having queried the structured medication list
- Supplement-induced interaction discovered only after adverse event or ineffective therapy

**Root Cause**
Interaction databases (RxNorm, DDI sets) are built around regulated pharmaceuticals with standardized identifiers. Herbal and dietary supplements are reported inconsistently as free text, often without a matching code, so structured interaction-checking pipelines silently skip them. An LLM agent that queries "the medication list" rather than parsing the full intake history will not see supplements unless explicitly told to extract and normalize them first.

**Example**
```
Scenario: Patient on sertraline (SSRI) self-reports "taking St. John's Wort for mood"
Agent: Logs supplement as free-text note, does not map to a drug interaction code
New prescription: Tramadol added for pain
Interaction check: Passes (tramadol-sertraline checked; St. John's Wort not in structured field)
Missed interaction: St. John's Wort + SSRI + tramadol → elevated serotonin syndrome risk
Impact: Preventable serotonin syndrome risk goes unflagged
```

**Key Statistics**
- A large share of patients on prescription medication also use herbal or dietary supplements, and most do not disclose this unless directly and specifically asked
- Documented clinically significant herb-drug interactions exist for commonly used supplements including St. John's Wort, ginkgo, garlic, and ginseng
- Supplement use is disproportionately under-captured in structured EHR medication fields compared to free-text intake notes

---

## Mitigation Strategies

1. **Mandatory Supplement Extraction**: Require the agent to parse free-text intake notes for supplement/herbal mentions and normalize them to a known interaction-checkable entity before running any interaction check
2. **Explicit Supplement Prompt**: Add a structured intake question ("any vitamins, herbs, or supplements?") whose answer is routed into the same interaction pipeline as prescriptions
3. **Herb-Drug Interaction Table**: Maintain a dedicated herb/supplement-to-drug-class interaction table separate from but queried alongside the standard DDI database
4. **Unmapped-Substance Flag**: If a reported substance cannot be mapped to a known interaction entity, flag it for pharmacist review rather than silently dropping it

### Metrics
- % of patient-reported supplements successfully mapped to an interaction-checkable entity
- Rate of "no interactions found" results where supplement fields were non-empty but unmapped
- Adverse events attributable to herb-drug interactions post-deployment

### Alerts
- Unmapped supplement co-occurring with a new prescription known to interact with common herbs → P1
- "No interactions found" returned with non-empty free-text supplement field → P2

---

## References

- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
- [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482)
