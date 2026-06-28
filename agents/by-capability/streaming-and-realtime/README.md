# Streaming & Real-Time Agentic Workflows

Failures specific to continuous, streaming execution of agent inference as opposed to batch processing.

## Goals

| Goal | Description | Patterns |
|------|-------------|----------|
| [Interruption Recovery](goals/interruption-recovery/) | Connection drops, partial completions | In progress |
| [Real-Time Consistency](goals/real-time-consistency/) | State consistency under time pressure | In progress |
| [Token Limits](goals/token-limits/) | Context/token overflow during streaming | In progress |

**Status**: ~25 patterns planned

## Key Challenges

1. **Connection Volatility**: Network drops mid-stream corruption state
2. **Low-Latency Accuracy Tradeoff**: Speed demands sacrifice correctness
3. **Partial State Commits**: Incomplete outputs treated as complete
4. **Backpressure Handling**: Consumer too slow, buffer overflow
5. **Streaming vs Batch Divergence**: Different model serving stacks produce different outputs
