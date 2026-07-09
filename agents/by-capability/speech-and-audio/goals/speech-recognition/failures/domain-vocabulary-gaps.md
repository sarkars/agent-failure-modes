# Domain Vocabulary Gaps

## Issue: ASR Fails to Recognize Industry-Specific Terms

**Frequency**: Common

**Symptoms**
- Technical terms transcribed as similar common words
- Product names consistently wrong
- Medical/legal/financial terms mangled
- Acronyms expanded incorrectly
- Jargon replaced with phonetically similar words

**Root Cause**
General-purpose ASR models are trained on common speech and lack domain-specific vocabulary. Medical terms, product names, technical jargon, and industry acronyms are either missing from the vocabulary or have low probability, causing the ASR to substitute more common words that sound similar.

**Example**
```
Scenario: Healthcare voice assistant

Patient: "I'm taking metformin for my diabetes"
ASR: "I'm taking met for men for my diabetes"

Doctor note: "Patient presents with dyspnea and tachycardia"
ASR: "Patient presents with this near and tacky card area"

Prescription: "Lisinopril 10mg once daily"
ASR: "Listen a pill 10mg once daily"

Domain vocabulary analysis:
  Medical terms in utterance: 847
  Correctly transcribed: 612 (72%)
  Phonetically mangled: 198 (23%)
  Completely wrong: 37 (5%)

Critical errors:
  - Drug names wrong: 15% (dangerous for prescriptions)
  - Dosages misheard: 8% (safety risk)
  - Conditions wrong: 12% (misdiagnosis risk)
  
Comparison with domain-adapted ASR:
  General ASR medical accuracy: 72%
  Domain-adapted accuracy: 94%
```

**Key Statistics**
From Domain ASR Research (2026):
- General ASR on medical terms: 70-80% accuracy
- Domain-adapted ASR: 92-97% accuracy
- Legal terminology: 25% error rate with general ASR
- Financial products: 30% error rate
- Technology terms: 20% error rate

**Domain Vocabulary Gaps**
| Domain | Common Errors | Risk Level |
|--------|---------------|------------|
| Medical | Drug names, conditions | Critical |
| Legal | Case citations, Latin terms | High |
| Financial | Product names, ticker symbols | High |
| Technology | Commands, product names | Medium |
| Automotive | Part names, model numbers | Medium |

**Contributing Factors**
- ASR trained on general speech corpora
- Domain terms rare in training data
- No custom vocabulary injection
- Acronyms not in pronunciation dictionary
- New products/terms not added
- No domain-specific language model

## Mitigation Strategies

### Prevention
1. **Domain-Specific Vocabulary Injection Pipeline**: Maintain domain term inventory (medical: 5K+ drug names, conditions; legal: 3K+ terms; financial: 2K+ products). Inject custom lexicon into ASR with phonetic pronunciations at decoding time. Use pronunciation rules specific to domain (e.g., medical Latin, legal French). Update vocabulary quarterly with new product launches, FDA approvals, regulatory terms. Implement A/B testing of pronunciation variants to optimize accuracy.
2. **Domain Language Model Ensembling**: Train domain-specific language models (LM) on domain corpora (medical journal abstracts, legal documents, financial transcripts). Deploy LM-weighted decoding that combines general LM with domain LM. Use context priors: if conversation mentions "medication", boost medical term LM weight by 3-5x. For risk-critical domains (healthcare, legal), enforce minimum domain LM score thresholds before accepting transcription.
3. **Contextual Semantic Boosting**: Before each utterance, extract expected domain terms from conversation state, user profile, or task context. Pass these as "hints" or "boosts" to ASR (typically 2-3x weight increase). Example: User is discussing "Lisinopril prescription" → boost drug name variants in search graph. Implement time-decay for context relevance (older hints expire faster). Measure guidance accuracy to prevent over-boosting wrong terms.

### Detection & Response
1. **Out-of-Vocabulary (OOV) Rate Tracking**: Monitor percentage of domain terms in transcribed output that are OOV (not in ASR vocabulary). Target: <2% OOV for critical domains. Segment by domain: medical <2%, legal <3%, financial <2%. Alert when OOV rate increases 1+ point from baseline, indicating vocabulary drift or new terminology. Automatically trigger vocabulary update process for high-frequency OOV terms.
2. **Domain Term Accuracy Auditing**: Segment transcription accuracy specifically on domain-critical terms (drug names, product names, monetary amounts). Target: 95%+ accuracy on high-risk terms. Implement automated comparison of transcribed domain terms against canonical lists. Track false positives (general words mistranscribed as domain terms) separately. Monthly domain expert review of 100+ error examples.
3. **Semantic Plausibility Checking**: For each domain term transcribed, verify semantic plausibility in context. Example: If medical assistant heard "metformin" but ASR output "met for men", check if "metformin" plausible in medical conversation vs. "met for men". Use domain knowledge graphs to flag implausible terms. Alert on >3 implausible terms per 100 utterances, triggering re-analysis.

### Architecture Patterns
1. **Custom Lexicon Decoding Intercept**: Place pre-decoding stage that extracts custom vocabulary rules from domain registry (drug list, product names, acronyms). Pass lexicon weights into Viterbi search graph during ASR decoding. Use pronunciation variant tables specific to domain pronunciation rules. Fallback to base pronunciation if domain-specific not available. Implement versioning of lexicon (v1, v2, v3) to safely roll out new terms without breaking production.
2. **Dual-Model Confirmation Pipeline**: Run transcription through both general ASR model and domain-specific model (if available). Compare outputs: if differ, flag as high-uncertainty for human review or additional confirmation. Use confidence score blending: if domain model confidence >85% AND general model <70%, trust domain model. Implement timeout logic so domain model doesn't block if slower than general.
3. **Post-Processing Rule Engine with Semantic Repair**: After ASR transcription, run domain-specific post-processing rules (regex-based or ML-based) to detect and correct likely domain term errors. Example rules: "met for men" → "metformin", "listen a pill" → "lisinopril". Use context from conversation history (recent mentions of medications, diagnoses) to guide corrections. Implement human review queue for novel patterns.

### Metrics
1. **domain_term_accuracy_percent**: Target: 95%+ for critical terms (drugs, products, amounts). Measure: (correct_domain_terms) / (total_domain_terms_in_reference). Track by domain and term category. Alert: <93% accuracy or >2 point drop from baseline.
2. **out_of_vocabulary_rate_percent**: Target: <2% for critical domains, <3% for medium-risk. Measure: (oov_terms) / (total_terms). Alert: increase of >0.5 points indicates vocabulary gap.
3. **domain_vocabulary_coverage_percent**: Target: 99%+ of domain terms present in ASR + custom lexicon. Measure: (covered_terms) / (total_terms_in_domain_registry). Alert: <98% coverage, trigger immediate vocabulary sync.
4. **semantic_implausibility_rate**: Target: <1% of transcriptions contain semantically implausible domain terms. Measure: (implausible_terms) / (total_terms). Alert: >2%, escalate to domain review.
5. **domain_assisted_wer_vs_general_wer**: Target: Domain-adapted WER 15-20% lower than general. Measure: WER on domain-specific test set with/without domain features. Track improvement as justification for domain customization cost.

### Alerts
1. **Critical Domain Term Misrecognition** (P1): Condition - Drug name, medical condition, or financial product incorrectly transcribed 2+ times in 1-hour window for same entity. Action: Immediate alert to domain expert, add term to custom lexicon with corrected pronunciation, re-test on recent examples, consider vocabulary freeze pending review.
2. **Domain Vocabulary Drift** (P2): Condition - OOV rate increases 1+ point from 7-day rolling average, OR >10 new high-frequency OOV terms detected in 24 hours. Action: Trigger vocabulary audit, identify new products/terms causing gap, add to domain lexicon, retest, plan vocabulary release.
3. **Semantic Implausibility Spike** (P2): Condition - Implausible domain term substitutions detected at >2x baseline rate in 1-hour window. Action: Alert ML team, check for model degradation, review recent training data changes, consider rollback if spike >5x baseline.

---

## References

- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Vocabulary issues
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Domain adaptation
- [Google Cloud Speech: Custom Vocabulary](https://cloud.google.com/speech-to-text/docs/speech-adaptation) - Customization
- [AWS Transcribe: Custom Vocabulary](https://docs.aws.amazon.com/transcribe/latest/dg/custom-vocabulary.html) - Domain terms
