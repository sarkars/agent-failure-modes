# Handoff Protocol Version Mismatch

## Issue
The sending agent packages a handoff using one version of the task schema (field names, required/optional fields, encoding conventions) while the receiving agent was built against a different version. The two versions overlap enough that the handoff doesn't fail outright — the receiving agent parses the payload without an error — but fields have been renamed, restructured, or reinterpreted between versions, so the receiving agent either misreads a field's meaning or silently drops fields it doesn't recognize.

**Frequency**: Occasional

**Symptoms**
- Receiving agent successfully parses a handoff payload but acts on wrong or default values for fields that changed meaning between schema versions
- Fields present in the sending agent's payload that never appear in the receiving agent's processed output, with no parse error logged
- Behavior differences correlated with recent deployment of one agent but not the other in the same pipeline
- Debugging reveals the sending and receiving agents were built or last updated against different versions of a shared schema/interface definition

## Root Cause
In multi-agent systems built and deployed independently — different teams, different release cadences, sometimes different codebases entirely — the handoff schema is a shared contract that isn't always versioned or validated as strictly as an internal data structure would be. When one side updates the schema (renaming a field, changing units, deprecating a value in favor of a new one) without a corresponding, coordinated update on the other side, permissive parsing on the receiving end — ignoring unknown fields, defaulting missing ones — hides the mismatch instead of surfacing it. The failure is silent specifically because most schema evolution tooling optimizes for backward compatibility (don't crash on old payloads), which is the same property that lets a receiving agent misinterpret a payload without ever raising an error.

## Example
```
A "lead-qualification" agent hands off qualified leads to a
"lead-routing" agent using a shared schema. In schema v1, the field
"priority" is an integer 1-5. The lead-qualification team ships v2,
which changes "priority" to an enum string: "low"/"medium"/"high", and
adds a new field "priority_score" (0-100) to replace the old numeric
scale. They update lead-qualification-agent to emit v2 payloads.

lead-routing-agent was last deployed against v1 and expects "priority"
as an integer for its routing-threshold comparison
(if priority >= 4: route to fast-lane). It receives "priority": "high"
(a string) in the new payload. Its comparison logic, written in a
loosely-typed language, evaluates "high" >= 4 as a type-coerced
falsy/unexpected result and routes every lead to the standard queue
instead of the fast lane, with no exception thrown.

Three days of high-priority leads are routed to the slow queue before
a sales manager notices response-time SLAs slipping and traces it to
the schema change.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 5-10% of cross-team agent handoff integrations experience at least one schema-version-related silent misbehavior per year of active development | Typical range observed in multi-team agent pipeline maintenance |
| Adding explicit schema version tags and validation at the receiving boundary catches the large majority of version mismatches before they cause behavioral drift | Reported range across teams introducing contract testing on handoff schemas |
| Silent type-coercion-related mismatches (as opposed to outright missing-field errors) take disproportionately longer to detect, often measured in days | Estimated from postmortems on cross-agent schema drift incidents |

## Mitigations
1. **Explicit schema versioning with validation**: Tag every handoff payload with an explicit schema version, and have the receiving agent validate the payload against the version it declares, rejecting (not permissively parsing) payloads it doesn't recognize.
2. **Contract testing across agent boundaries**: Maintain automated tests that exercise the actual handoff interface between sending and receiving agents, run in CI for either agent's pipeline, so a schema change on one side that breaks the other is caught before deployment.
3. **Strict typing and enum validation**: Use strongly-typed schema definitions (not loosely-typed dynamic parsing) for handoff payloads so a type change like int-to-enum fails loudly rather than silently coercing.
4. **Deprecation windows with dual-field support**: When changing a field's meaning or type, emit both old and new fields for a transition period, and monitor which consumers are still reading the deprecated field before removing it.
5. **Centralized schema registry**: Maintain handoff schemas in a shared, versioned registry that both sending and receiving agents reference directly, rather than each team maintaining its own copy that can drift out of sync.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| schema_version_mismatch_count | Count of handoff payloads received with a schema version older or newer than the receiving agent's expected version | Alert if > 0 |
| unrecognized_field_drop_rate | Rate of fields present in handoff payloads but absent from the receiving agent's parsed representation | Alert if > 0% |
| type_coercion_fallback_count | Count of times a field's value required implicit type coercion during parsing | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Schema version mismatch detected | A handoff payload's declared schema version doesn't match the receiving agent's supported version(s) | High | Reject the payload, alert both owning teams, block further handoffs until resolved |
| Behavioral drift correlated with deployment | A downstream metric (e.g., routing distribution) shifts sharply following a deployment on either the sending or receiving agent | Medium | Compare schema versions across the deployment boundary, roll back if mismatch confirmed |

## Related Patterns
- [Handoff Context Incompleteness](./handoff-context-incompleteness.md) - a version mismatch is one specific mechanism that can produce incomplete or misinterpreted context at the receiver
- [Handoff Permission Downgrade](./handoff-permission-downgrade.md) - both are silent degradations that pass a superficial validation check while breaking the task's actual intent
- [Handoff State Loss](./handoff-state-loss.md) - schema mismatches can manifest as apparent state loss when fields are silently dropped during parsing
