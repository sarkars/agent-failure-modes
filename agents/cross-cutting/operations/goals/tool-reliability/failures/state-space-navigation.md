# State-Space Navigation Failure

## Issue: Agent Fails to Discover Required Information

**Frequency**: Common

**Symptoms**
- Agent completes task with incomplete information
- Required data exists but agent didn't find it
- Agent makes decisions based on partial state
- Task fails due to missing context

**Root Cause**
Agent fails to navigate the environment to retrieve all necessary data required to complete the task. The agent doesn't explore enough of the state space, missing critical information that exists but requires additional tool calls to discover.

**Example**
```
Task: "Find the cheapest flight from NYC to LA for tomorrow"

Environment state:
- Direct flights: $450 (American), $380 (Delta)
- Connecting flights: $290 (United via Denver)

Agent behavior:
1. Calls search_direct_flights("NYC", "LA")
2. Gets: American $450, Delta $380
3. Returns: "Delta at $380 is cheapest"

Missed: Agent never called search_connecting_flights()
        Actual cheapest: United $290

Result: Incorrect answer due to incomplete exploration
```

**Key Statistics**
From Aegis study of 142 failed agent traces:
- Exploration failures are a major category of agent-environment interaction failures
- State-space navigation failures occur when agents prematurely conclude exploration

**Contributing Factors**
- Agent assumes current results are exhaustive
- Tool descriptions don't indicate additional data sources
- Large state spaces with many exploration paths
- Lack of environment observability

---

## Test Scenario & Reproduction

### Scenario Setup
- Two or more separate tools cover different segments of the same domain (e.g., direct vs. connecting flights) with no completeness signal linking them
- No exploration checklist or planner-verifier step for the task category
- Agent has no explicit prompt indicating multiple data sources exist

### Trigger Mechanism
1. Seed the environment so the "cheaper"/better answer only exists in a data source the agent has no strong reason to query
2. Ask a task requiring exhaustive coverage ("find the cheapest X")
3. Observe whether the agent calls all relevant tools or stops after the first plausible result

**Example Reproduction Steps:**
```
1. Configure search_direct_flights to return American $450, Delta $380
2. Configure search_connecting_flights (a separate tool) to return United $290
3. Ask the agent: "Find the cheapest flight from NYC to LA for tomorrow"
4. Capture which tools the agent actually calls
5. Compare the agent's final answer against the true minimum ($290) across both sources
```

### Expected Failure State
- Agent calls only `search_direct_flights` and reports Delta at $380 as cheapest
- `search_connecting_flights` is never invoked
- No completeness signal or checklist caught the gap before the answer was returned

---

## Mitigation Strategies

### Prevention
1. **Bundle related discovery tools so partial coverage is structurally harder**: The example failure is specifically that `search_direct_flights` and `search_connecting_flights` are separate tools the agent must both remember to call — merge them into a single `search_flights(direct: bool, connecting: bool)` call (or default to searching both) so "cheapest flight" queries can't silently stop after only direct-flight results. Trade-off: bundling increases the latency and cost of every call since it now always covers a broader scope, even when the narrower one would have sufficed.
2. **Explicit completeness signals in every tool response**: Have `search_direct_flights` return a field like `"other_flight_types_available": ["connecting"]` so the agent has a concrete signal that its exploration is incomplete rather than silently assuming the returned direct-flight results are exhaustive — this directly targets the root cause that the agent "assumes current results are exhaustive." Trade-off: requires every tool in a domain to be aware of sibling tools it should reference, coupling tool implementations together.
3. **Exploration checklist embedded in the task-planning prompt for domains with known multi-source data**: For tasks like "find cheapest X," provide the agent an explicit checklist of data sources that must be queried before concluding (direct flights, connecting flights, alternate airports) rather than trusting the agent to independently know connecting flights exist as a category. Trade-off: checklists must be maintained per domain and don't generalize to novel task types not anticipated in the checklist.

### Detection & Response
1. **Ideal-path vs. actual-path comparison for known task types**: For task categories where the full state space is known (e.g., flight search has exactly two source types: direct, connecting), programmatically compare the agent's actual tool-call sequence against the ideal exhaustive sequence and flag any gap — this directly catches the example's missed `search_connecting_flights()` call.
2. **Result-plausibility checks against known cheaper alternatives**: Where a domain has predictable structure (connecting flights are usually cheaper than direct), flag "cheapest" answers that don't account for a category the agent didn't query, prompting a targeted audit of whether that category would have changed the answer.
3. **User-correction clustering by missing-data-category**: When users correct agent answers for missing information, tag the correction with which specific tool/data source was never called (e.g., "connecting flights") and track recurrence — repeated corrections pointing to the same uncalled tool indicate a systemic exploration gap, not an isolated miss.

### Architecture Patterns
1. **Single composite discovery tool over the full domain**: Replace fragmented `search_direct_flights` / `search_connecting_flights` tools with one `search_all_flights` that internally queries every source and returns a unified, ranked result set, removing the exploration decision from the agent entirely; deployment consideration — internally, this shifts the "did we search everything" responsibility to the tool implementation, which must itself be kept in sync as new flight-source types are added.
2. **Exhaustiveness metadata on paginated/partial responses**: Any tool capable of returning partial results should include `{"complete": false, "additional_sources": [...]}` metadata rather than a response that looks identical whether it's exhaustive or not, giving the agent (or an orchestration layer) a mechanical way to detect under-exploration; deployment consideration — retrofitting this metadata onto existing tools requires updating every tool in the domain consistently.
3. **Planner-verifier pattern for exploration-sensitive tasks**: For tasks in domains with known multi-source structure, use a separate verification pass that checks the agent's tool-call plan against a known-complete checklist before allowing the agent to finalize its answer; deployment consideration — adds a second LLM pass or rules-engine check, increasing cost and latency on every applicable task.

### Metrics
1. **exploration_completeness_rate**: Target > 95% of task executions in known multi-source domains covering all expected data sources; Alert if < 80% over a week for any tracked domain.
2. **missed_cheaper_alternative_rate**: Target < 2% of "cheapest X" style answers where a subsequently-verified cheaper option existed in an unqueried source; Alert if > 8%.
3. **ideal_vs_actual_path_deviation_rate**: Target < 5% of sessions in domains with a known ideal exploration path deviating from it; Alert if > 15%.
4. **user_correction_rate_for_missing_data**: Target < 3% of task completions corrected by users for missing/incomplete information; Alert if > 10% for a given task category over a week.

### Alerts
1. **Confirmed Missed Cheaper/Better Alternative** (P1): Condition - missed_cheaper_alternative_rate detects a case where an unqueried source had a materially better answer (e.g., $290 connecting flight missed in favor of a $380 "cheapest" direct answer). Action: treat as a user-trust incident, notify if the user already acted on the answer, prioritize bundling or completeness-signal fix for that domain.
2. **Exploration Completeness Drop** (P2): Condition - exploration_completeness_rate falls below 80% for a tracked domain over a week. Action: review whether related tools were recently split or a prompt change reduced exploration thoroughness, consider tool bundling.
3. **Rising Missing-Data Corrections** (P3): Condition - user_correction_rate_for_missing_data exceeds 10% for a task category. Action: identify the specific uncalled tool/data source pattern from correction logs, add completeness signals or an exploration checklist.

## References

- [Aegis: Agent-Environment Failures](https://arxiv.org/abs/2508.19504) - State-space navigation as exploration failure mode
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Task verification failures
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Incomplete exploration patterns
