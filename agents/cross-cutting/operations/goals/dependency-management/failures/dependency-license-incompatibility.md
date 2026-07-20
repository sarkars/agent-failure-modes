# Dependency License Incompatibility

## Issue
An agent's development workflow — often an agent itself, tasked with "add a library that does X" — pulls in a new dependency without checking its license against the project's own licensing terms or the terms of the dependencies already in the tree. A permissively-licensed project unknowingly incorporates a copyleft-licensed package (or one with a restrictive commercial-use clause), creating a legal obligation (source disclosure, attribution, non-commercial restriction) the project's license terms don't account for, and the conflict surfaces only during a legal review, an acquisition due-diligence process, or a customer's compliance audit.

**Frequency**: Occasional

**Symptoms**
- A license audit or SBOM (software bill of materials) scan flags a dependency with a license incompatible with the project's declared license
- A transitive dependency (pulled in by a direct dependency, not chosen explicitly) carries a restrictive license nobody on the team was aware of
- Legal or compliance review during a fundraising, acquisition, or enterprise customer contract process surfaces the conflict, well after the dependency has been in production for months or years
- An agent tasked with autonomously selecting and installing packages has no license-awareness in its tool-selection logic, and treats "does it solve the problem" as the only selection criterion
- Removing or replacing the offending dependency late in the project's life requires a nontrivial rewrite because other code has come to depend on it

## Root Cause
License compatibility is a legal analysis, not a technical one, so it sits outside the normal build/test/deploy feedback loop that would otherwise catch a problem quickly — a license conflict doesn't break the build or fail a test, it creates a legal exposure that is invisible to every automated check except a dedicated license scanner. When dependency selection is delegated to an agent optimizing for functional fit (does this package do what's needed, is it well-maintained, does it have good documentation), license terms are rarely part of the agent's evaluation criteria unless explicitly engineered in, and transitive dependencies compound the problem because a license conflict several levels deep in the dependency tree is invisible to anyone reviewing only the direct, explicitly chosen packages.

## Example
```
An engineering team asks a coding agent to "add PDF generation to the
invoicing service." The agent searches available packages, evaluates several
by feature set and popularity, and installs a well-regarded PDF library that
best matches the feature requirements: precise layout control, table
support, embedded fonts.

The library is licensed under AGPL-3.0, which requires that any service
making the software's functionality available over a network must offer its
complete corresponding source code to users of that service. The invoicing
service is closed-source SaaS. The agent's package selection considered
download counts, test coverage, and API ergonomics, but had no license
filter, so it did not flag the AGPL terms as a problem.

The conflict is not discovered for eight months, until an enterprise
customer's procurement team runs a third-party license audit as part of a
vendor security review and flags the AGPL dependency as incompatible with
the customer's own compliance requirements for closed-source vendors. The
team must now urgently identify and replace the library, a multi-week
effort since PDF generation is by then threaded through several features,
while the enterprise deal is on hold pending resolution.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 5-15% of codebases with automated or semi-automated dependency selection contain at least one direct or transitive dependency with a license incompatible with the project's stated license | Typical range observed in open-source license audits |
| License conflicts introduced via transitive dependencies (not directly chosen) account for an estimated 40-60% of flagged incompatibilities | Estimated from SBOM scan results across audited codebases |
| Projects with automated license scanning integrated into CI catch an estimated 90%+ of incompatible licenses before merge, versus manual or ad hoc review | Reported range across teams using CI-integrated license scanners |

## Mitigations
1. **Automated license scanning in CI**: Run a license-compliance scanner against every direct and transitive dependency on every build, failing the build (or requiring explicit sign-off) when an incompatible license is detected.
2. **License allow-list for automated/agentic dependency selection**: Constrain any agent or automated tool with package-installation capability to a pre-approved allow-list of license types, rather than leaving license terms out of its selection criteria entirely.
3. **SBOM generation and periodic audit**: Maintain a software bill of materials for the full dependency tree, including transitive dependencies, and review it on a recurring cadence, not just at major release or fundraising milestones.
4. **License review as a required PR gate for new dependencies**: Require any PR introducing a new direct dependency to pass an automated license check before merge, treating it with the same rigor as a security review.
5. **Early legal involvement in dependency policy**: Have legal/compliance define an explicit, documented license policy (which license types are acceptable, under what conditions) that engineering and any agentic tooling can be configured against, rather than relying on ad hoc case-by-case judgment.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| incompatible_license_dependency_count | Count of dependencies (direct + transitive) with a license flagged incompatible with project policy | Alert if > 0 |
| unscanned_new_dependency_rate | Fraction of newly introduced dependencies that merged without passing a license scan | Alert if > 0% |
| agent_installed_package_license_coverage | Fraction of packages installed by an autonomous agent that were checked against the license allow-list before installation | Alert if < 100% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Incompatible license detected pre-merge | CI license scan flags a new dependency's license as incompatible | High | Block merge, require legal review or dependency substitution |
| Incompatible license found in production dependency tree | Periodic SBOM audit finds an existing production dependency with an incompatible license | High | Prioritize replacement, involve legal to assess exposure, notify affected stakeholders if customer-facing |

## Related Patterns
- [Dependency Security Vulnerability](./dependency-security-vulnerability.md) - both are non-functional dependency risks (legal and security) that standard build/test checks don't catch without dedicated tooling
- [Transitive Dependency Explosion](./transitive-dependency-explosion.md) - an uncontrolled transitive dependency tree makes license auditing dramatically harder, since license conflicts hide several levels deep
- [Dependency Breaking Change](./dependency-breaking-change.md) - both describe risks introduced by a dependency that go unnoticed because they fall outside the standard functional test suite
