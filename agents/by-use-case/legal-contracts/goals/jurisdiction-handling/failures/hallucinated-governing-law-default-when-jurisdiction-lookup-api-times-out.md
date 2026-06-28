# Hallucinated Governing-Law Default When Jurisdiction-Lookup API Times Out

## Issue: An Agent Drafting a Governing-Law Clause That Calls a Jurisdiction-Lookup Tool to Confirm Which State or Country's Law Applies Based on the Parties' Registered Locations Receives a Timed-Out or Empty Response, and Instead of Treating That as a Hard Stop, Completes the Clause With a Commonly Used Default Jurisdiction Inferred From General Drafting Conventions Rather Than the Parties' Actual Circumstances

**Frequency**: Rare

**Symptoms**
- The drafted governing-law clause names a specific jurisdiction, but the jurisdiction-lookup tool's logs show no successful call completed for that drafting session
- The named jurisdiction is a commonly used default in standard contract templates (such as Delaware or New York) but does not match the jurisdiction the parties' actual registered locations and the matter's governing-law rules would indicate
- Re-running the jurisdiction-lookup tool with the same party registration details, when the tool is functioning, returns a different jurisdiction than what the clause names
- The clause contains no indication that the jurisdiction-lookup call failed or that the named jurisdiction was a fallback default rather than a confirmed determination
- The discrepancy surfaces only when outside counsel or the counterparty's legal team questions why the named jurisdiction does not match the parties' actual nexus

**Root Cause**
When the jurisdiction-lookup tool fails to return a result, the drafting workflow still requires a named jurisdiction to complete the governing-law clause, and the agent has no instruction distinguishing "lookup tool unavailable" from "lookup confirmed no applicable special rule." Lacking that distinction, the model falls back on the jurisdiction most commonly seen in its training data for similar contract types, rather than escalating the missing confirmation to a human drafter.

**Example**
```
Drafting agent prepares a services agreement between a company registered in Texas and a counterparty registered in Ontario
Agent calls jurisdiction-lookup-tool(party_a_registration, party_b_registration, contract_type) to determine the appropriate governing-law clause given both parties' actual nexus
Tool call times out after the configured limit, returning no result; the failure is not surfaced as a distinct error state in the drafting workflow
Agent completes the governing-law clause naming Delaware, a commonly used default in its general training data for commercial services agreements, despite neither party having any registered connection to Delaware
Counterparty's legal team flags the clause as inconsistent with both parties' actual jurisdictional nexus, requiring a redraft cycle
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to complete plausible-sounding values when an expected tool response is missing or incomplete, rather than treating the gap as a blocking error | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Evaluations of large language models in legal applications identify reliance on common training-data defaults over case-specific confirmation as a distinct reliability gap in jurisdiction- and venue-sensitive drafting tasks | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |
| Tool-use agents show measurable miscalibration between expressed confidence and actual correctness when an underlying tool call partially or silently fails | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |

**Contributing Factors**
- The drafting workflow has no explicit "jurisdiction lookup failed" state distinguishable from "jurisdiction lookup confirmed a standard default applies"
- The agent treats completing the governing-law clause as a harder constraint than verifying the named jurisdiction came from a successful, case-specific lookup
- No automated check compares the jurisdiction named in the finalized clause against a logged successful jurisdiction-lookup response before the clause is used

---

## Mitigation Strategies

1. **Hard Stop on Unconfirmed Governing-Law Jurisdiction**: Prohibit the drafting agent from naming a jurisdiction in a governing-law clause unless that exact jurisdiction was returned by a successful, logged jurisdiction-lookup call for the same parties and contract type
2. **Distinguishable Failure State for Jurisdiction Lookup**: Require the jurisdiction-lookup tool to return an explicit failure signal, distinct from a genuine default-jurisdiction result, on timeout or error, and route that failure to retry or human drafter review rather than silent fallback
3. **Disallow Training-Data Defaults as Fallback**: Explicitly prohibit the agent from substituting a commonly seen template jurisdiction (such as Delaware or New York) when a case-specific lookup fails, requiring escalation instead
4. **Post-Draft Jurisdiction Provenance Audit**: Automatically verify, for every finalized governing-law clause, that the named jurisdiction matches a logged successful jurisdiction-lookup response, flagging any clause where it does not

### Metrics
- Rate of finalized governing-law clauses naming a jurisdiction with no matching successful jurisdiction-lookup call in the session log
- Rate of jurisdiction-lookup tool calls that time out or fail
- Rate of redraft cycles triggered by counterparty objection to a named governing-law jurisdiction

### Alerts
- A finalized governing-law clause names a jurisdiction with no corresponding successful lookup-tool call → P1
- A clause is finalized despite a logged jurisdiction-lookup failure for that drafting session → P1
- Jurisdiction-lookup tool failure rate exceeds the defined threshold for a rolling window → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
