# Confidence Miscalibration

## Issue: Model Confidence Doesn't Match Answer Reliability

**Frequency**: Very Common

**Symptoms**
- High confidence on wrong or poorly-grounded answers
- Low confidence on well-supported answers
- Uncertainty not expressed when context is ambiguous
- All answers have similar confidence regardless of support

**Root Cause**
LLMs are trained to produce fluent, confident text. They don't naturally express calibrated uncertainty based on context support.

**Example**
```
Context: "The meeting might be rescheduled to either Tuesday or 
Wednesday, pending confirmation from the VP."

Query: "When is the meeting?"

Agent: "The meeting is on Tuesday." (stated definitively)

Reality: Day is uncertain, pending confirmation

Result: User misses meeting because they assumed Tuesday
```

**Mitigation Strategies**
1. **Uncertainty prompting**: Ask model to express confidence
2. **Calibration training**: Fine-tune for calibrated confidence
3. **Evidence strength signaling**: "Strongly supported" vs. "mentioned briefly"
4. **Hedged language**: Use "may", "possibly", "according to" appropriately
5. **Confidence scoring**: Separate confidence assessment step
6. **Human-readable uncertainty**: "I'm not certain, but..."

**Detection**
- Calibration curves (confidence vs. accuracy)
- Track confidence distributions by answer correctness
- User feedback on overconfident wrong answers
- Test with deliberately uncertain contexts
