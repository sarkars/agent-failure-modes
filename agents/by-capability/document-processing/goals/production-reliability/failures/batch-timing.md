# Batch Timing Failures

## Issue: Batch Processing Timing Failures

**Frequency**: Occasional

**Symptoms**
- Documents processed out of order
- Amendments processed before originals
- Cut-off date violations

**Root Cause**
Batch processing doesn't guarantee order. Documents may arrive, be scanned, or be processed in unexpected sequences.

**Example**
```
Received: Amendment to Invoice #123 (processed at 2:00 PM)
Received: Original Invoice #123 (processed at 4:00 PM)

Result: Amendment rejected - "Invoice #123 not found"
        Original processed - amendment never applied
```

## Mitigation Strategies

### Prevention
1. **Dependency detection before processing**: Before processing a document, check whether it references or depends on another document (e.g., "Amendment to Invoice #123") and, if the referenced document hasn't been processed yet, queue the dependent document rather than rejecting it outright. Trade-off: requires reliable reference detection, which itself can fail on documents with ambiguous or missing reference identifiers.
2. **Idempotent processing operations**: Design every processing step (extraction, ERP write, notification) to be safely re-runnable with the same input producing the same result, so a document held in a dependency queue and reprocessed later — or reprocessed after a failure — never creates duplicate or conflicting records. Trade-off: requires deduplication/upsert logic throughout the pipeline rather than simple append-only writes.
3. **Explicit sequence/version numbering over arrival-time ordering**: Where the document source can provide it (vendor invoice numbering, contract amendment sequence), use explicit sequence or version numbers to establish true logical order rather than relying on scan/arrival timestamp, since arrival order and logical order frequently diverge in real-world document flows. Trade-off: many document sources don't provide reliable sequence metadata, so this only helps where such metadata exists.

### Detection & Response
1. **Dependency-queue depth and age monitoring**: Track how many documents are sitting in the dependency-wait queue and for how long, since a growing queue with aging entries indicates dependent documents whose referenced originals never arrived (dead dependencies) needing manual intervention.
2. **Rejection-then-later-arrival correlation**: When a document is rejected for a missing dependency (e.g., "Invoice #123 not found"), log the rejection and automatically re-check when a document with the referenced ID arrives later, rather than requiring the rejected document to be manually resubmitted.
3. **Out-of-order processing audit sampling**: Periodically sample processed document chains (original + amendments) to verify the final state reflects the correct logical order of application, since out-of-order application can silently produce a "successfully processed" but logically wrong final state.

### Architecture Patterns
1. **Dependency-aware queue with automatic requeue on resolution**: Architect batch processing around an explicit dependency graph where documents with unresolved references are held in a distinct queue state and automatically triggered for reprocessing when their dependency resolves, rather than a simple FIFO or arrival-order queue.
2. **Event-sourced document state with replay**: Model each document/entity's state as a sequence of applied events (original, amendment 1, amendment 2, ...) that can be replayed in corrected logical order if a timing issue is detected, rather than a single mutable record that's overwritten in arrival order.
3. **Idempotency keys on every write**: Attach a stable idempotency key (derived from document identity + operation type) to every downstream write operation, so retries and out-of-order reprocessing can be safely deduplicated by downstream systems.

### Metrics
1. **dependency_queue_depth**: Target: < 50 documents waiting at any time; Alert if > 200 or growing for > 48 hours
2. **dead_dependency_rate**: Target: < 1% of queued documents never resolve within 7 days; Alert if > 5%
3. **out_of_order_processing_rate**: Target: < 2% of document chains show out-of-order application (via audit); Alert if > 8%
4. **reprocessing_idempotency_failure_rate**: Target: 0% of reprocessing attempts create duplicate/conflicting records; Alert on any occurrence

### Alerts
1. **Dependency Queue Backlog** (P2): Condition - dependency queue depth exceeds 200 or has been growing for more than 48 hours. Action: Investigate whether a specific document source is systematically producing orphaned dependent documents (originals never arriving), escalate to manual reconciliation.
2. **Dead Dependency Accumulation** (P3): Condition - dead dependency rate (referenced document never arrives within 7 days) exceeds 5%. Action: Route affected documents to human review for manual linkage or resolution.
3. **Idempotency Violation** (P1): Condition - a reprocessing event creates a duplicate or conflicting downstream record. Action: Treat as an incident; halt the affected write path, deduplicate the created records, fix the idempotency key logic before resuming.

## References

- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - Batch processing patterns
- [Agentic Document Processing](https://www.llamaindex.ai/blog/agentic-document-processing) - Document ordering
- [IDP Challenges 2026](https://idp-software.com/guides/idp-challenges-2026/) - Processing dependencies
