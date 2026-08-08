# Memory Conflict

## Issue: Two memories contradict; agent fails to resolve.

**Frequency**: Occasional

**Symptoms**
- Conflicting preferences used interchangeably.
- Agent alternates between two contradictory values for the same field across consecutive turns without any intervening update.
- No superseded_by link exists between the two conflicting records, so both remain "live" in the store simultaneously.
- Agent picks a value arbitrarily (e.g., whichever was retrieved first) instead of applying recency or source-authority ranking.
- User has to repeatedly re-clarify the same fact because the conflict was never surfaced or resolved.

**Root Cause**
Preference fields are modeled as an append-only list of facts rather than single-valued, versioned fields, so a new value never actually supersedes an old one — both simply coexist as equally "live" records. No write-time contradiction check runs before a new record is committed, and because records carry no timestamp or source-authority tier, retrieval has no deterministic basis for preferring one conflicting value over the other, arbitrarily returning whichever it happens to fetch first. Inferred or third-party-imported facts are stored with the same trust weight as an explicit user statement, and with no scheduled scan job hunting for contradictory pairs, conflicts sit unresolved until a user notices the agent contradicting itself.

**Example**
```
User (Session 1): "My shipping address is 12 Oak St."
[Stored: subject=user, predicate=shipping_address, object="12 Oak St"]

User (Session 2, inferred from a delivery form the agent processed): shipping_address
inferred as "45 Pine Ave" from a third-party import, stored without conflict check.

Session 3:
Agent: "I'll ship to 12 Oak St." (uses old record)
...later in the same session...
Agent: "Confirming delivery to 45 Pine Ave." (uses the conflicting inferred record)
User: "Which address do you actually have on file? You gave me two different ones."
```

**Contributing Factors**
- No write-time contradiction check runs before a new memory record is committed, so conflicting values for the same subject/predicate coexist unresolved.
- Preference fields are modeled as an append-only list of facts rather than single-valued, versioned fields, allowing two live values to exist for one slot.
- Memory records lack timestamps or source-authority tiers, so retrieval has no deterministic way to prefer one conflicting value over another.
- Inferred or third-party-imported facts are stored with the same trust weight as explicit user statements, making low-confidence guesses just as likely to be surfaced as confirmed facts.
- No scheduled contradiction-scan job exists to catch conflicting pairs before they reach generation.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Write-time contradiction detection | A new memory write conflicts with an existing record for the same subject/predicate | Write is routed to resolution (supersession link or review flag) instead of silently accepted | Both conflicting records exist unresolved after the write |
| Recency/authority ranking test | Two conflicting records with different timestamps and source-authority tiers (explicit statement vs. inferred) | Retrieval deterministically returns the higher-authority, more-recent record | A lower-authority or older record is returned, or the response blends both |
| Interchangeable-use regression test | Same preference slot queried across consecutive turns with a known unresolved conflict | Agent asks a clarifying question or uses the resolved value consistently | Agent returns different values for the same slot across turns without an intervening update |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| conflict_detection_recall | > 95% | Seed a test store with known conflicting pairs and measure the fraction the write-time/scan job correctly flags |
| resolution_consistency_rate | 100% | Query a conflicted slot repeatedly in a test harness and verify the same resolved value is returned every time |
| auto_resolution_correctness_rate | > 90% | For conflicts with clear recency/authority signals, verify the auto-resolver picks the correct winner against a labeled test set |

---

## Mitigation Strategies

### Prevention
1. **Write-Time Conflict Detection**: Before committing a new memory record, run a contradiction check against existing records for the same subject/predicate (e.g., dietary_preference, shipping_address). If a conflict is detected, the write is not silently accepted — it is routed into a resolution step that either supersedes the old record with an explicit link or flags both for review.
2. **Recency and Source-Authority Ranking**: Every memory record carries a timestamp and a source-authority tier (explicit user statement > inferred from behavior > third-party import). When two records conflict at read time and no explicit resolution exists, the retrieval layer deterministically prefers the higher-authority, more-recent record rather than picking arbitrarily or blending both.
3. **Single-Writer Field Semantics**: Model mutable preference fields (e.g., "preferred contact method") as single-valued with versioning, not as an append-only list of facts. A new value supersedes rather than coexists with the old one, eliminating the possibility of two live, contradictory values for the same field.

### Detection & Response
1. **Contradiction Scan Job**: Run a scheduled batch job over the memory store that pairs records sharing the same subject/predicate and flags pairs whose values conflict and lack a superseded_by link. Surface these as an unresolved-conflict queue.
2. **Interchangeable-Use Monitoring**: Instrument response generation to log which memory_id was used to satisfy a given preference lookup. If the same preference slot resolves to different memory_ids across consecutive turns for the same user without an intervening update, flag as active conflict leakage.
3. **User-Facing Resolution Prompt**: When the agent detects it is about to use a conflicted field, it asks the user a targeted clarifying question ("You mentioned both X and Y for this — which is current?") instead of guessing, and the answer is written back as the authoritative record.

### Architecture Patterns
1. **Versioned Memory Records with Supersession Links**: Store memory as an append-only log where each new value for a field points to the record it supersedes; the "current" view is computed as the latest non-superseded record per subject/predicate, giving conflict detection a clean diff surface.
2. **Conflict Resolution Service**: A dedicated service intercepts writes, checks for existing conflicting records, and either auto-resolves (using recency/authority rules) or opens a resolution ticket consumed by a clarification-prompt flow before the conflicting fact is ever surfaced to generation.
3. **Read-Time Merge Guard**: The retrieval layer that assembles memory context for the prompt refuses to inject two contradictory values for the same slot; it either picks the resolved winner or omits the field entirely rather than passing both into the model's context.

### Metrics
1. **unresolved_conflict_count**: Target: 0 open > 24h; Alert threshold: > 10 unresolved conflicts open > 24h
2. **conflict_auto_resolution_rate_percent**: Target: > 90%; Alert threshold: < 70% (too many require manual resolution)
3. **conflicted_field_leakage_rate_percent**: Target: 0% (conflicted values reaching generation); Alert threshold: > 0.5% of responses
4. **mean_time_to_conflict_resolution_hours**: Target: < 4h; Alert threshold: > 24h

### Alerts
1. **Conflicted Value Reached Generation** (P1 - Critical): Condition - a response was generated using a memory field flagged as actively conflicted. Action: Suppress the response's personalization for that field, trigger immediate clarification prompt, audit for downstream action taken on the wrong value.
2. **Conflict Queue Backlog** (P2 - Warning): Condition - unresolved_conflict_count exceeds 10 open items older than 24h. Action: Escalate to memory-ops on-call, review auto-resolution rule coverage for gaps.
3. **Authority Ranking Failure** (P2 - Warning): Condition - retrieval selected a lower-authority/older record despite a higher-authority conflicting record existing. Action: Investigate ranking logic bug, patch retrieval query, re-audit affected user sessions.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| unresolved_conflict_count | > 10 unresolved conflicts open > 24h |
| conflict_auto_resolution_rate_percent | < 70% |
| conflicted_field_leakage_rate_percent | > 0.5% of responses |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Conflicted Value Reached Generation | A response was generated using a memory field flagged as actively conflicted | Critical |
| Conflict Queue Backlog | unresolved_conflict_count exceeds 10 open items older than 24h | Warning |

---

## References

- [MS-Agentic-Failure-Taxonomy](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)
- Note: Agentic AI failure modes; safety/security; memory poisoning; tool use; multi-agent risks.
