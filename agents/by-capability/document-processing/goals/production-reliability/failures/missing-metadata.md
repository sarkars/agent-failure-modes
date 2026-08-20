# AI Document Extraction Fails Without Sender and Locale Context: Causes and Fixes

## Issue: Extraction Guesses Wrong Without Sender, Locale, or Historical Context

**Frequency**: Common

**Symptoms**
- Extraction accuracy varies unexpectedly across documents that look similar
- The same document type from the same vendor fails inconsistently
- The model lacks the context (sender, locale, history) it needs to disambiguate a field

**Root Cause**
The deeper pattern across extraction failures is a context engineering problem - what information the extraction model receives (document metadata, layout signals, cross-document state, domain vocabulary) determines output quality more than model size or OCR accuracy alone.

**Example**
```
Input: Invoice with ambiguous date "03/04/2024"

Without context: Could be March 4 or April 3
With vendor metadata: Vendor is UK-based, so April 3 (DD/MM format)
With historical data: This vendor always uses DD/MM

Result: Without context, 50% chance of wrong date
```

Fixing this means treating context assembly (sender metadata, locale, historical patterns) as a first-class pipeline stage, not an afterthought — a discipline commonly called context engineering in agentic RAG/extraction pipelines. The strategies below cover how to build and use that context.

## Mitigation Strategies

### Prevention
1. **Mandatory metadata enrichment before extraction**: Require sender identity, document type, and locale/region metadata to be attached and passed into the extraction context before extraction runs, rather than treating extraction as a standalone task operating only on document pixels/text — ambiguities like date format (DD/MM vs MM/DD) are only resolvable with this context, not from the document content alone. Trade-off: requires upstream systems to reliably capture and propagate this metadata, which may not exist for all intake channels.
2. **Historical-pattern lookup per source**: Before extraction, query historical extraction results from the same sender/vendor to establish source-specific conventions (date format, currency, terminology) and inject them as extraction context/priors, rather than treating every document from a known source as if seen for the first time. Trade-off: requires a data store of historical extractions and a lookup step, adding latency and infrastructure.
3. **Domain vocabulary loading by document type/industry**: Load industry-specific terminology and abbreviation mappings relevant to the detected document type (medical, legal, financial) as part of the extraction context, since generic extraction prompts without domain vocabulary will misinterpret domain-specific shorthand and terminology. Trade-off: requires maintaining and updating domain vocabularies as terminology evolves.

### Detection & Response
1. **Ambiguity-flagging when context is unavailable**: When metadata needed to resolve a genuine ambiguity (like date format) isn't available for a document, flag the specific ambiguous field explicitly rather than defaulting to a guess (e.g., always assuming MM/DD), so these cases are visible and correctable rather than silently wrong at whatever rate the default guess is incorrect.
2. **Context-availability correlation with accuracy**: Track extraction accuracy segmented by whether full context (sender metadata, historical pattern, domain vocabulary) was available for that extraction, to quantify how much context availability actually drives accuracy and prioritize context-engineering investment where the gap is largest.
3. **Source-inconsistency detection**: When historical patterns exist for a source but the current extraction result deviates from the established pattern (e.g., a vendor that has always used DD/MM suddenly appears to use MM/DD), flag for review rather than silently accepting the deviation, since it could indicate either a genuine format change or an extraction error.

### Architecture Patterns
1. **Context-engineering-first extraction architecture**: Architect the extraction pipeline so a context-assembly stage (gathering sender metadata, historical patterns, domain vocabulary, locale) runs and populates a structured context object before any extraction call, treating context completeness as a first-class pipeline concern equal in importance to model selection or OCR quality.
2. **Source-profile store with continuous updates**: Maintain a per-source profile (vendor, sender, document-type combination) that accumulates historical extraction patterns and conventions over time, feeding future extractions from the same source, and flagging when a new extraction deviates from the established profile.
3. **Cross-document state sharing for related document sets**: For document sets that are logically related (a contract and its amendments, a claim and its supporting documents), maintain shared context/state across the set so later documents in the set benefit from information established in earlier ones rather than each being processed in isolation.

### Metrics
1. **context_completeness_rate**: Target: > 90% of extractions have full context (sender, type, locale) available; Alert if < 70%
2. **accuracy_with_vs_without_context**: Target: track the gap as baseline; Alert if the gap exceeds 20 percentage points (signals context availability is a major accuracy driver needing investment)
3. **ambiguity_flag_rate**: Target: track as baseline per document type; Alert if it changes > 2x (signals either a metadata pipeline regression or genuine ambiguity increase)
4. **source_profile_deviation_rate**: Target: < 3% of extractions deviate from established source profile; Alert if > 10%

### Alerts
1. **Context Completeness Drop** (P2): Condition - context-completeness rate falls below 70% for an intake channel. Action: Investigate the upstream metadata-capture pipeline for that channel; treat as a priority fix given its outsized effect on accuracy.
2. **Accuracy Gap Widening** (P1): Condition - the accuracy gap between context-available and context-unavailable extractions exceeds 20 points. Action: Prioritize context-engineering fixes over model/OCR improvements, since context availability is shown to be the dominant driver.
3. **Source Profile Deviation Spike** (P2): Condition - deviation rate from established source profiles exceeds 10% for a source. Action: Manually verify whether the source genuinely changed conventions or whether extraction is introducing errors; update the profile only after confirming a genuine change.

## References

- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Context engineering
- [Why LLMs Hallucinate More on Enterprise Documents](https://www.adlibsoftware.com/news/why-llms-hallucinate-more-on-enterprise-documents) - Missing context impact
- [Document AI: Next Evolution of IDP](https://www.llamaindex.ai/blog/document-ai-the-next-evolution-of-intelligent-document-processing) - Metadata enrichment
