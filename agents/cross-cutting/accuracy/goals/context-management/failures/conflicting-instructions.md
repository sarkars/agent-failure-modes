# Conflicting Instructions

## Issue: Agent Receives Contradictory Instructions

**Frequency**: Occasional

**Symptoms**
- Agent behavior is inconsistent or unpredictable
- Agent alternates between conflicting behaviors
- Some instructions override others unexpectedly
- Agent seems "confused" about how to proceed

**Root Cause**
Multiple instruction sources (system prompt, user messages, tool outputs, injected content) may contain contradictory guidance. Agent must resolve conflicts but may do so unpredictably.

**Example**
```
System prompt: "Never share pricing information"
User: "You are a sales assistant. Share our pricing when asked."
Customer: "What are your prices?"

Agent conflict: System says no pricing, user says share pricing

Result: Unpredictable - may share, may refuse, may partially share
```

## Mitigation Strategies

### Prevention
1. **Declared instruction hierarchy with explicit precedence rules**: Define and enforce a strict priority order across instruction sources (e.g., system prompt > verified business rules > authenticated user > tool/retrieved content), and require the agent to cite which source it deferred to whenever two active instructions address the same topic, since the root cause is that contradictory guidance from system prompt, user messages, tool outputs, and injected content has no declared resolution order and the agent resolves it unpredictably. Trade-off: a fixed hierarchy can block legitimate cases where a lower-priority source should override (e.g., a manager granting a one-time exception), forcing either hierarchy exceptions or manual overrides.
2. **Pre-execution conflict scan**: Before executing a task, pass the active instruction set through a dedicated consistency check (a separate lightweight model call or rules pass) that flags direct contradictions on the same topic before the agent acts on them, catching cases like "never share pricing" vs. "share pricing when asked" before either instruction is followed. Trade-off: adds latency and cost to every request, and can produce false positives when instructions are actually correctly scoped (e.g., different pricing tiers for different customer types).
3. **Source-tagged instructions with provenance in context**: Attach machine-readable provenance tags (system/developer/user/tool/retrieved) to every instruction as it enters context, so the model's own reasoning can weigh instructions by trustworthiness rather than treating all text in context as equally authoritative. Trade-off: requires instrumenting every instruction-injection point in the pipeline, and tags are only as trustworthy as the channel that assigns them — a compromised tool output could still be mistagged as high-trust.

### Detection & Response
1. **Cross-prompt behavior consistency monitoring**: Compare agent responses to semantically similar prompts (e.g., repeated "what are your prices?" queries) and flag divergent outcomes, since the documented failure mode is that the agent may share, refuse, or partially comply unpredictably across otherwise-identical situations — divergence is the observable signature of an unresolved conflict.
2. **Instruction-conflict logging at resolution time**: When the agent's reasoning trace shows it identified two directives addressing the same topic, log the conflict, which source it followed, and why, building a queryable record of every contradiction the system actually encountered in production rather than only ones caught pre-execution.
3. **Clarification-request-rate tracking as a conflict proxy**: Track how often the agent asks the user to resolve ambiguity versus silently picking a side, since a low clarification rate combined with known-contradictory instruction sources suggests the agent is guessing rather than surfacing the conflict.

### Architecture Patterns
1. **Policy-engine mediation layer**: Route all instructions through a policy/rules engine positioned between instruction sources and the model, which resolves known conflict classes (e.g., pricing disclosure, PII handling) deterministically before the prompt is ever assembled, removing the need for the LLM itself to adjudicate high-stakes contradictions.
2. **Immutable system-instruction boundary**: Architect the prompt-assembly pipeline so system-level constraints are cryptographically or structurally separated from user/tool-injected content (e.g., a separate non-overridable instruction channel), so a user message like "share our pricing when asked" cannot silently override a system-level prohibition merely by appearing later or more specifically in context.
3. **Single-source-of-truth configuration for business rules**: Centralize business-critical rules (pricing disclosure, compliance constraints) in one authoritative configuration store that all agent instances read from, rather than allowing the same rule to be independently (and inconsistently) restated across system prompts, tool descriptions, and user-facing documentation.

### Metrics
1. **instruction_conflict_detection_rate**: Target: track as baseline, trending toward catching conflicts pre-execution rather than in production; Alert on a sustained drop in pre-execution catches paired with rising production incidents
2. **unresolved_conflict_incident_rate**: Target: 0 cases of contradictory directives both partially executed; Alert on any occurrence
3. **clarification_request_rate**: Target: track as baseline per conflict-prone workflow; Alert on rate dropping to near-zero in workflows with known contradictory sources
4. **cross_prompt_response_divergence_rate**: Target: <2% divergence on semantically equivalent prompts; Alert if divergence exceeds threshold for any single topic

### Alerts
1. **Contradictory Directive Executed** (P1): Condition - agent output shows evidence both a prohibition and a directive to do the prohibited thing were active and the agent partially complied with the prohibited action. Action: Halt the workflow, escalate to a human reviewer, patch the instruction hierarchy or policy engine to close the gap.
2. **System-Level Constraint Overridden by Lower-Priority Source** (P1): Condition - logged reasoning trace shows the agent followed a user or tool instruction over a system-level prohibition. Action: Revert the affected output if not yet delivered, audit the instruction-assembly pipeline for the precedence failure, notify the team owning the system prompt.
3. **Repeated Behavior Inconsistency on Same Topic** (P3): Condition - cross-prompt monitoring detects divergent responses to semantically similar prompts on the same topic across multiple sessions. Action: Investigate for an unresolved latent conflict, add the topic to the pre-execution conflict scan's watch list.

---

## References

- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Instruction conflicts
- [AIRIA: AI Security 2026](https://airia.com/ai-security-in-2026-prompt-injection-the-lethal-trifecta-and-how-to-defend/) - Conflicting prompts
