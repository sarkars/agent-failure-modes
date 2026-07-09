# Premature Finalization

## Issue: Agent returns final answer before completing required subtasks.

**Frequency**: Occasional

**Symptoms**
- Missing citations, skipped verification, incomplete checklist.
- [Add more specific symptoms]

**Root Cause**
Agent returns final answer before completing required subtasks.

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
1. **Completion Gate Tied to Acceptance Criteria**: The "return final answer" action is blocked unless a structured checklist derived from the task spec (each item with required evidence) is marked complete; the agent cannot invoke the finalize tool with unchecked items present.
2. **Mandatory Verification Step Before Finalize**: For task types requiring citations, tests, or self-consistency checks, encode the verification step as a required plan step that must execute and pass before the finalize action becomes available — not an optional step the agent may skip under time pressure.
3. **Structured Output Contract**: Require the final answer to conform to a schema with explicit fields (e.g., `citations: []`, `verification_status: str`); schema validation rejects finalize calls with empty required fields rather than accepting a plausible-looking but incomplete answer.

### Detection & Response
1. **Checklist Completion Scanner**: At finalize time, compare the structured checklist state against the required list from the task spec; any incomplete item blocks finalization and returns the agent to the outstanding subtask.
2. **Missing-Citation/Verification Linter**: Run an automated linter over the final output checking for required elements (citations, verification markers, test results) before it is released to the user, independent of what the agent claims it did.
3. **Post-Hoc Sampling Audit**: Sample completed tasks and have a human or LLM-judge reviewer verify completeness against the original spec, tracking a premature-finalization rate over time to catch gate bypasses or gaps in the checklist schema itself.

### Architecture Patterns
1. **Finalize Gate Service**: Sits in front of the "return to user" action, validating checklist/schema completeness before allowing the response to be released; fail-closed on ambiguous completion state.
2. **Structured Checklist State Machine**: Tracks each required subtask/verification item as pending/in-progress/complete in session state, giving the finalize gate a single source of truth to check against.
3. **Verification Sub-Agent**: An independent sub-agent or tool automatically invoked before finalize to re-check citations, run tests, or validate consistency, decoupled from the main agent's self-assessment.

### Metrics
1. **premature_finalization_rate_percent**: Target: 0%; Alert threshold: > 1%
2. **checklist_completion_rate_at_finalize_percent**: Target: 100%; Alert threshold: < 98%
3. **missing_citation_rate_percent**: Target: 0%; Alert threshold: > 2%
4. **verification_skip_rate_percent**: Target: 0%; Alert threshold: > 1%

### Alerts
1. **Finalize Without Required Verification** (P1 - Critical): Condition - finalize action invoked with verification step not completed. Action: Block release, force verification step, alert task owner.
2. **Checklist Incomplete at Finalize** (P1 - Critical): Condition - one or more required checklist items unmarked at finalize attempt. Action: Return agent to outstanding subtask, do not release response.
3. **Elevated Missing-Citation Rate** (P2 - Warning): Condition - missing_citation_rate exceeds 2% over a rolling day. Action: Review output schema enforcement and linter coverage.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
