# Variable Binding Error

## Issue: Agent attaches wrong value to wrong entity.

**Frequency**: Common

**Symptoms**
- Wrong name/account/date in action.
- An action executes with an entity-attribute pairing that doesn't match any valid combination in the source records (e.g., an account number paired with a different customer's name).
- The bound value appears to come from "the closest mentioned value" in the prose rather than from a specific, traceable source record.
- Multi-entity tasks (several accounts, several dates, several people) show values swapped between two similar entities.
- No pre-execution restatement or confirmation step exists to catch a mismatched binding before the action takes effect.

**Root Cause**
Agent attaches wrong value to wrong entity.

**Example**
```
Task: "Move $500 from Account A to Account B, and update Account C's
mailing address to the one on file for Account B."

While assembling the transfer action, the agent binds Account B's
old mailing address (mentioned two sentences earlier) to Account A
instead, because both accounts were referenced close together in the
same paragraph and the agent inferred the binding positionally
rather than reading from a structured entity table.

The executed action updates Account A's address instead of Account
C's, using a value that was never sourced from Account A's own
records at all.
```

**Contributing Factors**
- Entity-value associations are inferred positionally from free text ("the closest mentioned value") instead of read from a structured, keyed binding table.
- No typed entity resolution step converts ambiguous references ("the account," "that date") into canonical entity_ids before attribute values are attached.
- Tasks involving multiple similar entities (several accounts, several people, several dates) increase the chance of cross-entity mix-ups.
- No pre-execution confirmation restates the specific binding for high-stakes actions before they take effect.
- No validation gate cross-checks a bound value's provenance against the source record it claims to come from prior to execution.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Multi-entity proximity confusion | Task mentions two similar entities (Account A, Account B) close together with attributes for each | Each attribute binds to the correct entity_id per the structured binding table | An attribute from one entity is bound to a different entity in the executed action |
| Cross-reference validation | Action bound to entity X using a value claimed to come from entity X's source record | Validation gate confirms the value actually exists in entity X's record before execution | Action executes with a value that doesn't appear in the claimed source entity's data |
| Pre-execution confirmation catch | High-stakes action (fund transfer) with a fully assembled binding is presented for confirmation before execution | Confirmation step restates the exact binding, allowing a mismatched binding to be caught and corrected | Action executes without a restated confirmation, or confirmation text doesn't match the actual bound parameters |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| eval_binding_accuracy_percent | >= 99% of eval multi-entity test cases bind values to the correct entity_id | Run eval suite with proximity-confusable multi-entity scenarios, compare bound values against ground truth |
| eval_cross_reference_validation_catch_rate_percent | >= 99% of injected mis-bindings are caught by the validation gate | Inject deliberately wrong entity-value pairings into eval scenarios, measure gate rejection rate |
| eval_confirmation_restatement_accuracy_percent | 100% of eval high-stakes actions produce a confirmation matching the actual bound parameters | Compare pre-execution confirmation text against the actual parameters passed to the eval tool call |

---

## Mitigation Strategies

### Prevention
1. **Structured Entity-Slot Binding with Type/ID Verification**: Rather than letting the model freely associate values to entities in free text, extract each entity reference into a typed slot (entity_type, entity_id, resolved_value) and validate that the bound value's type and source match what the slot expects (e.g., a date slot cannot bind a value extracted from a different customer's record) before it's used in an action.
2. **Explicit Binding Table for Multi-Entity Tasks**: When a task involves multiple similar entities (several accounts, several dates, several people), the agent constructs an explicit table (entity_id → attribute → value) and every downstream reference reads from a specific table cell by key, not from positional/contextual inference in prose, eliminating the "closest mentioned value" mis-binding pattern.
3. **Pre-Execution Binding Confirmation for High-Stakes Actions**: Before executing an action with bound entity-value pairs (money transfer, appointment booking, record update), the agent restates the specific binding ("transferring $500 from Account A to Account B") and requires confirmation, catching swapped or misattributed bindings before they take effect.

### Detection & Response
1. **Cross-Reference Validation Against Source Records**: After binding, verify each bound value against its claimed source record (e.g., the date bound to "Account A" actually appears in Account A's data, not Account B's) and block execution on mismatch.
2. **Wrong-Entity Action Detection**: Monitor executed actions for entity-attribute combinations that don't match any valid source record combination in the task's data (e.g., an account number bound with a name that doesn't correspond in the source system) and flag as binding errors, ideally pre-execution but at minimum post-hoc.
3. **User/Downstream Correction Tracking**: Log cases where a user or downstream system reports a wrong name/account/date was used in an action, and trace back through the binding table to identify where the mis-binding occurred (extraction, table construction, or final action-parameter assembly).

### Architecture Patterns
1. **Typed Entity Resolution Layer**: A dedicated component resolves every entity mention in a task to a canonical entity_id with a defined type, before any attribute values are attached, so binding operates on resolved IDs rather than ambiguous surface text like "the account" or "her date."
2. **Binding Table as Single Source of Truth**: All entity-attribute-value bindings for a task live in a structured table that both the planning/reasoning step and the final action-execution step read from identically, preventing divergence between what was reasoned about and what was actually executed.
3. **Action-Parameter Validation Gate**: Before any tool call that takes entity-scoped parameters, a validation gate cross-checks each parameter against the binding table and the source record it claims to come from, rejecting the call if any parameter's provenance doesn't match its claimed entity.

### Metrics
1. **binding_validation_failure_rate_percent**: Target: < 0.5% of multi-entity tasks; Alert threshold: > 2%
2. **wrong_entity_action_count**: Target: 0 per week; Alert threshold: > 1 per week
3. **pre_execution_confirmation_catch_rate_percent**: Target: tracked (bindings corrected at confirmation step before execution); Alert threshold: sudden drop signals confirmation step being skipped
4. **cross_reference_mismatch_rate_percent**: Target: < 0.2%; Alert threshold: > 1%

### Alerts
1. **Wrong-Entity Action Executed** (P1 - Critical): Condition - an action executed with an entity-attribute binding that doesn't match the source record (e.g., wrong account debited). Action: Immediate reversal where possible, notify affected parties, incident review of the binding/validation pipeline.
2. **Validation Gate Bypass** (P1 - Critical): Condition - an action executed without passing through the action-parameter validation gate. Action: Freeze the execution path, patch the bypass, audit recent actions of that type for undetected mis-bindings.
3. **Rising Binding Validation Failures** (P2 - Warning): Condition - binding_validation_failure_rate_percent exceeds 2% over a rolling week for a specific task type. Action: Review entity resolution logic for that task type, check for ambiguous source data (duplicate names, overlapping IDs) causing systematic mis-binding.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| binding_validation_failure_rate_percent | > 2% |
| wrong_entity_action_count | > 1 per week |
| cross_reference_mismatch_rate_percent | > 1% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Wrong-Entity Action Executed | An action executed with an entity-attribute binding that doesn't match the source record (e.g., wrong account debited) | Critical |
| Validation Gate Bypass | An action executed without passing through the action-parameter validation gate | Critical |
| Rising Binding Validation Failures | binding_validation_failure_rate_percent exceeds 2% over a rolling week for a specific task type | Warning |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
