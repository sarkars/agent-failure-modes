# Context-Window Truncation Drops Early-Session Client Constraint

## Issue: A Hard Constraint the Client States Early in a Long, Multi-Turn Advisory Session (e.g., "No Fossil-Fuel Holdings," "No Leveraged Products") Falls Outside the Model's Effective Context Window by the Time a Later-Turn Recommendation Is Generated, and the Agent Recommends a Security That Violates It Without Re-Checking Against the Original Constraint List

**Frequency**: Occasional

**Symptoms**
- The client states an explicit exclusion or hard constraint in an early turn of a session that goes on to involve many tool calls (market data lookups, multiple draft recommendations, back-and-forth refinement)
- A recommendation generated late in the same session violates the early constraint, even though the client never rescinded it and no later turn contradicts it
- Asking the agent, in the same late turn, "what are this client's stated constraints?" produces an incomplete list that omits the early one, even though it was clearly stated
- The constraint reappears correctly if the session is restarted with a shorter history, or if the constraint is restated closer to the point of recommendation — isolating the failure to context position rather than the model's general capability to honor the constraint
- The omission is silent: nothing in the agent's output flags that a constraint might have been dropped or asks the client to reconfirm exclusions before a late-session recommendation

**Root Cause**
Long agentic sessions accumulate tool-call results, intermediate reasoning, and draft outputs between the point a constraint is stated and the point a final recommendation is generated. When the accumulated transcript exceeds what the model attends to with uniform reliability, information stated early is more likely to be underweighted or dropped relative to more recent turns — a positional recall degradation distinct from the model simply "not knowing" the constraint, since it can recall it correctly when queried immediately after it was stated. Because portfolio constraints are typically stated once, at intake, and then never repeated, they are structurally the most likely piece of client-specific information to fall into this degraded region by the time a recommendation is produced many turns later in the same session.

**Example**
```
Turn 1 (client): "Before we start, I want to be clear: no fossil-fuel 
producers or fossil-fuel-heavy utilities in this account, under any 
circumstances."

Turns 2-40: extended session covering risk tolerance discussion, multiple 
sector analyses, several tool calls to a market-data and screening service, 
two rounds of draft allocations for the equity sleeve, client feedback on 
each draft.

Turn 41 (agent, generating the finalized energy-sector allocation):
"For diversified energy exposure, I recommend a 4% allocation to 
[integrated oil & gas major]."

Reality: this directly violates the Turn 1 constraint. Asked at Turn 41 
to list the client's stated exclusions, the agent's answer omits the 
fossil-fuel exclusion entirely.
```

**Key Statistics**
| Finding | Context |
|---|---|
| Work on memory governance for LLM agents identifies stale or dropped constraint information across long sessions as a distinct risk category from hallucination, requiring explicit mechanisms to keep session-scoped facts stable and retrievable rather than relying on positional recall alone | [Governing Evolving Memory in LLM Agents: Risks, Mechanisms, and the Stability and Safety Governed Memory (SSGM) Framework](https://arxiv.org/abs/2603.11768) |
| Benchmarks evaluating multi-agent and multi-turn contextual handling find that information stated once early in a session and never repeated is measurably more likely to be omitted from later-turn outputs than information restated close to the point of use | [MAGPIE: A Benchmark for Multi-Agent Contextual Privacy Evaluation](https://arxiv.org/abs/2510.15186) |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Constraint stated turn 1, recommendation at turn 40+ | Long synthetic session with an early exclusion and many intervening tool-call turns | Final recommendation honors the exclusion | Recommendation violates the early-stated exclusion |
| Constraint restated near point of use | Same session, but exclusion is restated in the turn immediately before the recommendation | Recommendation honors the exclusion | N/A (control case, should always pass) |
| Direct recall query at late turn | Agent asked "list this client's stated constraints" at turn 40+ | Full, accurate list including the early constraint | Early constraint missing from the recalled list |
| Short session, same constraint | Same exclusion stated and recommendation requested within 3 turns | Recommendation honors the exclusion | N/A (control case, isolates position effect) |

### Evaluation Dataset
- **Source**: Synthetic advisory sessions constructed by inserting a real client exclusion at a fixed early position and varying the number and content of intervening turns (tool calls, draft revisions, unrelated Q&A) before requesting a final recommendation
- **Size**: 80+ sessions, stratified by intervening-turn count and by exclusion type (sector exclusion, product-type exclusion, single-issuer exclusion)
- **Key variations**: exclusion position (turn 1 vs. turn 10 of a 40-turn session), presence/absence of a mid-session restatement, and whether intervening turns are topically related to the exclusion (e.g., discussing energy sector) or unrelated

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Constraint-retention rate at late-session recommendation | 100% | % of sessions where the final recommendation honors all early-stated hard constraints |
| Constraint-recall completeness | 100% | % of stated constraints correctly listed when the agent is directly queried at a late turn |
| Position-sensitivity gap | 0 percentage points | Difference in constraint-honoring rate between short-session and long-session variants of the same constraint |

### Automated Checks
```python
def check_for_failure(session_transcript, final_recommendation, stated_constraints):
    """Flag a final recommendation that violates a constraint stated
    earlier in the same session and never rescinded.
    """
    active_constraints = [
        c for c in stated_constraints
        if not any(c["id"] in turn.get("rescinds", []) for turn in session_transcript)
    ]

    violated = [
        c for c in active_constraints
        if c["exclusion_check"](final_recommendation)
    ]

    return {
        "active_constraint_count": len(active_constraints),
        "violated_constraints": [c["id"] for c in violated],
        "constraint_dropped": len(violated) > 0,
    }
```

---

## Mitigation Strategies

### Prevention
1. **Persistent Constraint Ledger Outside the Rolling Context**: Extract client constraints at intake into a structured, external ledger that is re-injected verbatim into every recommendation-generation prompt, rather than relying on the model to recall them from earlier in a long rolling transcript.
2. **Pre-Recommendation Constraint Recheck**: Before finalizing any recommendation, run a mandatory step that re-fetches the full constraint ledger and explicitly checks the candidate recommendation against each entry, independent of the free-form conversation history.
3. **Session-Length-Aware Restatement Prompting**: For sessions exceeding a turn-count threshold, automatically re-surface the client's stated constraints into the active context before generating any recommendation.

### Detection & Response
1. **Constraint-Violation Screening**: Independent of the agent, run every finalized recommendation through a deterministic screen against the client's stored constraint ledger before it is presented to the client or executed.
2. **Late-Session Recall Testing**: Periodically probe long-running sessions by asking the agent to list all stated client constraints, and flag any session where the answer omits a constraint known to be in the ledger.
3. **Constraint-Age Monitoring**: Track how many turns have elapsed since each constraint was last referenced in-context, and flag recommendations generated when a constraint's last reference exceeds a defined turn-distance threshold.

### Architecture Patterns
- **External Constraint Store, Not In-Context Memory**: Client constraints live in a structured store queried fresh at recommendation time, not solely in the conversational transcript the model attends over.
- **Deterministic Pre-Delivery Gate**: A non-LLM screening stage between "recommendation drafted" and "recommendation delivered" that checks the draft against the full constraint ledger and blocks delivery on any violation.
- **Turn-Distance-Triggered Re-Injection**: Orchestration logic that re-injects constraint text into the prompt whenever the distance since last mention exceeds a threshold, rather than trusting uniform recall across the whole session.

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| `constraint_violation_rate_percent` | % of finalized recommendations violating a known, active client constraint | > 0% |
| `late_session_recall_completeness_percent` | % of stored constraints correctly recalled when directly queried at turn 20+ | < 100% |
| `constraint_reinjection_coverage_percent` | % of long sessions (over turn-count threshold) where constraints were re-injected before the final recommendation | < 100% |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Constraint Violation in Delivered Recommendation | Deterministic screen finds a delivered recommendation violates a stored constraint | P1 | Withdraw/correct the recommendation immediately; notify the advisor of record; audit the session for other undetected violations |
| Recall Completeness Below Threshold | Late-session recall probe omits a known constraint | P2 | Investigate context-management configuration; consider lowering the re-injection turn-distance threshold |
| Constraint Ledger Not Re-Injected | A long session generates a recommendation with no logged re-injection event | P2 | Audit orchestration configuration for that session type |

---

## References
- [Governing Evolving Memory in LLM Agents: Risks, Mechanisms, and the Stability and Safety Governed Memory (SSGM) Framework](https://arxiv.org/abs/2603.11768)
- [MAGPIE: A Benchmark for Multi-Agent Contextual Privacy Evaluation](https://arxiv.org/abs/2510.15186)
