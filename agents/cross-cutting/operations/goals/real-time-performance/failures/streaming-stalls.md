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

## Chat assistant examples

### Streaming that rewrites itself

*Illustrative dialogue, not a real transcript.*

**Before** (Skyline Air help chat in a phone app, tokens shown as they arrive; policy check runs in parallel):
> **Dana:** I bought a Basic Economy ticket to Denver on Monday. Can I get a refund?
> **Assistant (streaming):** Yes, you are eligible for a full refund. Just tap Cancel Trip and
> **Assistant (replaced mid-stream):** Basic Economy tickets bought more than 24 hours ago are not refundable. You can cancel for a travel credit minus a $99 fee.

**After** (the eligibility check finishes before the first sentence that states a decision):
> **Dana:** I bought a Basic Economy ticket to Denver on Monday. Can I get a refund?
> **Assistant:** Let me check your fare rules. *(shown at once)*
> **Assistant:** Your Basic Economy ticket was bought more than 24 hours ago, so it is not refundable. You can cancel for a travel credit minus a $99 fee. Want me to start that?

**What the user experiences:** Dana reads "you are eligible for a full refund," then watches the text vanish and say the opposite, so she cannot tell which answer to trust.

**Fix:** Stream only text that no later check can retract, such as the "Let me check your fare rules" line, and run the refund-eligibility check before streaming any sentence that says yes or no. If a retraction cannot be avoided, show a line such as "My earlier message was wrong" instead of silently swapping the text. Test it by replaying the Basic Economy case and confirming no streamed sentence is later replaced; for the related silent-failure handling, see [Silent Failure and Timeout](../../../../../by-capability/human-machine-interface/goals/response-time/failures/silent-failure-and-timeout.md).

Vendor docs show why this happens. Microsoft's Azure OpenAI guide says Asynchronous Filter returns tokens without buffering, so policy signals are delayed and the app must be able to "remove or replace content that was already displayed" ([Content Streaming in Azure OpenAI](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/content-streaming)). Default mode buffers content until it is checked, so text arrives in chunks instead of token by token.

---

## References

- [OpenAI Streaming Best Practices](https://platform.openai.com/docs/api-reference/streaming)
- [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
