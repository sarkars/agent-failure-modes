# Missing PII Detection Framework

## Issue: Team relies on ad-hoc regex or manual review for PII detection/redaction instead of adopting an established, maintained framework, missing entity types and edge cases the framework would catch by default.

**Frequency**: Common

**Symptoms**
- PII redaction logic is a small set of hand-written regexes (email, phone, SSN patterns) rather than an NER-plus-pattern-plus-checksum pipeline
- Detection misses common entity types (addresses, dates of birth, financial account numbers, medical record numbers) that a maintained NER model would flag by default
- Regex patterns show high false-negative rates on non-US formats (international phone numbers, IBANs, non-US national ID numbers) because they were only ever tested against US-centric samples
- No confidence scoring exists on matches, so redaction is all-or-nothing: a pattern either fires and masks the text, or the entity silently passes through unredacted
- Redaction logic is duplicated across services (one regex set at ingestion, a different ad-hoc filter before logging) with no shared library, so coverage silently drifts between them
- PII exposure is discovered only through customer complaints or manual spot-checks, not through proactive scanning of a representative sample of stored transcripts

**Root Cause**
Team relies on ad-hoc regex or manual review for PII detection/redaction instead of adopting an established, maintained framework, missing entity types and edge cases the framework would catch by default.

**Example**
```
A fintech onboarding pipeline uses an LLM agent to extract and summarize applicant
identity documents before handing structured fields to a KYC service. To keep raw
document text out of long-term logs, an engineer wrote three regexes to redact
email, US phone numbers, and 9-digit SSNs before the extracted text was persisted
to the audit log store.

Six months later a compliance audit sampled stored logs and found unredacted
UK National Insurance numbers, passport numbers, and full home addresses sitting
in plaintext across thousands of records - none of which the original regex set
was ever built to catch, since the team had only tested against US-formatted
sample documents. There was no confidence scoring or entity-type inventory to
reveal the gap earlier; the regexes either matched or didn't, with no signal
that whole categories of identifiers were never being checked at all. The
company had to notify affected users in three jurisdictions and rebuild the
redaction layer under regulatory deadline pressure, work that an established
PII detection framework's default entity library would have covered from day one.
```

**Contributing Factors**
- No evaluation of established open-source PII frameworks (analyzer + anonymizer + confidence scoring) was done before building custom regex-based detection in-house
- PII redaction was treated as "a quick regex task" and assigned to whichever engineer had spare time, rather than routed through security/compliance for a build-vs-buy decision
- Shipping deadline pressure led to copying generic regex snippets rather than mapping detection coverage against the org's actual data classification policy
- No single owner was assigned to the redaction pipeline, so entity coverage was never revisited as new document formats and locales were onboarded downstream
- Compliance requirements were captured only as a high-level "PII must be redacted" checkbox, never translated into a concrete list of entity types the detector needed to cover

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| International format coverage | Support transcript containing UK NI numbers, German phone numbers, and IBANs alongside a US SSN | All entities detected and redacted with per-entity confidence scores | Non-US formatted entities pass through unredacted |
| Low-confidence entity handling | Ambiguous numeric string that could be an account number or an internal order ID | Entity flagged to a review queue with confidence score attached, not silently released or silently blocked | Entity is treated as a certain match (or ignored entirely) with no confidence signal recorded |
| Cross-format consistency | The same customer's PII embedded in a PDF invoice, a chat transcript, and a structured JSON log | Detector finds the same entity types at comparable recall across all three formats | Detection rate varies significantly by input format |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| PII recall on labeled benchmark | >= 95% recall | Run the detector monthly against a held-out, human-labeled sample of production-like data covering all compliance-mandated entity types |
| False negative rate on international formats | < 5% | Sample transcripts from non-US locales; compare detector output against manual labels |
| Entity type coverage ratio | 100% of org's compliance-mandated entity list | Diff the detector's supported entity types against the data classification policy each quarter |

---

## Mitigation Strategies

### Prevention
1. **Adopt Microsoft Presidio (or equivalent maintained framework)**: Replace hand-written regex with an analyzer that combines NER models, pattern matching, and checksum validators (e.g., Luhn for card numbers), each returning a confidence score, plus an anonymizer for consistent masking/hashing/redaction.
2. **Run a build-vs-buy evaluation before new PII work**: Before extending any regex-based detector, compare its entity coverage against the org's actual data classification/compliance entity list and against a maintained framework's default coverage.
3. **Centralize redaction into one shared library/service**: Route ingestion, logging, and prompt-assembly redaction through a single canonical detector instead of letting each service maintain its own copy.

### Detection & Response
1. **Scheduled sampling audits**: Pull a random sample of stored transcripts/logs weekly and re-run them through the canonical detector to catch entities the legacy ad-hoc method missed.
2. **Confidence-score review queue**: Route low-confidence detections to human review instead of silently passing them through or silently blocking them.
3. **Incident postmortems**: Treat any customer-reported or audit-discovered PII exposure as a trigger to identify which entity type/locale/format was missed and add a corresponding regression test case.

### Architecture Patterns
1. **Analyzer + anonymizer separation**: Separate detection (entities + confidence scores) from the redaction action (mask/hash/redact) so redaction policy can be tuned per entity type without touching detection logic.
2. **Defense-in-depth redaction points**: Redact at ingestion, before storage, and again before model input/prompt assembly and logging - not just at a single chokepoint.
3. **Shadow-mode migration**: Run the new framework alongside the legacy regex in shadow mode, diff outputs on real traffic, and only cut over once recall parity (or improvement) is confirmed.

### Metrics
1. **pii_recall_rate**: Target: >= 95%; Alert threshold: < 90%
2. **unredacted_entity_incidents_per_month**: Target: 0; Alert threshold: >= 1
3. **entity_type_coverage_ratio**: Target: 100% of compliance-mandated entity types; Alert threshold: < 90%

### Alerts
1. **Unredacted PII Detected in Stored Data** (P1 - Critical): Condition - audit scan finds a compliance-listed entity type present unmasked in stored transcripts/logs. Action: page on-call security, quarantine affected records, open incident review.
2. **PII Recall Regression** (P2 - Warning): Condition - weekly benchmark recall drops more than 5 points from baseline. Action: block deployment of detector changes, notify pipeline owner.
3. **Entity Coverage Gap on New Source** (P3 - Info): Condition - a new document format or data source is onboarded without a recorded PII framework coverage check. Action: notify data platform team to run a coverage check before go-live.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| unredacted_pii_incidents_per_month | >= 1 |
| pii_detection_recall_pct | < 90% |
| manual_review_queue_backlog_hours | > 24h |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Unredacted PII found in production logs | Audit scan flags a compliance-listed entity type unmasked in stored data | High |
| Recall drop on scheduled benchmark | Weekly recall benchmark falls more than 5 points below baseline | High |
| New data source onboarded without coverage check | A new ingestion source goes live without a recorded PII framework coverage confirmation | Medium |

---

## Related Patterns

- [PII Field Exposure](../../tool-access-scope-limits/failures/pii-field-exposure.md) - the downstream symptom (PII actually exposed); this pattern is the upstream root cause of not adopting a proven detection framework in the first place
- [PII Field Leakage in Responses](../../tool-access-scope-limits/failures/pii-field-leakage-in-responses.md) - a related downstream leakage symptom this pattern's missing framework would help prevent

## References

- [Microsoft Presidio: PII Detection Guide 2026](https://explainx.ai/blog/microsoft-presidio-pii-detection-anonymization-guide-2026) - open-source framework combining NER, regex, and checksum validation with confidence scoring, plus an anonymizer for redaction/masking/hashing
- [Preventing PII leakage when using LLMs: An introduction to Microsoft's Presidio](https://ploomber.io/blog/presidio/) - recommended pipeline placement: analyze input, anonymize, retrieve, redact chunks, assemble prompt, redact output before storing the trace
- [The complete guide to PII detection and redaction tools for AI pipelines in regulated industries](https://predictionguard.com/blog/pii-detection-redaction-llm-pipelines-regulated-industries) - survey of PII tooling options for regulated-industry AI pipelines
