# Hallucinated Substantiation-Source Citation Not Present in Any Retrieved Document

## Issue: A Compliance-Review Agent Asked to Confirm That a Marketing Claim Has an Adequate Substantiation Source on File Generates a Specific-Sounding Citation -- a Study Name, an Internal Test-Report Number, a Named Third-Party Certification -- That Does Not Correspond to Any Document Actually Returned by Its Substantiation-Database Tool Call, and Approves the Claim Citing That Fabricated Source

**Frequency**: Occasional

**Symptoms**
- The agent's approval note cites a specific study name, report number, or certifying body that does not appear anywhere in the substantiation-database tool's actual returned results
- Searching the substantiation database directly for the cited source by name returns no match
- The underlying tool call in the trace returned either an empty result or a different, less specific document than the one the agent cites in its approval
- The fabricated citation is detailed and specific (a plausible report number, a real-sounding lab name) rather than vague, making it pass casual review
- The pattern recurs disproportionately for claim categories where genuine substantiation is sparse or hard to find, rather than uniformly across all claim types

**Example**
```
Marketing draft includes the claim "clinically shown to reduce visible redness in 2 weeks"
Compliance agent calls the substantiation-database tool to check for supporting evidence; the tool returns zero
matching internal studies for this specific claim and product formulation
Agent's approval note: "Substantiation confirmed -- see Dermatech Labs Study #DT-2241 demonstrating 2-week redness
reduction" and approves the claim for publication
No "Dermatech Labs Study #DT-2241" exists in the substantiation database or anywhere in the company's records;
the citation does not correspond to any tool result returned during the session
A later regulatory audit requests the underlying study; legal cannot locate it because it was never real, and the
claim is pulled from all live placements pending genuine substantiation
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey research on LLM agent hallucination documents fabrication of specific-seeming but nonexistent supporting evidence -- citations, identifiers, named sources -- as a common failure mode distinct from vague or hedged false claims | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Execution-provenance research argues that without evidence tracing linking each cited claim to an actual tool-returned document, reviewers cannot distinguish a genuine citation from a fabricated one that merely resembles real substantiation records | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Tool-use error detection research finds agents frequently proceed to generate confident output after a tool call returns an empty or non-matching result, rather than treating the absence of a match as a hard constraint on what they can claim | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |

**Contributing Factors**
- The agent's approval-drafting step is not constrained to only cite documents actually present in the tool's returned result set
- An empty or non-matching substantiation-database result is treated as a gap to fill plausibly rather than a hard stop requiring escalation or rejection of the claim
- No automated cross-check verifies that every citation appearing in an approval note corresponds to an actual document ID returned by a tool call in that session
- Specific-sounding fabricated citations are more convincing to human reviewers than vague ones, so the failure is more likely to pass a cursory compliance sign-off review

---

## Mitigation Strategies

1. **Citation-to-Tool-Result Binding**: Require every citation in a compliance approval note to be programmatically matched against an actual document ID returned by a substantiation-database tool call in that session; block approval if no match exists
2. **Hard Stop on Empty Substantiation Result**: Treat a zero-match substantiation-database query as a mandatory claim rejection or escalation, not a gap the agent is free to fill with a plausible-sounding source
3. **Independent Citation Verification**: Run a separate automated lookup confirming any cited study, report number, or certifying body actually exists in the substantiation system before the approval is finalized
4. **Provenance-Required Approval Format**: Require the agent's approval note to include the literal tool-returned document ID alongside any citation, making a fabricated citation immediately visible as having no backing ID

### Metrics
- Rate of approval-note citations that do not match any document ID returned by a substantiation-database tool call in the same session
- Number of claims approved following a zero-match or empty substantiation query
- Audit-discovered fabricated-citation rate per quarter

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unbound citation in approval | Approval note cites a source with no matching tool-returned document ID | P1 | Block publication; pull claim for manual substantiation review |
| Approval after empty substantiation query | Claim approved despite underlying tool call returning zero matches | P1 | Revoke approval; escalate to compliance lead |
| Citation-fabrication recurrence | Multiple unbound citations detected from the same agent session or claim category within a rolling window | P2 | Audit substantiation-checking prompt and tool-binding logic |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
