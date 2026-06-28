# Documentation-Driven Upcoding/Downcoding Risk

## Issue: Agent-Generated Clinical Note Language Inflates or Deflates Billing Code Level Relative to Actual Care Delivered

**Frequency**: Common

**Symptoms**
- Agent-drafted note includes boilerplate phrases ("comprehensive review of systems performed") that were not actually performed, inflating E/M code level
- Conversely, terse agent-generated summaries omit complexity factors (number of problems addressed, data reviewed) that were genuinely present, causing downcoding and revenue loss
- Note's documented complexity does not match the time or decision-making actually recorded elsewhere in the encounter
- Auto-suggested billing code is accepted by the clinician without independent verification against the note content

**Root Cause**
LLM scribes and note-drafting agents are trained to produce complete-sounding, well-structured clinical narratives, which biases them toward including standard template phrases regardless of whether each element was actually performed. Because billing codes are frequently derived algorithmically from note structure (counts of systems reviewed, data points discussed), inflated or padded language directly and mechanically shifts the suggested code, creating compliance exposure that has nothing to do with the actual clinical encounter.

**Example**
```
Scenario: Brief follow-up visit, single stable problem, no new data reviewed
Agent-generated note: Includes templated "10-point ROS negative" and "reviewed prior labs, imaging, and specialist notes"
Actual encounter: 2-point ROS, no records reviewed
Billing engine: Derives Level 4 E/M code from note content
Audit finding: Documentation does not support code level billed
Impact: Compliance exposure, potential payer clawback, audit risk
```

**Key Statistics**
- E/M coding audits frequently identify documentation-billing mismatches as a leading driver of payer-initiated clawbacks
- AI scribe tools that auto-populate templated exam/ROS language without source verification are flagged in early audits as a growing upcoding risk vector
- Underdocumentation (downcoding) from overly terse AI-generated notes has separately been shown to cause measurable revenue leakage in ambulatory settings

---

## Mitigation Strategies

1. **Source-Grounded Note Generation**: Generate each documented element (ROS item, data review, exam finding) only from an explicit signal in the encounter transcript or chart action, never from a template default
2. **Code-Justification Trace**: Require the agent to show which specific note elements justify the suggested billing code, so a clinician can verify each one was actually performed
3. **Clinician Attestation Step**: Require explicit clinician sign-off on any auto-suggested code, with the underlying justifying elements visible, not just the final code
4. **Audit Sampling**: Routinely sample agent-generated notes against the documentation actually required for the billed code level

### Metrics
- % of billed codes with full element-level justification traceable to transcript/chart
- Note-to-code mismatch rate identified in internal audit sampling
- Revenue variance attributable to up/downcoding drift over time

### Alerts
- Billing code level changes when template language is removed in QA review → P1
- Code level suggested without traceable source for required elements → P2

---

## References

- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
- [Reinventing Clinical Dialogue: Agentic Paradigms for LLM Enabled Healthcare Communication](https://arxiv.org/pdf/2512.01453)
