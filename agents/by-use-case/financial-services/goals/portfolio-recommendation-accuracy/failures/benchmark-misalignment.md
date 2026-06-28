# Benchmark Misalignment in Portfolio Recommendations

## Issue: Model Optimizes Against a Generic Benchmark That Does Not Match the Client's Actual Risk Profile, Goals, or Constraints

**Frequency**: Very Common

**Symptoms**
- Recommended allocation matches a default 60/40 or S&P 500 benchmark regardless of client's stated time horizon, liabilities, or tax situation
- Retirees receive growth-tilted portfolios benchmarked to equity indices instead of liability-matching benchmarks
- Performance reporting shows "beating the benchmark" while client's actual goals (e.g., funding a specific liability) are unmet
- Client complaints about volatility despite "on benchmark" performance

**Root Cause**
Recommendation agents frequently default to industry-standard benchmarks (S&P 500, 60/40 blend) baked into training data and evaluation metrics, rather than constructing a custom benchmark from the client's goals, liabilities, time horizon, and constraints. Optimizing relative performance against the wrong benchmark produces a portfolio that is "correct" by the model's metric but wrong for the client.

**Example**
```
Scenario: Advisor-agent generates retirement portfolio for a 68-year-old client
Client's stated goal: Fund $40k/year withdrawals starting immediately
Model benchmark: S&P 500 (default in training data)
Recommendation: 75% equities to "beat the benchmark"
Reality: Sequence-of-returns risk in down market years forces premature drawdown of principal
Impact: Client runs out of funds 8 years earlier than a liability-matched glide path would project
```

**Key Statistics**
- Default-benchmark recommendation errors are implicated in a meaningful share of suitability complaints in retail advisory reviews
- Liability-relative benchmarking reduces sequence-of-returns shortfall risk by an estimated 25-35% versus index-relative benchmarking for near-retirees
- Mismatched benchmark selection is one of the most common root causes cited in robo-advisor suitability audits

---

## Mitigation Strategies

1. **Goals-Based Benchmark Construction**: Build a custom benchmark from the client's liabilities, time horizon, and withdrawal needs instead of defaulting to a market index
2. **Suitability Gate**: Require explicit confirmation that the chosen benchmark reflects the client's risk capacity (not just risk tolerance survey answers)
3. **Glide-Path Modeling**: For near-retirees, evaluate recommendations against liability-matching glide paths, not static index blends
4. **Benchmark Audit Trail**: Log which benchmark was used and why, for compliance and suitability review

### Metrics
- % of recommendations using client-derived vs. default benchmark
- Suitability complaint rate tied to benchmark mismatch
- Sequence-of-returns shortfall risk under goals-based vs. index-relative benchmark

### Alerts
- Default benchmark used for client with stated liability/withdrawal goal → P2
- Suitability complaint flags benchmark mismatch → P1

---

## References

- [Evaluating LLMs in Finance Requires Explicit Bias Consideration](https://arxiv.org/abs/2602.14233)
- [Toward Reliable Evaluation of LLM-Based Financial Multi-Agent Systems](https://arxiv.org/abs/2603.27539)
