# Dependency Hell & Version Compatibility Blindness

## Issue: Deployment Agent Doesn't Detect Breaking Changes in Dependencies; Deploys Incompatible Versions

**Frequency**: Common

**Symptoms**
- Dependency update: Version X.Y.Z → X.(Y+1).Z (minor version bump assumed safe)
- Actually: Breaking change in minor version (semver not followed)
- Deployment proceeds; code breaks in production
- "This worked in staging!" but dependencies different between env

**Root Cause**
Semantic versioning rules assume: patch = bugfix, minor = backward-compatible, major = breaking. But many packages violate this. Deployment agents don't validate semantic versioning compliance. No automated compatibility testing before deployment.

**Example**
```
Scenario: Python library update
Requirements: 'requests >= 2.25.0'
Installed in staging: requests 2.28.0 (no breaking changes)
Latest available: requests 2.29.0 (introduced breaking change in URL encoding)
Deployment: Upgrades to 2.29.0 in prod (different from staging!)
Result: URL encoding breaks; 500 errors
Impact: Production incident; rollback needed
```

**Key Statistics**
- Semver violations: 10-30% of packages violate semver
- Env mismatch (staging ≠ prod dependencies): 20-40% of orgs
- Detection rate of breaking changes: 10-40% (human manual)

---

## Mitigation Strategies

1. **Lock Dependencies**: Use lock files (package-lock.json, Pipfile.lock)
2. **Test in Prod-Like Env**: Staging should have exact same dependencies as prod
3. **Dependency Checking**: Scan for known breaking changes before deploying
4. **Gradual Rollout**: Canary deployment; monitor errors before full rollout

### Metrics
- Version mismatch between environments
- Breaking change detection rate
- Incident rate from dependency issues

### Alerts
- Dependencies differ between staging and prod → Warn
- Known breaking change in dependency → P1

---

## References

- [Dependency Resolution in Package Managers](https://arxiv.org/abs/1811.09935)
- [Software Supply Chain Security](https://arxiv.org/abs/2008.08459)
