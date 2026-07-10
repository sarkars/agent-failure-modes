# Intent Boundary Confusion

## Issue: Similar Intents Misclassified Due to Overlapping Definitions

**Frequency**: Common

**Symptoms**
- "Not interested" treated as "Do not contact"
- "Busy now" routed to rejection instead of callback
- Hesitant responses marked as clear decline
- Soft objections escalated to hard objections
- Qualification status inconsistent across similar calls

**Root Cause**
Voice agents often have multiple intent categories with subtle semantic boundaries. Without clear, mutually exclusive intent definitions, the classifier—whether rule-based or LLM-based—confuses adjacent intents. A caller saying "I'm not sure" could be hesitant (continue pitch), not interested (stop pitch), or requesting more info (provide details). Overlapping intent instructions compound the problem.

**Example**
```
Intent definitions in system:
- Not Interested: "Caller declines or refuses the offer"
- Do Not Contact: "Caller asks for removal or no future contact"
- Callback: "Caller asks to be called later"

Scenario 1: Ambiguous decline
Caller: "I don't think this is for me right now"

Interpretation A: Not Interested (decline the offer)
Interpretation B: Callback (not right NOW = call later)
Interpretation C: Hesitant (needs more info)

Agent chose: Do Not Contact ✗ (over-escalation)
Correct: Not Interested or Hesitant

---

Scenario 2: Busy vs rejection
Caller: "No, I can't talk right now"

Agent interpreted: Not Interested ("No, I can't")
Correct: Callback (can't talk NOW = busy)

---

Scenario 3: Soft vs hard objection
Caller: "Please don't WhatsApp me"

Agent interpreted: Not Interested (declined offer)
Correct: Do Not Contact (no-contact request)

---

Intent confusion matrix (500 calls):
                    Classified As:
                    NotInt  DNC   Callback  Hesitant
Actual NotInt        78%    12%     5%       5%
Actual DNC           15%    80%     2%       3%
Actual Callback      20%     3%    72%       5%
Actual Hesitant      25%     2%     8%      65%

Cross-category errors: 22% average
Most confused: NotInterested ↔ DNC (13.5%)
```

**Key Statistics**
From Voice Agent Intent Classification (2026):
- Intent boundary confusion: 15-25%
- Adjacent intent misclassification: 10-20%
- Over-escalation rate (soft → hard): 8-15%
- Under-escalation rate (hard → soft): 5-10%
- Impact on customer satisfaction: -25% for misclassified

**Common Intent Boundary Confusions**
| Intent A | Intent B | Confusion Trigger |
|----------|----------|-------------------|
| Not Interested | Do Not Contact | "Don't" + action |
| Busy | Not Interested | "No" + temporal |
| Hesitant | Not Interested | Uncertain tone |
| Callback | Not Available | "Later" ambiguity |
| Qualified | Interested | Permission vs curiosity |

**Contributing Factors**
- Overlapping intent definitions
- Missing temporal qualifiers (now vs. ever)
- No intensity gradient (soft vs. hard decline)
- Single-label classification for multi-intent
- Tone/prosody ignored in classification
- Insufficient negative examples in training

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Temporal "no" | "No, not right now" | Callback | Not Interested |
| Soft decline | "I'm not sure about this" | Hesitant | Not Interested |
| Hard decline | "I'm not interested, don't call again" | DNC | Not Interested |
| Busy signal | "I'm in a meeting" | Callback | Unable to Continue |
| WhatsApp-specific | "Don't WhatsApp me" | DNC | Not Interested |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Intent accuracy | > 90% | Label vs. human annotation |
| Adjacent confusion | < 5% | Errors between neighboring intents |
| Over-escalation | < 3% | Soft → hard misclassification |
| Boundary F1 | > 0.85 | Precision/recall on boundary cases |

---

## Mitigation Strategies

### Prevention
1. **Mutually exclusive definitions**: Ensure intents don't overlap semantically
2. **Hierarchical classification**: First classify category, then sub-intent
3. **Temporal markers**: Explicitly check for "now", "later", "ever" qualifiers
4. **Intensity gradient**: Separate soft/hard variants of each intent
5. **Multi-turn context**: Use conversation history, not just last turn
6. **Confidence thresholds**: Route low-confidence to clarification

### Intent Hierarchy
```python
class IntentClassifier:
    """Hierarchical intent classification with boundary handling"""
    
    INTENT_HIERARCHY = {
        "negative": {
            "hard": ["do_not_contact", "wrong_number"],
            "soft": ["not_interested", "hesitant"],
            "temporal": ["busy", "callback"]
        },
        "positive": {
            "confirmed": ["qualified"],
            "partial": ["interested", "curious"]
        },
        "neutral": {
            "unable": ["unable_to_continue", "voicemail"]
        }
    }
    
    TEMPORAL_MARKERS = ["now", "right now", "at the moment", 
                        "currently", "abhi", "filhaal"]
    HARD_MARKERS = ["don't call", "don't contact", "remove", 
                    "stop calling", "mat karo"]
    
    def classify(self, transcript: str, context: list) -> dict:
        # First: check for hard markers (highest priority)
        if self.has_hard_markers(transcript):
            return {"intent": "do_not_contact", "confidence": 0.95}
        
        # Second: check temporal qualifiers
        has_temporal = self.has_temporal_markers(transcript)
        
        # Third: classify with context
        base_intent = self.llm_classify(transcript, context)
        
        # Adjust based on temporal
        if has_temporal and base_intent == "not_interested":
            return {"intent": "callback", "confidence": 0.8,
                    "note": "temporal_override"}
        
        return base_intent
    
    def has_hard_markers(self, text: str) -> bool:
        text_lower = text.lower()
        return any(marker in text_lower for marker in self.HARD_MARKERS)
    
    def has_temporal_markers(self, text: str) -> bool:
        text_lower = text.lower()
        return any(marker in text_lower for marker in self.TEMPORAL_MARKERS)
    
    def get_clarification_prompt(self, ambiguous_intent: str) -> str:
        """Generate clarification question for ambiguous cases"""
        clarifications = {
            "not_interested_or_callback": 
                "Just to confirm—would you prefer I call back later, "
                "or is this not something you're interested in?",
            "not_interested_or_dnc":
                "Got it. Should I also make sure we don't reach out again?"
        }
        return clarifications.get(ambiguous_intent, "")
```

### Intent Definitions Best Practice
```yaml
intents:
  do_not_contact:
    definition: "Caller explicitly requests removal from contact lists 
                 OR refuses any future WhatsApp/call follow-up"
    triggers:
      - "don't call me"
      - "remove my number"
      - "don't WhatsApp me"
      - "stop contacting"
    NOT: "Simple decline of current offer without contact restriction"
    
  not_interested:
    definition: "Caller declines the current offer but does NOT 
                 request removal from future contact"
    triggers:
      - "not interested"
      - "not for me"
      - "don't want this"
    NOT: "Busy/unavailable OR requesting no future contact"
    
  callback:
    definition: "Caller indicates they ARE interested but cannot 
                 talk NOW, with temporal qualifier"
    triggers:
      - "call me later"
      - "busy right now"
      - "in a meeting"
      - "not now"
    REQUIRES: Temporal qualifier (now, currently, right now)
```

### Detection & Response

1. **Intent-classification audit logging with boundary-accuracy tracking**: For each call, log: {call_id, detected_intent (enum: soft_no|hard_no|interested|interested_but_later|not_qualified), intent_confidence_score (0-1.0), boundary_classification_correct (Y/N), escalation_triggered (Y/N), escalation_type (if yes: soft_to_hard|interested_to_action|unqualified_push), caller_satisfaction_indicator}. Daily audit: sample 10% of calls, manually verify intent classification against actual caller intent. Alert if: intent_accuracy <85%, or soft_to_hard escalation rate >5%, or hard_no misclassification rate >2%.

2. **Escalation-compliance monitoring with temporal-qualifier validation**: Track every escalation: when escalation happened, what temporal qualifier was present (if any). Verify: was temporal qualifier present before escalation? If no temporal qualifier, was escalation still triggered? Alert if agent escalates without temporal qualifier presence (potential over-escalation). Monthly report: "Escalations by intent type", "Over-escalations (missing temporal qualifier)", "Misclassifications (soft_no treated as interested)".

### Architecture Patterns

1. **Intent Classifier with Boundary Enforcement**: On caller response, classifier analyzes: (a) explicit keywords ("stop", "no", "interested"), (b) temporal qualifiers ("right now", "later", "eventually"), (c) intent score and confidence threshold. Maps to intent_enum: soft_no → callback eligible; hard_no → do not contact; interested → pitch; interested_but_later → callback; not_qualified → soft exit. Boundaries enforced: if soft_no detected, NO escalation unless temporal_qualifier present.

2. **Escalation Gate with Temporal-Qualifier Validation**: Before agent escalates from soft_no to hard_no or push, check: temporal_qualifier present? If absent, block escalation. If present, proceed with qualified escalation. All escalations logged with temporal_qualifier reference.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Intent Classification Accuracy | >95% | <85% | # of correctly classified intents / total intents (audited manual check) |
| Soft-No to Callback Rate | >80% | <70% | # of soft_no calls that receive callback preference capture / total soft_no calls |
| Hard-No Respect Rate | 99%+ | <98% | # of hard_no calls where agent terminates without push / total hard_no calls |
| Over-Escalation Rate | <2% | >5% | # of escalations from soft_no to hard_no without temporal qualifier / total escalations |
| DNC Misclassification Rate | <1% | >2% | # of hard_no/DNC calls misclassified as interested (audited via post-call complaints) / total hard_no calls |
| Intent Confidence Threshold Accuracy | >90% | <80% | # of low-confidence classifications correctly escalated for human review / total low-confidence intents |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Soft-No Misclassified | Caller's soft-no ("not right now") classified as hard-no (DNC) without temporal qualifier present | CRITICAL | Flag call for correction; update DNC classification; may require callback to correct customer expectation |
| Over-Escalation Detected | Agent escalates from soft_no to hard_no push without temporal qualifier ("right now", "currently") present | HIGH | Flag as boundary violation; escalate to agent coaching; audit similar calls from same agent |
| Hard-No Disrespected | Agent continues pitching after caller clearly indicated hard-no (DNC intent) | CRITICAL | Flag compliance violation; may impact compliance/legal risk if repeated; escalate to supervisor |
| Intent Confidence Below Threshold | Classifier confidence on intent <70%; escalate for human review before proceeding | MEDIUM | Route to human agent or escalation team; do not proceed with automated action until verified |
| Temporal-Qualifier Requirement Missed | Agent should have awaited temporal qualifier before escalating; proceeded without | MEDIUM | Investigate whether temporal-qualifier detection is functioning; may require NLP model update |

---

## References

- [Intent Classification Survey](https://arxiv.org/abs/2101.08091) - Multi-intent challenges
- [Dialog State Tracking](https://arxiv.org/abs/2009.07261) - Boundary handling
- [Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Classification issues
- [Conversational AI Research](https://www.beconversive.com/blog/voice-ai-challenges) - Intent design
