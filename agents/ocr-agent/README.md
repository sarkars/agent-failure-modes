# OCR Agent

OCR (Optical Character Recognition) Agents extract text and structured data from images and documents. They're commonly used in invoice processing, ID verification, form digitization, and document archival.

## Goals

| Goal | Description | Common Issues |
|------|-------------|---------------|
| [Extraction Quality](extraction-quality.md) | Accurate text extraction from documents | Character confusion, font handling, noise |
| [Layout Understanding](layout-understanding.md) | Preserving document structure | Table detection, column ordering, headers |
| [Document Classification](document-classification.md) | Identifying document types | Similar templates, multi-page handling |
| [Multimodal Failures](multimodal-failures.md) | VLM and multimodal LLM-specific issues | Silent failures, hallucination, confidence calibration |
| [Agentic Failures](agentic-failures.md) | AI agent orchestration failures | Tool calling, reasoning errors, infinite loops |
| [Production Pipeline Failures](production-pipeline-failures.md) | System-level extraction failures | Template drift, integration errors, silent failures |

## Key Challenges

1. **Image Quality Variability**: Production documents range from pristine scans to phone photos of crumpled papers
2. **Domain-Specific Vocabulary**: Technical terms, abbreviations, and codes that don't appear in training data
3. **Structured Data Extraction**: Converting visual layouts into machine-readable formats
4. **Multi-Language Support**: Handling mixed-language documents and special characters
5. **Silent Failures**: VLMs and MLLMs fail silently with plausible-looking wrong outputs
6. **Template Drift**: Vendor format changes break extraction without triggering alerts
7. **Agent Orchestration**: Multi-tool pipelines introduce new failure modes at the reasoning layer

## Key Statistics (2026)

| Finding | Source |
|---------|--------|
| 88% of businesses report errors in automated data pipelines | Parseur 2026 |
| 50%+ of OCR data requires manual checking | Enterprise Survey |
| Frontier agents score <50% on enterprise document reasoning | Databricks OfficeQA |
| 30% of invoice requests fail first iteration (templates) | Accenture |
| Legacy OCR plateaus at 60-70% automation | Industry analysis |
| IDP reduces error rates by 52% vs OCR-only | Benchmark study |
| VLMs fail silently on ambiguous inputs | NeurIPS 2025 |

## Common Evaluation Metrics

- Character Error Rate (CER)
- Word Error Rate (WER)
- Field-level accuracy (for structured extraction)
- End-to-end accuracy (correct document, correct fields, correct values)
- Silent failure rate (wrong outputs with no error signal)
- Human escalation rate (documents routed to review)
