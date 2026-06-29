# Embedding Retrieval Selects Similar but Wrong Canned Response

## Issue: A Support Agent That Selects a Canned Response or Macro From a Library Via Semantic/Embedding Similarity to the Customer's Message, Rather Than by Matching the Customer's Actual Account State or Issue Category, Retrieves a Response That Is Lexically and Topically Close to What the Customer Wrote but Answers a Different Underlying Situation -- Sending Confident, On-Topic-Sounding Guidance That Does Not Actually Apply to the Customer's Case

**Frequency**: Common

**Symptoms**
- Selected canned response addresses the same general topic as the customer's message (e.g., billing, account access) but the specific scenario it covers does not match the customer's actual account state
- Customer's follow-up indicates the response didn't address their actual situation ("that's not what I'm asking" or "I already tried that, it's a different issue")
- Re-running retrieval against the same message but filtered to the customer's actual account-state metadata (subscription tier, region, issue category) surfaces a different, more applicable canned response
- The retrieved response's similarity score to the customer's message is high, despite the response being written for a meaningfully different precondition (e.g., a different subscription tier, a different error code, a resolved-vs-unresolved prior ticket)
- Agents reviewing transcripts confirm the response "sounds relevant" on a topic level but was written for a different precondition than what's actually true of this customer

**Example**
```
Customer on a legacy grandfathered pricing plan writes: "my card was charged twice this month for my subscription"
Embedding-based macro retrieval matches this message most closely to a canned response written for "duplicate charge due to a known billing-system bug affecting current standard-tier subscribers," which is lexically very similar to the customer's wording
Agent sends that canned response, including instructions specific to the standard-tier billing bug (a self-service refund link that only works for standard-tier accounts)
Customer's actual situation is unrelated to that bug -- their duplicate charge stems from a proration issue specific to legacy grandfathered plans, which has a different resolution path
Self-service refund link in the sent response fails for the customer's account type, and the customer returns to support frustrated that the "fix" didn't work
Review finds a different canned response, written specifically for legacy-plan proration issues, existed in the library and was a better match by account-state criteria, but ranked lower by pure text-similarity to the customer's wording
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Failure-mode taxonomies for LLM systems document retrieval mechanisms selecting content based on surface-level lexical or semantic similarity rather than the criteria that actually determine correctness for the specific case, producing confident but inapplicable output | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |
| Survey of hallucination in LLM-based agents notes that retrieval-augmented pipelines can still produce ungrounded or mismatched output when the retrieved content is topically similar but not actually applicable to the query's specific preconditions | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds dialogue systems frequently fail to verify that a selected response or action actually matches the caller's specific state before acting on it | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |

**Contributing Factors**
- Canned-response retrieval is keyed purely on embedding similarity to the customer's message text, with no filtering or re-ranking by structured account-state metadata (plan tier, region, prior ticket history)
- Library contains multiple responses covering topically adjacent but materially different scenarios (different plan tiers, different bug fixes), and their text similarity to common customer phrasing can outrank the structurally correct match
- No verification step confirming the selected response's stated preconditions (e.g., "for standard-tier accounts") actually match the customer's real account attributes before sending
- Agents and reviewers judge response relevance by topic match in spot-checks, making a precondition mismatch easy to miss without explicitly checking account-state fields

---

## Mitigation Strategies

1. **Metadata Pre-Filter Before Similarity Ranking**: Filter the canned-response candidate set by structured account-state attributes (plan tier, region, issue category) before applying embedding-similarity ranking, so a precondition mismatch cannot outrank a structurally correct match
2. **Precondition Verification Gate**: Require the agent to confirm the selected response's stated applicability conditions against the customer's actual account fields before sending, flagging any mismatch for re-selection
3. **Response-Library Precondition Tagging**: Tag every canned response in the library with explicit structured applicability conditions, separate from its free text, so retrieval can be constrained rather than relying purely on text similarity
4. **Mismatch Feedback Loop**: Log cases where a customer's follow-up indicates the sent response didn't apply, and use those cases to retrain or re-rank the retrieval model away from the lexically-similar-but-wrong match

### Metrics
- Rate of sent canned responses whose stated applicability conditions do not match the customer's actual account attributes
- Customer follow-up rate indicating a previously sent response did not address their actual issue
- Similarity-score gap between the retrieved (wrong) response and the structurally correct response that existed in the library for the same case

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Precondition mismatch at send time | Selected response's stated applicability conditions disagree with customer's actual account attributes | P1 | Block send; force re-selection or human review |
| Repeated mismatch for a response template | Same canned response repeatedly flagged as mismatched across multiple distinct customers | P2 | Re-tag template preconditions; adjust retrieval ranking |
| Customer-reported non-applicability spike | Rate of "that's not my issue" follow-ups rises for a given topic category | P3 | Audit retrieval ranking and library tagging for that category |

---

## References

- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
