# Multi-Agent Handoff Drops Promotion-Cancellation Update Before Demand-Forecast Run

## Issue: A Promotions-Planning Agent Communicates a Promotion's Cancellation or Shortened Duration in Free-Text Notes, but the Structured Promotional-Calendar Input Consumed by the Demand-Forecasting Agent Is Not Updated, So the Forecast Continues to Bake In Lift From a Promotion That Is No Longer Happening

**Frequency**: Occasional

**Symptoms**
- A demand forecast shows an expected sales lift aligned with a promotion's original dates, even though the promotions-planning agent's own notes record that the promotion was cancelled or cut short days earlier
- The structured promotional-calendar feed the forecasting agent queries still lists the original promotion as active, while the promotions agent's free-text planning log shows the cancellation decision and rationale
- Forecasts generated after a promotion-cancellation decision show no measurable change in projected lift for the cancelled promotion's SKUs and date range, compared to forecasts generated before the cancellation
- Inventory and staffing commitments sized to the forecast's promotional lift are made for a window in which no promotion is actually running, discovered only when realized demand comes in well below the forecast
- The mismatch concentrates on promotions cancelled or shortened after the promotional calendar was last synced to the forecasting agent's structured input, rather than on promotions cancelled before the calendar sync

**Root Cause**
The demand-forecasting agent's promotional-lift adjustment is driven entirely by the structured promotional-calendar feed it queries, and a promotions-planning agent's free-text decision to cancel or shorten a promotion has no effect on that feed unless the cancellation is explicitly propagated into the same structured calendar record the forecasting agent reads. Because the two agents' interaction happens through natural-language planning notes rather than a shared, continuously synced structured state, a cancellation decision made in one agent's context is invisible to the other agent's decision logic, even though both agents are reasoning over the same underlying promotional event.

**Example**
```
Promotions-planning agent decides three weeks before a planned discount event to cancel it due to a supplier cost increase, recording the decision and rationale in its free-text planning notes
Structured promotional-calendar feed used by the demand-forecasting agent is not updated, since the cancellation only exists in the planning agent's notes
Demand-forecasting agent runs its weekly forecast refresh, queries the still-active calendar entry, and applies the expected promotional lift to its SKU-level forecast
Inventory team receives the lift-adjusted forecast and increases purchase orders for the affected SKUs to cover the expected promotional demand
Realized demand during the original promotion window comes in at baseline, since no promotion ran, leaving the inventory team with a surplus sized to a promotion that never happened
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent consensus-seeking research in supply-chain contexts identifies the absence of a shared, continuously synced structured state between planning-stage agents as a distinct reliability gap from either agent's individual reasoning quality | [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184) |
| Surveys of multi-agent LLM system failures identify information loss at agent-to-agent handoff boundaries, where a decision made by one agent fails to propagate into the structured state a downstream agent consumes, as a recurring and distinct failure category | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Hybrid demand-forecasting research incorporating event knowledge for e-commerge contexts identifies stale or unsynced promotional-event metadata as a primary driver of forecast error distinct from baseline demand-model accuracy | [EventCast: Hybrid Demand Forecasting in E-Commerce with LLM-Based Event Knowledge](https://arxiv.org/html/2602.07695v1) |

**Contributing Factors**
- Promotions-planning agent's cancellation decisions are recorded only in free-text planning notes, with no automated propagation into the structured promotional-calendar feed
- Demand-forecasting agent's promotional-lift logic trusts the structured calendar feed as authoritative with no cross-check against the planning agent's most recent decision log
- No change-event mechanism notifies the forecasting agent (or triggers a forecast re-run) when a promotion referenced in an upcoming forecast window is cancelled or modified

---

## Mitigation Strategies

1. **Promotion-Cancellation Triggers Mandatory Calendar Sync**: Require any promotion-cancellation or duration-change decision recorded by the promotions-planning agent to immediately update the structured promotional-calendar feed before the decision is considered final
2. **Change-Event Triggered Forecast Re-Run**: Have the promotional-calendar feed emit a change event on any cancellation or modification, and automatically re-flag any in-flight demand forecast referencing that promotion's window for a fresh run
3. **Cross-Check Forecast Inputs Against Planning Decision Log**: Before finalizing a forecast that applies promotional lift, require a check of the promotions-planning agent's most recent decision log for the relevant promotion, not just the structured calendar feed
4. **Track Calendar-Sync Lag**: Continuously measure the time lag between a promotion-cancellation decision being recorded and the structured calendar feed reflecting it, and between the calendar update and any affected forecast being re-run

### Metrics
- Rate of demand forecasts that apply promotional lift for a promotion subsequently found to have been cancelled before the forecast's reference date
- Time lag between a promotion-cancellation decision and the structured calendar feed update
- Inventory or staffing variance attributable to forecasts built on a stale (not-yet-cancelled) promotional-calendar entry

### Alerts
- A demand forecast applies promotional lift for a promotion the planning agent's decision log shows as cancelled prior to the forecast's run time → P1
- Calendar-sync lag between a cancellation decision and the structured feed update exceeds the defined SLA → P2
- An in-flight forecast referencing a promotion is not re-flagged for re-run within the defined window after that promotion's calendar entry changes → P2

---

## References

- [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184)
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [EventCast: Hybrid Demand Forecasting in E-Commerce with LLM-Based Event Knowledge](https://arxiv.org/html/2602.07695v1)
