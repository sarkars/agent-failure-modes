# State Serialization Failure

## Issue
State that an agent needs to persist or transmit across a process, network, or storage boundary fails to serialize or deserialize correctly — the write produces a truncated or malformed payload, or the read cannot fully reconstruct the original object graph. Unlike an encoding mismatch (where values decode to the wrong thing) or a version mismatch (where an old/new schema disagrees), this is a failure of the serialization mechanism itself: an unsupported type, a circular reference, a size limit, or a partial write leaves the stored representation broken rather than merely inaccurate.

**Frequency**: Occasional

**Symptoms**
- Deserialization throws an exception (unexpected end of input, invalid format) on state that was "successfully" written moments earlier
- Object graphs come back with fields silently set to null or default values where the original had populated data (types the serializer couldn't handle)
- Large state objects are truncated at a consistent byte/size boundary, matching a buffer or message-size limit
- Serialization succeeds in testing with small/simple objects but fails intermittently in production with larger or more deeply nested real data
- Circular or self-referencing state structures cause infinite recursion or stack overflow during serialization

## Root Cause
Serialization is a lossy translation between an in-memory object model and a wire/storage format, and that translation has edges the in-memory model doesn't respect: not every language-native type has a canonical representation in the target format (dates, enums, custom classes, NaN/Infinity floats), not every format has an unbounded size, and not every write is atomic (a crash or timeout mid-write leaves a partial, unparseable payload on disk or in the queue). Agent systems are especially exposed because the state being serialized is often produced dynamically by an LLM or composed from multiple tool outputs, so it's less likely to have been designed up front against the serializer's constraints, and edge cases (a tool returning a deeply nested or self-referential structure) surface only when they actually occur rather than being caught by a fixed schema at design time.

## Example
```
A multi-agent planning system serializes its full task-dependency graph
to JSON after each planning step, so the graph can be persisted and
resumed if the process restarts.

Step 12: the planner's tool-output parser builds a dependency graph
where, due to a bug in cycle detection, task "deploy" ends up with
a dependency edge pointing back to task "provision", which itself
depends on "deploy" - a circular reference in the in-memory object
graph.

The serializer (a standard JSON encoder that doesn't detect cycles)
recurses into "deploy" -> "provision" -> "deploy" -> "provision"
indefinitely, exhausts the call stack, and the serialization call
raises a stack-overflow error mid-write.

The partial write has already flushed 40KB of a planned 45KB payload
to the state file before the crash, leaving a syntactically invalid,
truncated JSON file. When the process restarts and attempts to resume
from this checkpoint, deserialization fails immediately with "Unexpected
end of JSON input", and the entire planning session's progress -
11 completed steps - is unrecoverable.
```

## Statistics
| Finding | Context |
|---------|---------|
| 5-10% of serialization failures in agent state pipelines stem from circular or self-referential object graphs rather than type or size issues | Typical range observed in production agent telemetry |
| Non-atomic writes (no write-to-temp-then-rename pattern) account for an estimated 30-50% of "unparseable state on restart" incidents | Estimated from postmortems involving crash-during-write scenarios |
| Adding cycle detection and pre-serialization validation reduces stack-overflow/malformed-payload incidents by roughly 90% | Reported range across teams that added guard checks before the serialization call |

## Mitigations
1. **Atomic write pattern**: Write serialized state to a temporary file/key and atomically rename/swap it into place only after the full write succeeds, so a crash mid-write never leaves a corrupt, partially-written record as the "current" state.
2. **Cycle detection before serialization**: Validate the object graph for circular references before attempting to serialize, and fail fast with a clear error rather than recursing until a stack overflow produces a truncated payload.
3. **Schema-constrained state types**: Restrict what can go into persisted agent state to a known, serializer-safe set of types (no raw language-native objects, no unbounded nesting), enforced at the point state is constructed, not just at serialization time.
4. **Chunked/streaming serialization for large state**: For state that can grow large (long conversation histories, big dependency graphs), use a streaming or chunked serialization approach with explicit size limits and graceful truncation/summarization instead of a single all-or-nothing write that can hit a hard size ceiling.
5. **Round-trip validation on write**: Immediately deserialize what was just serialized as part of the write operation itself, and treat a failed round-trip as a failed write, catching corruption before it's treated as durably persisted.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| serialization_error_rate | Rate of exceptions or failures during state serialization/deserialization | Alert if > 0.5% |
| truncated_payload_count | Count of stored state payloads that fail parsing due to unexpected end-of-input | Alert if > 0 |
| round_trip_validation_failure_rate | Fraction of writes where immediate deserialize-after-serialize doesn't match the original object | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unrecoverable checkpoint on restart | A process fails to deserialize its most recent state checkpoint after a restart | High | Page on-call, fall back to the last known-good checkpoint, investigate the write that produced the corrupt payload |
| Serialization stack overflow | A serialization call fails due to excessive recursion depth | Medium | Investigate the object graph for circular references, add cycle-detection guard at the identified construction point |

## Related Patterns
- [State Encoding Mismatch](./state-encoding-mismatch.md) - a related but distinct boundary failure where the serialized data is well-formed but decoded with the wrong assumptions
- [State Version Incompatibility](./state-version-incompatibility.md) - describes a serialization boundary failure driven by schema evolution rather than mechanism limits
- [State Garbage Collection Failure](./state-garbage-collection-failure.md) - a schema/serialization change can be the exact trigger that silently breaks a downstream collector's deserializer
