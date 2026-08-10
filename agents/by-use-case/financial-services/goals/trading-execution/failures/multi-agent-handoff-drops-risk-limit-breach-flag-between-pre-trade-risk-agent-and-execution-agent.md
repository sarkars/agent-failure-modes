# Multi-Agent Handoff Drops Risk-Limit-Breach Flag Between Pre-Trade Risk Agent and Execution Agent

## Issue: A Pre-Trade Risk Agent Notes in Free Text That an Order, Combined With Existing Positions, Would Push a Concentration or Leverage Limit Into a Marginal Breach Under a Plausible Adverse Price Move, but the Structured Pre-Trade Check Result Handed Off to the Execution Agent Has Only a Pass/Fail Field on Static Current-State Limits, So the Execution Agent Routes the Order as Clear

**Frequency**: Occasional

**Symptoms**
- An order is routed and executed as risk-clear, even though the pre-trade risk agent's own notes flagged that the order, combined with existing positions, would put a concentration or leverage limit into marginal breach under a plausible adverse price scenario
- The structured pre-trade check result handed off to the execution agent contains only a pass/fail field against current static limit calculations, with no field for a scenario-conditional or marginal-breach finding the risk agent's free-text analysis raised
- Execution agents operating purely from the structured pass/fail field show a materially higher routing rate on orders with a noted marginal-breach scenario than execution agents given the risk agent's full scenario-analysis transcript
- The marginal breach becomes an actual breach within the same trading session when the flagged adverse price move occurs, and is only then traced back to the risk agent's pre-trade note that the execution agent's structured input never carried
- Orders that are comfortably clear of every limit even under an adverse scenario rarely surface this, because a simple pass/fail check and a scenario-conditional check would agree anyway; the gap only bites at the 104%-of-limit margin, where the two checks disagree

**Root Cause**
The pass/fail field on the pre-trade check result answers a single question -- is the order within limit right now -- because that is what a static, point-in-time risk calculation produces. The risk agent's 3%-adverse-move finding answers a different question entirely, one the schema was never built to hold a field for, so writing "pass" for the current-state check and noting the scenario conditionally in free text are both correct within their own terms; nothing in the handoff forces those two answers to be reconciled before the execution agent sees only the former. The execution agent's routing logic then has a single boolean to act on and no reason to suspect a second, scenario-qualified answer exists elsewhere in the risk agent's output.

**Example**
```
Pre-trade risk agent evaluates a new order against a single-name concentration limit and notes in free text: "Order passes current-state concentration check, but combined with existing position, a 3% adverse move in the underlying would push concentration to 104% of the limit"
Risk agent records a "pass" in the structured pre-trade check result, since the static current-state calculation is within limit
Structured result handed off to the execution agent shows a clean pass, with no field for the scenario-conditional marginal-breach finding
Execution agent routes and fills the order without escalation
Underlying moves adversely by 3% later that session, pushing the position into an actual concentration-limit breach that risk-reporting only discovers at end-of-day reconciliation
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of multi-agent LLM system failures identify narrow handoff interfaces between staged agents, where a downstream agent's structured input omits a finding an upstream agent's free-text reasoning surfaced, as a distinct and recurring failure category | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Platform-orchestrated agentic workflow failure studies find that narrowing the interface between orchestrated stages to a fixed pass/fail schema is a primary mechanism by which a scenario-conditional or marginal finding present upstream fails to reach a downstream execution stage | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |
| Research on agentic trading systems identifies the absence of a shared, scenario-aware structured state between sequential risk-check and execution stages as a distinct reliability gap from either stage's individual calculation accuracy | [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337) |

**Contributing Factors**
- Structured pre-trade check schema captures only a pass/fail outcome against static current-state limit calculations, with no field for a scenario-conditional or marginal-breach finding
- Risk agent's scenario analysis is recorded only in free-text notes, with no structured escalation path into the execution agent's input
- No mandatory hold or escalation is triggered in the execution workflow when the risk agent's free-text notes contain marginal-breach or scenario-conditional language, since the execution agent's logic does not parse those notes

---

## Mitigation Strategies

1. **Add a Scenario-Conditional Risk Field to the Handoff Schema**: Require the pre-trade risk agent to record any marginal-breach or scenario-conditional finding in a dedicated structured field passed to the execution agent, rather than leaving it only in free-text scenario-analysis notes
2. **Execution Agent Cross-Checks Risk Transcript for Marginal-Breach Language**: Require the execution agent to scan the risk agent's free-text notes for marginal-breach or scenario-conditional language before routing an order as fully clear, not just the structured pass/fail field
3. **Mandatory Escalation on Near-Threshold Orders**: Automatically route any order the risk agent's scenario analysis flags as approaching a limit threshold under a plausible adverse move to a human risk-desk review before execution, regardless of its current-state pass/fail status
4. **Track Conditional-Field-Absent Routing Rate**: Continuously measure how often an order with a noted marginal-breach scenario is nonetheless routed as clear when the handoff schema lacked a conditional-risk field

### Metrics
- Rate of order executions where the pre-trade risk transcript contains marginal-breach or scenario-conditional language not reflected in a structured conditional-risk field
- Time between an order execution and a same-session actual limit breach traced back to a flagged-but-unescalated scenario finding
- Routing rate for near-threshold orders, segmented by presence vs. absence of a structured scenario-conditional field in the handoff

### Alerts
- An order executes while the pre-trade risk transcript contains unresolved marginal-breach language with no structured conditional-risk flag → P1
- An actual limit breach occurs within the same session following a previously flagged-but-unescalated scenario-conditional finding → P1
- Conditional-field-absent routing rate across a rolling window exceeds the defined threshold → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
