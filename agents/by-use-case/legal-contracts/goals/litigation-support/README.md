# What Are the Most Common Litigation-Support Failures in AI Agents?

**Litigation-support failures concentrate on three points in the evidence-handling pipeline: classifying discovery documents for relevance when vocabulary shifts (code names, abbreviations, terminology drift over time) cause the classifier to miss genuinely responsive documents; omitting material admissions from deposition summaries due to positional bias (mid-document content is systematically under-weighted); and failing to identify privileged communications when they arrive through indirect channels (forwarded threads, in-house counsel without legal-domain email addresses, business executives summarizing legal advice).** Unlike contract-analysis failures, litigation-support failures bear directly on case outcomes and ethics rules: missed responsive documents create spoliation exposure, omitted admissions undermine case preparation, inadvertent privilege waivers destroy attorney-client protection and create waiver-related sanctions. Because the outputs (discovery classifications, deposition summaries, privilege logs) are themselves litigation artifacts, errors in the agent's work become discoverable and attackable by opposing counsel.

## Key Takeaways

- 3 patterns are documented here: vocabulary-mismatch discovery misclassification (code names and abbreviations cause false negatives), positional bias in long-document summarization (mid-document content systematically omitted), and privilege misidentification (privilege-by-reference and work-product missed when they arrive through indirect communication channels).
- Vocabulary mismatch is a well-documented TAR (technology-assisted review) failure requiring active-learning iteration; static keyword or similarity classifiers achieve unacceptably high false-negative rates on documents using internal terminology unknown to the classifier at training time.
- Positional bias in long-context summarization is a property of transformer attention mechanisms: mid-document content is retrieved and represented far less reliably than beginning or end content, even when the entire document is within context window, producing a U-shaped recall curve where middle-third recall can drop 10-15 percentage points below end-content recall on the same material.
- Privilege misidentification via metadata heuristics (attorney sender/recipient filtering) has a documented false-negative rate above acceptable thresholds; multi-pass attorney sampling is the standard mitigation precisely because single-pass automated privilege classification is not considered reliable enough to certify production without independent verification.

## Scope

- **Discovery Vocabulary Mismatch** — [Discovery Document Relevance Misclassification](failures/discovery-document-relevance-misclassification.md). Code names and abbreviations cause vocabulary blindness in similarity classifiers, leading to false-negative (non-responsive) classifications of genuinely responsive documents.
- **Positional Bias** — [Positional Bias Omits Mid-Document Admission in Deposition Summary](failures/positional-bias-omits-mid-document-admission-in-deposition-summary.md). Mid-document admissions in long transcripts are systematically omitted from summaries despite being within the model's context window, due to attention-weight distribution in long-context processing.
- **Privilege Misidentification** — [Privilege Waiver Risk in AI-Assisted Document Review](failures/privilege-waiver-risk.md). Privilege-by-reference communications (business-executive emails summarizing legal advice, internal memos discussing legal strategy) are classified as non-privileged because metadata heuristics miss indirect privilege channels.

## When Litigation-Support Matters

- A document-review project involves discovery on a matter with internal code names, project names, or abbreviations that don't appear in the discovery request's literal terms
- A deposition or other long-form document needs to be summarized and trial/deposition teams will rely on the summary for preparation or cross-examination
- A privilege review is being certified for production and the producing party needs to have confidence that privileged material will not be inadvertently produced

## Cross-Pattern Insight

Litigation-support failures are particularly high-stakes because litigation artifacts themselves carry legal consequences and ethical obligations. All 3 patterns share a dependence on heuristics or single-pass classification that omit or misclassify material content: vocabulary heuristics miss terminology shifts, positional weighting misses middle-document content, metadata filters miss indirect privilege channels. Unlike contract-analysis failures (which often surface only in disputes years later), litigation failures can be audited and attacked during discovery itself. The mitigation across all three is to pair automated classification with iterative human review: active-learning vocabulary discovery for discovery classification, overlap-chunked summarization with deterministic sweep verification for depositions, and multi-pass attorney sampling with explicit false-negative rate tracking for privilege.

## Frequently Asked Questions

### How do you find missed responsive documents caused by vocabulary mismatch?
Before classification runs, conduct vocabulary discovery: custodian interviews, document sampling, and codename-identification to build a codename-to-standard-term map. Seed the classifier with expanded vocabulary. After classification, sample borderline cases (confidence 40-60%) plus a random 5% for attorney review, feeding corrections back to the classifier iteratively until misclassification rates stabilize — see [Discovery Document Relevance Misclassification](failures/discovery-document-relevance-misclassification.md).

### Can you prevent positional bias in deposition summaries?
The documented mitigation is to split long documents into overlapping chunks smaller than the length at which positional degradation occurs, summarize each chunk independently, then merge chunk summaries — the chunked approach prevents any passage from being structurally disadvantaged by its position in the document. Additionally, run a deterministic keyword/entity sweep across the entire document in parallel, and flag any sweep hit not in the summary for attorney review — see [Positional Bias Omits Mid-Document Admission in Deposition Summary](failures/positional-bias-omits-mid-document-admission-in-deposition-summary.md).

### How do you prevent inadvertent privilege waiver in discovery production?
Use purpose-driven classification, not metadata-only heuristics: scan all documents for advice-seeking language and legal-risk content regardless of sender; identify privilege-by-reference (business communications relaying legal advice), work product (litigation strategy memos), and litigation-preparation language. Then mandatory multi-pass attorney sampling: sample 10%+ of agent-classified-as-non-privileged documents, have licensed attorney review, calculate false-negative rate. If >2%, expand sample or re-classify entire set. Before production, require attorney sign-off on privilege log with specific, defensible basis statements — see [Privilege Waiver Risk in AI-Assisted Document Review](failures/privilege-waiver-risk.md).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Discovery Document Relevance Misclassification](failures/discovery-document-relevance-misclassification.md) | Vocabulary mismatch from code names and abbreviations causes classifier to miss responsive documents using internal terminology |
| [Positional Bias Omits Mid-Document Admission in Deposition Summary](failures/positional-bias-omits-mid-document-admission-in-deposition-summary.md) | Long-document summarization systematically under-weights middle-third content, omitting material admissions despite full in-context availability |
| [Privilege Waiver Risk in AI-Assisted Document Review](failures/privilege-waiver-risk.md) | Metadata-heuristic privilege classification misses privilege-by-reference and work-product protected communications arriving through indirect channels |

**Total: 3 patterns**

## Related Goals

- [Compliance](../compliance/) — where similar multi-agent handoff failures occur between review and summary stages in regulatory contexts
- [Due Diligence](../due-diligence/) — where multi-agent handoff and entity-matching risks occur in contract and financial analysis
