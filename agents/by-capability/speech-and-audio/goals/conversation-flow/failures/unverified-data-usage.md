# Unverified Data Usage

## Issue: Agent Uses Caller-Provided Information Without Verification

**Frequency**: Common

**Symptoms**
- Agent uses caller's name without confirmation
- Assumed identity from greeting ("Hi John" when caller said "This is John")
- Phone number from caller ID used as fact
- Previous conversation data applied to wrong person
- Third-party information treated as verified

**Root Cause**
Voice agents often receive contextual data (caller ID, CRM records, previous interactions) and hear caller-provided information (name, role, preferences). Without explicit verification, agents may use this data incorrectly—addressing someone by an unverified name, assuming the person who answered is the intended recipient, or applying stale CRM data to a new context.

**Example**
```
Scenario 1: Name usage without verification

Caller: "Hello, this is Rahul"
Agent: "Hi Rahul! Thanks for filling the ambassador form..."

Problem: 
- Caller might be answering someone else's phone
- Name might be misheard ("Rahul" vs "Raghul" vs "Rajul")
- Using unverified name creates false familiarity

---

Scenario 2: Caller ID assumption

Outbound call to: +91-98765-43210
CRM shows: "Priya Sharma, Delhi University"

Someone answers: "Hello?"
Agent: "Hi Priya! This is about the form you filled..."

Actual: Priya's roommate answered the phone
Result: Confusion, privacy concern

---

Scenario 3: Third-party information

Caller: "My friend Amit told me about this program"
Agent: "Great! Amit mentioned you'd be perfect for this."

Problem: Agent has no information about what Amit said
Agent fabricated a claim about third party

---

Scenario 4: Stale CRM data

CRM: "Last interaction: Declined offer in January"
Agent: "I see you weren't interested before, but..."

Actual: Different person now using this number
Result: Offensive assumption

---

Scenario 5: Misheard name persistence

Turn 1 - Caller: "This is Saurabh" 
        (Agent heard: "Sourav")
Turn 3 - Agent: "So Sourav, which college are you at?"
Turn 4 - Caller: "It's Saurabh, not Sourav"
Turn 6 - Agent: "Got it Sourav, I'll note that down"

← Wrong name persisted despite correction

---

Unverified data analysis (500 calls):
  Caller provided name: 234
  Agent used unverified name: 89 (38%)
  Name was incorrect: 12 (13% of used)
  
  Wrong person answered: 23 (4.6% of calls)
  Agent assumed correct person: 19 (83% of wrong)
  
  Privacy concern raised: 8 calls
```

**Key Statistics**
From Voice Agent Identity Research (2026):
- Unverified name usage: 30-50%
- Wrong person answered rate: 3-8%
- Misheard name rate: 10-20%
- Name correction ignored: 5-15%
- Privacy complaints from misidentification: 2-5%

**Unverified Data Types**
| Data Source | Risk | Impact |
|-------------|------|--------|
| Caller-stated name | Mishearing, wrong person | False familiarity |
| Caller ID | Shared phone, wrong person | Privacy breach |
| CRM records | Stale data, wrong context | Offensive assumptions |
| Third-party mentions | No verification possible | Fabrication |
| Previous call data | Context mismatch | Confusion |

**Contributing Factors**
- Design assumes caller ID = person
- Names used for rapport without verification
- CRM auto-populated into prompts
- No "wrong person" detection flow
- ASR errors on names not corrected
- Over-personalization pressure

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Name stated | "This is Rahul" | Don't use name | "Hi Rahul" |
| Wrong person | "She's not here" | Handle gracefully | Continue as if right person |
| Name correction | "It's Priya, not Priti" | Use "Priya" | Continue with "Priti" |
| Third party | "My friend mentioned..." | Don't claim knowledge | "Yes, they told us..." |
| No name | Caller doesn't state name | Don't assume | Use CRM name |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Unverified name usage | 0% | Name used without confirmation |
| Wrong person handling | > 95% | Correct detection and routing |
| Name correction acceptance | > 98% | Corrected name used after |
| Third-party fabrication | 0% | Claims about third parties |

---

## Mitigation Strategies

### Prevention
1. **Never use unverified names**: Treat caller-stated names as unverified
2. **Identity confirmation**: Ask "Is this [name]?" if critical
3. **Graceful anonymity**: Design conversations that work without names
4. **Wrong-person flow**: Explicit handling when someone else answers
5. **CRM data as hints**: Use for routing, not addressing
6. **Name correction tracking**: Update immediately when corrected

### Implementation
```python
class IdentityManager:
    """Manage caller identity with verification levels"""
    
    VERIFICATION_LEVELS = {
        "unverified": 0,    # Caller stated, not confirmed
        "caller_id": 1,     # From phone number
        "crm_match": 2,     # CRM + caller ID match
        "confirmed": 3,     # Explicitly verified
    }
    
    def __init__(self):
        self.caller_name = None
        self.verification_level = "unverified"
        self.name_corrections = []
    
    def process_caller_statement(self, transcript: str) -> dict:
        """Extract but don't trust caller-stated identity"""
        # Detect name statements
        name_patterns = [
            r"this is (\w+)",
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"(\w+) speaking",
            r"(\w+) here"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, transcript, re.IGNORECASE)
            if match:
                stated_name = match.group(1)
                return {
                    "name_detected": True,
                    "stated_name": stated_name,
                    "verification": "unverified",
                    "should_use": False  # Don't use without verification
                }
        
        return {"name_detected": False}
    
    def handle_name_correction(self, transcript: str) -> dict:
        """Detect and apply name corrections"""
        correction_patterns = [
            r"it's (\w+),? not",
            r"actually,? (\w+)",
            r"my name is (\w+)",  # Re-statement = correction
            r"call me (\w+)"
        ]
        
        for pattern in correction_patterns:
            match = re.search(pattern, transcript, re.IGNORECASE)
            if match:
                corrected_name = match.group(1)
                self.name_corrections.append({
                    "old": self.caller_name,
                    "new": corrected_name,
                    "turn": "current"
                })
                self.caller_name = corrected_name
                return {
                    "correction_detected": True,
                    "corrected_to": corrected_name
                }
        
        return {"correction_detected": False}
    
    def detect_wrong_person(self, transcript: str) -> bool:
        """Detect if someone else answered"""
        wrong_person_signals = [
            "not here",
            "not available", 
            "wrong number",
            "who is this for",
            "she's not",
            "he's not",
            "they're not",
            "can I take a message",
            "woh nahi hai",
            "unke paas nahi"
        ]
        
        transcript_lower = transcript.lower()
        return any(signal in transcript_lower 
                   for signal in wrong_person_signals)
    
    def get_safe_greeting(self) -> str:
        """Generate greeting that doesn't assume identity"""
        # Never use name even if we have it
        return "Hi, this is Riya from Zapp Chess."
    
    def can_use_name(self) -> bool:
        """Check if name is safe to use"""
        # Only use if explicitly confirmed
        return self.verification_level == "confirmed"


class ConversationDesign:
    """Design conversations that work without names"""
    
    # Bad: Uses unverified name
    BAD_OPENING = "Hi {caller_name}! Thanks for filling the form..."
    
    # Good: Works without name
    GOOD_OPENING = "Hi! This is Riya from Zapp Chess—you'd filled " \
                   "the Campus Ambassador form. Got a minute?"
    
    # Bad: References third party
    BAD_REFERENCE = "Your friend {referrer} mentioned you'd be great..."
    
    # Good: Neutral acknowledgment
    GOOD_REFERENCE = "Great that you heard about it!"
    
    @staticmethod
    def generate_safe_response(template: str, 
                               identity: IdentityManager) -> str:
        """Generate response without unverified data"""
        # Remove name placeholders if not verified
        if not identity.can_use_name():
            template = re.sub(r'\{caller_name\}', '', template)
            template = re.sub(r', \{caller_name\}', '', template)
        
        return template.strip()
```

### Prompt Instructions
```yaml
instructions: |
  ## IDENTITY RULES (CRITICAL)
  
  NEVER use the caller's name:
  - Even if they say "This is [name]"
  - Even if CRM shows their name  
  - Even if caller ID matches a record
  
  WHY: The person who answered may not be the intended recipient.
       Names may be misheard. Using unverified names creates 
       false familiarity and privacy risks.
  
  NEVER reference third parties:
  - Don't say "Your friend mentioned..."
  - Don't say "[Name] told us you'd be interested"
  - You have no verified information about third parties
  
  IF someone else answers:
  - Detect: "not here", "wrong number", "who's calling for"
  - Ask: "Is [expected person] available?"
  - If not: Apologize and close as wrong_number
  
  IF caller corrects their name:
  - You shouldn't have used it, but if referenced:
  - Acknowledge briefly and never use the name again
```

### Detection & Response

1. **Data-verification audit logging with unverified-data-usage tracking**: For each call, log: {call_id, data_source: (from_caller|from_crm|from_system), data_verified (Y/N), data_used_in_greeting (Y/N), caller_confirmed_or_corrected (Y/N), wrong_person_detected (Y/N), data_accuracy_issue: (none|partial_mismatch|complete_mismatch)}. Alert immediately if: unverified_data used in greeting, or caller corrects data, or wrong person indicated. Track monthly: % of calls with unverified-data issues, breakdown by data_source, impact (complaints filed, dissatisfaction indicators).

2. **Real-time wrong-person detection and immediate correction protocol**: During call, monitor for signals of wrong-person: (a) caller says "you have the wrong number", (b) caller says "I'm not [name used]", (c) caller corrects name/email unprompted. On any signal: immediately stop using any pre-populated data, apologize, request correct information from caller, don't use CRM data for rest of call. Log incident with severity_rating (potential privacy breach).

### Architecture Patterns

1. **Data-Verification Gate with Forced Confirmation**: Before using any CRM data in greeting, gate checks: verified=true? If false, require verification from caller before use. Alternatively, use data-neutral greeting ("Hi, is this a good time to talk?") without using pre-populated names/emails.

2. **Wrong-Person Detector with Immediate Data Disabling**: Monitors caller utterances for wrong-person signals. On detection: (a) flag data_source as unreliable, (b) disable all pre-populated data for rest of call, (c) request correct information directly from caller, (d) escalate to CRM team to investigate data quality issue.

3. **CRM-Data Freshness Monitor**: Tracks staleness of pre-populated data. On calls >6 months after data last updated, treat as UNVERIFIED and require caller confirmation before use.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Unverified-Data Usage Rate | 0% | >0% | # of calls where unverified CRM data used without caller confirmation / total calls with pre-populated data |
| Wrong-Person Detection Accuracy | >99% | <95% | # of wrong-person signals detected by agent / total wrong-person calls (audited via call review) |
| Data-Correction Acknowledgment Rate | 100% | <98% | # of caller corrections that agent acknowledged and stopped using incorrect data / total caller-initiated corrections |
| CRM-Data Accuracy Rate | >95% | <90% | # of CRM data points confirmed/not-corrected by caller / total data points used (post-call audit) |
| Privacy-Related Complaint Rate | <1% | >2% | # of complaints mentioning privacy, data accuracy, or wrong-person issues / total calls |
| Data-Freshness Compliance | >90% | <80% | # of calls with CRM data <6 months old or verified by caller / total calls using pre-populated data |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unverified Data Used in Greeting | Agent uses CRM name/email in greeting without caller confirmation (e.g., "Hi John") | MEDIUM | Flag call; if caller corrects, escalate to CRM data-quality review; may indicate data staleness or system error |
| Wrong Person Not Detected | Caller indicates wrong number/wrong person, but agent continues using pre-populated data | HIGH | Flag call as compliance violation; immediately disable CRM data for call; escalate to superviso |
| Caller-Initiated Correction Ignored | Caller corrects pre-populated data (e.g., "My name is actually Jane, not John"), but agent continues using original data | HIGH | Flag as non-responsiveness; log for agent coaching; may impact customer trust |
| Stale Data in Use | CRM data >6 months old being used without verification | MEDIUM | Escalate to CRM data-refresh team; may indicate data-sync issues; require caller verification for older data |
| Third-Party Privacy Breach | Agent references data about family members, household composition, or other third-party information without explicit caller consent | CRITICAL | Immediate escalation to legal/compliance; may violate GDPR/CCPA; assess customer impact; may require breach notification |
| Multiple Data-Accuracy Issues on Call | >1 data inaccuracy or correction in single call | MEDIUM | Flag account for CRM re-verification; may indicate identity mismatch or systematic data-quality issue |

---

## References

- [Voice Agent Privacy](https://www.beconversive.com/blog/voice-ai-challenges) - Identity concerns
- [CRM Data Quality](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Stale data issues
- [Conversational Design](https://arxiv.org/abs/2106.07837) - Identity-free patterns
- [GDPR Voice Agents](https://ico.org.uk/) - Privacy compliance
