# AI Agent Trusts Stale RAG/OCR Text Over the Authoritative Database: Causes and Fixes

## Issue: The agent answers from OCR- or RAG-retrieved text when the live database or source document should have won.

**Frequency**: Common

**Symptoms**
- Answer conflicts with the authoritative system of record.
- Agent quotes a value extracted via OCR/RAG that differs from the live database record, and no hierarchy check catches the conflict before the value is used.
- Investigation finds the authoritative source was queryable and available the whole time, but the agent defaulted to the retrieved/extracted text anyway.

This is a common failure in RAG pipelines built with frameworks like LangChain or LlamaIndex, where retrieval is wired as the default lookup and the authoritative database is only a fallback.

**Root Cause**
The retrieval pipeline treats RAG/OCR-extracted text and the live authoritative database as equally valid inputs because no explicit source-of-truth hierarchy is encoded anywhere in the system — and in practice the RAG pipeline is queried first by default, with the database treated as a fallback rather than the primary source. Without a conflict-detection step that compares retrieved text against the authoritative source before answering, and with cached extracted content often outliving the freshness window of the data it represents, the agent has no mechanism to notice it is answering from a stale or lower-precedence source even when the correct one was queryable the whole time.

**Example**
```
A customer asks an agent for their current account balance. The agent's RAG
pipeline retrieves a cached statement PDF showing a balance from three weeks
ago and answers with that figure, even though the live account database
(the actual source of truth) is queryable and shows a materially different
current balance. The customer makes a purchasing decision based on the stale
figure and later disputes a declined transaction.
```

**Contributing Factors**
- No explicit source-of-truth hierarchy encoded — RAG/OCR retrieval and live database queries are treated as equally valid inputs.
- RAG pipeline is queried by default/first, with the authoritative database treated as a fallback rather than the primary source.
- No conflict-detection step comparing retrieved text against the authoritative source before answering.
- Caching of extracted/retrieved content outlives the freshness window of the underlying authoritative data.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Database available, RAG also has an answer | Live database has current balance; cached statement PDF has stale figure | Agent uses database value | Agent uses RAG/OCR value despite database availability |
| Sources conflict | Extracted document value differs from database record | Agent applies hierarchy (database wins), logs conflict | Agent picks whichever source it queried first, no conflict logged |
| Database unavailable | Authoritative database is down | Agent falls back to next-tier source with explicit disclaimer | Agent answers from lower-tier source with no indication of reduced confidence |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| database_first_query_compliance_eval_percent | 100% | % of eval cases where agent queries the authoritative database before falling back to RAG/OCR |
| source_hierarchy_violation_rate_eval_percent | 0% | % of eval cases where the answer is based on a lower-precedence source despite a higher-precedence one being available |

---

Fixing this means encoding an explicit source-of-truth hierarchy so the database wins conflicts instead of whichever source was queried first.

## Mitigation Strategies

### Prevention
1. **Source-of-Truth Hierarchy**: Define explicit authoritative source hierarchy for each data type. Example: [1] Live Database (authoritative), [2] API System-of-Record, [3] Source Document (original), [4] RAG/OCR (extracted text), [5] LLM Knowledge (lowest authority). Query sources in priority order; stop at first available.
2. **Database-First Query Strategy**: Before using RAG/OCR/LLM knowledge, query authoritative database/system. If authoritative source available, use it (don't supplement with RAG). Only use RAG/OCR when database source unavailable.
3. **Source Conflict Resolution**: When sources conflict (e.g., database says $500 but OCR shows $5000), follow hierarchy: database wins. Log conflict for investigation. Alert if conflicts frequent (data integrity issue).

### Detection & Response
1. **Source-of-Truth Violation Detection**: Monitor all decisions. For each decision, verify source matches hierarchy. Example: if decision based on OCR but database available, flag violation. Log all violations.
2. **Source Conflict Tracking**: When multiple sources provide different answers, log conflict: source_A=value_A, source_B=value_B, hierarchy_decision=winner, outcome. Track conflict patterns.
3. **Authoritative Source Availability Audit**: For each data type, measure: % of queries where authoritative source is available. Alert if availability drops (data integrity issue emerging). High availability = should not use RAG.

### Architecture Patterns
1. **Source Precedence Middleware**: Middleware that enforces source hierarchy. Query in priority order: db → api → document → rag → llm. Use first available source. Log which source was used. Fail on hierarchy violation.
2. **Source Verification Layer**: After decision made, verify source matches hierarchy. If conflict detected (decision used low-precedence source when high-precedence available), alert and consider decision reversal.
3. **Conflict Alert System**: When sources conflict, generate alert with conflicting values + hierarchy decision. Route to human expert for resolution. Log resolution for future similar conflicts.

### Metrics
1. **source_hierarchy_violation_rate_percent**: Target: 0%; Alert threshold: > 0.1%; Any violation is incident
2. **database_first_query_compliance_percent**: Target: 100%; Always query database when available
3. **source_conflict_resolution_accuracy_percent**: Target: 100%; Hierarchy decisions correct
4. **rag_usage_when_database_available_percent**: Target: 0%; Should never use RAG if DB available
5. **authoritative_source_availability_percent**: Target: > 95%; High availability expected

### Alerts
1. **Source-of-Truth Hierarchy Violation** (P1 - Critical): Condition - decision based on low-precedence source when high-precedence source available. Action: Immediate decision review, escalate to expert, potential decision reversal, source system investigation.
2. **Source Conflict Detected** (P2 - Warning): Condition - multiple sources provide conflicting answers. Action: Alert expert, log conflict, apply hierarchy resolution, investigate why conflict exists.
3. **Database Unavailability** (P2 - Warning): Condition - authoritative database unavailable for query. Action: Alert to database team, route to manual review if critical query, switch to fallback source with disclaimer.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| source_hierarchy_violation_rate_percent | > 0.1% |
| rag_usage_when_database_available_percent | > 0% |
| authoritative_source_availability_percent | < 95% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Source-of-Truth Hierarchy Violation | Decision based on low-precedence source when high-precedence source was available | Critical |
| Source Conflict Detected | Multiple sources provide conflicting answers | Warning |
| Database Unavailability | Authoritative database unavailable for query | Warning |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
