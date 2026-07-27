# What Are the Most Common Tool Invocation Failures in AI Agents?

**Tool invocation fails when agents pass wrong arguments, use wrong ID or key formats, misunderstand tool semantics, fail to page results, or retry non-idempotent operations without side-effect awareness.** The 12 invocation patterns documented here cover the challenge of calling tools correctly — from parameter validation through pagination, query scoping, timezone handling, and understanding when operations are idempotent. Invocation failures are particularly common because agents must understand and respect tool contracts (what parameters it accepts, what they mean, what side effects occur), and misunderstanding any part of that contract leads to failed or incorrect tool calls.

## Key Takeaways

- 12 patterns documented: parameter validation, ID/key usage, query scoping, pagination, timezone, idempotency, side effects, rate-limiting, result handling, and format errors.
- Missing Required Parameter and Wrong Argument Format are most severe: missing required parameters cause tool failures, wrong format (string vs integer) causes parsing errors.
- Over Broad Query and Over Narrow Query are second-order: agents don't scope queries correctly, returning too much (inefficient, expensive) or too little (missing relevant results) data.
- Idempotency Failure and Side Effect Misunderstanding are architectural failures: agents don't know whether operations are idempotent or what side effects they cause, leading to unwanted retries or cascading effects.

## Scope

- **Parameter and Format Correctness** — [Missing Required Parameter](failures/missing-required-parameter.md), [Wrong Argument Format](failures/wrong-argument-format.md), [Wrong ID/Key Usage](failures/wrong-idkey-usage.md). Arguments must be provided, formatted correctly, and reference correct IDs; missing or malformed arguments cause failures.
- **Scoping and Boundaries** — [Over Broad Query](failures/over-broad-query.md), [Over Narrow Query](failures/over-narrow-query.md). Queries must be scoped correctly; too broad returns expensive results, too narrow misses relevant data.
- **Temporal and Measurement** — [Wrong Date Range/Timezone](failures/wrong-date-rangetimezone.md), [Wrong Units/Currency](failures/wrong-unitscurrency.md). Date ranges, timezones, units must be correct; timezone mismatch returns data from wrong time period, unit mismatch causes wrong calculations.
- **Result Handling** — [Pagination Failure](failures/pagination-failure.md), [Partial Result Misuse](failures/partial-result-misuse.md). Results may be paginated; agents must handle pagination or may miss results; agents must not use partial results as if they were complete.
- **Safety and Semantics** — [Idempotency Failure](failures/idempotency-failure.md), [Side Effect Misunderstanding](failures/side-effect-misunderstanding.md), [Rate Limit/Timeout Mishandling](failures/rate-limittimeout-mishandling.md). Agents must understand idempotency and side effects; retrying non-idempotent operations causes duplicates, misunderstanding side effects causes cascading failures.

## When Tool Invocation Matters

- Agents invoke tools with complex parameters where correct formatting and scope matter.
- Tools have side effects or state changes; retrying without idempotency awareness causes duplicate writes.
- Tools return paginated results; agents must navigate pagination to get complete data.

## Cross-Pattern Insight

The 12 invocation patterns describe systems where tool semantics are implicit: agents guess what parameters mean, whether operations are idempotent, whether queries are scoped correctly, without explicit validation or documentation. Tool documentation exists but is incomplete, and agents must infer semantics from example usage or error messages. Most teams discover invocation failures only after agents start calling tools incorrectly and cascading failures reveal the misunderstandings. The mitigation that recurs across nearly every pattern is explicit contract validation: use API contracts to specify required parameters and their formats, document idempotency and side effects explicitly, test tool invocation with correct and incorrect parameters, and add agent-level validation before calling tools.

## Frequently Asked Questions

### How do you prevent wrong-argument-format errors?
Per [Wrong Argument Format](failures/wrong-argument-format.md), validate argument types and formats before calling tools: check that IDs are strings not integers, dates are ISO 8601 not user-locale format, amounts are in correct currency. Use API contracts (OpenAPI, schema) to specify expected formats and validate against them.

### What should an agent do if pagination is required?
Per [Pagination Failure](failures/pagination-failure.md), agents should check for pagination metadata (e.g., `has_next`, `next_token`), and iterate through all pages rather than assuming first page is complete. Test pagination by requesting large result sets and verifying all results are retrieved.

### How do you understand tool idempotency?
Per [Idempotency Failure](failures/idempotency-failure.md), ask the tool documentation: is calling this operation twice with same parameters safe? If yes, idempotent; if no, non-idempotent. Never retry non-idempotent operations automatically — log the failure and require manual intervention or explicit retry logic that accounts for side effects.

### Can over-broad queries be optimized after the fact?
Partially — per [Over Broad Query](failures/over-broad-query.md), agents should scope queries before calling (filter by date range, category, etc.) rather than retrieving everything and filtering client-side. Over-broad queries waste resources and cost; filter server-side first.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Idempotency Failure](failures/idempotency-failure.md) | Non-idempotent operation is retried; retries cause duplicate writes or state corruption |
| [Missing Required Parameter](failures/missing-required-parameter.md) | Tool requires a parameter; agent doesn't provide it; call fails |
| [Over Broad Query](failures/over-broad-query.md) | Query is not scoped; returns expensive results; agent wastes resources and cost |
| [Over Narrow Query](failures/over-narrow-query.md) | Query is over-scoped; misses relevant results; agent gets incomplete data |
| [Pagination Failure](failures/pagination-failure.md) | Results are paginated; agent doesn't iterate through pages; misses data |
| [Partial Result Misuse](failures/partial-result-misuse.md) | First page of paginated results is used as if it's complete; missing data treated as not-found |
| [Rate Limit/Timeout Mishandling](failures/rate-limittimeout-mishandling.md) | Tool returns rate-limit or timeout error; agent doesn't backoff appropriately |
| [Side Effect Misunderstanding](failures/side-effect-misunderstanding.md) | Agent doesn't understand or underestimates operation side effects; cascading failures result |
| [Wrong Argument Format](failures/wrong-argument-format.md) | Argument format is wrong (string vs integer, ISO date vs locale date); tool parsing fails |
| [Wrong Date Range/Timezone](failures/wrong-date-rangetimezone.md) | Date range is wrong timezone; agent retrieves data from wrong time period |
| [Wrong ID/Key Usage](failures/wrong-idkey-usage.md) | Agent uses wrong ID format or references wrong ID; retrieves wrong record |
| [Wrong Units/Currency](failures/wrong-unitscurrency.md) | Units or currency are mismatched; calculations are incorrect |

**Total: 12 patterns**

## Related Goals

- [Tool Reliability](../tool-reliability/) — invocation correctness affects tool reliability
- [Tool Selection](../tool-selection/) — selecting the right tool complements correct invocation
- [Observability Monitoring](../observability-monitoring/) — invocation errors should be logged and analyzed
