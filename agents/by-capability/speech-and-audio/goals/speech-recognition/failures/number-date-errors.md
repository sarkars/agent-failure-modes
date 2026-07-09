# Number and Date Errors

## Issue: ASR Incorrectly Transcribes Numbers, Dates, and Times

**Frequency**: Very Common

**Symptoms**
- Quantities wrong in orders
- Phone numbers have digit errors
- Dates transcribed in wrong format
- Credit card numbers corrupted
- Addresses have wrong house numbers

**Root Cause**
Numbers are critical in many voice applications but particularly error-prone. Similar-sounding digits (15/50, 13/30), format ambiguity (oh vs. zero), and context sensitivity (date vs. time vs. phone number) create multiple failure modes. A single digit error in a phone number, credit card, or order quantity causes complete transaction failure.

**Example**
```
Scenario: Phone order system

User: "My phone number is 415-555-0150"
ASR: "My phone number is 415-555-0115" ← 50→15 confusion

User: "I'd like fifteen of those"
ASR: "I'd like fifty of those" ← 3x quantity error

User: "The appointment is on March 3rd at 3pm"
ASR: "The appointment is on March 30th at 3pm" ← Date error

User: "Card number 4532-0150-8834-5513"
ASR: "Card number 4532-0115-8834-5513" ← Transaction fails

Number error analysis:
  Number-containing utterances: 5,000
  Total numbers: 12,340
  Digit errors: 847 (6.9%)
  
High-impact by type:
  Phone numbers: 8% error rate → Undeliverable calls
  Credit cards: 5% error rate → Payment failures
  Quantities: 12% error rate → Order errors
  Dates: 10% error rate → Scheduling errors
  Addresses: 7% error rate → Delivery failures
```

**Key Statistics**
From Voice Commerce Research (2026):
- Number transcription errors: 5-15%
- Digit confusion (13/30, 14/40, 15/50): 15-20%
- Phone number errors: 8-12%
- Date format errors: 10-15%
- Quantity errors cost $2.3M annually for large retailers

**Common Number Errors**
| Confusion | Sound | Error Rate |
|-----------|-------|------------|
| 15 / 50 | "fifteen" / "fifty" | 18% |
| 13 / 30 | "thirteen" / "thirty" | 15% |
| 0 / O | "zero" / "oh" | 12% |
| 4 / 4th | cardinal / ordinal | 10% |
| 100 / 110 | missing "and" | 8% |

**Contributing Factors**
- Similar phonetics between numbers
- No digit-by-digit confirmation
- Format ambiguity (date vs. phone)
- Regional pronunciation differences
- Speaking rate affects clarity
- Background noise amplifies errors

## Mitigation Strategies

### Prevention
1. **Numeric Context-Aware Decoding**: Pre-transcription, inject expected number format into ASR decoder. If context is "phone number", constrain grammar to 10-digit patterns; if "credit card", 16-digit patterns; if "quantity", single digits with range (1-99). Use context priors to boost likelihood of valid numbers. Implement format-specific acoustic models (trained on isolated digits, sequences). Use temporal context: if user recently said "shipping address", incoming digits likely house number, phone number likely follows intro phrase. Implement beam search with format constraints: prune invalid number sequences early.
2. **Digit-Specific Acoustic Modeling**: Train isolated digit recognition model (0-9) separate from full ASR. For utterances containing expected numbers, run digit model in parallel with general ASR. Use digit confidence scores to detect ambiguous digits. For high-confusion pairs (15/50, 13/30), implement specialized pair classifiers. Use formant analysis and duration features to distinguish similar digits (4/8, 9/5). Implement confidence-based mode switching: high-confidence general ASR → use as-is; low-confidence + number context → fall back to digit model.
3. **Format Validation & Correction Rules**: Post-ASR, apply format-specific validation. Phone numbers: verify checksum (if applicable), check for valid area codes. Credit cards: Luhn algorithm validation. Dates: verify valid month/day combinations, resolve ambiguous formats (3/4 = March 4th or April 3rd based on context). Implement rule-based correction: "fifty-teen" → "fifty" (likely "15" transcribed as "50-10"), "thir-ty" → "thirteen" (likely "13" as "30"). Use edit distance to identify likely transcription errors.

### Detection & Response
1. **Number-Specific WER Tracking**: Segment accuracy on numbers vs. general words. Track digit error rate (WER on individual digits). Target: Digit WER <3% (vs. general 2-5%). Break down by number type: phone (target <3%), credit card (target <2%, critical), quantities (target <5%), dates (target <5%). Alert when digit WER increases 1+ point from baseline. Monthly confusion matrix analysis: identify persistent digit-pair confusions (13/30, 15/50, etc.).
2. **Transaction Failure Correlation**: For financial transactions, analyze failures attributed to number errors. Cross-reference ASR transcription vs. database record. Measure recovery rate: how many failures would be prevented by stricter number validation. Alert if >5% of transaction failures from number transcription errors. Segment by number type: phone numbers causing lookup failures, credit cards causing payment rejections, quantities causing order errors.
3. **Confirmation Effectiveness Measurement**: When system confirms numbers (read-back), track whether user accepts confirmation despite error (false acceptance). Target: <2% false acceptance rate. If user corrects >20% of confirmations, number transcription quality unacceptable, trigger investigation. Measure latency cost of confirmations to ensure acceptable UX.

### Architecture Patterns
1. **Dual-Model Digit Confidence Fusion**: Run general ASR + specialized digit model for sequences with expected numbers. For each digit position, compare confidence scores. If both models agree with high confidence (>0.85), use that digit. If models disagree or both low confidence, flag for confirmation. Implement weighted confidence: general ASR weight 0.6 + digit model weight 0.4. Use maximum confidence approach: use whichever model produces higher-confidence result.
2. **Format-Constrained Grammar Decoding**: Define formal grammars for each number type (phone: [area][exchange][line], credit: [4x4-digit-groups], etc.). Compile grammar into ASR decode graph. During decoding, constrain search space to valid number sequences only. Implement cascading grammars: universal digit grammar initially, then narrow to specific format when context clear. Use grammar weights to prefer well-formed numbers over malformed.
3. **Multi-Pass Number Verification Pipeline**: Pass 1: ASR generates hypothesis. Pass 2: Run digit model, compute confidence. Pass 3: Apply format validation rules. Pass 4: If confidence insufficient or validation fails, generate corrected hypothesis using most-likely corrections. Pass 5: If still uncertain, trigger confirmation flow. Implement fallback sequence: high-confidence auto-accept → medium confidence (70-85%) confirmation → low confidence (<70%) digit-by-digit spelling.

### Metrics
1. **digit_error_rate_percent**: Target: <3% overall; phone <2.5%, credit card <1%, quantities <4%. Measure: digit_errors / total_digits. Alert: Any category >5%.
2. **number_format_validation_success_rate**: Target: 99%+ of transcribed numbers pass format validation (correct structure, valid values). Measure: valid_numbers / total_numbers. Alert: <98%.
3. **critical_number_transaction_failure_rate**: Target: <0.5% of transactions fail due to number transcription errors. Measure: failures_from_number_errors / total_transactions. Alert: >1%.
4. **digit_pair_confusion_rate_for_high_risk_pairs**: Target: <5% error rate for pairs 15/50, 13/30, 40/14. Measure: errors_for_pair / total_occurrences_of_pair. Alert: >8% for any high-risk pair.
5. **number_confirmation_latency_ms**: Target: <2s total latency for read-back confirmation. Measure: time_to_confirm_number. Alert: >3s, impacts user experience.

### Alerts
1. **Critical Number Transcription Error** (P1): Condition - Credit card number error detected (Luhn validation fails, user reports wrong charge), OR high-value transaction error (>$1000 order quantity error). Action: Immediate alert, block transaction, contact user, verify correct information via secondary channel, update digit model.
2. **Digit Confusion Spike** (P2): Condition - Error rate for specific digit-pair (15/50, 13/30, etc.) increases 3+ points from baseline in 1-hour window. Action: Investigate ASR changes, check for acoustic degradation, consider reverting recent updates, enable confirmations for high-error pair.
3. **Number Validation Bypass** (P2): Condition - >2% of transcribed numbers fail format validation, indicating format grammar not working or confused transcription. Action: Check format grammar configuration, audit recent ASR changes, review sample errors, consider requiring all number confirmations.

---

## References

- [McDonald's AI Drive-Thru](https://www.cnbc.com/2024/06/17/mcdonalds-to-end-ibm-ai-drive-thru-test.html) - Quantity errors (260 nuggets)
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Number handling
- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Digit errors
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
