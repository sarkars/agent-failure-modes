# Outcome Classification Errors

## Issue: Call Outcomes Incorrectly Classified, Affecting Follow-up Actions

**Frequency**: Common

**Symptoms**
- "Qualified" marked without full qualification criteria
- "Not Interested" when caller was actually busy
- "Callback" without captured callback time
- Intent routing to wrong end-node
- Follow-up actions don't match actual outcome
- Data captured but outcome contradicts it

**Root Cause**
Voice agents must classify call outcomes for downstream processing—CRM updates, follow-up queues, analytics. When classification is based on incomplete signals, misinterpreted intents, or premature judgments, the outcome label doesn't match reality. This causes wrong follow-ups, wasted effort, and data integrity issues.

**Example**
```
Scenario 1: Premature qualification

Captured:
- Interest: "Yeah sounds interesting"
- WhatsApp permission: NOT captured (call ended early)

Classified as: "Qualified"
Correct: "Interested but incomplete"

← Missing required field (WhatsApp permission)
← Follow-up will attempt WhatsApp without permission

---

Scenario 2: Busy vs Not Interested confusion

Caller: "Can't talk now, maybe later"
Classified as: "Not Interested"
Correct: "Callback"

← "Maybe later" signals callback, not rejection
← Lost opportunity due to misclassification

---

Scenario 3: Callback without time

Caller: "Call me back"
Agent: "Sure!" [ends call]

Classified as: "Callback"
Callback time: [blank]

← Callback classified but no time captured
← When should system call back?

---

Scenario 4: DNC vs Not Interested

Caller: "No thanks, not for me"
Classified as: "Do Not Contact"
Correct: "Not Interested"

← Caller declined offer, didn't request no-contact
← May have been interested in future offers

---

Scenario 5: Data/outcome mismatch

Captured:
- permission_to_send_playbook: "yes"
- whatsapp_number: "same_number"
- qualification_status: "not_interested"

← Data says qualified
← Status says not interested
← Contradiction will cause confusion

---

Classification analysis (500 calls):
  Correct classification: 362 (72%)
  
  Errors by type:
    Premature qualification: 45 (9%)
    Busy → Not Interested: 38 (8%)
    Missing callback time: 28 (6%)
    DNC over-classification: 15 (3%)
    Data/outcome mismatch: 12 (2%)
```

**Key Statistics**
From Voice Outcome Classification Research (2026):
- Classification accuracy: 65-80%
- Premature qualification: 8-15%
- Intent boundary errors: 10-18%
- Missing required fields on close: 5-12%
- Data-outcome contradictions: 3-8%
- Follow-up waste from misclassification: 15-25%

**Classification Error Types**
| Error | Cause | Impact |
|-------|-------|--------|
| Premature | Closed before completion | Incomplete follow-up |
| Intent confusion | Similar intents misread | Wrong queue |
| Missing fields | Outcome without data | Can't execute follow-up |
| Over-escalation | Soft decline → DNC | Lost opportunity |
| Contradiction | Data says X, outcome says Y | System confusion |

**Contributing Factors**
- No pre-close validation
- Intent boundaries overlap
- Outcome assigned on first signal
- Missing required field checks
- No data-outcome consistency check
- Classification done by same LLM as conversation

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Complete qualification | All fields captured | "Qualified" | Other status |
| Missing WhatsApp | Interest but no permission | "Incomplete" | "Qualified" |
| Busy signal | "Call me later" | "Callback" | "Not Interested" |
| Soft decline | "Not for me" | "Not Interested" | "DNC" |
| Callback no time | "Call back" + no time | Prompt for time | Close anyway |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Classification accuracy | > 90% | Manual audit |
| Premature close rate | < 5% | Missing required fields |
| Intent boundary errors | < 5% | Adjacent misclassification |
| Data-outcome consistency | > 98% | Field vs status match |

---

## Mitigation Strategies

### Prevention
1. **Pre-close validation**: Check required fields before routing
2. **Clear intent boundaries**: Explicit distinction between similar intents
3. **Data-driven classification**: Derive outcome from captured data
4. **No premature routing**: Complete all steps first
5. **Consistency checks**: Validate data matches outcome
6. **Multi-signal classification**: Don't route on first signal

### Implementation
```python
class OutcomeClassifier:
    """Classify call outcomes with validation"""
    
    OUTCOME_REQUIREMENTS = {
        "qualified": {
            "required_fields": ["permission_to_send_playbook", 
                               "whatsapp_number"],
            "field_values": {
                "permission_to_send_playbook": ["yes"],
                "whatsapp_number": lambda x: x and x != ""
            }
        },
        "callback": {
            "required_fields": ["callback_time"],
            "field_values": {
                "callback_time": lambda x: x and x != ""
            }
        },
        "not_interested": {
            "required_fields": [],
            "must_not_have": ["do_not_contact"]  # DNC is different
        },
        "do_not_contact": {
            "required_fields": ["do_not_contact"],
            "field_values": {
                "do_not_contact": ["Y", "yes", True]
            }
        }
    }
    
    def validate_outcome(self, proposed_outcome: str, 
                         captured_data: dict) -> dict:
        """Validate proposed outcome against captured data"""
        requirements = self.OUTCOME_REQUIREMENTS.get(proposed_outcome)
        if not requirements:
            return {"valid": False, "error": "Unknown outcome"}
        
        issues = []
        
        # Check required fields
        for field in requirements.get("required_fields", []):
            if field not in captured_data or not captured_data[field]:
                issues.append({
                    "type": "missing_required",
                    "field": field,
                    "message": f"'{proposed_outcome}' requires '{field}'"
                })
        
        # Check field values
        for field, validator in requirements.get("field_values", {}).items():
            value = captured_data.get(field)
            if callable(validator):
                if not validator(value):
                    issues.append({
                        "type": "invalid_value",
                        "field": field,
                        "value": value
                    })
            elif value not in validator:
                issues.append({
                    "type": "invalid_value",
                    "field": field,
                    "value": value,
                    "expected": validator
                })
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "proposed": proposed_outcome
        }
    
    def derive_outcome(self, captured_data: dict) -> str:
        """Derive outcome from captured data"""
        # Check in priority order
        
        # DNC takes priority
        if captured_data.get("do_not_contact") in ["Y", "yes", True]:
            return "do_not_contact"
        
        # Check for qualification
        has_permission = captured_data.get(
            "permission_to_send_playbook") == "yes"
        has_number = bool(captured_data.get("whatsapp_number"))
        
        if has_permission and has_number:
            return "qualified"
        
        # Check for callback
        if captured_data.get("callback_time"):
            return "callback"
        
        # Check for interest without completion
        interest = captured_data.get("interest_expressed")
        if interest and not has_permission:
            return "interested_incomplete"
        
        # Default to not interested
        return "not_interested"
    
    def check_consistency(self, outcome: str, 
                          captured_data: dict) -> list:
        """Check for data-outcome contradictions"""
        contradictions = []
        
        # Qualified but missing permission
        if outcome == "qualified":
            if captured_data.get("permission_to_send_playbook") != "yes":
                contradictions.append(
                    "Qualified but permission not 'yes'"
                )
        
        # Not interested but has permission
        if outcome == "not_interested":
            if captured_data.get("permission_to_send_playbook") == "yes":
                contradictions.append(
                    "Not interested but permission is 'yes'"
                )
        
        # Callback but no time
        if outcome == "callback":
            if not captured_data.get("callback_time"):
                contradictions.append(
                    "Callback but no callback_time captured"
                )
        
        return contradictions


class PreCloseValidator:
    """Validate before routing to close"""
    
    def __init__(self):
        self.classifier = OutcomeClassifier()
    
    def can_close(self, target_outcome: str, 
                  captured_data: dict) -> dict:
        """Check if we can close with target outcome"""
        validation = self.classifier.validate_outcome(
            target_outcome, captured_data
        )
        
        if not validation["valid"]:
            # Determine what's missing
            missing = [i["field"] for i in validation["issues"]
                      if i["type"] == "missing_required"]
            
            return {
                "can_close": False,
                "missing_fields": missing,
                "suggested_action": f"Capture: {', '.join(missing)}",
                "alternative_outcome": self.get_alternative(
                    target_outcome, captured_data
                )
            }
        
        # Check consistency
        contradictions = self.classifier.check_consistency(
            target_outcome, captured_data
        )
        
        if contradictions:
            return {
                "can_close": False,
                "contradictions": contradictions,
                "suggested_outcome": self.classifier.derive_outcome(
                    captured_data
                )
            }
        
        return {"can_close": True, "outcome": target_outcome}
```

### Prompt Design
```yaml
instructions: |
  ## OUTCOME CLASSIFICATION RULES
  
  QUALIFIED requires ALL of:
  - Interest expressed (yes or open)
  - WhatsApp permission: "yes"
  - WhatsApp number: confirmed (same or different)
  
  CALLBACK requires:
  - Caller said busy/call later
  - Callback time captured (evening/weekend/specific)
  
  NOT INTERESTED:
  - Caller declined the offer
  - Did NOT request no-contact
  
  DO NOT CONTACT:
  - Caller explicitly said "don't call", "remove me", 
    "no WhatsApp", "don't contact"
  
  BEFORE routing to close, check:
  1. Do I have all required fields for this outcome?
  2. Does my data match the outcome I'm routing to?
  3. If "Qualified"—do I have permission AND number?
  4. If "Callback"—do I have the callback time?
  
  COMMON ERRORS to avoid:
  - "Qualified" without WhatsApp permission
  - "Not Interested" when caller just said "busy"
  - "Callback" without capturing when
  - "DNC" for simple "no thanks"
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `outcome.accuracy` | < 85% |
| `outcome.premature_close` | > 8% |
| `outcome.missing_fields` | > 5% |
| `outcome.contradictions` | > 3% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Classification Accuracy Drop | < 80% | P2 |
| Premature Qualification | > 10% | P1 |
| Data-Outcome Mismatch | > 5% | P2 |
| Callback No Time | > 10% | P3 |

---

## References

- [Intent Classification](https://arxiv.org/abs/2101.08091) - Outcome boundaries
- [Dialog State Tracking](https://arxiv.org/abs/2009.07261) - Classification methods
- [Voice Agent Analytics](https://www.beconversive.com/blog/voice-ai-challenges) - Outcome accuracy
- [CRM Integration](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Data consistency
