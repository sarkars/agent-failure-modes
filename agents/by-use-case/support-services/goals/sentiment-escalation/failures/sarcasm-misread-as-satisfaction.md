# Sarcasm Misread as Satisfaction

## Issue: Sentiment-Escalation Agent Classifies Sarcastic or Passive-Aggressive Customer Messages as Positive, Suppressing an Escalation That Should Have Triggered

**Frequency**: Occasional

**Symptoms**
- Messages like "Oh great, another delay, just what I needed" are scored as positive sentiment due to the word "great," and the escalation path is not triggered
- Customers expressing frustration through understatement ("fine, I guess we'll just wait forever") are scored as neutral rather than negative
- Escalation-eligible keywords list catches explicit negative words ("angry," "furious," "cancel") but misses sarcastic positive-phrased frustration entirely
- Customers who were sentiment-misclassified and not escalated show disproportionately high churn or complaint-to-management rates afterward
- Sentiment model accuracy on direct negative statements is high while accuracy on sarcastic/indirect negative statements is measurably lower in QA sampling

**Root Cause**
Sentiment classifiers, including LLM-based ones, are trained predominantly on direct sentiment expression and tend to weight individual emotionally-charged words heavily. Sarcasm and passive-aggressive phrasing intentionally invert the literal polarity of the words used, which defeats lexical and even many embedding-based sentiment signals unless the model is specifically tuned to detect tonal incongruity (positive words + negative context, exclamation patterns, etc.). Escalation logic gated on a sentiment score threshold then inherits this blind spot directly — a sarcastic message scoring "positive" never reaches the escalation gate at all.

**Example**
```
Customer message: "Wow, three reschedules in a row. Really feeling the love here."
Lexical signal: "love," "wow" -> scored positive sentiment, 0.78 confidence
Actual intent: Sharp frustration after repeated service failures
Escalation gate: Requires sentiment score below negative threshold -> not triggered
Customer: Receives standard non-escalated response, cancels service within the week
Impact: A clear escalation signal was present in the message but invisible to the lexical/embedding-only model
```

**Key Statistics**
- Sarcasm and irony detection remains a well-documented hard subproblem in sentiment analysis, with accuracy gaps of 15-30+ percentage points relative to direct-sentiment accuracy reported across NLP sarcasm-detection benchmarks
- Customers who express frustration indirectly (sarcasm, understatement) and are not escalated show measurably higher silent-churn rates than customers whose frustration is escalated, in customer success analyses correlating sentiment handling with retention
- QA-sampled review of "positive-scored" tickets that were later escalated by a human typically reveals a non-trivial fraction were sarcastic or tonally incongruent

---

## Mitigation Strategies

1. **Tonal Incongruity Detection**: Add a secondary check for incongruity between positive lexical content and negative contextual signals (repeated complaints in history, exclamation patterns, short curt phrasing) rather than relying on lexical polarity alone
2. **Escalation History Weighting**: Weight escalation decisions partly on recent interaction history (number of prior contacts about the same issue) independent of the current message's sentiment score, since repeated contact itself is an escalation signal
3. **Human Spot-Check on Borderline Positive**: Route a sample of "positive" classifications following 2+ prior contacts on the same issue to human QA review to catch sarcasm misses
4. **Escalation Threshold Recalibration**: Periodically recalibrate sentiment thresholds using QA-confirmed sarcasm cases as adversarial test examples

### Metrics
- Sentiment model accuracy on a held-out sarcasm/indirect-negative test set, tracked separately from direct-sentiment accuracy
- Rate of "positive" or "neutral" classified tickets that are followed by a complaint, cancellation, or churn event
- Escalation rate for repeat-contact customers vs. first-contact customers

### Alerts
- A ticket classified positive/neutral is followed by a cancellation or formal complaint within a defined window → P2
- Sarcasm-test-set accuracy drops below a defined threshold after a model update → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Complexity Prediction in Support](https://arxiv.org/abs/2008.02455)
