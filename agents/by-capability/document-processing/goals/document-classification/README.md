# What Are the Most Common Document Classification Problems in AI Agents?

**Document classification fails when a pipeline cannot correctly determine what a document is, where it starts and ends, or which schema applies, before extraction ever begins.** The root causes split into three distinct problems — pages that don't map cleanly onto document boundaries (blank pages, embedded attachments, scrambled multi-page batches), documents that look structurally identical to a different type or version (invoice vs. purchase order, 2023 template vs. 2024 template), and quality gates that reject readable-but-degraded input. Classification failures matter because every downstream extraction step inherits whatever the classifier got wrong — a purchase order routed through an invoice schema extracts nothing meaningful, since "Amount Due" doesn't exist on a PO.

## Key Takeaways

- 6 patterns cover document classification, grouped into three mechanisms: document-boundary detection, type/version confusion between similar templates, and quality-based rejection.
- Similar-templates failures are common across a documented set of confusable pairs — invoice/purchase-order, quote/invoice, receipt/invoice, packing-slip/invoice, statement/invoice, and credit-memo/invoice all share layouts, logos, or line-item structure closely enough to defeat layout-only classification.
- Boundary-detection failures compound in both directions: batch scans can over-split (one invoice becomes two documents) or under-split (two invoices merge into one), and both directions require the same multi-signal boundary-confidence fix.
- Quality rejection is a calibration failure, not a detection failure — the mitigation is tiered/channel-specific quality routing rather than a single global accept/reject threshold, since a fax channel has a lower achievable quality ceiling than a flatbed scan.

## Scope

- **Document-boundary detection** — [blank-pages](failures/blank-pages.md), [embedded-documents](failures/embedded-documents.md), [page-grouping](failures/page-grouping.md). All three are about determining what constitutes one document unit before classification runs: filtering non-content pages, detecting a nested document inside a container (an invoice attached to an email), and correctly grouping/splitting pages in a batch scan.
- **Type and version confusion** — [similar-templates](failures/similar-templates.md), [version-confusion](failures/version-confusion.md). Both are cases where the document is correctly identified as belonging to a document-unit, but the wrong type or wrong schema version gets assigned because layout, logo, and field structure look alike across types (invoice vs. PO) or across time (2023 vs. 2024 template from the same sender).
- **Quality-based rejection** — [quality-rejection](failures/quality-rejection.md). A quality gate calibrated for a high-fidelity source (flatbed scan) incorrectly rejects legitimate but lower-fidelity input (fax, copy-of-a-copy) as unreadable.

## When Document Classification Matters

- Documents arrive as batch scans, bulk uploads, or email attachments where page-to-document boundaries aren't given upfront and must be inferred
- The same sender or industry produces multiple document types (invoice, PO, packing slip, credit memo) sharing near-identical templates, logos, and line-item layouts
- Input arrives through mixed channels (fax, mobile photo, flatbed scan) where a single global quality threshold would systematically over-reject the lowest-fidelity channel

## Cross-Pattern Insight

All 6 patterns converge on the same two-part fix: combine multiple weak signals into a single confidence score, then route only the low-confidence cases to human review rather than gating on any one signal alone. Boundary detection fuses separator sheets, first-page indicators, and continuity analysis because each fails in different scenarios; type confusion fuses header-term detection with field-presence validation because layout alone can't distinguish an invoice from a PO; version confusion fuses template fingerprinting with date-based fallback because senders don't always retire old templates cleanly; and quality rejection replaces a binary threshold with per-channel calibration plus a tiered enhanced-processing path. In every pattern, the mitigation explicitly rejects a single hard-coded rule or threshold in favor of a confidence-scored, multi-signal decision with a human-review escape valve for the ambiguous middle.

## Frequently Asked Questions

### What's the difference between similar-templates and version-confusion?
Similar-templates is confusion between different document *types* that share a layout — classifying a purchase order as an invoice. Version-confusion is confusion between different *versions* of the same document type from the same sender — correctly classifying something as an invoice but applying the wrong (e.g., 2023 vs. 2024) field-position schema to it.

### How is document-classification's version-confusion different from production-reliability's template-drift?
Version-confusion is a per-document routing problem: a single document needs the right schema version selected from a registry of known variants. [Template drift](../production-reliability/failures/template-drift.md) in Production Reliability is a fleet-level monitoring problem: detecting, at the pipeline level, that a sender has started using an unrecognized template across many documents and the registry itself needs updating.

### How does page grouping fail in both directions — over-splitting and under-splitting?
Both directions trace back to the same missing signal: an explicit document boundary marker. Without separator sheets or a reliable first-page indicator, continuity/header-matching analysis has to infer boundaries from content similarity, and it either over-trusts weak similarity (under-splitting, merging two documents) or under-trusts a false discontinuity (over-splitting one document into several).

### Can a stricter quality threshold reduce downstream extraction errors?
Not without a cost. The quality-rejection pattern shows that tightening a global quality threshold reduces bad input reaching extraction but also rejects legitimate, readable documents (a readable fax) — the actual fix is per-channel calibrated thresholds plus a tiered enhanced/manual-assist path, not a single stricter global cutoff.

### Which classification failures cause the most downstream damage?
Similar-templates misclassification is typically the most damaging because it doesn't just delay processing — it actively runs the wrong extraction schema, extracting nothing meaningful from fields that don't exist on the actual document type (no "Amount Due" on a PO) and can route a document into the wrong business workflow entirely (a PO sent to an AP payment workflow).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Blank Pages](failures/blank-pages.md) | Blank/near-blank or signature-only pages classified as a document type or flooding review |
| [Embedded Documents](failures/embedded-documents.md) | Attachment inside a container file classified only as the container, swallowing the nested document |
| [Page Grouping](failures/page-grouping.md) | Batch-scan pages incorrectly split, merged, or scrambled across document boundaries |
| [Quality Rejection](failures/quality-rejection.md) | Overly aggressive quality gate rejects legitimate low-fidelity (fax, copy) documents |
| [Similar Templates](failures/similar-templates.md) | Shared layout/logo across document types (invoice vs. PO) defeats classification |
| [Version Confusion](failures/version-confusion.md) | Correct type, wrong template-version schema applied to a drifted document layout |

**Total: 6 patterns**

## Related Goals

- [Accurate Text Extraction](../accurate-text-extraction/) — runs after classification succeeds, and inherits whatever document type/schema classification assigned
- [Production Reliability](../production-reliability/) — fleet-level template drift and accuracy monitoring, versus per-document classification decisions here
- [Agentic Orchestration](../agentic-orchestration/) — reasoning and tool-call failures that occur once a document has already been classified and handed to an agent
