# Context-Window Loss Drops Early-Stated Demand-Driver Correction in Long Planning Session

## Issue: In a Long, Multi-Turn Demand-Planning Conversation, a Planner's Early Correction to a Demand Driver -- Stating That a Promotion Has Been Cancelled or a Store Closure Has Been Delayed -- Fails to Persist Into the Final Forecast the Agent Generates Many Turns Later in the Same Conversation, With the Agent Reverting to the Original, Uncorrected Assumption

**Frequency**: Occasional

**Symptoms**
- A final forecast generated late in a long planning conversation incorporates a demand driver (a promotion, a store closure, a launch date) exactly as it was originally stated early in the conversation, even though the planner explicitly corrected that driver partway through
- Asking the agent, immediately after the final forecast, to restate the demand drivers it used surfaces the original, uncorrected version rather than the planner's correction
- The correction is more likely to be dropped the further back in the conversation it was stated relative to the turn that triggers the final forecast generation, consistent with reduced effective attention to early-conversation content in long sessions
- Re-stating the same correction immediately before the forecast-generation turn, in an otherwise identical conversation, produces a forecast that correctly reflects it
- Planners who do not re-verify the final forecast's stated assumptions against their own correction proceed to allocate inventory or labor against the uncorrected driver

**Root Cause**
As a conversation accumulates turns, the model's effective use of information earlier in the context window degrades, particularly for content that is not the most recent or most repeated; a single, unreinforced correction stated once early in a long planning session is a documented case where this degradation causes earlier content to be underweighted relative to the original framing of the same fact. The forecast-generation turn then draws on the conversation's accumulated context as a whole rather than re-confirming each demand driver against its most recent stated value, so the original, uncorrected driver resurfaces in the final output.

**Example**
```
Turn 3: Planner tells the demand-forecasting agent that Store #142 is closing for renovation in week 6, to be excluded from the regional forecast from that week onward
Turn 4-30: Planner and agent continue an extended planning conversation covering unrelated SKUs, regions, and seasonal adjustments
Turn 12: Planner corrects the earlier statement: the Store #142 renovation has been delayed and the store will remain open through week 6 after all
Turn 31: Planner asks the agent to generate the final regional forecast for the period including week 6
Agent's forecast excludes Store #142 from week 6 onward, reflecting the original closure statement from turn 3 rather than the turn-12 correction
Regional inventory allocation under-ships to Store #142 for week 6 based on the uncorrected forecast
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Empirical evaluation of language models on long-context tasks finds that performance on information located in the middle of a long context degrades measurably relative to information at the very start or very end, regardless of the information's importance to the task | [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) |
| Multi-turn conversation evaluation finds that LLMs systematically lose track of instructions and corrections established earlier in an extended conversation, with reliability degrading as conversation length increases | [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) |
| Research on LLM agents for supply chain management identifies demand-driver assumption tracking across an extended planning interaction as a distinct reliability requirement separate from the forecasting computation itself | [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597) |

**Contributing Factors**
- No structured, persistent record of demand-driver assumptions is maintained outside the raw conversation history, so a correction's only representation is its position in a long, unstructured context
- Forecast-generation turn does not require the agent to re-state and confirm each demand driver against its most recently stated value before proceeding
- Planners default to trusting the final forecast's incorporated assumptions without independently re-checking each driver against their own correction history

---

## Mitigation Strategies

1. **Structured Demand-Driver Ledger Outside Conversation History**: Maintain demand-driver assumptions (promotions, closures, launches) in a structured, explicitly-updated record outside the raw conversation transcript, with each correction overwriting rather than appending to the prior value
2. **Mandatory Driver Restatement Before Forecast Generation**: Require the agent to explicitly restate every demand driver it intends to use, sourced from the structured ledger rather than the conversation transcript, immediately before generating a final forecast
3. **Correction Acknowledgment Requirement**: When a planner states a correction to a previously stated driver, require the agent to explicitly acknowledge the prior value being overwritten, creating a clear audit point distinct from a silent context update
4. **Forecast-Assumption Diff Against Ledger**: Before presenting a final forecast, automatically diff the assumptions it incorporated against the current structured ledger and flag any mismatch for planner review

### Metrics
- Rate of final forecasts whose stated demand-driver assumptions do not match the most recently corrected value in conversation history
- Mean conversation distance (turns) between a demand-driver correction and the forecast-generation turn, for forecasts later found to use the uncorrected value
- Planner override rate when a forecast-assumption diff against the structured ledger flags a mismatch

### Alerts
- A final forecast incorporates a demand-driver value that contradicts a later correction present in the same conversation → P1
- A forecast-generation turn proceeds with no driver restatement sourced from the structured ledger → P2
- Driver-correction-loss rate across all planning sessions exceeds the defined threshold for a rolling window → P3

---

## References

- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)
- [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120)
- [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597)
