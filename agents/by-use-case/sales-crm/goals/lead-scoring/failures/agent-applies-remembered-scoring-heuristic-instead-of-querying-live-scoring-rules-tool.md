# Agent Applies Remembered Scoring Heuristic Instead of Querying Live Scoring-Rules Tool

## Issue: A Lead-Scoring Agent, When Asked to Explain or Compute a Lead's Score, Falls Back on a Generic Firmographic-Weighting Heuristic Resembling Common Industry Lead-Scoring Conventions It Absorbed During Pretraining (e.g., "Company Size and Title Seniority Are Typically Weighted Most Heavily") Rather Than Calling the Company's Live Scoring-Rules Tool, Which Reflects a Recently Updated Weighting Scheme That Down-Weights Company Size in Favor of a Recent Intent-Signal Category the Marketing Team Just Promoted, Producing a Score and Explanation That No Longer Match What the Company's Actual Current Rules Would Produce

**Frequency**: Occasional

**Symptoms**
- Agent's explanation of why a lead scored highly cites factors (company size, title seniority) that, per the live scoring-rules tool, are no longer the top-weighted factors for the current quarter
- Querying the live scoring-rules tool directly for the same lead returns a different weighting breakdown than what the agent's explanation described, with intent-signal categories (recent product-page visits, pricing-page engagement) weighted higher than the agent's narrative reflects
- The discrepancy appears specifically for leads scored after a recent scoring-rules update, while leads scored and explained before the update show no mismatch
- Sales reps trust the agent's stated reasoning to prioritize outreach, deprioritizing leads that the live rules would actually rank highly based on the newer intent-signal weighting
- The agent had the scoring-rules tool available and authorized for this query, but the execution trace shows no call to it before the explanation was generated

**Example**
```
Marketing updates the company's lead-scoring rules this quarter to weight recent
pricing-page visits and competitor-comparison-page visits much more heavily than company
size, reflecting a shift toward intent-based qualification
A rep asks the lead-scoring agent: "Why did this lead score a 72?"
Agent has a live scoring-rules tool available that returns the company's current,
authoritative weighting scheme and the specific factor contributions for this lead
Agent answers using a generic explanation pattern: "This lead scored well primarily due
to company size (500+ employees) and the contact's VP-level title" -- a plausible-sounding
explanation resembling conventional lead-scoring wisdom, with no tool call logged
The live scoring-rules tool, queried separately, shows the actual top contributors to
this lead's score were three pricing-page visits and a competitor-comparison-page visit
in the past week -- company size and title contributed only a small fraction of the score
Rep deprioritizes a different, lower-firmographic-profile lead that the live rules would
actually flag as high-intent, because the agent's stated reasoning for similar leads
emphasized firmographics the rep now (wrongly) believes dominate scoring this quarter
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Hallucination survey research documents agents defaulting to generic, plausible-sounding domain conventions absorbed during pretraining when a live, more current and applicable tool result is actually available | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds agents frequently answer questions a specific available tool was designed to answer without invoking that tool, relying instead on parametric knowledge that may no longer match the live system | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Research on miscalibration in tool-use agents finds agents express confident, fluent explanations regardless of whether the underlying claim was actually verified against a live tool result, contributing to a gap between stated confidence and grounded accuracy | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |

**Contributing Factors**
- No hard instruction requiring the agent to call the live scoring-rules tool before generating any explanation of factor contributions to a lead's score
- Generic lead-scoring conventions (firmographic weighting) are common enough in training data that the agent's fallback explanation sounds authoritative and domain-appropriate even when wrong for this specific, recently updated rule set
- Scoring-rule updates roll out on a cadence (quarterly, post-campaign) that a static pretrained pattern can never reflect, regardless of how recent the agent's training cutoff is
- The agent's explanation output is not labeled with its source (live rules-tool output vs. generic pattern), so reps cannot tell an unverified explanation from a grounded one

---

## Mitigation Strategies

1. **Mandatory Tool Call for Factor Explanations**: Require the agent to call the live scoring-rules tool before generating any explanation of why a lead received its score; block generic explanations when the tool was not called
2. **Source-Labeled Factor Contributions**: Require every stated scoring factor in agent output to be labeled with its source (live scoring-rules tool vs. unverified), making ungrounded explanations visible to reps
3. **Post-Update Explanation Audit**: After any scoring-rules update, audit a sample of agent-generated explanations against the new live rules to confirm the agent is reflecting the updated weighting rather than a stale pattern
4. **Tool-Call Enforcement Check**: Automatically flag any agent response describing scoring factor contributions that lacks a corresponding scoring-rules-tool call in the same execution trace

### Metrics
- Rate of factor-contribution explanations generated without a corresponding live scoring-rules-tool call in the trace
- Delta between agent-stated top factors and the live tool's actual top factors for the same lead
- Number of outreach-prioritization decisions traced back to an unverified, stale-pattern explanation

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Factor explanation without tool call | Response describes scoring factors with no scoring-rules-tool call in trace | P1 | Block response; force tool call and regenerate |
| Factor-weighting mismatch | Agent-stated top factors differ from live tool's actual top factors for the same lead | P2 | Correct explanation; review recently prioritized/deprioritized leads in the same segment |
| Post-rules-update drift | Sampled explanations after a scoring-rules update still reflect pre-update weighting patterns | P3 | Audit and reinforce mandatory tool-call enforcement |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
