# Self-Verification Illusion in Duplicate-Therapy Check

## Issue: When Asked to Double-Check Its Own Medication Reconciliation for Duplicate or Overlapping Therapy, the Same Agent Re-Examines the Same Medication List Using the Same Reasoning Path That Produced the Original Reconciliation, Confirms Its Own Conclusion, and Reports the List as Verified Even Though the Recheck Never Consulted an Independent Drug-Class Database

**Frequency**: Occasional

**Symptoms**
- A "verify this reconciliation for duplicate therapy" request returns a confident confirmation that no duplicates exist, even on a medication list that an independent drug-class cross-reference shows contains two agents from the same therapeutic class
- The agent's self-check re-reads the same medication names and re-applies the same class-matching judgment that produced the original miss, rather than querying a structured drug-class or interaction database
- Asking the agent to explain how it verified the list describes re-reading the list and reasoning about it again, not consulting any source independent of its own prior output
- Running the same medication list through a structured drug-class lookup tool, independent of the agent's narrative reasoning, surfaces the duplicate that the self-check missed
- The duplicate-therapy miss concentrates on cases where the two overlapping medications have dissimilar brand or generic names within the same class, so the overlap is not obvious from name inspection alone

**Root Cause**
A same-model self-check re-derives its judgment from the same internal representation and reasoning process that produced the original conclusion, so any systematic gap in that reasoning -- such as not recognizing that two differently named medications belong to the same therapeutic class -- is reproduced rather than corrected on recheck. Because the self-check produces a fluent, confident restatement of the original conclusion, it is indistinguishable in tone from a recheck that actually consulted independent evidence, giving reviewers false confidence that verification occurred.

**Example**
```
Reconciliation agent compiles a discharge medication list including metoprolol succinate and carvedilol, both beta-blockers, listed under their generic names
Reconciliation output does not flag the overlap; both drugs are listed as continuing home medications
Pharmacist requests the agent verify the list for duplicate or overlapping therapy before discharge
Agent re-reads the same list, reasons that the two drug names "look like different medications for different purposes," and reports: "Reconciliation verified, no duplicate therapy identified"
An independent structured drug-class lookup against the same list immediately flags both as beta-blockers, a clinically significant duplication the self-check did not catch
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Tool-use agents show a measurable gap between expressed confidence after a self-check and the actual correctness of the underlying conclusion, particularly when the self-check does not introduce independent evidence | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Surveys of agent hallucination identify self-consistency checks performed by the same model as an unreliable substitute for grounding in an independent, structured source | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Surveys of LLM-based agents in medicine identify independent, structured drug-interaction and drug-class verification as a distinct safety requirement separate from narrative re-review of a medication list | [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1) |

**Contributing Factors**
- The verification step is implemented as a second prompt to the same model rather than a call to an independent, structured drug-class or interaction database
- No distinction is enforced between "re-reasoned about the same list" and "checked against an independent source" in how the verification result is logged or reported
- Drug-class overlap detection depends on the model recognizing therapeutic-class membership from generic or brand names alone, with no structured class lookup required

---

## Mitigation Strategies

1. **Independent Drug-Class Database as Mandatory Verification Source**: Require any duplicate-therapy verification step to query a structured, independent drug-class database for every medication on the list, rather than relying on the same model re-reasoning about the list
2. **Disallow Same-Model Self-Check as Sole Verification**: Prohibit a verification step from being satisfied solely by a second response from the same model that produced the original reconciliation; require either an independent tool call or independent human review
3. **Label Verification Source in Output**: Require any "verified" status on a reconciliation to indicate explicitly whether verification consulted an independent structured source or only re-reasoned narratively, so reviewers can distinguish the two
4. **Pharmacist Review Trigger on Class-Database Mismatch**: When the independent drug-class database and the agent's reconciliation disagree on whether a duplication exists, route the case to pharmacist review rather than resolving the disagreement automatically

### Metrics
- Rate of "verified" reconciliations where an independent drug-class database lookup, run after the fact, surfaces a duplicate therapy the verification missed
- Rate of verification steps that consulted an independent structured source versus those that re-reasoned narratively only
- Time between discharge and detection of a missed duplicate therapy, when caught downstream

### Alerts
- An independent drug-class lookup finds a duplicate therapy on a list marked "verified" by self-check alone → P1
- A verification step completes with no record of an independent structured-source query → P2
- Self-check-only verifications as a share of total verifications exceed the defined threshold for a rolling window → P3

---

## References

- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
