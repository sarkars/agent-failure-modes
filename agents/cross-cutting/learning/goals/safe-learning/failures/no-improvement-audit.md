# No Improvement Audit

## Issue: Cannot explain what changed and why.

**Frequency**: Common

**Symptoms**
- No change rationale or source trace.
- A prompt/policy update is live in production but no one can point to the incident, feedback batch, or eval result that motivated it, or which specific behavior it was supposed to fix.
- When a regression is later discovered, engineers cannot quickly determine which of several recent changes caused it because none of the changes have linked rationale or eval evidence.

**Root Cause**
Cannot explain what changed and why.

**Example**
```
A team notices the support agent's tone has shifted to be noticeably more apologetic over the past
quarter. Six prompt revisions were pushed in that period, each merged with a commit message like
"tune response style" and no linked feedback IDs, eval scores, or rationale. When a customer complains
that the new tone reads as insincere, nobody can determine which of the six changes introduced the
shift, whether it was a deliberate response to specific feedback, or whether any eval was run before
each change shipped -- so the team can't confidently roll back to a specific known-good version.
```

**Contributing Factors**
- Change record creation (rationale, trigger source, eval evidence) is optional/manual rather than enforced by the deployment pipeline.
- Hotfixes or urgent tuning changes are pushed outside the normal review process "just this once," bypassing the audit gate entirely.
- Commit messages and PR descriptions are treated as sufficient documentation even though they aren't linked to feedback IDs or eval results in a queryable ledger.
- No periodic reconciliation sweep exists to catch deployed artifacts that have no matching audit record.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Missing-rationale deployment attempt | Candidate deployment with a diff but no linked feedback ID, rationale, or eval evidence | CI gate blocks the deployment until the change record is complete | Deployment proceeds with an incomplete or empty change record |
| Orphan artifact detection | Production artifact hash with no matching entry in the change ledger (simulated bypass) | Reconciliation sweep flags the artifact as an orphan within one scheduled run | Orphan artifact remains undetected across multiple sweep cycles |
| Rationale lookup latency | Query for "why did behavior X change between version N and N+1" | Ledger returns the linked rationale, trigger source, and eval diff in a single lookup | Answering requires manually searching commit history/chat logs across multiple sources |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| change_audit_completeness_percent (eval) | 100% | Sample recent deployments and check for a complete linked change record |
| ci_gate_bypass_rate_percent | 0% | Audit deployment logs for artifacts that reached production without passing the audit-metadata gate |
| mean_time_to_locate_change_rationale (eval) | < 5 minutes | Time a reviewer performing a single ledger lookup to explain a given behavior change |

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
| orphan_deployment_count | any occurrence |
| change_audit_completeness_percent | < 95% |
| change_records_missing_eval_evidence_percent | > 5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Orphan Deployment Detected | a production artifact exists with no matching change ledger record | High |
| Incomplete Change Record Merged | audit completeness scan finds a record missing rationale or eval evidence | Medium |
| Reconciliation Sweep Finds Drift | retroactive sweep finds a mismatch between deployed hash and ledger | Low |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
