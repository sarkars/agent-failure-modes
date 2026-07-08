# Preference Vs Instruction Confusion

## Issue: Agent treats a soft preference as a hard rule.

**Frequency**: Rare

**Symptoms**
- Unneeded refusal or rigid behavior.
- [Add more specific symptoms]

**Root Cause**
Agent treats a soft preference as a hard rule.

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
1. **Explicit Preference Strength Typing at Write Time**: When a memory is stored, classify it into a strength tier — hard_constraint (must never violate, e.g., allergy), soft_preference (default unless overridden, e.g., "prefers concise answers"), or contextual_hint (weak signal). Storage requires this classification, using phrasing cues ("never", "always" vs "I like", "usually") and, for ambiguous cases, defaults to soft_preference rather than hard_constraint.
2. **Task-Level Override Mechanism**: The current turn's explicit instruction always outranks a stored soft_preference of the same slot. The prompt-construction layer applies stored preferences only as defaults, and any in-conversation instruction that conflicts with a soft_preference silently overrides it for that task without requiring the user to first "cancel" the preference.
3. **Confidence-Weighted Application**: Soft preferences are applied with hedging/flexibility (the agent can deviate if the task calls for it) while hard constraints are applied with zero flexibility and always surfaced explicitly if they'd block a request. This distinction is enforced structurally, not left to the model's in-context judgment alone.

### Detection & Response
1. **Unnecessary Refusal/Rigidity Pattern Detection**: Monitor for responses where the agent declines or rigidly restricts an otherwise-reasonable request, then trace back to whether a stored soft_preference was the cited reason. Flag these as suspected mistyped preferences.
2. **User Override Frequency Tracking**: If a user repeatedly has to explicitly override the same stored preference within a task, that's a signal the preference was mistyped as too strong (or its scope is too broad); log the memory_id and override count.
3. **Preference Type Audit Sampling**: Periodically sample stored preferences and re-classify them against the original source utterance, checking for the storage-time classifier over-promoting soft language into hard_constraint tier.

### Architecture Patterns
1. **Two-Tier Preference Schema**: Memory schema distinguishes `strength: hard_constraint | soft_preference | contextual_hint` as a first-class field, with retrieval and prompt-assembly logic branching on this field rather than treating all stored facts uniformly.
2. **Instruction-Priority Resolver**: A resolver component ranks all applicable directives for a turn (explicit current-turn instruction > hard_constraint memory > soft_preference memory > contextual_hint) and only passes the resolved, non-conflicting directive set into the generation prompt.
3. **Preference Reclassification Feedback Loop**: When a mistyped preference is detected (via unnecessary refusal or user override), an automated or human-reviewed step downgrades its strength tier, closing the loop rather than requiring the same failure to repeat.

### Metrics
1. **unnecessary_refusal_rate_percent**: Target: < 0.5% of tasks; Alert threshold: > 2%
2. **preference_override_frequency_per_user**: Target: < 1 override per 20 tasks for same slot; Alert threshold: > 1 per 5 tasks
3. **mistyped_preference_count**: Target: < 5 per month found in audit; Alert threshold: > 20 per month
4. **hard_constraint_misclassification_rate_percent**: Target: < 1%; Alert threshold: > 3%

### Alerts
1. **Rigid Behavior Blocking Legitimate Task** (P2 - Warning): Condition - unnecessary_refusal_rate_percent exceeds 2% over a rolling week tied to a specific preference category. Action: Downgrade that preference's strength tier, review storage-time classifier prompt/rules, notify affected users if task was blocked.
2. **Repeated Override on Same Preference Slot** (P3 - Info): Condition - a user overrides the same soft_preference 3+ times within a week. Action: Auto-flag for reclassification review, consider lowering its default weight or scope.
3. **Hard Constraint Misclassification Found** (P1 - Critical): Condition - audit finds a genuine hard_constraint (e.g., safety/allergy) was stored or applied as soft_preference and got overridden. Action: Immediate correction of the record, review all recent tasks where that constraint may have been silently skipped, notify user if relevant.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Low |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
