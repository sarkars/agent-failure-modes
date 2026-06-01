# AI Model Reliability

> LLM hallucination, verification integrity, and model accuracy in mortgage document processing

## Overview

As mortgage lenders deploy LLMs and AI models for document processing and underwriting, new failure modes emerge. This goal covers failures specific to AI model behavior—hallucination in data extraction, the "verification collapse" where AI validates its own work, and the gap between vendor promises and production reality.

## Key Statistics

| Finding | Source |
|---------|--------|
| Rocket Mortgage's LLM achieves 90% accuracy on document extraction | AWS Case Study |
| LLMs hallucinate on financial specifics (rates, terms, eligibility) | PerformLine Research |
| Lenders report AI solutions "falling short in quiet, distributed ways" | Indecomm 2026 |
| 63% of AI-using lenders rely on AI for document classification/indexing | Industry Survey |
| 54% use AI for data extraction | Industry Survey |

## Failure Patterns (7)

| Pattern | Description | Frequency |
|---------|-------------|-----------|
| [Verification Collapse](failures/verification-collapse.md) | AI systems validating their own outputs without independent verification | Critical |
| [Extraction Hallucination](failures/extraction-hallucination.md) | LLMs fabricating or misreading values from mortgage documents | Common |
| [Confidence Miscalibration](failures/confidence-miscalibration.md) | AI reporting high confidence on incorrect extractions | Common |
| [Template Brittleness](failures/template-brittleness.md) | Models failing when document formats change | Common |
| [Vendor Promise Gap](failures/vendor-promise-gap.md) | Marketed accuracy vs. production reality | Common |
| [Silent Downstream Errors](failures/silent-downstream-errors.md) | Extraction errors propagating undetected through workflow | Occasional |
| [Human Review Bottleneck](failures/human-review-bottleneck.md) | Exception queues overwhelming manual review capacity | Common |

## Why This Goal Matters

AI reliability in mortgage processing creates unique risks:

1. **Verification Collapse**: When AI systems "sign their own homework," validating the same data they rely on to make decisions, a dangerous dynamic emerges. Speed has outpaced data integrity.

2. **Hallucination in High-Stakes Context**: Unlike general chatbots, hallucinated mortgage data directly impacts loan eligibility, compliance, and borrower outcomes.

3. **Quiet Failures**: Most AI failures in mortgage are "quiet and distributed rather than loud and obvious." Unreliable output requires downstream manual rechecks.

4. **Vendor Overpromise**: "There's a misconception in the market that IDP is a magic wand. Vendors often overpromise and underdeliver, touting 100 percent accuracy."

## The Verification Collapse Problem

> "Decision engines are increasingly 'signing their own homework,' validating the same data they rely on to make decisions. This is the Verification Collapse."
> — National Mortgage Professional, 2026

When AI underwriting validates AI-extracted data without independent verification:
- Income figures extracted by AI → validated by AI
- Asset verification automated → approved by same system
- Document classification → trusted without human review
- Fraud signals → filtered by same model that approved the loan

## References

- [NMP: The Verification Collapse](https://nationalmortgageprofessional.com/news/verification-collapse-why-ai-underwriting-building-fragile-foundation)
- [Indecomm: Why Document AI Breaks Mortgage Ops](https://indecomm.com/article/why-document-ai-breaks-mortgage-ops/)
- [AWS: Rocket Close Case Study](https://aws.amazon.com/blogs/machine-learning/rocket-close-transforms-mortgage-document-processing-with-amazon-bedrock-and-amazon-textract/)
- [SCN Soft: LLMs for Mortgage](https://www.scnsoft.com/lending/large-language-models)
- [PerformLine: How LLMs Represent Financial Products](https://performline.com/blog-post/how-llms-represent-financial-products/)
