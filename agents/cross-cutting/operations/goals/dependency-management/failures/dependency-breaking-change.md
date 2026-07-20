# Dependency Breaking Change

## Issue
A library, SDK, or API the agent's toolchain depends on ships a breaking change — a removed function, an altered response format, a changed default behavior — and the agent's own team has no process that surfaces the change before it reaches production. Automated dependency updates, transitive upgrades pulled in by an unrelated package bump, or a provider's server-side API change (which requires no client-side upgrade at all) all ship the break silently from the agent team's point of view, and it is discovered only when the agent's behavior degrades or a build fails.

**Frequency**: Common

**Symptoms**
- Agent tool calls that worked yesterday start failing or returning subtly different results with no corresponding change in the agent's own code
- A routine dependency bump (patch or minor version) breaks functionality despite semantic-versioning expectations that it shouldn't
- A provider changes server-side API behavior with no client library version change at all, so there is no dependency diff to review
- The breaking change is discovered via a production incident rather than a changelog review, because changelogs weren't monitored
- Rollback is complicated because the breaking change shipped bundled with several unrelated dependency updates in the same deploy

## Root Cause
Dependency version constraints (semver ranges, "latest" tags, auto-merge bots) are designed to let updates flow in with minimal friction, which is good for security patching but means a team can end up running new dependency code without a deliberate decision to adopt it. Semantic versioning is a convention the maintainer promises to follow, not a guarantee enforced by tooling, so "breaking changes only in major versions" is routinely violated in practice, especially by less mature or fast-moving projects. For server-side or SaaS dependencies, there may be no client-visible version at all — the provider can change behavior behind a stable-looking endpoint URL, so even a team that pins every client library version precisely has no artifact to diff against.

## Example
```
An agent's document-parsing pipeline depends on a third-party PDF-extraction
library, pinned with a caret range "^3.2.0" to auto-accept compatible patch
and minor updates. The library publishes 3.4.0, which changes the default
text-extraction mode from "layout-preserving" to "reading-order" to fix a
bug reported by other users -- a change the maintainer considered a bug fix,
not a breaking change, so it ships as a minor version bump.

The agent's dependency-update bot auto-merges the 3.2.0 -> 3.4.0 upgrade
overnight as part of routine maintenance, along with four other unrelated
patch bumps in the same batch PR.

The agent's downstream logic, which relies on layout-preserving extraction
to correctly associate table cell values with their column headers, starts
misreading financial tables in uploaded documents -- numbers get attributed
to the wrong column. Because the change shipped as one of five dependency
bumps in a single auto-merged PR, and no test in the suite specifically
checks table-column association, the regression isn't caught in review and
ships to production, corrupting extracted data for two weeks before a user
reports incorrect figures in a generated report.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 15-20% of "minor" or "patch" version updates in actively maintained open-source libraries include at least one behavior change with observable downstream impact | Typical range observed in dependency-update regression studies |
| Auto-merged dependency updates are associated with a higher rate of undetected regressions than manually reviewed updates, when no dedicated regression tests exist for the affected behavior | Estimated from comparison of auto-merge vs. reviewed-update incident rates |
| Server-side/SaaS dependency changes with no corresponding client version bump account for an estimated 10-20% of "silent breaking change" incidents | Estimated from incident classification in teams tracking dependency-caused regressions |

## Mitigations
1. **Behavior-focused regression tests around dependency boundaries**: Maintain tests that assert on the actual observable behavior your code relies on from a dependency (specific output shape, specific default), not just "the call succeeds," so a silent behavior change is caught even within a semver-compatible bump.
2. **Staged dependency rollout**: Apply dependency updates to a canary or staging environment first, with automated behavior tests and a soak period, before promoting to production, rather than auto-merging directly to the main branch.
3. **Changelog and release-note review gate**: Require a human review of the changelog/release notes for any dependency update above a defined risk tier (core parsing, auth, payment-adjacent) before merge, even when CI passes.
4. **Isolated, single-dependency update PRs**: Avoid batching multiple unrelated dependency bumps into one PR/deploy, so that if a regression appears, the specific change responsible is immediately identifiable without bisecting.
5. **Provider API version pinning where available**: For SaaS/API dependencies that support versioned endpoints (e.g., an explicit API version header or URL segment), pin to a specific version explicitly rather than relying on "latest," and treat provider-announced deprecations as a scheduled migration task.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| dependency_update_regression_rate | Rate at which dependency updates are followed by a behavior-related incident within a defined window | Alert if trending upward |
| unreviewed_auto_merge_count | Count of dependency updates auto-merged without human changelog review, for dependencies above the defined risk tier | Alert if > 0 for high-risk dependencies |
| tool_call_output_shape_drift | Rate of unexpected shape/type/value changes in a dependency's output, detected via contract tests | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Behavior regression after dependency update | A regression test tied to a specific dependency behavior fails following an update | High | Roll back the specific dependency version, file upstream issue, add regression coverage |
| High-risk dependency auto-merged without review | A dependency tagged as high-risk is auto-merged bypassing the changelog review gate | Medium | Audit the merge, retroactively review changelog, tighten auto-merge policy for that dependency |

## Related Patterns
- [Dependency Version Pinning Conflict](./dependency-version-pinning-conflict.md) - pinning strategy is the primary lever for controlling exposure to this pattern, and conflicts often arise from attempts to guard against it
- [Data Pipeline Schema Drift](./data-pipeline-schema-drift.md) - both describe an upstream party changing behavior/shape without adequate downstream coordination, one in a code dependency and one in a data schema
- [Dependency Security Vulnerability](./dependency-security-vulnerability.md) - the same weak dependency-review process that lets breaking changes slip through often also delays vulnerability patching
