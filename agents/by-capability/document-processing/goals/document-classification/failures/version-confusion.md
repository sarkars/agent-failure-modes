# Version Confusion

## Issue: Version and Variant Confusion

**Frequency**: Occasional

**Symptoms**
- Old template version extracted with new schema (or vice versa)
- Different regional variants handled incorrectly
- Draft vs. final versions not distinguished

**Root Cause**
Document templates evolve over time. The same document type from the same sender may have multiple versions in circulation.

**Example**
```
Input: 2023 invoice template from Vendor B
Classification: invoice (correct)
Schema Applied: 2024 template schema (incorrect)

Result: "Total" field moved in 2024, now extracting from wrong position
```

## Mitigation Strategies

### Prevention
1. **Template fingerprinting for version detection**: Compute a layout hash/fingerprint (based on field positions, header structure, logo placement) for each document and match it against a registry of known template versions per sender, so the pipeline knows it's looking at the "2023 template" vs. "2024 template" before choosing an extraction schema. Trade-off: requires building and maintaining a template registry that's updated whenever a sender changes their document layout.
2. **Version detection as a first-class classification output**: Extend classification to output not just document type but also version/template ID (e.g., "invoice, Vendor B, v2024"), so schema selection is explicit and auditable rather than implicitly assuming the most recent schema always applies. Trade-off: adds classification complexity and requires labeled training examples per version.
3. **Date-based schema routing as a fallback signal**: When template fingerprinting is inconclusive, use the document's date (extracted or from metadata) to infer which schema version was likely in effect at that sender, since template changes correlate with time. Trade-off: senders don't always retire old templates cleanly, so a document dated in 2024 might still use the 2023 template if printed from old stock.

### Detection & Response
1. **Field-position failure monitoring by sender/template**: Track extraction failures where an expected field isn't found at its schema-defined position, broken out by sender; a spike for one sender specifically (rather than globally) signals that sender's template has changed and the schema mapping is stale.
2. **Fallback-extraction usage tracking**: Monitor how often fallback (alternate known position) extraction is invoked versus the primary schema position; a rising fallback-usage rate for a sender is an early warning that their primary template has drifted and the registry needs updating.
3. **New-fingerprint detection**: Automatically flag when a document's template fingerprint doesn't match any registered version for that sender, since this is the earliest possible signal of an undetected template change, before any field extraction even fails.

### Architecture Patterns
1. **Template-fingerprint-then-schema-select pipeline**: Architect extraction as fingerprint/version detection first, explicit schema selection second, then position-based field extraction third, rather than assuming a single fixed schema per sender.
2. **Confidence-gated human-in-the-loop review queue**: Route documents with an unrecognized template fingerprint, or with fallback-extraction triggered on critical fields, to review so the template registry can be updated with human confirmation.
3. **Versioned schema registry with fallback chain**: Maintain each sender's known schema versions with an ordered fallback chain (try v2024 positions, then v2023 positions, then generic heuristic extraction) rather than a single hardcoded schema per sender/type.

### Metrics
1. **unrecognized_template_fingerprint_rate**: Target: < 3% of documents per sender; Alert threshold: > 10%
2. **fallback_extraction_usage_rate**: Target: < 5% of field extractions; Alert threshold: > 15% for any sender
3. **field_position_failure_rate_by_sender**: Target: < 2%; Alert threshold: > 8% for any single sender
4. **template_registry_staleness**: Target: registry reviewed/updated within 30 days of a detected new fingerprint; Alert threshold: > 60 days unresolved

### Alerts
1. **New Template Fingerprint Detected** (P2): Condition - a sender's documents show an unrecognized template fingerprint at a rate above 10%. Action: Confirm new template version with a human reviewer, add to registry, define schema mapping.
2. **Fallback Extraction Surge** (P2): Condition - fallback-position extraction usage for a sender exceeds 15%. Action: Investigate whether the sender's primary template has changed; update schema registry.
3. **Registry Staleness** (P3): Condition - a detected new fingerprint remains unresolved (no schema mapping added) for more than 60 days. Action: Escalate to template registry owner for backlog resolution.

## References

- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - Template drift challenges
- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - Schema versioning strategies
- [AI Agents and Document Processing 2026](https://parsio.io/blog/ai-agents-document-processing-2026) - Template evolution handling
