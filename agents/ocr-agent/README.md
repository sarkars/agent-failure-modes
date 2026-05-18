# OCR Agent

OCR (Optical Character Recognition) Agents extract text and structured data from images and documents. They're commonly used in invoice processing, ID verification, form digitization, and document archival.

## Goals

| Goal | Description | Common Issues |
|------|-------------|---------------|
| [Extraction Quality](extraction-quality.md) | Accurate text extraction from documents | Character confusion, font handling, noise |
| [Layout Understanding](layout-understanding.md) | Preserving document structure | Table detection, column ordering, headers |
| [Document Classification](document-classification.md) | Identifying document types | Similar templates, multi-page handling |

## Key Challenges

1. **Image Quality Variability**: Production documents range from pristine scans to phone photos of crumpled papers
2. **Domain-Specific Vocabulary**: Technical terms, abbreviations, and codes that don't appear in training data
3. **Structured Data Extraction**: Converting visual layouts into machine-readable formats
4. **Multi-Language Support**: Handling mixed-language documents and special characters

## Common Evaluation Metrics

- Character Error Rate (CER)
- Word Error Rate (WER)
- Field-level accuracy (for structured extraction)
- End-to-end accuracy (correct document, correct fields, correct values)
