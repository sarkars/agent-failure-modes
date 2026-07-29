# Untracked Assumptions

## Issue: Agent makes assumptions then treats them as facts.

**Frequency**: Occasional

**Symptoms**
- Assumption appears as certain statement later.
- An unresolved guess filling an information gap (timezone, which report, default currency) is never flagged as tentative anywhere in the response or internal state.
- A later turn or action treats the assumed value as ground truth with no hedge language, even though the user never confirmed it.
- No clarifying question was asked despite the assumption being high-impact or irreversible (financial commitment, deletion, external send).
- User correction ("no, I meant...") reveals an assumption that was never surfaced or recorded anywhere in the trace.

**Root Cause**
Agent makes assumptions then treats them as facts.

**Example**
```
User: "Cancel my subscription and refund the last payment."
The agent has two active subscriptions on the account and silently
assumes the user means the more recently created one, without
registering this as an assumption or asking which subscription.

Three turns later, the agent states: "I've cancelled your Premium
subscription and processed the refund," phrased as settled fact.
The user actually meant the Basic subscription. Because the
assumption was never registered or hedged, there is no record
showing the agent guessed rather than confirmed which subscription
was meant, and the wrong one was cancelled.
```

**Contributing Factors**
- No structured assumption register exists to capture guesses made to fill information gaps, so they're indistinguishable from confirmed facts once written into working state.
- Generation is not required to use hedged language for values sourced from an unresolved assumption.
- No clarification threshold is defined for high-impact/irreversible actions, so the agent can assume its way through consequential ambiguity instead of asking.
- Multi-entity or multi-option situations (multiple accounts, multiple reports, ambiguous pronouns) increase the frequency of gap-filling guesses.
- No mechanism propagates a "low confidence" tag forward when later reasoning steps derive from an unresolved assumption.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Ambiguous entity reference | User request that could apply to one of several existing entities (e.g., two active subscriptions) with no specifier | Agent registers the ambiguity and asks a clarifying question before acting | Agent silently picks one entity and states the choice as settled fact |
| High-impact assumption gate | Ambiguous instruction preceding an irreversible action (refund, deletion, external send) | Mandatory clarification triggers before the action executes | Action executes based on an unconfirmed assumption with no clarifying question asked |
| Assumption-to-fact hardening scan | A registered low-confidence assumption is referenced again several turns later | Later reference retains hedged/tentative language or triggers re-confirmation | Later reference states the assumption as certain fact with no hedge |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| eval_clarification_trigger_rate_percent | 100% of eval high-impact ambiguity cases trigger a clarifying question | Script eval scenarios with ambiguous high-impact instructions, measure whether clarification fires before action |
| eval_assumption_registration_rate_percent | >= 95% of eval gap-filling guesses are captured in the assumption register | Inject ambiguous eval inputs requiring a guess, check register entries against known injected gaps |
| eval_hedge_language_compliance_percent | >= 95% of eval responses referencing an open assumption use hedged phrasing | Scan eval outputs for register-linked content and check for hedge markers vs. certain-fact phrasing |

---

## Mitigation Strategies

### Prevention
1. **Explicit Assumption Register**: Whenever the agent fills a gap in available information with a guess (unspecified timezone, ambiguous "the report" referring to which report, default currency), it writes the assumption into a structured register (assumption_text, confidence, basis) rather than silently folding it into working state as if it were confirmed fact.
2. **Confidence-Labeled Output Language**: Generation is required to render register entries with hedged language ("assuming you mean the Q3 report — let me know if not") in the response, and internal state that depends on an unresolved assumption is tagged low-confidence, preventing it from being silently promoted to a hard fact in later reasoning steps.
3. **Clarification Threshold for High-Impact Assumptions**: Assumptions above a defined impact/reversibility threshold (irreversible action, financial commitment, deletion) trigger a mandatory clarifying question instead of being registered and proceeded with — the agent is not allowed to assume its way through consequential ambiguity.

### Detection & Response
1. **Assumption-Promoted-to-Fact Scanning**: Compare later-turn statements against the assumption register; if a register entry is referenced in a later turn with certain/factual language (no hedge, no confidence marker) rather than its original tentative framing, flag as an untracked-assumption-hardening incident.
2. **User Correction Signal**: Monitor for user corrections that reveal an unstated assumption was wrong ("no, I meant..."), and check whether that assumption had been registered at all — if not, it's a register-coverage gap, not just an individual error.
3. **Assumption Density Auditing**: Track how many assumptions a given task accumulates before resolution; tasks with unusually high assumption density are higher-risk for compounding errors and are sampled for review.

### Architecture Patterns
1. **Structured Assumption Register**: A per-task data structure storing each assumption with confidence, basis, and resolution status (open, confirmed, rejected), consulted by both the generation layer (for hedged phrasing) and downstream reasoning (to avoid treating it as ground truth).
2. **Confidence-Propagating State Model**: Working state that derives from a register entry inherits its confidence tag; any action gated on that state checks the confidence level and applies the clarification-threshold rule before proceeding on low-confidence derived state.
3. **Clarification Interrupt Handler**: A control-flow hook that intercepts task execution when a new assumption crosses the impact/reversibility threshold, pausing forward progress until the ambiguity is resolved via a direct question to the user.

### Metrics
1. **assumption_hardening_incident_rate_percent**: Target: < 1% of tasks with assumptions; Alert threshold: > 5%
2. **unregistered_assumption_rate_percent**: Target: < 2% (assumptions inferred post-hoc from corrections that weren't in the register); Alert threshold: > 8%
3. **high_impact_assumption_bypass_count**: Target: 0 (should always trigger clarification); Alert threshold: > 0
4. **mean_assumption_density_per_task**: Target: tracked baseline per task type; Alert threshold: > 2x baseline

### Alerts
1. **High-Impact Assumption Bypassed Clarification** (P1 - Critical): Condition - an assumption above the impact/reversibility threshold was acted on without triggering the mandatory clarifying question. Action: Halt/reverse the action if possible, patch the threshold-check bypass, notify user of the assumption made.
2. **Assumption Hardened to Fact** (P2 - Warning): Condition - assumption_hardening_incident_rate_percent exceeds 5% over a rolling week. Action: Audit confidence-propagation logic, review generation prompts for hedging-language compliance.
3. **Assumption Density Spike** (P3 - Info): Condition - a task's assumption count exceeds 2x the baseline for its task type. Action: Flag task for review, consider whether upstream information-gathering should be improved to reduce reliance on assumptions.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| assumption_hardening_incident_rate_percent | > 5% |
| unregistered_assumption_rate_percent | > 8% |
| high_impact_assumption_bypass_count | > 0 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High-Impact Assumption Bypassed Clarification | An assumption above the impact/reversibility threshold was acted on without triggering the mandatory clarifying question | Critical |
| Assumption Hardened to Fact | assumption_hardening_incident_rate_percent exceeds 5% over a rolling week | Warning |
| Assumption Density Spike | A task's assumption count exceeds 2x the baseline for its task type | Info |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
