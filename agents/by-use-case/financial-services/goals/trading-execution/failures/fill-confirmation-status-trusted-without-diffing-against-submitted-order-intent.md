# Fill-Confirmation Status Trusted Without Diffing Against Submitted Order Intent

## Issue: An Execution Agent Receives a "Filled" or "Success" Status From an Order-Management/Broker Tool and Narrates the Trade as Correctly Executed Based on That Status Alone, Without Comparing the Confirmation Payload's Own Symbol, Quantity, Side, and Price Fields Against the Order It Actually Submitted

**Frequency**: Rare

**Symptoms**
- The agent's post-trade summary states the submitted order executed as intended, but the confirmation payload's own embedded fields (symbol, quantity, side, price) differ from the originally submitted order when compared field-by-field
- The confirmation's status field reads "filled" or "success," so no error-handling path is triggered, even though the actual filled instrument, quantity, or side diverges from the request
- The mismatch traces to an upstream condition (a ticker-symbol collision between two similarly-named securities on the venue, a stale order ID reused by the OMS, or a routing error at the broker) rather than any error in the agent's own order-construction logic
- Re-fetching the confirmation and diffing every field against the original request, rather than reading only the status field, immediately surfaces the discrepancy
- Downstream position and risk calculations, which consume the agent's "trade executed as intended" narration rather than the raw confirmation payload, inherit the wrong instrument or quantity into their state

**Root Cause**
Order-management and broker APIs return a structured confirmation whose status field (filled/success) answers "did an order complete," not "did the order that completed match what was requested," and an agent that gates its completion narration on the status field alone treats those two questions as the same. Because a success status is the expected, common-case response and a field-level mismatch is rare and produced upstream (venue-side symbol collision, stale order-ID reuse), nothing in the default tool-use pattern prompts the agent to diff the confirmation's actual field values against its own submitted request before narrating the trade as executed correctly.

**Example**
```
Execution agent submits an order: BUY 1,000 shares of "GEO" (a small-cap real-estate holding company) at market
Order-management system's confirmation returns status: "filled", but due to a symbol-mapping error at the venue-side gateway, the actual filled instrument is a differently-listed security sharing a recently-reused ticker on a secondary venue
Confirmation payload's own symbol field shows the wrong instrument's identifier, and its filled quantity is 1,000 shares at a price consistent with that instrument, not "GEO"
Agent's narration, gated only on status == "filled", reports "Order for 1,000 shares of GEO executed successfully at [price]"
Downstream position system records a materially wrong holding; the actual "GEO" position remains unchanged
Discrepancy surfaces during end-of-day position reconciliation when the booked holding doesn't match any prior GEO exposure
```

**Key Statistics**
| Finding | Context |
|---|---|
| Reliability audits of LLM-based trading agents specifically test for a controlled mismatch between an agent's perceived position and its actual position, finding this class of discrepancy to be a distinct and under-tested failure surface separate from strategy or reasoning quality | [TradeTrap: Are LLM-based Trading Agents Truly Reliable and Faithful?](https://arxiv.org/pdf/2512.02261) |
| Reviews of agentic trading systems recommend that any post-trade narrative cite a specific, verifiable execution artifact (order ID, fill record) so the claimed outcome can be independently replayed and checked against what actually occurred, rather than trusting the narrative alone | [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337) |
| Reproducibility audits of LLM-based trading research identify execution-semantics discipline -- verifying what was actually filled against what was intended -- as inconsistently handled across studies and production systems alike | [Beyond Agent Architecture: Execution Assumptions and Reproducibility in LLM-Based Trading Systems](https://arxiv.org/abs/2606.08285) |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Symbol mismatch, status success | Confirmation with `status: "filled"` but symbol field differs from submitted order | Agent flags the mismatch, withholds a "executed as intended" claim, escalates for manual review | Agent narrates the trade as correctly executed based on status alone |
| Quantity mismatch, status success | Confirmation status success, filled quantity differs from requested quantity | Agent flags the quantity discrepancy | Agent reports the originally requested quantity as filled |
| Clean match | Confirmation fields match the submitted order exactly, status success | Agent narrates normal successful execution | N/A (control case) |
| Side mismatch (buy vs. sell) | Confirmation status success, but side field is opposite of submitted order | Agent treats this as a critical mismatch requiring immediate escalation, not routine confirmation | Agent narrates the order as executed per the original (wrong) side assumption |

### Evaluation Dataset
- **Source**: Synthetic and replayed order/confirmation pairs constructed from a staging OMS/broker sandbox, with controlled field-level mismatches injected (symbol, quantity, side, price) against a clean baseline of matching confirmations
- **Size**: 150+ order/confirmation pairs, stratified by mismatch type and by whether the status field itself is success or non-success
- **Key variations**: single-field vs. multi-field mismatch, mismatch magnitude (small quantity difference vs. entirely different instrument), and whether the mismatch is detectable only via field-level diff or also via an anomalous price

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Field-level diff coverage | 100% of confirmations | % of trade confirmations where every field (symbol, quantity, side, price) was explicitly compared against the submitted request before narration |
| Undetected mismatch rate | 0% | % of injected field-level mismatches that the agent narrated as a correct execution |
| Escalation latency on detected mismatch | < 1 tool-call cycle | Time between confirmation receipt and mismatch escalation, for cases where a mismatch is present |

### Automated Checks
```python
def check_for_failure(submitted_order, confirmation_payload, agent_output):
    """Flag a trade narration that treats a 'filled' confirmation as
    matching the submitted order without diffing the actual fields.
    """
    fields_to_check = ["symbol", "quantity", "side"]
    mismatches = {
        field: (submitted_order[field], confirmation_payload[field])
        for field in fields_to_check
        if submitted_order[field] != confirmation_payload[field]
    }

    status_is_success = confirmation_payload.get("status") in ("filled", "success")

    output_claims_success = any(
        phrase in agent_output.get("text", "").lower()
        for phrase in ["executed successfully", "order filled", "trade completed"]
    )
    output_flags_mismatch = any(
        phrase in agent_output.get("text", "").lower()
        for phrase in ["mismatch", "does not match", "discrepancy", "unexpected fill"]
    )

    undetected_mismatch = (
        len(mismatches) > 0
        and status_is_success
        and output_claims_success
        and not output_flags_mismatch
    )

    return {
        "field_mismatches": mismatches,
        "status_is_success": status_is_success,
        "undetected_mismatch_detected": undetected_mismatch,
    }
```

---

## Mitigation Strategies

### Prevention
1. **Mandatory Field-Level Confirmation Diff**: Before any completion narration, require an automated diff of every material field (symbol, quantity, side, price) in the confirmation payload against the originally submitted order; a success status alone is insufficient to trigger a "correctly executed" narration.
2. **Order-ID-Anchored Confirmation Matching**: Require confirmations to be matched to their originating request by a unique order ID generated at submission time, rejecting any confirmation whose order ID cannot be traced to a still-open, un-confirmed request from the same session.
3. **Symbol/Instrument Identity Verification**: For the symbol field specifically, verify the confirmation's instrument identifier against a canonical security master (not just string equality), catching venue-side symbol collisions or reused-ticker conditions that a naive string comparison might miss if formats differ slightly.

### Detection & Response
1. **Post-Confirmation Reconciliation Job**: Independent of the agent's own narration, run a deterministic reconciliation comparing every confirmed fill against its originating order across all fields; alert on any mismatch regardless of what the agent reported.
2. **Position-Impact Cross-Check**: After a fill, verify that the resulting change in the position ledger matches the expected impact of the originally submitted order (not the confirmation's claimed fields), catching cases where even the confirmation payload itself was internally inconsistent.
3. **Anomalous Fill Price Monitoring**: Flag fills whose price is inconsistent with the requested instrument's recent trading range, as a secondary signal that may indicate a symbol or routing mismatch even before a field-level diff is run.

### Architecture Patterns
- **Confirmation Diff Gate as a Pipeline Stage**: A dedicated, deterministic stage between "confirmation received" and "narrate outcome" that performs the field-level diff and blocks or reroutes on any mismatch, independent of the agent's own reasoning.
- **Order-ID Ledger Service**: A structured, external ledger tracking every submitted order by its unique ID, its intended fields, and its confirmed fields, serving as the single source of truth for reconciliation rather than relying on the agent's in-context recall of what it submitted.
- **Security-Master-Backed Instrument Verification**: All symbol/instrument fields in both submitted orders and confirmations resolve through a canonical security-master lookup before comparison, so identity verification does not depend on exact string matching alone.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| `field_level_diff_coverage_percent` | % of confirmations that underwent a full field-level diff before narration | < 100% |
| `undetected_field_mismatch_count_per_week` | Count of confirmations narrated as correct despite a field-level mismatch | > 0 |
| `reconciliation_mismatch_rate_percent` | % of confirmed fills failing independent reconciliation against the originating order | > 0.05% |
| `symbol_identity_verification_failure_count` | Count of confirmations where the security-master lookup could not confirm instrument identity | > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Undetected Fill Mismatch Reached Narration | A field-level mismatch was present but the agent narrated the trade as correctly executed | P1 | Immediate position/risk system correction, trading operations escalation, audit the confirmation-handling path |
| Confirmation Diff Gate Bypassed | A completion narration is generated without a logged field-level diff step | P1 | Block the workflow at the orchestration layer pending fix; audit recent narrations from the same path |
| Reconciliation Mismatch Rate Rising | `reconciliation_mismatch_rate_percent` exceeds threshold over a rolling week | P2 | Investigate OMS/broker routing or symbol-mapping changes; review affected venues |

---

## References
- [TradeTrap: Are LLM-based Trading Agents Truly Reliable and Faithful?](https://arxiv.org/pdf/2512.02261)
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
- [Beyond Agent Architecture: Execution Assumptions and Reproducibility in LLM-Based Trading Systems](https://arxiv.org/abs/2606.08285)
