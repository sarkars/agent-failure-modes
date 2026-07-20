# Memory Corruption Detection Failure

## Issue
Individual entries in a persistent memory store can become corrupted — truncated writes from a crashed process, malformed JSON from a partial serialization, encoding mangling, or a bad migration that silently drops or garbles fields — and the retrieval path has no validation step that would catch this before the corrupted entry is handed to the agent. Instead of failing loudly, the agent receives a mangled fact, a broken embedding, or a record with fields swapped and treats it as valid input, often producing a confidently wrong answer that is harder to diagnose than an outright retrieval failure would have been.

**Frequency**: Occasional

**Symptoms**
- Agent produces oddly specific but wrong statements traceable to a garbled memory field (swapped values, truncated strings, mismatched encoding)
- Retrieval succeeds (no error) but the returned record fails basic schema/shape expectations on inspection
- A memory record's embedding vector and its text content are mismatched after an interrupted write
- Downstream parsing of a memory entry throws only when a specific field is accessed, not at retrieval time
- Corruption is discovered only when a human manually inspects a specific record after a bad outcome, not through automated detection

## Root Cause
Memory writes are not always atomic, especially across distributed or multi-step storage backends (write the text record, then write the embedding, then update the index) — a crash, timeout, or partial failure between these steps can leave a record in an inconsistent state that no single write ever "failed" but the overall result is corrupt. Storage layers also rarely run integrity checks (checksums, schema validation, encoding validation) on read, because doing so on every retrieval is a performance cost most systems don't budget for. The retrieval path is optimized for the happy path — deserialize and return — so a corrupted record deserializes into a technically-valid-but-wrong object (wrong types coerced, missing fields defaulted, truncated strings) rather than raising an error the agent or a monitor could catch.

## Example
```
Memory record for user preference, written via a two-phase process:
  1. Write structured fact to primary store
  2. Write corresponding embedding to vector index

A network timeout occurs between step 1 and step 2. Step 1 completes:
  { "user_id": "u_4471", "fact": "prefers email over SMS for alerts",
    "updated_at": "2026-07-15T10:02:00Z" }

Step 2 never completes for this write, but a stale embedding from
a previous, different fact ("prefers SMS for urgent alerts") remains
indexed under the same record ID from an earlier version.

Later retrieval by semantic search for "how should we contact this
user" returns the record ID, whose *text* now says "prefers email"
but whose *embedding* was generated from "prefers SMS" — so the
record surfaces for SMS-related queries it no longer actually
matches, and the agent, reading only the text field, tells a
downstream system to use email for an urgent-alert workflow that
was querying for SMS preference, producing a plausible-sounding
but wrong routing decision with no error anywhere in the pipeline.
```

## Statistics
| Finding | Context |
|---------|---------|
| Multi-step memory writes (text + embedding + index update) that lack atomic commit typically show a small but nonzero partial-failure rate under normal network conditions | Typical range for distributed multi-store writes without transactions |
| Systems without read-time schema/checksum validation detect corrupted records almost exclusively through downstream symptom reports, not proactively | Reported pattern across teams without integrity checks |
| Adding lightweight checksum or schema validation on read catches a meaningful share of otherwise-silent corrupted records before they reach the agent | Estimated from teams that added post-hoc validation passes |

## Mitigations
1. **Atomic multi-step writes**: Use a transactional or two-phase-commit pattern (or a single write with an explicit "pending" state until all steps confirm) so a partial failure never leaves a record half-updated.
2. **Checksum/schema validation on read**: Validate each retrieved record's shape and, where feasible, a content checksum before handing it to the agent; reject or quarantine records that fail validation instead of passing them through.
3. **Embedding-text consistency checks**: Periodically re-embed a sample of stored text and compare against the indexed vector to detect drift between a record's text and its embedding caused by partial writes.
4. **Quarantine and repair pipeline**: Route detected corrupt records to a quarantine queue for reprocessing or deletion rather than silently serving them, and alert on quarantine volume.
5. **Write-ahead logging with replay**: Log intended writes before applying them so an interrupted multi-step write can be detected and replayed/rolled back on the next maintenance pass instead of persisting in a corrupted state.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| corrupt_record_detection_rate | Fraction of retrieved records failing schema/checksum validation | Alert if > 0.5% |
| embedding_text_mismatch_rate | Fraction of sampled records whose re-embedded text diverges significantly from the stored vector | Alert if > 1% |
| quarantined_record_count | Number of records flagged and held for repair | Alert if growth rate increases week over week |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Corrupted record served to agent | A record failing validation was retrieved and used before quarantine caught it | High | Quarantine record, audit downstream actions taken using it |
| Partial write detected | A multi-step write pipeline reports one step succeeded and a dependent step failed/timed out | High | Roll back or complete the write, log for corruption audit |

## Related Patterns
- [Memory Interleaving Corruption](./memory-interleaving-corruption.md) - a different corruption mechanism (concurrent writes racing) producing similarly undetected bad records
- [Retrieval Index Corruption](./retrieval-index-corruption.md) - corruption at the index/structural level rather than within individual records, degrading all lookups rather than one
- [Memory Not Updated Stale Retrieval](./memory-not-updated-stale-retrieval.md) - both stem from multi-step or multi-store writes that aren't atomic, though this produces corruption rather than staleness
