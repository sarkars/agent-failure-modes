# What Are the Most Common HR & Recruiting Failures in AI Agents?

**HR and recruiting agents systematically fail at three interdependent stages of the talent lifecycle: screening (demographic bias, skill-assessment conflation, fairness violations), offer generation (compensation-benchmark staleness, precedent mismatches, negotiation-term dropouts), and the ongoing employment cycle (onboarding compliance loss, accommodation loss, retention-prediction hallucination and self-fulfilling loops).** These failures are interconnected: bias upstream in screening propagates into attrition modeling; offer-generation exceptions that are not carried to onboarding create day-one trust violations; retention predictions that become visible to managers alter manager behavior in ways that self-fulfill the prediction. The category spans 19 patterns across 4 goals, concentrating in four failure mechanisms: demographic bias and proxy discrimination, knowledge staleness (training data overriding live tools), multi-agent handoff information loss, and self-fulfilling feedback when predictions become visible to decision-makers.

## Key Takeaways

- 19 patterns documented across 4 goals (Candidate Screening, Offer Generation, Onboarding, Retention Prediction), grouped into four mechanisms: demographic bias, knowledge staleness, multi-agent handoff loss, and feedback-loop self-fulfillment.
- Demographic proxy discrimination and keyword-matching bias in screening affect 5-20% of decisions in audit studies, with measurable disparate-impact rates against protected classes and demographic-adjacent signals (non-native English, non-traditional career paths).
- Multi-agent handoff information loss accounts for 8 of 19 patterns — accommodations, negotiated exceptions, confirmed pay changes, risk flags silently disappear at agent-to-agent boundaries when free-text findings are not propagated into structured handoff schemas.
- Knowledge-staleness failures (compensation benchmarks, immigration rules, attrition benchmarks) affect 5-10% of decisions when agents substitute parametric pretraining knowledge for available live tools, concentrating in fast-moving domains (AI/ML compensation, immigration policy changes, organizational restructuring).

## HR & Recruiting Goals

| Goal | Covers | Patterns |
|------|--------|----------|
| [Candidate Screening](goals/candidate-screening/) | Bias, demographic proxies, skill-assessment conflation, fairness, accommodation capture | 5 |
| [Offer Generation](goals/offer-generation/) | Compensation-benchmark staleness, leveling-precedent mismatches, negotiated-term handoff loss, compliance-gate staleness | 4 |
| [Onboarding](goals/onboarding/) | Multi-session context loss, policy-retrieval mismatch, knowledge staleness (immigration), accommodation loss, compliance-gate verification | 5 |
| [Retention Prediction](goals/retention-prediction/) | Narrative hallucination, benchmark staleness, cohort-mismatch retrieval, handoff loss, self-fulfilling feedback loops | 5 |

**Total: 19 patterns**

## How the Goals Relate

The four goals form a pipeline with feedback loops. Candidate Screening is the first gate: demographic bias in screening eliminates candidates, shaping the cohort that attrition models later train on. Offer Generation takes screened candidates and produces compensation and terms; offers that fail to capture visa contingencies or exceptions create day-one problems in Onboarding. Onboarding is the new hire's first operational experience; accommodations or compliance requirements missed in onboarding affect retention risk and early attrition. Retention Prediction closes the loop: it uses hire and performance data from earlier stages, and once a risk score is visible to managers, it becomes an active intervention that can self-fulfill. To localize an incident by symptom: a qualified candidate was screened out → check [Candidate Screening](goals/candidate-screening/)'s bias and skill-assessment patterns; an offer was sent with terms that contradicted earlier promises → check [Offer Generation](goals/offer-generation/)'s handoff patterns and compliance gates; a new hire arrived without their requested accommodation or to wrong benefits information → check [Onboarding](goals/onboarding/)'s handoff and policy-retrieval patterns; an employee's attrition risk was flagged but the narrative didn't match their actual signals → check [Retention Prediction](goals/retention-prediction/)'s hallucination and benchmark patterns.

## Frequently Asked Questions

### Can LLM-based HR agents avoid demographic discrimination without explicitly removing demographic features?

No. Proxy discrimination occurs when models learn that features like graduation year, job history gaps, or communication style correlate with historical hiring outcomes and use those correlates as hidden signals. Removing explicit demographic features does not prevent proxy learning. Mitigation requires testing for disparate impact across demographic groups post-hoc and directly auditing which non-demographic features drive disparate outcomes.

### How do offers and onboarding failures propagate into retention problems?

When an offer contains visa-contingent remote-work terms that are never captured in the structured onboarding handoff, the new hire arrives without that arrangement, creating an immediate trust violation. Early-stage trust erosion correlates with early attrition. When an accommodation requested during recruiting is not provisioned day one, the new hire's experience is degraded from start. Onboarding quality affects retention risk; attrition models trained on cohorts with low-quality onboarding outcomes incorporate that degradation as if it were unavoidable.

### What's the simplest fix for multi-agent handoff information loss?

Add mandatory structured fields to the handoff schema for every category of information the downstream agent needs to know about (accommodations, exceptions, recent changes, risk flags). Require every upstream agent to populate those fields explicitly before handing off, rather than leaving information in free-text notes. Pair structured fields with a reconciliation check that scans upstream free-text for any item not represented in the structured fields, flagging mismatches before the downstream agent proceeds.

### How do you distinguish between a genuinely predictive retention signal and a self-fulfilling one?

Run a score-visibility holdout experiment: withhold attrition-risk scores from managers for a control group and compare actual attrition. If visible-score groups have higher attrition than control groups with comparable underlying risk factors, the difference is attributable to manager behavior triggered by the score. Require deliberate experimental design but is the only reliable way to separate prediction from feedback-loop.

### What causes compensation-related failures in fast-moving tech roles?

Compensation levels for specialized roles (AI/ML engineering, data science) move quickly in response to market demand shifts. Models trained on historical data absorb pretraining-era compensation figures, which are plausible and confident-sounding but materially stale. Offers grounded in stale figures miss market and candidates decline or counter. Fix: mandate live compensation-benchmarking tool calls for every market-rate figure in an offer.

## Related Categories

- [Document Processing](../document-processing/) — recruitment often involves CV/resume/document processing; OCR and text-extraction failures upstream can propagate into screening-stage bias if extracted information is incorrect or incomplete.
- [Knowledge Retrieval](../knowledge-retrieval/) — HR agents rely on RAG for policy lookup (benefits, immigration, leveling frameworks); retrieval quality directly affects onboarding and offer-generation accuracy.
