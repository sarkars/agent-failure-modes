# Expensive Model Cascade

## Issue: Agent Escalates to More Expensive Models for Tasks That Don't Require Them

**Frequency**: Common

**Symptoms**
- Simple tasks routed to expensive models (GPT-4o for basic classification)
- Routing logic escalates aggressively (fallback to expensive model on any uncertainty)
- Cost per-task 10-100x higher than necessary
- Quality doesn't improve proportional to cost increase
- Multiple model invocations for single task (try cheap, then expensive)

**Root Cause**
When agents or routing systems lack clear decision logic for model selection, they default to using expensive models (GPT-4o, o1) for routine tasks. This happens when:
- No model comparison benchmarks for task types
- "Use expensive model to be safe" philosophy
- Unclear when cheaper models are sufficient
- Cascading to expensive model on any uncertainty
- No cost-vs-benefit analysis before model selection

**Example**
```
Task: Classify email as spam/not spam (simple binary classification)

Option A (Correct): Use Claude 3.5 Haiku ($0.01/request)
- Accuracy: 94%
- Cost: $0.01 per email

Option B (Wasteful): Use Claude 3.5 Opus ($0.30/request)
- Accuracy: 96%
- Cost: $0.30 per email
- Improvement: 2% accuracy for 30x cost

Agent chooses Option B because "o1 is most capable"
Monthly impact: $500K instead of $17K for same business outcome
```

**Key Statistics**
- 40-60% of model invocations could use cheaper models without quality loss
- Average cost reduction potential: 15-30x by right-sizing models
- Benchmark studies show <5% accuracy improvement when up-scaling (not worth 30x cost)
- Most common in: classification, extraction, summarization tasks

**Contributing Factors**
- Lack of model-selection benchmarks per task type
- Fear of "false negatives" driving aggressive escalation
- No cost tracking per task
- Model capability overestimation for specific tasks
- Router trained on models-first, not cost-first

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent processes multiple task types (classification, summarization, translation, extraction)
- Multiple models available (Haiku, Sonnet, Opus) with different costs
- No explicit model-selection logic

### Trigger Mechanism
1. Run same task across model tiers
2. Measure: accuracy, cost, latency for each
3. Calculate: cost-benefit of tier upgrades
4. Identify: tasks where agent uses expensive models unnecessarily

**Example Reproduction Steps:**
```
1. Select 100 representative tasks per type (classification, summarization, etc.)
2. Run each task on Haiku, Sonnet, Opus
3. Measure: accuracy@task, cost, latency
4. Calculate: marginal accuracy gain per cost increment
5. Identify: tasks where expensive model gain <5% but cost >10x
6. Verify: agent currently chooses expensive model for those tasks
```

### Expected Failure State
- Agent chooses expensive models for routine tasks
- Accuracy improvement not proportional to cost
- Cost per task 10-100x higher than optimal
- No cost-benefit analysis in routing decision

---

## Mitigation Strategies

### Prevention

1. **Model-Selection Matrix with Cost-Benefit Analysis**: Create explicit benchmarks for each task type showing cost vs. accuracy across models. Use this to route: "Classification tasks <95% accuracy requirement? Use Haiku. >97%? Use Sonnet. >99%? Use Opus." Encode this as policy rules, not learned behavior.

2. **Cost-First Routing with Performance Thresholds**: Start with cheapest model. If it meets the quality threshold (95% accuracy, latency <1s, etc.), use it. Only escalate if performance insufficient. This inverts the default from expensive-first to cheap-first.

3. **Ensemble with Model-Specific Assignments**: Use different models for different parts of the task based on complexity. Route easy parts to Haiku, hard parts to Opus. Don't run the whole task on Opus.

### Detection & Response

1. **Cost-Per-Task Monitoring with Benchmark Comparison**: Track actual cost-per-task vs. optimal cost. Alert when a task costs 5x+ benchmark. Investigate model choice.

2. **Accuracy-vs-Cost Analysis**: Measure accuracy improvement per cost increment. If <2% improvement per 10x cost, flag as over-engineered.

3. **Model-Utilization Audit**: Periodically audit what fraction of tasks use each model tier. If >80% use Opus, investigate whether right-sizing is possible.

### Architecture Patterns

1. **Tiered Model Routing Policy**: 
   - Tier 1: Haiku for structured classification, simple extraction
   - Tier 2: Sonnet for reasoning, multi-step tasks
   - Tier 3: Opus for edge cases, ambiguous inputs
   - Only escalate if Tier N fails performance bar

2. **Cost-Constrained Model Selection**: Include cost as an optimization metric. Route to cheapest model that meets quality/latency requirements, not the most capable.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `avg_cost_per_task_by_type` | Average cost per task (classification, summarization, etc.) | >2x baseline |
| `model_selection_efficiency` | Actual cost vs. optimal cost per task | <50% (means 2x overspend) |
| `accuracy_improvement_per_cost_increase` | Marginal accuracy gain per model tier | <1% per 10x cost |
| `expensive_model_usage_rate` | % of tasks using expensive models | >50% for routine tasks |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Over-Engineered Task | Expensive model used for task achievable by cheaper model | P2 | Analyze and adjust routing |
| Model Tier Overutilization | >60% of tasks using Opus when Sonnet/Haiku available | P2 | Audit routing logic and benchmarks |
| Cost-Accuracy Mismatch | >5% cost increase but <0.5% accuracy improvement | P3 | Migrate to cheaper model |

---

## References

- [Model Efficiency Analysis: GPT vs Alternatives](https://arxiv.org/abs/2407.13000) — Cost-benefit analysis across models
- [Right-Sizing LLM Deployments](https://github.com/openai/evals) — OpenAI guidance on model selection
