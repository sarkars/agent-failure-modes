# Cost Attribution Errors

## Issue: Costs Cannot Be Accurately Attributed to Users, Agents, or Use Cases

**Frequency**: Common

**Symptoms**
- Cannot determine which user/agent caused costs
- Chargeback calculations inaccurate
- Cost centers receive wrong allocations
- Cannot identify expensive operations
- Billing disputes unresolvable

**Root Cause**
Multi-tenant agent systems often lack proper cost tagging. When multiple users, agents, or use cases share infrastructure, costs get aggregated without attribution. Without request-level tagging that flows through to billing, organizations cannot implement accurate chargebacks or identify optimization targets.

**Example**
```
Shared agent infrastructure:
  
Month-end bill: $15,000

Attribution attempt:
  User A: ??? (no tracking)
  User B: ???
  Agent Type 1: ???
  Agent Type 2: ???
  
Actual breakdown (if tracked):
  User A: $12,000 (power user, expensive queries)
  User B: $800
  Agent Type 1: $2,500
  Agent Type 2: $11,700
  
Problem: User A's department wasn't charged
         Wrong team optimized the wrong agent
```

**Contributing Factors**
- No request-level cost tagging
- Shared API keys across users/agents
- Async billing without request correlation
- Missing metadata in LLM calls
- Aggregated invoices only
- No tenant isolation in billing

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Multi-user session | Users A, B, C make requests | Per-user cost breakdown | Aggregated only |
| Agent attribution | Different agent types | Per-agent costs | Undifferentiated |
| Chargeback accuracy | Known cost distribution | Matches actual | >5% variance |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Attribution coverage | 100% | Requests with cost tags |
| Chargeback accuracy | >98% | Attributed vs. actual |
| Attribution latency | <1 hour | Time to cost visibility |

---

## Mitigation Strategies

### Prevention
1. **Request tagging**: Add user/agent/tenant ID to every LLM call
2. **Correlation IDs**: Flow IDs from request to billing
3. **Per-tenant API keys**: Separate keys for billing isolation
4. **Real-time attribution**: Calculate costs per-request

### Architecture Pattern
```
Request → [Tag: user_id, agent_id, tenant_id]
              ↓
         LLM Call (tags in metadata)
              ↓
         [Cost calculated with tags]
              ↓
         Attribution DB
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `attribution.coverage` | <100% |
| `attribution.untagged_cost` | >$0 |
| `chargeback.variance` | >5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Unattributed Cost | Any untagged spend | P2 |
| Attribution Gap | Coverage <95% | P2 |
| Chargeback Mismatch | Variance >10% | P3 |

---

## References

- [OpenAI: Usage Tracking](https://platform.openai.com/docs/api-reference/usage)
- [Anthropic: Message Metadata](https://docs.anthropic.com/en/api/messages)
