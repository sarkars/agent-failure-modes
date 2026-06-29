# Multi-Agent Handoff Drops Field-of-Use Limitation Between Clearance Agent and Licensing Agent

## Issue: An IP-Clearance Agent That Reviews an Inbound License and Determines, in Its Own Narrative Analysis, That the Granted Right Is Limited to a Specific Field of Use or Product Line Hands Off Its Finding to a Downstream Licensing Agent Through a Structured "Rights Cleared: Yes/No" Field That Has No Place to Carry the Field-of-Use Limitation, So the Licensing Agent Treats the Right as Cleared for Any Use

**Frequency**: Occasional

**Symptoms**
- Licensing agent's output authorizes use of a third-party patent, trademark, or content license across product lines or markets the original clearance never covered
- The clearance agent's own analysis, when reviewed retroactively, explicitly named the field-of-use restriction (e.g., "licensed for use in the consumer mobile app only; does not extend to the enterprise platform") in prose, but the handoff artifact consumed by the licensing agent contained only a boolean "cleared" flag
- The licensing agent's downstream output (a usage authorization, a product-launch sign-off) shows no awareness that any restriction existed, because its input schema had no field capable of representing one
- Tracing the handoff log shows the field-of-use limitation was generated and then never propagated -- it exists in the clearance agent's transcript but not in the structured record the licensing agent actually consumed
- Re-running the handoff with a structured "scope/field-of-use" field added to the interchange format causes the licensing agent to correctly restrict its authorization, confirming the omission was a schema gap rather than a misjudgment by either agent individually

**Example**
```
Clearance agent reviews an inbound patent license for a sensor technology, used by the company's wearables division
Clearance agent's analysis: "License Section 2.1 grants rights limited to wearable consumer devices; does not cover automotive or industrial sensor applications" -- correctly identifies a field-of-use cap
Clearance agent's handoff to the licensing-authorization agent is a structured record: { patent_id: "US-XXXXXXX", cleared: true, expiration: "2031-04-01" } -- no field for field-of-use scope
Licensing agent, three months later, processes a request from the automotive division to use the same patented sensor technology, sees "cleared: true" for that patent_id, and issues an internal authorization for automotive use
Automotive product ships with the patented technology; the original licensor's audit identifies the field-of-use breach a year later, after the automotive product is already in market
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent system failures frequently originate at agent-to-agent handoff points where information generated correctly by an upstream agent is lost because the downstream agent only consumes a fixed structured interface, not the upstream agent's full reasoning | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| LLM-based agents are documented to fabricate or omit nuance when forced to compress a nuanced finding into a constrained structured field, rather than flagging the field as insufficient to represent the finding | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Execution-provenance research for LLM agents argues that traceable evidence linking a downstream decision to the specific upstream finding it relied on is necessary because handoff schemas do not reliably preserve qualifying conditions attached to an upstream conclusion | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- The interchange schema between the clearance agent and the licensing agent was designed around a binary cleared/not-cleared outcome, with no field anticipating a scoped or conditional clearance
- The clearance agent's full reasoning is logged but not treated as part of the authoritative handoff payload the licensing agent is required to consume
- No validation step rejects a "cleared: true" handoff that lacks an explicit scope field when the source clearance analysis itself contains scope-limiting language
- Field-of-use restrictions are common enough in IP licensing that treating clearance as a simple boolean systematically underrepresents the real shape of most clearance findings

---

## Mitigation Strategies

1. **Structured Scope Field in the Handoff Schema**: Require every clearance-to-licensing handoff to include an explicit scope/field-of-use field, populated from the clearance agent's analysis, with "unrestricted" as an explicit value rather than an implied default
2. **Schema-Completeness Validation**: Before a handoff is accepted, run an automated check comparing the clearance agent's free-text analysis against the structured payload to flag cases where the analysis contains scope-limiting language not reflected in any structured field
3. **Block Boolean-Only Clearance Records**: Reject "cleared: true/false" as a valid handoff format on its own; require at minimum a scope field, even if its value is "no restriction identified"
4. **Per-Division Authorization Cross-Check**: Require the licensing agent to confirm the requesting division or product line matches the scope field before issuing authorization, rather than authorizing based on patent/license ID alone

### Metrics
- Rate of licensing authorizations issued for a patent/license ID where the original clearance record contains scope-limiting language absent from the structured handoff field
- Number of handoffs using a boolean-only cleared field versus a scoped field
- Mean time between a field-of-use breach and detection (internal audit vs. licensor-flagged)

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Scope-language and structured-field mismatch | Clearance analysis contains field-of-use language not present in the structured handoff payload | P1 | Block downstream licensing authorization pending scope-field correction |
| Boolean-only handoff detected | Handoff record lacks a scope field entirely | P2 | Require schema update before authorization proceeds |
| Cross-division authorization on scoped patent | Licensing agent authorizes use for a division not matching a previously recorded scope restriction | P1 | Immediate authorization recall; legal review of actual usage |

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
