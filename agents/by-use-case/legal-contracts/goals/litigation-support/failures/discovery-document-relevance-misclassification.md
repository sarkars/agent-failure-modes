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

1. **Code-Name and Terminology Discovery Step**: Before classification, run a dedicated pass to identify internal code names, abbreviations, and terminology variants for the subject matter (via custodian interviews or document sampling) and expand the search/classification vocabulary accordingly
2. **Active-Learning Iterative Refinement**: Use attorney review of borderline and randomly-sampled classified documents to iteratively retrain or adjust the classifier, rather than relying on a single static classification pass
3. **Statistically Validated Recall Sampling**: Perform recall/precision validation sampling sufficient to support a defensible certification of discovery completeness, consistent with TAR protocol standards used in court-approved processes
4. **Time-Period-Aware Vocabulary Tracking**: For long discovery date ranges, account for terminology that may have changed over time (product renamed, team restructured) rather than applying a single fixed vocabulary across the entire period

### Metrics
- Recall and precision rates from statistically validated sampling against the classifier's relevance determinations
- Number of vocabulary variants (code names, abbreviations) identified and incorporated per discovery matter
- Rate of borderline-classified documents overturned upon attorney review during active-learning passes

### Alerts
- Validated recall sampling falls below the agreed-upon or court-ordered threshold → P1
- A known code name or terminology variant for the subject matter is identified mid-review after initial classification has already run → P2

---

## References

- [Better Bill GPT: Comparing Large Language Models against Legal Invoice Reviewers](https://arxiv.org/pdf/2504.02881)
- [Semantic Parsing of Legal Text](https://arxiv.org/abs/2104.08671)
