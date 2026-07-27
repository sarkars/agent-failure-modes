# What Are the Most Common Tool Special Constraint Failures in AI Agents?

**Tool special constraints fail when tools have non-obvious requirements (authentication scope, allowlisted IPs, data residency restrictions) that agents don't satisfy, when regulatory constraints are violated, or when tool preconditions are not met before invocation.** The 6 special-constraint patterns documented here cover niche but critical tool requirements — from authentication and authorization scope through data residency and regulatory compliance, to tools requiring specific network conditions or preconditions. Special-constraint failures are particularly dangerous because they're often context-specific (work in dev, fail in prod) and cause silent failures (no error, just wrong behavior or data loss).

## Key Takeaways

- 6 patterns span authentication scope, data residency, regulatory constraints, network requirements, and preconditions.
- Authentication Scope Violation and Data Residency Requirement Not Met are most severe: calling a tool with wrong authentication causes failures or data access violations, data residency violations cause compliance incidents.
- Regulatory Constraint Violation is second-order: tool must be called only for certain data types or regions; constraint is violated.
- Tool Precondition Not Met is architectural: tool requires specific system state (DB connection open, cache warm) that agent doesn't verify.

## Scope

- **Authentication and Access** — Authentication scope (OAuth scopes, API keys, roles), authorization checks.
- **Data and Compliance** — Data residency (EU data stays in EU), PII handling, regulatory constraints.
- **Network and Infrastructure** — Allowlisted IPs, VPN requirement, special network topology.
- **State and Prerequisites** — Tool requires system state (connection open, cache available, DB transaction active).

## When Special Constraints Matter

- Tools have complex access control or authentication requirements.
- Tools are constrained by regulatory or compliance requirements.
- Tools are deployed across multiple regions or environments with different constraints.

## Cross-Pattern Insight

Special-constraint failures result from incomplete documentation and insufficient testing across environments. Constraints that don't apply in dev (e.g., data residency, IP allowlisting) become critical in prod. The mitigation is explicit constraint discovery and per-environment validation: document all tool constraints, test tools in all deployment environments (not just dev), and validate constraints at agent deployment time.

## Frequently Asked Questions

### How do you discover tool special constraints?
Query tool documentation for authentication, authorization, data residency, compliance, and network requirements. If undocumented, test tool in different environments and configurations to discover constraints.

### What should an agent do if a special constraint cannot be met?
Fail loudly with clear error messaging that identifies which constraint is violated. Don't attempt to call the tool in an invalid context.

## Patterns

| Pattern | Mechanism |
|---|---|
| Authentication scope violation | Agent calls tool with wrong OAuth scope or API key | 
| Authorization scope violation | Agent calls tool on data it shouldn't access given auth scope |
| Data residency requirement not met | Tool requires data stay in specific region; agent calls tool from other region |
| PII handling constraint violation | Tool requires special PII handling; agent violates constraint |
| Regulatory constraint violation | Tool can only be called for specific data types; agent calls for wrong type |
| Network requirement not met | Tool requires allowlisted IP, VPN, or special network; agent calls from wrong network |

**Total: 6 patterns**

## Related Goals

- [Tool Access Scope Limits](../tool-access-scope-limits/) — access control is one form of constraint
- [System Integration](../system-integration/) — integration constraints
- [Observability Monitoring](../observability-monitoring/) — constraint violations should be detected and logged
