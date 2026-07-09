# No Improvement Audit

## Issue: Cannot explain what changed and why.

**Frequency**: Common

**Symptoms**
- No change rationale or source trace.
- [Add more specific symptoms]

**Root Cause**
Cannot explain what changed and why.

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
1. **Mandatory Change Record Schema**: Every prompt, model, tool, or policy change must be accompanied by a structured record before merge — trigger source (incident/feedback IDs), rationale, diff, eval evidence, approver, and rollback ID — enforced by the CI pipeline rather than left to author discretion.
2. **Immutable Audit Trail Enforcement**: Write change records to an append-only ledger; a deployment cannot proceed unless its record passes a completeness check, so an under-documented change is structurally blocked rather than merely discouraged by process.
3. **Change Review Checklist / Sign-off Gate**: Require a named reviewer to confirm the change record explains "why" (not just "what") before approval, with the checklist itself versioned so review rigor is consistent across reviewers and time.

### Detection & Response
1. **Audit Completeness Scanning**: Periodically scan deployed artifacts against the change ledger to confirm every production version has a matching, complete record; any deployed artifact without one is flagged as an orphan.
2. **Retroactive Change Reconciliation**: Run a scheduled sweep matching deployed artifact hashes to ledger entries to catch changes that bypassed the gate (e.g., hotfixes applied outside normal pipeline), surfacing gaps before they compound.
3. **Escalation on Untraceable Change**: When an orphan deployment or incomplete record is found, automatically open an incident requiring the responsible team to backfill rationale or justify the exception, rather than letting it pass silently.

### Architecture Patterns
1. **Change Ledger Service**: An append-only store keyed by change_id containing trigger_source, rationale, diff, eval_results, approver, and rollback_id, queryable by both the deployment pipeline and audit tooling.
2. **CI/CD Gate Requiring Audit Metadata**: A pipeline stage that queries the change ledger for a complete, linked record before allowing an artifact to be promoted; missing or incomplete metadata blocks deployment outright.
3. **Change-to-Outcome Dashboard**: A view linking each recorded change to the downstream metric/eval movement it produced, supporting retrospective analysis of which changes actually helped and enabling faster diagnosis when investigating a later regression.

### Metrics
1. **change_audit_completeness_percent**: Target: 100%; Alert threshold: < 95%
2. **orphan_deployment_count**: Target: 0; Alert threshold: any occurrence
3. **mean_time_to_locate_change_rationale**: Target: < 5 minutes (single ledger lookup); Alert threshold: > 1 hour (indicates missing/scattered records)
4. **change_records_missing_eval_evidence_percent**: Target: 0%; Alert threshold: > 5%

### Alerts
1. **Orphan Deployment Detected** (P1 - Critical): Condition - a production artifact exists with no matching change ledger record. Action: Freeze further deployments from that pipeline, require immediate backfill or rollback, investigate how the gate was bypassed.
2. **Incomplete Change Record Merged** (P2 - Warning): Condition - audit completeness scan finds a record missing rationale or eval evidence. Action: Require the author to backfill within a defined SLA, block that change from being cited as precedent until complete.
3. **Reconciliation Sweep Finds Drift** (P3 - Info): Condition - retroactive sweep finds a mismatch between deployed hash and ledger. Action: Investigate deployment path for bypass, update pipeline enforcement to close the gap.

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

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
