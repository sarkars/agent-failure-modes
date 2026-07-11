# Conflicting Information

## Issue: Conflicting Information Across Document Locations

**Frequency**: Common

**Symptoms**
- Same field appears in multiple places with different values
- Agent picks arbitrary or first occurrence
- No reconciliation or flagging of conflicts

**Root Cause**
Long documents may contain draft values, amendments, corrections, or simple errors resulting in the same information appearing multiple times with conflicting values.

**Example**
```
Input: 150-page contract
Page 3: "Contract Value: $500,000"
Page 47 (Amendment A): "Revised Contract Value: $475,000"
Page 98 (Final Terms): "Total Contract Value: $475,000 + $25,000 bonus = $500,000"

Agent extraction: "$500,000" (grabbed first occurrence)

Result: Agent missed amendment, used superseded value
```

## Mitigation Strategies

### Prevention
1. **Multi-location extraction with cross-comparison**: Extract every occurrence of a field across the full document rather than stopping at the first match, then diff the values before committing any single one downstream. Trade-off: increases extraction cost roughly linearly with document length since every page must be scanned for the field, not just the first hit.
2. **Amendment/supersession section detection**: Classify sections as "original," "amendment," or "final terms" using structural cues (headings like "Amendment A," "Revised," "Final Terms") and apply a recency-wins heuristic only within that classification, not raw page order. Trade-off: depends on documents following recognizable amendment-labeling conventions; free-form renegotiation language may not be caught.
3. **Explicit reconciliation prompting**: When multiple values for the same field are found, force the agent to reason explicitly about which one is authoritative and why (e.g., "cite the clause that supersedes the others") rather than silently picking one, making the reconciliation logic auditable.

### Detection & Response
1. **Field-value variance monitoring**: Track, per document type, how often extracted fields have multiple non-identical candidate values across the source document; a sudden rise flags either a new document template or a broken reconciliation step.
2. **Low-confidence conflict escalation**: When automatic recency/amendment heuristics can't determine which value is authoritative with high confidence, route the specific conflict (not the whole document) to a human reviewer with all candidate values and their source locations shown side by side.
3. **Downstream reconciliation audits**: Periodically sample extracted "final" values against manual re-reads of the full source document to check whether the reconciliation logic actually picked the value a human would consider authoritative.

### Architecture Patterns
1. **Extract-then-reconcile pipeline**: Separate the extraction stage (pull every candidate value with its page/location) from a dedicated reconciliation stage that applies recency/amendment rules, so reconciliation logic can be tested, versioned, and audited independently of extraction.
2. **Provenance-tagged extraction**: Store each extracted value with its source location (page, section) and extraction confidence, so any downstream conflict can be traced back to exactly where the conflicting values came from without re-scanning the document.
3. **Human-in-the-loop conflict queue**: Route only genuinely ambiguous conflicts (not all multi-occurrence fields) to a lightweight review UI showing the conflicting values with surrounding context, keeping human effort focused on the cases automation can't resolve.

### Metrics
1. **multi_value_field_rate**: Target: track as baseline per document type, no fixed target; Alert if it changes > 20% week-over-week without a known template change
2. **conflict_auto_resolution_rate**: Target: > 90% of detected conflicts resolved without human review; Alert if < 75%
3. **reconciliation_accuracy_vs_manual_read**: Target: > 97% agreement in periodic audit sampling; Alert if < 90%
4. **conflict_review_queue_backlog**: Target: median resolution time < 4 hours; Alert if > 24 hours

### Alerts
1. **Conflict Rate Spike** (P2): Condition - multi-value field detection rate exceeds baseline by 20%+ for a document source. Action: Sample recent documents from that source to check for a new template or amendment convention the reconciliation logic doesn't handle.
2. **Reconciliation Accuracy Drop** (P1): Condition - periodic audit shows reconciliation accuracy below 90% against manual re-read. Action: Freeze auto-reconciliation for the affected document type, route all conflicts to human review until root cause is fixed.
3. **Review Queue Backlog** (P3): Condition - conflict review queue median resolution time exceeds 24 hours. Action: Add reviewer capacity or tighten auto-resolution confidence threshold to reduce queue volume.

## References

- [Why Frontier Agents Can't Read Documents](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - Long document challenges
- [Document AI: Next Evolution of IDP](https://www.llamaindex.ai/blog/document-ai-the-next-evolution-of-intelligent-document-processing) - Multi-location extraction
- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - Conflict resolution
