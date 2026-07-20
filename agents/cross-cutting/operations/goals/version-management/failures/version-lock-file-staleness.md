# Version Lock File Staleness

## Issue
A project's lock file (`package-lock.json`, `poetry.lock`, `Cargo.lock`, `Gemfile.lock`) pins the exact resolved version of every dependency at the moment it was last regenerated, and that lock file is checked into source control and treated as the source of truth for what actually gets installed in CI and production. Over time, the manifest's version ranges (`^2.1.0`, `>=1.4`) would permit newer releases, but because nobody regenerates the lock file, every install — regardless of how much time has passed — keeps resolving to the same increasingly old exact versions, silently accumulating unpatched vulnerabilities and missed bug fixes while the manifest itself looks perfectly current.

**Frequency**: Very Common

**Symptoms**
- A vulnerability scanner flags a CVE in a specific dependency version, but the manifest's declared range would already permit a patched version — the lock file is simply pinning an old resolution that predates the fix
- `npm install`/`pip install` locally (without the lock file) resolves to different, newer versions than what CI installs via `npm ci`/`pip install -r requirements.txt` with a frozen lock file, causing "works on my machine" discrepancies
- Lock file's last-modified date or git history shows no update in many months despite the manifest's dependencies having had multiple releases in that window
- Renovate/Dependabot-style automated update PRs pile up unmerged, meaning the tooling to keep the lock file current exists but its output isn't being acted on
- A routine dependency bump (adding one new package) regenerates the entire lock file and pulls in dozens of unrelated version changes at once, because so much drift had accumulated since the last regeneration

## Root Cause
Lock files exist specifically to make installs reproducible by freezing the exact resolved version graph, which is valuable for stability but has the side effect of decoupling "what the manifest allows" from "what actually gets installed" — the moment the lock file is generated, it stops tracking new releases within its own permitted ranges unless something explicitly triggers regeneration. Without an automated process that periodically re-resolves the lock file (or opens a PR proposing to), regeneration only happens as a side effect of unrelated work (adding a new dependency), which for a stable codebase with few new dependencies can be rare. Because a stale lock file produces no error — installs succeed, tests pass, the exact-pinned versions work exactly as they did when pinned — there's no natural forcing function that surfaces the growing gap between "pinned version" and "currently available, patched version" until a vulnerability scan, an EOL notice, or a forced upgrade elsewhere in the dependency tree makes the staleness visible.

## Example
```
A team's Node service has package.json specifying "express": "^4.17.0"
and a package-lock.json that resolved and pinned express@4.17.1 when
the project was first scaffolded. Over the following 18 months, the
manifest range ^4.17.0 would permit any 4.x release including several
that patch known vulnerabilities, but the lock file is only
regenerated when a new top-level dependency is added - which hasn't
happened.

Every CI build and every production deploy runs `npm ci`, which
installs exactly what the lock file specifies: express@4.17.1,
unchanged for 18 months, along with dozens of transitive dependencies
frozen at the same original resolution.

A routine vulnerability scan flags a known CVE in a transitive
dependency pulled in by that pinned express@4.17.1 resolution - a CVE
that was patched in a later 4.x release the manifest's own range
already permits. The fix requires no manifest change at all, only
regenerating the lock file - but because nothing had triggered that
regeneration in 18 months, the vulnerable version had been
continuously deployed to production the entire time without anyone
intending to pin it that long.
```

## Statistics
| Finding | Context |
|---|---|
| A significant share of dependency-related CVE exposure in production systems stems from lock files pinning versions older than what the project's own manifest ranges would already permit | Estimated from vulnerability-scan findings correlated against manifest version ranges |
| Projects with automated lock-file update tooling (Dependabot/Renovate) configured but with a high rate of unmerged update PRs show similar staleness levels to projects with no automation at all | Typical finding when update PRs are opened but not triaged or merged |
| Time since last lock-file regeneration correlates strongly with the count of known-patched vulnerabilities present in the frozen dependency graph | Typical pattern observed across projects audited for supply-chain hygiene |

## Mitigations
1. **Scheduled automated lock-file regeneration**: Run a recurring (e.g., weekly) automated job that regenerates the lock file within the manifest's existing version ranges and opens a PR, rather than relying on regeneration as an incidental side effect of adding new dependencies.
2. **Treat update-bot PRs as a queue with an SLA, not a backlog to ignore**: Configure and actually triage Dependabot/Renovate output on a defined cadence; an update tool that's configured but unmerged produces the same staleness as having no tool at all.
3. **CVE scanning against the resolved lock file, not just the manifest**: Run vulnerability scans against the exact pinned versions in the lock file (what's actually deployed), since scanning only the manifest's permitted ranges can miss that the lock file is pinning an older, vulnerable resolution within those ranges.
4. **Separate "add a dependency" regeneration from "refresh existing pins" regeneration**: Don't rely on the lock file only changing when a new package is added; explicitly schedule a distinct maintenance task for refreshing already-present pins to their latest permitted versions.
5. **Alert on lock-file age, not just on discovered CVEs**: Track and alert on how long it's been since the lock file was last regenerated as a leading indicator, rather than only reacting after a scanner finds a specific vulnerability in an old pin.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| lock_file_age_days | Days since the lock file was last regenerated (not just committed for an unrelated change) | Alert if > 30 days for actively maintained projects |
| unmerged_dependency_update_prs | Count of open automated dependency-update PRs older than a defined SLA | Alert if > 10 open PRs older than 14 days |
| pinned_version_cve_count | Count of known CVEs affecting exact versions currently pinned in the lock file | Alert on any newly introduced CVE affecting a currently pinned version |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Lock file stale beyond threshold | lock_file_age_days exceeds the configured threshold | Medium | Trigger scheduled regeneration job, review resulting diff for breaking changes before merge |
| CVE present in pinned version already patched within manifest range | Vulnerability scan finds a CVE in a pinned version where a patched version is already permitted by the manifest's own range | High | Regenerate lock file immediately, fast-track the resulting PR |

## Related Patterns
- [Version Pinning Expiration](./version-pinning-expiration.md) - closely related: pinning expiration covers the broader pattern of any pinned version (including explicit exact pins, not just lock-file-resolved ones) going stale without review; lock-file staleness is the specific case where the pinning mechanism is an auto-generated lock file rather than an explicit manifest pin
- [Dependency Version Conflicts](../../dependency-management/failures/dependency-version-conflicts.md) - a related but distinct dependency-management failure about incompatible version constraints between packages, rather than a single resolution silently aging past its patched alternatives
- [Version Downgrade Failure](./version-downgrade-failure.md) - a stale lock file can obscure which version was actually last known-good, complicating an attempted downgrade during an incident
