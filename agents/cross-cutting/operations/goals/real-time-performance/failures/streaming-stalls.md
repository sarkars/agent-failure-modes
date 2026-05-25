# Streaming Stalls

## Issue: Token Streaming Pauses or Stutters During Response

**Frequency**: Common

**Symptoms**
- Visible pauses in streamed output
- User sees text appear in bursts, not smoothly
- Time to first token acceptable but mid-stream delays
- Voice synthesis has audible gaps

**Root Cause**
Streaming responses can stall due to compute bottlenecks, network buffering, tool calls mid-stream, or backend processing delays. Users perceive stuttering as system unreliability.

**Example**
```
Expected streaming (smooth):
"The answer is..." [50ms] "that you should..." [50ms] "consider..."

Actual streaming (stalled):
"The answer is..." [50ms] "that you should..." [2000ms STALL] "consider..."

Stall causes:
- Tool call initiated mid-response
- GPU memory pressure
- Network buffer flush delay
- Backend rate limiting
```

**Contributing Factors**
- Tool calls during generation
- Shared GPU resources
- Network buffering settings
- Rate limiting on API
- Large context causing compute spikes

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Streaming smoothness | Long response | < 100ms between chunks | > 500ms gaps |
| Mid-stream tool call | Query requiring lookup | Graceful pause indication | Silent stall |
| Concurrent load | 10 parallel streams | Even distribution | Some streams starved |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Inter-token latency P95 | < 100ms | Time between chunks |
| Stall events per response | 0 | Gaps > 500ms |
| Time to first token | < 200ms | First chunk latency |

---

## Mitigation Strategies

### Prevention
1. **Dedicated compute**: Isolate streaming workloads
2. **Smaller chunk sizes**: More frequent, smaller updates
3. **Pre-fetch tool results**: Call tools before generation
4. **Buffer tuning**: Optimize network buffer sizes
5. **Priority queuing**: Prioritize active streams

### Streaming Architecture
```python
async def stream_with_stall_detection(response):
    last_chunk_time = time.time()
    
    async for chunk in response:
        current_time = time.time()
        gap = current_time - last_chunk_time
        
        if gap > 0.5:  # 500ms stall
            log_stall_event(gap)
            yield "[processing...]"  # User feedback
        
        yield chunk
        last_chunk_time = current_time
```

### Recovery
- Send "thinking" indicators during stalls
- Client-side smoothing of bursty output
- Fallback to non-streaming on repeated stalls

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `stream.inter_token.p95` | > 200ms |
| `stream.stall.count` | > 0 per response |
| `stream.ttft` | > 500ms |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Streaming Stalls | stall_rate > 5% | P2 |
| TTFT Degradation | ttft_p95 > 1s | P2 |
| Stream Starving | some streams > 2s gap | P1 |

---

## References

- [OpenAI Streaming Best Practices](https://platform.openai.com/docs/api-reference/streaming)
- [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
