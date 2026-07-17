# Instruction Drift

## Issue: Agent Gradually Deviates from Original Instructions

**Frequency**: Common

**Symptoms**
- Agent behavior changes over long conversations
- Style or approach shifts from initial instructions
- Constraints mentioned early are violated later
- Agent "forgets" persona or role

**Root Cause**
As conversations grow, system instructions become proportionally smaller in context. Recent turns may implicitly override or contradict earlier instructions. Agent attention shifts toward recent content.

**Example**
```
System: "Always respond formally. Never use contractions."

Turn 1-10: Formal responses, no contractions
Turn 20: "Here's what you'll need to do..."
Turn 30: "Yeah, that's totally doable!"

Result: Agent has drifted from formal style to casual
```

---

## Test Scenario & Reproduction

### Scenario Setup
- A system prompt with an explicit, checkable style constraint ("Always respond formally. Never use contractions.")
- A single long-running conversation session (30+ turns) with no periodic instruction re-injection or constraint-checking middleware
- No adherence-scoring mechanism tracking output against the original constraint over the length of the session

### Trigger Mechanism
1. Establish the formal, no-contractions constraint in the system prompt
2. Conduct a long sequence of ordinary task turns (20-30+) without ever restating the constraint
3. Sample agent output at fixed turn checkpoints (e.g., turns 1-10, turn 20, turn 30) and check for contraction usage/tone shift
4. Compare adherence at the start of the conversation against adherence deep into it

**Example Reproduction Steps:**
```
1. System prompt: "Always respond formally. Never use contractions."
2. Turns 1-10: send routine task requests, record responses (expect formal, no contractions)
3. Turns 11-20: continue routine requests, sample response at turn 20 (e.g., "Here's what you'll need to do...")
4. Turns 21-30: continue routine requests, sample response at turn 30 (e.g., "Yeah, that's totally doable!")
5. Run a contraction/tone check against each sampled turn (1-10, 20, 30)
6. Plot adherence score against turn number
```

### Expected Failure State
- Contraction usage and casual tone increase measurably from the turn 1-10 baseline through turn 20 and turn 30, despite the original system constraint remaining unchanged
- Adherence score shows a downward trend correlated with turn number rather than staying flat
- No reminder or correction is triggered mid-session even as the violation persists
- A correctly-behaving system would maintain constant adherence to the formal/no-contractions rule regardless of conversation length

---

## Mitigation Strategies

### Prevention
1. **Periodic instruction re-injection**: Automatically re-insert the original system constraints (e.g., "respond formally, never use contractions") into context at a fixed turn interval or token threshold, rather than relying on a single system-prompt statement to remain influential as the conversation grows, since the root cause is that instructions become proportionally smaller in context over time and lose relative attention weight. Trade-off: repeated re-injection consumes additional tokens on every long conversation and can feel repetitive or robotic if surfaced to the user rather than kept in hidden system context.
2. **Instruction anchoring at high-attention positions**: Place critical constraints at both the start and immediately before the most recent user turn (the positions models attend to most reliably), rather than only at the very beginning of a long context, directly countering the mechanism where "agent attention shifts toward recent content" causes early instructions to lose influence. Trade-off: requires re-architecting prompt assembly to dynamically reposition constraints on every turn, adding complexity versus a static system prompt.
3. **Bounded session length with reset**: Cap conversation length (by turns or tokens) and prompt for a fresh session (carrying forward only an explicit summary of decisions, not full history) once the cap is reached, since a shorter effective context keeps the original instructions proportionally larger and closer to the model's attention. Trade-off: resets interrupt long-running workflows and require a reliable summarization step to avoid losing state when starting the new session.

### Detection & Response
1. **Instruction-adherence scoring over conversation length**: Periodically score agent outputs against the original constraints (e.g., "contains a contraction" as a formality violation) and plot adherence against turn number, since the documented pattern is gradual degradation over the length of the conversation — a downward trend is the direct signature of drift.
2. **Early-vs-late behavior comparison**: Automatically compare a sample of early-conversation outputs against late-conversation outputs on the same measurable dimension (tone, format, constraint compliance) and flag statistically significant divergence, catching drift that a single-point adherence check might miss.
3. **Explicit reminder triggers on detected drift**: When adherence scoring crosses a threshold, automatically inject an explicit reminder of the violated constraint into the next turn rather than waiting for the user to notice and re-state it, closing the loop between detection and correction within the same session.

### Architecture Patterns
1. **Constraint-checking middleware on output**: Architect a post-generation validation layer that checks agent output against the original constraint set (formality, banned phrases, persona rules) before it's returned, rejecting or auto-correcting violations rather than relying solely on the model's in-context adherence holding up over a long conversation.
2. **Persistent constraint store separate from conversational context**: Maintain the original instructions in a structured, external store that is re-rendered into the prompt fresh on every turn (rather than living only in the conversation history that grows and dilutes them), so instruction strength doesn't degrade as a function of conversation length.
3. **Session-summary-carrying reset architecture**: Architect long workflows as a sequence of bounded sub-sessions, each initialized with a compact structured summary (decisions, state, constraints) rather than raw history, so each sub-session starts with instructions at full relative strength instead of instructions that have been diluted across dozens of prior turns.

### Metrics
1. **instruction_adherence_score**: Target: no statistically significant decline from turn 1-10 baseline through turn 30+; Alert on adherence dropping more than 15% from early-conversation baseline
2. **constraint_violation_rate_by_turn_bucket**: Target: flat violation rate across turn buckets (1-10, 11-20, 21-30+); Alert on rate increasing with turn number
3. **drift_correction_trigger_rate**: Target: track as baseline; Alert on sustained high trigger rate indicating reminders aren't durably fixing drift
4. **session_length_at_reset**: Target: sessions reset before exceeding configured turn/token cap; Alert on sessions exceeding cap without a reset occurring

### Alerts
1. **Significant Instruction Adherence Decline** (P2): Condition - adherence score drops more than 15% from early-conversation baseline within a single session. Action: Inject an explicit constraint reminder into the next turn, log the session for review, consider forcing a session reset if the workflow supports it.
2. **Persona/Style Violation in Long Session** (P3): Condition - constraint-checking middleware flags an output violating a known persona rule (e.g., contraction detected in formal-mode session) in a session beyond turn 20. Action: Auto-correct the output if the middleware supports rewriting, otherwise flag for human review, log turn number for drift-pattern analysis.
3. **Session Exceeds Reset Threshold Without Reset** (P3): Condition - a session's turn or token count exceeds the configured cap without a reset/summarization event firing. Action: Investigate why the reset trigger failed, force a manual summarization checkpoint, review reset-logic configuration for that workflow.

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Instruction following degradation
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Behavioral drift patterns
