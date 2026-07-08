# Side-Effect Misunderstanding

## Issue: Agent misses that a tool sends email, bills, deploys, or notifies.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Unexpected external side effect.
- [Add more specific symptoms]

**Root Cause**
Agent misses that a tool sends email, bills, deploys, or notifies.

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
1. **Side-Effect Metadata on Every Tool**: Each tool definition carries a machine-readable side-effect classification (`none`, `internal-write`, `external-notify`, `billing`, `deploy`) surfaced both to the agent's planning prompt and to the orchestrator, so tools that look like reads but have hidden notify/bill effects are explicitly labeled rather than assumed safe.
2. **Approval Gate for Externally-Visible Actions**: Tools tagged `external-notify`, `billing`, or `deploy` require an explicit pre-execution confirmation step (from the user or a policy check) before firing, regardless of how the agent framed its intent internally.
3. **Dry-Run/Preview Mode Default**: Where the underlying API supports it, side-effecting tools default to a dry-run or preview call first (e.g., "this would send an email to 40 recipients") and only execute for real after the agent or user explicitly confirms based on the preview.

### Detection & Response
1. **Unintended Side-Effect Audit Log**: All calls to tools tagged with non-`none` side effects are logged with full context (what triggered it, was it confirmed) to a dedicated audit stream; entries lacking a corresponding confirmation event are flagged for review.
2. **External Signal Correlation**: External side-effect indicators (emails sent, invoices generated, deploy events) are cross-referenced against agent session logs to catch cases where a side effect fired but wasn't reflected in the agent's stated plan or the user-facing transcript.
3. **Post-Hoc User Impact Sampling**: Sessions where a side-effecting tool executed are periodically sampled and checked (via user feedback or downstream system state) for whether the side effect was intended and expected by the user, not just technically successful.

### Architecture Patterns
1. **Side-Effect Classification Registry**: A central registry maps every tool to its side-effect category and blast radius (internal-only, single-user-external, multi-user-external, financial, infrastructure); the orchestrator consults this registry before every call to decide whether an approval gate applies.
2. **Two-Phase Commit for Notify/Bill/Deploy Actions**: High-blast-radius tools are split into a `prepare` call (returns a preview of what would happen) and a `commit` call (executes it), with the orchestrator requiring an explicit commit signal distinct from the initial tool selection.
3. **Blast-Radius-Aware Sandboxing**: In staging/test agent runs, side-effecting tools are automatically routed to sandboxed/mock endpoints (no real emails sent, no real charges) based on the same side-effect registry, so side-effect bugs are caught before touching production systems.

### Metrics
1. **unconfirmed_external_side_effect_count**: Target: 0; Alert threshold: > 0 per day
2. **side_effect_tool_classification_coverage_percent**: Target: 100% of tools tagged; Alert threshold: < 100%
3. **dry_run_to_commit_ratio**: Target: tracked per tool; Alert threshold: commit-without-preceding-dry-run rate > 5% for eligible tools
4. **post_hoc_unintended_side_effect_rate_percent**: Target: < 0.5%; Alert threshold: > 2%

### Alerts
1. **Unconfirmed High-Blast-Radius Action Fired** (P1 - Critical): Condition - a tool tagged `external-notify`/`billing`/`deploy` executed without a logged confirmation event. Action: Immediate incident, assess and communicate impact (recall email if possible, reverse charge), freeze the tool pending root-cause fix.
2. **Unclassified Tool Invoked** (P2 - Warning): Condition - a tool without a side-effect classification tag is called in production. Action: Block or route through manual approval by default until classified, notify tool owner.
3. **Dry-Run Bypass Detected** (P3 - Info): Condition - the commit-without-dry-run rate rises for a tool that supports preview mode. Action: Reinforce prompt/orchestrator logic requiring the preview-first flow.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Critical |

---

## References

- [OWASP-LLM-Top10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Note: LLM application risks including prompt injection, insecure output handling, supply chain, sensitive information disclosure, excessive agency.
