# No Long-Horizon Evaluation

## Issue: Multi-step degradation is missed.

**Frequency**: Common

**Symptoms**
- Single-turn tests pass; workflow fails.
- [Add more specific symptoms]

**Root Cause**
Multi-step degradation is missed.

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
1. **Multi-Turn Trajectory Eval Suite**: Build eval cases that span full multi-step workflows (not single-turn Q&A), scoring both the final outcome and intermediate state consistency at each step, so compounding drift across turns is caught before shipping.
2. **Long-Horizon Regression Benchmarks**: Maintain a fixed set of long-running task scenarios (e.g., 10+ turn conversations, multi-day workflows with state persistence) re-run on every release to catch degradation that only appears after several steps.
3. **State Consistency Checkpointing in Design**: Require the agent architecture to explicitly checkpoint and validate critical state (task progress, accumulated facts, user intent) at defined intervals during long workflows, rather than relying on unbounded context accumulation that silently drifts.

### Detection & Response
1. **Turn-by-Turn Quality Degradation Tracking**: Score each turn in production multi-turn sessions and plot quality/accuracy against turn number; alert if there's a statistically significant downward trend as sessions lengthen.
2. **Workflow Completion Rate by Length Bucket**: Track task completion/success rate bucketed by workflow length (number of steps/turns); a completion rate that drops sharply past a certain length indicates long-horizon degradation invisible to single-turn evals.
3. **Context Drift Detection**: Monitor for signals of context drift in long sessions (contradicting earlier statements, forgetting established facts, repeating already-completed steps) via automated consistency checks against session history.

### Architecture Patterns
1. **Trajectory-Level Eval Harness**: Eval infrastructure runs full multi-step scenarios end-to-end (simulating user turns, tool calls, and state transitions) rather than isolated single-turn prompts, scoring trajectory-level success and per-step consistency.
2. **State Summarization and Checkpointing Layer**: The architecture periodically summarizes and re-anchors critical state into a compact, explicit representation (rather than raw growing context) to bound drift over long horizons, with each checkpoint eval-tested independently.
3. **Session Replay and Diff Tooling**: Tooling replays a full production session and diffs agent-stated facts/decisions turn-by-turn against ground truth or earlier turns, used both for debugging and to mine new long-horizon eval cases.

### Metrics
1. **quality_degradation_slope_per_turn**: Target: ~0 (no significant downward trend); Alert threshold: statistically significant negative slope
2. **workflow_completion_rate_by_length_bucket_pct**: Target: < 10 point drop from short to long bucket; Alert threshold: > 25 point drop
3. **context_drift_incident_rate_pct**: Target: < 2% of long sessions; Alert threshold: > 8%
4. **long_horizon_eval_coverage_count**: Target: >= 20 multi-turn scenarios in regression suite; Alert threshold: < 10

### Alerts
1. **Long-Horizon Completion Rate Collapse** (P1 - Critical): Condition - workflow completion rate for the long-length bucket drops more than 25 points below the short-length bucket. Action: Block release, run the trajectory-level eval suite to isolate the failing step range.
2. **Context Drift Spike** (P2 - Warning): Condition - context drift incident rate exceeds 8% of long sessions in a monitoring window. Action: Review state-summarization logic, add drift cases to the long-horizon eval suite.
3. **Quality Degradation Trend Detected** (P2 - Warning): Condition - turn-by-turn quality shows a statistically significant downward slope in production sampling. Action: Investigate context window management, prioritize long-horizon regression fix.

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

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
