# Self-Verification Illusion in Clause-Conflict Recheck

## Issue: When Asked to Double-Check a Drafted Contract for Internal Clause Conflicts, the Same Agent Re-Reads the Document Using the Same Interpretation of Each Clause That Produced the Original Draft, Confirms No Conflict Exists, and Reports the Contract as Internally Consistent Even Though an Independent Clause-by-Clause Structured Comparison Would Surface a Genuine Conflict

**Frequency**: Occasional

**Symptoms**
- A "check this draft for internal conflicts" request returns a confident statement that no conflicts exist, even though two clauses in the same document impose contradictory obligations under specific conditions
- The agent's recheck re-reads the same clauses with the same interpretive framing that produced the original draft, rather than extracting each clause's obligations into a structured form and comparing them independently
- Asking the agent to explain how it checked for conflicts describes re-reading the document and reasoning about it again, not a structured, clause-by-clause obligation extraction and comparison
- Running the same draft through an independent, structured obligation-extraction pass (listing each clause's triggering condition and resulting obligation) surfaces the conflict the self-check missed
- The conflict concentrates on clauses separated by many pages or sections, where the contradiction is not visually adjacent and depends on tracing a conditional trigger defined in one clause against an obligation defined in a distant clause

**Root Cause**
A same-model self-check re-derives its judgment from the same interpretive frame that produced the original draft, so a conflict the drafting process did not recognize as a conflict is not recognized on recheck either, since the same reasoning path is simply repeated. Because the self-check produces a fluent, confident restatement of internal consistency, it is indistinguishable in tone from a check that actually performed an independent structured comparison, giving reviewers false confidence that the conflict check was substantive.

**Example**
```
Drafting agent produces a services agreement with a termination-for-convenience clause in Section 4 allowing either party to terminate with 30 days' notice, and a separate exclusivity clause in Section 11 stating the agreement remains exclusively binding for a fixed 18-month term with no early-termination carve-out
Drafting agent is asked to verify the draft has no internal conflicts
Agent re-reads both sections, reasons that "termination and exclusivity address different topics," and reports: "No internal conflicts identified, draft is consistent"
An independent structured pass extracting each clause's trigger and obligation flags that Section 4's termination right directly contradicts Section 11's fixed-term exclusivity with no termination carve-out
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Tool-use and reasoning agents show a measurable gap between expressed confidence after a self-check and the actual correctness of the underlying conclusion, particularly when the self-check does not introduce an independent representation of the artifact | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Evaluations of large language models in legal applications identify self-consistency checks performed by the same model as an unreliable substitute for independent, structured clause analysis | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |
| Surveys of agent hallucination identify same-model self-review as systematically prone to reproducing, rather than catching, the reasoning gap that produced the original error | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |

**Contributing Factors**
- The conflict-check step is implemented as a second prompt to the same model rather than a structured, independent clause-by-clause obligation extraction and comparison
- No distinction is enforced between "re-read the document narratively" and "extracted and compared structured obligations" in how the conflict-check result is logged or reported
- Conflicts spanning non-adjacent sections depend entirely on the model tracing conditional triggers across the full document, which a narrative re-read does not reliably do

---

## Mitigation Strategies

1. **Structured Obligation Extraction as Mandatory Conflict-Check Method**: Require any internal-conflict check to first extract every clause's triggering condition and resulting obligation into a structured list, then compare that list programmatically or independently for contradictions, rather than relying on narrative re-reading
2. **Disallow Same-Model Narrative Self-Check as Sole Verification**: Prohibit a conflict-check from being satisfied solely by a second narrative response from the same model that produced the draft; require either structured extraction or independent reviewer sign-off
3. **Label Verification Method in Output**: Require any "no conflicts found" result to indicate whether the check used structured obligation extraction or only narrative re-reading, so reviewers can prioritize which drafts need additional scrutiny
4. **Cross-Section Conflict Scan as Standard Pre-Execution Step**: Run a structured cross-section conflict scan on every draft before execution, independent of whether a conflict check was separately requested

### Metrics
- Rate of "no conflicts found" drafts where an independent structured obligation-extraction pass, run after the fact, surfaces a genuine conflict
- Rate of conflict checks that used structured extraction versus narrative re-reading only
- Number of executed contracts later found to contain an internal clause conflict during a dispute or amendment review

### Alerts
- A structured obligation-extraction pass finds a conflict in a draft previously marked "no conflicts found" by narrative self-check → P1
- A contract is executed with no record of a structured conflict-check pass having been run → P2
- Narrative-only conflict checks as a share of total conflict checks exceed the defined threshold for a rolling window → P3

---

## References

- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
