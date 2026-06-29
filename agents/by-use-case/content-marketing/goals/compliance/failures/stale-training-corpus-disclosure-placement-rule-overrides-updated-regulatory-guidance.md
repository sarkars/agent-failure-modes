# Stale Training-Corpus Disclosure-Placement Rule Overrides Updated Regulatory Guidance

## Issue: A Compliance-Review Agent Answers Questions About Where and How an Advertising Disclosure Must Appear (Required Proximity to a Claim, Minimum Font Size, Required Placement Before a "Buy Now" Action) from Facts Memorized During Pretraining Instead of Calling the Live Regulatory-Guidance Tool It Has Available, Producing Compliance Sign-Offs Based on Outdated Disclosure Rules

**Frequency**: Occasional

**Symptoms**
- Compliance sign-off rationale states a disclosure-placement rule (required proximity, font size, pre-action placement) with confidence but without a corresponding tool call to the live regulatory-guidance lookup in the agent's trace for that turn
- The placement rule cited matches an older regulatory guidance vintage rather than the current rule, discoverable by independently querying the live regulatory-guidance tool for the same claim type
- The error concentrates on disclosure types that have had a relatively recent guidance update (e.g., a regulator's revised clear-and-conspicuous standard, an updated influencer-disclosure rule) where the live guidance has diverged from what existed at the time of the model's training
- When the agent is explicitly prompted to "use the regulatory-guidance lookup tool" rather than left to decide whether a tool call is necessary, the live-vs-memorized discrepancy disappears, isolating the failure to the agent's default behavior of answering from parametric memory when a tool call is not explicitly forced
- Compliance sign-offs citing a disclosure-placement rule are occasionally inconsistent with the rule independently recorded elsewhere in the same campaign-review file from a separate, tool-grounded legal review, revealing that two parts of the same workflow disagree on a fact that should be a single source of truth

**Root Cause**
The compliance-review agent has access to a live regulatory-guidance lookup tool, but because the model also has substantial parametric "knowledge" about historically common disclosure-placement rules absorbed during pretraining, it can produce a fluent, specific-sounding answer to a disclosure-placement question without invoking the tool, especially when the prompt does not explicitly mandate a tool call for that field. The model has no internal signal distinguishing "this is a fact I am confident about because I retrieved it live" from "this is a fact I am confident about because it appeared frequently and consistently in training data" -- both surface as equally fluent, equally confident text.

**Example**
```
Compliance-review agent is asked to confirm the required placement and font size for a sponsorship disclosure on a paid social post
Regulator issued revised clear-and-conspicuous guidance after the agent's training cutoff, requiring the disclosure to appear before the first line of visible caption text rather than appended at the end
Agent answers "disclosure may appear anywhere within the caption, including at the end with a standard hashtag," directly from its parametric knowledge of the prior, superseded guidance, without invoking the live regulatory-guidance lookup tool it has available
Campaign is approved and published with the disclosure placed at the end of the caption, a placement the current guidance no longer treats as compliant, discovered only when a regulator inquiry or platform compliance audit flags the post
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to produce hallucinated or stale factual claims not grounded in live data when an explicit tool-grounding step is not enforced, a distinct failure mode from reasoning errors | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| LLM-based content-generation and review systems evaluated at scale show that grounding compliance-relevant determinations in retrieved, current source material rather than internal model knowledge materially affects output reliability | [LLMs for Customized Marketing Content Generation and Evaluation at Scale](https://arxiv.org/html/2506.17863v1) |
| Audits of agentic workflow failures in production platforms identify reliance on internal model knowledge in place of available live grounding tools as a recurring root cause of downstream compliance and decision errors | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- Agent's prompt or tool-use policy does not explicitly mandate a live regulatory-guidance tool call for every disclosure-placement determination, leaving the decision to call the tool to the model's own judgment
- No automated check compares the disclosure-placement rule cited in the compliance sign-off against the live regulatory-guidance tool's current output before the campaign is approved
- Model has substantial parametric knowledge of historically common disclosure rules, which surfaces with the same fluency and confidence as genuinely tool-retrieved current rules

---

## Mitigation Strategies

1. **Mandatory Tool Call for Every Disclosure-Placement Determination**: Require a live regulatory-guidance lookup as a non-optional step for every disclosure-placement, font-size, and pre-action-placement determination, rather than leaving the decision to invoke the tool to the model
2. **Post-Hoc Consistency Check Against Tool Output**: Before finalizing the compliance sign-off, run an automated comparison between the disclosure rule stated in the agent's rationale and the most recent live regulatory-guidance tool query result, blocking sign-off on mismatch
3. **Strip Disclosure-Placement Facts from Model Context When Unsupported by a Tool Call**: If no tool-call trace exists for a disclosure-placement field in a given turn, treat any placement claim in the agent's output as unverified and require a tool call before the field can be used in the compliance sign-off
4. **Periodic Re-Verification on Guidance-Revision Events**: When a regulator issues revised disclosure guidance, flag all in-flight and recently approved campaigns of the affected claim type for mandatory re-verification rather than relying on the next scheduled compliance review cycle alone

### Metrics
- Rate of compliance sign-offs citing a disclosure-placement rule with no corresponding live tool-call trace for that turn
- Discrepancy rate between agent-stated disclosure rule and live regulatory-guidance tool query result, sampled per campaign at sign-off
- Time lag between a regulatory guidance revision and full re-verification of affected in-flight and recently approved campaigns

### Alerts
- Compliance sign-off finalized with a disclosure-placement field that has no tool-call trace and disagrees with the live regulatory-guidance tool's current output → P1
- Guidance-revision event issued by a regulator with no corresponding re-verification sweep initiated within the defined SLA → P2
- Tool-call rate for disclosure-placement determinations drops below the mandated baseline for a given compliance workflow → P3

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [LLMs for Customized Marketing Content Generation and Evaluation at Scale](https://arxiv.org/html/2506.17863v1)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
