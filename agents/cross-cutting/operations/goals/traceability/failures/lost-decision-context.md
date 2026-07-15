# Lost Decision Context

## Issue: Cannot Understand Why Agent Made Specific Decisions

**Frequency**: Common

**Symptoms**
- Agent output correct but reasoning unknown
- Cannot explain decision to stakeholders
- Policy compliance unverifiable
- Cannot distinguish bug from feature
- Improvement impossible without understanding

**Root Cause**
Agents make decisions through complex reasoning processes that aren't captured in outputs. The final action is logged, but the chain of reasoning—what information was considered, what alternatives were evaluated, what trade-offs were made—is lost. This makes it impossible to understand, explain, or improve agent decision-making.

**Example**
```
Loan Application Decision:

Output logged:
  {
    "decision": "DENIED",
    "application_id": "APP-12345",
    "timestamp": "2026-04-15T10:30:00Z"
  }

What's missing:
  - Which factors contributed to denial?
  - What was the confidence level?
  - Were there borderline considerations?
  - What would have changed the decision?
  - Did the agent consider all required factors?
  - Was this consistent with similar applications?

Customer complaint:
  "Why was I denied? I have good credit."

Investigation:
  - Can't explain the specific denial
  - Can't verify discrimination didn't occur
  - Can't check if policy was followed
  - Can't improve decision quality

Regulatory inquiry:
  "Provide the factors that led to this adverse action"
  
Response: "We don't have that information"
          → Compliance violation
```

**Key Statistics**
From AI Governance Research (2026):
- Explainability requirements in EU AI Act, CCPA, ECOA
- Most agent frameworks don't capture reasoning
- "Right to explanation" increasingly enforced
- Unexplainable decisions create legal liability
- Trust requires understanding, not just accuracy

**Lost Context Types**
| Context | Importance | Typical Capture |
|---------|------------|-----------------|
| Input factors considered | Critical | Rarely |
| Weights/importance | High | Almost never |
| Alternatives evaluated | High | Rarely |
| Uncertainty/confidence | Medium | Sometimes |
| Policy rules applied | Critical | Sometimes |
| Similar case comparisons | Medium | Rarely |

**Contributing Factors**
- LLM reasoning is implicit in weights
- Chain-of-thought not always captured
- Structured logging not implemented
- Focus on outcomes, not process
- Explainability seen as optional

## Mitigation Strategies

### Prevention
1. **Mandatory factor-attribution logging for adverse decisions**: For any decision with real consequences (loan denial, account action), require the pipeline to log which specific input factors contributed to the outcome and their relative weight, not just the final `"decision": "DENIED"` record — directly closes the gap that left the regulatory inquiry with "we don't have that information." Trade-off: factor-attribution logging adds structure and overhead to every decision path, including the many low-stakes ones that don't strictly need it.
2. **Policy-checkpoint logging at each rule evaluation**: Record which policy rules were checked and their pass/fail result as part of the decision process, so "was this consistent with policy" and "did the agent consider all required factors" are answerable from the log rather than requiring reconstruction. Trade-off: requires the decision logic itself to expose rule-checkpoint hooks, which is a design requirement on the decisioning system, not just the logging layer.
3. **Confidence and borderline-case logging**: Capture the decision's confidence level and whether it was a borderline call, since "were there borderline considerations" and "what would have changed the decision" are unanswerable without this — a denial issued with 51% confidence needs to be distinguishable from one issued with 99% confidence for both explanation and quality-improvement purposes. Trade-off: confidence scores from LLM-based decisioning are themselves imperfectly calibrated and need their own validation before being treated as reliable explanatory data.

### Detection & Response
1. **Explanation-request fulfillment tracking**: Measure what fraction of "why was I denied" customer or regulatory requests can actually be answered with logged factor/policy data versus resulting in "we don't have that information" — this is the exact failure surfaced in the example and is directly measurable as a fulfillment rate.
2. **"Why did it do that?" question-frequency monitoring**: Track how often stakeholders (customers, compliance, internal reviewers) ask for an explanation the current logging can't provide, using frequency as a leading indicator of where decision-context capture needs to be added before it becomes a compliance incident.
3. **Compliance-audit-finding tracking**: Log and trend audit findings specifically related to unexplainable decisions, since "unexplainable decisions create legal liability" is the named consequence and audit findings are the concrete evidence of that liability materializing.

### Architecture Patterns
1. **Structured decision-record schema captured at decision time**: Define and enforce a schema (factors considered, weights, alternatives evaluated, policy checkpoints, confidence) that every consequential decision must populate as part of its execution, rather than layering logging on afterward. Deployment consideration: requires redesigning the decisioning pipeline to expose these internals, which is a bigger investment than adding a log statement after the fact — but is what makes the EU AI Act/ECOA "right to explanation" requirement actually satisfiable.
2. **Explanation-generation service built on the structured decision record**: Generate a human-readable rationale from the structured factor/policy/confidence record (not from asking the LLM to retroactively rationalize a decision it already made), so the explanation is grounded in what was actually recorded rather than a plausible-sounding post-hoc story. Deployment consideration: requires the structured record to exist first; without it, "explanation generation" risks producing confident-sounding fabricated rationale, which is its own accuracy failure mode.
3. **Similar-case comparison index for consistency verification**: Maintain a queryable index of past decisions with their factor records so a new decision can be checked for consistency against similar historical cases, directly supporting "was this consistent with similar applications" and providing discrimination-verification capability. Deployment consideration: needs careful design to avoid the comparison index itself encoding and perpetuating past biased decisions.

### Metrics
1. **explanation_fulfillment_rate**: % of explanation requests (customer or regulatory) answerable from logged decision-context data; target > 95%; alert if < 80%.
2. **factor_attribution_capture_rate**: % of consequential decisions with logged factor attribution and weights; target 100% for regulated decision types (loans, adverse actions); alert if < 95%.
3. **policy_checkpoint_logging_rate**: % of decisions with logged policy-rule-evaluation results; target 100% for regulated categories; alert if < 90%.
4. **compliance_audit_finding_rate**: Number of audit findings per quarter related to unexplainable decisions; target 0; alert on any nonzero finding for a regulated decision category.

### Alerts
1. **Regulatory Explanation Request Unfulfillable** (P1): Condition — a regulatory inquiry for decision factors cannot be answered from logged data (explanation_fulfillment_rate failure on a specific case). Action: escalate immediately to compliance/legal; treat as an active compliance violation and prioritize retrofitting factor-attribution logging for that decision category.
2. **Factor Attribution Capture Gap** (P1): Condition — factor_attribution_capture_rate falls below 95% for a regulated decision type (loans, adverse actions). Action: block further decisions of that type from shipping without factor logging, or add a compensating manual-review step until the gap is closed.
3. **Compliance Audit Finding on Unexplainable Decision** (P1): Condition — compliance_audit_finding_rate registers any event for a regulated category. Action: treat as a P1 compliance incident; conduct root-cause review of the decisioning pipeline's logging gaps and report remediation timeline to compliance stakeholders.

## References

- [EU AI Act](https://artificialintelligenceact.eu/) - Explainability requirements
- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Transparency requirements
- [Responsible AI Labs: AI Safety 2024](https://responsibleailabs.ai/knowledge-hub/articles/ai-safety-incidents-2024) - Explainability failures
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - Accountability gaps
