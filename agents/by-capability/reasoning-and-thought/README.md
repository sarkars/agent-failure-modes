# Reasoning & Chain-of-Thought

Failures in extended reasoning processes, test-time compute, and chain-of-thought reasoning (o1/o3-style models).

## Goals

| Goal | Description | Patterns |
|------|-------------|----------|
| [Search Space Explosion](goals/search-space-explosion/) | Unbounded token generation, memory exhaustion | In progress |
| [Reasoning Overconfidence](goals/reasoning-overconfidence/) | Convincing but incorrect reasoning; confidence-accuracy mismatch | In progress |
| [Reasoning Latency](goals/reasoning-latency/) | Unpredictable compute time, SLA breaches, tail latency | In progress |
| [Intermediate Token Overflow](goals/intermediate-token-overflow/) | Token limits exceeded mid-reasoning chain | In progress |

**Status**: ~35 patterns planned

## Key Challenges

1. **Unbounded Reasoning**: Models can think indefinitely; no convergence guarantee
2. **Reasoning Overconfidence**: Intermediate steps seem valid but cascade to wrong answer
3. **Latency Variance**: Same query produces 2s or 60s reasoning time
4. **Context Loss**: Early reasoning forgotten in long chains
5. **Irreproducibility**: Sampling variation makes reasoning paths unpredictable
