# Inherited Errors

## Issue: Agent Propagates Errors from Sources or Tools

**Frequency**: Common

**Symptoms**
- Tool returns incorrect data, agent passes it through
- Source document contains error, agent repeats it
- Upstream agent makes mistake, downstream agent doesn't catch it

**Root Cause**
Agents trust their inputs. If a tool, document, or another agent provides incorrect information, the agent typically won't question it.

**Example**
```
Tool response: { "user_balance": 1000 }  // Database bug, actual: 10000

Agent: "Your current balance is $1,000"

User: "That's wrong, I deposited $9,000 yesterday"

Agent: "According to my records, your balance is $1,000"  // Confidently wrong

Result: Agent trusts tool over user, provides incorrect information
```

## Mitigation Strategies

### Prevention
1. **User-assertion cross-check before restating a contradicted fact**: When a user directly contradicts a tool-provided value with a specific counter-claim (as in "I deposited $9,000 yesterday"), require the agent to re-query the source or flag the discrepancy for verification rather than simply repeating the original tool output — the example's core failure is trusting the tool over a specific, checkable user claim. Trade-off: opens a path for users to socially-engineer the agent into distrusting correct data, so the re-check must be a verification step, not an automatic acceptance of the user's claim.
2. **Sanity bounds on high-stakes tool outputs**: For financial/critical data, validate tool outputs against plausible bounds and recent history (e.g., a balance that doesn't reflect a very recent, large, known transaction) before presenting it as fact. Trade-off: bounds need domain-specific tuning and can produce false positives on legitimately unusual but correct values.
3. **Source reliability weighting in multi-agent pipelines**: When an upstream agent or tool has a known error history, weight its outputs lower and require corroboration before a downstream agent repeats them as fact — prevents "upstream agent makes mistake, downstream agent doesn't catch it." Trade-off: requires tracking reliability scores per source over time, adding operational overhead.

### Detection & Response
1. **Tool-output error-rate tracking by source**: Log discrepancies between tool outputs and later-confirmed ground truth per tool/source, so a buggy database (like the "user_balance" bug in the example) is identified by pattern rather than one user complaint at a time.
2. **User-correction-to-tool-trust feedback loop**: When a user disputes an agent's tool-sourced answer, log it as a candidate tool error and route it to verification rather than silently re-asserting the same tool output on retry — directly prevents the example's repeated confident wrongness.
3. **Reasoning-chain provenance audit**: For multi-step or multi-agent tasks, periodically audit whether each claim in the final output can be traced to a specific tool/agent output, and flag chains where an unverified claim was propagated unchanged across multiple steps.

### Architecture Patterns
1. **Verification-before-assertion gate for disputed high-stakes claims**: Route any tool output that a user directly disputes through a mandatory re-verification call (fresh query, alternate source, or human check) before the agent responds again, rather than looping the same unverified value back to the user. Deployment consideration: needs a way to detect "this is a dispute" versus a general follow-up question, which requires some intent classification.
2. **Multi-source cross-validation for critical fields**: For fields like account balance where being wrong has direct financial consequences, query at least two independent sources (primary DB plus a transaction-log reconciliation) and flag mismatches rather than trusting a single tool call. Deployment consideration: doubles the calls needed for critical fields and requires reconciliation logic for conflicting sources.
3. **Confidence propagation through the pipeline**: Track and surface a confidence/reliability score alongside data as it moves through tool calls and agent handoffs, so a low-reliability source's output is visibly flagged rather than presented with the same certainty as verified data. Deployment consideration: requires every component in the pipeline to participate in confidence propagation, which is a broader design commitment than a point fix.

### Metrics
1. **tool_output_error_rate**: % of tool outputs later found incorrect against ground truth, tracked per source; target < 1%; alert if > 5% for any single source.
2. **user_dispute_unresolved_rate**: % of user-disputed tool outputs where the agent re-asserted the same value without re-verification; target < 2%; alert if > 10%.
3. **cross_source_mismatch_rate**: % of critical-field queries where independent sources disagree; target < 1%; alert if > 5%.
4. **unverified_claim_propagation_rate**: % of multi-step reasoning chains where an unverified upstream claim reaches the final output unchecked; target < 5%; alert if > 15%.

### Alerts
1. **User Dispute Re-Asserted Without Verification** (P1): Condition — agent repeats a disputed tool value without triggering re-verification (user_dispute_unresolved_rate spike). Action: immediately escalate the session to human review and patch the dispute-handling path to force re-query.
2. **Tool Source Error Rate Spike** (P1): Condition — tool_output_error_rate exceeds 5% for a given source. Action: page the owning team for that data source/tool, and temporarily downgrade its reliability weighting pending investigation.
3. **Cross-Source Mismatch on Critical Field** (P2): Condition — cross_source_mismatch_rate exceeds 5% for balance/financial fields. Action: freeze automated actions relying on that field until reconciliation logic or the underlying data bug is fixed.

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Research on error propagation in multi-agent systems
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Analysis of inherited error patterns in AI agent pipelines
