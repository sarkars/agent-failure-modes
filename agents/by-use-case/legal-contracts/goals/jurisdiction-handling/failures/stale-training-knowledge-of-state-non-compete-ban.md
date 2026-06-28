# Stale Training Knowledge of State Non-Compete Ban

## Issue: An Agent Drafting or Reviewing a Non-Compete Clause Answers Whether the Clause Is Enforceable in a Given State From Facts Memorized During Pretraining Rather Than Calling a Live Statute-Lookup or Legal-Database Tool It Has Available, Producing an Enforceability Assessment Based on the Law as It Stood Before the Model's Training Cutoff Even Though the State's Rule Has Since Changed

**Frequency**: Occasional

**Symptoms**
- Agent states a non-compete clause is enforceable (or enforceable with standard limitations) in a state that has since banned or substantially restricted non-competes by statute or regulation after the model's training cutoff
- The agent's stated reasoning cites general legal principles ("reasonable in scope, duration, and geography") rather than referencing the specific state's current statute or regulatory text, even though a live legal-database tool is available in the agent's toolset
- Re-running the same enforceability question with an explicit instruction to call the statute-lookup tool before answering produces the correct, current answer, isolating the failure to the agent defaulting to memorized knowledge rather than the tool being unavailable or non-functional
- The error concentrates on states with recent legislative or regulatory non-compete changes, where the gap between the model's training cutoff and the current legal landscape is largest
- A contract is executed with a non-compete clause that is unenforceable under current law, discovered only when the company attempts to enforce it and opposing counsel raises the recent statutory change

**Root Cause**
The model's pretraining corpus encodes the non-compete enforceability landscape as it existed up to its training cutoff, and absent an explicit instruction or workflow step forcing a live lookup, the model defaults to answering from this memorized snapshot because it is immediately available and the question's surface form (a legal-reasoning question) does not itself signal that the underlying facts are time-sensitive. The agent has a live statute-lookup tool available specifically to avoid this, but nothing in the default workflow requires the agent to prefer the tool's output over its own memorized answer when the two would conflict.

**Example**
```
Drafting request: "Is a 12-month, 50-mile non-compete enforceable for a mid-level employee under [State]'s law?"
Agent answers from memorized training knowledge: "Yes, this is within typical reasonableness bounds for [State]," consistent with the state's law as of the model's training cutoff
The state, in fact, enacted a near-total ban on employee non-competes after the model's training cutoff, which a live statute-lookup tool available to the agent would have surfaced
Non-compete clause is drafted and included in the employment agreement as enforceable
Company later attempts to enforce the clause against a departing employee; opposing counsel cites the post-cutoff statutory ban, and the clause is found void
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of LLMs in legal applications identify reliance on static, pretraining-encoded legal knowledge -- rather than live regulatory sources -- as a specific, named failure category for jurisdiction- and time-sensitive legal questions | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |
| Retrieval-grounding research in legal RAG systems finds that models with tool access still default to parametric knowledge unless workflow design explicitly forces tool-grounded answers for time-sensitive facts | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Version and currency tracking for legal source material is identified as a distinct technical requirement precisely because regulatory text changes faster than model training cycles | [Version Control for Legal Documents](https://arxiv.org/abs/2108.06421) |

**Contributing Factors**
- Workflow does not require the agent to call the statute-lookup tool before answering a jurisdiction-specific enforceability question, leaving the choice to the model's own judgment about whether a lookup is needed
- The question's surface form (a legal-reasoning question about reasonableness) does not signal to the model that the underlying facts are time-sensitive in the way a question about "current law" explicitly would
- No automated check compares the agent's stated enforceability conclusion against the most recent version of the cited state's statute before the clause is finalized

---

## Mitigation Strategies

1. **Mandatory Statute Lookup for Jurisdiction-Specific Enforceability Questions**: Require any non-compete (or other jurisdiction-sensitive clause) enforceability determination to be preceded by a logged call to the live statute-lookup tool, and block the determination from being used in drafting if no such call occurred
2. **Recency Flag on All Jurisdiction-Specific Legal Conclusions**: Require the agent to explicitly state the as-of date of the legal source it relied on, making it visible when a conclusion is based on memorized knowledge with no stated current source
3. **Automated Cross-Check Against Current Statute Text**: Before a non-compete clause is finalized for a given state, automatically diff the agent's stated enforceability rationale against the current statute text retrieved from the legal database, flagging any conflict
4. **Maintain a Recent-Change Watchlist**: Maintain and surface to the agent a running list of states with recent (post-training-cutoff-relevant) non-compete law changes, forcing a mandatory lookup specifically for any state on the watchlist

### Metrics
- Rate of jurisdiction-specific enforceability determinations made without a logged statute-lookup tool call
- Number of finalized non-compete clauses in states later found to conflict with a statutory change predating the clause's drafting date
- Percentage of legal conclusions in drafted clauses that include an explicit as-of date for their cited source

### Alerts
- A non-compete clause is finalized for a state on the recent-change watchlist without a logged statute-lookup call → P1
- Automated cross-check finds the agent's stated enforceability rationale conflicts with the current statute text and the clause proceeds to drafting → P1
- A jurisdiction-specific legal conclusion is generated with no as-of date for its source → P2

---

## References

- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [Version Control for Legal Documents](https://arxiv.org/abs/2108.06421)
