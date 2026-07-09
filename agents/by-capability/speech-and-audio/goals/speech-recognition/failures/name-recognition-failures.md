# Name Recognition Failures

## Issue: ASR Fails to Correctly Transcribe Personal and Business Names

**Frequency**: Very Common

**Symptoms**
- Customer names consistently misspelled
- Business names transcribed as common words
- Ethnic names particularly error-prone
- Account lookups fail due to name mismatch
- Address names (streets, cities) wrong

**Root Cause**
Names are open-vocabulary—they can be any sequence of sounds, including rare combinations not in ASR training data. Ethnic names, unusual spellings, and names that sound like common words are especially problematic. Since names are often critical for identity and account lookup, errors directly impact transaction success.

**Example**
```
Scenario: Bank account lookup

User: "My name is Siobhan O'Brien"
ASR attempts:
  - "My name is Sha von O'Brien"
  - "My name is See oh bon O'Brien"  
  - "My name is Chevon O'Brien"
Correct: "Siobhan O'Brien"
Account found: No

User: "The account is under Nguyen"
ASR: "The account is under Win" / "New Yen" / "Gwen"
Correct: "Nguyen"
Account found: No

User: "I'm calling about my son, Aditya Krishnamurthy"
ASR: "I'm calling about my son, a duty a Krishna Murphy"
Correct: "Aditya Krishnamurthy"

Name error analysis:
  Name lookups attempted: 10,000
  Exact match success: 6,200 (62%)
  Fuzzy match recovered: 2,100 (21%)
  Failed lookups: 1,700 (17%)
  
Error distribution:
  Anglo names: 8% error rate
  Hispanic names: 15% error rate
  Asian names: 25% error rate
  African names: 28% error rate
  Gaelic/Celtic names: 22% error rate
```

**Key Statistics**
From Name Recognition Research (2026):
- Name WER: 20-40% (vs. 5-10% for common words)
- Ethnic name error rate: 2-4x higher
- Failed account lookups from name errors: 15-20%
- Customer callbacks due to name issues: 12%
- Name-based discrimination complaints increasing

**Common Name Errors**
| Name Type | Error Pattern | Error Rate |
|-----------|---------------|------------|
| Gaelic (Siobhan) | Phonetic mismatch | 30-40% |
| Vietnamese (Nguyen) | Unfamiliar phonemes | 35-45% |
| Indian (Krishnamurthy) | Length/complexity | 25-35% |
| Arabic (Abdulrahman) | Compound handling | 20-30% |
| Chinese (Xiaoping) | Tone/romanization | 25-35% |

**Contributing Factors**
- Names not in ASR vocabulary
- Ethnic phonemes missing
- No name-specific model
- Spelling vs. pronunciation mismatch
- No fuzzy matching in lookup
- Training data bias toward Western names

## Mitigation Strategies

### Prevention
1. **Comprehensive Name Vocabulary Database**: Build name inventory from customer databases (actual names in system) + public name lists (10K+ most common names across ethnicities). Include phonetic pronunciations for non-standard names (Siobhan → /ʃɪ'voʊn/, Nguyen → /wɪn/, etc.). Inject all names into ASR lexicon with boosted probabilities during decoding. Implement context-aware boosting: if user searching for "accounts", pre-load known account holder names. Update quarterly with new customer names. Use weighted sampling: common names higher weight than rare.
2. **Ethnic Phoneme Coverage & Acoustic Modeling**: Audit ASR acoustic model for coverage of phonemes from major ethnic groups (Vietnamese /ŋ/, Hindi retroflexes, Mandarin tones, Arabic pharyngeals). Augment training data with name-specific speech from diverse speakers. Train specialized name-recognition model on name-only audio. Implement name-specific confidence adjustment: boost confidence for well-represented phonemes, lower for rare combinations. Use transfer learning: pretrain name model on multilingual data, fine-tune on customer names.
3. **Fuzzy Matching & Phonetic Similarity Lookup**: Instead of exact name matching after ASR, implement fuzzy lookup using Soundex, Metaphone, or ML-based phonetic distance. Pre-compute all account holder names and their phonetic variants. During lookup, generate phonetic variants of transcribed name, check against all variants. Target 90%+ recovery rate for names that have correct phonetic match despite spelling error. Implement name similarity scoring: threshold for auto-accept vs. confirmation.

### Detection & Response
1. **Name-Specific WER Monitoring**: Segment transcription accuracy for sequences tagged as names vs. common words. Target: Name WER <15% (vs. general WER <5%). Track separately: Western names, Asian names, African names, Arabic names, Hispanic names. Alert when name WER for any ethnicity exceeds 20% or rises 5+ points from baseline. Monthly ethnicity-specific error analysis: identify high-error name patterns.
2. **Account Lookup Failure Analysis**: Track failed account lookups. Segment by reason: name mismatch (60-70%), ambiguous name match (15-20%), other (10-15%). For name-mismatch failures, compare ASR transcription to actual name. Measure recovery rate: how many would succeed with fuzzy matching. Alert if >15% failures are from name errors, trigger name vocabulary/lookup improvement.
3. **Name Confirmation Accuracy Tracking**: When agent asks user to confirm name, track acceptance rate. If user rejects 3+ times, escalate to spelling mode. Monitor if accepted "confirmed" names still cause lookup failures (indicates confirmation ineffective). Target: >98% of confirmed names found in system. Alert: <95%, review confirmation process.

### Architecture Patterns
1. **Multi-Stage Name Recognition Pipeline**: Stage 1: ASR generates transcription. Stage 2: Name entity recognition tags likely names. Stage 3: Name validation against customer DB using fuzzy matching (phonetic + string similarity). Stage 4: If confidence <80%, request confirmation or spelling. Stage 5: Spelling mode letter-by-letter: "Is that S-I-O-B-H-A-N?". Implement confidence threshold routing: high-confidence (>90%) → auto-lookup; medium (70-90%) → confirmation; low (<70%) → spelling mode.
2. **Phonetic Variant Generation Engine**: For transcribed name, generate phonetic variants using multiple algorithms (Soundex, Metaphone, custom ethnic phonetic rules). Create name variant tree at indexing time for all account holder names. During lookup, perform tree search with fuzzy matching. Implement prefix matching: "Kri" matches "Krishnamurthy" even if remainder unclear. Use confidence scoring: exact match highest, phonetic match medium, prefix match lowest. Return confidence-ranked candidates.
3. **Spelling Mode Integration**: When name recognition fails or confidence low, transition to spelling mode. Ask user to spell name letter-by-letter: "I'll need to confirm the spelling. Is that spelled S for Sierra, I for India...". Implement alphabet challenge-response: user spells name, agent repeats back (e.g., "So that's Sierra-Iota-Omega-Bravo-Hotel-Alpha-November?"), user confirms. Implement abort: if spelling takes >30s or >5 corrections, escalate to human.

### Metrics
1. **name_word_error_rate_percent**: Target: <15% overall; <18% for non-Western names. Measure: name_errors / total_names_transcribed. Track by ethnicity. Alert: Any ethnicity >20%.
2. **name_lookup_success_rate_percent**: Target: 95%+ of transcribed names successfully matched to accounts (exact or fuzzy). Measure: successful_lookups / total_name_lookups. Alert: <90%.
3. **phonetic_variant_recovery_rate_percent**: Target: 85%+ of phonetically-similar-but-misspelled names recovered via fuzzy matching. Measure: (would_succeed_with_fuzzy) / (failed_exact_match). Alert: <75%.
4. **name_confirmation_acceptance_rate_percent**: Target: 98%+ of confirmed names found in system, indicating confirmation effective. Measure: confirmed_names_found / total_confirmations. Alert: <95%.
5. **name_ethnicity_error_gap**: Target: <5% absolute error rate gap between highest-error and lowest-error ethnic groups. Measure: max_ethnicity_error - min_ethnicity_error. Alert: >10%, indicates discriminatory failure.

### Alerts
1. **Name Recognition Failure** (P2): Condition - User unable to complete call due to name transcription error (3+ retries, then escalation). Action: Alert customer service, log name for vocabulary improvement, follow up with customer, offer apology credit.
2. **Ethnic Name Discrimination** (P1): Condition - Any ethnic name group has >20% error rate or error rate 3x+ higher than baseline ethnic group. Action: Immediate escalation to legal/compliance, pause deployment, initiate retraining on balanced ethnic data, prepare customer communication.
3. **Fuzzy Matching Ineffective** (P2): Condition - >10% of failed exact-match lookups still not found with fuzzy phonetic matching, indicating phonetic model issues. Action: Audit fuzzy matching algorithm, review phonetic representations, consider retraining phonetic model, evaluate adding more name variants.

---

## References

- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Name issues
- [Stanford: Racial Disparities in ASR](https://www.pnas.org/doi/10.1073/pnas.1915768117) - Name bias
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Identity handling
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
