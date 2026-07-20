# Required Field Added To API

## Issue
An external API the agent depends on introduces a new required field in its request schema — often as part of a routine vendor update, a compliance requirement, or a new feature rollout — and every existing call the agent makes, built against the prior schema, starts failing validation because the field is absent. Unlike a breaking removal or rename, this failure mode is easy for the vendor to consider "backward compatible" from their side (old fields still work, nothing was removed), while it silently breaks every caller that doesn't proactively track schema changes.

**Frequency**: Occasional

**Symptoms**
- A previously stable API integration begins failing 100% of calls at a specific point in time with a 400-class validation error referencing a field name the agent's request payload never included
- Vendor changelog or API documentation shows a new required field was added, often described by the vendor as a minor or non-breaking update
- The agent's request-building logic has no schema validation step of its own, so the malformed request isn't caught until the external API rejects it
- Error messages naming the specific missing field are available in the API response but not surfaced anywhere the on-call team would see them quickly

## Root Cause
API providers frequently treat adding a new required field as routine evolution — from their side, it's often driven by an external mandate (a new regulatory requirement, a fraud-prevention measure, a new pricing model needing a cost-center tag) and they consider existing integrations responsible for adapting. Agents that build requests from a fixed, hardcoded schema (rather than dynamically introspecting the API's current schema) have no way to detect the change until they experience the failure directly, because nothing in a typical polling or webhook-based agent architecture proactively watches an external API's schema for changes between calls. The gap between "vendor ships a new required field" and "agent's request-building code is updated to include it" is where every call fails.

## Example
```
An expense-reporting agent submits reimbursement requests to a
third-party payments API using a request payload built from a schema
defined 8 months ago: {amount, currency, recipient_id, memo}.

The payments vendor, complying with a new regional tax-reporting
requirement, adds "tax_category" as a required field to the
reimbursement-submission endpoint, announced in their changelog as
"Enhancement: added tax_category field for improved reporting" -- not
flagged as a breaking change because it's additive to the schema, not
a removal.

Starting the day the change goes live, every reimbursement submission
from the expense-reporting agent fails with: {"error": "validation_
failed", "field": "tax_category", "message": "tax_category is
required"}. The agent's error handling logs a generic "submission
failed" message without surfacing the specific field name prominently,
and 340 pending reimbursements queue up unprocessed over the following
2 days before an engineer manually inspects a raw API response and
spots the actual cause.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 5-10% of third-party API integrations experience at least one additive-but-breaking schema change (new required field) per year of active use | Typical range observed in long-running API integration maintenance |
| Integrations using schema-validation-at-build-time or contract testing against the live API catch the large majority of these changes before they cause call failures in production | Reported range across teams using automated schema drift detection |
| Time-to-detection for a new-required-field break is substantially shorter when error responses are parsed for specific field names rather than logged as generic failures | Estimated from comparing incident response times across error-handling maturity levels |

## Mitigations
1. **Schema drift monitoring**: Periodically fetch and diff the external API's published schema (OpenAPI spec, GraphQL schema, or documented field list) against the schema the agent's request-building code assumes, and alert on any divergence.
2. **Detailed error-field surfacing**: Parse validation error responses for the specific field name(s) causing the failure and surface them prominently in alerts, rather than logging a generic "call failed" message that requires manual log inspection to diagnose.
3. **Contract testing against the live API**: Run scheduled integration tests against the actual external API (not just a mock) to catch schema changes as soon as they go live, independent of production task traffic.
4. **Vendor changelog subscription**: Subscribe to the API provider's changelog, deprecation notices, or developer newsletter, and route relevant entries to the team owning the integration rather than relying solely on runtime failure detection.
5. **Graceful degradation for non-critical new fields**: Where the new field has a sensible default, build the agent's request layer to supply one automatically pending a proper fix, rather than leaving every call fully blocked while a manual patch is developed.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| api_validation_error_rate | Rate of external API calls failing with a schema/validation error | Alert if > 1% sustained, or any spike to 100% |
| schema_drift_check_failures | Count of detected mismatches between the agent's assumed request schema and the live API's current schema | Alert if > 0 |
| unrecognized_error_field_count | Count of validation errors referencing a field name not present in the agent's current request-building logic | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Sudden 100% call failure on external API | A previously stable external API integration begins failing all calls with a validation error | High | Parse the error for the specific missing/invalid field, patch request builder, deploy hotfix |
| Schema drift detected | A scheduled schema comparison finds a new required field not present in the agent's request payload | Medium | Update request-building logic proactively before the field becomes required in production traffic |

## Related Patterns
- [Transitive Tool Dependency Failure](./transitive-tool-dependency-failure.md) - both involve an agent's tool integration breaking due to a change in something outside its direct control that it has no visibility into ahead of time
- [Cascading External Failures](./cascading-external-failures.md) - a schema change on one shared upstream API can simultaneously break multiple tools built on top of it
