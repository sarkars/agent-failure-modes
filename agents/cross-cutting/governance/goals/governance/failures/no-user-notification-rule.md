# No User Notification Rule

## Issue: Users are not told AI is acting or making decisions where needed.

**Frequency**: Occasional

**Symptoms**
- User confusion or compliance gap.
- [Add more specific symptoms]

**Root Cause**
Users are not told AI is acting or making decisions where needed.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
