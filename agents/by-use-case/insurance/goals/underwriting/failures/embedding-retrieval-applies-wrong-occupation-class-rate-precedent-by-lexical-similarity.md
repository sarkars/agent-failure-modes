# Embedding-Retrieval Applies Wrong Occupation-Class Rate Precedent by Lexical Similarity

## Issue: An Underwriting Agent's Retrieval Step, Used to Find a "Similar Prior Case" Precedent for Classifying an Applicant's Occupation Into the Correct Risk Class for Pricing, Surfaces a Prior Underwriting Case That Is Embedding-Similar by Job-Title Wording but Belongs to a Materially Different Risk Class, Causing the Agent to Apply the Wrong Class's Rate Factor to the Current Applicant

**Frequency**: Occasional

**Symptoms**
- An applicant is priced under an occupation risk class that does not match the actual duties described in their application, while matching the job-title wording of a retrieved but substantively different prior case
- The retrieved precedent case shares similar words in the job title (e.g., both contain "technician" or "engineer") but involves materially different on-the-job risk exposure (field versus office-based, hazardous-materials handling versus none)
- Re-running the classification with the applicant's full duty description, rather than job-title text alone, yields a different and more appropriate risk class
- The mis-classification pattern recurs for occupation titles that are lexically similar across genuinely different risk profiles (e.g., "field service technician" for HVAC versus for software systems)
- Underwriting audit sampling finds the rate factor applied traces back to a retrieved precedent case rather than to the current applicant's own duty description

**Example**
```
Applicant lists their occupation as "field service technician" for a telecommunications equipment installer, a role
involving primarily low-roof indoor cabling work with minimal fall-height or hazardous-material exposure
Underwriting agent's retrieval step searches prior underwriting cases for a similar occupation to determine the
correct risk class and rate factor, and surfaces a prior case also titled "field service technician" -- but for an
industrial refrigeration repair role involving elevated platform work and ammonia-based refrigerant handling
The two roles are embedding-similar due to shared job-title wording but belong to different risk classes under the
carrier's occupation-classification schedule
Agent applies the refrigeration technician's higher-risk rate factor to the telecom applicant, producing an
overpriced quote; a different applicant in a reverse scenario could be underpriced for an actually higher-risk role
On manual review, the underwriter notes the duty description in the application clearly indicates indoor cabling
work, which the correct classification schedule would have priced into a lower risk class entirely
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey work on LLM agent hallucination and grounding failures documents retrieval-augmented pipelines surfacing topically or lexically similar but substantively mismatched source material as a recurring failure mechanism distinct from outright fabrication | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Broader failure-mode research on LLM systems documents retrieval-step mismatches -- where a similarity-ranked result is substantively wrong despite superficial relevance -- as a distinct and recurring root cause separate from generation-time errors | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |
| Execution-provenance research argues that without evidence tracing linking a pricing decision to the actual duty-description match criteria rather than just a retrieved precedent's similarity score, reviewers cannot verify whether a classification is substantively justified | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- The retrieval step ranks prior cases primarily by job-title text similarity rather than by the structured risk attributes (work environment, hazard exposure, equipment handled) that actually determine the correct occupation class
- The occupation-classification schedule's risk-determining attributes are not consistently captured as structured, separately indexed fields the retrieval step could match on instead of free-text job titles
- The agent treats a high-similarity retrieved precedent as sufficient justification for a classification decision without independently verifying the retrieved case's actual duty profile matches the current applicant's stated duties
- No discrepancy check compares the applicant's own duty-description text against the retrieved precedent's duty description before the precedent's rate factor is applied

---

## Mitigation Strategies

1. **Structured Attribute Matching Over Title-Text Similarity**: Re-rank or filter retrieved occupation precedents using structured risk attributes (work environment, hazard exposure category, equipment handled) rather than relying primarily on job-title lexical similarity
2. **Duty-Description Discrepancy Check**: Require an automated comparison between the applicant's stated duty description and the retrieved precedent's duty description before the precedent's rate factor is applied, flagging material mismatches for manual classification
3. **Classification Confidence Threshold**: Require retrieval similarity scores below a defined confidence threshold, or any case with materially different hazard-attribute tags, to route to manual underwriter classification rather than automatic application
4. **Audit Sample of Retrieval-Based Classifications**: Periodically sample occupation classifications driven by retrieval precedent and verify the underlying duty-description match against the actual classification schedule criteria

### Metrics
- Rate of occupation classifications where the applied rate factor traces to a retrieved precedent with a hazard-attribute mismatch against the applicant's stated duties
- Number of underwriting audit findings citing occupation mis-classification due to title-similarity-driven retrieval
- Average duty-description similarity score versus structured-attribute match rate across classified applications

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Hazard-attribute mismatch on applied classification | Retrieved precedent's hazard attributes differ materially from applicant's stated duty description | P2 | Route to manual underwriter classification before binding |
| Low structured-attribute confidence | Retrieval match relies primarily on title-text similarity with low structured-attribute overlap | P3 | Flag for classification review before quote is finalized |
| Repeated mis-classification pattern | Same occupation-title pair recurringly mis-classified across multiple applications within a rolling window | P2 | Audit classification-schedule indexing and retrieval ranking logic |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
