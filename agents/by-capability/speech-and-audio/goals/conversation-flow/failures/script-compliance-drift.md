# Script Compliance Drift

## Issue: Agent Deviates from Required Phrases, Boundaries, or Conversation Structure

**Frequency**: Common

**Symptoms**
- Closing phrases differ from required exact wording
- Prohibited words/phrases appear in responses
- Agent adds unsolicited information
- Promises made that shouldn't be made
- Over-explanation despite brevity instructions
- Re-pitching after clear decline

**Root Cause**
Voice agents often have strict compliance requirements: exact closing phrases, prohibited words, information boundaries, and response length limits. LLMs naturally elaborate, soften, or vary language for naturalness—directly conflicting with compliance needs. Without explicit enforcement, the model drifts toward its training patterns rather than staying within prescribed boundaries.

**Example**
```
Scenario 1: Closing phrase deviation

Required: "All good, totally understand. All the best!"
Agent said: "No problem at all, I completely understand. 
            Best of luck with everything!"

← Same sentiment, wrong words (compliance failure)

---

Scenario 2: Promise leakage

Boundary: Never say "team will send" or "you'll receive"

Agent said: "Great! The team will share the playbook 
            on WhatsApp shortly."

← Violated promise boundary

---

Scenario 3: Prohibited phrase usage

Prohibited: "quick", "just", "basically", "simply", "kindly"

Agent said: "So basically, I just wanted to quickly 
            check if you're interested..."

← Three prohibited words in one sentence

---

Scenario 4: Over-explanation

Instruction: Keep turns to 5-12 words, 45-60 seconds total

Agent said: "So this is a campus ambassador program where 
            you'd be helping us run chess tournaments at 
            your college. We provide all the creatives and 
            support, plus you'd get a certificate, trophy, 
            and there's a five hundred rupee cash prize for 
            the campus winner. The LinkedIn founder shoutout 
            is pretty cool too for top performers..."

← 60+ words in single turn, violates brevity

---

Scenario 5: Re-pitch after decline

Instruction: Never re-pitch after clear decline

Caller: "No thanks, not interested"
Agent: "I understand, but just so you know, it's really 
        low commitment and the perks are quite good..."

← Re-pitched after clear "not interested"

---

Script compliance analysis (500 calls):
  Closing phrase exact match: 45%
  Prohibited words used: 23% of calls
  Promise boundary violated: 12% of calls
  Re-pitch after decline: 8% of calls
  Turn length exceeded: 35% of calls
```

**Key Statistics**
From Voice Agent Compliance Research (2026):
- Exact phrase compliance: 40-60%
- Prohibited word usage: 15-30%
- Boundary violations: 10-20%
- Over-explanation rate: 25-40%
- Re-pitch after decline: 5-15%

**Compliance Drift Types**
| Type | Description | Impact |
|------|-------------|--------|
| Phrase deviation | Wrong words, same meaning | Legal/brand risk |
| Promise leakage | Saying what shouldn't be said | False expectations |
| Boundary violation | Adding prohibited info | Compliance failure |
| Verbosity creep | Responses too long | User fatigue |
| Re-engagement | Pitching after decline | Harassment |

**Contributing Factors**
- LLM training favors elaboration
- Natural language variation
- No post-generation compliance check
- Negative instructions hard to enforce
- Long instruction lists ignored
- Context length pushes out constraints

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Exact closing | Not Interested outcome | Exact phrase match | Any variation |
| Prohibited words | Any response | Zero prohibited words | Any prohibited word |
| Promise boundary | Qualified outcome | No "will send/share" | Promise language |
| Turn length | Any turn | < 15 words | > 25 words |
| No re-pitch | "Not interested" | Single acknowledgment | Additional pitch |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Phrase compliance | > 95% | Exact match on required phrases |
| Prohibited word rate | 0% | Count prohibited words in output |
| Promise leakage | 0% | Detect promise patterns |
| Turn length compliance | > 90% | Word count per turn |

---

## Mitigation Strategies

### Prevention
1. **Post-generation validation**: Check output before TTS
2. **Templated closings**: Use fixed templates for required phrases
3. **Prohibited word filter**: Block responses with prohibited terms
4. **Length enforcement**: Truncate or regenerate long responses
5. **Structured output**: Force specific format for compliance-critical turns
6. **Instruction prioritization**: Put compliance rules at prompt end

### Compliance Layer
```python
class ComplianceChecker:
    """Validate agent responses before delivery"""
    
    PROHIBITED_WORDS = [
        "quick", "quickly", "just", "basically", "simply",
        "kindly", "would you", "perfect", "awesome"
    ]
    
    PROMISE_PATTERNS = [
        r"team will (send|share|deliver|contact|reach)",
        r"you('ll| will) (receive|get|hear)",
        r"(sending|sharing) (it|the playbook)",
        r"(shortly|soon|today|tomorrow|in \d+ minutes)"
    ]
    
    REQUIRED_CLOSINGS = {
        "not_interested": "All good, totally understand. All the best!",
        "wrong_number": "Oh sorry, my bad!",
        "dnc": None  # Dynamic based on context
    }
    
    def __init__(self, max_turn_words=15):
        self.max_turn_words = max_turn_words
    
    def validate(self, response: str, context: dict) -> dict:
        """Validate response against compliance rules"""
        issues = []
        
        # Check prohibited words
        prohibited_found = self.check_prohibited(response)
        if prohibited_found:
            issues.append({
                "type": "prohibited_words",
                "words": prohibited_found,
                "severity": "high"
            })
        
        # Check promise patterns
        promises = self.check_promises(response)
        if promises:
            issues.append({
                "type": "promise_leakage",
                "patterns": promises,
                "severity": "critical"
            })
        
        # Check turn length
        word_count = len(response.split())
        if word_count > self.max_turn_words:
            issues.append({
                "type": "verbosity",
                "words": word_count,
                "limit": self.max_turn_words,
                "severity": "medium"
            })
        
        # Check required closing if applicable
        if context.get("is_closing"):
            closing_issue = self.check_closing(
                response, context.get("outcome")
            )
            if closing_issue:
                issues.append(closing_issue)
        
        return {
            "compliant": len(issues) == 0,
            "issues": issues,
            "response": response
        }
    
    def check_prohibited(self, text: str) -> list:
        text_lower = text.lower()
        return [w for w in self.PROHIBITED_WORDS 
                if w in text_lower]
    
    def check_promises(self, text: str) -> list:
        import re
        found = []
        for pattern in self.PROMISE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                found.append(pattern)
        return found
    
    def check_closing(self, response: str, outcome: str) -> dict:
        required = self.REQUIRED_CLOSINGS.get(outcome)
        if required and response.strip() != required:
            return {
                "type": "closing_mismatch",
                "expected": required,
                "actual": response,
                "severity": "high"
            }
        return None
    
    def fix_response(self, response: str, issues: list, 
                     context: dict) -> str:
        """Attempt to fix compliance issues"""
        fixed = response
        
        for issue in issues:
            if issue["type"] == "prohibited_words":
                # Remove prohibited words
                for word in issue["words"]:
                    fixed = re.sub(
                        rf'\b{word}\b', '', fixed, 
                        flags=re.IGNORECASE
                    )
            
            if issue["type"] == "closing_mismatch":
                # Replace with required closing
                required = self.REQUIRED_CLOSINGS.get(
                    context.get("outcome")
                )
                if required:
                    fixed = required
            
            if issue["type"] == "promise_leakage":
                # Regenerate - can't easily fix promises
                return None  # Signal regeneration needed
        
        return fixed.strip()
```

### Instruction Design
```yaml
# Put compliance rules at END of prompt (recency bias)
instructions: |
  ... [main instructions] ...
  
  ## CRITICAL COMPLIANCE RULES (ALWAYS FOLLOW)
  
  NEVER use these words: quick, just, basically, simply, kindly
  
  NEVER say:
  - "team will send/share/deliver"
  - "you'll receive/get"
  - Any promise of delivery timing
  
  ALWAYS use exact closing phrases:
  - Not Interested: "All good, totally understand. All the best!"
  - Wrong Number: "Oh sorry, my bad!"
  
  ALWAYS keep responses under 15 words.
  
  NEVER re-pitch after caller declines.
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `compliance.phrase.exact` | < 90% |
| `compliance.prohibited.rate` | > 5% |
| `compliance.promise.leakage` | > 0% |
| `compliance.verbosity.rate` | > 20% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Promise Leakage | Any occurrence | P1 |
| Phrase Deviation | < 85% compliance | P2 |
| Prohibited Words | > 10% of calls | P2 |
| Re-Pitch Detected | > 5% of declines | P2 |

---

## References

- [Controllable Text Generation](https://arxiv.org/abs/2201.05337) - Constraint enforcement
- [LLM Instruction Following](https://arxiv.org/abs/2303.18223) - Why instructions fail
- [Voice Agent Compliance](https://www.beconversive.com/blog/voice-ai-challenges) - Regulatory needs
- [AppInventiv: Voice Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Script adherence
