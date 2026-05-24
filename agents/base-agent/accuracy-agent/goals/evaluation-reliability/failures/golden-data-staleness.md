# Golden Data Staleness

## Issue: Golden Dataset Contains Outdated Information or Expectations

**Frequency**: Common

**Symptoms**
- Agent gives correct current answer, marked wrong
- Expected responses reference deprecated features
- Golden data reflects old business rules
- Evaluation scores drop after real-world improvements
- New capabilities not covered in golden set

**Root Cause**
Golden datasets are created at a point in time and reflect the knowledge, products, and expectations of that moment. As the world changes—products update, prices change, policies evolve, knowledge advances—the golden dataset becomes stale. Agents giving correct current answers are penalized for not matching outdated expected responses.

**Example**
```
Scenario: Customer support agent evaluation

Golden dataset created: January 2025
Evaluation run: June 2026

Golden test case #47:
  Query: "What is the price of the Pro plan?"
  Expected: "$29/month"
  
Current reality:
  Pro plan price: $39/month (changed March 2026)
  
Agent response: "$39/month"
Evaluation result: FAIL (doesn't match expected)

Impact:
  - Agent marked as "inaccurate"
  - Development time spent "fixing" correct behavior
  - Evaluation score: 94% (should be 98%)
  - 47 of 1000 test cases have stale expectations

Root cause analysis:
  - No golden data refresh process
  - Expected responses hardcoded
  - No connection to source of truth
  - Last audit: 18 months ago
```

**Key Statistics**
From Data Quality Research (2026):
- Average golden dataset age: 8-14 months
- 15-25% of test cases stale after 6 months
- 40% of "failures" are actually stale expectations
- Only 23% of organizations have golden data refresh process
- Price/feature data stale within 30-90 days

**Staleness Dimensions**
| Dimension | Example | Decay Rate |
|-----------|---------|------------|
| Pricing | Product costs | 30-90 days |
| Features | Product capabilities | 60-180 days |
| Policies | Business rules | 90-365 days |
| Knowledge | Facts, statistics | 180-365 days |
| Personnel | Contact info, roles | 30-60 days |

**Contributing Factors**
- No refresh schedule for golden data
- Manual golden data maintenance
- No connection to authoritative sources
- Expected responses hardcoded as strings
- No staleness detection mechanism
- Infrequent evaluation audits

**Mitigation Strategies**
1. **Scheduled refresh**: Regular golden data update cycle
2. **Dynamic expectations**: Pull expected values from source systems
3. **Staleness scoring**: Track age of each golden record
4. **Assertion-based tests**: Test properties, not exact strings
5. **Automated audits**: Flag potential stale entries
6. **Version tracking**: Track when each golden entry was validated

**Detection**
- Monitor failure rate trends (sudden spikes = staleness)
- Sample failed cases for manual review
- Compare golden data timestamps to source updates
- Track "false failure" rate from audits
- Alert on golden data age thresholds

## References

- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Evaluation best practices
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Data quality issues
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Evaluation challenges
- [FloTorch: RAG Performance Landscape](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know) - Benchmark limitations
