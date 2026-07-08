# Memory Privilege Leak

## Issue: Agent uses private memory in inappropriate context.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Sensitive prior context appears in current answer.
- [Add more specific symptoms]

**Root Cause**
Agent uses private memory in inappropriate context.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Context-Scoped Access Control Lists**: Every memory record is tagged with an access scope (owner_user_id, sharing_tier, allowed_contexts such as "support_ticket" vs "public_chat"). The retrieval layer enforces the ACL as a hard filter at query time — a record tagged private-to-context-A can never be returned when assembling context for context-B, regardless of semantic relevance.
2. **Purpose-Limitation Tagging**: Memory is tagged with the purpose it was collected for (e.g., billing_support, medical_intake). Retrieval queries declare their purpose, and records are only eligible if the query purpose matches or is explicitly allowlisted against the record's purpose tag, preventing reuse of sensitive context outside its original consent scope.
3. **Multi-Tenant/Multi-User Isolation at the Store Level**: Memory stores are partitioned (separate indexes or hard row-level security) per tenant/user rather than relying on application-layer filtering alone, so a bug in prompt construction cannot cross-contaminate another user's private memory even if the ACL check is skipped.

### Detection & Response
1. **Sensitive-Content Leak Scanner**: Run outgoing responses through a classifier that checks for patterns matching known-sensitive memory categories (health, financial, legal, other-user identifiers) and cross-references whether that content's source memory was scoped to the current context. Flag any mismatch as a privilege leak.
2. **Cross-Context Injection Audit**: Log, for every response, the list of memory_ids injected into the prompt along with their access scope and the current request's context. A scheduled audit job flags any injected memory whose scope did not match the serving context, even if generation happened to filter it out of the final text.
3. **Canary Memory Records**: Seed test accounts with synthetic "canary" private facts and periodically probe the system from a different context/user to confirm the canary never surfaces; any leak is caught before it affects real users.

### Architecture Patterns
1. **ACL-Enforcing Retrieval Gateway**: All memory reads pass through a single gateway service that resolves the caller's context and purpose, applies ACL and purpose-limitation filters at the query layer (not post-hoc filtering of results), and returns only in-scope records — fail-closed on missing scope metadata.
2. **Tenant-Partitioned Memory Store**: Physically or logically partition memory storage per tenant/user with row-level security enforced by the database itself, so cross-tenant leakage requires a database-level bypass rather than an application logic bug.
3. **Redaction Layer on Generation Output**: A final output-scrubbing pass checks generated text against a registry of known-sensitive tokens tied to out-of-scope memory records for the current context and redacts/blocks before the response is sent, as a last line of defense.

### Metrics
1. **privilege_leak_incidents_per_month**: Target: 0; Alert threshold: > 0 (any incident is critical)
2. **acl_filter_bypass_rate_percent**: Target: 0%; Alert threshold: > 0% detected via audit
3. **canary_leak_detection_count**: Target: 0; Alert threshold: > 0
4. **cross_context_injection_rate_percent**: Target: 0%; Alert threshold: > 0.1% of audited responses

### Alerts
1. **Sensitive Memory Leak Detected** (P1 - Critical): Condition - sensitive-content scanner or canary probe confirms out-of-scope memory appeared in a response. Action: Immediate incident, pull the response, notify security/privacy team, assess breach notification obligations, patch the ACL gap.
2. **ACL Filter Bypass Found in Audit** (P1 - Critical): Condition - cross-context injection audit finds a memory record served outside its scope even if not visibly leaked in text. Action: Freeze retrieval gateway deploys, root-cause the filter bug, re-audit recent traffic for exposure window.
3. **Missing Scope Metadata** (P2 - Warning): Condition - a memory record was written without ACL/purpose tags (fail-open risk). Action: Quarantine the record from retrieval until tagged, alert data-ingestion owners to fix the write path.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Critical |

---

## References

- [OWASP-LLM-Top10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Note: LLM application risks including prompt injection, insecure output handling, supply chain, sensitive information disclosure, excessive agency.
