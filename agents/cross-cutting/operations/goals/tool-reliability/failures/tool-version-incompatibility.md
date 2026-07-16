# Tool Version Incompatibility

## Issue: Agent Uses Tool Incorrectly Due to Version Mismatch

**Frequency**: Occasional

**Symptoms**
- Tool calls fail with unexpected errors
- Parameters that worked before now rejected
- Response format changed, parsing fails
- Deprecated endpoints return errors
- Agent trained on old tool version

**Root Cause**
Tools evolve over time—APIs add parameters, change response formats, deprecate endpoints, or modify behavior. Agents trained or configured with one tool version encounter production tools at different versions. The agent's "knowledge" of the tool becomes stale, leading to calls with wrong parameters, misinterpreted responses, or use of removed functionality.

**Example**
```
Scenario: Agent using payment processing API

Agent trained on API v2.0:
  - Endpoint: /charge
  - Parameters: {amount, currency, card_token}
  - Response: {success: true, transaction_id: "xxx"}

Production API v3.0:
  - Endpoint: /payments/create (v2 deprecated)
  - Parameters: {amount_cents, currency_code, payment_method_id}
  - Response: {status: "succeeded", id: "xxx", ...}

Agent call (using v2 knowledge):
  POST /charge
  {amount: 10.00, currency: "USD", card_token: "tok_123"}

Result:
  - 404: Endpoint not found
  - Agent retries same call
  - Eventually fails with "unknown error"

Root cause analysis:
  - Agent tool description outdated
  - No version negotiation
  - Breaking changes not communicated
  - No schema validation before call
```

**Key Statistics**
From API Versioning Research (2026):
- Average API breaking change frequency: 1-2 per year
- 34% of tool integrations use outdated schemas
- Version mismatch causes 12% of integration failures
- Mean time to detect version mismatch: 2-5 days
- 45% of organizations don't version their tool schemas

**Version Mismatch Types**
| Type | Example | Impact |
|------|---------|--------|
| Endpoint change | /v1/users → /v2/users | 404 errors |
| Parameter rename | user_id → userId | Validation errors |
| Response format | {data: x} → {result: x} | Parse failures |
| Removed feature | endpoint deleted | Complete failure |
| New required param | Added required field | Validation errors |

**Contributing Factors**
- No tool schema versioning
- Static tool descriptions
- No runtime schema validation
- Breaking changes without migration
- Agent training data outdated
- No version negotiation protocol

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent's tool configuration reflects an older API version (fields, endpoint) with no dynamic schema loading
- No runtime pre-call validation against the live API's current schema
- No deprecation shim/translation layer on the provider side

### Trigger Mechanism
1. Migrate the backend API to a new version (renamed endpoint, renamed/restructured fields) while leaving the agent's tool configuration on the old version
2. Have the agent attempt a normal call using its stale knowledge
3. Observe the resulting error and whether the agent can self-correct

**Example Reproduction Steps:**
```
1. Configure the agent with v2.0 knowledge: POST /charge {amount, currency, card_token}
2. Deploy a test backend that has migrated to v3.0: POST /payments/create {amount_cents, currency_code, payment_method_id}, with /charge removed
3. Ask the agent to process a payment
4. Capture the resulting error (expect 404) and the agent's subsequent retry behavior
5. Measure: does the agent retry the identical stale call, or adapt to the new schema?
```

### Expected Failure State
- Agent's call fails with a 404 on the deprecated endpoint
- Agent retries the same stale call shape repeatedly before giving up with a generic "unknown error"
- No pre-call validation or dynamic schema fetch caught the version mismatch before the call was attempted

---

## Mitigation Strategies

### Prevention
1. **Dynamic schema loading at call time instead of static baked-in tool knowledge**: The example's core failure is the agent using "v2.0 knowledge" (`/charge` with `{amount, currency, card_token}`) against a production API that migrated to v3.0 (`/payments/create` with different field names) — eliminate this class of error by having the tool-calling layer fetch the current live API schema/OpenAPI spec at session start rather than relying on the agent's trained or configured knowledge of the tool's shape. Trade-off: dynamic loading adds a dependency on the schema source being available and correctly published, and a stale or broken schema endpoint becomes a new single point of failure.
2. **Runtime pre-call validation against the current schema, not the agent's assumed schema**: Before dispatching `POST /charge {amount: 10.00, currency: "USD", card_token: "tok_123"}`, validate the call shape against the actual current API contract and fail with a specific "this endpoint is deprecated, use /payments/create with {amount_cents, currency_code, payment_method_id}" error rather than letting it hit a bare 404 that the agent can't self-correct from. Trade-off: requires maintaining an always-current schema source separate from the live API itself, or querying the API's own schema endpoint on every session, adding latency.
3. **Deprecation window with the old endpoint still functioning and warning, not immediately removed**: Rather than fully removing `/charge` the moment `/payments/create` ships, keep the deprecated endpoint operational (perhaps proxying to the new one) for a defined window while returning a deprecation warning in the response body, giving agent configurations time to be updated before the old shape starts hard-failing with 404s as in the example. Trade-off: maintaining backward-compatible shims for deprecated endpoints is ongoing engineering cost and can mask the urgency of migrating callers.

### Detection & Response
1. **404-on-known-endpoint tracking as a version-mismatch signal**: The example shows the agent's call resulting in a 404 that it then retries fruitlessly — specifically flag 404s on endpoints the agent's configuration lists as known/supported (as opposed to genuinely-unknown endpoints), since this pattern strongly indicates the agent's tool knowledge has gone stale relative to the live API, distinct from a normal not-found error.
2. **Tool-description freshness audit against the live API**: Given the cited stat that 34% of tool integrations use outdated schemas and mean detection time is 2-5 days, run a scheduled job comparing each configured tool's schema against the live API's actual current schema (via its OpenAPI spec or a canary call) rather than waiting for production failures to surface the drift.
3. **Retry-then-give-up pattern detection**: The example shows the agent retrying the same failing v2-shaped call before eventually failing with "unknown error" — detecting this exact retry-without-adaptation pattern on a specific endpoint is a strong, fast signal of version incompatibility that predates the 2-5 day average detection time cited in the stats.

### Architecture Patterns
1. **Schema registry with explicit version pinning per agent deployment**: Maintain a central registry recording which API version each agent configuration expects, and validate at deploy/session time that the pinned version still matches what the live API serves, catching the v2-vs-v3 mismatch in the example before any call is attempted; deployment consideration — requires disciplined version-bumping discipline on both the API-provider and agent-configuration sides.
2. **API gateway with version translation/adapter layer**: Insert a gateway that accepts legacy-shaped calls (the old `/charge` with `card_token`) and translates them to the current API's shape (`/payments/create` with `payment_method_id`) server-side, buying time for agent configurations to migrate without hard 404 failures; deployment consideration — the translation layer itself becomes a long-lived piece of infrastructure that needs its own deprecation plan eventually.
3. **Contract tests running against the live production API on a schedule**: Automated tests that exercise each tool integration's exact call shape against the real API (or a staging mirror) on a recurring cadence, surfacing breaking changes proactively rather than via the 2-5 day mean-time-to-detect cited in production incident data; deployment consideration — needs safe test credentials/sandbox environments for APIs like payments where test calls have real-world side effects if misconfigured.

### Metrics
1. **schema_staleness_days** (per tool): Target < 7 days since last verified against live API; Alert if > 30 days for any tool with a known active version-change cadence (1-2 breaking changes/year per the cited stat implies periodic checks matter).
2. **version_mismatch_404_rate**: Target < 0.5% of calls to known/configured endpoints resulting in 404; Alert if > 5% over a 1-hour window (strong version-drift signal).
3. **retry_without_adaptation_rate**: Target < 2% of failed calls retried with an identical shape rather than an adapted one; Alert if > 10% for a specific tool (indicates the agent has no mechanism to self-correct on version mismatch).
4. **mean_time_to_detect_version_drift**: Target < 4 hours via contract testing (down from the cited 2-5 day production-detection baseline); Alert if a drift incident's detection time exceeds 24 hours.

### Alerts
1. **Breaking Version Mismatch Confirmed** (P1): Condition - version_mismatch_404_rate spikes above 5% for a critical tool (e.g., payments) over 1 hour. Action: page immediately, especially for payment/financial-transaction tools where a silent failure or retry storm carries real business risk; deploy a translation shim or update the agent's schema source urgently.
2. **Stale Schema Detected by Contract Test** (P2): Condition - a scheduled contract test finds the live API schema diverges from the configured/agent-facing schema. Action: update the tool schema source, notify the team owning the agent configuration, assess whether a deprecation window is needed for a graceful transition.
3. **Retry-Without-Adaptation Pattern** (P3): Condition - retry_without_adaptation_rate exceeds 10% for a tool. Action: investigate whether the agent's error-handling logic needs a specific "schema changed" recovery path, review recent API changelog for that integration.

## References

- [MCP Protocol](https://modelcontextprotocol.io/) - Tool protocol standardization
- [OpenAPI Versioning](https://swagger.io/docs/specification/api-versioning/) - API version management
- [Schema Drift](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - Tool schema issues
- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - Tool design patterns
- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - Version handling
