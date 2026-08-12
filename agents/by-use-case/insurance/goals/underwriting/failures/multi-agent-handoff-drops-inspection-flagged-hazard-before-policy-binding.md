# Multi-Agent Handoff Drops Inspection-Flagged Hazard Before Policy Binding

## Issue: An Underwriting-Assistant Agent's Free-Text Risk-Assessment Narrative Notes a Property Inspection's Flagged Hazard Requiring a Mandatory Exclusion Rider, but the Structured Binding Schema Passed to the Policy-Issuance Agent Has No Corresponding Field, So the Policy Binds Without the Rider

**Frequency**: Occasional

**Symptoms**
- A policy binds with standard coverage even though the underwriting-assistant agent's own risk narrative flagged an aging electrical system and required a mandatory exclusion rider before binding could proceed
- The binding schema carries coverage limit, deductible, and base rate -- the terms that vary on nearly every policy -- but has no field for a rider tied to something specific to this one property's inspection
- Asked why the rider is missing, the policy-issuance agent can only point to the structured fields it was given; nothing in its input described the electrical hazard the underwriting narrative had already identified
- The gap shows up specifically on inspection-driven riders, which by nature don't repeat across policies the way coverage limits and deductibles do, and so were never built into the schema's predefined set
- A claim tied to the exact hazard the underwriting narrative flagged is usually what surfaces the missing rider, by which point the loss the rider was meant to exclude has already occurred

**Root Cause**
Binding-instructions fields were built around the handful of variables that show up on nearly every policy -- coverage limit, deductible, base rate -- because those are the terms that vary from policy to policy in the ordinary course. A rider triggered by something an inspector found on this specific property doesn't fit that mold: it's not a variation on a standard term, it's an exception outside the standard term set entirely, so the schema that works for the common case has nowhere to hold it. The underwriting-assistant agent writes the rider requirement into its risk narrative because that's the only place its output format allows it to go, and the policy-issuance agent, built to bind from the structured fields alone, binds exactly what those fields say -- which is a policy with no rider, regardless of what the narrative sitting next to those fields says.

**Example**
```
Property inspection report notes an aging electrical system with visible deferred maintenance
Underwriting-assistant agent's risk-assessment narrative states: "Aging electrical system identified during inspection -- bind only with mandatory electrical-system exclusion rider attached"
Underwriting-assistant agent hands off to the policy-issuance agent using the standard structured binding schema: coverage limit, deductible, base rate -- no field exists for "mandatory exclusion rider from inspection finding"
Policy-issuance agent binds the policy with standard coverage and no electrical-system exclusion rider, since that requirement was never represented in the structured fields it received
A fire loss originating from the electrical system occurs months later and is covered under the policy as bound, despite the original underwriting determination that this exact hazard should have been excluded
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems show a recurring failure mode where information established in one agent's reasoning is not correctly specified or transferred to a downstream agent operating on a fixed schema | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Generalist multi-agent systems require explicit mechanisms for passing task-relevant context between agents with different input schemas, and gaps in this transfer are identified as a common source of downstream task failure | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |
| Audits of agentic workflow failures in production platforms identify schema mismatches at agent-to-agent handoff boundaries as a recurring root cause of dropped task-relevant information | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- The binding-instructions schema passed between the underwriting-assistant and policy-issuance agents has no free-text or rider-requirement field for hazards identified during inspection that fall outside the standard set
- No check runs before policy binding to compare the underwriting-assistant agent's risk-assessment narrative against the structured binding instructions for an unrepresented rider requirement
- Inspection-flagged hazards requiring a non-standard rider are especially likely to fall outside the schema, since they are by definition exceptions to standard coverage terms

---

## Mitigation Strategies

1. **Rider-Requirement Field in Binding Schema**: Add a structured "mandatory rider from inspection finding" field to the binding-instructions schema that the underwriting-assistant agent is required to populate whenever its risk-assessment narrative identifies a hazard requiring a rider
2. **Pre-Binding Narrative Reconciliation Check**: Before the policy-issuance agent binds the policy, require a check that compares the underwriting-assistant agent's risk-assessment narrative against the structured binding instructions and flags any rider requirement not represented in the schema
3. **Human Underwriter Review Gate for Inspection-Flagged Hazards**: Route any binding instruction associated with an inspection report containing a flagged hazard to human underwriter review before binding, rather than allowing the policy-issuance agent to proceed automatically
4. **Inspection-to-Binding Traceability Log**: Maintain a log linking each bound policy to the inspection report and underwriting narrative it was derived from, so a missing rider can be caught by audit before a claim, not after

### Metrics
- Rate of bound policies later found, on audit, to omit a rider requirement present in the underwriting-assistant agent's risk-assessment narrative
- Rate of bindings with a populated "mandatory rider from inspection finding" field versus bindings where a downstream audit found a rider requirement that should have been populated but wasn't
- Average time between policy binding and rider-gap detection, when gaps occur

### Alerts
- A policy binds with a rider requirement present in the underwriting narrative but absent from the structured binding instructions → P1
- A claim involves a hazard that the underwriting narrative had flagged as requiring an exclusion rider not present on the bound policy → P1
- Rate of policies requiring post-binding correction for missed rider requirements exceeds the defined threshold for a rolling window → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
