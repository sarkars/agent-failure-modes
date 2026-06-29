# Context-Window Loss Reintroduces Previously Resolved Pricing Objection in Long Deal Thread

## Issue: A Deal-Management Agent Drafting a Customer-Facing Recap or Summary Partway Through a Long, Multi-Month Enterprise Deal Thread Re-Surfaces a Pricing Objection or Discount Request That the Customer Raised and the Account Executive Already Resolved Early in the Negotiation, Because That Resolution Falls Out of the Portion of the Thread the Model Weighs Most Heavily Once Many Subsequent Rounds (Security Review, Legal Redlines, Implementation Scoping) Have Been Added, Causing the Agent to Generate a Recap That Implies the Objection Is Still Open

**Frequency**: Occasional

**Symptoms**
- Agent-generated deal recap or internal summary lists a pricing objection as "open" or "to be addressed" when the actual thread shows it was explicitly resolved (discount agreed, or customer explicitly withdrew the objection) many messages earlier
- Re-reading the full thread chronologically confirms the resolution language is unambiguous and was never reopened by either party
- The reintroduction occurs specifically in recaps generated after the thread has grown substantially (security questionnaire exchanges, legal redlines, multiple scoping calls) -- recaps generated shortly after the original resolution do not show the error
- Account executive, relying on the agent's recap, proactively reopens a pricing conversation with the customer that the customer considered settled, creating an awkward and unnecessary renegotiation moment
- Internal deal-desk notes generated from the same recap propagate the stale "open objection" status into the deal's official record, requiring manual correction

**Example**
```
Month 1: Customer raises a pricing objection on the proposed per-seat rate; AE and
customer agree on a 10% volume discount; customer confirms "that works for us, let's move
forward"
Months 2-3: Thread grows substantially with security-questionnaire responses, three
rounds of legal redlines on the MSA, and two implementation-scoping calls
Month 4: AE asks the deal-management agent to "summarize where we stand on this deal for
the QBR"
Generated summary includes: "Pricing: customer has raised concerns about the per-seat
rate; discount request still under discussion" -- contradicting the explicit resolution
from month 1, which the summary omits entirely
AE, trusting the summary, opens the QBR by proactively offering to "revisit pricing,"
confusing the customer who believed that was settled three months prior and now wonders
if the deal has unresolved issues
Reviewing the full thread confirms the resolution was clear and never contested again
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Research on long-context language models shows information in the middle of a long input -- such as an early resolution in a since-extended conversation -- is recalled and weighted substantially less reliably than information near the beginning or end of the context | [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) |
| Hallucination survey research identifies omission of previously established facts, including resolved objections or decisions, as a distinct failure mode in long-running multi-turn agent interactions, separate from outright fabrication | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Failure-mode research on production LLM systems finds summarization and recap-generation steps over long histories are a recurring point where earlier resolved state is silently dropped or contradicted in the generated summary | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |

**Contributing Factors**
- The deal has no persistent, structured "resolved issues" ledger separate from the raw chronological thread -- whether an objection is open or resolved is re-inferred from the full transcript each time a summary is requested
- The original resolution was a single exchange early in the thread with no recurring restatement in later rounds, making it more susceptible to being weighted lower as the thread grows
- Summary generation is prompted holistically ("summarize where we stand") rather than against an explicit, itemized status list of known objections and their resolution state
- No reconciliation step compares a freshly generated recap against the deal's actual resolved-issues history before it is used in a customer-facing or internal-record context

---

## Mitigation Strategies

1. **Persistent Resolved-Issues Ledger**: Maintain a structured, append-only record of every objection raised and its resolution status throughout the deal, and generate recaps from this ledger rather than re-deriving status from the raw thread each time
2. **Status-Diff Before Recap Use**: Require the agent to diff any freshly generated recap against the resolved-issues ledger and flag contradictions (an item marked resolved in the ledger but described as open in the recap) before the recap is used
3. **Periodic Re-Anchoring of Resolved State**: For deals exceeding a defined thread length or duration, periodically re-surface a compact summary of all resolved items back into active context before generating new recaps
4. **AE Confirmation for Status-Sensitive Recaps**: Require AE sign-off comparing the agent's recap against their own recollection of resolved items before using it in a customer-facing setting such as a QBR

### Metrics
- Rate of generated recaps that mark a ledger-resolved objection as open or unresolved
- Correlation between deal-thread length/duration and recap-accuracy errors on resolved items
- Number of customer-facing renegotiation moments traced back to a stale agent-generated recap

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Resolved-item reopened in recap | Generated recap marks a ledger-resolved objection as open or pending | P1 | Block recap from customer-facing use; regenerate from ledger |
| Long-thread recap without ledger diff | Recap generated for a deal exceeding a defined thread length without a ledger-diff check | P2 | Force reconciliation step before recap is shared |
| AE reopens settled pricing conversation | AE proactively revisits a pricing point the ledger marks resolved | P3 | Audit recap-generation pipeline for that deal |

---

## References

- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
