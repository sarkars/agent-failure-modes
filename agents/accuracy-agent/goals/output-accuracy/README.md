# Goal: Output Accuracy

Eliminate hallucinations and ensure all outputs are grounded in available information. Fabricated content is one of the most damaging agent failure modes.

## Business Context

- Hallucinated facts cause legal liability and reputational damage
- Users trust agent outputs, amplifying impact of errors
- Confident wrong answers are harder to catch than obvious errors
- Regulatory compliance often requires factual accuracy

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Confident Fabrication](failures/confident-fabrication.md) | Common | Critical |
| [Source Misattribution](failures/source-misattribution.md) | Common | High |
| [Temporal Confusion](failures/temporal-confusion.md) | Common | High |
| [Entity Confusion](failures/entity-confusion.md) | Common | High |
| [Extrapolation Beyond Data](failures/extrapolation.md) | Very Common | Medium |
| [Inherited Errors](failures/inherited-errors.md) | Common | High |
| [Bias Amplification](failures/bias-amplification.md) | Common | High |
| [Verification Failure](failures/verification-failure.md) | Common | High |
| [Domain Mismatch](failures/domain-mismatch.md) | Common | High |
| [Algorithmic Discrimination](failures/algorithmic-discrimination.md) | Common | Critical |
| [Content Fabrication](failures/content-fabrication.md) | Very Common | High |

## Key Statistics

| Finding | Source |
|---------|--------|
| 52% of enterprise AI responses contain fabrications with ungoverned RAG | Enterprise Survey 2026 |
| Legal RAG tools hallucinate 17-33% | Stanford Study |
| Only 29% of developers trust AI output accuracy | Industry Survey |

## Key Metrics

- Hallucination rate (fabricated facts / total facts)
- Groundedness score (claims supported by sources)
- Citation accuracy
- Factual error detection rate
