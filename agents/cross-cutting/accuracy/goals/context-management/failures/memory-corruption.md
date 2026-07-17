# Memory Corruption

## Issue: Agent's Long-Term Memory Becomes Corrupted

**Frequency**: Occasional

**Symptoms**
- Agent recalls facts that were never true
- Stored information differs from original
- Memory entries contradict each other
- Outdated information not updated

**Root Cause**
When agents store information to long-term memory:
- Summarization may lose or distort facts
- Overlapping updates may conflict
- No validation of stored content
- Memory poisoning through malicious inputs

**Example**
```
Original fact: "User's budget is $10,000"
Stored (summarized): "User budget is flexible, around $10K"
Later retrieved: "User has approximately $10,000 budget but flexible"
Used as: "User can go higher than $10,000"

Result: Agent makes recommendations exceeding actual budget
```

---

## Test Scenario & Reproduction

### Scenario Setup
- A user states a precise, numerically critical fact in conversation (e.g., "User's budget is $10,000")
- The long-term memory pipeline passes this fact through a summarization step rather than storing it verbatim
- No validation-against-source check runs before the summarized memory entry is committed or later reused

### Trigger Mechanism
1. State the exact critical fact in the source conversation
2. Allow the memory pipeline to summarize and store it
3. Retrieve the stored memory entry in a later turn/session and inspect its wording against the original
4. Have the agent use the retrieved memory entry to drive a recommendation and check whether it violates the original constraint

**Example Reproduction Steps:**
```
1. Source turn: "User's budget is $10,000"
2. Trigger the memory-write pipeline and capture the stored entry (expect something like "User budget is flexible, around $10K")
3. In a later session/turn, retrieve the memory entry (expect further drift, e.g., "User has approximately $10,000 budget but flexible")
4. Ask the agent to recommend a product/plan based on the retrieved memory
5. Record the agent's recommendation and check whether it exceeds $10,000
6. Diff the final retrieved value against the original verbatim source statement
```

### Expected Failure State
- The stored memory entry no longer matches the original number/qualifier ("$10,000" becomes "flexible, around $10K")
- A subsequent retrieval further drifts the meaning (e.g., interpreted as "can go higher than $10,000")
- The agent's recommendation exceeds the user's actual stated budget, directly contradicting the original fact
- A correctly-behaving system would store and retrieve the exact "$10,000" figure unchanged, or explicitly flag that the value was derived from a summarization step

---

## Mitigation Strategies

### Prevention
1. **Verbatim storage for critical facts, summarization only for context**: Store numerically or legally critical facts (budgets, quantities, dates, commitments) verbatim rather than passing them through a summarization step, reserving summarization for softer contextual color, since the demonstrated failure mode is exactly a summarization step turning "$10,000" into "flexible, around $10K" and later into "can go higher than $10,000." Trade-off: requires explicitly classifying which facts are summarization-exempt, and over-broad verbatim storage increases storage volume and can reintroduce context-overflow pressure if not bounded.
2. **Validation against source before write**: Before committing a new or updated memory entry, validate it against the original source statement (exact string match or a strict extraction check for critical fields) rather than accepting a freeform summarized restatement as ground truth, closing the "no validation of stored content" gap identified as a root cause. Trade-off: adds a verification step to every memory write, and strict validation can reject legitimate paraphrased updates that are actually accurate, requiring careful tuning of what counts as a validation failure.
3. **Write-access restriction with conflict-aware merge**: Restrict which processes/turns can write to long-term memory, and when two updates would overlap on the same fact, require an explicit merge/reconciliation step (not last-write-wins) that flags the conflict rather than silently overwriting, since the root cause explicitly cites "overlapping updates may conflict" as a corruption path. Trade-off: conflict-aware merging is more complex to implement than last-write-wins and can stall a workflow awaiting reconciliation on facts that need to be resolved quickly.

### Detection & Response
1. **Memory-vs-source audit**: Periodically sample stored memory entries and diff them against the original source turn/document they were derived from, flagging any entry where the current value doesn't match the source, directly catching drift like "$10,000" becoming "around $10K" before it's used in a decision.
2. **Contradiction detection across memory entries**: Scan the memory store for entries that address the same fact but disagree (e.g., two different stated budgets for the same user), and flag for reconciliation before either is used, since the root cause explicitly notes "memory entries contradict each other" as a symptom.
3. **Pre-use critical-fact validation**: Before using a high-stakes memory entry (e.g., budget) to drive a recommendation or action, re-validate it against its source attribution rather than trusting the stored summary at face value, adding a checkpoint at the point of highest consequence rather than relying solely on periodic audits.

### Architecture Patterns
1. **Source-attributed, versioned memory store**: Architect memory storage so every entry links back to its originating source (turn ID, document, timestamp) and every update creates a new version rather than overwriting in place, so any entry's provenance and full edit history can be inspected when a discrepancy is found — directly addressing both "source attribution" and "versioned memory" as structural requirements.
2. **Separate exact-fact store from narrative-summary store**: Architect two distinct memory tiers — an exact-value store for critical structured facts (budgets, dates, commitments) that is never summarized, and a separate narrative-summary store for softer context — so summarization's inherent lossiness can never touch the tier used for high-stakes decisions.
3. **Memory write pipeline with schema validation and access control**: Architect memory writes to pass through a validation/access-control layer that enforces schema correctness (e.g., budget must be a number sourced from an explicit user statement) and restricts which agent processes may write which fact categories, structurally narrowing the "memory poisoning through malicious inputs" vector cited as a root cause.

### Metrics
1. **memory_source_mismatch_rate**: Target: 0% of audited entries diverge from their source; Alert on any divergence found for a critical-fact category
2. **memory_contradiction_rate**: Target: 0 unresolved contradictory entries for the same fact; Alert on any detected contradiction
3. **critical_fact_summarization_incidence**: Target: 0 critical facts (budget, dates, commitments) stored only in summarized form; Alert on any critical fact lacking a verbatim entry
4. **pre_use_validation_failure_rate**: Target: track as baseline; Alert on any failure for a high-stakes decision path

### Alerts
1. **Critical Fact Diverges From Source** (P1): Condition - memory-vs-source audit finds a stored critical fact (budget, quantity, commitment) that doesn't match its original source statement. Action: Correct the entry from source immediately, flag and review any decisions already made using the corrupted value, investigate which write path bypassed verbatim storage.
2. **Contradictory Memory Entries for Same Fact** (P1): Condition - two memory entries addressing the same fact disagree. Action: Freeze use of both entries pending reconciliation, re-derive the correct value from source, log the conflicting write events for root-cause analysis.
3. **Unauthorized or Unvalidated Memory Write** (P2): Condition - a memory write occurs that bypasses schema validation or originates from an unauthorized process. Action: Reject the write, quarantine the entry for review, audit the write path for a potential memory-poisoning attempt.

---

## References

- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Memory poisoning
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Memory corruption patterns
