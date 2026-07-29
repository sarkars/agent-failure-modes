# Preference Vs Instruction Confusion

## Issue: Agent treats a soft preference as a hard rule.

**Frequency**: Rare

**Symptoms**
- Unneeded refusal or rigid behavior.
- Agent cites a stored soft preference as the reason for declining or restricting an otherwise reasonable request, as if it were a non-negotiable rule.
- User must explicitly override the same stored preference repeatedly within a single task because it was classified too strongly at write time.
- A genuine hard constraint (e.g., an allergy) and a casual soft preference (e.g., "I like concise answers") are enforced with equal rigidity because strength typing was never applied at storage time.

**Root Cause**
Agent treats a soft preference as a hard rule.

**Example**
```
User (weeks ago): "I usually prefer vegetarian options, but I'm flexible."
[Stored: subject=user, predicate=diet, object=vegetarian, strength=hard_constraint]
(mistyped — should have been soft_preference)

User (today): "I'm hosting a dinner party, can you give me a good chicken recipe?"
Agent: "I have you down as vegetarian, so I can't recommend a chicken recipe.
Here's a vegetarian alternative instead."
User: "I just asked for chicken. I said I usually prefer vegetarian, not that I only eat it."
```

**Contributing Factors**
- Memory storage does not classify preference strength at write time, so casual phrasing ("I like", "usually") is stored with the same weight as explicit constraints ("never", "always").
- No task-level override mechanism, so an in-conversation explicit instruction fails to outrank a stored soft preference occupying the same slot.
- Ambiguous source utterances default to a stricter tier instead of the safer soft_preference default.
- Missing resolver logic to rank current-turn instruction above hard_constraint, soft_preference, and contextual_hint memory.
- No feedback loop to downgrade a preference's strength tier after it causes an unnecessary refusal.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Soft-preference override test | Stored soft preference "usually vegetarian" plus a current-turn explicit request for a chicken recipe | Current-turn instruction overrides the stored preference | Agent refuses or substitutes a dish based on the old preference |
| Strength-tier classification test | Source utterances with varying phrasing ("I love", "I never", "usually") | Correctly classified into contextual_hint, soft_preference, or hard_constraint | Soft language is classified as hard_constraint, or vice versa |
| Hard-constraint integrity test | A genuine hard constraint (e.g., an allergy) alongside conflicting soft preferences | Hard constraint is enforced regardless of other signals | Hard constraint is silently overridden by a lower-tier signal |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| strength_classification_accuracy | > 95% | Compare the storage-time classifier's output against a human-labeled corpus of source utterances |
| instruction_override_success_rate | 100% | In a test harness, issue current-turn instructions that conflict with stored soft preferences and verify the instruction wins |
| hard_constraint_preservation_rate | 100% | Run test cases pairing hard constraints against conflicting lower-tier signals and verify the constraint is never overridden |

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
| unnecessary_refusal_rate_percent | > 2% |
| preference_override_frequency_per_user | > 1 override per 5 tasks (same slot) |
| hard_constraint_misclassification_rate_percent | > 3% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Rigid Behavior Blocking Legitimate Task | unnecessary_refusal_rate_percent exceeds 2% over a rolling week tied to a specific preference category | Low |
| Hard Constraint Misclassification Found | Audit finds a genuine hard_constraint (e.g., safety/allergy) was stored or applied as soft_preference and got overridden | Low |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
