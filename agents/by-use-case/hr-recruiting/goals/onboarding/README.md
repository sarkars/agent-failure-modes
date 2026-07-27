# What Are the Most Common Onboarding Failures in AI Agents?

**Onboarding agents lose track of conditional requirements (visa-status-specific tasks, jurisdiction-specific benefits, accommodations) across multi-session workflows, retrieve wrong-jurisdiction benefits policies because embedding similarity favors shared boilerplate over distinguishing clauses, answer immigration questions from parametric pretraining knowledge instead of querying live policy tools, and fail to carry accommodations or exceptions from recruiter pre-boarding conversations into equipment-provisioning tickets.** Onboarding errors affect compliance (visa paperwork, tax withholding missing deadlines), employee experience (accessibility accommodations not ready day one), and operational correctness (wrong benefits eligibility communicated). The patterns cluster around three mechanisms: context loss across sessions, retrieval-induced policy mismatch, and multi-agent handoff brittleness.

## Key Takeaways

- 5 distinct failure patterns affect new-hire onboarding, grouped into three mechanisms: multi-session context loss, embedding-retrieval policy selection, knowledge staleness (immigration rules), and multi-agent handoff loss (accommodations, compliance requirements).
- Conditional onboarding tasks tied to visa status, work state, or employment classification are documented to be lost across multi-session workflows at "occasional" frequency, with compliance deadlines missed as a consequence.
- Wrong-jurisdiction benefits-policy retrieval affects 10-15% of new-hire benefits questions when policies are template-derived with distinguishing clauses representing only a small fraction of embedding space, concentrating in underrepresented employment classifications.
- Immigration-sponsorship guidance diverges from live policy tools in 5-10% of cases where the agent answers from pretraining knowledge instead of querying the live tool, creating filing delays when outdated document lists are submitted.

## Scope

- **Multi-Session Context Loss** — [multi-step-onboarding-agent-loses-context-on-conditional-task-across-sessions](failures/multi-step-onboarding-agent-loses-context-on-conditional-task-across-sessions.md). Conditional requirements established in one onboarding session (this hire is international, needs state-specific tax forms) are communicated to the new hire but not written to structured fields, so later sessions operating from the structured record alone omit the conditional task.
- **Retrieval-Induced Policy Mismatch** — [embedding-retrieval-pulls-wrong-jurisdiction-benefits-policy-during-onboarding](failures/embedding-retrieval-pulls-wrong-jurisdiction-benefits-policy-during-onboarding.md). Benefits policies for different jurisdictions or employment classifications share template-derived boilerplate, so embedding-similarity retrieval returns the dominant (full-time domestic) policy instead of the one matching the new hire's actual classification, producing wrong eligibility terms.
- **Knowledge Staleness & Tool Avoidance** — [stale-training-corpus-visa-sponsorship-rule-overrides-live-immigration-policy-tool](failures/stale-training-corpus-visa-sponsorship-rule-overrides-live-immigration-policy-tool.md). Immigration-sponsorship rules change more frequently than pretraining data refreshes, but the agent answers visa questions from generic pretraining knowledge instead of calling the live company immigration-policy tool.
- **Handoff Loss: Accommodations and Compliance** — [multi-agent-handoff-drops-confirmed-accommodation-before-equipment-provisioning](failures/multi-agent-handoff-drops-confirmed-accommodation-before-equipment-provisioning.md), [onboarding-agent-notifies-manager-of-background-check-clearance-without-verifying-source-status](failures/onboarding-agent-notifies-manager-of-background-check-clearance-without-verifying-source-status.md). Accommodations confirmed in recruiter pre-boarding chat are not carried to equipment-provisioning agents; background-check clearance notifications are sent based on cached state rather than live vendor status.

## When Onboarding Matters

- Onboarding is the new hire's first operational experience with the company and sets the tone for inclusion and trust — missing accommodations or communicating wrong benefits eligibility creates a negative start and compliance exposure.
- Time-sensitive compliance tasks (visa filing, tax elections, state-specific registrations) have hard deadlines that onboarding agents can easily miss if conditional triggers (visa status, work state) are not captured in structured, persistent state.
- Multi-session onboarding workflows (HR coordinator, IT provisioning, payroll, compliance) are the rule in large organizations, making information loss at handoff boundaries a systematic risk rather than an exception.

## Cross-Pattern Insight

All five onboarding patterns share a structural vulnerability: information established conversationally in one agent's session (a conditional requirement, a confirmed accommodation, a benefits-eligibility question) exists only in that session's transcript unless it is explicitly written to a structured, persistent field the next agent will actually read. Onboarding agents that generate checklists or take actions based on structured record fields alone have no visibility into what a prior agent discussed conversationally or noted in free text. When an agent answers from parametric knowledge (immigration rules) instead of calling a live tool, or when retrieval-similarity matching is unconstrained by metadata filters (jurisdiction, employment classification), silent errors accumulate. Mitigation is architectural: every conditional trigger and confirmed commitment must be written to a mandatory structured field before a session ends; every compliance-critical question must route through a live tool; every retrieval must pre-filter by structured metadata; every compliance gate must be verified against live source systems immediately before action.

## Frequently Asked Questions

### How do conditional onboarding tasks get lost across sessions?

Each session operates on the hire's persistent structured record. If a conditional requirement (visa-status-specific tax form, remote-work-state registration) is only established conversationally and never written to a structured field, a later session reading from the structured record sees no flag and omits the conditional task. Fix: require every session that identifies a conditional requirement to write it to a mandatory structured field before the session is closed.

### What's the difference between retrieval-based benefits-policy errors and knowledge-staleness errors in immigration?

Retrieval errors happen at the policy-selection stage — the right policy exists in the system but similarity search returns the wrong one. Knowledge-staleness errors happen at the answer stage — an agent has access to a live tool with current information but answers from pretraining knowledge instead. Both produce wrong guidance; different architectures fix each.

### Can a new hire's benefits information be corrected after onboarding?

Only by retroactive outreach — the new hire has already received and internalized the wrong terms. Mitigation requires accuracy-checking before the information is communicated: validate retrieved policies against the new hire's recorded classification before presenting eligibility terms; mandate live-tool calls for immigration questions before providing guidance.

### How do accommodations get lost in handoffs?

Accommodations are inherently new-hire-specific and non-standard, so they rarely appear in standard handoff schemas (which carry role, start date, manager, standard equipment). Accommodations are also often discussed conversationally and noted in chat rather than recorded in structured fields, making them invisible to downstream agents reading from a fixed schema.

### How do you verify that background-check clearance notifications are safe?

Require the agent sending a clearance notification to make a fresh, synchronous call to the background-check vendor's status API immediately before the notification is sent. The vendor's status field must explicitly equal the defined "clear" value, not just "no longer in progress" or "absent from the internal task list." Quote the literal status and timestamp from the API response in the notification so downstream provisioning teams can verify it if needed.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Multi-Step Onboarding Agent Loses Context on Conditional Task Across Sessions](failures/multi-step-onboarding-agent-loses-context-on-conditional-task-across-sessions.md) | Conditional fact (international hire, remote in new state) established conversationally in one session is not written to structured field; later session's checklist omits the conditional task |
| [Embedding Retrieval Pulls Wrong-Jurisdiction Benefits Policy During Onboarding](failures/embedding-retrieval-pulls-wrong-jurisdiction-benefits-policy-during-onboarding.md) | Template-derived policies for different jurisdictions share boilerplate; embedding similarity retrieves dominant domestic policy instead of classification-specific one |
| [Stale Training-Corpus Visa-Sponsorship Rule Overrides Live Immigration-Policy Tool](failures/stale-training-corpus-visa-sponsorship-rule-overrides-live-immigration-policy-tool.md) | Agent answers visa/sponsorship questions from pretraining knowledge instead of calling live immigration-policy tool, producing outdated document lists and timelines |
| [Multi-Agent Handoff Drops Confirmed Accommodation Before Equipment Provisioning](failures/multi-agent-handoff-drops-confirmed-accommodation-before-equipment-provisioning.md) | Accessibility accommodation confirmed in recruiting-coordinator pre-boarding chat is not captured in structured handoff to provisioning agent; standard equipment ships |
| [Onboarding Agent Notifies Manager of Background-Check Clearance Without Verifying Source Status](failures/onboarding-agent-notifies-manager-of-background-check-clearance-without-verifying-source-status.md) | Access-approval notification sent based on background-check item disappearing from agent's task list, not a re-query of vendor's live "clear" status |

**Total: 5 patterns**

## Related Goals

- [Offer Generation](../offer-generation/) — upstream; visa-contingent offer terms and negotiated exceptions established at offer stage must be carried into onboarding tasks.
- [Retention Prediction](../retention-prediction/) — uses hire and onboarding data; onboarding errors (wrong benefits info, missing accommodations) affect early employee satisfaction and attrition risk.
