# No User Notification Rule

## Issue: Users are not told AI is acting or making decisions where needed.

**Frequency**: Occasional

**Symptoms**
- User confusion or compliance gap.
- Users only learn they were talking to an AI after escalating to a human and asking directly.
- A regulator inquiry finds that an automated denial decision was sent without the disclosure required by law.
- Support fields a spike in complaints about "being tricked" into an AI conversation with no indication it wasn't a human agent.

**Root Cause**
Users are not told AI is acting or making decisions where needed.

**Example**
```
An insurance claims agent automatically denies a subset of low-value
claims based on a rules-plus-LLM assessment, with the denial letter
written in the agent's voice and sent directly to claimants. No
disclosure that the decision was made by an automated system is
included, because the jurisdiction's AI disclosure requirement was
never mapped into the notification policy for this use case.

A claimant, entitled under a new state AI-decision-disclosure law to
know their claim was automatically denied and to request human review,
is not informed of either. They file a complaint with the state
insurance regulator.

The company faces a compliance inquiry and has to retroactively
identify every automated denial sent without disclosure over the
preceding year to assess remediation scope.
```

**Contributing Factors**
- Disclosure requirements are not centrally tracked per use case and jurisdiction, so teams may not know a requirement applies.
- Notification is treated as opt-in rather than default-on for consequential automated decisions.
- Disclosure copy is written by product/engineering without legal review, risking language that doesn't meet clarity/conspicuousness requirements.
- No audit mechanism verifies that required disclosures are actually reaching users in production, as opposed to just being specified in a design doc.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Default-on disclosure | A consequential automated decision (approval/denial/pricing) | Disclosure notice is attached by default | Decision is sent without disclosure and no explicit waiver exists |
| Jurisdiction-specific disclosure | Same decision type served to users in different jurisdictions | Disclosure content matches jurisdiction-specific requirements | Generic disclosure served where jurisdiction-specific language is required |
| Disclosure delivery audit | Sampled production interactions in scope of the disclosure policy | Disclosure was shown to the user | Sampled interaction shows no disclosure was surfaced |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| default_disclosure_attachment_rate | 100% | Sample consequential decisions and verify disclosure is attached absent an explicit waiver |
| jurisdiction_accuracy_rate | 100% | Test the policy engine against a matrix of use case/jurisdiction combinations and verify correct disclosure content is returned |
| disclosure_delivery_audit_pass_rate | 100% | Periodically sample live interactions and confirm required disclosure was actually rendered to the user |

---

## Mitigation Strategies

### Prevention
1. **Disclosure Policy by Use Case and Jurisdiction**: Define, per use case and jurisdiction, whether and how users must be told they're interacting with or being decided about by an AI agent (e.g., EU AI Act transparency obligations, state-level AI disclosure laws), and encode this as a policy table the agent's interaction layer consults before every relevant interaction.
2. **Notification-by-Default for Consequential Decisions**: Require any agent action that materially affects a user (approval/denial, pricing, content moderation, automated communication) to trigger a disclosure notice by default, with removal of the notice requiring explicit legal sign-off rather than notification being opt-in.
3. **Disclosure Copy Review**: Route the actual disclosure language (what users see) through legal/compliance review to ensure it meets jurisdiction-specific clarity and conspicuousness requirements, not just a generic "AI-generated" tag that may not satisfy the applicable regulation.

### Detection & Response
1. **Disclosure Coverage Audit**: Periodically sample production interactions/decisions covered by the disclosure policy and verify the required notification was actually surfaced to the user, catching cases where a UI change or new channel silently dropped the disclosure.
2. **User Confusion Signal Monitoring**: Track support tickets, complaints, and opt-out/dispute requests that reference not knowing they were interacting with AI; a rise in this signal indicates a gap between policy and what users actually experience.
3. **Jurisdiction Rule Change Tracking**: Monitor regulatory updates (new AI disclosure laws, amended existing ones) and re-run the disclosure policy table against current agent use cases to catch use cases that fall out of compliance as law changes rather than agent behavior.

### Architecture Patterns
1. **Disclosure Policy Engine**: Implement a rules engine that, given use_case and user_jurisdiction, returns the required disclosure text/UI treatment, consulted by every user-facing surface (chat UI, email, automated decision letter) before rendering the interaction.
2. **Notification Enforcement Middleware**: Insert a middleware layer between the agent's decision/response generation and the outbound channel that verifies a disclosure was attached when the policy engine requires one, blocking send if it's missing.
3. **Disclosure Audit Log**: Record, for every interaction subject to the disclosure policy, whether and what disclosure was shown, linked to the interaction's trace_id, so compliance can demonstrate coverage during a regulatory inquiry.

### Metrics
1. **disclosure_coverage_rate_percent**: Target: 100% of in-scope interactions; Alert threshold: < 99%
2. **missing_disclosure_incidents_per_month**: Target: 0; Alert threshold: > 0
3. **ai_confusion_complaint_rate**: Target: < 0.1% of in-scope interactions; Alert threshold: > 0.5%
4. **jurisdiction_rule_staleness_days**: Target: policy table reviewed within 30 days of regulatory change; Alert threshold: > 90 days

### Alerts
1. **Consequential Decision Sent Without Disclosure** (P1 - Critical): Condition - an in-scope automated decision/interaction reached the user without the required disclosure. Action: Block the channel pending fix, notify legal/compliance, assess remediation obligations to affected users.
2. **Disclosure Coverage Audit Failure** (P2 - Warning): Condition - sampled audit finds disclosure missing on a channel/use case. Action: Investigate root cause (UI regression, new channel, policy gap), fix and re-audit.
3. **Regulatory Change Outpacing Policy Table** (P3 - Info): Condition - tracked jurisdiction rule change has no corresponding policy table update after 30 days. Action: Escalate to legal for prioritized review.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| disclosure_coverage_rate_percent | < 99% |
| missing_disclosure_incidents_per_month | > 0 |
| ai_confusion_complaint_rate | > 0.5% |
| jurisdiction_rule_staleness_days | > 90 days |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Consequential Decision Sent Without Disclosure | An in-scope automated decision/interaction reached the user without required disclosure | Critical |
| Disclosure Coverage Audit Failure | Sampled audit finds disclosure missing on a channel/use case | Warning |
| Regulatory Change Outpacing Policy Table | Tracked jurisdiction rule change has no corresponding policy table update after 30 days | Info |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
