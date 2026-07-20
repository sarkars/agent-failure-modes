# Input Recursion Limit

## Issue
An agent's parser (JSON, XML, YAML, or a custom nested-structure format) receives an input with excessive nesting depth — either from a legitimately complex source, a buggy upstream serializer that loops, or a deliberately crafted payload — and the recursive-descent parsing logic exceeds the language runtime's call-stack limit or the parser's own recursion guard, crashing the process rather than rejecting the input gracefully. Because the crash happens inside the parsing library itself, it often takes down the whole request-handling worker rather than failing just the one bad input.

**Frequency**: Occasional

**Symptoms**
- Worker process crashes with a stack-overflow or `RecursionError` traceback pointing into a JSON/XML/YAML parsing library
- A single malformed or deeply-nested input takes down an entire request-handling process, affecting concurrent unrelated requests
- Crash is intermittent and hard to reproduce because it depends on the specific input's nesting depth and the runtime's current stack usage
- No graceful error response reaches the caller — the connection simply drops or times out
- Retrying the same request deterministically reproduces the crash, unlike most transient failures

## Root Cause
Most general-purpose parsers for nested formats (JSON, XML, YAML) are implemented as recursive-descent parsers for simplicity, where each level of nesting in the input corresponds to one additional stack frame in the parser. Language runtimes impose a maximum call-stack depth (a few thousand frames is typical), and unless the parser explicitly tracks and caps nesting depth as a first check, the recursive calls will exceed that runtime limit before any input-validation logic gets a chance to reject the input as "too deeply nested." The failure is a raw runtime exception (stack overflow, `RecursionError`, or in unmanaged runtimes, a hard crash) rather than a caught, application-level validation error, which is why it typically bypasses normal error-handling paths.

## Example
```
An agent ingests JSON configuration payloads submitted via an API and
parses them with a standard recursive-descent JSON library configured
with no explicit depth limit.

A misbehaving upstream client has a serialization bug that, under a rare
condition, wraps a config value in a self-referential-looking nested
array structure 50,000 levels deep (a legitimate structure was meant to
be 3 levels deep, but a loop counter bug caused re-wrapping on every
retry attempt for six hours before anyone noticed).

The agent's parser begins recursing into the structure. At roughly frame
3,000-8,000 (depending on the runtime and current stack usage), the
process hits its stack limit and crashes with a stack overflow. Because
this happens inside a shared worker process handling multiple concurrent
requests, all in-flight requests on that worker are dropped, not just the
one with the bad payload. The process restarts, the same payload is
retried by the client's retry logic, and the worker crashes again in a
loop until the payload is manually purged from the retry queue.
```

## Statistics
| Finding | Context |
|---------|---------|
| Recursive-descent parsers without an explicit depth cap typically fail somewhere between 1,000 and 10,000 levels of nesting, depending on runtime and stack size | General characteristic of common parsing libraries and default stack sizes |
| A small but recurring share of parser-related production crashes in agent input pipelines trace to unbounded nesting rather than malformed syntax | Typical range observed in crash-report triage |
| Adding an explicit max-depth check before or during parsing eliminates this crash class with negligible performance cost | Estimated from the low cost of a depth counter relative to parse time |

## Mitigations
1. **Explicit depth limits**: Configure or wrap the parser with an explicit maximum nesting depth (e.g. 32 or 64 levels, well within realistic legitimate use) and reject anything deeper with a normal validation error before recursion approaches the runtime's stack limit.
2. **Iterative parsing for untrusted input**: For input sources that are untrusted or externally controlled, prefer an iterative (explicit-stack) parser implementation over a recursive-descent one, so depth is bounded by available heap memory and an application-level check rather than the call stack.
3. **Process isolation for parsing untrusted payloads**: Parse untrusted or externally-sourced structured input in an isolated worker/sandbox so a stack-overflow crash doesn't take down concurrent unrelated requests on the same process.
4. **Pre-parse size and structural sanity checks**: Reject payloads exceeding a reasonable raw size or bracket/tag-depth count via a cheap pre-scan before handing them to the full parser.
5. **Upstream serializer bug monitoring**: Track nesting-depth distribution of legitimate payloads from each source over time, and alert when a source's typical depth suddenly spikes, indicating a serialization bug rather than a change in legitimate data shape.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| parser_crash_rate | Rate of worker crashes originating inside structured-input parsing code | Alert if > 0 sustained |
| input_nesting_depth_p99 | 99th percentile nesting depth of accepted structured inputs | Alert if p99 approaches the configured max-depth limit |
| depth_limit_rejection_count | Count of inputs rejected for exceeding the configured max nesting depth | Alert on sudden spike (possible attack or upstream bug) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Worker crash in parser | A request-handling process crashes with a stack-overflow/RecursionError inside a parsing library | High | Isolate and quarantine the triggering payload, verify depth limits are configured, restart affected workers |
| Nesting depth spike from a known source | A specific upstream source's payload nesting depth deviates sharply from its historical baseline | Medium | Contact source owner, inspect for a serialization bug |

## Related Patterns
- [Input Size Not Validated](./input-size-not-validated.md) - both are failures to bound an input's cost (depth vs. raw size) before the parser fully commits to processing it
- [Input Schema Evolution](./input-schema-evolution.md) - an upstream serialization bug causing runaway nesting is a specific case of unexpected structural drift
- [Output Truncation Silent](./output-truncation-silent.md) - a related failure where an oversized structure causes silent data loss rather than a crash
