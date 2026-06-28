# Circuit Split Blindness in Citation Selection

## Issue: Legal Research Agent Cites a Precedent as Settled Law Without Flagging That a Circuit Split (or Equivalent Jurisdictional Disagreement) Exists, Leading to a Brief That Misrepresents the Strength of the Authority

**Frequency**: Common

**Symptoms**
- Agent cites a single appellate decision in support of a legal proposition without noting that one or more other circuits/jurisdictions have reached the opposite conclusion on the same question
- Drafted briefs or memos present a holding as "the rule" rather than "the rule in this circuit, with a contrary rule in others," understating the actual litigation risk
- Opposing counsel's response brief cites the contrary-circuit authority that the agent's research never surfaced, catching the legal team off guard
- Research memos generated for multi-jurisdiction matters fail to differentiate which circuit's rule applies to which entity or transaction in the matter
- Citation-checking review finds that the agent's underlying retrieval ranks decisions by semantic relevance to the query, not by circuit-split awareness, so contrary authority is retrievable but never surfaced unless explicitly searched for

**Root Cause**
Legal research agents built on semantic retrieval over case law typically rank and return the most topically relevant decisions for a query, but "topically relevant" does not equate to "represents the full landscape of authority on this question." Without an explicit step that checks whether other circuits or jurisdictions have addressed the identical question and reached a different conclusion -- a step that requires structured awareness of circuit splits, not just semantic similarity -- the agent will confidently present a single jurisdiction's holding as if it were uncontested law.

**Example**
```
Research question: "Is a clickwrap arbitration clause enforceable without affirmative assent beyond browsing?"
Agent cites: Ninth Circuit decision finding such clauses unenforceable absent conspicuous notice and affirmative action
Agent's brief language: "Courts have held that browsewrap-style arbitration clauses are unenforceable without affirmative assent."
Missing: Second and Seventh Circuit decisions enforcing materially similar clauses under a constructive-notice standard
Outcome: brief overstates the strength of the unenforceability argument in a matter that may ultimately be litigated in a circuit following the contrary rule
```

**Key Statistics**
- Surveys of LLMs in legal applications report that hallucinated or incomplete citation -- including omission of contrary authority -- remains one of the most consistently observed failure categories even in retrieval-augmented legal research tools
- Legal AI evaluation research notes that retrieval-based legal research tools, when evaluated specifically for split-authority awareness rather than topical relevance, show materially lower recall of contrary-jurisdiction holdings than of same-conclusion holdings on the same question
- Practitioner-facing legal AI benchmarking work emphasizes that citation completeness (not just citation accuracy) is a distinct and under-tested dimension of legal AI reliability

**Contributing Factors**
- Retrieval ranks by semantic similarity to the query, not by an explicit "does contrary authority exist" check
- No structured circuit-split database integrated into the research pipeline
- Drafting step does not require the agent to affirmatively state "no contrary authority identified" as a checkable claim, leaving omission undetectable until opposing counsel responds

---

## Mitigation Strategies

1. **Explicit Contrary-Authority Search Step**: Require the research pipeline to run a dedicated search specifically for contrary holdings on the same legal question, separate from and in addition to the topical-relevance search
2. **Circuit-Split Database Cross-Reference**: Integrate a maintained circuit-split tracker (commercial or internally curated) and require the agent to cross-reference any cited holding against it before drafting
3. **Mandatory Disclosure Language for Unsettled Questions**: Require draft language to explicitly characterize a cited holding as jurisdiction-specific and to flag known splits, rather than presenting any holding as universally settled
4. **Attorney Sign-Off Specifically on Citation Completeness**: Add a review checkpoint distinct from substantive review that specifically asks "has contrary authority been searched for and addressed," not just "is this citation accurate"

### Metrics
- Rate of cited holdings in agent-drafted research subsequently found (via human review or post-hoc audit) to have unflagged contrary authority
- Coverage rate of known circuit splits correctly flagged when the underlying legal question is researched
- Rate of opposing-counsel-cited authority that was retrievable by the firm's own research tool but not surfaced in the original research memo

### Alerts
- Draft brief or memo cites a holding on a legal question with a known tracked circuit split, without contrary-authority language present → P1
- Contrary-authority search step returns zero results for a question flagged as multi-jurisdictional → P2
- Post-filing discovery that opposing counsel cited contrary authority not surfaced in internal research → P2

---

## References

- [Large Language Models Meet Legal Artificial Intelligence: A Survey](https://arxiv.org/pdf/2509.09969)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Better Bill GPT: Comparing Large Language Models against Legal Invoice Reviewers](https://arxiv.org/pdf/2504.02881)
