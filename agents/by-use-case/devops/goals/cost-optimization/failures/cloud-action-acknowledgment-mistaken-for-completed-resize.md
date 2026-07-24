# Cloud API Acknowledgment Mistaken for Completed Resize/Termination

## Issue: Cost-Optimization Agent Reports an Autonomous Resize or Termination as Successful Based on the Cloud API's Synchronous "Request Accepted" Response, Without Polling the Resource's Actual Post-Action State

**Frequency**: Occasional

**Symptoms**
- Agent logs "resized instance-4471 to a smaller type, saving $340/month" immediately after the cloud provider's resize API returns `202 Accepted`, with no subsequent call to confirm the instance actually came back up at the new size
- A termination call against a resource with deletion protection enabled, or with an attached load balancer/elastic IP blocking teardown, still returns an accepted/queued response; the async worker that actually processes the request fails minutes later, but nothing in the agent's flow ever re-checks that outcome
- Weekly billing-export reconciliation shows spend for a "terminated" resource continuing unchanged, while the agent's own action log and cost-savings dashboard both show the termination as complete
- Engineers discover a resource the agent reported as terminated is still running only when they encounter it during unrelated troubleshooting, capacity review, or a manual billing audit
- The gap concentrates on operations with a distinct async failure path from the one that authorized the initial call — e.g., an IAM policy permits the resize request itself but blocks the async worker's follow-up step, a failure mode invisible to anything that only checks the initial call's response code

**Root Cause**
Cloud provider control planes for resize and termination operations are typically asynchronous: the synchronous API response confirms only that a request was accepted and queued, not that the underlying operation completed or even that it will succeed. Actual success or failure is determined afterward by an async worker and is exposed solely through a separate state-polling call or event notification. A cost-optimization agent whose action-reporting logic branches on "did the API call throw an error" rather than "does the resource's current state match the intended post-action state" has no mechanism to detect the class of failures that occur strictly after acceptance — termination-protection blocks, dependent-resource conflicts, quota errors on the async path, or async-step permission gaps distinct from the synchronous call's own authorization.

**Example**
```
Cost-optimization agent identifies ec2-instance-4471 as underutilized, issues a terminate-instance
call as part of a nightly cleanup run
Cloud API response: 200 OK, {"terminatingInstances": [{"instanceId": "i-4471", "currentState": "shutting-down"}]}
Agent logs: "Terminated i-4471, projected savings $340/month" and marks the cleanup task complete
Actual outcome: i-4471 has termination protection enabled from a prior manual safeguard; the async
teardown worker rejects the request 90 seconds later and reverts the instance to "running"
Agent never issues a follow-up state check, so this reversal is never observed
Two weeks later: monthly billing review shows i-4471 still accruing full charges; the agent's own
"cost savings realized" report for the period is overstated by the full $340, and the underlying
underutilization the cleanup was meant to fix is still unaddressed
```

**Key Statistics**
| Finding | Context |
|---|---|
| Runtime verification research on governed AI agent actions finds that supervisory requirements increasingly apply to whether an agent's claimed action matches what actually occurred in the environment, not just whether the initiating call succeeded | [Proof of Execution: Runtime Verification for Governed AI Agent Actions](https://arxiv.org/html/2607.05397) |
| Execution-provenance research on LLM agents treats the gap between a tool call's immediate response and the eventual, ground-truth outcome of that action as a distinct accountability failure requiring dedicated evidence tracing, not just error-code checking | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Multi-agent CloudOps automation research identifies asynchronous cloud control-plane behavior as a structural source of agent action failures distinct from request-authorization failures, requiring explicit post-action state confirmation | [Engineering LLM Powered Multi-agent Framework for Autonomous CloudOps](https://arxiv.org/abs/2501.08243) |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Termination-protected resource | Terminate call against a resource with deletion protection enabled | Agent reports "termination blocked, protection flag active" after polling actual state | Agent reports "terminated" based only on the initial 202/200 response |
| Async worker permission gap | Resize call authorized by the caller's IAM role, but async resize-worker role lacks a required permission | Agent detects the resource never left its original instance type and reports failure | Agent reports "resized" without ever re-checking instance type |
| Dependent-resource block | Terminate call against an instance still referenced by an active load balancer target group | Agent detects the instance remains in "running" state and escalates | Agent reports savings realized while the instance keeps running |
| Genuinely successful action | Resize call against an unblocked, unprotected resource | Agent polls post-action state, confirms new instance type, then reports savings | N/A (control case; savings report should require polling to occur, not merely be correct by coincidence) |

### Evaluation Dataset
- **Source**: Synthetic cloud-action traces constructed from documented async failure modes of major cloud providers' compute/termination APIs (deletion protection, dependent-resource conflicts, IAM async-path permission gaps), combined with a sample of real "reported savings vs. actual billing" discrepancies pulled from cost-optimization audit logs
- **Size**: 150+ synthetic action traces spanning at least 4 async-failure categories, plus any available production discrepancy cases
- **Key variations**: synchronous-accept-then-async-success vs. synchronous-accept-then-async-failure; failure surfaced via polling vs. failure surfaced only via billing reconciliation; single-resource actions vs. batch cleanup runs where only a subset of actions in the batch fail post-acceptance

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Post-action state-verification rate | 100% of resize/terminate actions | % of autonomous cost actions followed by an explicit state-poll call before being logged as complete |
| False-completion rate | 0% | % of actions reported "complete" where the resource's polled state does not match the intended post-action state |
| Savings-report vs. billing-reconciliation discrepancy | < 1% of projected savings | Delta between agent-reported realized savings and actual billing-export spend for the same resources over the following billing cycle |

### Automated Checks
```python
def check_for_failure(action_log_entry, polled_state=None):
    """
    action_log_entry: {"resource_id": str, "action": "resize"|"terminate",
                        "api_response_status": "accepted"|"error", "reported_outcome": "success"|...}
    polled_state: {"resource_id": str, "current_type_or_state": str, "matches_intended": bool} or None
    """
    if action_log_entry["api_response_status"] != "accepted":
        return False  # a rejected call can't produce this failure

    if action_log_entry["reported_outcome"] == "success" and polled_state is None:
        # Reported success with no post-action verification call in the trace at all
        return True

    if polled_state is not None and not polled_state["matches_intended"]:
        # Verification was attempted but the actual state contradicts the "success" report
        if action_log_entry["reported_outcome"] == "success":
            return True

    return False
```

---

## Mitigation Strategies

### Prevention
1. **Mandatory Post-Action State Poll Before Success Reporting**: Require every autonomous resize/terminate action to be followed by an explicit poll of the resource's actual current state (instance type, lifecycle state, deletion-protection flag) before the agent is permitted to log the action as complete or record projected savings; a bare non-error API response is never sufficient on its own.
2. **Asynchronous-Outcome Timeout Gate**: For operations known to resolve asynchronously, require the agent to wait for and consume a definitive terminal state (or an explicit timeout-and-escalate path) rather than proceeding to the next queued action immediately after the synchronous accept.
3. **Separate Authorization Check for the Async Execution Path**: Where the platform distinguishes request-authorization permissions from async-worker execution permissions, validate both explicitly during pre-flight checks so an async-path permission gap is caught before the action is attempted, not discovered after a false "success."

### Detection & Response
1. **Savings-vs-Billing Reconciliation Job**: On each billing cycle, automatically compare agent-reported realized savings per resource against the actual billing export for that resource, and flag any resource where reported "terminated/resized" status does not match observed spend.
2. **Unverified-Action Audit**: Continuously scan the action log for any resize/terminate entry marked "success" with no corresponding post-action state-poll call in the trace, and treat every such entry as unverified until retroactively checked.

### Architecture Patterns
- **Verify-Then-Report Action Wrapper**: Wrap every cost-optimization action-executing tool call so the agent's "success" narration can only be generated after a required verification sub-call confirms the resource's actual state; unverifiable outcomes route to retry or human escalation instead of a success report.
- **Async Outcome Ledger**: Log every asynchronous cloud action to an append-only ledger with pending/verified/failed status; downstream cost-savings reporting reads only from entries marked verified, never from the initiating call's response alone.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| unverified_action_completion_rate | % of resize/terminate actions logged "success" without a post-action state poll | > 0% |
| false_completion_rate | % of verified actions where polled state contradicts the "success" report | > 1% |
| savings_billing_discrepancy_pct | Delta between reported realized savings and actual billing-export spend | > 5% for any resource |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Resize/terminate reported success without verification | An action is logged "complete" with no corresponding state-poll entry in the trace | P2 | Retroactively poll resource state; correct the savings report; block the agent from further unverified reporting until patched |
| Billing reconciliation mismatch | A resource marked "terminated"/"resized" shows unchanged billing spend in the following cycle | P1 | Manually verify resource state; re-issue the action or escalate to on-call; audit other actions from the same run |

---

## References
- [Proof of Execution: Runtime Verification for Governed AI Agent Actions](https://arxiv.org/html/2607.05397)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [Engineering LLM Powered Multi-agent Framework for Autonomous CloudOps](https://arxiv.org/abs/2501.08243)
