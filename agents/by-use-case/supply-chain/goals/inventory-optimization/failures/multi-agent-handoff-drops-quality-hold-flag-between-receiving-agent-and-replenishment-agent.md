# Multi-Agent Handoff Drops Quality-Hold Flag Between Receiving Agent and Replenishment Agent

## Issue: A Receiving Agent That Notes, in Its Own Inspection Reasoning, That a Newly Received Lot Has Been Placed on Quality Hold Pending Inspection Hands Off Inventory Levels to a Replenishment Agent Through a Structured Available-to-Promise Field That Counts the Held Lot as Available, So the Replenishment Agent Treats Held Stock as Usable and Under-Orders Replacement Inventory

**Frequency**: Occasional

**Symptoms**
- The replenishment agent's reorder math counts the full 5,000-unit lot as usable stock as soon as it's received, even though the receiving agent's own inspection notes placed that same lot on hold pending supplier confirmation
- A lot rejected outright would eventually show up as a shortfall once removed from inventory entirely; the failure instead concentrates on partial holds, where a sampled 30% carton discrepancy puts a whole lot in limbo while the available-to-promise number never reflects any uncertainty
- The receiving agent's inspection reasoning is accurate and complete at the moment it's written -- the miss happens entirely in what does and doesn't carry into the replenishment agent's input
- Three days elapse between the hold being noted and the lot's formal rejection, during which the replenishment agent has already trimmed the next order on the assumption the held units were sellable
- A stockout against already-committed orders is the first sign anything went wrong, surfacing well after the under-ordering decision that caused it

**Root Cause**
Available-to-promise here is a single quantity -- on-hand minus committed -- a design built for stock that is simply present or absent, not for stock that is provisionally present pending a supplier's confirmation. The receiving agent's hold determination is a judgment call captured in its inspection notes, and the replenishment agent's reorder calculation reads the ATP number directly without checking whether any of the quantity behind it carries an open question, so a partial hold on part of a lot has nowhere to register a discount against the quantity it actually affects.

**Example**
```
Receiving agent inspects an incoming lot of 5,000 units and notes: "Visual inspection of sample shows inconsistent labeling on approximately 30% of cartons, placing full lot on quality hold pending supplier confirmation before release to usable inventory"
Receiving agent updates the structured inventory record with received_quantity: 5,000, with no corresponding field set to reflect the hold status
Replenishment agent calculates available-to-promise as on-hand quantity (which includes the held 5,000 units) minus committed orders, concluding stock is sufficient and reducing the next scheduled reorder
Lot fails supplier confirmation three days later and is fully rejected, removing 5,000 units from usable inventory that the replenishment agent had already counted as available
Resulting stockout affects committed orders that the reduced reorder was meant to cover
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems exhibit a documented failure category where a determination established by one agent is lost or never reaches a downstream agent's effective input, distinct from either agent reasoning incorrectly on its own | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Multi-agent consensus-seeking research in supply-chain contexts identifies structured state propagation between agents performing sequential supply-chain steps as a distinct reliability requirement from any single agent's task accuracy | [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184) |
| Generalist multi-agent system designs are shown to require explicit, structured task and constraint specification between agents, since narrative reasoning alone does not reliably propagate to a downstream agent acting on a fixed schema | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |

**Contributing Factors**
- The available-to-promise schema represents inventory as a single usable quantity with no field for quality-hold status or partial-lot holds
- The replenishment agent's reorder calculation consults only the structured ATP field, never the receiving agent's inspection transcript
- No reconciliation step compares hold-status language in the receiving agent's inspection notes against what the structured ATP field actually encodes before reorder calculations run

---

## Mitigation Strategies

1. **Structured Quality-Hold Field in Inventory Schema**: Extend the available-to-promise schema to carry an explicit, structured quality-hold quantity separate from usable on-hand quantity, and require the receiving agent to populate it directly from its own inspection determination
2. **Exclude Held Quantity From ATP Calculation by Default**: Require the replenishment agent's available-to-promise calculation to automatically exclude any quantity flagged with an active quality hold, rather than defaulting to treat all received quantity as usable
3. **Pre-Reorder Hold-Status Reconciliation Pass**: Before a replenishment agent calculates a reorder quantity, automatically scan the receiving agent's inspection transcript for hold-status language and flag any mismatch against the structured ATP field
4. **Time-Bound Hold Resolution Tracking**: Require every quality hold to carry an expected resolution date, and trigger automatic replenishment-agent re-evaluation if a hold remains unresolved past that date, rather than leaving it indefinitely counted as either available or unavailable by default

### Metrics
- Rate of reorder calculations where the receiving agent's inspection transcript contains hold-status language not reflected in the structured ATP field
- Rate of stockouts attributable to a quality-hold quantity being miscounted as available during replenishment calculation
- Time between a quality-hold determination and its reflection in the structured inventory record

### Alerts
- A replenishment calculation runs against an ATP figure that includes a quantity flagged with an active quality hold in inspection notes → P1
- A stockout occurs on an order that a reduced reorder calculation, based on a miscounted held lot, was meant to cover → P1
- Hold-status reconciliation mismatch rate exceeds the defined threshold for a rolling window → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
