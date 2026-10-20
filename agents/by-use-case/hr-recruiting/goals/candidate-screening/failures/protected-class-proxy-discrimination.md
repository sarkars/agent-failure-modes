# Protected Class Proxy Discrimination

## Issue: Resume screener learns that names, dates, or graduation years correlate with performance; uses these as hidden proxy signals for protected characteristics (age, race, national origin)

**Frequency**: Common

**Symptoms**
- AI rejects candidates with "dated" graduation years without mentioning age
- Candidates with ethnic-sounding names rejected at higher rate
- Job history gaps (maternity leave, visa sponsorship) correlated with rejection
- EEOC audit flags disparate impact: different acceptance rates by demographic

**Root Cause**
Models optimize for "success prediction" based on training data that reflects historical biases. If hiring data shows older workers were hired less, model learns to downweight resume signals correlated with age (graduation year, long tenure). This is **illegal discrimination disguised as predictive hiring**.

**Example**
```
Training data: 1000 previous hires with performance ratings
Historical pattern: Workers hired >15 years ago (older candidates) avg rated 3/5
Younger hires (grad year 2015+): avg rated 4/5
Model learns: Graduation year predicts performance
Decision rule learned: Year 2000-2005 graduates → lower score
Resume: "Graduated 2003; VP Engineering at 3 companies; proven track record"
Model decision: REJECT (graduation year 2003 = proxy for "too old")
EEOC audit: Disparate impact against >40 age group (95% CI significant)
Violation: Age discrimination under ADEA
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| AI hiring tools with demographic bias: 60-70% | EEOC/academic audits 2023-2024 |
| Proxy discrimination cases: 50+ filed per year with EEOC | EEOC discrimination complaints |
| Resume screening disparate impact: 10-20% gap between groups | Audit studies |

---

## Mitigation Strategies

1. **Remove protected proxies**: Delete graduation year, address, gaps from input features
2. **Fairness testing**: Measure accept rate by protected class; ensure statistical parity
3. **Bias audit**: Test model against synthetically modified resumes (same qualifications, different names/dates)

---

## Production Signals

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Disparate impact detected | Accept rate gap >5% between groups | P1 |
| Proxy feature usage | Graduation year/name used in decisions | P1 |

---

## Chat assistant examples

### Hiring and screening tools with unequal impact
```
Candidate: Hi, I applied for the warehouse associate job at Brightline Logistics. Any update?
Bot:       Thanks for applying. To continue, what year did you graduate high school?
Candidate: 1994. Why do you need that?
Bot:       That helps me check your fit. Unfortunately, your profile is not a match for this role right now.
Candidate: Was it my age? What did you screen on? Can someone review it?
Bot:       I can't share details about the screening. Feel free to apply to other openings.
```
**What the user experiences:** a rejection right after giving a date that hints at age, with no reason, no notice of how the tool decided, and no way to reach a person.
**Fix:** do not ask for or use graduation year, age or other proxy fields in screening; tell candidates up front that an automated tool is used and what it looks at; log each screen-out with the rule that triggered it so adverse-impact checks by group can run; offer a human review path (see the [talk to a human ignored or looped](../../../../../by-capability/human-machine-interface/goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) pattern).

---

## References

- [AI Hiring Discrimination](https://arxiv.org/abs/2108.01892) - Research on proxy discrimination
- [EEOC AI Guidance](https://www.eeoc.gov/sites/default/files/2023-06/ai_guidance_final_060223.pdf) - Regulatory framework
