# Version Compatibility Matrix Explosion

## Issue
An agent platform accumulates enough independently-versioned components — the orchestrator, several tool adapters, a prompt-template library, the underlying model version, a retrieval index schema — that the number of combinations needing to be verified compatible grows multiplicatively rather than additively. What started as "we support the last two orchestrator versions" becomes an unmanageable grid of orchestrator x tool-adapter x model-version x prompt-schema combinations, most of which have never actually been tested together, so nobody can confidently say whether a given production combination is known-good, known-bad, or simply untested.

**Frequency**: Occasional

**Symptoms**
- The team cannot answer "is orchestrator v14 with tool-adapter v6 and model version 2024-09 a supported combination?" without manual investigation
- Compatibility documentation (if it exists at all) is stale, contradicts itself, or hasn't been updated in multiple release cycles
- Regression test suites cover only a small fraction of the theoretically possible version combinations actually running in production across different customers/environments
- Bugs are reported against combinations the team didn't know were in use, because no inventory tracks which combinations are actually deployed where
- Adding support for one new version of one component requires disproportionate effort because it must be manually cross-checked against every other component's supported versions

## Root Cause
Each component's team typically manages its own version support policy in isolation — "we support N-2 versions of our component" — without a shared model of how those policies compose across the whole system. When component A supports 3 versions, component B supports 4, and component C supports 3, the naive combinatorial space is 36 combinations, but almost none of that space is actually being tested end-to-end; testing effort per team stays roughly constant (each team tests their own component against what they assume is "the current" version of everything else) while the actual space of deployed combinations grows with every independent release. Because no single team owns the cross-product, the compatibility matrix is discovered reactively, one bug report at a time, rather than being deliberately curated, and the matrix's true size is usually far larger than anyone realizes until someone tries to enumerate it.

## Example
```
"AgentPlatform" has four independently versioned components with
their own release cadence and support windows:
- Orchestrator: supports its last 3 minor versions (v12, v13, v14)
- Tool-adapter SDK: supports its last 4 versions (v4-v7)
- Prompt-template schema: 2 active schema versions (v2, v3)
- Underlying model endpoint: 3 pinned model snapshots in active use

Naive combination count: 3 x 4 x 2 x 3 = 72 combinations.

The core team's CI only runs the full integration suite against
what they call "the current default stack" - orchestrator v14,
tool-adapter v7, schema v3, latest model snapshot - a single point
in that 72-combination space.

A customer running orchestrator v12 (still within support window)
paired with tool-adapter v7 (also within window, upgraded
independently for an unrelated tool-adapter bug fix) hits a crash:
v12's tool-call serialization format is incompatible with a
breaking change introduced in tool-adapter v6, three versions
before v7's release notes had assumed anyone still on v12 would
have also upgraded orchestrator in lockstep - an assumption never
actually validated because that specific pairing had never been
tested.

Support spends two days reproducing the issue because it's the
first time anyone has run that particular combination outside of
this one customer's environment.
```

## Statistics
| Finding | Context |
|---------|---------|
| Combinatorial compatibility space grows multiplicatively with each independently-versioned component, while integration testing effort typically stays roughly linear per team | Typical structural mismatch reported across multi-component platform teams |
| A small minority of the theoretical compatibility matrix is commonly covered by active integration tests in platforms with 4+ independently versioned components | Estimated from teams that audited their test coverage against their full version matrix |
| Reducing the supported-version window per component and enforcing lockstep upgrades for tightly-coupled pairs substantially shrinks the untested matrix in teams that adopted the practice | Reported range across teams that consolidated version support policies |

## Mitigations
1. **Explicit, centrally-owned compatibility matrix**: Maintain a single, actively curated document or machine-readable manifest listing which combinations are tested-and-supported, known-incompatible, or untested, owned by one team rather than inferred from each component's individual support policy.
2. **Shrink the supported-version window**: Reduce how many versions back each component supports, and coordinate deprecation timelines across components so the combinatorial space stays small enough to actually test.
3. **Lockstep versioning for tightly-coupled components**: For component pairs with a history of breaking incompatibilities (like the orchestrator and tool-adapter SDK), require them to be upgraded together as a bundled release rather than allowing independent version drift.
4. **Automated compatibility test matrix in CI**: Run integration tests against the full supported matrix (or a representative, risk-weighted sample of it) automatically on every release, rather than testing only the single "current default stack."
5. **Production combination inventory**: Track which version combinations are actually deployed across environments/customers, so the team can prioritize testing effort toward combinations with real usage rather than guessing, and can proactively flag customers running untested pairings.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| tested_combination_coverage_ratio | Share of actually-deployed version combinations covered by an automated integration test | Alert if < 80% of production combinations |
| untested_combination_deploy_count | Number of production environments running a version combination with no corresponding test coverage | Alert if > 0 for customer-facing deployments |
| compatibility_matrix_staleness | Time since the compatibility matrix/manifest was last updated relative to the most recent component release | Alert if > 1 release cycle out of date |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Untested combination in production | A deployment is detected running a version pairing with no test coverage or documented compatibility status | Medium | Flag for prioritized testing, document current known status, notify the affected environment's owner |
| Compatibility matrix out of date | compatibility_matrix_staleness exceeds threshold after a new component version ships | Low | Assign matrix update as part of the release checklist for the newly shipped component |

## Related Patterns
- [Version Skipping Unsupported](./version-skipping-unsupported.md) - an upgrade path issue that becomes far more likely to go unnoticed when the compatibility matrix is already too large to reason about
- [Version Deprecation Timeline Miss](./version-deprecation-timeline-miss.md) - failing to actually retire old supported versions is a direct driver of matrix growth over time
- [Deployment Dependency Deadlock](./deployment-dependency-deadlock.md) - both stem from independently-versioned components lacking a shared, explicit compatibility contract
