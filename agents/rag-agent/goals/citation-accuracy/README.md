# Goal: Citation Accuracy

Correctly attribute information to sources. Citations build trust and enable verification, but wrong or missing citations undermine both.

## Business Context

- Users rely on citations to verify information
- Wrong citations waste user time and erode trust
- Missing citations make claims unverifiable
- Legal/compliance contexts require accurate attribution

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Wrong Source Cited](failures/wrong-source.md) | Common | High |
| [Fabricated Citations](failures/fabricated-citations.md) | Occasional | Critical |
| [Missing Citations](failures/missing-citations.md) | Common | Medium |
| [Citation Doesn't Support Claim](failures/unsupported-claim.md) | Common | High |
| [Granularity Mismatch](failures/granularity-mismatch.md) | Common | Medium |
| [Broken References](failures/broken-references.md) | Occasional | Medium |

## Key Statistics

| Finding | Source |
|---------|--------|
| 17-33% hallucination rate in legal RAG despite citations | Stanford Study |
| Citation verification catches 40% of subtle errors | Research |
| Users trust cited answers 3x more than uncited | User Study |

## Key Metrics

- Citation precision (cited sources support claims)
- Citation recall (all claims have citations)
- Citation validity (cited sources exist and accessible)
- Citation granularity (points to specific location)
