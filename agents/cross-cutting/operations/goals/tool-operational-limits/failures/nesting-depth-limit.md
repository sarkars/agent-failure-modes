# Nesting Depth Limit

## Issue
Many tools reject JSON or other structured payloads once object/array nesting exceeds a fixed depth — commonly somewhere between 10 and 32 levels — to protect their parsers from stack-exhaustion and pathological-input attacks. Agents that build payloads through recursive composition (e.g., chaining tool outputs into a nested config object, recursively expanding a tree-shaped data structure, or composing several sub-tool results into a wrapper object) can produce structures that grow deeper than intended without any single step looking unusual, because the depth accumulates across composition steps that the agent reasons about independently rather than as a whole.

**Frequency**: Occasional

**Symptoms**
- Payload rejected with a generic parse error or a specific "maximum nesting depth exceeded" message, with no indication of which part of the structure is too deep
- Failures that appear only for certain inputs (e.g., deeply nested org charts, recursive comment threads, deeply nested config merges) and not others
- Agents that recursively compose tool outputs (tool A's output embedded inside tool B's input, embedded inside tool C's input) with no depth tracking across the composition chain
- Payloads that pass local schema validation (which may not enforce depth) but fail at the transport/parser layer of the receiving tool
- Stack-overflow-adjacent errors on the server side surfaced to the agent as an opaque 400 with no depth number, making the failure hard to diagnose from the response alone

## Root Cause
JSON and similar recursive-descent parsers are vulnerable to stack exhaustion on deeply nested input, so tool providers impose a hard depth ceiling independent of overall payload size — a payload can be well under any byte-size limit and still be rejected purely for structural depth. Agents that build nested structures through iterative or recursive composition (wrapping one tool's structured output inside another's input field, or recursively serializing a tree-shaped domain object) do not typically track cumulative nesting depth across composition boundaries, since each individual composition step looks locally reasonable ("just add this object as a field"). The depth limit is therefore violated emergently, from the combination of several individually-unremarkable steps, rather than from any single obviously-oversized operation.

## Example
```
An agent flattens a company's org chart into a nested JSON structure for
a headcount-planning tool, where each manager node contains a `reports`
array of subordinate nodes recursively. For a 14-level-deep management
hierarchy, the resulting payload nests 14 levels of `{"reports": [...]}`
plus 3 wrapper levels the agent's serialization code adds (a request
envelope, a "org" field, and a "snapshot" field), totaling 17 levels.
The target API enforces a max JSON nesting depth of 16. The call fails
with `400 Bad Request: {"error": "max_depth_exceeded"}` and no further
detail. The agent's error handling, built for field-validation errors
with a `field` name in the response, cannot map this error to any
specific field and reports "unknown validation failure" to the user,
who has to manually inspect the payload to discover the 3 wrapper
levels are what pushed a valid 14-level org chart over the limit.
```

## Statistics
| Finding | Context |
|---------|---------|
| JSON parsers commonly enforce nesting depth limits between 10 and 32 levels as a stack-exhaustion defense | Common default in JSON parsing libraries and API gateways |
| Nesting-depth violations are typically independent of payload byte size, so byte-size validation alone will not catch them | Structural distinction from payload-size limits |
| Recursive/tree-shaped domain data (org charts, comment threads, category hierarchies, nested BOMs) is the most common source of emergent depth violations in agent-constructed payloads | Based on typical recursive-composition patterns in agent tool chains |

## Mitigations
1. **Track nesting depth during payload construction, not just size**: When recursively building a structure, maintain a running depth counter and flag or restructure before the tool's known limit is reached.
2. **Account for wrapper/envelope depth added by serialization code**: Include any fixed wrapping levels (request envelopes, metadata fields) in the depth budget, since these silently consume headroom that would otherwise be available for the recursive domain data.
3. **Flatten deeply recursive structures where the tool supports it**: Convert tree-shaped data into a flat list with parent-reference IDs (adjacency-list form) instead of nested objects, when the target tool or a suitable alternative representation supports it.
4. **Validate depth client-side before submission**: Walk the constructed payload and compute its maximum depth against the tool's documented limit before sending, converting a possible opaque server rejection into an actionable pre-flight check.
5. **Chunk deep hierarchies into multiple shallower calls**: For inherently deep domain structures, submit sub-trees separately (e.g., one call per top-level branch) rather than one call encompassing the full depth.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `payload.max_nesting_depth_constructed` | Deepest level reached in an agent-constructed payload for a given tool | Alert when within 2 levels of the tool's documented max |
| `payload.depth_rejection_count` | Count of payloads rejected specifically for exceeding max nesting depth | Alert if > 0 |
| `payload.wrapper_depth_overhead` | Number of fixed envelope/wrapper levels added by serialization code, tracked separately from domain-data depth | Track to inform depth budgeting |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Nesting depth limit exceeded | Payload rejected with a max-depth or generic parse error correlated with deep structure | Medium | Flatten or chunk the payload, add pre-submission depth check |
| Opaque depth failure with no field attribution | Rejection with no field-level detail, following construction of a recursively nested payload | Low | Route to manual inspection, add client-side depth validation to prevent recurrence |

## Related Patterns
- [Join Depth Limit](./join-depth-limit.md) - the same depth-limiting principle applied to query relation traversal rather than payload structure
- [Request Payload Size Limit](./request-payload-size-limit.md) - a size-based sibling limit that a deeply nested but small payload can pass while still failing on depth
- [Query Complexity Limit](./query-complexity-limit.md) - another structural-cost limit, scored rather than depth-counted, that can reject a payload for similar underlying reasons
