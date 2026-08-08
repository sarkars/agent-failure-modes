# Over-Scoped Credentials

## Issue: Agent has broad access when narrow scope was enough.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Credential can access unrelated systems/data.
- Single API token grants permissions to read/write/delete across multiple databases/services.
- Agent credential includes wildcards or overly broad scopes (e.g., "all databases" instead of "product_db only").
- Service account used by agent also has admin/root permissions in production environment.
- Credential has been in use for 6+ months without review or re-authentication.
- Same credential used across dev, staging, and production environments.

**Root Cause**
Credentials are provisioned once, broadly, for convenience — a single token covering every operation an agent might ever need — rather than scoped per task to the minimum permissions that task actually requires, and no access-control review at deployment time questions whether each granted permission is necessary. Because nothing logs which permissions a credential actually exercises in practice, over-scoping goes undetected indefinitely, and without a rotation or expiration policy the same broad credential remains valid and usable long after the context that justified its scope has changed. The result is that a single compromised credential grants an attacker the union of everything the agent could ever theoretically need, rather than only what it needed for the specific operation being carried out at the time of compromise.

**Example**
```
Scenario: E-commerce platform uses a single service account for multiple agents.

Setup:
- Agent is designed to process refunds on customer orders.
- Service account has permissions: ["databases:read:*", "databases:write:*", "admin:users:read"]
- Credential is stored in plaintext in config file with git history.

Attack/Failure:
1. Attacker gains access to agent config (via Git history, CI/CD logs, or compromised host).
2. Attacker extracts the API key.
3. Uses key to access:
   - Customer payment database (customer_db) → exports 100K credit cards
   - Internal audit database (audit_db) → deletes evidence of unauthorized access
   - User management (admin API) → creates new admin account for persistent backdoor

Impact:
- PCI DSS violation (payment data exposure)
- Loss of audit trail
- Attacker maintains persistent admin access
- Regulatory fine of $10K-$100K+ per card exposed
- Customer trust loss and likely lawsuits
```

**Contributing Factors**
- Credential provisioning follows convenience-over-security principle; one token for all agent use cases.
- No access control policy review before deployment (assumed safe if "for agents").
- Credentials stored in source code, config files, or environment variables with insufficient access controls.
- No credential rotation policy or expiration date enforced.
- Insufficient logging of which permissions each credential actually uses.
- Team unfamiliar with least-privilege principle; assume "admin" tokens are necessary.
- Credential granted to service account in multiple environments without tenant/environment isolation.
- No segregation of duties (refund agent should not have audit log deletion access).

---


## Test Scenario & Reproduction

### Scenario Setup
- Agent has credentials with excessive permissions
- Credentials used for all operations
- No principle of least privilege
- No per-operation permission scoping

### Trigger Mechanism
```
1. Agent credentials: admin permissions for entire database
2. Attacker compromises agent or injects malicious prompt
3. Agent/attacker can delete, modify any database record
4. User credentials bypass normal access controls
5. Entire database modified or deleted
```

### Expected Failure State
- Agent credentials grant excessive permissions
- Single compromised credential affects entire system
- No granular access control per operation
- Attacker gains full database access

### Mitigation Validation Protocol
**Test Checklist:**
- [ ] Reproduce: Credential compromise affects entire system
- [ ] Apply mitigations (least privilege, scoped credentials)
- [ ] Re-run attack → limited to specific operations
- [ ] Test permission boundaries

**Success Criteria:**
- Credentials scoped to minimum required permissions
- Each operation has dedicated low-privilege credential
- Credential compromise limits damage scope

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Refund agent attempts admin action | Refund agent's credential used to call `admin:users:read` | Call rejected — refund credential scoped to refund DB only | Call succeeds, admin data returned |
| Credential compromise blast-radius test | Simulated theft of the agent's API key, attempt lateral access to unrelated services | Access limited to the single scoped resource | Compromised key accesses multiple unrelated databases/services |
| Stale credential audit | Credential unused/unreviewed for 90+ days | Flagged for review or auto-revoked | Credential remains active with full original scope indefinitely |
| In-scope legitimate action | Refund agent processes a refund within its scoped database | Action succeeds normally | N/A (control case) |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Agents with least-privilege (single-purpose) credentials | 100% | % of agent service accounts whose granted permissions match their documented minimum required scope |
| Credential blast-radius on simulated compromise | Limited to 1 resource/system | Red-team exercise measuring how many distinct systems a single compromised credential can reach |
| Credentials past rotation/review deadline | 0 | Count of active credentials exceeding the defined max age (e.g., 90 days) without re-approval |

---

## Mitigation Strategies

### Prevention
1. **Scoped credentials per agent**: Each agent gets a dedicated credential with minimal necessary permissions. Refund agent only has refund database read/write, not user management or audit log access.
2. **Automated access review cycle**: Quarterly or semi-annual review of agent credentials. Question each permission: "Does this agent actually need this?" Revoke unused permissions.
3. **Credential rotation policy**: Enforce credential expiration (max 90 days). Rotate automatically or require re-approval to extend.
4. **Secrets management system**: Store credentials in vault (AWS Secrets Manager, HashiCorp Vault), not in code. Audit all access to secrets.
5. **Environment-specific credentials**: Use different credentials for dev/staging/prod. Never reuse production credentials in non-prod.
6. **Segregation of duties**: Separate read permissions from write, write from delete, normal operations from admin operations across different credentials.
7. **Capability-based tokens**: Use token systems that explicitly list allowed operations (not role-based wildcards). Example: `token_can_read:refunds_db_2024` not `token_role:admin`.

### Detection
- Credential can access unrelated systems/data.

### Recovery
**Immediate (Stop the Attack)**
1. Revoke the compromised credential immediately in all systems (IAM, API key vault, database ACLs).
2. Terminate any active sessions or connections using that credential.
3. If credential was exposed in git history, force-push to remove it and invalidate all clones.
4. Block associated IP addresses or API consumer IDs if identifiable.

**Investigation (Understand Scope)**
1. Retrieve API/database audit logs for all actions using the compromised credential in the last 30-90 days.
2. Identify all systems the credential could access (cross-reference with IAM policy, database user permissions).
3. For each system, query audit logs for unauthorized reads/writes/deletes (data export, admin account creation, audit log deletion).
4. Correlate with external threat intelligence (IP reputation, WHOIS) to determine if attacker is known threat actor.
5. Estimate data exposure: how many records were read? Which customer/transaction IDs?

**Remediation (Prevent Recurrence)**
1. Implement least-privilege credentials and automated access review (see Prevention).
2. Audit all other service accounts for over-scoping; create remediation plan.
3. Rotate all credentials across the infrastructure (even ones not directly impacted, to be safe).
4. Implement credential secrets scanning in CI/CD and code repositories to prevent re-exposure.
5. Notify affected customers per regulatory requirements (GDPR, CCPA, PCI DSS).
6. Conduct post-incident review to identify process gaps (code review, secrets scanning, access control).

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| Credentials with wildcard/`admin:*`-style scopes | > 0 |
| Credentials unrotated past policy age (e.g., 90 days) | > 0 |
| Cross-system access events from a single-purpose credential | > 0 |
| Service accounts without a documented minimum-scope justification | > 0 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Credential Used Outside Documented Scope | An agent credential is used to access a system/resource not in its documented least-privilege scope | Critical |
| Wildcard/Admin-Scoped Credential Detected | Access-review scan finds a credential granted broad or wildcard permissions | Critical |
| Credential Rotation Overdue | A credential's age exceeds the policy rotation window without renewal | High |

---

## References

- [CSA-Agentic-Profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)
- Note: Agentic AI governance profile built around NIST RMF.
