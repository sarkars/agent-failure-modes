# Self-Verification Illusion in Agent-Led De-Identification Recheck

## Issue: When an Agent That Produced a "De-Identified" Clinical Extract Is Asked to Re-Check Its Own Output for Remaining Identifiers Before Release, the Same Agent Re-Reads Its Own Prior Output Through the Same Reasoning Path That Produced It, Confirms the Redaction as Complete, and Reports the Extract as Verified -- Even Though the Recheck Never Independently Re-Scans the Source Document or Applies a Different Detection Method, So Identifiers the First Pass Missed Are Missed Again in the "Verified" Pass

**Frequency**: Occasional

**Symptoms**
- Agent's self-recheck output states the extract "has been reviewed and contains no identifying information" while a residual identifier (a rare-disease combination, a free-text date plus department reference, an unredacted provider name in a quoted note) remains present
- The specific identifiers missed in the recheck are the same ones missed in the original de-identification pass, rather than a new, different set -- indicating the recheck reproduced the same blind spot rather than catching it
- An independent rule-based PHI scanner or a second, separately-prompted agent instance run on the same extract flags identifiers the first agent's self-recheck cleared
- The agent's recheck reasoning trace shows it re-reading its own redacted output text rather than re-comparing against the original unredacted source document
- Recheck completes with high stated confidence despite never invoking a different detection mechanism than the one used to produce the original redaction

**Example**
```
Research-extract agent de-identifies a clinical note for a registry submission, redacting name, MRN, and explicit dates
The note contains a rare combination of diagnosis, treatment site, and a referenced "the attending who performed the index procedure on the unit's only such case that month" -- a quasi-identifier the agent's redaction pass does not recognize as identifying
Compliance workflow asks the same agent instance to double-check its own de-identified output for remaining identifiers
Agent re-reads the redacted text, finds no explicit name/MRN/date pattern remaining, and reports "verification complete, no identifying information found"
A separately-run rule-based PHI detector applied to the same extract flags the quasi-identifying combination as a re-identification risk
Review finds the self-recheck used the same redaction logic and the same blind spot as the original pass, producing false assurance rather than independent verification
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLMs that confidently catch and repair errors in externally-presented content systematically fail to identify identical errors in their own prior output, an asymmetry traced to how models process their own reasoning versus content framed as external | [The Self-Correction Illusion: LLMs Correct Others but Not Themselves](https://arxiv.org/html/2606.05976) |
| Research on LLM self-verification finds recheck behaviors overwhelmingly fall into a confirmatory pattern -- reaffirming the original conclusion -- rather than a corrective pattern that surfaces genuine errors | [Self-Verification Dilemma: Experience-Driven Suppression of Overused Checking in LLM Reasoning](https://arxiv.org/html/2602.03485v1) |
| Execution-provenance research argues that traceable links between a claim and independent verifying evidence are necessary precisely because models do not reliably self-report when a stated verification lacks independent grounding | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- Recheck step is executed by the same agent instance and prompt pattern that produced the original redaction, rather than an independently configured detector
- No requirement that verification re-derive identifiers from the original unredacted source rather than re-reading the agent's own redacted output
- Quasi-identifiers (rare combinations of non-explicit attributes) fall outside the pattern-matching categories the redaction step was tuned to catch, and the recheck inherits the same category blind spot
- Compliance workflow treats "agent reports verification complete" as sufficient sign-off without requiring a structurally different second check

---

## Mitigation Strategies

1. **Independent Detector Requirement**: Require de-identification verification to run through a separate detection mechanism (a rule-based PHI scanner or a distinctly-configured second model call) rather than the same agent re-reading its own output
2. **Source-Document Re-Comparison**: Require the recheck step to re-scan the original unredacted source document for identifiers, not just re-read the redacted output, so quasi-identifiers omitted from the first pass have a chance to be caught against the full source
3. **Quasi-Identifier Checklist**: Maintain an explicit checklist of quasi-identifying patterns (rare diagnosis-site-timing combinations, unique role/unit references) for the verification step to test against, beyond the explicit-identifier patterns the redaction step targets
4. **Verification Provenance Logging**: Require the verification report to state which method and which document version it checked against, so "verified" claims with no independent provenance are visibly distinguishable from genuine independent checks

### Metrics
- Rate of extracts where an independent scanner flags identifiers after the agent's self-recheck cleared the same extract
- Overlap rate between identifiers missed in the original redaction and identifiers missed in the self-recheck (high overlap indicates blind-spot reproduction rather than independent verification)
- Number of registry/research submissions requiring post-release correction due to residual identifiers

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Recheck-original overlap | Self-recheck clears an extract that an independent scanner subsequently flags | P1 | Block release; route to compliance officer for manual review |
| Same-instance verification | Verification step executed by the same agent instance/prompt as the original redaction with no independent method | P2 | Re-route through independent detector before sign-off |
| Quasi-identifier miss pattern | Recurring category of quasi-identifier (e.g., rare combination phrasing) missed across multiple extracts | P3 | Update redaction and checklist patterns; retrain detection rules |

---

## References

- [The Self-Correction Illusion: LLMs Correct Others but Not Themselves](https://arxiv.org/html/2606.05976)
- [Self-Verification Dilemma: Experience-Driven Suppression of Overused Checking in LLM Reasoning](https://arxiv.org/html/2602.03485v1)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
