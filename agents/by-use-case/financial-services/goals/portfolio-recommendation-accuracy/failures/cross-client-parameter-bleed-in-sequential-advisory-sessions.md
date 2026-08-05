# Cross-Client Parameter Bleed in Sequential Advisory Sessions

## Issue: An Advisor-Facing Agent That Processes Multiple Clients Within a Single Continuous Session Carries a Computed Suitability Parameter (Risk Tolerance, Tax Bracket, Liquidity Need) From One Client Forward Into Its Reasoning for the Next Client, Without Any Literal Data From the First Client Appearing in the Second Client's Output

**Frequency**: Occasional

**Symptoms**
- An advisor copilot processes a queue of clients sequentially in one working session, and a recommendation for client N reflects a risk-tolerance, tax-bracket, or liquidity-horizon assumption that matches client N-1's profile rather than client N's own onboarding data
- The leaked value never appears as literal text belonging to another client, so PII scanning and data-loss-prevention tooling find nothing to flag; it only surfaces as a silently wrong number baked into an allocation percentage or a suitability statement
- The error is most likely when client N-1 and client N are processed back-to-back with superficially similar profile fields (both "moderate growth" objective, both retirement accounts), so the wrong value is plausible on its face and passes a cursory review
- The agent's own tool call to retrieve client N's profile returns the correct record, but the final recommendation still reflects client N-1's parameter, indicating the bleed happens during the model's synthesis step rather than in the data-retrieval layer
- Restarting the agent with a fresh, isolated context per client eliminates the error even though the underlying tool calls and database queries are byte-for-byte identical to the session that produced the error

**Root Cause**
Advisor-facing agents are commonly built to keep a single conversational session open across an entire client queue or workday, for continuity, cost, and latency reasons, rather than opening an isolated context per client interaction. When the agent's own prior turns computed and reasoned about client N-1's risk tolerance, tax situation, or liquidity constraint, that computed value remains present and salient in the context window. When client N's task begins, the model correctly retrieves client N's own profile through a fresh tool call, but its synthesis step draws on the accumulated session context rather than exclusively on the newly retrieved record, so a derived parameter from the prior client blends into or quietly displaces the parameter that should have been freshly derived for the current client. This is distinct from an infrastructure-level multi-tenant isolation failure — there is no shared cache, no cross-request data exposure, and no literal record from client N-1 appearing anywhere in client N's output. It is a single continuous LLM context carrying a computed value across a client-switch boundary that nothing in the session's structure marks as a hard reset point.

**Example**
```
Scenario: Financial advisor uses a copilot to prepare recommendations for 12 client review meetings in one afternoon session
Client 7 (age 61, near retirement, conservative, low liquidity need): Agent computes and states "recommended equity allocation: 35%, reflecting your stated risk tolerance and short time horizon"
Client 8 (age 34, high risk tolerance, long time horizon, stated need for liquidity toward a house down payment in 18 months): Agent's tool call correctly retrieves Client 8's own profile (age 34, growth objective, 18-month liquidity earmark)
Client 8's generated recommendation: "recommended equity allocation: 38%, reflecting a conservative near-term liquidity posture" -- the 18-month liquidity earmark is genuinely Client 8's own, but the "conservative near-term" framing and the allocation figure track much closer to Client 7's profile than to Client 8's own stated growth objective and long horizon
Advisor, reviewing 12 recommendations in sequence within the same afternoon, does not catch the mismatch because each recommendation individually looks internally plausible
Impact: Client 8 receives an equity allocation misaligned with their own stated objective, discovered only weeks later when the client questions why the allocation looks unexpectedly conservative relative to what was discussed in the meeting
```

**Key Statistics**
- Evaluations of multi-agent and multi-party LLM interactions find that sensitive or party-specific information can leak into outputs intended for a different party even when the model is explicitly instructed to keep contexts separate, at rates that vary by model but are consistently non-trivial
- Research on persistent and evolving agent memory identifies context or state solidifying across what should be independent interactions as a distinct failure category from classic infrastructure-level tenant-isolation bugs, since no access-control boundary is actually crossed
- Advisory platforms running long, single-session copilot workflows report this class of error clustering among clients reviewed later in a session or queue, consistent with a carry-forward mechanism rather than a uniformly random error rate

---

## Mitigation Strategies

1. **Hard Context Reset at Client Boundaries**: Force a new, isolated context or session for every client interaction; never reuse conversational context across clients even when doing so would improve caching efficiency or latency.
2. **Parameter Provenance Tagging**: Require every suitability parameter used in a recommendation to be tagged with the specific tool call and timestamp it was derived from within the active client's own session, and block any recommendation whose parameter provenance doesn't match the currently active client ID.
3. **Fresh-Retrieval Enforcement Before Synthesis**: Force a mandatory, non-cached re-fetch of the client's own profile immediately before generating a recommendation, and structurally exclude any prior client's profile data from the prompt content sent to the model for that generation step.
4. **Cross-Client Diff Audit**: Run an automated post-hoc check that diffs each client's recommendation parameters against both their own onboarding record and the immediately preceding client's parameters in the same session, flagging suspicious similarity to the prior client.

### Metrics
- Rate of recommendation parameters matching the prior-client-in-session value more closely than the active client's own retrieved profile
- Context-reset compliance rate (% of client interactions executed in a freshly isolated context)
- Parameter-provenance-tag mismatch rate

### Alerts
- A recommendation parameter for client N matches client N-1's profile value within a tight tolerance while diverging from client N's own retrieved profile → P1
- A session serves more than one client without a context-reset boundary between them → P2

---

## Related Patterns
- [Cross-Session Data Bleed](../../../../../cross-cutting/security/goals/data-loss-prevention/failures/cross-session-bleed.md) — infrastructure-level session/cache isolation failure; this pattern is the LLM-context-carryover variant that occurs even with correct infrastructure isolation
- [Tool Mutation State Leak](../../../../../cross-cutting/operations/goals/tool-selection-sequencing/failures/tool-mutation-state-leak.md) — related hidden-state carryover mechanism, but across tools within one task rather than across clients within one advisory session
- [KYC Refresh Staleness](../../regulatory-compliance/failures/kyc-refresh-staleness.md) — related suitability-parameter integrity issue in financial services advisory workflows

## References

- [MAGPIE: A Benchmark for Multi-Agent Contextual Privacy Evaluation](https://arxiv.org/abs/2510.15186)
- [Governing Evolving Memory in LLM Agents: Risks, Mechanisms, and the Stability and Safety Governed Memory (SSGM) Framework](https://arxiv.org/abs/2603.11768)
