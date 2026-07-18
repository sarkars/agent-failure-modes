# Plugin Compatibility Matrix

## Issue
A tool connector or plugin only officially supports specific combinations of host platform version and tool/API version — a compatibility matrix the vendor publishes but that the agent's deployment doesn't actively validate against. When the deployment environment drifts outside that supported matrix (a platform upgrade, a plugin auto-update, a tool-side version bump), the integration doesn't necessarily fail outright — it often keeps running with subtle, partial breakage that's far harder to diagnose than a clean failure.

**Frequency**: Occasional

**Symptoms**
- The integration works for most operations but fails or produces wrong results on a specific subset of calls, with no obvious pattern at first
- A routine platform or plugin update (not touching the agent's own code) precedes the onset of subtle bugs
- Vendor support, when contacted, points to a compatibility matrix showing the current platform+plugin+tool version combination isn't officially supported
- Behavior differs between two environments running supposedly "the same" integration, because their underlying platform or plugin patch versions differ
- Errors are intermittent or feature-specific rather than total, since some code paths in the plugin still work across versions while others silently break

## Root Cause
Plugins and connectors are typically built and QA-tested against a finite, explicitly enumerated matrix of platform and tool versions, and the vendor makes no correctness guarantee outside that matrix. Automatic updates (platform auto-upgrades, plugin marketplace auto-updates) can silently move a deployment out of its tested combination without anyone deliberately choosing an unsupported configuration. Because unsupported combinations frequently still "mostly work" — the plugin doesn't refuse to load, most API calls succeed — there's no clear failure signal at the moment compatibility is broken; the breakage surfaces later as a specific feature misbehaving, which looks like a logic bug rather than a version-compatibility issue.

## Example
```
1. An agent uses a database platform's official change-data-capture (CDC) plugin to
   stream row-level updates into a downstream processing pipeline. The plugin's published
   compatibility matrix supports database engine versions 14.x and 15.x with plugin
   versions 2.3-2.5.
2. The database platform is auto-upgraded by the infrastructure team from 15.2 to 16.0
   as part of a routine security patch cycle, unaware that 16.x isn't in the plugin's
   supported matrix.
3. The CDC plugin continues running and streaming most row updates correctly, since the
   core replication protocol is largely unchanged between 15.x and 16.x.
4. However, updates involving a specific data type (a newly changed JSON column encoding
   in 16.0) are silently mis-decoded by the plugin, producing corrupted values in the
   downstream stream for that column only.
5. Three weeks pass before a data-quality check on the downstream pipeline flags
   corrupted JSON values, and it takes a support ticket to the plugin vendor to learn
   that database engine 16.x was never in the supported compatibility matrix.
```

## Statistics
| Finding | Context |
|---------|---------|
| Plugin/connector compatibility gaps caused by platform auto-upgrades are a recurring source of subtle, delayed-detection data-quality incidents, with time-to-detection commonly measured in weeks rather than hours | Because partial breakage rarely triggers hard errors or existing alerting |
| Explicitly pinning platform and plugin versions together (rather than allowing independent auto-upgrade) has been observed to prevent the large majority of compatibility-matrix incidents | By removing the silent drift that creates unsupported combinations |
| A meaningful share of "it worked yesterday" integration bugs reported to plugin vendor support, often cited around 20-30%, resolve to an unsupported version combination rather than a genuine plugin defect | Consistent with auto-update mechanisms operating independently of compatibility testing |

## Mitigations
1. **Pin and coordinate version upgrades explicitly**: Treat the platform version, plugin version, and tool API version as a single coordinated unit; require an explicit, tested decision before any one of them is upgraded independently.
2. **Automated compatibility-matrix checks in CI/CD**: Before deploying a platform or plugin upgrade, programmatically check the resulting version combination against the vendor's published compatibility matrix and block the deploy if it falls outside the supported set.
3. **Disable auto-update on critical-path plugins**: Where the plugin marketplace or platform supports it, disable automatic updates for connectors on the critical path, and instead schedule upgrades as deliberate, tested changes.
4. **Data-quality monitoring on plugin-mediated pipelines**: Add automated checks (schema validation, value-range checks, row-count reconciliation) downstream of any plugin-based data pipeline, since compatibility breakage often manifests as data corruption rather than a hard error.
5. **Maintain a known-good version snapshot**: Document the exact tested and supported platform+plugin+tool version combination currently in production, and require any drift to go through the same review as a code change.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `plugin.version_combination_supported` | Boolean/derived signal comparing current platform+plugin+tool versions against the vendor's published compatibility matrix | Alert immediately on any unsupported combination detected |
| `pipeline.data_quality_check_failure_rate` | Rate of downstream data-quality check failures on plugin-mediated data | Alert on any sustained increase above historical baseline |
| `plugin.silent_version_drift_events` | Count of platform or plugin version changes not accompanied by a corresponding compatibility review | Alert on any occurrence |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unsupported version combination detected | `version_combination_supported` evaluates false after any component upgrade | High | Roll back the upgrade or pin to last known-good combination pending vendor confirmation |
| Data quality degradation on plugin pipeline | `data_quality_check_failure_rate` rises after a platform/plugin version change | High | Suspect compatibility-matrix issue first; check recent version changes before assuming a data bug |

## Related Patterns
- [Sdk Version Incompatibility](./sdk-version-incompatibility.md) - closely related: client-library version mismatch versus platform/plugin version mismatch
- [Undocumented Api Behavior](./undocumented-api-behavior.md) - unsupported version combinations often produce behavior that diverges from documentation in the same subtle way
- [Api Version Schema Mismatch](../../tool-capability-limits/failures/api-version-schema-mismatch.md) - a related version-mismatch failure at the wire-schema level rather than the plugin-compatibility level
