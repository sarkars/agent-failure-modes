# Response Adaptation Failure

## Issue: Agent Continues Planned Flow Instead of Adapting to Caller's Response

**Frequency**: Very Common

**Symptoms**
- Agent ignores what caller just said
- Pre-planned next question asked regardless of answer
- Caller's concern acknowledged but not addressed
- Conversation feels like parallel monologues
- Agent misses signals that require path change
- "That's not what I asked" from caller

**Root Cause**
Voice agents often follow scripted flows with predetermined next steps. When the caller's response requires a different path—a question, objection, tangent, or unexpected answer—the agent continues its plan instead of adapting. This happens because the agent prioritizes flow completion over responsive conversation.

**Example**
```
Scenario 1: Question ignored

Agent: "So we're looking for campus ambassadors. Interested?"
Caller: "Wait, what exactly would I have to do?"
Agent: "Great! Which college are you at?"

← Caller asked a question, agent moved to next script step
← Should have answered the "what do I do" question first

---

Scenario 2: Concern not addressed

Agent: "Can I share the playbook on WhatsApp?"
Caller: "I'm worried this will spam me with messages"
Agent: "So is this same number okay for WhatsApp?"

← Caller expressed concern about spam
← Agent continued to next step without addressing

---

Scenario 3: Tangent steamrolled

Agent: "The perks include certificate, trophy—"
Caller: "Oh, I actually participated in your tournament 
        last month!"
Agent: "—and a T-shirt. So sounds interesting?"

← Caller shared relevant context
← Agent completed sentence and continued script

---

Scenario 4: Unexpected answer ignored

Agent: "Which college are you at?"
Caller: "I graduated last year"
Agent: "And can I send the playbook to your WhatsApp?"

← Answer indicated they may not be eligible
← Agent didn't acknowledge the graduation context

---

Scenario 5: Conditional agreement missed

Caller: "Yeah maybe, but only if it doesn't take much time"
Agent: "Perfect! So which college?"

← Caller had a condition ("not much time")
← Agent treated as unconditional yes

---

Adaptation analysis (500 calls):
  Responses requiring adaptation: 312
  Correctly adapted: 187 (60%)
  Ignored and continued: 94 (30%)
  Partially acknowledged: 31 (10%)
  
  Adaptation triggers missed:
    Direct questions: 25%
    Expressed concerns: 28%
    Conditional answers: 22%
    Relevant context shared: 15%
    Objections: 10%
```

**Key Statistics**
From Voice Agent Adaptation Research (2026):
- Responses requiring flow change: 40-60%
- Correct adaptation rate: 50-70%
- User frustration from ignored response: 45%
- "Not listening" complaints: 25-35%
- Adaptation → completion correlation: +30%

**Adaptation Failure Types**
| Trigger | Agent Behavior | Impact |
|---------|----------------|--------|
| Question asked | Continues to next step | Frustration |
| Concern raised | Acknowledges, doesn't address | Distrust |
| Condition stated | Treats as unconditional | Misalignment |
| Context shared | Ignores relevance | Impersonal |
| Objection raised | Continues pitch | Pushiness |

**Contributing Factors**
- Rigid flow state machine
- Turn-by-turn prompting without context
- No response classification layer
- Script prioritized over responsiveness
- Missing conditional branch logic
- LLM not instructed to check for triggers

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Direct question | "What would I do?" | Answer question | Next script step |
| Concern | "Will this spam me?" | Address concern | Continue flow |
| Condition | "Only if it's easy" | Acknowledge condition | "Perfect!" |
| Context | "I already know about this" | Adjust pitch | Full pitch anyway |
| Objection | "I don't have time" | Handle objection | Continue pitch |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Adaptation rate | > 85% | Triggers met with relevant response |
| Question answering | > 90% | Questions addressed before continuing |
| Concern addressing | > 80% | Concerns acknowledged AND addressed |
| Condition acknowledgment | > 90% | Conditions noted in response |

---

## Mitigation Strategies

### Prevention
1. **Response classification**: Detect triggers before generating response
2. **Interrupt flow**: Questions/concerns override planned next step
3. **Context injection**: Include caller's last response in prompt
4. **Conditional branching**: Handle "yes but..." differently from "yes"
5. **Acknowledgment first**: Address what they said before continuing
6. **Relevance check**: Ask "Does my planned response fit what they said?"

### Implementation
```python
class ResponseAdapter:
    """Adapt conversation flow based on caller response"""
    
    QUESTION_MARKERS = [
        "what", "how", "why", "when", "where", "who",
        "can you", "could you", "will", "would",
        "kya", "kaise", "kyun", "kab"
    ]
    
    CONCERN_MARKERS = [
        "worried", "concerned", "afraid", "spam",
        "too many", "bother", "annoy", "privacy",
        "safe", "secure", "trust"
    ]
    
    CONDITION_MARKERS = [
        "only if", "but only", "as long as", "if",
        "depends", "maybe if", "unless"
    ]
    
    OBJECTION_MARKERS = [
        "don't have time", "too busy", "not sure",
        "sounds like a lot", "complicated"
    ]
    
    def classify_response(self, transcript: str) -> dict:
        """Classify what type of response adaptation is needed"""
        transcript_lower = transcript.lower()
        
        # Check for questions (highest priority)
        if any(m in transcript_lower for m in self.QUESTION_MARKERS):
            if "?" in transcript or self.is_question_structure(transcript):
                return {
                    "type": "question",
                    "action": "answer_first",
                    "can_continue_after": True
                }
        
        # Check for concerns
        if any(m in transcript_lower for m in self.CONCERN_MARKERS):
            return {
                "type": "concern",
                "action": "address_concern",
                "can_continue_after": True
            }
        
        # Check for conditions
        if any(m in transcript_lower for m in self.CONDITION_MARKERS):
            return {
                "type": "conditional",
                "action": "acknowledge_condition",
                "can_continue_after": True
            }
        
        # Check for objections
        if any(m in transcript_lower for m in self.OBJECTION_MARKERS):
            return {
                "type": "objection",
                "action": "handle_objection",
                "can_continue_after": False
            }
        
        return {"type": "standard", "action": "continue_flow"}
    
    def generate_adapted_response(self, classification: dict,
                                   caller_input: str,
                                   planned_response: str) -> str:
        """Generate response that addresses caller before continuing"""
        
        action = classification["action"]
        
        if action == "answer_first":
            # Extract and answer the question, then continue
            answer = self.generate_answer(caller_input)
            if classification["can_continue_after"]:
                return f"{answer} {planned_response}"
            return answer
        
        if action == "address_concern":
            # Acknowledge concern, provide reassurance, then continue
            reassurance = self.generate_reassurance(caller_input)
            return f"{reassurance} {planned_response}"
        
        if action == "acknowledge_condition":
            # Note the condition, then continue
            acknowledgment = self.acknowledge_condition(caller_input)
            return f"{acknowledgment} {planned_response}"
        
        if action == "handle_objection":
            # Handle objection - may change flow entirely
            return self.handle_objection(caller_input)
        
        return planned_response


class AdaptiveFlowManager:
    """Manage conversation flow with adaptation"""
    
    def __init__(self):
        self.adapter = ResponseAdapter()
        self.current_step = "opening"
        self.pending_question = None
    
    def process_turn(self, caller_input: str) -> dict:
        # First: classify what the caller said
        classification = self.adapter.classify_response(caller_input)
        
        # If they asked a question, answer it first
        if classification["type"] == "question":
            self.pending_question = caller_input
            return {
                "response_type": "answer_question",
                "then_continue": self.current_step,
                "instruction": f"Answer their question: '{caller_input}' "
                              f"Then continue with {self.current_step}"
            }
        
        # If they raised a concern, address it
        if classification["type"] == "concern":
            return {
                "response_type": "address_concern",
                "concern": caller_input,
                "instruction": f"Address their concern about: '{caller_input}' "
                              f"Then continue naturally"
            }
        
        # Normal flow
        return {
            "response_type": "standard",
            "continue_with": self.current_step
        }
```

### Prompt Design
```yaml
instructions: |
  ## ADAPTATION RULES (CRITICAL)
  
  Before generating your response, CHECK what the caller said:
  
  IF they asked a QUESTION:
  → Answer it FIRST, then continue with your planned response
  → Example: "Good question—[answer]. So, [continue]..."
  
  IF they raised a CONCERN:
  → Address it FIRST, don't just acknowledge
  → Example: "Totally get that—[address concern]. [continue]..."
  
  IF they said YES with a CONDITION ("only if...", "but..."):
  → Note the condition before continuing
  → Example: "Got it, [acknowledge condition]. [continue]..."
  
  IF they shared CONTEXT (already know, participated before):
  → Acknowledge relevance before continuing
  → Example: "Oh nice! [connect to context]. [continue]..."
  
  IF they raised an OBJECTION:
  → Handle it—don't continue the pitch
  → This may change the flow entirely
  
  NEVER:
  - Continue to next script step ignoring their question
  - Say "Great!" then ask an unrelated question
  - Acknowledge a concern without addressing it
  - Treat a conditional yes as an unconditional yes
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `adaptation.question.answered` | < 85% |
| `adaptation.concern.addressed` | < 75% |
| `adaptation.condition.acknowledged` | < 80% |
| `adaptation.not_listening_complaints` | > 10% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Questions Ignored | answered < 80% | P2 |
| Concerns Unaddressed | addressed < 70% | P2 |
| High Frustration | complaints > 15% | P1 |

---

## References

- [Conversational AI Responsiveness](https://arxiv.org/abs/2106.07837) - Adaptive dialog
- [Voice Agent UX](https://www.beconversive.com/blog/voice-ai-challenges) - Responsiveness
- [Dialog State Tracking](https://arxiv.org/abs/2009.07261) - Context handling
- [AppInventiv: Voice Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Adaptation
