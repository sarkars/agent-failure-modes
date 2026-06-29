# Onboarding Agent Notifies Manager of Background-Check Clearance Without Verifying Source Status

## Issue: An Onboarding Agent Responsible for Notifying a New Hire's Manager When Pre-Employment Screening Steps Clear -- So the Manager Can Authorize Systems Access and a Start-Date Confirmation -- Sends the "Background Check Cleared, Access Approved" Notification Based on the Screening Step Simply No Longer Appearing in the Agent's Outstanding-Tasks List, Without Re-Querying the Background-Check Vendor's API for the Actual Current Status Field, and the Step Had In Fact Moved to "Pending Adjudication" Rather Than "Clear"

**Frequency**: Occasional

**Symptoms**
- Manager receives an access-approval notification and provisions systems access before the background check has actually cleared
- The agent's notification message states the check "cleared" with no citation of the specific status value or timestamp returned by the background-check vendor's API
- Re-querying the vendor API directly at the time of notification would have shown "pending adjudication," a distinct status from "clear" that the agent's task-list view did not surface as a separate state
- The same failure recurs specifically for candidates whose check enters adjudication, a minority status the agent's checklist-completion logic was not built to distinguish from a true clear
- Compliance review flags that the agent took an autonomous, access-granting-adjacent action (the notification triggers manager-initiated provisioning) without re-confirming the specific tool output it claimed to be reporting

**Example**
```
New hire's background check moves out of "in progress" in the vendor's tracking system
Agent's internal task tracker interprets "no longer in progress" as "complete," and renders
the onboarding checklist item as checked off
Agent sends manager: "Background check cleared for [candidate] -- you're clear to confirm
start date and request systems access"
Vendor's actual API status field reads "pending adjudication" (a flagged item requires
manual review before a final clear/no-clear determination), a status the agent never
explicitly queried or quoted before sending the notification
Manager requests access provisioning; IT grants it
Three days later the adjudication step resolves; HR discovers access was granted before
the check was genuinely clear and has to retroactively audit what the new hire touched
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey work on LLM-agent hallucination documents agents asserting a status or outcome as confirmed when the underlying evidence available to them was incomplete or did not actually state that outcome | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Research on miscalibration in tool-use agents finds that agents acting without verifying tool outputs exhibit a "confidence dichotomy" -- expressing high confidence in a reported status without it being validated against the actual returned value, especially for less-common status states the agent's logic does not distinguish | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Execution-provenance research argues every consequential autonomous action should be traceable to the specific tool output it claims to be grounded in, rather than to an internal task-list state derived secondhand from that output | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- Agent's checklist logic treats "no longer in progress" as a binary proxy for "cleared," collapsing distinct vendor status values (clear, pending adjudication, failed) into a single completed/not-completed state
- No requirement that an access-approval-triggering notification quote the literal status string and timestamp from the source API call rather than a derived checklist state
- Adjudication is a low-frequency status, so the collapsed-state logic passes testing on the common-case "clear" path and the gap is not caught before production
- The notification is treated as informational by the agent's own design, even though in practice it functions as the trigger for an irreversible action (access provisioning) once the manager acts on it

---

## Mitigation Strategies

1. **Quote-the-Source Requirement**: Require any notification that triggers access provisioning to include the literal status value and timestamp from the most recent vendor API call, not a derived checklist state
2. **Explicit Status Enumeration**: Replace the binary "in progress / not in progress" checklist logic with explicit handling of every status value the vendor API can return, including a defined behavior for adjudication and failure states
3. **Re-Query Before Notification**: Require the agent to make a fresh status call to the vendor API immediately before sending any clearance notification, rather than relying on a cached or task-list-derived state
4. **Provisioning Gate Tied to Verified Status**: Block the manager-facing notification template for "cleared" language unless the most recent API response's status field literally equals the vendor's defined "clear" value

### Metrics
- Rate of clearance notifications sent without a fresh, quoted API status call in the same task execution
- Number of access-provisioning actions later found to precede a true vendor "clear" status
- Mean time between a background-check status change and the agent's notification reflecting it accurately

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Clearance notification without quoted status | Notification sent containing "cleared" language with no literal API status string in the triggering tool call | P1 | Recall/correct notification; re-verify with vendor before any access is granted |
| Adjudication-state mismatch | Vendor status is anything other than the defined "clear" value at notification time | P1 | Block notification; escalate to HR compliance review |
| Access granted pre-clearance | IT provisioning action logged before a verified "clear" status timestamp | P2 | Trigger retroactive access audit |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
