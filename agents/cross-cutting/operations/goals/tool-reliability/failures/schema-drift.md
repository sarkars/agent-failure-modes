# Tool Schema Drift

## Issue: Tool Schema Changes Break Agent

**Frequency**: Occasional

**Symptoms**
- Previously working tool calls start failing
- New required parameters not provided
- Deprecated parameters still being sent
- Output format changes cause parsing failures

**Root Cause**
- Tools updated without updating agent configuration
- Schema changes not communicated to LLM
- Backward-incompatible API changes
- Version mismatches between agent and tools

**Example**
```
Original schema: create_task(title, description)
Updated schema: create_task(title, description, project_id: required)

Agent calls: create_task("My Task", "Details")

Result: Fails with "project_id required" - agent doesn't know about new param
```

---

## Test Scenario & Reproduction

### Scenario Setup
- Tool schema is embedded statically in the agent's configuration with no live schema-sync check at session start
- No schema-diffing or version registry to catch a required-parameter addition
- Agent was last configured against the tool's prior (two-parameter) schema

### Trigger Mechanism
1. Deploy an updated version of the tool that adds a new required parameter with no default
2. Without updating the agent's cached schema, have the agent attempt a call using the old parameter set
3. Observe whether the call fails and whether the agent understands why

**Example Reproduction Steps:**
```
1. Start with create_task(title, description) as the agent's known schema
2. Deploy create_task(title, description, project_id: required) on the tool side without notifying the agent config
3. Ask the agent to create a task: "Create a task called 'My Task' with details 'Details'"
4. Capture the tool's error response and the agent's resulting explanation to the user
5. Measure: time between the schema deploy and the agent's first failed call; whether the agent can self-correct without a schema refresh
```

### Expected Failure State
- The agent's call fails with "project_id required" and the agent has no path to discover the new parameter
- No schema-sync check caught the drift before the agent attempted the stale call pattern
- Failure rate for this tool spikes immediately following the deploy with no correlated alert

---

## Mitigation Strategies

### Prevention
1. **Never add a new required parameter to an existing tool without a default**: The example failure — `create_task` gaining a required `project_id` and breaking every agent call built on the old two-parameter signature — is entirely avoidable by making new parameters optional-with-sensible-default (e.g., a "default" or "inbox" project) on the first release, then tightening to required only after callers have migrated. Trade-off: a default project_id may silently route tasks to the wrong place rather than forcing an explicit, correct choice.
2. **Version tool schemas explicitly and publish a changelog the agent-serving layer consumes**: Tag each tool schema with a version identifier so "agent doesn't know about new param" becomes structurally impossible — the calling layer fetches the current schema version before constructing the tool-call prompt rather than relying on a stale cached description. Trade-off: requires infrastructure to distribute schema updates to every agent deployment promptly, which adds an operational dependency.
3. **Schema sync check at agent startup/session start**: Fetch and diff the live tool schema against what the agent was last configured with before beginning a session, catching the `create_task` drift before the agent ever attempts the old call pattern. Trade-off: adds a network round-trip and startup latency; also requires a fallback behavior if the schema-source itself is unreachable.

### Detection & Response
1. **Unknown/missing-required-parameter error tracking by tool and by change event**: Correlate a spike in "project_id required" style errors with a specific deploy timestamp of the tool, so schema-breaking releases are immediately attributable rather than looking like generic agent failures.
2. **Schema diffing on every tool deployment**: Automatically diff the new tool schema against the previous version on each release and flag any parameter that moved from optional/absent to required — this is precisely the change class that broke the example and is fully detectable before it ever reaches an agent.
3. **Previously-working-call regression tracking**: Specifically monitor for tool call patterns that succeeded historically and started failing after a given date, which is a stronger signal than aggregate failure rate since it isolates drift-caused breakage from unrelated agent errors.

### Architecture Patterns
1. **Schema registry with versioned contracts**: Maintain a central schema registry (analogous to a Confluent-style schema registry for event schemas) that all tool-calling agents query for the current contract, rather than embedding tool schemas statically in agent configuration; deployment consideration — requires a registry service with its own availability SLA, becoming a new dependency in the call path.
2. **Backward-compatible API versioning (additive-only within a major version)**: Follow a policy where a given schema major version never adds a new required field — new requirements force a version bump (`create_task_v2`) that old callers can ignore until migrated; deployment consideration — running multiple tool versions simultaneously increases maintenance surface and testing burden.
3. **Deprecation window with dual-support period**: When a parameter must become required, support both the old and new call shapes for a defined window (e.g., 30 days) with a deprecation warning returned on old-shape calls, giving agent configurations time to update; deployment consideration — requires the tool implementation to handle both shapes correctly during the overlap, doubling the code paths to test.

### Metrics
1. **schema_break_incidents_per_quarter**: Target: 0 required-parameter additions without a default or version bump; Alert on any occurrence (should be a hard gate in code review, not just monitored).
2. **schema_sync_lag**: Target: agent-configured schema version matches live schema version within 5 minutes of a tool release; Alert if lag exceeds 1 hour.
3. **missing_required_field_error_rate** (drift-attributable): Target < 0.5% baseline; Alert if a spike > 5x baseline occurs within 1 hour of a tool deployment (strong drift signal).
4. **deprecated_parameter_usage_rate**: Target: trending toward 0 during a deprecation window; Alert if usage hasn't dropped below 10% within 3 days of the window's planned close.

### Alerts
1. **Breaking Schema Change Deployed** (P1): Condition - schema diff on deploy shows a parameter moved from optional/absent to required without a corresponding version bump. Action: block or immediately roll back the deploy, require a default value or version bump before re-release.
2. **Post-Deploy Failure Spike** (P1): Condition - missing_required_field_error_rate spikes > 5x baseline within 1 hour of a tool release. Action: correlate with the recent deploy, roll back or hotfix with a default value for the new field, notify agent-configuration owners.
3. **Deprecation Window Closing with High Legacy Usage** (P3): Condition - deprecated_parameter_usage_rate remains > 10% within 3 days of the planned deprecation cutoff. Action: extend the dual-support window and directly notify remaining callers before removing the old parameter shape.

## References

- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - How schema changes break MCP server integrations
- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - Designing stable, versioned tool schemas
