# Goal: Multimodal Reliability

Vision-Language Models (VLMs) and multimodal LLMs bring new capabilities to document processing, but also introduce failure modes that differ fundamentally from traditional OCR.

## Business Context

- Silent failures pass bad data to production systems
- Hallucinated content causes compliance and legal risks
- Miscalibrated confidence prevents effective human routing

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Plausible Wrong Outputs](failures/plausible-wrong-outputs.md) | Very Common | Critical |
| [Fabricated Content](failures/fabricated-content.md) | Common | Critical |
| [Object Hallucination](failures/object-hallucination.md) | Occasional | High |
| [Attribute Hallucination](failures/attribute-hallucination.md) | Common | High |
| [Relational Hallucination](failures/relational-hallucination.md) | Common | High |
| [Visual Degradation](failures/visual-degradation.md) | Common | High |
| [Table Cell Omission](failures/table-cell-omission.md) | Very Common | High |
| [Complex Table Structures](failures/complex-tables.md) | Common | High |
| [Input Quality Gap](failures/input-quality-gap.md) | Very Common | High |
| [Confidence Miscalibration](failures/confidence-miscalibration.md) | Very Common | High |

## Key Statistics

| Finding | Source |
|---------|--------|
| Frontier agents score <50% on enterprise document reasoning | Databricks OfficeQA |
| VLMs fail silently on ambiguous inputs | NeurIPS 2025 |
| 52% of enterprise AI responses contain fabrications | Enterprise Survey 2026 |

## Key Metrics

- Silent failure rate
- Hallucination detection rate
- Confidence calibration error
