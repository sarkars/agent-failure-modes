# Billing Reconciliation Gaps

## Issue: Internal Cost Tracking Doesn't Match Vendor Invoices

**Frequency**: Common

**Symptoms**
- Internal metrics show different costs than invoices
- Cannot explain billing discrepancies
- Chargeback totals don't match actual spend
- Missing costs from certain request types
- Timing mismatches between tracking and billing

**Root Cause**
Internal token counting and cost calculation often differs from vendor billing. Reasons include: different tokenization methods, missed request types (embeddings, fine-tuning), timing differences, price changes not reflected, or failed requests still billed. Without reconciliation, organizations lose visibility into actual spend.

**Example**
```
Monthly reconciliation:

Internal tracking: $8,450
Vendor invoice:    $12,230
Gap:               $3,780 (31% undercount!)

Investigation reveals:
- Embedding calls not tracked: $1,200
- System prompts undercounted: $800
- Failed requests still billed: $450
- Price increase not updated: $1,330

Root causes:
1. Only tracked completion tokens, not prompt tokens
2. Embeddings used different API, not instrumented
3. Assumed failed = free (wrong)
4. Hardcoded old prices
```

**Contributing Factors**
- Different tokenizers (internal vs. vendor)
- Missing request types in tracking
- Prompt tokens ignored
- Failed requests not counted
- Price changes not updated
- Timing/timezone differences
- Caching not accounted for

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Token count accuracy | Known text | Match vendor count | >1% variance |
| All request types | Chat, embed, etc. | All tracked | Missing types |
| Failed request cost | Trigger failures | Costs tracked | Zero cost recorded |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Reconciliation accuracy | >98% | Internal vs. invoice |
| Coverage | 100% | Request types tracked |
| Price accuracy | 100% | Internal vs. current pricing |

---

## Mitigation Strategies

### Prevention
1. **Use vendor tokenizer**: tiktoken for OpenAI, etc.
2. **Track all request types**: Chat, embeddings, images, fine-tuning
3. **Include prompt tokens**: Both input and output
4. **Track failures**: Billed even if failed
5. **Auto-update prices**: Fetch from pricing APIs
6. **Daily reconciliation**: Compare internal vs. billing API

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `reconciliation.gap_percent` | >5% |
| `tracking.coverage` | <100% |
| `price.last_updated` | >7 days |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Reconciliation Gap | >10% variance | P2 |
| Missing Request Type | Untracked API calls | P3 |
| Stale Pricing | >30 days old | P3 |

---

## References

- [OpenAI: Tokenizer](https://github.com/openai/tiktoken)
- [OpenAI: Usage API](https://platform.openai.com/docs/api-reference/usage)
