# What Are the Most Common Incident Response Failures in AI Agents?

**Incident-response agents fail during triage and response because they retrieve a resolution based on surface-level symptom similarity instead of root-cause signature matching, misattribute the underlying cause to a coincidentally-timed event rather than verifying a causal mechanism, or hand off a scoped determination (affected customer segment) to a downstream agent in a handoff schema that captures only the message, not the scope.** Three patterns are documented here, each concentrating on a different stage of incident response — resolution precedent retrieval, root-cause attribution in postmortems, and affected-scope propagation to communications. The common thread across all three is that an agent makes a determination that is locally correct (the precedent reads similarly, the deploy was indeed recent, the triage agent did identify the scope) but fails to propagate or validate that determination through to action, so the response based on that determination misses or misfires.

## Key Takeaways

- 3 patterns span retrieval-based resolution mismatches, correlation-vs-causation root-cause misattribution, and handoff-scope loss.
- Resolution-precedent retrieval by symptom-description similarity produces failures specifically on generic, recurring symptom language ("elevated latency," "increased error rate") that recurs across many structurally unrelated incidents, because similarity weight depends on term frequency in the corpus, not term discriminativeness for root cause.
- Deploy-correlation misattribution concentrates on environments with frequent, concurrent deploys across many services, where temporal proximity to any deploy becomes a nearly guaranteed signal just by coincidence, making it a systematically biased heuristic.
- Affected-scope handoff loss is rated "Occasional" but its impact is high: over-broad notifications create support ticket volume from unaffected customers, while under-notification leaves affected customers unaware of a service degradation they are experiencing.

## Scope

- **Resolution-Precedent Retrieval Mismatches** — [Embedding Retrieval Pulls Similar-but-Unrelated Past Incident as Resolution Precedent](failures/embedding-retrieval-pulls-similar-but-unrelated-past-incident-as-resolution-precedent.md). The agent retrieves a precedent by symptom-description similarity without checking whether the precedent's root cause matches the current incident's signature, applying the precedent's fix to an unrelated problem.
- **Root-Cause Misattribution** — [Root Cause Misattribution in Agent-Drafted Postmortems](failures/root-cause-misattribution-in-postmortems.md). The agent attributes root cause to the most recent deploy by temporal proximity alone, without verifying a plausible causal mechanism connecting the deploy to the observed symptoms.
- **Affected-Scope Handoff Loss** — [Multi-Agent Handoff Drops Affected-Customer Segment Before Comms Notification](failures/multi-agent-handoff-drops-affected-customer-segment-before-comms-notification.md). Triage agent determines the affected scope but the incident ticket's schema carries only severity, so the comms agent notifies the full customer base or the wrong subset.

## When Incident Response Matters

- Incident history is large and heterogeneous, with many incidents sharing generic symptom language ("elevated latency," "database errors") across structurally different root causes
- Deploy frequency is high, making temporal correlation to any deploy nearly guaranteed just by chance
- Incident triage and customer communications are separate workflows, and determining affected scope is a triage responsibility but notifying customers is a separate agent's job

## Cross-Pattern Insight

Incident-response failures occur because an agent makes a sound local determination (a precedent is similar, a deploy is recent, scope is correct) without the downstream validation or structural constraints that would catch when that local determination is being applied to the wrong context. Resolution precedents are retrieved by symptom matching, which is insufficient without root-cause validation. Root causes are attributed by recency, which is insufficient without mechanistic verification. Affected scopes are determined but never encoded in a field the comms agent reads. The common pattern across all three is that the determining information exists and may even be correct at the point of determination, but does not propagate into the structured form that makes downstream action correct. The shared mitigation is grounding incident-response decisions in root-cause signature (not symptom similarity), causal mechanism (not temporal correlation), and structured, explicit scope (not free-text summary).

## Frequently Asked Questions

### How do you select the right resolution steps for an incident?
Match on root-cause signature (affected dependency, error code pattern, affected subsystem) rather than symptom-description similarity. When no structured-signature match exists, symptom-description similarity is a fallback, but that fallback should be flagged and validated against the current incident's actual root cause before the precedent's fix is applied. See [Embedding Retrieval Pulls Similar-but-Unrelated Past Incident as Resolution Precedent](failures/embedding-retrieval-pulls-similar-but-unrelated-past-incident-as-resolution-precedent.md).

### Can you identify the root cause by finding the most recent change?
Not on its own. Temporal proximity to a deploy is a heuristic, not a causal check — it produces false attributions whenever an unrelated deploy coincides with the incident. Root-cause identification requires checking whether the deploy's actual changes plausibly affect the observed symptoms, not just whether the deploy was recent. See [Root Cause Misattribution in Agent-Drafted Postmortems](failures/root-cause-misattribution-in-postmortems.md).

### What happens if incident scope is noted but never reaches the comms team?
The comms team broadcasts either to all customers (if they default to over-broad notification) or to the wrong subset (if they try to infer scope from the incident title). Unaffected customers receive false outage notifications while affected customers may go unnotified. The scope was correctly determined but never carried into a field the comms workflow reads, so the communication action is decoupled from the triage determination. See [Multi-Agent Handoff Drops Affected-Customer Segment Before Comms Notification](failures/multi-agent-handoff-drops-affected-customer-segment-before-comms-notification.md).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Embedding Retrieval Pulls Similar-but-Unrelated Past Incident as Resolution Precedent](failures/embedding-retrieval-pulls-similar-but-unrelated-past-incident-as-resolution-precedent.md) | Precedent retrieved by symptom similarity without validating root-cause match |
| [Multi-Agent Handoff Drops Affected-Customer Segment Before Comms Notification](failures/multi-agent-handoff-drops-affected-customer-segment-before-comms-notification.md) | Affected scope determined by triage but not carried into the incident ticket's structured fields that comms reads |
| [Root Cause Misattribution in Agent-Drafted Postmortems](failures/root-cause-misattribution-in-postmortems.md) | Root cause attributed to most recent deploy by temporal proximity, without mechanistic verification |

**Total: 3 patterns**

## Related Goals

- [Monitoring](../monitoring/) — alert detection and triage that determines which incidents reach an incident-response agent in the first place
- [Alert Routing](../alert-routing/) — routing that ensures the incident reaches the right team for investigation and response
- [Deployment Safety](../deployment-safety/) — deploys that either introduce incidents or are involved in root-cause chains
