# Dependency Version Pinning Conflict

## Issue
A team pins a dependency to an exact version — often deliberately, to avoid an earlier breaking-change incident or to satisfy a compliance requirement for reproducible builds — and later, a different part of the system introduces a new requirement (a new package, a new feature, a security patch) that needs a minimum version higher than the pin. The pin, which was added specifically to provide stability, now actively blocks a change the system needs, and resolving the conflict requires either revisiting the original reason for the pin or accepting the very risk the pin was meant to prevent.

**Frequency**: Occasional

**Symptoms**
- A new package installation or security patch fails because it requires a minimum version above an existing exact pin elsewhere in the manifest
- Engineers are unsure why a pin exists (the original incident that motivated it predates their tenure) and are reluctant to remove it without understanding the risk
- A security-critical update is delayed specifically because unpinning would also pull in unrelated breaking changes bundled in the same version jump
- The pin was added to work around a specific bug that has since been fixed in later versions, but nobody has revisited whether it's still needed
- Two teams within the same organization maintain conflicting pins on the same shared internal library, each pinned to satisfy their own historical incident

## Root Cause
A version pin freezes a point-in-time decision without an expiration or a mechanism to revisit it, so it persists long after its original justification may have become obsolete, while the rest of the dependency ecosystem continues to move forward and eventually requires something the frozen pin can't satisfy. Pins are usually added reactively, during an incident, by someone focused on the immediate goal of stopping the bleeding — pin the version, ship the fix, move on — without a corresponding process to periodically ask "is this pin still necessary" or to document the pin's rationale in a way that a future engineer, weighing whether to unpin it, can actually evaluate the tradeoff instead of just inheriting an unexplained constraint.

## Example
```
Eighteen months ago, a team pinned "date-utils" to exactly version 3.4.2 in
their agent's scheduling service, after 3.5.0 introduced a timezone-handling
regression that caused the agent to schedule reminders an hour off during
daylight-saving transitions. The pin was added under incident pressure with
a one-line commit message: "pin date-utils, 3.5.0 broke DST handling."

Today, the security team flags a critical CVE in a different package,
"ical-generator," which the scheduling service also depends on. The fix
requires ical-generator 2.0.0, which in turn requires date-utils >=4.0.0 for
a new date-formatting API it relies on.

Nobody currently on the team knows whether the original DST bug in
date-utils 3.5.0+ was ever fixed in a later 3.x or 4.x release, because the
pin's commit message doesn't reference an upstream issue and no one
re-tested newer versions since. The security patch is stuck: applying it
requires unpinning date-utils, which risks reintroducing the DST bug (now
undiagnosed for 18 months against a completely different date-utils major
version), so the critical CVE fix is deferred for three weeks while an
engineer manually re-verifies DST behavior across the intervening date-utils
releases from scratch.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 30-40% of long-lived exact-version pins in production codebases have no documented rationale traceable to a specific issue or upstream bug report | Typical range observed in dependency-pin audits |
| Security patches blocked or delayed by an unrelated version pin account for an estimated 10-15% of overdue critical CVE remediations | Estimated from vulnerability remediation delay analysis |
| Pins with an attached expiration or periodic-review policy are revisited and resolved (removed, tightened, or reconfirmed) at a substantially higher rate than pins with no review mechanism | Reported directional finding across teams adopting pin review policies |

## Mitigations
1. **Documented, linked pin rationale**: Require every exact-version pin to be accompanied by a comment or tracked issue explaining specifically what upstream problem it avoids, so a future engineer can evaluate whether that problem still applies to newer versions.
2. **Pin expiration and periodic review**: Attach a review date or a "revisit when upstream issue X is resolved" trigger to every pin, and periodically audit pins older than a defined threshold to check whether they're still necessary.
3. **Narrow, targeted pins over broad exact pins**: Where possible, express the constraint as "exclude the specific broken version range" rather than an exact pin to one old version, so future minimum-version requirements from other dependencies aren't unnecessarily blocked.
4. **Conflict-aware dependency update tooling**: Use tooling that, when a new minimum-version requirement conflicts with an existing pin, surfaces both the pin's original rationale and the new requirement side by side, rather than just failing with a generic resolution error.
5. **Regression test coverage for the original pin's issue**: When a pin is added to work around a specific bug, add a regression test that exercises that exact bug, so future attempts to unpin can verify quickly whether the underlying issue has actually been fixed upstream instead of re-diagnosing from scratch.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| undocumented_pin_count | Count of exact-version pins in the manifest with no linked rationale or issue reference | Alert if > 0 for pins older than a defined age threshold |
| pin_blocked_update_count | Count of dependency updates (including security patches) currently blocked by an existing pin's constraint | Alert if > 0, especially for security-classified updates |
| pin_age | Time since a pin was last reviewed or reconfirmed as still necessary | Alert if > defined review interval (e.g., 6 months) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Security patch blocked by version pin | A critical/high CVE fix cannot be applied due to an existing pin's version constraint | High | Prioritize re-evaluating the pin, add regression test for original issue, unpin or patch around it |
| Stale undocumented pin detected | A pin exceeds the review interval with no linked rationale | Medium | Assign an engineer to investigate and either document, narrow, or remove the pin |

## Related Patterns
- [Dependency Version Conflicts](./dependency-version-conflicts.md) - a pinning conflict is a special case where one side of the incompatible-version collision is a deliberate historical pin rather than an unconstrained transitive requirement
- [Dependency Breaking Change](./dependency-breaking-change.md) - pins are frequently created specifically in reaction to a breaking change, making the two patterns causally linked
- [Dependency Security Vulnerability](./dependency-security-vulnerability.md) - a stale pin is one of the most common concrete reasons a known-fixed vulnerability remains unpatched
