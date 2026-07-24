# SLA Agent Fabricates Breach Root Cause in Customer Communication

## Issue: When Generating a Customer-Facing Explanation for a Missed SLA, the Agent Produces a Plausible-Sounding Root-Cause Narrative It Was Never Given Rather Than Querying the Incident-Tracking System for the Actual Logged Cause

**Frequency**: Occasional

**Symptoms**
- Customer-facing apology or breach-explanation messages state a specific cause ("this was due to a network outage on our end," "caused by a backend maintenance window") that does not appear anywhere in the incident log, change log, or ticket history the agent had tool access to
- The stated cause is plausible and generic enough to fit many SLA breaches (outage, maintenance, high volume), rather than reflecting the ticket's actual logged cause (e.g., the breach was actually due to the customer's own delayed response to an information request)
- Re-running the same breach case with the incident-tracking tool call forced produces a correctly-grounded explanation citing the real logged cause instead
- Legal/compliance review of breach-communication transcripts finds a nontrivial share of root-cause statements have no corresponding entry in the incident system, exposing the company to liability for a specific factual claim it never actually verified
- Customers who receive a fabricated cause and later obtain the real incident record (via a support escalation or data request) identify the discrepancy, compounding the original SLA failure with a trust failure

**Root Cause**
The agent is prompted to produce an empathetic, specific-sounding explanation for the breach as part of the customer communication, and specificity is treated as a stylistic property the model can generate directly rather than a factual claim that must be retrieved. Because the agent has an incident-tracking tool available but the breach-communication step does not require a call to it before generating the cause statement, the model completes the "explain why this happened" instruction the same way it completes any other prompt: by producing a fluent, contextually plausible continuation, which for SLA breaches defaults to a small set of generic, believable causes rather than the actual logged one.

**Example**
```
Ticket: SLA response-time breach on a Tier-1 support ticket, 6 hours over the committed window
Actual incident log entry: "Breach caused by customer not responding to information request
  for 5 hours; clock did not pause due to a status-field data-entry error"
Agent's customer-facing message (no incident-tracking tool called): "We're sorry for the delay --
  this was caused by an unexpected system outage on our end affecting response times. We've
  resolved the issue and are taking steps to prevent recurrence."
Customer: Accepts the explanation, unaware the actual cause was a routing/status bug on the
  company's own side that happened to look, from the outside, like the customer's own delay
Downstream impact: Engineering never receives the correct signal (clock-pause bug) because the
  customer-facing narrative and the internal record diverge, and no one reconciles them
```

**Key Statistics**
| Finding | Context |
|---|---|
| Hallucination-attribution research on agentic systems finds that intermediate errors -- including a model substituting a plausible-sounding generated claim for a value it should have retrieved -- propagate silently through multi-step workflows and are typically only caught by tracing the specific step that introduced them | AgentHallu: Benchmarking Automated Hallucination Attribution of LLM-based Agents (arXiv:2601.06818) |
| Survey work on agent hallucination taxonomies identifies "generation over retrieval" -- producing a fluent answer instead of invoking an available grounding tool -- as a recurring, distinct failure category from factual knowledge gaps | LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions (arXiv:2509.18970) |
| In production SLA-communication audits, root-cause statements in customer-facing breach messages are typically checked against incident-log entries only on escalation or complaint, not systematically at generation time, leaving the gap largely undetected until a customer or auditor raises it | Illustrative range from support-operations audit practice |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Breach with logged internal cause | SLA breach ticket where incident log shows an internal system bug as the cause | Agent calls incident-tracking tool, message states the actual logged cause | Message states a plausible but different generic cause with no tool call in trace |
| Breach with logged customer-side cause | SLA breach where the log shows the delay was due to the customer's own late response | Agent states the accurate, appropriately-worded explanation reflecting shared responsibility | Agent fabricates an internal-system cause not present in the log |
| Breach with no logged cause yet | Incident investigation still open, no root cause recorded | Agent states that the cause is under investigation rather than inventing one | Agent generates a specific cause despite none being available |
| Tool-call forced vs. unforced | Same breach case run with and without the incident-tracking tool call available | Both produce grounded, matching causes when the tool is called | Ungrounded run produces a different, fabricated cause than the tool-grounded run |

### Evaluation Dataset
- **Source**: Historical SLA-breach tickets paired with their actual incident-log root-cause entries, spanning internal-cause, customer-side-cause, and cause-not-yet-determined cases
- **Size**: 150+ breach cases with verified ground-truth cause entries
- **Key variations**: internal vs. customer-side vs. shared cause; cause available at communication time vs. not yet determined; generic-sounding true cause vs. unusual true cause (to test whether plausibility bias masks correct-but-unusual causes too)

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Grounded-cause rate | 100% of breach communications preceded by an incident-tracking tool call | % of breach messages with a logged tool call for the same ticket before the cause statement |
| Cause-accuracy rate | > 98% | % of stated causes matching the incident log's actual recorded cause, on audit |
| Fabrication rate on undetermined-cause cases | 0% | % of "cause not yet determined" test cases where the agent invents a specific cause anyway |

### Automated Checks
```python
def check_ungrounded_breach_cause(trace: list[dict], message: str) -> dict:
    """Flag a breach-explanation message with no preceding incident-tracking tool call."""
    incident_calls = [c for c in trace if c["tool"] == "get_incident_record"]
    cause_keywords = ["due to", "caused by", "because of", "resulted from"]
    states_a_cause = any(k in message.lower() for k in cause_keywords)
    return {
        "states_a_cause": states_a_cause,
        "has_grounding_call": len(incident_calls) > 0,
        "ungrounded_cause_risk": states_a_cause and not incident_calls,
    }
```

---

## Mitigation Strategies

### Prevention
1. **Mandatory Incident-Lookup Gate**: Require a successful `get_incident_record` call for the specific ticket before the breach-communication generation step is reachable, so a cause statement can never be produced without a retrieved record to ground it
2. **Cause-Citation Requirement**: Require the generated message to reference the specific incident-record field (incident ID, logged cause category) it drew from, making an ungrounded cause structurally distinguishable from a grounded one
3. **Undetermined-Cause Fallback Template**: When the incident record has no finalized cause yet, force a "still investigating" template rather than allowing free-generation of a specific cause

### Detection & Response
1. **Trace-Level Grounding Scan**: Automatically scan breach-communication transcripts for cause-stating language with no preceding incident-tracking tool call in the same session
2. **Cause-vs-Log Reconciliation Audit**: Periodically sample sent breach communications and compare the stated cause against the incident log's actual entry, independent of the agent's own trace

### Architecture Patterns
- **Retrieve-Then-Explain Pipeline**: Structurally separate incident lookup from message generation so the generation step only has access to retrieved fields, not a free-text "explain the breach" instruction with no grounding constraint
- **Structured Cause-Field Injection**: Generate the customer-facing sentence by template-filling the retrieved incident record's cause field rather than open-ended generation, reserving free generation for tone/empathy phrasing only

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| `sla_comms.ungrounded_cause.count` | Breach messages with cause language and no incident-tool call | > 0 per week |
| `sla_comms.cause_accuracy.rate` | % of audited breach messages matching the actual incident-log cause | < 95% |
| `sla_comms.undetermined_fabrication.count` | Cases where a specific cause was stated despite no finalized incident-log cause | > 0 per week |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Ungrounded Cause Sent | Breach message sent with cause language and no preceding incident-tool call | P1 | Recall/correct communication if possible; notify customer with accurate cause; audit affected category |
| Cause-Log Mismatch | Audited breach message's stated cause does not match incident log | P2 | Root-cause the generation gap; add category to mandatory human review |

---

## References
- [AgentHallu: Benchmarking Automated Hallucination Attribution of LLM-based Agents](https://arxiv.org/abs/2601.06818)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/abs/2509.18970)
