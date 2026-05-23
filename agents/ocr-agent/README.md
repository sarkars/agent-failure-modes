# OCR Agent

OCR (Optical Character Recognition) Agents extract text and structured data from images and documents. They're commonly used in invoice processing, ID verification, form digitization, and document archival.

## Goals

| Goal | Description | Failure Patterns |
|------|-------------|------------------|
| [Accurate Text Extraction](goals/accurate-text-extraction/) | Extract text correctly from documents | 8 patterns |
| [Layout Preservation](goals/layout-preservation/) | Preserve document structure and spatial relationships | 6 patterns |
| [Document Classification](goals/document-classification/) | Correctly identify document types | 6 patterns |
| [Multimodal Reliability](goals/multimodal-reliability/) | Handle VLM/MLLM-specific failure modes | 10 patterns |
| [Agentic Orchestration](goals/agentic-orchestration/) | Orchestrate multi-tool document processing | 8 patterns |
| [Production Reliability](goals/production-reliability/) | Operate reliably at scale | 10 patterns |

## Structure

```
ocr-agent/
├── README.md
└── goals/
    ├── accurate-text-extraction/
    │   ├── README.md
    │   └── failures/
    │       ├── character-confusion.md
    │       ├── punctuation-errors.md
    │       └── ...
    ├── layout-preservation/
    │   ├── README.md
    │   └── failures/
    │       └── ...
    ├── document-classification/
    ├── multimodal-reliability/
    ├── agentic-orchestration/
    └── production-reliability/
```

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
