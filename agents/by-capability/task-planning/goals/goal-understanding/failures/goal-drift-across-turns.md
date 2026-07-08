# Goal Drift Across Turns

## Issue: Agent's objective changes over long conversations or workflows.

**Frequency**: Common

**Symptoms**
- Later actions no longer match initial goal statement.
- [Add more specific symptoms]

**Root Cause**
Agent's objective changes over long conversations or workflows.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Durable Goal Anchor Object**: Capture the original goal statement and acceptance criteria once at session start into an immutable "goal contract," and inject it into context at every turn rather than relying on the model to reconstruct intent from a growing conversation history where it can be diluted or overwritten by intervening turns.
2. **Turn-by-Turn Objective Diffing**: Before executing each turn's action, diff the currently-inferred objective against the anchored goal contract. Material divergence requires an explicit confirmation that the goal has intentionally changed, rather than letting the shift happen silently over several turns.
3. **Periodic Goal Re-Anchoring Checkpoints**: At fixed intervals (every N turns or a time budget), the agent re-states its current understood goal against the anchor and surfaces it for a lightweight confirm/correct step, catching slow accumulated drift before it compounds across a long session.

### Detection & Response
1. **Semantic Drift Scoring**: Embed the goal anchor and the current turn's working objective, compute cosine similarity each turn, and track the trendline. Alert when similarity drops below a threshold or shows a sustained downward trend rather than waiting for a single bad turn.
2. **Action-to-Goal Traceability Audit**: Tag every executed action with the specific part of the goal contract it serves. Actions with no traceable link to the anchor are flagged as drift candidates for review, independent of whether they look individually reasonable.
3. **Session Replay Diffing**: An offline job replays session transcripts, extracting the goal statement from turn 1 and the final action taken, and computes a drift score. Use this for regression testing across model/prompt changes and for a drift dashboard across all sessions.

### Architecture Patterns
1. **Goal Contract Store**: A session-scoped, immutable store holds the original goal object separate from the mutable conversation buffer. The planner reads from this store every turn instead of inferring the goal solely from recent conversational history.
2. **Drift Detector Middleware**: A stateless service between planner and executor computes anchor-vs-current similarity per turn and can block or flag execution when drift crosses threshold, keyed by session_id so it scales independently of the agent.
3. **Re-Anchoring Prompt Injection**: The orchestrator periodically injects a system-level reminder turn containing the original goal contract verbatim into the context window, counteracting recency bias in long-running sessions.

### Metrics
1. **goal_similarity_score_avg**: Target: > 0.85 (embedding cosine similarity to anchor); Alert threshold: < 0.6
2. **turns_since_last_reanchor**: Target: below the defined checkpoint interval (e.g., 10 turns); Alert threshold: exceeded without a checkpoint firing
3. **action_goal_traceability_rate_percent**: Target: > 95%; Alert threshold: < 85%
4. **session_drift_flag_rate_percent**: Target: < 5% of long sessions (> 15 turns); Alert threshold: > 15%

### Alerts
1. **Severe Goal Drift Detected** (P1 - Critical): Condition - goal similarity score drops below 0.5 mid-session. Action: pause autonomous execution and re-present the original goal contract to the user for confirmation before continuing.
2. **Re-Anchor Checkpoint Missed** (P2 - Warning): Condition - a session exceeds the checkpoint interval without a logged re-anchoring event. Action: force a checkpoint immediately; if systemic across many sessions, alert orchestration on-call.
3. **Untraceable Action Spike** (P3 - Info): Condition - more than 10% of actions in a session have no link to the goal contract. Action: flag the session for manual audit and review for scope creep alongside drift.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [MS-Agentic-Failure-Taxonomy](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)
- Note: Agentic AI failure modes; safety/security; memory poisoning; tool use; multi-agent risks.
