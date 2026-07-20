# Domain Risk Blindness

## Issue
An agent operating in a specialized domain fails to flag a risk factor that any competent domain practitioner would immediately recognize as significant, not because the underlying fact is missing from its knowledge base, but because that fact was never tagged or weighted as risk-relevant. The agent retrieves and states the fact correctly when directly asked, yet doesn't proactively surface it as a concern in a context where a domain expert would treat it as a red flag requiring attention.

**Frequency**: Occasional

**Symptoms**
- Agent states a risk-relevant fact accurately when explicitly queried, but omits it from proactive summaries or recommendations where it matters
- Domain experts reviewing agent output ask "why didn't it flag X" about information that was technically present in context
- Risk factors specific to intersections of conditions (drug interactions, combined financial exposures, compounding structural loads) are missed even when each individual condition is known
- No risk-scoring or flagging layer distinguishes "informational fact" from "fact that should trigger a warning"

## Root Cause
General-purpose knowledge retrieval and language generation optimize for relevance and coherence, not for domain-specific risk salience — there is no inherent signal in a passage of text that says "this combination of facts is dangerous," only what a domain expert's trained pattern-recognition would infer from years of case exposure. Without an explicit risk-relevance layer (a taxonomy of known risk patterns, interaction rules, or red-flag combinations specific to the domain) sitting on top of raw retrieval, the agent has no mechanism to elevate a fact from "background information" to "this requires a warning." The knowledge is present; the domain-specific judgment about what that knowledge implies is not.

## Example
```
A financial-planning agent is asked to summarize a client's portfolio
and retirement readiness. The agent has access to records showing: the
client is 61, has 85% of retirement assets in employer stock, and plans
to retire in 3 years.

The agent produces an accurate summary of holdings and a projected
retirement income figure, correctly stating each fact when it appears.
It does not flag the concentration risk of holding 85% of retirement
assets in a single employer's stock so close to retirement — a
textbook red flag any financial advisor would raise immediately,
given the combination of concentration, proximity to retirement, and
lack of diversification.

The client proceeds without addressing the concentration, and a
downturn in the employer's stock price six months before retirement
substantially reduces their available retirement funds.
```

## Statistics
| Finding | Context |
|---------|---------|
| Agents without an explicit risk-flagging layer surface domain-standard red flags in proactive output at an estimated 30-50% rate versus near-total recognition by human domain experts reviewing the same data | Estimated from comparative audits of agent vs. expert review in regulated advisory domains |
| Risk factors arising from a combination of individually-unremarkable facts are missed at a substantially higher rate than single-fact risks | Typical pattern observed in domain-expert review of agent output |
| Adding a structured, domain-specific risk-pattern checklist to the generation step raises red-flag surfacing rates significantly in tested deployments | Reported range across teams that added risk-pattern layers |

## Mitigations
1. **Explicit risk-pattern taxonomy**: Build and maintain a structured list of known domain risk patterns (interaction effects, concentration thresholds, combination red flags) and check retrieved facts against it explicitly, rather than relying on the generating model to infer risk salience from raw text.
2. **Mandatory risk-scan step**: Add a distinct generation step, separate from the primary summary/response, whose sole purpose is to scan available facts against the risk taxonomy and surface matches before finalizing output.
3. **Domain-expert-sourced red-flag rules**: Derive risk-pattern rules directly from domain expert review of past cases and near-misses, rather than assuming general-purpose relevance ranking will surface them organically.
4. **Combination-risk testing in evaluation**: Specifically test agent behavior on scenarios where risk arises only from the combination of individually-benign facts, since single-fact risk detection is a much lower bar and passing it provides false confidence.
5. **Human review gate for risk-scan misses**: Route cases where the risk-scan step finds zero matches, in domains with historically high red-flag rates, to human review as a backstop against taxonomy gaps.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| risk_flag_surfacing_rate | Rate at which known risk patterns present in available data are actually surfaced in proactive agent output | Alert if < 90% against a labeled benchmark set |
| combination_risk_miss_rate | Miss rate specifically for risks arising from fact combinations vs. single facts | Track separately; alert if markedly worse than single-fact miss rate |
| zero_flag_session_rate | Share of sessions in risk-relevant domains producing zero risk flags | Alert if trending toward implausibly low rates given domain base rate |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Known risk pattern unflagged | Post-hoc audit or expert review finds a taxonomy-matched risk pattern present in data but absent from output | High | Investigate risk-scan step failure, add case to taxonomy test set |
| Risk-scan step returns empty on high-base-rate domain | Risk-scan step yields zero flags in a domain where the historical flag rate is well above zero | Medium | Trigger human review, audit risk-scan step for regression |

## Related Patterns
- [Domain Constraint Violation](./domain-constraint-violation.md) - a hard-constraint version of the same "domain-specific significance not captured by generic retrieval" mechanism
- [Domain Exception Not Handled](./domain-exception-not-handled.md) - both involve domain judgment not encoded in retrieval ranking, one for exceptions and one for risk salience
- [Domain Rule Misunderstanding](./domain-rule-misunderstanding.md) - shares the underlying gap between literal fact retrieval and domain-expert-level judgment
