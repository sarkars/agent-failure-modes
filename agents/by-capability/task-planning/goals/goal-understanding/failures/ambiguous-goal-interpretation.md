# Ambiguous Goal Interpretation

## Issue: Agent optimizes for a different meaning of the user's/business goal.

**Frequency**: Common

**Symptoms**
- Clarification avoided; final output solves adjacent problem.
- [Add more specific symptoms]

**Root Cause**
Agent optimizes for a different meaning of the user's/business goal.

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
1. **Structured Goal Restatement Gate**: Before execution, the agent must produce a paraphrase of the request plus explicit, checkable acceptance criteria. Execution proceeds only if the user (or an automated confidence check) confirms the restatement, or if a calibrated confidence score clears a threshold. This forces the ambiguity to surface as a question instead of a silent default reading.
2. **Ambiguity Scoring via Interpretation Enumeration**: Before planning, sample multiple candidate interpretations of the request (e.g., via multi-sample generation or a lightweight parser) and score how much they diverge. If more than one materially different, plausible interpretation exists, block auto-execution and route to a clarifying question instead of picking the most likely one silently.
3. **Interpretation-Locked Context Injection**: Maintain an org/domain glossary of previously-resolved ambiguous terms and examples ("when a user says X in context Y, they mean Z"). Retrieve and inject the relevant entries before execution so default readings are grounded in prior resolutions rather than the model's unconstrained guess.

### Detection & Response
1. **Divergence-from-Candidate-Interpretations Check**: After generation, compare the final output's content/keywords against each candidate interpretation identified pre-execution. Flag and hold for review any output that aligns with a non-primary (adjacent) interpretation rather than the one the user most likely meant.
2. **Clarification-Avoidance Rate Monitoring**: Track, per session, the fraction of ambiguity-flagged requests where the agent proceeded without asking a clarifying question. A rising trend indicates the clarification gate is being bypassed or under-triggering, and should page the owning team.
3. **Post-Delivery Correction Mining**: Scan follow-up user turns for correction phrases ("I meant," "no, I wanted," "that's not right") tied to an earlier ambiguous request. Feed confirmed misinterpretations back into the ambiguity classifier and the interpretation glossary so the same phrasing is caught next time.

### Architecture Patterns
1. **Clarification Middleware**: A pre-execution service sits between the input parser and the planner. It runs the ambiguity classifier on every incoming request and either forwards it to the executor or returns a clarifying-question response, so ambiguity handling is enforced outside the model's own discretion.
2. **Multi-Sample Consensus Check**: Sample N candidate plans from the model at a relaxed decoding setting; if the plans diverge substantially (different target entities, different scope), route to a human-in-the-loop or clarifying question rather than silently taking the majority-vote plan.
3. **Goal Contract Object**: Generate a structured object (task, scope, explicit exclusions, acceptance criteria) once at request intake and pass it through the entire execution pipeline as the single source of truth for "what the goal means," versioned so later steps can't silently reinterpret it.

### Metrics
1. **ambiguity_flagged_rate_percent**: Target: 10-20% of genuinely ambiguous request types; Alert threshold: < 5% (classifier likely under-triggering)
2. **clarification_ask_rate_on_flagged_percent**: Target: > 90%; Alert threshold: < 70%
3. **post_delivery_reinterpretation_rate_percent**: Target: < 5%; Alert threshold: > 15%
4. **interpretation_divergence_score_avg**: Target: < 0.3; Alert threshold: > 0.5

### Alerts
1. **Silent Reinterpretation Spike** (P1 - Critical): Condition - post_delivery_reinterpretation_rate exceeds 15% over a rolling 24h window. Action: force clarification-first mode for the affected request category, pause unattended auto-execution.
2. **Ambiguity Classifier Drift** (P2 - Warning): Condition - ambiguity_flagged_rate falls below 5% for a sustained week despite historical baseline being higher. Action: recalibrate/retrain the classifier, audit recent unflagged sessions for missed ambiguity.
3. **Repeated Correction on Same Task Template** (P3 - Info): Condition - 3+ user corrections logged against the same task template within 7 days. Action: review and update the task template wording or glossary entry to close the interpretation gap.

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
