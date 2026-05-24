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

**Mitigation Strategies**
1. **Custom vocabulary**: Add domain terms to ASR lexicon
2. **Domain LM**: Use domain-specific language model
3. **Boosting**: Increase probability of expected terms
4. **Hints/context**: Provide likely terms as hints
5. **Post-processing**: Domain-specific correction rules
6. **Regular updates**: Add new products/terms continuously

**Detection**
- Track accuracy on domain-specific terms
- Monitor OOV (out-of-vocabulary) rates
- Review transcriptions of technical conversations
- Compare general vs. domain-adapted performance
- Survey domain experts on transcription quality

## References

- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Vocabulary issues
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Domain adaptation
- [Google Cloud Speech: Custom Vocabulary](https://cloud.google.com/speech-to-text/docs/speech-adaptation) - Customization
- [AWS Transcribe: Custom Vocabulary](https://docs.aws.amazon.com/transcribe/latest/dg/custom-vocabulary.html) - Domain terms
