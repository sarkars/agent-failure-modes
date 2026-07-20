# Version Prerelease In Production

## Issue
A dependency, model endpoint, or platform component is pinned to a prerelease, beta, release-candidate, or nightly-build version — sometimes intentionally to get early access to a needed fix or feature, sometimes accidentally because a version-range specifier didn't exclude prerelease tags — and that prerelease version ends up running in production rather than being confined to a controlled evaluation. Prerelease versions carry no stability or support guarantee: the vendor can change, break, or withdraw them without following the deprecation notice process used for stable releases, and production traffic ends up exposed to instability that a stable-channel pin would never have carried.

**Frequency**: Occasional

**Symptoms**
- A manifest or lockfile pins a version string containing a prerelease tag (`-rc.1`, `-beta`, `-alpha`, `-nightly`, `-dev`) in a production deployment
- The pinned prerelease version silently disappears or changes behavior without any deprecation notice, because vendors typically don't apply the same support commitments to prerelease channels
- A version-range specifier intended to track stable releases (`^2.0.0`) unexpectedly resolves to a prerelease build because the package ecosystem's prerelease-exclusion rules weren't applied correctly
- Production incidents trace back to a bug specific to the prerelease build that was already fixed (or reintroduced) in the subsequent stable release, meaning production was running code less stable than what was actually available
- The prerelease pin was added for a specific short-term reason (an urgently needed fix) that has since shipped in a stable release, but the pin was never updated to track it

## Root Cause
Prerelease versions exist specifically to let consumers preview upcoming changes before the vendor commits to their stability, which means the vendor's own support and compatibility guarantees explicitly don't apply to them — a prerelease can be replaced, altered, or withdrawn between one build and the next without the advance-notice process that governs stable-channel deprecations. When a prerelease is pinned into production, either deliberately (to unblock on an urgently needed fix not yet in a stable release) or accidentally (a version-range specifier that wasn't scoped to exclude prerelease tags, which many package ecosystems do not exclude by default), the system inherits that lack of guarantee without anyone treating it as unusual, because the pin looks like any other version pin in the manifest. The risk compounds because prerelease pins are rarely tracked separately from stable pins in dependency-review processes, so there's typically no distinct alert or review gate that catches "this pin points at a prerelease" the way there might be for an EOL stable version.

## Example
```
A team hits a critical bug in a message-queue client library that's
fixed in an as-yet-unreleased version. Under deadline pressure, they
pin directly to the fix commit's nightly build tag rather than
waiting for the next stable release, intending to switch back to a
stable pin "once it ships."

The nightly build is never intended for production use and the
maintainers make an unrelated breaking change to the client's retry
behavior in a subsequent nightly two weeks later - because nightlies
aren't subject to the same compatibility guarantees as stable
releases, and nothing in the team's pin protects them from picking up
a newer nightly by accident during a routine dependency-bump sweep
that didn't distinguish "nightly" from "stable" version strings.

The team's next scheduled dependency update inadvertently moves the
pin to a newer nightly build (rather than the intended target-stable
release, which had in fact already shipped by then), silently
changing retry behavior in production message processing and causing
a spike in duplicate message handling that takes a week to trace back
to the dependency bump, since nothing flagged that the "update" moved
between two prereleases rather than landing on the stable release
that had superseded both.
```

## Statistics
| Finding | Context |
|---|---|
| A nontrivial share of production dependency manifests contain at least one pin resolving to a prerelease/beta/nightly tag, often unintentionally | Estimated from typical dependency-audit findings across production codebases |
| Prerelease pins added to unblock an urgent fix are frequently never migrated back to the corresponding stable release once one ships | Typical finding when auditing the age and justification of prerelease pins |
| Incidents attributable to unannounced prerelease behavior changes are disproportionately concentrated in ecosystems whose default version-range resolution does not exclude prerelease tags | Typical pattern observed comparing ecosystems with prerelease-exclusive-by-default resolution against those without |

## Mitigations
1. **Explicitly flag and separately track prerelease pins**: Treat any pin resolving to a prerelease/beta/nightly tag as a distinct, tracked risk category in dependency review, with an explicit expectation that it's temporary and a target date to migrate to the corresponding stable release.
2. **Exclude prerelease tags from automatic range resolution by default**: Configure package managers and update bots to never resolve a version range to a prerelease tag automatically, requiring an explicit, deliberate override to pin one intentionally.
3. **Automated migration reminder tied to stable-release availability**: When a prerelease pin's corresponding stable release ships, automatically flag the pin for update rather than relying on someone remembering the original "switch back once it ships" intent.
4. **Isolate prerelease usage to non-production environments where feasible**: Default to only running prerelease versions in staging/canary environments, requiring an explicit, documented exception process before a prerelease pin is allowed to reach production.
5. **Treat prerelease pins as carrying no support guarantee in incident response**: When triaging an incident involving a prerelease dependency, assume the vendor may not provide a fix or advance notice for the specific prerelease build in use, and prioritize migrating to a stable release over waiting for a prerelease-specific fix.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| production_prerelease_pin_count | Count of dependency pins in production manifests resolving to a prerelease/beta/nightly tag | Alert on any nonzero count without an active, tracked justification |
| prerelease_pin_age_days | Days since a prerelease pin was added, relative to whether a corresponding stable release has since shipped | Alert if a corresponding stable release has shipped and the pin hasn't been migrated within 14 days |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Untracked prerelease pin detected in production | A dependency scan finds a prerelease-tagged version pinned in a production manifest with no tracked justification | High | File a tracked migration task, assess current production exposure |
| Corresponding stable release available | The stable release superseding a tracked prerelease pin has shipped | Medium | Schedule migration to the stable pin in the next release cycle |

## Related Patterns
- [Version Pinning Expiration](./version-pinning-expiration.md) - a related pattern about any pin (stable or prerelease) going stale without review; this pattern is the specific case where the pin was never on a supported channel to begin with
- [Beta Feature Instability](../../tool-capability-limits/failures/beta-feature-instability.md) - a related pattern about using a vendor's beta-labeled feature/API, sharing the same "no stability guarantee" root cause applied to a feature flag rather than a pinned dependency version
- [Version Compatibility Matrix Explosion](./version-compatibility-matrix-explosion.md) - prerelease pins compound this pattern by adding untested, unstable version combinations to an already-unmanageable compatibility matrix
