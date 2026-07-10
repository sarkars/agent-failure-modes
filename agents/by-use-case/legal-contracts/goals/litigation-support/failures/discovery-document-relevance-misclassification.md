# Discovery Document Relevance Misclassification

## Issue: Litigation-Support Agent Marks Materially Relevant Documents as Non-Responsive (or Vice Versa) During Discovery Review, Creating Spoliation or Over-Production Risk

**Frequency**: Common

**Symptoms**
- Agent classifies emails using narrow keyword matching against the discovery request's literal terms, missing relevant documents that discuss the same subject matter using different terminology or internal code names
- Documents discussing a product by its internal codename (used before public launch) are not retrieved when the discovery request references only the product's market name
- Over-inclusive classification flags large volumes of clearly irrelevant documents as potentially responsive, inflating privilege-review costs and producing documents that should have been excluded
- A document later proven highly relevant in opposing counsel's possession (obtained another way) was available in the client's own document set but classified non-responsive during the agent's review
- Sampling-based QA reveals a relevance-classification error rate above what outside counsel considers acceptable for certifying discovery completeness

**Root Cause**
Document relevance classification for discovery is frequently implemented as similarity matching between document content and the discovery request's defined terms or a seed set of known-relevant documents. This approach is brittle to vocabulary mismatch — internal code names, abbreviations, or topic drift over the relevant time period — because the classifier has no mechanism to recognize that semantically equivalent content uses different surface language unless that variation was represented in training/seed examples. Without active-learning-style iterative refinement using attorney feedback on borderline cases, the classifier's blind spots persist throughout the review rather than narrowing.

**Example**
```
Discovery request: "All documents relating to the XYZ product defect"
Internal documents: Reference the product exclusively by its pre-launch codename "Project Falcon" during the period when the defect was first identified and discussed internally
Agent's relevance classifier: Trained/seeded on documents using "XYZ," does not recognize "Project Falcon" as the same subject matter
Result: A substantial set of the most damaging internal discussions (occurring during the pre-launch period under the codename) are classified non-responsive
Discovery risk: If opposing counsel later obtains these documents independently, the producing party faces a spoliation or discovery-misconduct allegation
```

**Key Statistics**
- Vocabulary mismatch (code names, abbreviations, terminology drift over time) is a well-documented failure mode in technology-assisted review (TAR) and predictive coding literature, generally requiring iterative seed-set expansion to mitigate
- Courts applying TAR/predictive-coding protocols typically require statistically validated recall and precision sampling before certifying discovery completeness specifically because classifier blind spots of this kind are foreseeable
- Active-learning review protocols (iterative attorney feedback on borderline-classified documents) demonstrate measurably better recall on vocabulary-shifted relevant documents than static keyword/similarity classifiers in TAR validation studies

---

## Mitigation Strategies

### Prevention

1. **Pre-classification vocabulary discovery with codename/abbreviation mapping**: Before classifier runs, conduct vocabulary discovery: (a) custodian interviews to identify internal codenames/abbreviations, (b) document sampling to find terminology variants, (c) build vocabulary map: {internal_term → standard_term}. Seed classifier with expanded vocabulary. Re-run classification. Root cause: Prevents vocabulary blindness by discovering codenames before classification.

2. **Active-learning iterative refinement with attorney feedback loops**: Sample borderline classifications (confidence 40-60%) + random sample (5%) for attorney review. Attorney marks as responsive/non-responsive. Feed corrections back to classifier; update seed set; re-run affected corpus. Repeat until misclassification rate stabilizes. Root cause: Iterative refinement catches systematic errors.

3. **Recall-biased tuning with statistical validation sampling**: Configure classifier: false_negative penalty >> false_positive penalty. Accept higher false positives; privilege review downstream filters. Run statistically valid sample (n>200, attorney re-reviews independently) on final classifications. Compute recall/precision. If recall <95%, halt certification; re-run with expanded seed set. Root cause: Quantifies confidence in completeness before certifying to opposing counsel.

### Detection & Response

1. **Classification audit logging with vocabulary tracking and validation results**: Log: (a) vocabulary map built, (b) codenames discovered, (c) active-learning iterations completed, (d) validation sample results (recall/precision). Measure: codename_discovery_rate, recall, precision, vocabulary_mismatch_incidents.

2. **Post-discovery audit if opposing counsel surfaces missed documents**: If opposing counsel obtains documents we classified non-responsive, immediately trace to root cause: was it a codename we missed? Add to vocabulary; re-run classification; re-validate; assess misconduct exposure.

### Architecture Patterns

1. **Vocabulary Discovery & Mapping System**: Custodian interviews + doc sampling → codename registry.

2. **Iterative Active-Learning Classifier**: Classifier + attorney feedback on borderlines/sample → seed-set retraining.

3. **Statistically Valid Recall Sampler**: Random sample of final classifications; attorney re-review; precision/recall calculation.

### Key Metrics

| Metric | Target | Alert |
|--------|--------|-------|
| Recall (Validation Sample) | >95% | <90% |
| Precision (Validation Sample) | >75% | <65% |
| Codename Discovery Rate | >95% | <90% |
| Post-Certification Document Recovery | 0 | >0 |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Recall < 95% in Validation | Statistical sample shows missed relevant docs | CRITICAL | Halt cert; expand vocab; re-classify; re-validate |
| Codename Discovered During Review | Unidentified internal term discovered mid-review | HIGH | Add to vocab registry; re-run classification |
| Post-Certification Document Recovery | Opposing counsel obtains docs we missed | CRITICAL | Assess spoil/misconduct exposure; trace to vocab gap |

---

## References

- [Better Bill GPT: Comparing Large Language Models against Legal Invoice Reviewers](https://arxiv.org/pdf/2504.02881)
- [Semantic Parsing of Legal Text](https://arxiv.org/abs/2104.08671)
- [Technology-Assisted Review and Predictive Coding Standards](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3456789)
