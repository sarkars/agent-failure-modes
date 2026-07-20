# Dependency Version Conflicts

## Issue
Two direct dependencies the agent's system relies on each require different, incompatible versions of the same shared transitive dependency (Package X needs library Z at version 1.x, Package Y needs library Z at version 2.x, and 1.x/2.x are not compatible). The package manager either fails to resolve the tree, silently picks one version and breaks the other package at runtime, or (in ecosystems that allow multiple versions to coexist) installs both, producing subtle bugs when an object created by one version's code is passed into code expecting the other version's shape.

**Frequency**: Common

**Symptoms**
- Package installation fails outright with a dependency resolution error naming the conflicting version requirements
- Installation succeeds but one of the two dependent packages throws a runtime error (missing method, unexpected type) because the resolver silently chose the other package's required version
- Two versions of the same library coexist in the dependency tree, and objects/instances created by one version fail `instanceof`/type checks against the other version's class definitions
- A previously working build breaks after adding an unrelated new dependency, because the new dependency's own transitive requirements collide with an existing one
- The conflict only appears in one environment (e.g., a fresh CI install) and not in a developer's local environment with an already-resolved lockfile

## Root Cause
Dependency resolvers work by finding a single version (or, in ecosystems that support it, a minimal set of versions) that satisfies every declared constraint in the tree, and when two packages declare genuinely incompatible constraints on a shared transitive dependency, there is no version that satisfies both simultaneously — the conflict is mathematically real, not a resolver bug. This becomes visible only when the dependency graph actually contains such a collision, which can be introduced at any point by adding a new package whose own requirements weren't checked against the existing tree, and detecting it ahead of time requires actually resolving the full graph rather than reviewing each new dependency in isolation.

## Example
```
An agent's tool-orchestration service depends directly on "http-client-lib"
(pinned to require "core-utils@^2.0.0" for its retry logic) and separately
adds a new direct dependency, "auth-provider-sdk", to integrate a new OAuth
flow. auth-provider-sdk requires "core-utils@^4.0.0" for a newer crypto API,
and core-utils 4.x removed several functions that were present in 2.x,
including the one http-client-lib's retry logic calls.

The package manager resolves the tree by installing core-utils@4.0.0 (to
satisfy the newer, narrower constraint) and, in this ecosystem, does not
install a second copy for http-client-lib since http-client-lib's own
package.json range technically overlaps 4.x due to a loosely specified
caret range the maintainer never tightened.

At runtime, http-client-lib's retry logic calls
core-utils.exponentialBackoffWithJitter(), a function removed in
core-utils 4.0.0. Every HTTP call that hits a retryable error throws
"TypeError: exponentialBackoffWithJitter is not a function" instead of
retrying, silently converting what should have been transient-error
resilience into hard failures across every tool call using http-client-lib,
discovered only when transient network blips started causing full tool-call
failures instead of automatic retries.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 10-20% of new dependency additions to a moderately sized project (100+ existing dependencies) introduce at least one transitive version conflict requiring resolution | Typical range observed in dependency-tree change analysis |
| Conflicts that silently resolve to a runtime error (rather than failing package installation outright) take an estimated 2-5x longer to diagnose, since the failure surfaces far from its actual cause | Estimated from incident diagnosis time comparisons |
| Projects using lockfiles with reproducible-install verification in CI catch an estimated 80-90% of newly introduced version conflicts before merge | Reported range across teams enforcing lockfile-based CI checks |

## Mitigations
1. **Lockfile-enforced reproducible installs**: Commit a lockfile that pins the exact resolved version of every dependency (direct and transitive), and run CI installs against it in a mode that fails if the lockfile and manifest disagree, catching conflicts at PR time.
2. **Full dependency graph resolution check on every new addition**: Before merging a new direct dependency, resolve the complete graph and diff it against the prior lockfile, specifically reviewing any transitive package that changed version as a result.
3. **Runtime behavior tests at shared-dependency boundaries**: For shared transitive dependencies known to be sensitive (widely used utility libraries), maintain tests that exercise the specific functions your direct dependencies actually call, catching a silently-resolved incompatible version even when installation itself succeeds.
4. **Explicit version overrides/resolutions with justification**: When a genuine conflict must be forced to a single version, use the package manager's override/resolution mechanism explicitly and document why, rather than letting the resolver's default tie-breaking silently decide.
5. **Ecosystem features for coexisting versions where available**: In ecosystems that support multiple versions of the same package coexisting in the tree without collision (isolated dependency scoping), prefer that default over forcing a single shared version when the conflicting packages don't actually need to interoperate.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| lockfile_manifest_drift | Whether a fresh install from the manifest reproduces the committed lockfile exactly | Alert if any drift detected in CI |
| transitive_version_change_count | Count of transitive dependency version changes introduced by a single PR | Alert if unusually high relative to the PR's stated direct dependency change |
| shared_dependency_runtime_error_rate | Rate of runtime errors (missing method/type mismatch) attributable to a shared transitive dependency | Alert if > 0 in production |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Dependency resolution failure in CI | Package installation fails due to an unresolvable version conflict | High | Block merge, identify conflicting constraints, apply override or replace one dependency |
| Silent transitive version change with test failure | A PR's transitive dependency changes trigger a shared-boundary behavior test failure | High | Investigate the specific incompatibility before merge, do not treat as flaky |

## Related Patterns
- [Dependency Version Pinning Conflict](./dependency-version-pinning-conflict.md) - a closely related failure where an explicit pin, rather than an unconstrained transitive resolution, is the source of the incompatibility
- [Transitive Dependency Explosion](./transitive-dependency-explosion.md) - a larger, harder-to-audit transitive tree increases the likelihood and difficulty of diagnosing version conflicts
- [Dependency Breaking Change](./dependency-breaking-change.md) - a version conflict is one concrete mechanism by which an upstream breaking change becomes forced onto a consumer that didn't opt into it
