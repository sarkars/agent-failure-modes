# Integration Impedance Mismatch

## Issue
Two integrated systems model the same real-world concept using fundamentally different structures or semantics — one represents an address as a single free-text field, the other as five typed sub-fields; one treats a missing value as "unknown," the other as "explicitly empty"; one uses a flat list, the other a nested tree — and every call across the integration boundary requires a lossy or ambiguous translation between the two models. Unlike a one-time schema mismatch that a migration can fix, this is a standing structural incompatibility baked into how each system fundamentally represents the domain, so every single request/response pair pays a translation tax, and some translations are not fully recoverable in either direction.

**Frequency**: Common

**Symptoms**
- A translation/adapter layer between two integrated systems has persistent special-case logic that keeps growing, rather than converging, because the two data models don't map cleanly onto each other
- Round-tripping data through both systems (write to A, read from B, write back to A) doesn't reproduce the original value, because information is lost or defaulted during at least one direction of translation
- The same downstream error recurs for a specific category of input (e.g. multi-value fields, deeply nested structures, a particular null/empty distinction) that one system supports and the other cannot faithfully represent
- Developers maintain a mental (or literal, undocumented) mapping table explaining "how field X in System A corresponds to fields Y and Z in System B," because no schema-level mapping fully captures the relationship
- Adding a new field or capability to either system routinely breaks the integration, because the translation layer was built around the two systems' current shapes rather than a model that tolerates either side evolving

## Root Cause
Impedance mismatch arises because each system's data model was designed independently around its own internal concerns — a relational system optimizing for normalized storage, a document store optimizing for nested read locality, a CRM optimizing for sales-process fields — and neither model was designed with the other as a target. Translating between them requires either discarding information that has no equivalent representation on the other side, inventing a default/convention to fill a structural gap (deciding what an empty list means when the source has no concept of "list" at all), or maintaining an increasingly complex adapter that tries to approximate a mapping that doesn't actually exist cleanly. Because the mismatch is structural rather than a specific bug, no single fix resolves it — the adapter layer absorbs the impedance permanently, and every schema change on either side reopens the mapping problem.

## Example
```
An agent synchronizes customer records between a CRM (which models
"customer address" as a single free-text field, since sales reps
paste in whatever a customer provides) and a shipping-integration API
(which requires five discrete typed fields: street, city, state,
postal_code, country, each independently validated).

The agent's sync adapter uses an LLM call to parse the CRM's free-text
address into the five structured fields before calling the shipping
API. For most well-formed US addresses this works. For an address like
"Apt 4B, 221 Baker St (use side entrance), London" the parser has no
reliable way to map "use side entrance" into any of the five fields -
it either drops the instruction (losing information the customer
explicitly provided) or stuffs it into "street" (corrupting the
field the shipping API's own validation expects to contain only a
street address, causing a downstream validation failure).

Round-tripping in the other direction is equally lossy: when the
shipping API's five structured fields are written back into the CRM's
single text field, the reconstruction uses a fixed field order and
comma-joining convention that doesn't match how the original sales rep
had formatted it, so every synced record's free-text address now looks
subtly different from what the customer or rep originally entered -
a diff with no actual underlying change, that shows up in every audit
log and confuses support staff investigating "who edited this address."
```

## Statistics
| Finding | Context |
|---|---|
| Adapter/translation layers between structurally mismatched systems tend to accumulate special-case branches over time rather than stabilizing, in the absence of a deliberate canonical intermediate model | Typical pattern observed in long-lived point-to-point integrations |
| A significant share of cross-system data-quality complaints in synced systems trace back to lossy field mapping rather than outright sync failures | Estimated from data-quality audits of CRM/ERP/shipping integration pipelines |
| Introducing a canonical intermediate schema between two structurally mismatched systems reduces adapter-layer special-case growth substantially compared to point-to-point translation | Reported range across teams that refactored point-to-point adapters into a canonical-model pattern |

## Mitigations
1. **Canonical intermediate model**: Define an explicit, versioned intermediate representation that captures the domain concept independently of either system's native shape, and translate each system to/from the canonical model rather than writing a direct point-to-point mapping that hardcodes both systems' current structures together.
2. **Make lossy translations explicit and logged**: When a translation cannot faithfully represent a value (a field with no equivalent on the other side), log the drop/default explicitly rather than silently discarding or defaulting it, so data loss is visible and auditable instead of invisible.
3. **Avoid full round-tripping through both systems' native formats**: Treat one system as authoritative for a given field and the other as a derived/read-mostly view where structural mismatch exists, rather than attempting bidirectional sync that requires the mapping to be lossless in both directions.
4. **Contract tests on the translation boundary, not just each system independently**: Test the adapter layer itself against edge cases specific to the structural mismatch (multi-value fields, null-vs-empty, nested-vs-flat), not just each system's own schema validation in isolation.
5. **Version the mapping alongside both systems' schemas**: Track the adapter's field-mapping logic as a versioned artifact that is reviewed whenever either system's schema changes, rather than letting the mapping drift out of sync with either side silently.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| translation_data_loss_rate | Rate of integration calls where the adapter drops or defaults a field due to structural mismatch | Alert if rate increases beyond established baseline |
| round_trip_fidelity_mismatch_rate | Rate at which round-tripped records differ from their original value after a write-read-write cycle across both systems | Alert on any sustained nonzero rate for fields expected to be stable |
| adapter_special_case_branch_count | Count of special-case handling branches in the translation layer, tracked over time | Alert on sustained upward trend without a corresponding schema-review event |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Silent field data loss detected | translation_data_loss_rate rises without a corresponding logged/reviewed schema decision | High | Audit affected records, add explicit logging/handling for the lossy field, notify data owners |
| Round-trip fidelity regression | round_trip_fidelity_mismatch_rate spikes after a schema change on either system | Medium | Review the mapping layer against the new schema, update the canonical model |

## Related Patterns
- [Integration Data Consistency](./integration-data-consistency.md) - impedance mismatch is a structural translation problem at each call; this sibling pattern is a temporal drift problem in shared state over time — a mismatched translation layer often causes the drift this pattern describes
- [Integration API Contract Violation](./integration-api-contract-violation.md) - contract violation is about a provider not honoring its own documented shape; impedance mismatch exists even when both systems perfectly honor their own contracts
- [Dependency Breaking Change](./dependency-breaking-change.md) - a schema change on either side of an impedance-mismatched integration is especially likely to break the adapter layer, since the mapping is already fragile
