# Multi-Party Obligation Tracking Failure

## Issue: Complex Contracts with Multiple Parties Have Obligations Model Fails to Track; Confuses Who Owes What

**Frequency**: Common

**Symptoms**
- Contract has 3+ parties; model misattributes obligations
- "Company A pays" vs. "Company B pays" — model gets confused
- Dependency chains not tracked (Party A pays only if Party B delivers)
- Obligations lost or misunderstood at execution

**Root Cause**
Multi-party contracts have complex graphs of obligations. Models trained on simpler 2-party contracts don't generalize well. Pronouns and references ("the said party", "such obligations") are ambiguous. Conditional obligations ("if X happens, then Y pays") require reasoning models don't do well.

**Example**
```
Scenario: Three-party service agreement
Parties: Customer, Vendor, Subcontractor
Obligations:
- Customer pays Vendor $100k
- Vendor pays Subcontractor $60k (if Subcontractor delivers by date X)
- If Subcontractor misses date, Vendor pays penalty to Customer

Model summary: "Vendor pays Customer $100k" (WRONG)
Correct: Vendor receives $100k; pays $60k; pays penalty if late

Impact: Budget miscalculation; cash flow crisis
```

**Key Statistics**
- Accuracy on 2-party contracts: 90%+
- Accuracy on 3-party contracts: 60-75%
- Accuracy on 4+ party contracts: <50%

---

## Mitigation Strategies

### Prevention

1. **Explicit entity tagging with multi-party relationship mapping**: Upon contract ingestion, identify all parties via contract header/signature block. Tag each party with entity ID and canonical name. For each clause, extract all mentions and resolve pronouns to canonical entity names (e.g., replace "the said party" with "Company A"). Build explicit party relationship graph: (Party A, Party B, relationship_type: primary_obligor, counter_party, subcontractor, guarantor). Validate: every obligation statement must explicitly name the obligor and obligee. Fail-safe: if entity resolution uncertain (pronoun ambiguous), flag as "[ENTITY RESOLUTION REQUIRED - ATTORNEY REVIEW]". Root cause mitigation: Prevents pronoun confusion by forcing explicit entity naming throughout.

2. **Obligation graph construction with conditional dependency tracking**: For each obligation identified, construct tuple: (obligor: Party X, obligee: Party Y, obligation: do Z, timing: by date T, condition: if event C, dependencies: [list of prerequisite obligations]). Build directed acyclic graph (DAG) of obligation dependencies: if Obligation A depends on Obligation B, mark edge A→B. For each obligation, trace its prerequisites: "Party C must pay only if Party A delivers by date T." Visualize obligation graph for attorney review. Root cause: Makes obligation dependencies explicit rather than implicit in paragraph text.

3. **Conditional obligation extraction with scenario mapping**: Extract all conditional obligations (if/then patterns). For each conditional, map both scenarios: (a) condition satisfied: what happens? (b) condition not satisfied: what happens? Generate scenario worksheets: "Scenario 1: Party B delivers on time → Party A pays $100k. Scenario 2: Party B misses deadline → Party A withholds payment + Party B pays penalty $10k." Both parties must sign off on scenario interpretation before execution. Root cause: Surfaces conditional dependencies explicitly rather than leaving them implicit.

### Detection & Response

1. **Multi-party obligation audit logging with dependency verification**: For every contract, log: (a) all parties identified with entity tags, (b) obligation graph with dependencies mapped, (c) conditional obligations and scenario mappings, (d) attorney verification status. Run automated verification: for contracts with 3+ parties, sample review of obligation graph accuracy vs. attorney's independent mapping. Measure: entity_resolution_accuracy, obligation_tracking_accuracy_by_party_count, conditional_parsing_accuracy.

2. **Retroactive obligation re-analysis on multi-party dispute**: When dispute arises involving multiple parties, trace to original obligation analysis. Did the model misattribute obligations? Did conditional scenarios play out differently than contracted? Update obligation graph patterns for future contracts. Track obligation misattributions by party count and complexity.

### Architecture Patterns

1. **Entity Resolution Engine**: (1) Extract all parties from contract header, (2) Tag with entity ID, (3) Resolve all pronouns to entity IDs, (4) Validate explicit obligor/obligee naming in all obligation clauses, (5) Build party relationship graph.

2. **Obligation Dependency Graph Builder**: (1) Extract all obligation statements, (2) Identify obligor/obligee/obligation/timing for each, (3) Identify prerequisites and dependencies, (4) Construct DAG of obligations, (5) Detect circular dependencies or missing prerequisites, (6) Visualize for human review.

3. **Conditional Scenario Mapper**: (1) Identify if/then patterns in obligations, (2) Map both outcome scenarios, (3) Cross-check contract language for specified remedies in each scenario, (4) Flag unhandled scenarios for negotiation, (5) Generate scenario worksheet for party alignment.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|-------------------|
| Entity Resolution Accuracy | 100% | <98% | # of parties correctly identified and tagged / total parties in contract (validated by attorney) |
| Obligation Tracking Accuracy (2-Party) | >95% | <90% | # of 2-party obligations correctly attributed to obligor / total obligations in 2-party contracts |
| Obligation Tracking Accuracy (3-Party) | >90% | <85% | # of 3-party obligations correctly attributed / total obligations in 3-party contracts |
| Obligation Tracking Accuracy (4+-Party) | >85% | <80% | # of 4+-party obligations correctly attributed / total obligations in 4+ party contracts |
| Conditional Obligation Parsing Accuracy | >95% | <90% | # of if/then obligations correctly parsed with both scenarios mapped / total conditional obligations |
| Dependency Graph Completeness | 100% | <98% | # of obligation dependencies correctly identified and mapped in graph / total dependencies in contract |
| Scenario Alignment Rate | 100% | <95% | # of contracts with both parties signed off on scenario interpretation / total multi-party contracts |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Multi-Party Contract Detected (3+) | Contract identified with 3 or more parties; obligation complexity increased | HIGH | Mandatory attorney review; require obligation graph and scenario mapping before execution; parties must align on interpretation |
| Entity Resolution Ambiguity | Pronoun or reference cannot be resolved to specific party; obligation clause has unclear obligor/obligee | CRITICAL | Block analysis; route to attorney for explicit entity naming; require contract amendment clarifying which party is obligor |
| Missing Dependency Detected | Obligation identified with prerequisite not found in contract (e.g., "Party C pays if Party A delivers" but no delivery obligation for Party A) | HIGH | Escalate to legal; potential contract gap; may require amendment or explicit clarification |
| Circular Dependency Detected | Obligation graph contains cycle (Party A must pay if Party B delivers; Party B must deliver if Party A pays) | CRITICAL | Block execution; deadlock condition; requires renegotiation to break cycle |
| Scenario Misalignment | Parties have conflicting interpretations of conditional scenarios; no agreement on what happens if condition not satisfied | HIGH | Route to legal/procurement for renegotiation; require explicit scenario worksheet sign-off before execution |
| Obligation Mismatch Post-Dispute | Dispute arises revealing party had different understanding of obligations than contracted; traces back to multi-party resolution failure | HIGH | Investigate root cause; update obligation graph patterns; audit similar contracts for same pattern |

---

## References

- [NLP for Contract Extraction](https://arxiv.org/abs/1906.11419)
- [Semantic Parsing of Legal Text](https://arxiv.org/abs/2104.08671)
- [Obligation Mining from Legal Documents](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3672842)
