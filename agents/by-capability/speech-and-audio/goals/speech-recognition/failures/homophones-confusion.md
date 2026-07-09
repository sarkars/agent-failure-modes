# Homophones Confusion

## Issue: ASR Selects Wrong Word Among Sound-Alike Options

**Frequency**: Very Common

**Symptoms**
- "To/two/too" consistently wrong
- "There/their/they're" errors
- Product names confused with common words
- Addresses transcribed incorrectly
- Commands misinterpreted as similar words

**Root Cause**
Homophones—words that sound identical but have different meanings and spellings—are fundamentally ambiguous in audio. ASR must use context to disambiguate, but context models often fail, especially for domain-specific terms, proper nouns, or short utterances without sufficient context.

**Example**
```
Scenario: E-commerce voice ordering

User: "I want to buy two blue shoes"
ASR: "I want to buy to blue shoes" ← Wrong homophone

User: "Ship it to 42 Maine Street"
ASR: "Ship it to 42 Main Street" ← Common substitution

User: "Add the Beats headphones"
ASR: "Add the beets headphones" ← Product name confusion

User: "I'll pay with my Citi card"
ASR: "I'll pay with my city card" ← Brand confusion

Homophone error analysis:
  Total utterances: 10,000
  Homophone-containing: 3,200 (32%)
  Homophone errors: 480 (15% of homophone cases)
  
High-impact errors:
  - Number homophones (two/to): 180 order quantity errors
  - Address homophones: 95 shipping errors
  - Product homophones: 205 wrong item searches
```

**Key Statistics**
From ASR Research (2026):
- 15-25% of homophone cases transcribed incorrectly
- Numbers (two/to/too): 20% error rate without context
- Addresses: 12% contain homophone errors
- Product names: 30% confused with common words
- Short utterances: 2x homophone error rate

**Common Homophone Errors**
| Sound | Options | Error Rate |
|-------|---------|------------|
| /tu:/ | to, two, too | 18-22% |
| /ðɛr/ | there, their, they're | 15-20% |
| /raɪt/ | right, write, rite | 12-18% |
| /meɪn/ | main, Maine, mane | 20-25% |
| /biːts/ | beats, beets | 35-40% |

**Contributing Factors**
- Insufficient context in short utterances
- Domain vocabulary not in language model
- Generic ASR not tuned for application
- No post-processing correction
- Homophones not in training focus
- Proper nouns treated as common words

## Mitigation Strategies

### Prevention
1. **Context-Aware Language Model Boosting**: Pre-transcription, inject expected homophones based on conversation context. If user is discussing e-commerce quantities, boost "two"/"too" probabilities over "to". Maintain per-domain confusion matrices (numbers: to/two/too, directions: there/their/they're, product names: specific variants). Use sliding window context (last 5 utterances) to inform boosting. Implement progressive boosting: utterance 1 uses global priors, utterances 2+ use specific context priors. Measure boost effectiveness via offline benchmarking before production deployment.
2. **Homophone Constraint Grammar**: For known high-error homophones, implement grammar rules that constrain search space. Example: If ASR detects numeric context ("order quantity"), restrict /tu:/ pronunciation to {two, too} and reject {to} unless preceded by preposition. Use domain-specific constraint sets: financial products, medication names, addresses. Implement soft constraints (reduce weight, don't eliminate) to avoid over-correcting unusual but valid utterances. Build constraint library from error analysis (top 20 homophone confusions per domain).
3. **Acoustic Modeling Specialization**: For highest-error homophones, augment training data with contrastive examples (to/two/too pronounced in isolation and in sentences). Train specialized acoustic model or confidence adjuster for homophone pairs. Use formant analysis (F1, F2 frequencies) to distinguish subtle pronunciation differences. Implement confidence score calibration specific to homophone pairs: if to/two/too confusion likely, lower confidence thresholds to trigger confirmation earlier.

### Detection & Response
1. **Homophone Error Pattern Monitoring**: Track error rates specifically for known homophone pairs (to/two/too: 18-22%, there/their/they're: 15-20%, right/write/rite: 12-18%). Maintain per-homophone confusion matrix. Alert when any homophone error rate increases 2+ points from baseline. Segment by context: numerical context, address context, product context. Monthly review of top 10 persistent homophone errors.
2. **Contextual Plausibility Checking**: After transcription, verify homophone choice matches context. Example: If "two" transcribed in address context ("42 Main Street"), check if "to" more plausible ("Ship to 42 Main Street"). Use semantic plausibility scorer: score homophone choice against sentence semantics. Flag low-confidence homophones (confidence 65-75%) + context mismatch for confirmation. Alert when >3 contextually implausible homophones per 100 utterances.
3. **User Confirmation Loop Integration**: When homophone detected + medium confidence (60-80%), proactively confirm: "Did you say TWO or TO?" Implement confirmation routing: auto-correct if high confidence (>90%), confirm if medium (60-90%), escalate if low (<60%). Track confirmation acceptance rate: aim for 95%+ accurate confirmations. Alert if user rejects >20% of confirmations for specific homophone.

### Architecture Patterns
1. **Multi-Pass Homophone Correction Pipeline**: Pass 1: ASR generates N-best hypotheses. Pass 2: For each N-best candidate, check if it's a high-error homophone in current context. Pass 3: Re-score based on language model and context priors. Pass 4: If confidence spread tight (top 2 candidates close), route to confirmation. Implement timeout: if multi-pass takes >1s, fallback to single-pass result to avoid latency degradation.
2. **Homophone Confidence Adjuster**: Train lightweight ML model (logistic regression, BayesNet) that predicts homophone error likelihood given: (acoustic features, language model score, preceding context, following context, domain). Use this predictor to adjust confidence: reduce confidence for high-error scenarios, increase for low-error. Implement re-calibration quarterly as error patterns evolve.
3. **Contrastive Grammar Decoding**: During ASR decoding, maintain parallel decode paths for known homophone pairs. Example: One path assumes "to", another assumes "two", another "too". Re-score paths using domain-specific language models. Select highest-scoring path as primary hypothesis. Implement fallback ranking: if primary confidence <70%, present top 3 hypotheses to user for selection (keyboard, voice confirmation, or text).

### Metrics
1. **homophone_error_rate_by_pair**: Target: <2% per homophone pair (e.g., to/two/too <2%, there/their/they're <2%). Measure: homophone_errors / total_homophone_occurrences. Track top 10 problematic pairs. Alert: Any pair >4%, escalate to model tuning.
2. **homophone_context_accuracy**: Target: 95%+ of homophones chosen correctly given context. Measure: (homophones_matching_context) / (total_homophones). Alert: <90%, indicates context model failure.
3. **homophone_confirmation_accuracy**: Target: 98%+ of user-confirmed homophones ultimately correct. Measure: (confirmed_correctly) / (total_confirmations). Alert: <95%, user confirmations unreliable, disable feature.
4. **critical_field_homophone_accuracy**: Target: 98%+ accuracy on critical fields (quantities, addresses, product names). Measure: homophone_errors on critical_fields / total_critical_fields. Alert: >1%, P1 escalation due to business impact.
5. **homophone_latency_ms**: Target: <100ms additional latency for homophone correction (multi-pass). Measure: latency(with_homophone_correction) - latency(baseline). Alert: >150ms, impacts user experience.

### Alerts
1. **Critical Field Homophone Error** (P1): Condition - Homophone error in critical field (quantity, address, amount) confirmed wrong by user. Action: Immediate alert, enable confirmation on all homophones for this user going forward, review recent ASR changes, retrain models.
2. **Homophone Error Rate Spike** (P2): Condition - Any homophone pair error rate increases 3+ points from baseline in 1-hour window. Action: Investigate recent ASR model changes, check for acoustic degradation, enable confirmations for affected homophone, consider rollback.
3. **Homophone Confirmation Loop** (P2): Condition - Same user confirms same homophone 3+ times in conversation, indicating persistent error. Action: Alert product team, switch to explicit confirmation mode for this homophone in this domain, consider text input fallback.

---

## References

- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - ASR errors
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Recognition issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real-world errors
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Common mistakes
