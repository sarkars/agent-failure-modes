# Unverified Clearance Opinion Filed Without Checking Cited Clause Against Source Agreement

## Issue: An IP-Clearance Agent Asked to Confirm a Company Holds Sufficient Rights to Use a Third-Party Asset (a Licensed Image, a Vendor-Supplied Code Library, a Co-Developed Patent Disclosure) Generates a Clearance Opinion That Quotes a Specific License Clause as Granting the Needed Right, Then Autonomously Files or Releases That Opinion to the Requesting Team Without Re-Reading the Actual Source License Text It Just Cited to Confirm the Quoted Clause Says What the Opinion Claims It Says

**Frequency**: Occasional

**Symptoms**
- Clearance opinion confidently states "Section 4.2 of the License Agreement grants worldwide, perpetual sublicensing rights" but Section 4.2 of the actual source document grants a narrower, non-sublicensable, field-of-use-restricted right
- The opinion's quoted clause language is close to but not an exact match for the source document's actual text -- a paraphrase that drifted toward the broader right the requesting team was hoping for
- Downstream teams (product, marketing, engineering) proceed to use the asset in a manner consistent with the opinion's claimed scope, not the source license's actual scope, before anyone re-reads the underlying agreement
- The discrepancy surfaces only when the licensor's counsy or an external audit re-reads the actual clause and flags that the company's use exceeds the granted rights
- Re-running the same clearance request with an explicit instruction to quote the source clause verbatim and diff it against the opinion's paraphrase reliably surfaces the mismatch, showing the agent had access to the correct text and simply did not check its own output against it before releasing the opinion

**Root Cause**
The agent treats opinion drafting and verification as a single pass: it generates the clearance opinion's characterization of a clause from its working understanding of the license, and the same generation step that produces the paraphrase also produces the opinion's confidence and the act of releasing it, with no independent verification step that re-reads the actual source clause text and checks the opinion's claim against it before the opinion is treated as actionable. Because the model's paraphrase of a clause is fluent and internally consistent with the rest of its own opinion, there is no internal signal that distinguishes a verified quote from a confident misremembering of the clause's actual scope.

**Example**
```
Engineering team asks the IP-clearance agent to confirm rights to sublicense a third-party code library bundled into a customer-facing product
Agent retrieves the vendor license agreement and produces an opinion: "Section 4.2 grants the Company a worldwide, perpetual, sublicensable license to incorporate the Library into Company products and distribute to end customers"
Opinion is filed directly to engineering's rights-clearance tracker as "Cleared -- sublicensing confirmed," unblocking the release
Six weeks later, the vendor's legal team flags that Section 4.2 actually grants a non-sublicensable, internal-use-only license; sublicensing requires a separate addendum that was never executed
Re-reading Section 4.2 against the opinion's quoted text shows the opinion's "sublicensable" characterization does not appear anywhere in the actual clause -- the agent generated it as a plausible extension of the surrounding license language rather than a verified reading of that specific term
Product is already shipped to customers with the unlicensed sublicense scope; remediation requires emergency relicensing negotiation under disadvantageous terms
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM agents asserting task completion (here, "clearance confirmed") frequently do so without verifying the actual state of the artifact they are claiming about, relying on surface-level confidence cues rather than a check against ground truth | [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/html/2606.09863) |
| LLM-based agents are documented to produce fabricated or drifted characterizations of source content that read as plausible and internally consistent, making self-generated paraphrases unreliable as a substitute for re-checking the original text | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Execution-provenance research for LLM agents argues that traceable evidence linking a generated claim to the exact source span it is based on is necessary because models do not reliably self-report when a claim has drifted from its cited source | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- No structural separation between the generation step that drafts the opinion's characterization of a clause and a distinct verification step that re-reads the actual clause text before the opinion is releasable
- The opinion's prose quotes the clause in a way that looks like a direct citation, giving downstream readers false confidence that the text was checked verbatim
- Autonomous filing/release of the opinion to a tracker that downstream teams treat as authoritative removes the natural human checkpoint where someone might otherwise re-read the source agreement before acting
- Time pressure from the requesting team to get a fast "cleared" answer discourages a slower, independent verification pass

---

## Mitigation Strategies

1. **Mandatory Verbatim-Quote-and-Diff Gate**: Before any clearance opinion can be filed or released, require the agent to extract the actual clause text verbatim from the source document and run an automated diff between that verbatim text and the opinion's characterization, blocking release on any unresolved discrepancy
2. **Independent Verification Pass**: Route the opinion through a second, independent re-read of the source document by a separate prompt or reviewer (human or model) that has not seen the original opinion's framing, rather than allowing the same generation pass to both draft and clear itself
3. **Confidence-Scope Labeling**: Require the opinion to explicitly label which scope claims are direct quotes (with page/section reference) versus the agent's own characterization or inference, so reviewers can immediately see which statements have not been independently checked
4. **Hold Autonomous Filing for High-Stakes Clearances**: For clearance opinions that unblock shipping or public release, require a human sign-off step after the verification gate rather than allowing the agent to file the opinion as final and actionable on its own

### Metrics
- Rate of filed clearance opinions where the quoted clause text does not exactly match the source document on independent re-read
- Mean time between opinion filing and detection of a scope discrepancy (internal verification vs. external/licensor-flagged)
- Percentage of clearance opinions that included a verbatim-quote-and-diff check before filing

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Verbatim diff mismatch | Verbatim-quote-and-diff gate finds opinion's characterization does not match source clause text | P1 | Block filing; route to independent legal review before any downstream team acts |
| Opinion filed without verification gate | Clearance opinion released to tracker with no record of a verbatim-quote-and-diff check | P2 | Retroactively verify; flag any downstream usage already taken in reliance on it |
| Recurring drift on same license type | Multiple verified discrepancies traced to the same source-license template or clause type | P3 | Audit clearance prompts/templates for that license type |

---

## References

- [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/html/2606.09863)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
