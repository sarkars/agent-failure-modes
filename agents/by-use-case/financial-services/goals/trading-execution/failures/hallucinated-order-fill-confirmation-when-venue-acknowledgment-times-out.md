# Hallucinated Order-Fill Confirmation When Venue Acknowledgment Times Out

## Issue: When an Execution Agent's Order-Routing Call to a Trading Venue Times Out Before Receiving a Fill Acknowledgment, the Agent Completes a Plausible "Order Filled" Result Instead of Treating the Missing Acknowledgment as an Unknown Order State, Leading the Position Ledger to Reflect a Fill That May Not Have Occurred

**Frequency**: Occasional

**Symptoms**
- An order is logged as "filled" in the position ledger for a routing attempt during which the venue's acknowledgment call actually timed out, with no fill confirmation actually received
- The execution agent's tool-call trace shows a timed-out or errored venue-acknowledgment request immediately followed by a fill-confirmation narrative consistent with a successful execution
- The order is later found, once the venue's actual order-status feed is checked, to have either not filled at all, partially filled, or filled at a different price than the agent's logged confirmation states
- Routing attempts that complete with a timed-out acknowledgment show the same "filled" outcome distribution as attempts backed by a genuinely received acknowledgment, when a timeout should instead produce a distinct "fill status unknown, pending venue confirmation" state
- The mismatch concentrates during periods of venue connectivity degradation or elevated order-flow volume, and a position discrepancy discovered later traces back to a routing attempt logged as filled despite no acknowledgment ever being received

**Root Cause**
When a venue-acknowledgment call times out, a language model generating the next step of an order-routing workflow has no inherent mechanism that forces it to treat the missing acknowledgment as terminal; absent an explicit instruction and control-flow branch for the timeout case, the model continues generating the most probable next output given the workflow's typical pattern, which is an affirmative "order filled" result rather than an explicit "fill status unknown" result. The model is not distinguishing "the venue confirmed the fill" from "no confirmation was ever received" unless the timeout is surfaced to it as a distinct state that blocks the fill-confirmation output.

**Example**
```
Execution agent routes a market order to a trading venue and waits for a fill acknowledgment
Acknowledgment call times out after the configured wait window is exhausted, returning no fill confirmation
Agent's next-step generation proceeds from the workflow's typical pattern as though the order filled normally, logging "order filled at limit price" in the position ledger and updating the portfolio's net position
Venue's order-status feed, queried independently ten minutes later, shows the order was in fact only partially filled before the connection dropped, with the remainder still resting on the book
Position ledger overstates the filled quantity until a reconciliation against the venue's order-status feed catches the discrepancy at end-of-day
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey taxonomies of LLM agent hallucination identify completion of a plausible result despite an upstream tool-call failure as a distinct hallucination category, separate from factual hallucination in open-domain generation | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds that agents frequently fail to differentiate a failed or erroring tool response from a successful one when generating the next step of a workflow, absent an explicit error-handling branch | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Research on agentic trading systems identifies reliance on point-in-time venue acknowledgments, without explicit handling for a failed or timed-out acknowledgment, as a documented gap distinct from the underlying execution-routing logic's accuracy | [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337) |

**Contributing Factors**
- No explicit control-flow branch distinguishes a timed-out venue acknowledgment from a successful one before the agent logs a fill-confirmation outcome
- The fill-confirmation log template is shared between the success path and any timeout path, so a timed-out acknowledgment produces the same "filled" entry as a genuinely confirmed execution
- No reconciliation job cross-checks logged "filled" orders against the venue's independent order-status feed to catch fills logged as confirmed without an actual acknowledgment

---

## Mitigation Strategies

1. **Hard-Stop on Acknowledgment Timeout**: Require the agent to treat any venue-acknowledgment timeout as a blocking event that prevents an "order filled" outcome from being logged, routing instead to a distinct "fill status unknown, pending venue confirmation" state
2. **Separate Unknown-State Log Entry**: Implement a distinct order-status history entry type for timed-out acknowledgments ("acknowledgment timeout, fill status pending verification") so a timeout cannot be logged identically to a confirmed fill
3. **Mandatory Status-Feed Query on Timeout**: Require an automatic query of the venue's independent order-status feed within a short window after any acknowledgment timeout, before the position ledger is updated
4. **Fill-Confirmation Reconciliation**: Run a continuous reconciliation job comparing every logged "filled" order against the venue's independent order-status feed, flagging any order logged as filled without a corresponding confirmed acknowledgment

### Metrics
- Rate of "filled" order log entries with no corresponding successful venue acknowledgment
- Venue-acknowledgment timeout rate, correlated against the rate of "filled" outcomes logged during the same window
- Time lag between an order routing attempt and the position ledger reflecting the venue's actual, independently confirmed fill status

### Alerts
- A "filled" order entry is logged with no corresponding successful venue acknowledgment → P1
- Venue-acknowledgment timeout rate exceeds the defined threshold for a rolling window while "filled" outcomes continue to be logged → P1
- An order is found, after an independent status-feed check, to have a fill status different from what the position ledger recorded → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
