# Content Fabrication

## Issue: AI Generates False Content Presented as Fact

**Frequency**: Very Common

**Symptoms**
- AI-generated articles contain factual errors
- Legal citations refer to non-existent cases
- AI content plagiarizes existing sources
- Generated "interviews" with people who weren't interviewed
- Fake events or quotes presented as real

**Root Cause**
AI generates content that appears authoritative but contains fabrications, errors, or plagiarized material. Unlike hallucination in responses (which users can verify), content fabrication in published material reaches audiences who assume it's been fact-checked.

**Example**
```
Case 1: CNET AI Articles (2023)

What happened:
- CNET used AI to write 77 financial explainer articles
- Published without adequate human review
- Over half (41 articles) required corrections

Errors found:
- Simple math errors in interest rate calculations
- Misunderstanding of basic financial concepts
- Plagiarized passages from other websites
- "Phrases not entirely original" in several articles

Result: Program paused, editor-in-chief left

---

Case 2: Lawyer ChatGPT Citations (2023)

What happened:
- Attorney Steven Schwartz used ChatGPT for legal research
- ChatGPT fabricated 6 court case citations
- Citations included fake quotes and detailed summaries
- Submitted in federal court brief

Result: $5,000 fine for "bad faith" and false statements
        Similar incidents followed (MyPillow case: 30 fake cases,
        Minnesota AG: AI-generated fabrications in court)
```

**Key Statistics**
From Digital Defynd AI Disasters Analysis (2026):
- CNET: 41 of 77 AI articles needed corrections (53%)
- Legal hallucinations: At least 3 major court cases with fake citations
- Google Bard: Single factual error cost $100B in market cap
- Die Aktuelle: Fired editor for AI "interview" with incapacitated celebrity

**Fabrication Types**
- **Factual errors**: Incorrect statistics, dates, or facts
- **Citation hallucination**: References to non-existent sources
- **Plagiarism**: Copying existing content without attribution
- **Fake interviews**: Generated quotes from real people
- **Event fabrication**: Made-up events presented as real (Dublin parade)
- **Historical inaccuracy**: Wrong historical claims (Google AI Overview)

**Contributing Factors**
- AI optimizes for plausibility, not truth
- No built-in fact-checking mechanism
- Human reviewers trust AI output
- Pressure to publish quickly
- AI presents fabrications confidently
- Difficult to distinguish real from generated

---

## Test Scenario & Reproduction

### Scenario Setup
- An AI content-generation pipeline producing domain-specific articles (e.g., financial explainers) or legal research output intended for publication/filing
- No mandatory citation-existence verification or expert review gate before publication
- Time/publishing-speed pressure incentivizing skipping the review step

### Trigger Mechanism
1. Generate a batch of domain-specific articles or a legal brief using the AI system without requiring citation resolution against real sources
2. Publish or submit the output without a blocking expert-review step
3. Independently attempt to resolve every citation/claim in the output against real, retrievable sources

**Example Reproduction Steps:**
```
1. Prompt the system to generate a financial explainer article involving an interest-rate calculation, mirroring the CNET program's 77-article batch
2. Prompt a legal-research variant to draft a brief citing case law relevant to a hypothetical dispute, mirroring the Schwartz ChatGPT filing
3. Attempt to resolve each cited case name against a real court-records database
4. Independently recompute the interest-rate/financial math stated in the financial article
5. Run the financial article text through a plagiarism-detection tool against existing web content
6. Record how many citations fail to resolve and how many math statements are incorrect
```

### Expected Failure State
- A meaningful fraction of generated citations (in the Schwartz case, all 6) do not resolve to any real case, or resolve to a case that doesn't support the stated quote/summary
- Financial calculations contain basic errors (as in CNET's interest-rate math mistakes) despite being presented with authoritative confidence
- Plagiarism detection flags passages as insufficiently original despite no attribution being given
- The content was published/submitted with no expert or citation-verification gate having caught any of the above before reaching the audience or the court

---

## Mitigation Strategies

### Prevention
1. **Mandatory citation-existence verification before publication**: Programmatically resolve every citation, case reference, or quoted source to a real, retrievable document before content ships — this alone would have caught all 6 fabricated case citations in the Schwartz filing and every "phrases not entirely original" plagiarism instance in the CNET articles. Trade-off: adds a verification pass that slows publication pipelines and requires access to authoritative source databases (e.g., court record systems, plagiarism indexes).
2. **Confidence-gated publication for domain content**: Route content into a "don't publish" or "flag for expert review" path when the generating model's confidence is low or the topic is domain-specialized (financial explainers, legal analysis, medical content) — directly targets the CNET pattern of publishing 77 financial articles with inadequate review. Trade-off: confidence signals from LLMs are themselves imperfectly calibrated, so this needs a secondary check, not blind trust in a confidence score.
3. **Expert human review as a hard gate, not advisory**: For domain content (legal, financial, medical), require a subject-matter expert's sign-off as a blocking step rather than an optional review — the CNET incident's root failure was publishing "without adequate human review," not the absence of a review policy on paper. Trade-off: materially slows time-to-publish and requires expert reviewer capacity that scales with content volume.

### Detection & Response
1. **Automated citation resolution audits**: Continuously sample published content and attempt to resolve every citation/reference to a real source; any citation that fails to resolve is a directly measurable fabrication signal (this is exactly how the fake ChatGPT case citations were eventually caught).
2. **Plagiarism-detection sweeps on AI-generated batches**: Run all AI-generated content through plagiarism detection before and periodically after publication, since fabrication and unattributed copying (as in the CNET "not entirely original" phrasing) often co-occur.
3. **Post-publication correction-rate tracking**: Track what fraction of AI-generated pieces require correction after publication (CNET's 53% correction rate is the benchmark for "this pipeline is broken") and treat a rising correction rate as an early warning to tighten the review gate.

### Architecture Patterns
1. **Retrieval-then-generate with citation binding**: Generate claims only from retrieved, citable source spans rather than free generation, and bind each output claim to its supporting span so downstream verification is structural, not a bolted-on check. Deployment consideration: requires a retrieval corpus authoritative enough for the domain, which isn't available for every content category.
2. **Two-stage pipeline: draft-then-verify agents**: Separate the generation agent from a dedicated verification agent whose only job is confirming citations exist and match claims, so verification isn't skipped under publishing-speed pressure. Deployment consideration: doubles inference cost per piece and adds latency to the publish pipeline.
3. **Publication circuit breaker on correction-rate spikes**: Automatically pause the AI-content pipeline (as CNET eventually did manually) when the rolling correction rate crosses a threshold, rather than relying on someone noticing and making the call. Deployment consideration: needs a reliable correction-tracking feed and an agreed threshold with the editorial/content team in advance.

### Metrics
1. **citation_resolution_rate**: % of citations/references that resolve to a real source; target 100%; alert if < 99.5%.
2. **post_publication_correction_rate**: % of AI-generated pieces requiring correction within 30 days; target < 5%; alert if > 15% (CNET's 53% is the failure case to avoid entirely).
3. **plagiarism_flag_rate**: % of AI-generated content flagged by plagiarism detection above similarity threshold; target < 1%; alert if > 5%.
4. **expert_review_bypass_rate**: % of domain-specialized content published without expert sign-off; target 0%; alert on any nonzero value.

### Alerts
1. **Unresolvable Citation Detected Pre-Publication** (P1): Condition — any citation fails resolution during the mandatory pre-publication check. Action: block publication of that piece until the citation is fixed or removed; do not allow manual override without editor sign-off.
2. **Correction Rate Spike** (P2): Condition — post_publication_correction_rate exceeds 15% over a rolling 30-day window for a content category. Action: pause AI-generation for that category pending root-cause review, mirroring the CNET program pause.
3. **Expert Review Bypassed** (P1): Condition — domain-specialized content published without a logged expert sign-off. Action: immediately unpublish or flag the content pending retroactive review; audit the publication pipeline for the gate failure.

## References

- [Digital Defynd: Top 40 AI Disasters](https://digitaldefynd.com/IQ/top-ai-disasters/) - CNET (#16), Lawyer citations (#25-27), Die Aktuelle (#17)
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Legal citation fabrication
- [Air Canada Chatbot Lawsuit](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416) - Fabricated policy information
