# Renamed Metric Empty Result Read as Healthy Zero

## Issue: Monitoring Agent Queries a Metric Under a Name It Knows From Training Data or a Stale Internal Doc, the Metric Was Renamed During a Schema Migration, and the Agent Interprets the Resulting Empty Series as "Value Is Zero / Check Passing" Instead of "Metric Does Not Exist"

**Frequency**: Occasional

**Symptoms**
- Agent builds or maintains an alert rule or dashboard query referencing a metric name it recalls from prior context (training data, an older internal runbook, a stale schema doc), the query executes without error against the metrics backend, and returns zero matching time series
- The agent's downstream logic treats "zero series returned" identically to "the metric's value is 0," reporting the associated check as passing or the system as healthy, rather than flagging that the queried metric could not be found
- The alert or dashboard tied to the renamed metric goes silent permanently after a metrics-taxonomy migration, with no error, warning, or gap indicator anywhere in the pipeline — it simply always reports "healthy" from that point forward
- The blind spot is discovered only when an actual incident occurs in the area the silently-disabled alert was supposed to cover, and post-incident review finds the alert had been effectively dead for weeks or months
- The gap concentrates on metrics renamed or relabeled during infrastructure migrations (label restructuring, metric-naming-convention changes, observability-platform migrations) where the old name simply stops matching anything rather than erroring

**Root Cause**
Metrics backends commonly return an empty result set, not an error, when a query's metric name or label selector matches no existing time series — this is indistinguishable at the response level from "the metric exists and its current value is legitimately zero." A monitoring agent whose query-result handling does not explicitly check for series existence before evaluating a threshold conflates these two structurally identical but semantically opposite outcomes. Combined with the agent's reliance on a metric name recalled from training-time knowledge or a document that predates a schema migration, rather than a live schema/existence check against the current metrics backend, the agent has no signal telling it the query is targeting a name that no longer resolves to anything — it simply evaluates "0 is within the healthy threshold" and moves on.

**Example**
```
Monitoring agent maintains an alert rule for elevated checkout failures, originally built against
the metric name checkout_error_total{service="checkout-api"}
Six weeks later: the observability team migrates to a standardized metric-naming convention during
a platform upgrade; checkout_error_total is renamed to checkout.errors.count as part of the migration,
with no aliasing/backward-compatible shim configured for the old name
Agent's alert rule still queries checkout_error_total{service="checkout-api"} — the query executes
successfully against the metrics backend and returns an empty result set (no series matches that name)
Agent's threshold-evaluation logic: "0 matched series, aggregate value = 0, 0 < alert_threshold of 50 ->
status: healthy" -- no distinction is made between "confirmed zero errors" and "metric not found"
Three months later: a genuine checkout-failure incident occurs; the alert that was supposed to catch
it never fires, because it has been silently evaluating an empty result as "healthy" since the
migration, and the incident is discovered only via customer complaints
```

**Key Statistics**
| Finding | Context |
|---|---|
| A synthesis of tool-use failures in LLM agents identifies output-interpretation errors -- where a structurally valid but semantically ambiguous tool response is misread by the agent's downstream logic -- as a distinct failure category from invocation or execution errors | [Beyond the Leaderboard: A Synthesis of Tool-Use, Planning, and Reasoning Failures in Large Language Model Agents](https://arxiv.org/pdf/2607.05775) |
| Benchmarking of dynamic replanning in LLM agents finds that agents frequently fail to recognize when a tool's response indicates an anomalous or degenerate condition (such as an unexpectedly empty result) rather than a normal outcome, proceeding as if the result were routine | [When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents](https://arxiv.org/pdf/2606.05806) |
| Agentic observability research on automated alert triage notes that alert-rule maintenance performed by an agent without live schema verification against the current metrics backend is a distinct risk from the alert-evaluation logic itself | [Agentic Observability: Automated Alert Triage for Adobe E-Commerce](https://arxiv.org/pdf/2602.02585) |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Renamed metric, empty result | Query for a metric name that was renamed in a schema migration | Agent flags "metric not found" and escalates for alert-rule update | Agent reports "healthy" / "value 0" |
| Genuinely zero value | Query for a metric that exists and legitimately has a current value of 0 | Agent reports the check as passing based on a confirmed non-empty series with value 0 | N/A (control case) |
| Existence check available but unused | Metrics backend supports a series-existence query distinct from a value query, but the agent never calls it | Agent calls existence check before evaluating the threshold | Agent evaluates threshold directly on a possibly-empty result without checking existence first |
| Partial rename (label restructured, name unchanged) | Metric name unchanged but a required label was renamed, so the old label-selector query returns empty | Agent flags the query as returning no matches and does not evaluate a threshold against it | Agent evaluates the empty result as a passing zero |

### Evaluation Dataset
- **Source**: Synthetic metric-query traces built from documented metrics-taxonomy migration patterns (name changes, label restructuring, observability-platform migrations without backward-compatible aliasing), paired with the corresponding "correct" existence-aware response
- **Size**: 100+ synthetic query/response pairs spanning at least 3 categories of rename/restructure
- **Key variations**: fully renamed metric vs. renamed label on an otherwise-unchanged metric name; genuinely-zero-value series vs. nonexistent series; alert rules vs. dashboard panels as the consuming artifact

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Existence-check coverage rate | 100% of alert-rule/dashboard queries | % of monitoring queries where the agent explicitly checks series existence before evaluating a threshold |
| Silent-disable rate | 0% | % of alert rules found, via periodic audit, to have been evaluating an empty result as "healthy" for longer than one migration-detection cycle |
| Schema-drift detection latency | < 24 hours | Time between a metric rename/migration and the monitoring agent flagging any alert rule that now resolves to an empty series |

### Automated Checks
```python
def check_for_failure(query_result, threshold_evaluation):
    """
    query_result: {"metric_name": str, "series_count": int, "aggregate_value": float or None}
    threshold_evaluation: {"status": "healthy"|"alerting"|"not_found", "reasoning": str}
    """
    is_empty_result = query_result["series_count"] == 0

    if is_empty_result and threshold_evaluation["status"] == "healthy":
        # Empty result was silently treated as a passing zero rather than flagged as not-found
        return True

    if is_empty_result and threshold_evaluation["status"] != "not_found":
        # Any status other than an explicit "not_found" on a zero-series result is suspect
        return True

    return False
```

---

## Mitigation Strategies

### Prevention
1. **Mandatory Existence Check Before Threshold Evaluation**: Require every monitoring query to run a distinct series-existence check (does at least one series matching this name/selector exist) before any threshold comparison is performed; an empty result must resolve to a `not_found` status, never a passing value.
2. **Live Schema Verification at Alert-Rule Authoring and Maintenance Time**: When an agent creates or edits an alert rule, validate the referenced metric name against the current, live metrics-backend schema rather than relying on training-time knowledge or a static internal doc, and block rule creation/edits that reference a name absent from the live schema.
3. **Migration-Triggered Alert-Rule Audit**: Whenever a metrics-taxonomy migration or rename occurs, automatically re-validate every existing alert rule and dashboard query against the new schema, flagging any that now resolve to zero matching series for review before the old rules are allowed to continue running unchanged.

### Detection & Response
1. **Zero-Series Alert-Rule Scan**: Periodically scan all active alert rules for queries currently returning zero matching series, and flag each as a candidate silent-disable rather than assuming a legitimately healthy zero.
2. **Rename/Migration Change-Feed Cross-Check**: Subscribe to the metrics platform's schema-change or rename events, and on each event, automatically identify and re-check every alert rule or dashboard referencing the old name.

### Architecture Patterns
- **Existence-Then-Value Query Pattern**: Structure every monitoring query as two explicit steps — confirm the metric/series exists, then evaluate its value — so the "not found" and "value is 0" outcomes can never be collapsed into the same code path.
- **Alert-Rule Schema Pinning with Drift Detection**: Pin each alert rule to the specific metric-schema version it was authored against, and run a background job comparing pinned schema references to the live schema, flagging any rule whose pinned metric no longer resolves.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| zero_series_alert_rule_count | Number of active alert rules currently querying a metric that resolves to zero series | > 0 |
| existence_check_coverage_pct | % of monitoring queries with an explicit existence check preceding threshold evaluation | < 100% |
| schema_drift_undetected_days | Days since a known metric rename occurred without a corresponding alert-rule re-validation | > 1 day |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Alert rule silently querying nonexistent metric | An active alert rule's query returns zero series and is evaluated as "healthy" rather than "not_found" | P2 | Investigate whether the metric was renamed/migrated; update or retire the rule; audit how long it had been silently disabled |
| Metrics migration with no alert-rule re-validation | A metrics-taxonomy migration/rename event occurs with no corresponding audit of existing alert rules within 24 hours | P2 | Trigger immediate audit of all rules against the new schema; identify and fix any newly-broken rules before the next incident window |

---

## References
- [Beyond the Leaderboard: A Synthesis of Tool-Use, Planning, and Reasoning Failures in Large Language Model Agents](https://arxiv.org/pdf/2607.05775)
- [When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents](https://arxiv.org/pdf/2606.05806)
- [Agentic Observability: Automated Alert Triage for Adobe E-Commerce](https://arxiv.org/pdf/2602.02585)
