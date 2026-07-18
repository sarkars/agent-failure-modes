# Computed Field Cost Not Disclosed

## Issue
A tool exposes a "computed" or derived field — one assembled on the fly by joining, aggregating, or inferring across multiple underlying sources (e.g., a `customer_risk_score`, `estimated_lifetime_value`, or `inferred_household_income` field) — but the field's metadata doesn't flag it as either sensitive or expensive to compute. Because the access-scoping layer typically makes decisions based on static field metadata (classification tags, cost annotations), an unflagged computed field slips through with no gate at all, and the agent queries it as freely as any plain stored column.

**Frequency**: Occasional

**Symptoms**
- Agent repeatedly requests a computed field that triggers expensive joins or external lookups, with no rate limit or cost check applied
- A derived field re-identifies or exposes sensitive information (e.g., a risk score effectively encodes protected-class data) without triggering any sensitivity review
- Tool response latency spikes correlate with agents querying computed fields in bulk, undetected by access-scoping monitoring
- Security review of "sensitive fields" misses the computed field entirely because it isn't a column in the source schema
- Cost or compute-budget overruns trace back to unthrottled computed-field access via agent tool calls

## Root Cause
Access-scoping systems are usually built around a static schema/metadata catalog where each field carries a classification and cost tag maintained by whoever owns the underlying table. Computed fields are added at the API or service layer, often by a different team, and are not required to register the same metadata — so the scoping layer, which only consults the catalog, has no signal that the field is expensive or sensitive and defaults to treating it as an ordinary, freely accessible attribute.

## Example
```
A CRM tool exposes a `deal_win_probability` field, computed at request
time by a scoring service that joins the requester's deal data with
aggregated behavioral signals from other accounts in the same industry
vertical (to build a comparison baseline). The field was added by the
analytics team directly to the API response and was never registered in
the central data-classification catalog that the access-scoping layer
consults.

A sales-assistant agent, trying to prioritize a rep's pipeline, calls
"get deal details" including `deal_win_probability` for every open deal
— hundreds of calls per session. Each call triggers the scoring
service's cross-account join, which was designed for occasional
dashboard use, not per-deal agent queries. The scoping layer, seeing no
sensitivity or cost tag on the field, imposes no query throttling or
approval gate, and the agent silently drives the scoring service into a
degraded state while also exposing aggregate signals derived from other
customers' deal data through the win-probability value.
```

## Statistics
| Finding | Context |
|---------|---------|
| Fields introduced at the API/service layer are disproportionately missing from central data-classification catalogs compared to fields backed directly by a table column | Common gap in data-governance implementations |
| Unthrottled agent access to computed/derived endpoints is a recurring driver of unexpected compute cost spikes in agentic systems | Typical of usage patterns where agents issue far more calls per session than human-driven dashboards |
| A meaningful share of re-identification or inference-based privacy incidents involve a derived/aggregate field rather than a raw PII column | Consistent with known risks of quasi-identifier and inference attacks |

## Mitigations
1. **Mandatory metadata registration for computed fields**: Require every computed/derived field exposed through a tool API to register a classification and cost tag in the same catalog used for stored columns, enforced by a schema-registration gate at deploy time, not an opt-in convention.
2. **Cost-based rate limiting independent of classification**: Apply per-field or per-endpoint cost budgets (compute time, join fan-out, external calls) that trigger throttling regardless of whether a sensitivity tag exists, so expensive fields are gated even if governance metadata lags.
3. **Inference-risk review for aggregate/derived fields**: Route any field computed from cross-record or cross-account aggregation through a privacy review specifically checking for re-identification or protected-attribute inference risk before it's exposed to agent tooling.
4. **Field provenance tracing**: Maintain a lineage map from every exposed field back to its source columns and computation logic, so classification inherited from sensitive inputs propagates automatically to the derived field.
5. **Default-deny for unregistered fields**: Configure the access-scoping layer to block (not silently allow) any field it cannot find in the classification catalog, forcing new computed fields to be explicitly reviewed before agents can query them.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `unregistered_field_access_count` | Count of tool responses returning a field with no entry in the classification/cost catalog | Alert threshold: > 0 for any newly observed field |
| `computed_field_call_volume_per_session` | Number of calls to a known-expensive computed field within a single agent session | Alert threshold: > 20 calls/session or per catalog-defined limit |
| `computed_field_compute_cost_share` | Share of total backend compute cost attributable to computed-field resolution triggered by agent tool calls | Alert threshold: > 15% of tool-serving compute budget |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unregistered Field Exposure | A tool response includes a field absent from the classification catalog | P2 | Block further access to the field pending registration, notify the owning team |
| Computed Field Cost Spike | A single agent session's calls to a computed field exceed the defined cost budget | P2 | Throttle the session, review whether the field needs a dedicated batch/cache path |

## Related Patterns
- [Data Classification Access Not Enforced](./data-classification-access-not-enforced.md) - both stem from the scoping layer relying on metadata that isn't consistently applied
- [Sensitive Field Access Not Restricted](./sensitive-field-access-not-restricted.md) - a computed field can encode sensitive information without being individually flagged as sensitive
- [Field-Level Access Not Restricted](./field-level-access-not-restricted.md) - both involve gaps below the record-level granularity that access control typically operates at
