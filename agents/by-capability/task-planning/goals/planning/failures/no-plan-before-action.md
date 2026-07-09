# No Plan Before Action

## Issue: Agent jumps into tool calls or actions without decomposing the workflow.

**Frequency**: Common

**Symptoms**
- Immediate write/action calls on complex task.
- [Add more specific symptoms]

**Root Cause**
Agent jumps into tool calls or actions without decomposing the workflow.

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
1. **Planner-First Gate**: For any task classified above a complexity threshold, the orchestrator requires a plan artifact (structured subtask list) to exist in session state before the first mutating tool call is permitted; the tool executor rejects calls made with no plan reference.
2. **Complexity Classifier**: Run a lightweight classifier over the incoming task (counting distinct entities, systems touched, and estimated steps) before execution begins. Tasks scoring above threshold are routed to the planning-required lane; simple single-step tasks are exempt to avoid unnecessary overhead.
3. **Tool-Call Rate Limiting Before Plan Exists**: Cap the number of tool calls an agent can make before a plan artifact is recorded (e.g., 1 read-only lookup allowed, then must plan), preventing the agent from chaining multiple actions without ever stepping back to decompose the task.

### Detection & Response
1. **Immediate-Action Detector**: Monitor the first N actions of every session for tool calls that occur before any plan or reasoning artifact is recorded; flag and log these as no-plan-before-action events.
2. **Plan Presence Audit**: Sample sessions above the complexity threshold and verify a plan artifact exists and was created before the first mutating action; missing plans are scored against session outcome quality.
3. **Correlate Skipped-Planning Sessions with Error/Rollback Rate**: Track whether sessions that skipped planning have a higher rate of errors, rollbacks, or user corrections than planned sessions, to quantify the real cost of skipping.

### Architecture Patterns
1. **Plan-Then-Execute Orchestrator**: Two distinct phases — a planning phase that must emit a structured plan artifact, and an execution phase gated on that artifact's existence — enforced by the orchestrator, not left to agent discretion.
2. **Plan Artifact Schema**: A structured object `{subtasks, dependencies, created_at}` stored in session state and referenced by the tool executor on every call to confirm a plan exists.
3. **Complexity Router**: Routes incoming tasks to either a "planning-required" execution lane or a "direct-execution" lane for genuinely trivial tasks, based on the complexity classifier's score.

### Metrics
1. **plan_presence_rate_percent**: Target: 100% for complex tasks; Alert threshold: < 98%
2. **premature_action_rate_percent**: Target: 0%; Alert threshold: > 1%
3. **complexity_misroute_rate_percent**: Target: < 3%; Alert threshold: > 8%
4. **mean_actions_before_plan**: Target: 0 mutating actions; Alert threshold: >= 1

### Alerts
1. **No-Plan High-Complexity Task** (P1 - Critical): Condition - a task classified as complex executed a mutating action with no plan artifact present. Action: Halt session, force planning phase, review classifier and gate logic.
2. **Elevated Premature Action Rate** (P2 - Warning): Condition - premature_action_rate exceeds 1% over a rolling day. Action: Audit recent classifier scores and gate enforcement for regressions.
3. **Complexity Classifier Drift** (P3 - Info): Condition - misroute rate trending upward over a week. Action: Retrain/recalibrate the complexity classifier.

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
