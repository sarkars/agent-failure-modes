# Variable Binding Error

## Issue: Agent attaches wrong value to wrong entity.

**Frequency**: Common

**Symptoms**
- Wrong name/account/date in action.
- [Add more specific symptoms]

**Root Cause**
Agent attaches wrong value to wrong entity.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
