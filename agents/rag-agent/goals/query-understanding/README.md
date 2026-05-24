# Goal: Query Understanding

Interpret user questions correctly to retrieve and synthesize appropriate answers. Misunderstood queries lead to irrelevant retrievals and wrong answers.

## Business Context

- Ambiguous queries need clarification, not guessing
- Multi-part questions need all parts addressed
- Follow-up questions require conversation context
- User intent may differ from literal query

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Ambiguity Mishandling](failures/ambiguity-mishandling.md) | Very Common | High |
| [Multi-Part Query Fragmentation](failures/multi-part-fragmentation.md) | Common | Medium |
| [Follow-Up Context Loss](failures/follow-up-context-loss.md) | Common | High |
| [Intent Misclassification](failures/intent-misclassification.md) | Common | High |
| [Scope Misunderstanding](failures/scope-misunderstanding.md) | Common | Medium |
| [Implicit Requirement Missing](failures/implicit-requirements.md) | Common | Medium |
| [False Premise Acceptance](failures/false-premise-acceptance.md) | Common | High |
| [Query Decomposition Failure](failures/query-decomposition-failure.md) | Common | High |

## Key Statistics

| Finding | Source |
|---------|--------|
| 30% of queries are ambiguous without context | Query Analysis |
| Multi-turn conversations have 40% higher failure rates | Research |
| Query reformulation improves retrieval by 15-25% | Benchmark |

## Key Metrics

- Query understanding accuracy
- Clarification request rate
- Multi-part coverage
- Follow-up handling success rate
