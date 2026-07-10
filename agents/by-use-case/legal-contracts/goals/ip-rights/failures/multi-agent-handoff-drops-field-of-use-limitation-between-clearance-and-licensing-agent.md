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

### Prevention

1. **Structured scope/field-of-use interchange schema with validation gates**: Redesign clearance-to-licensing handoff schema to include mandatory fields: {ip_asset_id, license_id, cleared (boolean), scope_type (enum: unrestricted|field_of_use_restricted|product_line_restricted|geographic_restricted|time_restricted), scope_details (string, free-text description), scope_limitations (object {field_of_use: [], product_lines: [], geographies: [], expiration_date: []}), clearance_evidence_doc_id (link to clearance agent's full analysis)}. Validation gate before handoff: if clearance_analysis contains field-of-use keywords ("limited to", "restricted to", "only in", "does not extend"), require scope_type != 'unrestricted' and scope_details populated. Fail-safe: handoff rejected if boolean-only schema used. Root cause: Prevents lossy handoff by enforcing scope as required field.

2. **Handoff schema validation with analysis-to-structure reconciliation**: Before licensing agent receives handoff, automated reconciliation: (a) extract field-of-use keywords from clearance_analysis using NLP, (b) compare extracted restrictions against structured scope_limitations fields, (c) if mismatch found (analysis mentions restrictions not in structure), escalate to clearance agent: "Your analysis mentions field-of-use restrictions. Please populate scope_limitations before handoff." (d) require explicit clearance-agent confirmation that scope_limitations captures all restrictions from analysis. Root cause: Ensures structure matches analysis before handoff.

3. **Per-use authorization gate with scope-checking at usage time**: Licensing agent never issues blanket authorization. Instead: (a) authorization request includes requesting_division/product_line/geography, (b) licensing agent checks request against scope_limitations from clearance record, (c) if request scope matches clearance scope, issue targeted authorization including scope restrictions: "Authorized for [mobile wearable products only] as of [clearance date]", (d) if request scope exceeds clearance scope, return DENIED and escalate to IP team for re-clearance. Root cause: Prevents cross-scope usage by enforcing scope-matching at authorization time.

### Detection & Response

1. **Handoff audit logging with scope-completeness verification**: For each clearance-to-licensing handoff, log: {clearance_id, ip_asset_id, scope_type_specified, scope_limitations_populated (Y/N), clearance_analysis_length, analysis_contains_scope_keywords (Y/N), scope_keyword_count, scope_in_structure (Y/N), mismatch_flag (Y/N), clearance_agent_confirmation}. Daily audit: sample 20% of handoffs from past 24h, verify: scope_type_specified=true, scope_in_structure=true, mismatch_flag=false. Alert if: >5% have mismatch_flag=true, or >10% missing scope_limitations.

2. **Usage audit and scope-enforcement monitoring**: When licensing agent issues authorization, log: {auth_id, ip_asset_id, requesting_division, scope_limitations_from_clearance, scope_match_check_passed (Y/N)}. Monthly: audit actual product usage against authorizations: scan product documentation, codebase, licensing metadata for evidence of IP use. Flag if: product use exceeds authorized scope. Escalate: if out-of-scope usage found, halt product shipment, notify licensor of breach, assess remediation.

### Architecture Patterns

1. **Clearance-Licensing Handoff Schema with Validation Engine**: Clearance agent generates analysis → NLP extracts scope-restriction keywords → Structured handoff schema populated (scope_type, scope_limitations, evidence_doc_id) → Validation: analysis-to-structure reconciliation check → If pass, transmit to licensing agent; if fail, escalate for manual correction. Licensing agent rejects boolean-only payloads.

2. **Per-Use Authorization Gate with Scope Enforcement**: Licensing authorization request includes use-context (division, product, geography). Licensing agent queries clearance record for scope_limitations, compares request context against limitations, issues scoped authorization or returns DENIED + escalation. Never issues unrestricted authorization if scope_limitations present.

3. **Usage Audit & Scope Violation Detection**: Automated product-analysis pipeline (scans product docs, code metadata, license files) identifies IP usage by asset_id. Cross-references against issued authorizations + scope_limitations. Reports out-of-scope usage to IP team for investigation + remediation.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Scope-Field Completeness in Handoffs | 100% | <99% | # of handoffs with scope_limitations populated / total clearance-licensing handoffs |
| Analysis-to-Structure Reconciliation Pass Rate | 100% | <99% | # of handoffs passing analysis-to-structure mismatch check / total handoffs |
| Scoped-Authorization Accuracy | 100% | <99% | # of authorizations correctly matching request scope against clearance scope / total authorization requests |
| Out-of-Scope Usage Detection Rate | >99% | <95% | # of out-of-scope usages detected by audit / total out-of-scope usages actually occurring (validated via IP holder audit) |
| Scope-Restriction Breaches Post-Authorization | 0% | >0.5% | # of scope-restriction breaches discovered post-authorization issuance / total issued authorizations |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Scope-Field Omitted in Handoff | Handoff missing scope_limitations field or scope_type='unrestricted' when clearance_analysis contains scope keywords | CRITICAL | Block licensing agent input; escalate to clearance agent for scope-field population; re-validate before handoff retry |
| Analysis-to-Structure Mismatch | Clearance analysis contains field-of-use language not represented in structured scope_limitations | HIGH | Pause handoff; require clearance agent confirmation that scope_limitations captures all restrictions; re-validate before proceeding |
| Out-of-Scope Authorization Request | Licensing authorization request for product/division outside clearance scope_limitations | CRITICAL | Deny authorization; escalate to IP team; may require re-clearance or licensor re-negotiation |
| Out-of-Scope Usage Detected | Product audit finds IP usage in product line/geography/market not matching clearance scope_limitations | CRITICAL | Halt product shipment; notify licensor immediately; assess remediation (remove IP, re-license, indemnify); escalate to legal/commercial teams |

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
