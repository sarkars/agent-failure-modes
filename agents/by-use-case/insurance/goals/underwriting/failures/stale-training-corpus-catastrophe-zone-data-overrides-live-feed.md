# Stale Training-Corpus Catastrophe-Zone Data Overrides Live Feed

## Issue: An Underwriting Agent Answers Risk-Zone Questions (Flood Zone, Wildfire Risk Tier, Hurricane Exposure Band) from Facts Memorized During Pretraining Instead of Calling the Live Catastrophe-Model or Mapping Tool It Has Available, Producing Risk Assessments Based on Outdated Zone Designations

**Frequency**: Occasional

**Symptoms**
- Underwriting rationale states a property's flood zone, wildfire tier, or hurricane exposure band with confidence but without a corresponding tool call to the live mapping or catastrophe-model API in the agent's trace for that turn
- The zone designation cited matches an older map vintage (consistent with the model's pretraining cutoff) rather than the current designation, discoverable by independently querying the live tool for the same address
- The error concentrates on addresses in areas that have had a relatively recent zone remapping (e.g., post-disaster FEMA flood map revision, updated wildfire-risk model release) where the live data has diverged from what existed at the time of the model's training
- When the agent is explicitly prompted to "use the flood zone tool" rather than left to decide whether a tool call is necessary, the live-vs-memorized discrepancy disappears, isolating the failure to the agent's default behavior of answering from parametric memory when a tool call is not explicitly forced
- Underwriting decisions citing a risk zone are occasionally inconsistent with the risk zone independently recorded elsewhere in the same policy file from a separate, tool-grounded process, revealing that two parts of the same workflow disagree on a fact that should be a single source of truth

**Root Cause**
The underwriting agent has access to a live catastrophe-modeling or geocoding tool, but because the model also has substantial parametric "knowledge" about geography and historically common risk-zone facts absorbed during pretraining, it can produce a fluent, specific-sounding answer to a risk-zone question without invoking the tool, especially when the prompt does not explicitly mandate a tool call for that field. The model has no internal signal distinguishing "this is a fact I am confident about because I retrieved it live" from "this is a fact I am confident about because it appeared frequently and consistently in training data" -- both surface as equally fluent, equally confident text.

**Example**
```
Underwriting agent is assessing a commercial property for a renewal quote and is asked to confirm the property's FEMA flood zone designation
Property's flood zone was reclassified from Zone X (minimal risk) to Zone AE (high-risk, mandatory flood insurance) after a FEMA map revision issued after the underwriting model's training cutoff
Agent answers "Zone X, minimal flood risk" directly from its parametric knowledge of the area's historically reported zone, without invoking the live FEMA flood-zone lookup tool it has available
Renewal is underwritten without the flood-risk premium adjustment and without the mandatory flood-insurance referral the current Zone AE designation actually requires, an error not caught until a subsequent claim triggers a coverage review
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to produce hallucinated or stale factual claims not grounded in live data when an explicit tool-grounding step is not enforced, a distinct failure mode from reasoning errors | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Agentic AI applied to commercial insurance underwriting is evaluated specifically against adversarially perturbed and incomplete-data cases to test whether agents over-rely on internal assumptions rather than verifying inputs against authoritative sources | [Agentic AI for Commercial Insurance Underwriting with Adversarial Self-Critique](https://arxiv.org/html/2602.13213) |
| Generative AI applications in actuarial science are documented to require explicit grounding against authoritative, current data sources rather than relying on a model's internal knowledge for risk-relevant facts | [Advanced Applications of Generative AI in Actuarial Science: Case Studies Beyond ChatGPT](https://arxiv.org/html/2506.18942v1) |

**Contributing Factors**
- Agent's prompt or tool-use policy does not explicitly mandate a live tool call for every risk-zone-relevant fact, leaving the decision to call the tool to the model's own judgment
- No automated check compares the risk-zone designation cited in the underwriting rationale against the live tool's current output before the quote or renewal is finalized
- Model has substantial parametric knowledge of historically common risk-zone facts, which surfaces with the same fluency and confidence as genuinely tool-retrieved current facts

---

## Mitigation Strategies

1. **Mandatory Tool Call for Every Risk-Zone Field**: Require a live catastrophe-model or mapping tool call as a non-optional step for every flood zone, wildfire tier, and hurricane exposure determination, rather than leaving the decision to invoke the tool to the model
2. **Post-Hoc Consistency Check Against Tool Output**: Before finalizing the underwriting decision, run an automated comparison between the risk-zone value stated in the agent's rationale and the most recent live tool query result for that same address, blocking finalization on mismatch
3. **Strip Risk-Zone Facts from Model Context When Unsupported by a Tool Call**: If no tool-call trace exists for a risk-zone field in a given turn, treat any risk-zone claim in the agent's output as unverified and require a tool call before the field can be used in the underwriting decision
4. **Periodic Re-Verification on Map Revision Events**: When an authoritative source (FEMA, state wildfire agency) issues a zone-map revision, flag all in-force and pending policies in affected geographies for mandatory re-verification rather than relying on the next natural renewal cycle alone

### Metrics
- Rate of underwriting decisions citing a risk-zone fact with no corresponding live tool-call trace for that turn
- Discrepancy rate between agent-stated risk zone and live tool query result, sampled per policy at bind/renewal
- Time lag between an authoritative zone-map revision and full re-verification of affected in-force policies

### Alerts
- Underwriting decision finalized with a risk-zone field that has no tool-call trace and disagrees with the live tool's current output → P1
- Map-revision event issued by an authoritative source with no corresponding re-verification sweep initiated within the defined SLA → P2
- Tool-call rate for risk-zone fields drops below the mandated baseline for a given underwriting workflow → P3

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Agentic AI for Commercial Insurance Underwriting with Adversarial Self-Critique](https://arxiv.org/html/2602.13213)
- [Advanced Applications of Generative AI in Actuarial Science: Case Studies Beyond ChatGPT](https://arxiv.org/html/2506.18942v1)
