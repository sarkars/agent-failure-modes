# Post-Liquidation State Blindness in Margin Call Resolution

## Issue: An Agent Resolving a Margin Call Through a Multi-Step Tool-Calling Sequence Continues Reasoning About Remaining Liquidation Needs Using the Account Equity and Margin-Usage Figures It Read Before Its Own Preceding Sell Order Executed, Rather Than Re-Fetching Current State After Its Own Action Changed It

**Frequency**: Occasional

**Symptoms**
- An agent resolving a margin deficit executes a first liquidation leg, then computes the remaining shortfall using the account equity or margin-usage figure it read at the start of the reasoning chain, not the updated figure that its own completed sell order produced
- The agent over-liquidates: a second or third sell leg is sized to close a shortfall that the first leg already fully or partially resolved, because the agent's running mental model of the account was never refreshed after its own action
- The discrepancy is not caused by market movement, another trader's activity, or a stale cache with measurable replication lag — the account state changed because of the agent's own preceding tool call within the same reasoning chain, and nothing external touched the account in between
- Re-querying account state immediately before sizing each subsequent liquidation leg (rather than reusing the value computed at the start of the chain) eliminates the over-liquidation entirely, confirming the issue is a self-caused stale reference rather than a data-freshness problem
- The pattern recurs specifically in multi-leg, single-session resolutions (margin calls, multi-tranche order amendments, sequential rebalancing to a target exposure) where the agent's own actions are the dominant driver of the very state it needs to keep re-reading

**Root Cause**
In a chained tool-calling reasoning loop, an LLM agent typically treats the values it read earlier in its own chain of thought as durable facts to reason forward from, rather than as observations that expire the moment a mutating action is taken. When the agent calls a sell-order tool that itself changes account equity and margin usage, the return value of that tool call (an order confirmation) does not automatically propagate back into the agent's running belief about the account's overall state — the agent has to explicitly issue a new state-read tool call to learn what its own action changed. Because chaining a read-after-write step is not enforced by the tool-calling framework and adds a visible extra step to the reasoning trace, the model frequently continues from the pre-action snapshot it already has in context, especially when the task appears to be a single continuous calculation ("resolve the margin call") rather than a sequence of independent state-dependent decisions. This differs from generic cache or replica staleness (no external system lagged behind ground truth) and from a hidden shared-state leak affecting an unrelated tool (the very same resource the agent is reasoning about was directly and knowingly mutated by the agent's own preceding call).

**Example**
```
Scenario: Account is $40,000 below the maintenance margin requirement; agent is authorized to liquidate positions to resolve the call
Step 1: Agent reads account state -> equity: $180,000, margin deficit: $40,000
Step 2: Agent sells Position A (largest concentrated holding) -> execution confirms $45,000 in proceeds, deficit fully resolved
Step 3: Agent's next reasoning step computes "remaining deficit" using the Step 1 deficit figure ($40,000) rather than re-querying post-sale account state, and treats the $40,000 as still outstanding because the Step 2 confirmation payload reported trade details (price, quantity, proceeds) but not the account's updated margin-deficit figure
Step 4: Agent sells Position B to cover the "remaining" $40,000 deficit it believes still exists
Result: Account is over-liquidated by roughly $45,000 beyond what was required to satisfy the maintenance call, forcing an unplanned sale and unwinding a position the client had no intention of exiting that day
Impact: Client's position in B is liquidated unnecessarily, realizing taxable gains and losses the client did not choose to trigger, and the desk must explain an execution that no risk rule actually required
```

**Key Statistics**
- Reviews of agentic trading and execution systems identify a gap between an agent's perceived account/position state and the account's actual state as a distinct, under-tested failure surface, separate from strategy quality or market-data freshness
- Architectural analyses of agent-driven financial execution find that systemic risk in these systems depends heavily on how tightly agent decision loops are coupled to authoritative state, with looser read-after-write coupling associated with a higher rate of self-inconsistent multi-step actions
- Multi-step, tool-chained agent tasks show measurably higher error rates as the number of sequential state-dependent actions grows, particularly when an intermediate action's own side effects are not automatically re-surfaced to the reasoning step that follows it

---

## Mitigation Strategies

1. **Mandatory Read-After-Write for State-Mutating Actions**: Require the agent to issue a fresh account-state query immediately after any action known to mutate account equity, margin usage, or position size, before any subsequent sizing decision may be computed.
2. **Tool-Level State Injection on Mutation**: Have order-execution tools return the account's updated margin/equity figures directly in the execution-confirmation payload, so the current state is available without depending on the agent remembering to re-query it.
3. **Chain-of-Thought Staleness Guard**: Structurally invalidate any account-state values captured earlier in the same reasoning chain once a mutating tool call has been issued, forcing the agent's next calculation to cite only post-mutation values.
4. **Liquidation Sizing Reconciliation Check**: Before executing any liquidation leg beyond the first, run an automated check comparing the agent's stated "remaining deficit" against an independently computed current deficit from authoritative account state, and block the leg on mismatch.

### Metrics
- Rate of multi-leg liquidation or amendment sequences where a later leg's sizing input does not match a fresh state query taken after the prior leg
- Over-liquidation amount (value liquidated beyond the minimum required to resolve the original deficit) per margin-call resolution
- Read-after-write compliance rate for state-mutating actions in multi-step sequences

### Alerts
- A liquidation leg's stated "remaining deficit" is computed from an account-state read that predates a prior liquidation leg in the same sequence → P1
- Total liquidated value in a single margin-call resolution exceeds the original deficit by more than a small execution-slippage tolerance → P1

---

## Related Patterns
- [Fill-Confirmation Status Trusted Without Diffing Against Submitted Order Intent](./fill-confirmation-status-trusted-without-diffing-against-submitted-order-intent.md) — related failure to reconcile a tool's confirmation payload against ground truth, but there the mismatch originates upstream rather than from the agent's own uncaptured side effect
- [Market-Impact Blindness in Trading Execution](./market-impact-blindness.md) — related execution-sizing failure where the agent's own prior actions are the un-modeled variable
- [Context Refresh Stale State](../../../../../cross-cutting/operations/goals/memory-management/failures/context-refresh-stale-state.md) — related stale-state mechanism, but driven by a lagging external read path rather than the agent's own unpropagated action

## References

- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
- [AI Agents in Financial Markets: Architecture, Applications, and Systemic Implications](https://arxiv.org/html/2603.13942v2)
