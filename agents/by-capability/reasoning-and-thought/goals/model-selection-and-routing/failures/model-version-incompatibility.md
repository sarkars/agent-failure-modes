# Model Version Incompatibility

## Issue
A router selects a model version that doesn't support a specific feature the calling code assumes is available — a particular tool-calling schema format, a structured-output mode, a system-message convention, or a token/parameter that a newer or older version handles differently — causing the call to fail, silently ignore part of the request, or behave unexpectedly. The mismatch arises because routing logic treats models within a family as interchangeable by name/cost/latency, without tracking per-version feature support as a routing constraint.

**Frequency**: Occasional

**Symptoms**
- A tool/function-calling request that works against one model version returns malformed or ignored tool calls against a different version selected by the router for the same logical request type
- A structured-output or JSON-mode parameter accepted by one version is silently ignored or causes an API error on another version in the same routing pool
- Code written and tested against one pinned model version starts failing intermittently once the router begins including a newer or older version in its candidate pool
- Feature-specific bugs appear only for the fraction of traffic landing on a specific version, making them hard to reproduce against the version used for local testing
- Provider release notes describe a behavior or parameter change between versions that the routing/calling code was never updated to account for

## Root Cause
Routing systems commonly group model versions into a pool addressed by a family name or capability label ("fast-tier," "reasoning-tier") for simplicity, but individual versions within that family can differ in exact feature support, parameter names, or default behaviors, especially across major or minor version boundaries from the provider. The calling code is typically written and tested against one specific version during development, and its assumptions about supported parameters or response shapes get baked in without an explicit per-version compatibility check at call time. When the routing pool later expands to include a newer or older version — often for cost or capacity reasons unrelated to the feature in question — nothing in the system verifies that the newly-added version supports every feature the calling code relies on, so the gap is discovered only when a request happens to land on the incompatible version.

## Example
```
An agent's tool-calling integration is built and tested against model
version "reasoner-2.1," which supports parallel tool calls in a single
turn. The calling code is written assuming this: it sends a multi-tool
schema and parses the response expecting possibly multiple tool_call
entries in one message.

Three months later, the routing pool is expanded to include "reasoner-2.0"
for cost reasons during high-load periods, without anyone checking its
feature support. Version 2.0 does not support parallel tool calls - it
returns only a single tool_call per turn - which the parsing code doesn't
account for.

During a load spike, roughly 12% of tool-calling requests route to
2.0. The agent's parser, expecting multiple tool calls, silently
processes only the first one returned and skips the rest, causing partial
task completion (e.g. only one of three requested lookups actually runs)
without raising any error, since the response was well-formed - just
missing the additional tool calls the code assumed would be present.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of routing-pool expansions (adding a new or older version to an existing pool) are not accompanied by a feature-compatibility audit against the calling code's assumptions | Estimated from review of routing configuration change processes |
| Version-incompatibility bugs are disproportionately hard to reproduce, since they only manifest on the fraction of traffic landing on the specific incompatible version | Typical pattern observed in incident postmortems for multi-version routing pools |
| Adding an explicit per-feature compatibility matrix checked at routing time eliminates the large majority of these incidents in subsequent testing | Typical range reported by teams that added this gate |

## Mitigations
1. **Per-version feature compatibility matrix**: Maintain an explicit, tested record of which features (tool calling, structured output, parameter support) each version in the routing pool actually supports, and gate routing decisions against it rather than assuming family-wide uniformity.
2. **Version-pinned integration tests**: Run the calling code's integration test suite against every version in the active routing pool, not just the version used in local development, before adding a version to production routing.
3. **Graceful feature-detection fallback**: Where the provider API supports it, detect feature support at call time (or via response inspection) and adapt parsing/request logic accordingly, rather than assuming a fixed contract across all versions in the pool.
4. **Routing-pool change review gate**: Require any change that adds or removes a version from an active routing pool to go through the same review as a code change to the calling integration, since it functionally is one.
5. **Version-attributed error monitoring**: Tag errors and malformed-response incidents with the specific model version that produced them, so version-specific incompatibilities are visible in aggregate rather than lost in overall error rates.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| version_specific_error_rate | Error/malformed-response rate broken out by model version within a routing pool | Alert if any version's rate exceeds 2x the pool average |
| feature_compatibility_matrix_staleness | Time since the compatibility matrix was last verified against the active routing pool | Alert if > 30 days or after any pool change |
| partial_completion_rate_by_version | Rate of tasks completing only partially (e.g. some tool calls skipped), broken out by version | Alert if any version shows elevated partial-completion rate |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Incompatible version added to pool | A version lacking a required feature is added to a routing pool that depends on that feature | High | Remove version from pool or gate it out of feature-dependent traffic, run compatibility audit |
| Version-specific error spike | version_specific_error_rate breaches threshold for one version in the pool | Medium | Isolate traffic from that version, investigate feature gap |

## Related Patterns
- [Model Capability Mismatch](./model-capability-mismatch.md) - a broader category of the same problem; version incompatibility is the fine-grained, within-family instance of a capability gap
- [Model Switching Mid-Session](./model-switching-mid-session.md) - a version incompatibility discovered mid-session compounds into a continuity break if the switch happens between versions with different feature support
- [Model Selection Nondeterminism](./model-selection-nondeterminism.md) - inconsistent version selection makes version-incompatibility bugs intermittent and hard to reproduce
