# Read Only Agent Write Access

## Issue
An agent is deliberately provisioned with read-only access to a data source — the intent being it can look things up but never modify anything — yet a misconfigured tool binding, an overly broad service credential, or an undocumented fallback code path still allows write operations to succeed. The read-only boundary exists in configuration or documentation but isn't actually enforced at the point where the write would occur.

**Frequency**: Common

**Symptoms**
- An agent's database credential has broader grants (e.g. `SELECT, INSERT, UPDATE`) than the "read-only" label implies, often because the credential was copied from a different, write-capable service
- A tool named `query_database` or `search_records` internally uses a client library capable of writes, and no query-type filter blocks non-SELECT statements
- The agent successfully executes an action described as impossible in its own documentation or system prompt ("this agent cannot modify records")
- A fallback or error-handling code path (e.g. "if lookup fails, create a placeholder record") performs a write despite the primary tool being read-only
- Infrastructure-as-code defines a read-only role, but the actual deployed credential doesn't match the defined role due to a manual override or stale rotation

## Root Cause
Read-only is a property that must be enforced at the lowest layer capable of performing the write — typically the database credential's grants or the API key's scope — because anything enforced only above that layer (tool description, system prompt, application-level routing) can be bypassed by an unexpected code path, a raw query construction bug, or an LLM that generates a write-shaped request the tool wrapper doesn't anticipate and filter. When teams treat "read-only" as a label on the tool rather than a property of the underlying credential, any gap between the two becomes exploitable.

## Example
```
1. An internal analytics agent is described as "read-only access to the customer database" and is given a
   tool called run_query(sql) intended for SELECT statements only.
2. The database credential configured for the agent's service account was copied from an existing
   internal-tools service during setup and retains INSERT/UPDATE/DELETE grants, because no one audited
   the actual GRANT statements against the "read-only" label.
3. The tool wrapper does basic prompt-level guidance ("only generate SELECT queries") but performs no
   server-side statement-type validation before executing the SQL it receives.
4. A user asks the agent an ambiguous question that causes it to generate an UPDATE statement intended to
   "fix" a data inconsistency it noticed while answering the read query.
5. The database accepts and executes the UPDATE, because the credential's actual grants allow it -- the
   read-only boundary existed only in the tool's name and documentation, not in the database permissions.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of "read-only" service credentials in production systems carry write grants beyond what the label implies, typically from credential reuse or copy-paste setup | Common finding in database access audits |
| Statement-type filtering implemented only at the application layer (not the database grant layer) is frequently bypassable through query construction edge cases | Typical finding in SQL-tool security reviews |
| Enforcing read-only at the database grant level, rather than the application layer alone, closes the large majority of these gaps | Standard remediation for least-privilege credential findings |

## Mitigations
1. **Enforce read-only at the credential/grant layer**: Provision the actual database user or API key with only SELECT/read grants, so writes fail at the data layer even if application logic tries to issue one.
2. **Add defense-in-depth query validation**: In addition to grant-level enforcement, parse and reject any generated query that isn't a read statement before it's sent to the database.
3. **Audit credential grants against their documented access level on a schedule**: Periodically diff each service account's actual grants against its intended access tier and flag mismatches automatically.
4. **Never reuse credentials across services with different access needs**: Provision a distinct, purpose-specific credential for each agent/tool rather than copying an existing one with broader scope.
5. **Remove write-capable fallback paths from read-only tools**: Audit error-handling and "self-healing" logic in read-only tools for any code path that performs a write, and eliminate or gate it separately.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| write_statements_from_readonly_credential | Count of non-SELECT statements executed using a credential labeled read-only | > 0 per day |
| credential_grant_drift | Read-only credentials whose actual database grants include write permissions | > 0 (checked on a recurring schedule) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Write executed via read-only agent | A read-only labeled tool/credential successfully performs an INSERT/UPDATE/DELETE | Critical | Revoke write grants immediately, roll back the write if possible, audit the credential's history |
| Grant drift detected | Scheduled audit finds a read-only credential with write grants | High | Rotate credential with corrected grants, investigate how the drift occurred |

## Related Patterns
- [Granular CRUD Permission Not Enforced](./granular-crud-permission-not-enforced.md) - this pattern is the specific, most severe case of granular CRUD enforcement failing (full write access instead of intended zero-write)
- [Role Permission Mismatch](./role-permission-mismatch.md) - both describe the agent's actual access diverging from the access its assigned role or label implies
- [Admin Operation Called By Non-Admin](./admin-operation-called-by-non-admin.md) - same underlying failure of enforcing a boundary only at the label/description layer instead of the execution layer
