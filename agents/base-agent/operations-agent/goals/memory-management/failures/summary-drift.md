# Summary Drift

## Issue: Repeated Summarization Degrades Information Quality

**Frequency**: Very Common

**Symptoms**
- Key details lost after multiple summaries
- Facts become vague or generalized
- Specific numbers become "approximately"
- Names and entities lost
- Summaries diverge from original content

**Root Cause**
Long-running agents often summarize conversation history to fit context windows. Each summarization cycle loses information. After 3-5 cycles, specific details degrade to generalities. "John ordered 5 widgets at $10 each" becomes "A customer ordered some products" - losing name, quantity, and price.

**Example**
```
Original conversation:
"User John (ID: 12345) reported a billing error on 
invoice #INV-2024-789. He was charged $450 instead 
of $350. The error occurred due to duplicate shipping 
charges. Refund of $100 approved by Sarah (manager)."

After summarization cycle 1:
"Customer John reported billing issue on invoice 789.
Overcharged by $100, refund approved."

After summarization cycle 2:
"Customer had billing problem, refund was processed."

After summarization cycle 3:
"There was a billing issue that was resolved."

Information lost:
- User ID: 12345
- Invoice number: INV-2024-789
- Specific amounts: $450, $350, $100
- Root cause: duplicate shipping
- Approver: Sarah
```

**Contributing Factors**
- Repeated summarization cycles
- No key fact extraction before summarization
- Generic summarization prompts
- No fidelity checks
- Compression ratio too aggressive
- No structured data preservation

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Multi-cycle summary | 5 summary cycles | Key facts preserved | Facts lost |
| Numeric preservation | Numbers in original | Numbers in summary | Generalized |
| Entity retention | Named entities | Entities preserved | Names lost |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Fact retention | >90% per cycle | Key facts in summary |
| Entity retention | >95% | Named entities preserved |
| Numeric accuracy | 100% | Numbers match original |

---

## Mitigation Strategies

### Prevention
1. **Key fact extraction**: Extract facts before summarizing prose
2. **Structured + prose**: Keep structured data separate
3. **Fidelity checks**: Verify summary contains key facts
4. **Limited cycles**: Cap summarization iterations
5. **Importance scoring**: Preserve high-importance facts
6. **Hierarchical summary**: Multiple detail levels

### Architecture Pattern
```
Original conversation
        ↓
[Key Fact Extraction]
        ↓
┌─────────────────────────────────┐
│ Structured facts (preserved):   │
│   user_id: 12345               │
│   invoice: INV-2024-789        │
│   refund_amount: $100          │
├─────────────────────────────────┤
│ Prose summary (compressed):     │
│   "Billing issue resolved"     │
└─────────────────────────────────┘
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `summary.fact_retention` | <90% |
| `summary.cycle_count` | >3 |
| `summary.entity_loss` | >0 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High Fact Loss | >20% facts lost | P2 |
| Excessive Cycles | >5 summarization cycles | P3 |
| Critical Entity Lost | Key entity missing | P2 |

---

## References

- [Summarization Quality](https://arxiv.org/abs/2301.13848)
- [Memory in LLM Agents](https://arxiv.org/abs/2312.08901)
