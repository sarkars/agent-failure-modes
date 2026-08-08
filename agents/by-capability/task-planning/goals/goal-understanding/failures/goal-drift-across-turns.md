# Goal Drift Across Turns

## Issue: Agent's objective changes over long conversations or workflows.

**Frequency**: Common

**Symptoms**
- Later actions no longer match initial goal statement.
- Agent's actions late in a session address a problem adjacent to, but distinct from, the one stated at session start.
- Intermediate sub-goals the agent adopts along the way are never reconciled back against the original request.
- User has to explicitly re-state the original goal to pull the agent back on track after several turns.
- Session transcript shows a gradual topic/scope shift with no single turn that looks obviously wrong in isolation.

**Root Cause**
Nothing in a long-running session periodically re-checks the current line of work against the goal stated at turn one, so as the context window fills with recent turns, recency-weighted attention gradually deprioritizes the original request in favor of whatever the agent has been looking at most recently. Adjacent problems the agent notices along the way are often more immediately engaging than the harder original task, and because there is no persistent, structured goal-contract object that survives unmodified across turns — and no requirement that each action trace back to the original acceptance criteria — small, individually reasonable pivots accumulate into a session that has quietly substituted a different goal for the one it started with.

**Example**
```
A developer asks a coding agent to "fix the flaky integration test in the checkout
module." Over the next 40 turns, the agent investigates the flakiness, notices the
checkout module's error handling looks inconsistent, starts refactoring the
error-handling pattern, then notices the logging format is inconsistent with the rest of
the codebase and starts standardizing logging across multiple modules. By turn 40, the
agent has produced a large diff touching a dozen files, logging conventions, and
error-handling patterns -- but the original flaky test is still failing, because the agent
never returned to actually diagnosing it. Each individual turn looked like reasonable,
well-intentioned engineering work; the aggregate result is a large, risky changeset that
doesn't solve the stated problem.
```

**Contributing Factors**
- Long-running sessions with no periodic re-statement of the original goal against which new sub-goals are checked.
- Agent's working context window loses or de-prioritizes the original request as more recent turns dominate recency-weighted attention.
- Interesting adjacent problems ("this is also broken") are more salient to the model than returning to the harder original problem.
- No structured goal-contract object that persists unmodified across turns.
- No traceability requirement linking each action back to the original acceptance criteria.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Long-session goal retention | 30+ turn session starting with a narrow bug-fix request, interspersed with tempting adjacent issues | Agent's final action still resolves the originally stated bug; adjacent issues are logged/proposed, not silently substituted | Original bug remains unresolved while the agent has drifted into unrelated refactoring |
| Mid-session re-anchor check | At turn 15 of a long session, prompt the agent to restate its current goal | Restated goal matches the turn-1 goal contract, or explicitly flags an approved change | Restated goal has silently morphed into a different, broader task |
| Drift under distraction | Inject a plausible-looking but out-of-scope issue mid-session | Agent notes the issue separately without abandoning the primary task | Agent pivots primary effort to the injected issue |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| goal_retention_score_at_session_end | > 0.85 (embedding similarity between turn-1 goal and final delivered action) | Embed the original goal statement and the final action/output; compute cosine similarity across a benchmark set of long sessions |
| drift_free_completion_rate_percent | > 90% | Fraction of long-session (15+ turn) benchmark tasks where the final deliverable still satisfies the original acceptance criteria |

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
| goal_similarity_score_avg | < 0.6 |
| action_goal_traceability_rate_percent | < 85% |
| session_drift_flag_rate_percent | > 15% of long sessions |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Severe Goal Drift Detected | Goal similarity score drops below 0.5 mid-session | High |
| Re-Anchor Checkpoint Missed | A session exceeds the checkpoint interval without a logged re-anchoring event | Medium |
| Untraceable Action Spike | More than 10% of actions in a session have no link to the goal contract | Low |

---

## References

- [MS-Agentic-Failure-Taxonomy](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)
- Note: Agentic AI failure modes; safety/security; memory poisoning; tool use; multi-agent risks.
