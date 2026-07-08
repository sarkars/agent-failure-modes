# Wrong Id/Key Usage

## Issue: Agent uses customer ID as account ID, message ID as thread ID, etc.

**Frequency**: Common

**Symptoms**
- Correct API called on wrong object.
- [Add more specific symptoms]

**Root Cause**
Agent uses customer ID as account ID, message ID as thread ID, etc.

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
1. **Nominal ID Typing**: Distinct ID types (customer_id, account_id, message_id, thread_id) are represented as distinct branded/nominal types — not interchangeable strings — in the tool-calling layer, so passing a customer_id where an account_id is expected is a type-level, schema-caught error rather than a silent runtime mix-up.
2. **Schema-Bound Key Validation with Format/Prefix Checks**: Each ID type has a recognizable format (prefix, length, checksum) enforced at the tool-call boundary; a validator rejects calls where the ID's format doesn't match what the target parameter expects (e.g., an `acct_` prefix required for account_id).
3. **Lookup-Before-Use Confirmation**: Before using an ID retrieved from one context (a customer_id from a search result) as an argument to a different-scoped call, the orchestrator confirms the ID's type/scope matches via a lightweight lookup or metadata check, rather than passing it through blind.

### Detection & Response
1. **Cross-Entity API Response Mismatch Detection**: When a call "succeeds" but the returned object's type/fields don't match what was expected for that ID's presumed type (asked for an account, got back message-like fields), the system flags it as a likely wrong-ID-type incident even though the call didn't error.
2. **ID-Type Confusion Pattern Mining**: The system logs the (parameter_name, actual_id_format) pair for every tool call and periodically mines for calls where the ID format doesn't match the parameter's declared type, surfacing systemic confusion even in cases that didn't hard-fail.
3. **Wrong-Object-Acted-On User Correction**: User corrections indicating the agent acted on/reported the wrong entity ("that's not my account, that's my order") are tracked and correlated with the ID values used in the preceding tool calls to confirm ID-mixup as root cause.

### Architecture Patterns
1. **Typed ID Wrapper Library**: All IDs entering the agent's working context are wrapped in typed value objects (`CustomerId`, `AccountId`) generated from the API schema, and tool-call construction is done through typed helper functions that won't validate if the wrong ID type is passed.
2. **Entity Resolution Gateway**: A shared "resolve entity" service takes any ID plus a claimed type and returns the canonical, verified entity — or an explicit type-mismatch error — before downstream tools use it, centralizing the type/scope check instead of trusting each tool call site.
3. **Relationship Graph Lookup**: For nested entities (a message belongs to a thread belongs to a conversation), a relationship-graph service lets the agent request "the thread_id for this message_id" explicitly rather than assuming one ID can substitute for a related one.

### Metrics
1. **id_type_format_mismatch_rate_percent**: Target: < 0.5% of calls; Alert threshold: > 2%
2. **wrong_entity_acted_on_user_corrections_per_week**: Target: < 1; Alert threshold: >= 3
3. **entity_resolution_gateway_rejection_rate_percent**: Target: tracked baseline; Alert threshold: sudden spike
4. **typed_id_coverage_percent**: Target: 100% of tool calls use typed ID wrappers; Alert threshold: < 95%

### Alerts
1. **ID Type Mismatch Blocked** (P2 - Warning): Condition - the entity resolution gateway rejects a call due to ID/parameter type mismatch. Action: Log full context, alert on repeated occurrences from the same code path/prompt.
2. **Wrong-Entity Action Confirmed** (P1 - Critical): Condition - user or reconciliation confirms an action was taken on the wrong entity due to ID confusion. Action: Immediate incident, assess and reverse/correct the wrong-entity action, audit the ID-sourcing path.
3. **Format Mismatch Rate Spike** (P3 - Info): Condition - id_type_format_mismatch_rate_percent exceeds threshold for a tool. Action: Review recent changes to ID-sourcing logic or upstream API ID format changes.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
