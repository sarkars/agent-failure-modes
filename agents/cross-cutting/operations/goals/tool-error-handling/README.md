# What Are the Most Common Tool Error Handling Failures in AI Agents?

**Tool error handling fails when error codes change meaning between API versions or services, when error response formats are inconsistent, or when agents cannot distinguish between different failure modes and apply inappropriate recovery strategies.** The 2 error-handling patterns documented here cover the challenge of interpreting tool errors consistently — from error codes that have different meanings in different contexts (a 429 might mean rate-limited or out-of-quota depending on service), through response format inconsistencies that make parsing fragile, to scenarios where the same error code means different things at different times. Error handling is particularly fragile in agents because agents must interpret errors and decide how to recover (retry, fallback, fail), and interpreting an error incorrectly (treating transient network errors as permanent failures) causes cascade failures downstream.

## Key Takeaways

- 2 patterns are documented here, spanning error-code semantic drift and response-format inconsistency.
- Error Code Semantic Drift is the most severe in multi-service ecosystems: a 429 might mean rate-limited in service A but out-of-quota in service B, and applying rate-limit recovery to a quota-exceeded error makes the problem worse.
- Error Response Format Inconsistency is a second-order failure: some services return error details in JSON body, others in HTTP headers, others in a separate error-details endpoint, and parsing code that works for one service breaks for another.
- Both patterns share a root cause: error semantics are not standardized, so agents must either handle each service's error format specially or use generic error handling that masks important distinctions between error types.

## Scope

- **Error Code Semantics** — [Error Code Semantic Drift](failures/error-code-semantic-drift.md). Same error code means different things in different services or API versions; agent's recovery strategy is inappropriate for the actual error.
- **Response Format** — [Error Response Format Inconsistency](failures/error-response-format-inconsistency.md). Different services return errors in different formats (JSON vs text, body vs headers); parsing code that works for one service fails for another.

## When Tool Error Handling Matters

- An agent calls multiple tools from different services, where error codes and formats differ across services.
- Recovery decisions depend on error type (transient vs permanent, rate-limit vs permanent failure), and misinterpreting error type causes inappropriate recovery.
- New API versions or services are added over time, and error codes change meaning as systems evolve.

## Cross-Pattern Insight

The 2 error-handling patterns describe systems where error semantics are implicit: agents must guess what an error means based on code, message, and context, and wrong guesses lead to wrong recovery strategies. Retrying a permanent failure wastes resources; treating a transient error as permanent causes unnecessary fallback. Most teams discover error-handling failures only after a cascade: a service returns a 429, the agent retries infinitely, and the retry storm brings down the service. The mitigation that recurs across both patterns is the same architectural move — standardize error semantics: use a common error taxonomy (transient, permanent, quota-exceeded, authentication-failed, etc.) and map each service's error codes and formats to the taxonomy. Test error handling by injecting failure scenarios (service returns 429, 503, 401, custom errors) and verifying that agent applies appropriate recovery for each.

## Frequently Asked Questions

### How do you distinguish between transient and permanent errors?
Per [Error Code Semantic Drift](failures/error-code-semantic-drift.md), transient errors (network timeouts, 503 temporarily unavailable) warrant retry; permanent errors (401 unauthorized, 404 not found, 400 bad request) don't. Create an explicit error taxonomy that maps service-specific codes to error types (transient, permanent, quota, auth, etc.), and use the taxonomy to decide retry strategy. Don't guess based on error message — map explicitly.

### What should an agent do if error format is inconsistent across services?
Per [Error Response Format Inconsistency](failures/error-response-format-inconsistency.md), wrap each service call with a consistent error-handling interface: normalize responses to a common format (e.g., structured error objects with code, message, type fields), and parse only what you need from that normalized format. This isolates agents from service-specific format changes.

### Can error-handling libraries prevent these failures?
Partially — a library can standardize error handling for one service, but won't catch semantic drift when services change or new services are added. Use libraries as a foundation, then layer standardization: map error codes to a common taxonomy, and update the mapping as services change.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Error Code Semantic Drift](failures/error-code-semantic-drift.md) | Same error code means different things in different services or API versions; recovery strategy is inappropriate |
| [Error Response Format Inconsistency](failures/error-response-format-inconsistency.md) | Different services return errors in different formats (JSON vs text, body vs headers); parsing fails for service with different format |

**Total: 2 patterns**

## Related Goals

- [Tool Reliability](../tool-reliability/) — error handling is foundational to tool reliability
- [Recovery Mechanisms](../recovery-mechanisms/) — error handling informs recovery decisions
- [Observability Monitoring](../observability-monitoring/) — errors should be logged and analyzed for patterns
