# SDR-to-AE Handoff Drops Unstructured Disqualifying Signal

## Issue: An SDR-Qualification Agent's Chat Transcript with a Prospect Contains a Disqualifying Signal (No Budget This Fiscal Year, Competitor Already Selected, No Executive Sponsor) That the Agent Mentions in Free-Text Notes but Never Writes to a Structured CRM Field, So the Downstream AE-Facing Forecasting Agent Counts the Opportunity at Full Pipeline Value

**Frequency**: Common

**Symptoms**
- Pipeline-forecasting agent's weighted-value calculation includes an opportunity at full stage-weighted value despite the SDR conversation transcript explicitly recording a disqualifying statement from the prospect (e.g., "we already signed with [competitor]" or "this isn't budgeted until next fiscal year")
- The structured CRM fields the forecasting agent reads (stage, close date, amount) show no flag corresponding to the disqualifying language present in the SDR's own chat log or call notes field
- Forecast accuracy audits find that opportunities later marked "Closed Lost -- No Budget" or "Closed Lost -- Competitor Selected" had the disqualifying reason stated by the prospect during the SDR qualification call, well before the opportunity reached the stage where forecasting weight became material
- The gap is most pronounced for opportunities that pass through an SDR-to-AE handoff, since opportunities qualified and forecasted by the same person/agent throughout show a lower rate of this discrepancy
- Re-processing the SDR transcript through the same forecasting agent in a single continuous context (transcript directly in context) correctly down-weights the opportunity, isolating the handoff -- not the model's underlying reasoning capability -- as the point of failure

**Root Cause**
The SDR-qualification agent and the forecasting agent operate as separate invocations with the structured CRM record, not the raw conversation transcript, as the interface between them. When the SDR agent's own output narrates a disqualifying signal in free text (call notes, chat summary) without writing a corresponding structured disqualification flag, the forecasting agent -- which is built to consume structured stage/amount/probability fields rather than to re-read every upstream conversation transcript -- has no way to incorporate that signal, even though the information needed to forecast correctly was generated earlier in the pipeline.

**Example**
```
SDR-qualification agent conducts a discovery call; prospect states "honestly we already picked [Competitor X], this call was really just due diligence for our records"
SDR agent's call-summary notes field records this verbatim, and the agent still advances the opportunity to "Qualified" stage in the structured CRM record because the call covered the required discovery-question checklist, with no separate disqualification flag written
Forecasting agent, reading only the structured stage/amount/close-date fields for its weighted-pipeline calculation, counts the opportunity at the qualified-stage weighting
Opportunity is marked Closed Lost two weeks later; post-mortem review of the original SDR call transcript shows the disqualifying signal was known at qualification time and simply never made it into a field the forecasting agent could see
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Failures in agentic CRM workflows are concentrated at task scenarios requiring agents to integrate information across interconnected records and policies, with leading agents reaching only ~35% success in multi-turn, multi-step CRM scenarios | [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878) |
| Multi-agent LLM systems exhibit measurable information loss at hand-off boundaries, where one agent's generated finding does not propagate into the structured state the next agent actually consumes | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Building powerful business agents benefits from shared memory architectures specifically because per-agent context silos otherwise cause exactly this class of cross-agent information loss in business workflows | [CRMWeaver: Building Powerful Business Agent via Agentic RL and Shared Memories](https://arxiv.org/pdf/2510.25333) |

**Contributing Factors**
- SDR-qualification agent's output contract allows advancing an opportunity's stage without a corresponding structured disqualification-risk field, even when its own free-text notes contain disqualifying language
- Forecasting agent is designed to consume structured stage/amount/probability fields only, with no step that re-scans upstream conversation transcripts for disqualifying language
- No automated keyword/sentiment scan of qualification-call transcripts cross-checks against the structured disqualification flag before an opportunity is counted in the weighted pipeline

---

## Mitigation Strategies

1. **Mandatory Structured Disqualification-Risk Field at Qualification**: Require the SDR-qualification agent to populate a structured `disqualification_risk` field (none/budget/competitor/no_sponsor/etc.) as part of every qualification handoff, derived from the same transcript it already summarizes, rather than leaving the signal in free text only
2. **Automated Transcript Scan Before Forecast Inclusion**: Run an automated scan of qualification-call transcripts and notes for disqualifying language as a gate before an opportunity is included at full stage-weighted value in the forecast, flagging mismatches between transcript content and structured flags for review
3. **Forecasting Agent Re-Reads Source Transcript on High-Value Opportunities**: For opportunities above a materiality threshold, require the forecasting agent to retrieve and check the original qualification transcript directly rather than relying solely on structured fields, as a higher-cost but more reliable check on larger forecast contributors
4. **Closed-Lost Reason Backtested Against Earlier Transcripts**: When an opportunity closes lost, automatically check whether the stated loss reason was already present in an earlier-stage transcript, and use the rate of this pattern as a direct measure of how often disqualifying signals are being dropped at handoff

### Metrics
- Rate of Closed Lost opportunities whose loss reason was already stated in an earlier qualification-stage transcript but never reflected in a structured disqualification flag
- Forecast accuracy (weighted-pipeline value vs. actual closed value) segmented by opportunities that passed through an SDR-to-AE handoff vs. those that did not
- Percentage of qualification handoffs missing a structured disqualification-risk field

### Alerts
- Opportunity counted at full stage-weighted forecast value despite an automated transcript scan detecting disqualifying language with no corresponding structured flag → P1
- Closed-Lost rate attributable to dropped disqualification signals exceeds baseline for a given SDR team or handoff path for two consecutive forecast cycles → P2
- SDR-qualification workflow modified or deployed without a mandatory structured disqualification-risk field → P3

---

## References

- [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878)
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [CRMWeaver: Building Powerful Business Agent via Agentic RL and Shared Memories](https://arxiv.org/pdf/2510.25333)
