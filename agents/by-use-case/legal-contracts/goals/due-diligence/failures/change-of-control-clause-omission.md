# Change-of-Control Clause Omission in M&A Due Diligence

## Issue: Agent Reviewing a Target Company's Contract Portfolio for M&A Due Diligence Fails to Flag Change-of-Control Provisions That Trigger on the Transaction Itself

**Frequency**: Common

**Symptoms**
- Due diligence summary reports a contract as "no termination rights triggered by the transaction" when the contract actually contains a change-of-control clause permitting the counterparty to terminate or renegotiate upon acquisition
- Change-of-control language phrased indirectly ("assignment without consent is prohibited," "a change in the ownership or management of either party shall be deemed an assignment") is not recognized as functionally equivalent to an explicit change-of-control clause
- Material contracts with change-of-control triggers are not aggregated into a single consolidated risk list for deal-team review; each is assessed in isolation
- Consent or notice requirements tied to the change-of-control trigger (e.g., "must notify counterparty within 30 days of closing") are identified but not linked to the actual closing timeline

**Root Cause**
Change-of-control provisions are drafted with significant variation in language — some are explicit, many are implicit within broader assignment or anti-assignment clauses. An agent scanning for a literal "change of control" heading or phrase will miss the functionally equivalent but differently worded triggers, and because this is a key M&A risk category, missing even a handful of material contracts can materially understate deal risk or post-closing obligations.

**Example**
```
Scenario: Due diligence review of target's top 50 customer contracts
Contract #23: No explicit "change of control" heading; assignment clause states "any change in ownership of more than 50% shall constitute an assignment requiring counterparty consent"
Agent scan: Searches for "change of control" phrase, does not match this assignment-based trigger
Due diligence report: Contract #23 not flagged as having a transaction-triggered consent requirement
Impact: Acquirer proceeds without obtaining required counterparty consent; risk of contract termination or breach post-closing
```

**Key Statistics**
- Change-of-control and assignment-clause review is consistently identified as one of the highest-value, highest-risk categories in M&A contract due diligence
- Semantic variation in how change-of-control triggers are drafted (explicit clause vs. functionally equivalent assignment language) is a documented source of missed findings in both manual and automated contract review
- AI-assisted due diligence benchmarking research shows meaningfully lower recall for implicitly-worded risk clauses compared to explicitly labeled ones

---

## Mitigation Strategies

1. **Semantic, Not Keyword, Detection**: Train/prompt the review agent to recognize functionally equivalent change-of-control triggers (ownership-change-as-assignment language) in addition to explicitly labeled clauses
2. **Consolidated Risk Register**: Aggregate every contract with a change-of-control or assignment trigger into a single deal-team risk register, with consent/notice deadlines mapped against the actual closing timeline
3. **Materiality-Weighted Triage**: Prioritize change-of-control review for contracts above a revenue or strategic-importance threshold, ensuring the highest-risk agreements get the most scrutiny
4. **Closing-Timeline Cross-Check**: For every identified consent/notice requirement, explicitly compute whether the required action can be completed before the closing date

### Metrics
- Recall rate for implicitly-worded change-of-control triggers vs. explicitly labeled ones, measured against attorney-reviewed ground truth
- % of identified triggers with consent/notice deadlines cross-checked against the closing timeline
- Number of material contracts with unflagged change-of-control risk discovered post-closing

### Alerts
- Change-of-control or equivalent assignment trigger identified in a top-tier contract without a deal-team risk register entry → P1
- Required consent/notice deadline falls after the planned closing date → P1

---

## References

- [Large Language Models Meet Legal Artificial Intelligence: A Survey](https://arxiv.org/pdf/2509.09969)
- [Better Bill GPT: Comparing Large Language Models against Legal Invoice Reviewers](https://arxiv.org/pdf/2504.02881)
