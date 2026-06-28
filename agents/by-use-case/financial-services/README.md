# Financial Services

Agents that make trading decisions, manage portfolios, and enforce regulatory compliance in financial systems face domain-specific failures around market data freshness, strategy divergence, and regulatory violations.

## Goals

| Goal | Description | Patterns |
|------|-------------|----------|
| [Market Data Freshness](goals/market-data-freshness/) | Stale prices, staleness windows, cache invalidation | In progress |
| [Regulatory Compliance](goals/regulatory-compliance/) | Threshold violations, regulatory rules, approval workflows | In progress |
| [Strategy Divergence](goals/strategy-divergence/) | Backtest-reality mismatch, overfitting, adaptation | In progress |
| [Trading Execution](goals/trading-execution/) | Liquidity errors, settlement failures, counterparty risk | In progress |

**Status**: ~50 patterns planned

## Key Challenges

1. **Market Volatility**: Real-time prices change faster than agent can react
2. **Regulatory Complexity**: Multi-jurisdiction rules, version control
3. **Backtest Illusion**: Strategy perfect in historical data, fails live
4. **Execution Risk**: Liquidity assumptions don't hold; slippage unaccounted
5. **Approval Bypass**: Agent circumvents required human/system gates
