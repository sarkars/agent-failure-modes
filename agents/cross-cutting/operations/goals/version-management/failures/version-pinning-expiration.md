# Version Pinning Expiration

## Issue
A team deliberately pins a dependency, container base image, or OS package to an exact version — for good reasons at the time (avoiding a breaking change, ensuring reproducible builds, working around a bug in a newer release) — and that pin is never revisited afterward. Unlike a range-based dependency that at least stays current within its bounds, an exact pin freezes the version indefinitely by design, so as months or years pass without an explicit review, the pinned version accumulates unpatched CVEs, falls off the vendor's support/EOL calendar, or becomes incompatible with newer tooling in the surrounding ecosystem, entirely because nothing was ever set up to force a periodic look at whether the original reason for pinning still applies.

**Frequency**: Very Common

**Symptoms**
- A pinned package or base image version has a documented EOL/end-of-support date that has already passed, discovered only during an unrelated audit
- Security scanning flags multiple CVEs against an exact-pinned version, several of which are fixed in later releases that the pin explicitly prevents from ever being installed
- The original comment or commit message explaining why a version was pinned (e.g., "pinning to 1.4.2 due to a regression in 1.5") references an issue that was fixed upstream long ago, but the pin was never removed
- A container image still references an OS base image tag (e.g., a specific Linux distribution point release) that the vendor has stopped publishing security updates for
- Attempting to unpin and upgrade during an unrelated, unplanned change surfaces a large number of accumulated breaking changes at once, because incremental upgrades were never applied while the pin was in place

## Root Cause
An exact version pin is a deliberate override of the normal "stay reasonably current" behavior a range-based dependency would otherwise provide, and by design it has no mechanism to un-pin itself — it will remain exactly where it was set indefinitely unless a human or an automated process explicitly revisits it. The pin is typically added to solve an immediate, specific problem, and once that problem stops being visible (the regression is no longer being hit, the team member who added the pin has moved on), there's no artifact reminding anyone that the pin was meant to be temporary or that its original justification should be periodically re-evaluated against the current state of the upstream package. Security and support-lifecycle risk accumulates silently because none of it produces an error at build or runtime — the pinned version keeps working exactly as it did the day it was pinned, so nothing forces attention back to it until an external signal (a CVE scanner, an EOL notice, an unrelated forced upgrade) surfaces the accumulated debt all at once.

## Example
```
A team pins their base Docker image to a specific Linux distribution
point release (e.g., a fixed minor version tag) after a newer point
release broke a system library their agent runtime depended on. The
Dockerfile comment reads: "pinned due to libssl ABI break in the next
point release - revisit later." No ticket, no expiration date, no
calendar reminder is attached to "revisit later."

Two years pass. The distribution vendor's security-update lifecycle
for that point release ends after one year, meaning the pinned image
has been running with no security patches for the second year
entirely. A routine container security scan finally flags a long list
of CVEs against packages baked into the pinned base image, several
rated critical, none of which have been receiving patches because the
vendor stopped supporting that exact point release.

Un-pinning turns out to require substantially more work than a normal
upgrade would have, because two years of accumulated changes in the
base image (library version bumps, changed default configurations,
a different init system in later releases) all have to be dealt with
simultaneously, rather than incrementally as they would have been if
the pin had been periodically revisited and lifted once the original
libssl issue was fixed upstream.
```

## Statistics
| Finding | Context |
|---|---|
| A large share of container base images and package pins in production systems are more than a year past their vendor's last security update for that exact version | Estimated from typical container/dependency security audits |
| Pins added with an explicit "temporary, revisit later" justification are disproportionately represented among long-expired pins, since no artifact tracks the intended revisit date | Typical finding when auditing pin-related code comments against actual pin age |
| Teams using automated dependency-update bots (Dependabot/Renovate) configured to also propose exact-pin updates (not just range-based updates) show meaningfully lower average pin age than teams relying on manual review | Typical range reported comparing automated vs. manual pin-maintenance practices |

## Mitigations
1. **Attach an explicit expiration/review date to every pin**: When adding an exact version pin, require a ticket or tracked annotation with a concrete re-review date (not just a comment saying "revisit later"), so the pin surfaces for reconsideration automatically rather than depending on someone remembering.
2. **Automated dependency-update bots configured to propose pin updates, not just range bumps**: Configure tools like Dependabot/Renovate to open PRs against exact pins too, so a human decision is prompted periodically even when the manifest technically doesn't need to change.
3. **CVE scanning against pinned versions on a recurring schedule**: Run vulnerability scans against exact-pinned dependencies and base images on an ongoing basis (not just at initial adoption), since the pin freezes the version but not the vulnerability landscape around it.
4. **EOL calendar tracking for pinned majors/distributions**: Maintain a tracked list of vendor-published support end dates for every pinned major version or OS distribution release, reviewed on a recurring cadence, so EOL is caught ahead of time rather than during an unrelated audit.
5. **Prefer narrow, justified pins over broad or indefinite ones**: When pinning is necessary, pin as narrowly as the actual constraint requires (a single package rather than an entire base image where possible) and document the specific upstream issue being avoided, so the pin's continued necessity can be checked against upstream's changelog rather than requiring a full re-investigation.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| pin_age_days | Days since a given exact version pin was last reviewed or updated | Alert if > 180 days without review |
| pinned_version_cve_count | Count of known CVEs affecting currently pinned exact versions | Alert on any newly disclosed CVE affecting a pinned version |
| pins_past_vendor_eol | Count of pinned versions/images past their vendor's documented end-of-support date | Alert on any nonzero count |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Pin past review date | A tracked pin's review date has passed with no re-evaluation | Medium | Assign owner to re-justify or lift the pin |
| CVE found in long-pinned version | Security scan finds a CVE in a pin older than the review threshold | High | Prioritize upgrade or apply a targeted patch/backport if upgrade isn't immediately feasible |

## Related Patterns
- [Model Version Pinning Expiration](../../../../../by-capability/reasoning-and-thought/goals/model-updates-and-versioning/failures/model-version-pinning-expiration.md) - the ML-model/LLM-provider counterpart of this same mechanism, where a pinned model or API version goes stale relative to newer, better-supported releases, requiring different (model-evaluation-driven rather than CVE-driven) mitigations
- [Version Lock File Staleness](./version-lock-file-staleness.md) - a closely related pattern where the staleness comes from an auto-generated lock file never being regenerated, rather than from a deliberate exact pin never being revisited
- [Version Deprecation Timeline Miss](../../tool-capability-limits/failures/deprecated-endpoint-retirement.md) - a related failure where a vendor-driven sunset date is missed entirely, as opposed to this pattern's slower, review-driven accumulation of risk on a pin nobody revisits
