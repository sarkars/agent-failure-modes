# Inferred Preference Silently Overrides Explicit Client Constraint

## Issue: An Agent Given an Explicit, Durable Client Constraint Infers a Broader or Conflicting Preference From the Client's Transaction History During Multi-Step Recommendation Generation and Silently Supersedes the Explicit Constraint Instead of Flagging the Conflict

**Frequency**: Occasional

**Symptoms**
- The client's explicit constraint (e.g., "no tobacco holdings," "no direct real estate exposure") is correctly present and retrievable in the client's profile at the moment the recommendation is generated — it has not fallen out of context and no second, conflicting explicit instruction was ever given
- The agent's recommendation nonetheless includes a holding that violates the explicit constraint, justified in the agent's own reasoning trace by a pattern it inferred from the client's recent unsolicited trades or watchlist activity ("client's recent purchases suggest comfort with adjacent sin-sector exposure")
- The conflict between the explicit constraint and the inferred pattern is never surfaced to the client or advisor for confirmation; the agent resolves it internally and presents only the final recommendation
- Removing the inferred-preference signal from the agent's input (holding the transaction-history context constant but omitting the specific pattern that triggered the inference) restores compliance with the explicit constraint, isolating the inference step as the cause rather than a retrieval or memory failure
- The violation is not accompanied by any explicit new instruction relaxing the constraint — the client never said "actually tobacco is fine now" — the override originates entirely from the model's own pattern-matching over historical data

**Root Cause**
Recommendation agents are commonly designed to personalize beyond a client's explicitly stated constraints by inferring additional preferences from behavioral signals such as trading history, watchlist activity, or engagement patterns, because richer personalization is treated as a quality improvement. When the inferred signal and the explicit constraint point in different directions, the model has no built-in mechanism forcing it to treat the explicit, durably stored instruction as higher-priority evidence than a pattern it derived itself from indirect behavioral data; both are just signals present in its reasoning context, and a sufficiently strong inferred pattern can outweigh the explicit constraint during generation. This is distinct from context-window decay (the explicit constraint has not fallen out of salience — it is fully present and correctly retrieved) and from a conflict between two explicit instructions from different sources (there is only one explicit instruction; the competing signal is one the model generated itself through inference over retrieved data). The failure is specifically in how an agent adjudicates between a stored explicit rule and a freshly inferred pattern, rather than in retention, retrieval, or instruction-source conflict.

**Example**
```
Scenario: Client's durable profile contains an explicit stored constraint: "exclude tobacco and tobacco-adjacent holdings" (set six months ago during onboarding, confirmed and unchanged since)
Recent activity: Client has independently placed several small, self-directed trades in consumer-staples names with diversified product lines, one of which derives roughly 8% of revenue from a tobacco subsidiary
Recommendation task: Agent is asked to suggest a core holding to fill a consumer-staples allocation gap in the client's model portfolio
Agent's retrieved profile correctly shows the explicit tobacco-exclusion constraint
Agent's reasoning also processes the client's recent self-directed trades and infers: "client's recent purchases indicate comfort with diversified consumer-staples names even where a tobacco-adjacent revenue line exists"
Agent recommends a specific diversified conglomerate ETF whose top holdings include a company deriving a double-digit percentage of revenue from tobacco products, treating the inferred pattern as effectively updating the stored constraint
No flag, caveat, or confirmation request is presented alongside the recommendation noting the tension with the explicit exclusion
Impact: Advisor implements the recommendation without independently re-checking it against the exclusion list; the violation is caught only during the next periodic mandate-compliance sweep, after the position has been held for several weeks
```

**Key Statistics**
- Surveys of personalized LLM-powered agents distinguish explicit preferences, which are directly specified by the user, from implicit preferences inferred from behavioral patterns, and note that personalization pipelines commonly blend both into a single downstream decision without a defined precedence rule between them
- Research on LLM-based recommendation highlights that systems built primarily around implicit behavioral signals can drift away from a user's explicitly stated context or constraints, since implicit signals are continuously available while explicit constraints are set once and must be actively re-surfaced and prioritized at generation time
- Portfolio-mandate compliance reviews in advisory settings identify silent constraint violations introduced during recommendation generation — rather than violations caused by the constraint being missing from the client record — as a recurring root cause distinct from data-entry or retrieval failures

---

## Mitigation Strategies

1. **Explicit-Constraint Precedence Rule**: Encode a hard rule that any explicit, durably stored client constraint always outranks an inferred behavioral signal during recommendation generation, with no code path that allows an inference to silently supersede it.
2. **Constraint-Violation Gate Independent of Narrative**: Run a deterministic post-generation check that screens every recommended holding against the client's explicit constraint list before it is surfaced, blocking any recommendation that fails regardless of the reasoning that produced it.
3. **Mandatory Conflict Disclosure**: When an inferred pattern from behavioral data points against an explicit constraint, require the agent to surface the tension explicitly to the advisor ("recent trading activity suggests X, which conflicts with stored exclusion Y") rather than resolving it silently in either direction.
4. **Separation of Inference Signals From Constraint Storage**: Architect client profiles so explicit constraints are stored and retrieved through a distinct, higher-trust channel than inferred behavioral preferences, so the two are never merged into an undifferentiated context block the model must adjudicate on its own.

### Metrics
- Rate of recommendations violating an explicit stored constraint, broken out by whether an inferred behavioral signal was present in the same generation
- Conflict-disclosure rate (% of cases where an inferred signal opposing an explicit constraint was surfaced rather than silently resolved)
- Time-to-detection for constraint violations introduced during recommendation generation, relative to periodic compliance sweeps

### Alerts
- A generated recommendation violates an explicit stored client constraint → P1
- An inferred-preference signal in the agent's reasoning trace opposes an explicit constraint without a corresponding conflict disclosure in the output → P2

---

## Related Patterns
- [Cross-Client Parameter Bleed in Sequential Advisory Sessions](./cross-client-parameter-bleed-in-sequential-advisory-sessions.md) — related suitability-parameter integrity failure in recommendation generation, driven by cross-session carryover rather than in-session inference overriding an explicit rule
- [Long-Session Context Loss Violates Earlier Constraints](../../../../../cross-cutting/accuracy/goals/context-management/failures/long-session-context-loss-violates-earlier-constraints.md) — related constraint-violation symptom, but caused by the constraint falling out of attention over a long session rather than being correctly retained and then outweighed by an inferred signal
- [Preference Vs Instruction Confusion](../../../../../cross-cutting/operations/goals/memory-safety/failures/preference-vs-instruction-confusion.md) — related but inverse mechanism: a soft preference mistakenly enforced as a hard rule, versus a hard rule mistakenly softened by an inferred preference

## References

- [Toward Personalized LLM-Powered Agents: Foundations, Evaluation, and Future Directions](https://arxiv.org/pdf/2602.22680)
- [Toward User Preference Alignment in LLM Recommendation via Explicit Context Feedback](https://arxiv.org/abs/2605.29141)
