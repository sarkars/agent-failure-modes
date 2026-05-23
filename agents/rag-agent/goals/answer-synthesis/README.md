# Goal: Answer Synthesis

Generate accurate answers from retrieved content. Even with perfect retrieval, the generation step can introduce errors, hallucinations, or miss key information.

## Business Context

- Users trust RAG answers as "grounded" but hallucination still occurs
- Cherry-picking evidence creates biased or incomplete answers
- Conflicting sources must be handled transparently
- Answer quality directly impacts user trust and decisions

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Context Ignored](failures/context-ignored.md) | Common | Critical |
| [Hallucination Despite Context](failures/hallucination-despite-context.md) | Common | Critical |
| [Source Contradiction](failures/source-contradiction.md) | Common | High |
| [Cherry-Picking Evidence](failures/cherry-picking.md) | Common | High |
| [Parametric Override](failures/parametric-override.md) | Common | High |
| [Synthesis Errors](failures/synthesis-errors.md) | Common | Medium |
| [Confidence Miscalibration](failures/confidence-miscalibration.md) | Very Common | High |

## Key Statistics

| Finding | Source |
|---------|--------|
| Legal RAG tools hallucinate 17-33% despite retrieval | Stanford Study |
| RAG reduces hallucination by only 30-50% vs. baseline | Research Analysis |
| 52% of enterprise AI responses contain fabrications | Enterprise Survey 2026 |

## Key Metrics

- Faithfulness (answer supported by context)
- Answer correctness (vs. ground truth)
- Context utilization rate
- Hallucination rate
