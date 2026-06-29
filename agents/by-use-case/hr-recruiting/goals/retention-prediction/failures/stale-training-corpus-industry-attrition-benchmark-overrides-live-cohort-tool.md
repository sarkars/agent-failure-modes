# Stale Training-Corpus Industry-Attrition Benchmark Overrides Live Cohort Tool

## Issue: A Retention-Prediction Agent, When Asked to Contextualize Whether an Employee's Computed Risk Score Is High Relative to Peers, Answers Using a General Industry Attrition-Rate Figure It Absorbed During Pretraining Rather Than Calling the Live Internal Cohort-Comparison Tool Available to It, Producing a Relative-Risk Characterization Anchored to an Outdated or Generic Benchmark Instead of the Company's Actual, Current Department-Level Attrition Baseline

**Frequency**: Occasional

**Symptoms**
- Agent's risk narrative states a comparison like "this is below the industry-average attrition rate for this role" using a specific percentage that does not match any figure returned by the company's internal cohort-comparison tool
- The live cohort tool, when queried directly for the same role/department/tenure band, returns a materially different current baseline (often because the company's actual attrition in that segment shifted significantly after a reorg, layoff, or comp-cycle change the pretrained figure could not reflect)
- The agent had the cohort-comparison tool available and authorized for this exact query, but the trace shows no call to it before the benchmark claim was generated
- Risk scores described as "below average" or "in line with peers" using the stale benchmark are, against the live internal baseline, actually elevated -- meaning employees who should have been flagged for intervention are not
- Asking the agent directly "what does the cohort tool say" after the fact produces a different, internally-sourced figure that contradicts the original narrative

**Example**
```
HR asks the retention-prediction agent: "Is [employee]'s risk score high compared to
others in their department?"
Agent has access to a live internal cohort-comparison tool that returns real-time
department-level attrition baselines computed from the company's own HRIS history
Agent answers: "This is roughly in line with typical attrition rates for this type of
role, around 12-15% annually" -- a generic figure resembling commonly cited industry
averages from its training data, with no tool call logged
The live cohort tool, queried separately, shows this specific department's actual
trailing-12-month attrition rate is 31% following a recent reorg -- meaning the
employee's risk score is well above the relevant current baseline, not in line with it
HR deprioritizes a retention conversation based on the "in line with peers" framing
The employee resigns two months later; post-mortem finds the live cohort data showing
elevated departmental risk was available the whole time and simply never queried
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Hallucination survey research documents LLM agents defaulting to memorized, pretraining-era figures for matters where a live, more current tool result is actually available and applicable | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error research finds agents frequently fail to invoke an available and relevant tool before answering a question that tool was specifically designed to answer, instead answering directly from parametric knowledge | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Research on agent-environment failures finds a recurring pattern where agents do not reliably recognize when a live, environment-grounded answer is required instead of a plausible-sounding generated one | [Aegis: Agent-Environment Failures in LLM-Driven Agentic Systems](https://arxiv.org/html/2508.19504) |

**Contributing Factors**
- No hard instruction requiring the agent to call the live cohort-comparison tool before making any relative-risk or peer-comparison claim
- The pretrained benchmark figure is fluent and plausible-sounding, giving HR no visible signal that it differs from what the company's own data would show
- Department-level attrition baselines can shift quickly after a reorg or layoff, a kind of change a static pretrained figure can never reflect regardless of how recent the model's training cutoff was
- The agent's tool-use policy treats the cohort tool as optional context rather than a mandatory grounding step for any comparative claim

---

## Mitigation Strategies

1. **Mandatory Tool Call for Comparative Claims**: Require the agent to call the live cohort-comparison tool before generating any statement comparing an individual's risk score to a peer group or baseline; block the response if the tool was not called
2. **Source-Labeled Benchmarks**: Require every benchmark figure in agent output to be labeled with its source (live internal cohort tool vs. general knowledge) so reviewers can immediately spot an unsourced claim
3. **Tool-Call Audit on Comparative Language**: Automatically flag any agent response containing comparative language ("in line with," "above/below average") that lacks a corresponding tool-call entry in the same execution trace
4. **Period Re-Baseline Reminder**: Surface a system note to the agent when department-level attrition baselines have moved significantly since the agent's last successful cohort-tool call, prompting a fresh query rather than reuse of an older answer

### Metrics
- Rate of comparative risk statements generated without a corresponding live cohort-tool call in the trace
- Delta between agent-stated benchmark figures and the live cohort tool's actual current value for the same segment
- Number of retention conversations deprioritized based on an "in line with peers" framing later contradicted by live data

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Comparative claim without tool call | Response contains peer/baseline comparison language with no cohort-tool call in trace | P1 | Block response; force tool call and regenerate |
| Benchmark mismatch detected | Agent-stated figure differs from live cohort-tool result for the same segment by more than a defined threshold | P2 | Correct narrative; re-evaluate any deprioritized cases from same segment |
| Stale-benchmark pattern recurrence | Multiple comparative claims across cases skip the cohort tool within a rolling window | P3 | Audit tool-use policy enforcement for the retention agent |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Aegis: Agent-Environment Failures in LLM-Driven Agentic Systems](https://arxiv.org/html/2508.19504)
