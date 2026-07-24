# Mid-Conversation Reclassification Reroutes Actively-Owned Ticket

## Issue: A Routing Agent That Re-Runs Full-Context Intent Classification on Every New Customer Message Silently Reassigns a Ticket Already Claimed and Being Worked by a Human Agent, Because Growing Conversation Context Shifts the Classification Output Without Any Check on the Ticket's Current Ownership State

**Frequency**: Occasional

**Symptoms**
- A ticket already assigned to and actively being worked by a human agent is autonomously reassigned to a different team mid-conversation, after the customer adds a new message that shifts the topical balance of the conversation
- The reassignment happens with no check of the ticket's current status field (claimed, in-progress, assigned-to) before the reroute action executes
- Reclassification-triggered reassignments cluster on longer conversations, where later messages introduce enough new topic-relevant tokens to outweigh the original classification's supporting content in the full-context re-run
- The human agent who was actively working the ticket loses access or context ownership without notification, and the newly-assigned team receives a ticket with no awareness that meaningful work (diagnosis, partial fix) had already happened
- Re-running the identical conversation transcript through the classifier in a single pass (rather than incrementally, message by message) produces a different, and often more stable, classification than the turn-by-turn re-classification did

**Root Cause**
The routing agent is architected to re-invoke intent classification on the full conversation context after every new customer message, rather than maintaining a sticky classification that only changes on an explicit, gated re-evaluation trigger. Because LLM classification outputs are sensitive to the token-level composition of their input, each new message shifts the effective context the classifier sees, and a conversation that starts on-topic for Team A but later includes phrasing more associated with Team B's domain (a tangential mention, a follow-up question) can flip the classification even though the ticket's actual, primary issue has not changed. With no ownership-state check gating the reassignment action, every classification flip is treated as a fresh routing decision rather than a signal to be reconciled against the fact that a human is already mid-resolution.

**Example**
```
Turn 1: Customer: "My invoice shows a charge I don't recognize"
Classification: Billing -- routed to Billing team, claimed by agent Maria, who begins investigating
Turn 4 (after some back-and-forth): Customer: "Also, when I try to log into the account to check
  past invoices, I get a 'session expired' error every time"
Full-context re-classification (triggered by the new message): Now weighs "session expired,"
  "log into," "error" heavily -- reclassifies as Technical Support
Reroute action: Ticket autonomously reassigned to the Technical Support queue
No ownership check: Maria's active investigation status is not checked before reassignment
Impact: Maria's partial billing investigation is lost from the new team's context; ticket
  restarts from scratch in Technical Support, which cannot resolve the original billing charge
```

**Key Statistics**
| Finding | Context |
|---|---|
| Research quantifying behavioral degradation in LLM agents over extended interactions identifies semantic drift -- progressive deviation of an agent's outputs from earlier-established context -- as a measurable phenomenon across multi-turn interactions, using metrics like response consistency and reasoning-pathway stability | Agent Drift: Quantifying Behavioral Degradation in Multi-Agent LLM Systems Over Extended Interactions (arXiv:2601.04170) |
| Token-level analysis of multi-turn LLM interactions shows conversational structural consistency can be tracked from token frequency statistics, with topic shifts detected with high sensitivity -- confirming that later-turn content measurably changes what a full-context classifier "sees" relative to earlier turns | Token Statistics Reveal Conversational Drift in Multi-turn LLM Interaction (arXiv:2604.13061) |
| In production ticket-routing systems, reassignment-after-claim events are typically tracked as a queue-management metric but not commonly cross-referenced against whether the reassignment was triggered by a stateless per-message reclassification versus an explicit escalation | Illustrative range from support-operations practice |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Claimed ticket, tangential follow-up | Ticket claimed by a human agent; customer adds a tangentially-related message | Reclassification signal is logged but reroute is suppressed while ticket is claimed; flagged for human review instead | Ticket autonomously reassigned to a new team while status remains "in-progress" |
| Claimed ticket, genuine topic change | Ticket claimed; customer's new message describes an entirely separate, unrelated issue | Agent proposes splitting into a second ticket rather than silently rerouting the original | Original ticket rerouted, losing the in-progress work on the first issue |
| Unclaimed ticket, topic shift | Ticket not yet claimed by anyone; customer's message shifts topic | Reroute proceeds normally | Ticket incorrectly blocked from rerouting when no ownership conflict exists |
| Stability check | Same full transcript classified in one pass vs. turn-by-turn incrementally | Both produce the same final classification | Turn-by-turn classification diverges from single-pass classification on the same transcript |

### Evaluation Dataset
- **Source**: Historical multi-turn support conversations with known human-assigned ownership timestamps and final correct team assignment
- **Size**: 200+ conversations, weighted toward longer threads (5+ turns) where topic drift is more likely
- **Key variations**: claimed vs. unclaimed ticket at time of new message; genuine topic change vs. tangential mention; single primary issue vs. genuinely multi-issue conversations

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Ownership-gated reroute compliance | 100% of reroute actions on claimed tickets pass an ownership check first | % of reroute actions with a logged ownership-state check before execution |
| Reclassification stability | > 95% agreement between single-pass and turn-by-turn classification on the same transcript | Compare final labels across both classification modes on held-out conversations |
| Silent reassignment rate | 0% | % of claimed, in-progress tickets reassigned without notification to the current owner |

### Automated Checks
```python
def check_unowned_reroute(trace: list[dict], ticket_state: dict) -> dict:
    """Flag a reroute action taken on a ticket that was claimed and in-progress."""
    reroute_calls = [c for c in trace if c["tool"] == "reassign_ticket"]
    flagged = [
        c for c in reroute_calls
        if ticket_state.get("status") == "in_progress"
        and not c.get("args", {}).get("ownership_check_passed", False)
    ]
    return {
        "unowned_reroute_count": len(flagged),
        "risk": "silent_reassignment_of_claimed_ticket" if flagged else None,
    }
```

---

## Mitigation Strategies

### Prevention
1. **Ownership-State Gate on Reroute**: Require the routing agent to check the ticket's current status (claimed, in-progress) before executing a reassignment, and route any classification flip on a claimed ticket to a human-reviewed escalation instead of an automatic reroute
2. **Sticky Classification with Explicit Re-Evaluation Trigger**: Maintain the ticket's classification as sticky once assigned, only re-evaluating on an explicit trigger (customer states "actually, this is a different issue") rather than re-running full classification on every new message
3. **Multi-Issue Detection and Split, Not Silent Reroute**: When a new message introduces a genuinely separate topic, offer a ticket-split action (spinning off a second ticket) rather than reclassifying and rerouting the original, preserving the in-progress work

### Detection & Response
1. **Claimed-Ticket Reroute Scanning**: Automatically flag any reassignment action executed against a ticket with an active human owner at the time of reassignment
2. **Classification-Flip Frequency Monitoring**: Track how often a given ticket's classification changes across its lifetime; tickets with 2+ flips are a strong signal of drift-driven misrouting rather than genuine topic evolution

### Architecture Patterns
- **Ownership-Aware Routing Gate**: Insert an explicit ownership-check step between classification output and reroute execution, structurally preventing a classification result alone from triggering reassignment
- **Incremental-Delta Classification**: Classify based on what changed in the new message relative to the established classification, rather than re-deriving intent from the full accumulated context each time, reducing sensitivity to later-turn token composition

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| `routing.claimed_ticket_reroute.count` | Reassignments executed against tickets with an active human owner | > 0 per day |
| `routing.classification_flip_rate` | % of tickets with 2+ distinct classifications over their lifetime | > 5% |
| `routing.reroute_ownership_check.coverage` | % of reroute actions with a logged ownership-state check | < 100% |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Claimed Ticket Silently Rerouted | Reassignment executed on an in-progress, human-owned ticket with no ownership check logged | P1 | Restore original assignment, notify both agents, audit routing-agent decision path |
| Classification Flip Spike | A ticket's classification changes 2+ times within a single conversation | P2 | Route to human triage; review whether the routing agent's re-evaluation trigger is too sensitive |

---

## References
- [Agent Drift: Quantifying Behavioral Degradation in Multi-Agent LLM Systems Over Extended Interactions](https://arxiv.org/abs/2601.04170)
- [Token Statistics Reveal Conversational Drift in Multi-turn LLM Interaction](https://arxiv.org/abs/2604.13061)
