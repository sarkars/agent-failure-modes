# Data Leakage

## Issue: Agent Exposes Sensitive Information

**Frequency**: Common

**Symptoms**
- Private data appears in responses
- Training data leaked through outputs
- User A's data shared with User B
- Internal information exposed externally

**Root Cause**
- No data classification or access controls
- Agent trained on or has access to sensitive data
- Output not filtered for sensitive content
- Session isolation failures

**Example**
```
User: "Show me an example customer record"

Agent: "Here's an example:
Name: John Smith
SSN: 123-45-6789
Address: 123 Main St..."

Result: Real customer PII exposed as "example"
```

**Real Incidents**
- 61% of AI agent security incidents involved sensitive data exposure
- Samsung employees leaked confidential code via ChatGPT
- Customer service bots exposing other customers' data

## Mitigation Strategies

### Prevention
1. **Mandatory data classification enforced before agent access**: Tag every data source (customer records, internal docs) with a classification label at ingestion, and gate the agent's retrieval layer so it can only access data whose classification matches the current session's authorization level, since the root cause is explicitly "no data classification or access controls" — the example's SSN exposure happened because nothing distinguished "real customer record" from "safe example data." Trade-off: retrofitting classification onto existing unlabeled data stores is a significant one-time effort, and misclassified data creates false confidence.
2. **Synthetic-only data for demonstrative/example requests**: Maintain a dedicated synthetic dataset for any request pattern resembling "show me an example," and route such requests to the synthetic source exclusively, structurally preventing the exact failure in the example where a request for "an example customer record" returned real PII. Trade-off: requires building and maintaining a realistic synthetic dataset that stays representative enough to be useful without ever touching production data.
3. **Strict session isolation preventing cross-user context bleed**: Architect session/context management so one user's conversation state, retrieved documents, or cached data can never be read into another user's session, directly preventing the documented pattern of "User A's data shared with User B" and the cited customer-service-bot incidents. Trade-off: strict isolation can complicate legitimate cross-session features (e.g., shared team knowledge bases) which now need explicit, audited exceptions rather than implicit shared state.

### Detection & Response
1. **PII/sensitive-pattern output filtering before response delivery**: Run every agent response through pattern-matching/DLP scanning for PII formats (SSNs, addresses, account numbers) and credential-shaped strings before delivery, redacting matches, catching leaks like the SSN in the documented example at the last line of defense.
2. **Cross-user data access monitoring in multi-tenant sessions**: Monitor retrieval and context-construction operations for any case where data tagged as belonging to one user/tenant appears in another user's session, directly targeting the "session isolation failures" root cause and enabling fast detection of the customer-service cross-contamination pattern.
3. **DLP integration with real-time blocking, not just post-hoc alerting**: Integrate a DLP system directly into the response pipeline (not just log analysis after the fact) so sensitive-pattern matches can block delivery in real time, since the 61% incident-rate statistic implies detection-after-delivery is too late to prevent the exposure itself.

### Architecture Patterns
1. **Classification-aware retrieval-access-control layer**: Architect the data-retrieval layer (RAG index, database queries) to enforce classification-based access control at the query level, so the agent's retrieval mechanism structurally cannot return data above the requesting session's clearance, rather than relying on the LLM to voluntarily withhold it.
2. **Synthetic-data sandbox for demonstration and training contexts**: Maintain a fully separate synthetic-data environment that demonstration/example-request handling is hard-routed to, isolated from any path that could reach the production data store, so "show an example" requests have no code path to real PII.
3. **Tenant-isolated session and context storage**: Architect session state, conversation history, and retrieval caches with hard per-user/per-tenant partitioning (separate storage namespaces or encryption keys), so a session-isolation bug fails closed (no data returned) rather than failing open (wrong user's data returned).

### Metrics
1. **unclassified_data_access_rate**: Target: 0% of agent data access hits unclassified/unlabeled sources; Alert on any access to unclassified data
2. **pii_pattern_leak_rate**: Target: 0 confirmed PII pattern matches delivered in responses per month; Alert on any confirmed match
3. **cross_tenant_data_access_incidents**: Target: 0 instances of one user's session containing another user's tagged data; Alert on any occurrence
4. **example_request_synthetic_routing_pct**: Target: 100% of demonstrative/example requests are served from the synthetic dataset; Alert on any example request that touches the production data store

### Alerts
1. **PII Detected in Agent Output** (P1): Condition - the output DLP scan matches a PII pattern (SSN, account number, address) in a response about to be delivered. Action: Block delivery, redact and regenerate, audit how the underlying data reached the agent's context.
2. **Cross-Tenant Data Access Detected** (P1): Condition - data tagged to one user/tenant appears in another user's session context or response. Action: Terminate the affected session immediately, notify both affected users per policy, investigate the session-isolation failure.
3. **Example Request Served Real Data** (P2): Condition - a request matching the "show me an example" pattern retrieved data from the production/classified store rather than the synthetic dataset. Action: Block the response, fix the routing logic, audit for prior instances of the same misrouting.

## References

## References
- [VentureBeat: 88% Enterprises Breached](https://venturebeat.com/security/most-enterprises-cant-stop-stage-three-ai-agent-threats-venturebeat-survey-finds/) - 61% data exposure
- [Kiteworks: 65% of Firms Hit](https://www.kiteworks.com/cybersecurity-risk-management/ai-agent-security-incidents-2026/)
- [Beam AI: 5 Real AI Agent Security Breaches 2026](https://beam.ai/agentic-insights/ai-agent-security-breaches-2026-lessons)
