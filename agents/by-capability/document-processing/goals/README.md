# Document Processing AI Agent Failures by Goal: 46 Patterns, Causes, and Fixes

**Document Processing AI agents fail in 6 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 46 documented patterns across 6 goals; the most documented is [Multimodal Reliability](multimodal-reliability/) with 10.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Document Processing Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Accurate Text Extraction](accurate-text-extraction/) | When OCR or vision-language models misread characters, numbers, or punctuation in a document image | 8 |
| [Agentic Orchestration](agentic-orchestration/) | When an agent's document reasoning is sound but the surrounding machinery — context management, tool calls, and self-correction — corrupts or loses the information the reasoning depends on. | 6 |
| [Document Classification](document-classification/) | When a pipeline cannot correctly determine what a document is, where it starts and ends, or which schema applies, before extraction ever begins. | 6 |
| [Layout Preservation](layout-preservation/) | When an agent reads every character correctly but flattens the document's two-dimensional structure into the wrong one-dimensional text stream. | 6 |
| [Multimodal Reliability](multimodal-reliability/) | When a vision-language model produces a fluent, confident-sounding extraction that isn't actually grounded in what the document shows. | 10 |
| [Production Reliability](production-reliability/) | When a document-processing pipeline that worked in testing degrades, silently or operationally, once it runs continuously at real-world scale. | 10 |

**Total: 46 patterns**

## Frequently Asked Questions

### What makes VLM hallucinations harder to catch than classical OCR errors?

Because classical OCR fails loudly — an unreadable character produces garbled output or a blank, which is visibly wrong. See [Multimodal Reliability](multimodal-reliability/).

### What's the difference between accuracy-regression and template-drift?

Accuracy-regression is caused by a pipeline-side change — a new model or prompt version deployed by the team running the pipeline. See [Production Reliability](production-reliability/).

### What's the difference between accurate text extraction and multimodal reliability failures?

Text extraction failures are character-level misreads — the model gets individual glyphs or words wrong, such as a `0` read as `O`. See [Accurate Text Extraction](accurate-text-extraction/).

## Related

- [Document Processing overview](../)
- [All agent failure patterns](../../../)
