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
1. **Pre-response trigger classification**: run a lightweight classifier on every caller turn (question / concern / condition / context / objection / standard) before generating the next agent turn, and require the response to address any detected trigger before continuing the planned flow, since the failure is structurally caused by the agent generating its next scripted step without first checking whether the caller's response requires a different path. Trade-off: adds a classification call (latency/cost) to every turn, and misclassified turns can still let genuine adaptation triggers slip through.
2. **Acknowledgment-before-continuation prompt constraint**: enforce a hard prompt/response-schema rule that any detected question, concern, or objection must be addressed in the response before any planned-flow content is emitted ("answer/address first, then continue"), since transcripts show the agent completing sentences and moving to the next script step even mid-caller-interruption. Trade-off: rigidly enforcing "address first" can produce overly long responses when multiple triggers stack in one caller turn.
3. **Conditional-branch library for common objection/condition patterns**: pre-author explicit conditional branches for frequent patterns ("yes, but only if...", "I already know about this," "I don't have time") so the flow has a designed alternate path rather than forcing the model to improvise a deviation from script, since the state machine's rigidity itself — not just the model's attentiveness — is a root cause. Trade-off: branch libraries require ongoing curation as new caller patterns emerge and can't cover every conversational variation.

### Detection & Response
1. **Turn-pair relevance scoring**: score each agent turn for topical relevance to the immediately preceding caller turn (embedding similarity or an LLM-judge check of "does this response address what was just said"); low-relevance pairs are the direct signature of a continued-script-ignoring-response failure. Response: flag the call segment for review and, for real-time-capable systems, insert a corrective clarifying turn.
2. **"Not what I asked" / correction-phrase detection**: detect caller phrases indicating the agent missed their input ("that's not what I asked," repeated restatements). Response: route matched call transcripts into a labeled adaptation-failure eval set and, if live, prompt the agent to re-acknowledge the missed input.
3. **Trigger-type miss-rate breakdown**: track, per trigger type (question/concern/condition/context/objection), what fraction were followed by an on-topic response versus a script continuation — this call-level breakdown identifies which trigger type the classifier or prompt is weakest on. Response: prioritize prompt/classifier fixes for the worst-performing trigger type.

### Architecture Patterns
1. **Interrupt-driven flow manager**: replace the linear/rigid flow state machine with an interrupt-driven design where classified triggers (question, concern, objection) can preempt the current planned step, requiring the flow manager to explicitly resume or re-route after handling the interrupt, structurally supporting deviation instead of only forward progression.
2. **Context-carrying turn generation**: inject the full classification result and the caller's last utterance, not just the next scripted step, into every generation call, so response generation is conditioned on "what do I need to address" as a first-class input rather than the model needing to infer it from raw transcript history under turn-by-turn prompting.
3. **Conditional branching engine**: implement conditions and objections as explicit branch nodes in the flow graph, not implicit model behavior, so a conditional "yes, but..." or an objection structurally routes to a different next-state than an unconditional "yes," matching the finding that conditional answers are among the most frequently mishandled trigger types.

### Metrics
1. **adaptation_rate**: Target: >85%; Alert on <75% over rolling 7-day call sample
2. **question_answered_before_continuation_rate**: Target: >90%; Alert on <80%
3. **concern_addressed_rate**: Target: >80%; Alert on <70%
4. **condition_acknowledgment_rate**: Target: >90%; Alert on <75%
5. **not_listening_complaint_rate**: Target: <10%; Alert on >15%

### Alerts
1. **Adaptation Rate Drop** (P2): Condition - adaptation_rate falls below 75% over a rolling 7-day window. Action: pull a call sample stratified by trigger type, identify the weakest classifier/prompt path, patch and re-eval before the next deploy.
2. **High Not-Listening Complaints** (P1): Condition - not_listening_complaint_rate exceeds 15%. Action: page the conversation-design owner, sample recent calls for repeated script-continuation failures, consider rolling back recent flow-script changes.
3. **Condition/Objection Mishandling Spike** (P2): Condition - condition_acknowledgment_rate falls below 75% or objection-handling relevance score drops sharply week over week. Action: review and expand the conditional-branch library for the specific patterns driving the drop.

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
