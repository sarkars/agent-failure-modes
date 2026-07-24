# Positional Bias Omits Mid-Document Admission in Deposition Summary

## Issue: Agent Summarizing a Long Deposition Transcript or Produced Document Systematically Under-Weights Content in the Middle of the Document, Omitting a Material Admission That Was Fully Within the Model's Context Window and Correctly Classified as Relevant

**Frequency**: Occasional

**Symptoms**
- A summary of a long deposition transcript (100+ pages) accurately captures statements from the opening background questioning and the closing questions, but omits a specific, damaging admission made roughly in the middle of the transcript, even though that portion was included in full in the model's input context
- The omitted admission is not filtered out by any relevance classifier — the document as a whole is correctly flagged as responsive/relevant, and the specific passage is not excluded by any keyword or vocabulary mismatch; it is simply absent from the generated summary despite being present and readable in the source text
- Re-running the same summarization request with the transcript re-ordered so the admission appears near the beginning or end (all other content unchanged) reliably surfaces the same admission in the summary, isolating the failure to the passage's position rather than its content or phrasing
- Attorneys preparing for trial or a subsequent deposition based on the agent-generated summary are unaware the admission exists in their own case file until a later full manual read-through, opposing counsel's use of the same testimony, or cross-examination surfaces it
- The omission rate increases with transcript length and is concentrated on passages roughly in the middle third of the document, following a documented U-shaped pattern rather than being randomly distributed

**Root Cause**
Long-context summarization by LLMs exhibits a well-documented positional bias in which information located near the beginning or end of the input context is retrieved and represented far more reliably than information in the middle, even when the entire document is fully within the context window and no content is dropped due to truncation. This is a property of how transformer-based models attend to and weight positions across long inputs during generation, not a relevance-classification failure or a vocabulary-matching gap — the content is present, in scope, and available to the model, but is disproportionately likely to be omitted from the generated output purely because of where it falls in the document. A deterministic keyword-search or full-text-index tool applied uniformly across the document would not exhibit this positional degradation; it would find the passage regardless of location.

**Example**
```
Scenario: 140-page deposition transcript of a former product manager, produced during discovery in a
product-liability matter, is fed in full to a summarization agent to prepare a witness-examination
outline for trial
Pages 1-15 (background, employment history): Summary accurately captures witness's role and tenure
Pages 60-75 (middle of the transcript, mid-deposition): Witness states, in response to a direct
question, that engineering flagged the defect internally six months before the product shipped and
that this was communicated to leadership -- a central admission for the case
Pages 125-140 (closing questions, counsel wrap-up): Summary accurately captures closing stipulations
Generated summary: Thoroughly covers the opening and closing sections; the mid-deposition admission
about the internal defect warning is not mentioned anywhere in the summary, despite pages 60-75 being
fully included in the input and the transcript overall being correctly used as the source for trial prep
Impact: Trial team builds its examination outline without reference to the case's most consequential
admission, discovered only when opposing counsel raises it during a pretrial hearing
```

**Key Statistics**
| Finding | Context |
|---|---|
| The foundational study on this phenomenon finds that language model performance is highest when relevant information occurs at the beginning or end of the input context and degrades significantly when the relevant information is in the middle of long contexts, even for models explicitly designed for long-context use | [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) |
| Long-document summarization research documents a U-shaped positional bias favoring content at the beginning and end of a document while neglecting middle content, including a demonstrated example on a long legal opinion | [ARC: Argument Representation and Coverage Analysis for Zero-Shot Long Document Summarization with Instruction Following LLMs](https://arxiv.org/html/2505.23654) |
| Faithfulness research on long-form summarization confirms the same U-shaped trend, finding that models faithfully summarize beginning and end content while neglecting middle content regardless of the middle content's actual relevance or importance | [On Positional Bias of Faithfulness for Long-form Summarization](https://arxiv.org/abs/2410.23609) |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Admission planted in document middle | Long transcript with a known material admission inserted at ~50% document position | Summary includes the admission | Summary omits the admission despite it being fully in-context |
| Same admission planted at document start/end | Identical transcript with the same admission moved to the first or last 10% of the document | Summary includes the admission | Summary omits the admission (would indicate a deeper failure beyond positional bias) |
| Position-shuffle consistency check | Same transcript content, admission relocated to multiple different positions across repeated runs | Admission recall rate should not vary sharply by position | Recall rate is materially lower for middle-third placements than for start/end placements |
| Chunked-summarization control | Same transcript processed in smaller overlapping chunks with per-chunk summaries merged, rather than single-pass full-document summarization | Admission is captured regardless of its position in the original document | Single-pass summary omits it while chunked approach retains it, confirming positional degradation as the mechanism |

### Evaluation Dataset
- **Source**: Deposition and produced-document transcripts (redacted/synthetic where real case material is unavailable) with known material statements inserted at controlled positions (10%, 25%, 50%, 75%, 90% through the document), modeled on the "needle in a haystack" long-context evaluation methodology
- **Size**: 100+ transcript variants across at least 5 position buckets, with 3+ document lengths (50, 100, 200 pages) to observe the length-dependence of the effect
- **Key variations**: document length; admission position; admission phrasing (explicit vs. phrased as a response to a compound question); single-pass vs. chunked summarization pipeline

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Position-independent recall rate | > 95% at every document-position bucket | % of planted material statements correctly included in the summary, broken out by position bucket (start/middle/end) |
| Start-vs-middle recall gap | < 5 percentage points | Difference in recall rate between start/end position buckets and the middle-third bucket |
| Chunked-vs-single-pass recall delta | Chunked approach should not show a materially higher recall than single-pass, once mitigations are applied | Recall rate comparison between chunked and single-pass pipelines on the same evaluation set |

### Automated Checks
```python
def check_for_failure(document_length_pages, admission_position_pct, summary_text, admission_keyphrases):
    """
    document_length_pages: int
    admission_position_pct: float, 0-100, position of the planted admission in the document
    summary_text: str, the generated summary
    admission_keyphrases: list[str], phrases that would indicate the admission was captured
    """
    admission_captured = any(phrase.lower() in summary_text.lower() for phrase in admission_keyphrases)

    is_middle_third = 33 <= admission_position_pct <= 67
    is_long_document = document_length_pages >= 80

    if is_middle_third and is_long_document and not admission_captured:
        return True  # positional-bias omission signature

    return False
```

---

## Mitigation Strategies

### Prevention
1. **Chunked Summarization with Position-Agnostic Merging**: Rather than a single full-document summarization pass, split long transcripts into overlapping chunks of bounded length, summarize each chunk independently, then merge chunk-level summaries — this prevents any single passage from being structurally disadvantaged by its position relative to the whole document.
2. **Mandatory Full-Document Keyword/Entity Sweep as a Cross-Check**: Run a deterministic keyword and named-entity sweep (not an LLM summarization pass) across the entire document for case-critical terms (product names, defect descriptions, key dates, named individuals) and require any hit not reflected in the LLM-generated summary to be flagged for attorney review, independent of the summary's own coverage.
3. **Position-Stratified Sampling for Human QA**: When human review samples a summarized transcript for quality assurance, deliberately over-sample passages from the middle third of long documents rather than sampling uniformly or focusing on start/end sections, since that is where this failure concentrates.

### Detection & Response
1. **Position-Bucketed Recall Auditing**: Periodically run known-content recall tests (planted statements at varying positions) against the production summarization pipeline and track recall rate by document-position bucket, alerting if the middle-third recall rate falls materially below the start/end recall rate.
2. **Post-Discovery Admission Trace**: When a material admission is discovered later (via opposing counsel, cross-examination, or manual re-review) that was present in a transcript the agent had already summarized, trace its position in the original document; if it falls in the middle-third band, log it as a confirmed instance of this failure mode for pipeline improvement.

### Architecture Patterns
- **Overlapping-Window Chunk-and-Merge Pipeline**: Documents are split into overlapping windows sized well below the position-degradation onset length observed in evaluation, summarized independently, and merged with de-duplication, so no passage is structurally distant from a chunk boundary.
- **Deterministic Sweep + LLM Summary Reconciliation Layer**: A non-LLM full-text/entity sweep runs in parallel with LLM summarization; a reconciliation step compares sweep hits against summary content and surfaces any sweep hit absent from the summary as a required-review item before the summary is used for case prep.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| middle_third_recall_rate | Recall rate for known-content on planted-statement audits, middle-third position bucket | < 90% |
| start_end_vs_middle_recall_gap | Difference in recall rate between start/end and middle-third position buckets | > 5 percentage points |
| sweep_summary_reconciliation_gap_count | Count of deterministic sweep hits absent from the corresponding LLM summary, per document | > 0 unreviewed |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Middle-third recall audit failure | Scheduled recall audit shows middle-third recall rate below threshold | P2 | Investigate current chunking configuration; re-run affected recent case summaries through the chunked pipeline; notify case teams using affected summaries |
| Unreconciled sweep hit on active case | Deterministic keyword/entity sweep finds a case-critical term in a transcript not reflected in its LLM summary | P1 | Route to attorney review before the summary is relied upon further; treat as a potential missed admission until confirmed otherwise |

---

## References
- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)
- [ARC: Argument Representation and Coverage Analysis for Zero-Shot Long Document Summarization with Instruction Following LLMs](https://arxiv.org/html/2505.23654)
- [On Positional Bias of Faithfulness for Long-form Summarization](https://arxiv.org/abs/2410.23609)
