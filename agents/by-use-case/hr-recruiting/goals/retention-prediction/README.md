# What Are the Most Common Retention Prediction Failures in AI Agents?

**Retention-prediction agents fabricate conversational details in risk-score narratives that are not grounded in any source record, use stale industry-attrition benchmarks instead of querying live cohort-comparison tools, and anchor risk scores to mismatched historical-employee analogs selected by name or description similarity rather than by structured risk-factor alignment.** The most damaging failure is self-fulfilling feedback: once an attrition-risk score is visible to managers, those managers deprioritize the flagged employee for growth opportunities, causing the predicted attrition to materialize as a consequence of the prediction itself rather than the pre-existing risk. These patterns cluster around narrative grounding, benchmark staleness, retrieval mismatches, and score visibility feedback loops.

## Key Takeaways

- 5 distinct failure patterns affect employee attrition prediction, grouped into four mechanisms: narrative hallucination without source grounding, benchmark staleness (industry baselines override live internal data), mismatched-cohort retrieval, and self-fulfilling feedback loops from manager behavior.
- Retention-risk narratives containing unsourced conversational details (fabricated 1:1 notes, invented quote fragments) occur at "occasional" frequency, with no corresponding source document retrievable, yet are treated as factual by HR business partners and influence retention interventions.
- Stale industry-attrition benchmarks replace live cohort-comparison tools in 5-10% of risk contextualization statements, leading HR to characterize elevated scores as "in line with peers" when internal data shows the department's actual attrition has shifted sharply post-reorganization.
- Feedback-loop self-fulfilling: high-risk-flagged employees systematically receive fewer stretch assignments and slower promotion consideration than unflagged peers, directly increasing their actual attrition independent of whether the model's original risk factors were predictive.

## Scope

- **Narrative Hallucination Without Grounding** — [retention-agent-fabricates-manager-conversation-detail-not-present-in-any-source-note](failures/retention-agent-fabricates-manager-conversation-detail-not-present-in-any-source-note.md). Free-text narrative explanations for risk scores construct plausible-sounding details (quotes, dated conversations) connecting available contextual elements without those elements appearing in any actual source document.
- **Benchmark Staleness & Tool Avoidance** — [stale-training-corpus-industry-attrition-benchmark-overrides-live-cohort-tool](failures/stale-training-corpus-industry-attrition-benchmark-overrides-live-cohort-tool.md). Relative-risk contextualization uses generic industry-average attrition rates from pretraining instead of calling the live internal cohort-comparison tool, producing "in line with peers" characterizations that diverge from actual department-level baselines.
- **Cohort-Mismatch Retrieval** — [embedding-retrieval-pulls-mismatched-historical-attrition-cohort-as-comparable](failures/embedding-retrieval-pulls-mismatched-historical-attrition-cohort-as-comparable.md). Risk scores anchored to retrieved departed-employee precedents select the lexically most similar but structurally most mismatched analog — shared title/tenure but different actual attrition drivers (relocation vs. compensation).
- **Multi-Agent Handoff Loses Recent Comp Changes** — [multi-agent-handoff-drops-confirmed-comp-adjustment-before-retention-risk-rescoring](failures/multi-agent-handoff-drops-confirmed-comp-adjustment-before-retention-risk-rescoring.md). Compensation-review agent confirms off-cycle pay adjustment but that change is not carried in structured handoff to retention-prediction agent, so risk score cites "below-market compensation" for an employee whose pay was already adjusted.
- **Self-Fulfilling Feedback Loop** — [attrition-risk-score-feedback-loop-self-fulfilling](failures/attrition-risk-score-feedback-loop-self-fulfilling.md). Employees flagged high-risk are deprioritized for growth opportunities by managers aware of the score, causing actual elevated attrition as a consequence of reduced investment rather than the original risk factors.

## When Retention Prediction Matters

- A retention-prediction score used to inform manager behavior (who gets stretch assignments, who gets prioritized for promotion conversations) becomes an active intervention, not a passive prediction — the score can materially change the outcome it claims to predict.
- Relative risk ("is this employee high-risk relative to their cohort?") is a different question from absolute risk ("will this employee leave?") and requires accurate cohort baselines; using generic industry benchmarks can mischaracterize departmental or company-specific attrition patterns.
- Attrition-risk interventions (proactive compensation review, development conversation, growth opportunity) are most effective for employees whose risk factors are genuinely addressable; interventions built on fabricated narrative details rather than real, grounded signals waste retention resources and erode trust.

## Cross-Pattern Insight

All five retention-prediction patterns share a vulnerability in how agents bridge from structured risk signals to human-readable justification and action. The underlying risk model may correctly identify structured signals (tenure plateau, compensation percentile, manager-change history), but the narrative explanation layered on top to justify the score to HR business partners is not bound to those signals. When a narrative is generated with access to contextual information (news events, prior interactions) not actually used as model inputs, or when a risk score's baseline benchmark is swapped from a live tool to parametric knowledge, or when a cohort analog is selected by textual similarity instead of structural risk-factor alignment, the confidence and fluency of the score's presentation masks these divergences. Mitigation requires separating decision (structured features) from justification (narrative), grounding every narrative claim in an actual source document or model-attribution result, mandating live tools for decision-relevant baselines, and testing whether manager behavior on flagged employees actually addresses the cited risk factors or simply treats the flag as a deprioritization signal.

## Frequently Asked Questions

### How do you catch narrative hallucinations in risk-score justifications?

Require every specific factual claim in a risk narrative (quotes, dated events, manager-conversation details) to cite the source document or note ID it came from. Strip or flag any claim that cannot be traced to a retrievable source. When free-text manager notes were not actually retrieved for an employee, explicitly state the score is based on structured signals alone; do not fabricate qualitative color.

### What's the difference between a stale benchmark and a mismatched cohort in retention prediction?

A stale benchmark is a single number (industry average attrition, 12%) that's outdated relative to live data. A mismatched cohort is a single departed employee selected as an analog (because their name or role title resembles the current employee) who actually departed for different reasons. Both produce wrong relative-risk characterizations; different detection methods apply (numeric comparison for benchmarks, structured-attribute comparison for cohorts).

### Can a feedback-loop self-fulfilling risk score be distinguished from a genuinely predictive one?

Run a score-visibility holdout experiment: withhold the risk score from managers for a randomized control group and compare actual attrition outcomes. If the visible-score group has higher attrition, the difference is attributable to manager behavior influenced by the score, not just the model's prediction accuracy. This requires deliberate experimental design but is the only way to isolate feedback-loop effects.

### How do you recover when a comp adjustment is confirmed but the retention agent hasn't re-scored?

Immediately trigger a manual re-score using current compensation data before any retention intervention is recommended to the employee. If a retention conversation was already scheduled, surface to HR that the compensation-related risk driver was already addressed and reframe the conversation around any remaining risk factors.

### What causes retention narratives to reference events that didn't affect the score?

When a justification-generation step has access to broad contextual information (news events, organizational changes) not used in the underlying risk model, it constructs plausible-sounding causal links between co-occurring elements. The risk model may have flagged tenure plateau as the driver, but if a regional news event co-occurs in time and geography, the narrative can fluently connect them without any actual dependency. Fix: require narrative claims to cite specific model-attributed features, not contextual background information.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Retention Agent Fabricates Manager-Conversation Detail Not Present in Any Source Note](failures/retention-agent-fabricates-manager-conversation-detail-not-present-in-any-source-note.md) | Narrative explanation generates specific conversation details (quotes, dated 1:1 notes) not grounded in any actual manager note or survey data retrieved |
| [Stale Training-Corpus Industry-Attrition Benchmark Overrides Live Cohort Tool](failures/stale-training-corpus-industry-attrition-benchmark-overrides-live-cohort-tool.md) | Relative-risk contextualization uses generic industry average instead of calling live internal cohort-comparison tool, producing mischaracterized peer comparison |
| [Embedding Retrieval Pulls Mismatched Historical-Attrition Cohort as Comparable](failures/embedding-retrieval-pulls-mismatched-historical-attrition-cohort-as-comparable.md) | Retrieved departed-employee analog is selected by name/role-title similarity but differs in actual attrition drivers (relocation vs. compensation vs. management change) |
| [Multi-Agent Handoff Drops Confirmed Comp Adjustment Before Retention-Risk Rescoring](failures/multi-agent-handoff-drops-confirmed-comp-adjustment-before-retention-risk-rescoring.md) | Compensation-review agent confirms off-cycle pay adjustment but handoff to retention agent lacks updated compensation data; score still cites below-market pay as risk driver |
| [Attrition-Risk-Score Feedback Loop Self-Fulfilling](failures/attrition-risk-score-feedback-loop-self-fulfilling.md) | Employees flagged high-risk are deprioritized for growth opportunities by managers, causing actual attrition as a consequence of manager behavior, not original risk factors |

**Total: 5 patterns**

## Related Goals

- [Candidate Screening](../candidate-screening/) — upstream; hiring bias can propagate into the employee cohort attrition models are trained on, biasing historical attrition patterns.
- [Onboarding](../onboarding/) — new-hire onboarding quality affects early tenure satisfaction and early-attrition risk; onboarding agents that miss accommodations or compliance requirements increase attrition risk.
