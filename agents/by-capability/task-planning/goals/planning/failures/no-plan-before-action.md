# No Plan Before Action

## Issue: Agent jumps into tool calls or actions without decomposing the workflow.

**Frequency**: Common

**Symptoms**
- Immediate write/action calls on complex task.
- Agent starts editing files or running migrations on the first turn of a multi-file refactor with no visible plan or task list.
- Later steps contradict earlier ones (e.g., renames a function, then a subsequent edit still calls the old name) because there was no upfront map of dependent files.
- Agent re-derives scope mid-task after already making changes, requiring rework or reverts.
- No task list, TODO breakdown, or reasoning trace precedes the first shell/file-write command for a task spanning multiple components.

**Root Cause**
Tasks that look simple on the surface — "just swap a library" — lead the agent to underestimate how much upfront decomposition they actually require, and with no complexity gate mandating a plan artifact before the first mutating call, there's nothing to correct that misjudgment before changes start happening. The agent's tool-use loop tends to reward fast, visible progress like file edits over an initial non-action planning turn, and dependencies between files or systems that would only become visible through an explicit enumeration step stay hidden until the agent stumbles into them mid-edit. Because the session enforces no distinction between exploratory read-only calls and the first truly committing action, the agent can commit to an approach before it has surveyed enough of the problem to know that approach won't hold for the whole task.

**Example**
```
A coding agent is asked to "migrate the app's date handling from moment.js to date-fns across the codebase." Instead of first enumerating the files that import moment.js, checking for usages with non-trivial API differences (timezone handling, locale formatting), and sequencing the change, the agent immediately opens the first file it finds and starts swapping imports and rewriting calls. Three files in, it hits a timezone-conversion usage that date-fns handles differently, requiring a different replacement pattern than the one it has been applying — but by then it has already committed inconsistent replacements across the first three files, and has to backtrack and redo work it could have planned around from the start.
```

**Contributing Factors**
- Task appears simple at first glance ("just swap a library") so the agent underestimates the need for upfront decomposition.
- No complexity classifier or gate requires a plan artifact before the first mutating tool call.
- Agent's tool-use loop rewards fast visible progress (file edits) over an initial non-action planning turn.
- Long-horizon dependencies (files that reference each other) aren't visible without an explicit search/enumeration step the agent skipped.
- No session-level enforcement distinguishes exploratory read-only calls from the first committing action.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Multi-file refactor gate | "Migrate date handling from moment.js to date-fns across the repo" | Agent produces a file-level plan/task list (enumerated affected files, sequencing) before the first file edit | First file edit occurs with no preceding plan artifact or enumeration step in the trace |
| Trivial single-file task exemption | "Fix the typo in README.md line 12" | Agent may act directly without a formal plan (task below complexity threshold) | Agent stalls generating an unnecessary plan for a genuinely trivial change |
| Dependency-aware sequencing | Task touching 5 interdependent files with shared imports | Plan lists files in a dependency-respecting order before edits begin | Edits proceed in file-discovery order with no dependency analysis, causing rework |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| plan_before_first_mutation_rate_percent | 100% for tasks above complexity threshold | Check trace for a plan/task-list artifact preceding the first file-write or shell-mutating call |
| rework_edit_rate_percent | < 10% | Count of files edited more than once due to inconsistent early changes, divided by total files touched |

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
| plan_presence_rate_percent | < 98% for complex tasks |
| premature_action_rate_percent | > 1% |
| mean_actions_before_plan | >= 1 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| **Mutating Action With No Plan Artifact** | A file-write, git-commit, or migration command executes with no plan/task-list present in session state | High |
| **Elevated Premature Action Rate** | premature_action_rate exceeds 1% over a rolling day | Medium |
| **Complexity Classifier Drift** | Misroute rate (simple-lane tasks that were actually complex) trending upward over a week | Low |

---

## References

- [MS-Agentic-Failure-Taxonomy](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)
- Note: Agentic AI failure modes; safety/security; memory poisoning; tool use; multi-agent risks.
