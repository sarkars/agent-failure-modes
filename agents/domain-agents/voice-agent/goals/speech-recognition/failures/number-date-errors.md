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

**Mitigation Strategies**
1. **Digit-by-digit mode**: Force individual digit recognition
2. **Format detection**: Identify expected format from context
3. **Confirmation**: Always confirm critical numbers
4. **Constraint validation**: Check numbers against expected format
5. **Read-back**: Agent repeats number for verification
6. **Visual fallback**: Show number on screen if available

**Detection**
- Track number-specific WER
- Monitor transaction failures from number errors
- Analyze digit confusion patterns
- Compare ASR vs. validated numbers
- Alert on high-value number errors

## References

- [McDonald's AI Drive-Thru](https://www.cnbc.com/2024/06/17/mcdonalds-to-end-ibm-ai-drive-thru-test.html) - Quantity errors (260 nuggets)
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Number handling
- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Digit errors
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
