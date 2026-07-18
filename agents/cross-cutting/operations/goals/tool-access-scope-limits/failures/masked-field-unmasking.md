# Masked Field Unmasking

## Issue
A field is designed to be masked or redacted before it reaches an agent — for example, a credit card number shown as `****-****-****-1234` or an SSN shown as `***-**-6789` — but the masking is applied in only one code path (typically the primary "get record" response), and a different query pattern through the same tool reaches the underlying unmasked value. Common triggers include export/bulk endpoints, search-and-filter queries that echo the matched raw value, join operations that pull the field from a different table without the masking view applied, or raw API parameters that request a specific field by name.

**Frequency**: Common

**Symptoms**
- The standard "view record" tool call correctly masks a field, but a search, export, or filter tool call on the same underlying data returns it unmasked
- Masking works when the field is displayed but not when it's used as a search/filter criterion, because matching against the raw value requires the raw value to be present somewhere in the pipeline
- Unmasked values appear in logs or intermediate tool outputs even though the final user-facing response is masked
- A newly added tool or integration re-implements its own query against the base table instead of the masked view, silently losing the masking
- Security review of the masking view catches direct queries but misses joins or aggregations that pull the underlying column through a different alias

## Root Cause
Masking is typically implemented as a presentation-layer transform — a database view, a response serializer, or a redaction step applied just before the final response is constructed — rather than as a property enforced on the underlying data itself. Any code path that reads from the base table/column directly, rather than through the designated masked view or serializer, bypasses the transform entirely. Agent tools that support flexible querying (search, filter-by-value, export, join-based lookups) are especially prone to this because they often need to touch the raw value internally (e.g., to match a search term) even when the intent is to mask it in the final output, and it's easy for that internal raw access to leak into the response.

## Example
```
A customer-service tool masks payment card numbers in its standard
"get customer" response, showing only the last four digits, by querying
a database view (`customers_masked`) that applies the mask at the SQL
level. A separate "search customers by payment method" tool, added
later to help agents find duplicate cards, was built directly against
the base `customers` table for performance reasons, since the masked
view doesn't support efficient prefix matching.

A support agent asks the assistant to "find any other accounts using
this same card." The assistant calls the search tool, which queries the
base table and returns full unmasked card numbers for every matching
account in its result set, because the tool was never routed through
the masking view — even though the exact same agent, moments earlier,
received a properly masked number when looking up the original
customer record directly.
```

## Statistics
| Finding | Context |
|---------|---------|
| Masking bypasses via search, export, or join paths are among the most commonly identified gaps in data-redaction audits, more so than direct view-bypass via raw table access | Common in enterprise data-masking implementations |
| Newly added tools built against base tables for performance or flexibility reasons are disproportionately represented in masking-bypass incidents compared to tools built against the original masked view | Typical pattern in tool-sprawl over shared datasets |
| Masked values are frequently found unmasked in intermediate logs (query logs, tool-call traces) even in systems where the final user-facing response is correctly masked | Common in logging-pipeline audits |

## Mitigations
1. **Mask at the storage/access-control layer, not presentation only**: Implement masking via row/column-level security or a hard access boundary at the database layer so that no query path — including new tools built later — can retrieve the raw value without an explicit elevated grant.
2. **Single source-of-truth masked interface**: Require all tools reading a masked field to go through one shared data-access interface (view, service, or API), and block direct base-table access for any new tool by default.
3. **Search/filter without raw exposure**: For search-by-masked-value use cases, implement matching via a hashed or tokenized index rather than the raw value, so a search tool can confirm a match without ever having the plaintext value flow through its response path.
4. **Log-path masking parity**: Apply the same masking transform to any logging, tracing, or debug-output pipeline that a tool's raw query result passes through, not just the final user-facing response.
5. **Automated unmasking regression tests**: For every tool touching a masked field, add a test asserting the response never contains the unmasked pattern (e.g., a full 16-digit card number), run on every deploy.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `unmasked_value_in_response_count` | Count of tool responses matching the unmasked pattern of a field designated for masking | Alert threshold: > 0 (any occurrence) |
| `unmasked_value_in_log_count` | Count of log/trace entries containing the unmasked pattern | Alert threshold: > 0 (any occurrence) |
| `base_table_direct_query_count` | Count of tool queries bypassing the designated masked view/interface for a masked field's underlying table | Alert threshold: > 0 for any new tool |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unmasked Value Returned | A tool response contains an unmasked pattern for a field designated for masking | P1 | Halt the tool immediately, rotate/notify affected data subjects per policy, patch the bypass |
| New Tool Bypassing Masked View | A newly deployed tool queries the base table directly instead of the masked interface | P2 | Block deploy or require immediate remediation before it reaches production traffic |

## Related Patterns
- [Sensitive Field Access Not Restricted](./sensitive-field-access-not-restricted.md) - masking is one specific control that sensitive fields rely on, and this pattern is what happens when that control is bypassed rather than absent
- [Field-Level Access Not Restricted](./field-level-access-not-restricted.md) - both involve controls that exist for a field but aren't consistently enforced across every access path
- [PII Field Leakage In Responses](./pii-field-leakage-in-responses.md) - a closely related failure where redaction works in the primary channel but not in a secondary one
