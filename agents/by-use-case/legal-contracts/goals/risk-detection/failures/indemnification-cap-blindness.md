# Indemnification Cap Blindness

## Issue: Agent Flags an Indemnification Clause as Present Without Evaluating Whether It Is Capped, Uncapped, or Mutual

**Frequency**: Common

**Symptoms**
- Contract review summary lists "indemnification clause: present" as a binary check rather than characterizing its scope, cap, and direction
- Uncapped indemnification obligation is treated the same as a liability-capped one in the risk summary
- One-sided (unilateral) indemnification obligations are not distinguished from mutual indemnification in the agent's output
- Carve-outs from a liability cap (e.g., IP infringement, gross negligence are excluded from the cap) are not surfaced, understating actual exposure

**Root Cause**
Indemnification analysis is treated by many contract-review pipelines as a clause-presence classification task (does an indemnification clause exist, yes/no) rather than a quantitative exposure-extraction task. The actual risk lives in the interaction between the indemnification clause and a separate limitation-of-liability clause — including which exclusions and carve-outs apply — which requires cross-referencing two clauses rather than evaluating either in isolation, a step that simple presence/absence classifiers skip entirely.

**Example**
```
Scenario: Vendor agreement, indemnification clause obligates vendor to indemnify customer for "any and all claims arising from vendor's performance"
Limitation of liability clause: Caps "all claims" at 12 months of fees, EXCEPT indemnification obligations, which are explicitly carved out and therefore uncapped
Agent summary: "Indemnification clause present, liability capped at 12 months fees"
Missed: Indemnification is explicitly carved out of the cap — vendor's actual exposure is uncapped
Impact: Material underestimation of contractual liability exposure
```

**Key Statistics**
- Legal AI benchmark work on clause-level risk identification (e.g., ContractEval-style evaluation) shows LLMs frequently miss cross-clause interactions like cap carve-outs even when individual clauses are correctly classified
- Survey research on LLMs in legal AI repeatedly identifies multi-clause reasoning (as opposed to single-clause classification) as a persistent weak point
- Indemnification-liability cap interactions are among the most commonly negotiated and most consequential terms in commercial contract review, per practitioner benchmarking studies (e.g., "Better Call GPT"-style evaluations)

---

## Mitigation Strategies

1. **Cross-Clause Linking**: Require the agent to explicitly locate and cross-reference the limitation-of-liability clause whenever an indemnification clause is identified, and check for carve-outs in both directions
2. **Exposure Characterization, Not Presence Classification**: Output a structured exposure summary (capped/uncapped, mutual/unilateral, carve-outs) instead of a binary presence flag
3. **Carve-Out Enumeration**: Explicitly enumerate every carve-out from the liability cap and state whether the indemnification obligation falls inside or outside each one
4. **Attorney Review Trigger**: Flag any uncapped or carved-out indemnification obligation above a materiality threshold for mandatory attorney review before contract execution

### Metrics
- % of indemnification clauses with full cap/carve-out cross-reference completed
- Rate of uncapped-exposure contracts correctly flagged vs. missed in QA sampling
- Time-to-attorney-review for flagged uncapped indemnification obligations

### Alerts
- Indemnification clause identified with no corresponding limitation-of-liability cross-reference → P1
- Carve-out from liability cap detected and not surfaced in summary → P1

---

## References

- [Large Language Models Meet Legal Artificial Intelligence: A Survey](https://arxiv.org/pdf/2509.09969)
- [Better Bill GPT: Comparing Large Language Models against Legal Invoice Reviewers](https://arxiv.org/pdf/2504.02881)
