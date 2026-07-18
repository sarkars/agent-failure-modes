# Api Version Schema Mismatch

## Issue
An agent was built and tested against a specific version of a tool's API schema — field names, types, nesting structure, enum values. When the tool vendor ships a new API version with a changed schema (a renamed field, a restructured nested object, a stricter enum), and the agent's requests still get routed there (via a default-version endpoint, an auto-upgraded SDK, or an account migration), the agent's parsing logic silently misreads or drops fields instead of failing loudly, producing corrupted downstream state rather than a clear error.

**Frequency**: Common

**Symptoms**
- Fields the agent expects to be populated come back empty or null after a vendor release, with no error thrown
- Downstream logic that depends on a specific field's value behaves as if that value were always the default/fallback
- Data quality regressions appear gradually and are hard to pin to a specific deploy, since the agent's own code didn't change
- Vendor changelog mentions a schema change around the same time the regression started, but nobody correlated it
- Requests still return HTTP 200 with a superficially valid response, masking the mismatch

## Root Cause
Many tool providers version their API but don't hard-require callers to pin a version, either defaulting unversioned requests to "latest" or auto-migrating accounts to a new version after a deprecation window. Agents typically parse responses with permissive deserialization (accessing fields by name, treating missing fields as null/default rather than raising an error) because strict schema validation adds friction during normal development. When a field is renamed or restructured, permissive parsing means the agent doesn't throw a parse error — it just silently gets `null` or a default value where it used to get real data, and that default often looks like valid input to downstream logic.

## Example
```
1. An agent integrates with a CRM's REST API v2, reading a `contact.status` field with
   values like "active", "churned", "trial" to drive a retention workflow.
2. The vendor ships API v3, renaming `contact.status` to `contact.lifecycle_stage` and
   changing enum values to "customer", "lapsed", "prospect". v2 is marked deprecated but
   still nominally supported.
3. Six weeks later, the vendor auto-migrates all accounts without an explicit version
   pin to v3 as part of a "sunset v2" rollout, silently changing the response shape for
   requests that didn't specify `Api-Version: 2`.
4. The agent's parsing code does `response.get("contact", {}).get("status")`, which now
   returns `None` for every contact since the field was renamed.
5. The retention workflow's branch logic treats `None` as "not churned" by default,
   so churned customers stop being flagged for outreach entirely.
6. Three weeks pass before a business analyst notices retention outreach volume has
   dropped to near zero and traces it back to the schema change.
```

## Statistics
| Finding | Context |
|---------|---------|
| Unpinned API version usage is a factor in a significant share of "silent regression after vendor update" incidents, commonly estimated around 20-35% of integration incidents | Consistent with default-to-latest versioning being widespread |
| Time-to-detection for schema mismatches that don't produce parse errors is typically measured in weeks, versus hours for mismatches that throw hard errors | Because silent field drift has no error-rate signal to trigger alerting |
| Adding schema validation (strict deserialization against an expected schema) at the integration boundary catches a large majority of these mismatches immediately, often cited above 90% | By converting silent drift into an immediate parse failure |

## Mitigations
1. **Explicit version pinning**: Always specify the API version explicitly in every request (header, URL path, or query param) rather than relying on the account/tool default, so vendor-side version changes never silently affect the agent.
2. **Strict schema validation at the integration boundary**: Validate responses against an explicit expected schema (e.g., a JSON schema or typed model) and raise a hard error on unexpected shape, rather than permissively defaulting missing fields to null.
3. **Subscribe to vendor deprecation and changelog notifications**: Track the vendor's API changelog/deprecation calendar and treat "version sunset" dates as hard deadlines for a planned migration, not a surprise.
4. **Contract tests against the live API**: Run scheduled integration tests that assert on exact response shape against the production API, so a vendor-side schema change is caught by a test failure before it reaches production data flows.
5. **Alert on unexpected null/default rates**: Monitor the proportion of records where a critical field comes back null or default-valued, and alert on statistically significant jumps, since a schema rename often produces a step-function change in null rate.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `integration.field_null_rate` | Percentage of responses where a critical expected field is null/missing | Alert on a step change greater than 20 percentage points day-over-day |
| `integration.schema_validation_failure_count` | Count of responses failing strict schema validation | Alert on any occurrence in production |
| `integration.unpinned_version_request_pct` | Share of outbound requests not specifying an explicit API version | Alert if above 0% for any production traffic |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Sudden spike in null critical fields | `field_null_rate` jumps sharply within a single day with no code deploy | High | Check vendor changelog for recent schema/version changes, pin to known-good version |
| Schema validation failures begin appearing | Any `schema_validation_failure_count` > 0 | High | Halt writes derived from the malformed field until schema is reconciled |

## Related Patterns
- [Undocumented Api Behavior](../../tool-integration-limits/failures/undocumented-api-behavior.md) - both involve reality diverging from what the agent's integration code assumes
- [Deprecated Endpoint Retirement](./deprecated-endpoint-retirement.md) - schema mismatches often precede outright endpoint retirement in a vendor's deprecation cycle
- [Sdk Version Incompatibility](../../tool-integration-limits/failures/sdk-version-incompatibility.md) - related failure where the client library itself, not just the wire schema, falls out of sync with the server
