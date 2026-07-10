# Response Latency Issues

## Issue: Agent Takes Too Long to Respond

**Frequency**: Very Common

**Symptoms**
- Awkward silence after user speaks
- Users ask "Are you there?"
- Users start repeating themselves
- Conversation feels slow and unnatural
- Task completion time increases

**Root Cause**
Voice agents have multiple latency sources: ASR processing, NLU inference, backend calls, LLM generation, TTS synthesis. Each adds delay. Users expect response within 500ms (similar to human conversation), but many voice agents take 1-3 seconds. This delay makes the agent feel slow, robotic, and frustrating.

**Example**
```
Scenario: Voice assistant latency breakdown

User: "What's the weather tomorrow?"
[End of speech detected]

Latency breakdown:
  ASR finalization:     200ms
  NLU processing:       150ms  
  LLM generation:       800ms  ← Biggest delay
  TTS synthesis:        300ms
  Audio streaming:      100ms
  ─────────────────────────────
  Total:               1550ms

User experience:
  0-300ms: Feels instant
  300-500ms: Acceptable
  500-1000ms: Noticeable delay
  1000-2000ms: "Is it working?"
  2000ms+: Frustrating

User behavior during 1550ms wait:
  - At 800ms: User shifts uncomfortably
  - At 1200ms: User says "Hello?"
  - At 1500ms: Agent finally responds
  
Impact:
  - User spoke "Hello?" → Creates confusion
  - Agent may respond to "Hello?" instead of weather
  - Conversation flow broken
```

**Key Statistics**
From Latency Research (2026):
- User expectation: <500ms response
- Average voice agent: 800ms-2000ms
- LLM contribution: 40-60% of latency
- Each 100ms delay: 1% satisfaction drop
- 2s+ latency: 25% abandonment increase

**Latency Contributors**
| Component | Typical | Optimal | Contribution |
|-----------|---------|---------|--------------|
| ASR | 200-400ms | 100-200ms | 15-20% |
| NLU/LLM | 500-1500ms | 200-400ms | 40-60% |
| Backend | 100-500ms | 50-100ms | 10-20% |
| TTS | 200-400ms | 100-200ms | 15-20% |
| Network | 50-200ms | 20-50ms | 5-10% |

**Contributing Factors**
- Large LLM models (slow inference)
- Sequential processing (not parallel)
- No streaming responses
- Cold start delays
- Distant servers
- No response caching

## Mitigation Strategies

### Prevention
1. **Streaming Pipeline with Incremental TTS**: Begin synthesizing and playing TTS audio as soon as the first sentence/clause of the LLM response is available, rather than waiting for the full response to generate, cutting perceived latency by overlapping generation and playback. Trade-off: streaming requires the LLM output and TTS engine to both support incremental/chunked processing, and early chunks can't be revised if the full response changes tone/content.
2. **Model Tiering by Task Complexity**: Route simple, well-defined requests (weather lookup, balance check) to smaller/faster models or cached logic, reserving larger LLM calls for genuinely open-ended reasoning, rather than sending every utterance through the same heavyweight model. Trade-off: requires reliable upfront complexity/intent classification to route correctly, and misrouting simple-looking-but-actually-complex requests degrades quality.
3. **Parallelized Pipeline Stages**: Overlap ASR finalization, NLU, and backend calls where they don't have hard sequential dependencies (e.g., start a backend lookup speculatively once partial ASR is confident enough) rather than a strictly serial ASR-then-NLU-then-backend-then-LLM-then-TTS chain.

### Detection & Response
1. **Per-Component Latency Instrumentation**: Break down end-to-end latency into ASR, NLU/LLM, backend, and TTS segments in production telemetry (not just aggregate latency), so regressions can be attributed to the specific stage that slowed down rather than treated as a single opaque number.
2. **Filler-Response Trigger on Latency Threshold**: When projected/actual response time exceeds a threshold (e.g., 700ms), automatically insert a lightweight filler ("Let me check that...") to preserve conversational rhythm and prevent user "Hello?" interjections, rather than leaving dead air.
3. **User Hello/Repeat Detection as Latency Proxy**: Treat user utterances like "Hello?" or exact repeats of the prior question as an implicit latency complaint signal; correlate their rate with p95/p99 latency to validate whether the perceived-latency threshold assumptions match real user tolerance.

### Architecture Patterns
1. **Streaming ASR-to-TTS Pipeline**: Standard low-latency voice architecture — streaming ASR emits partials, a fast intent router acts on high-confidence partials where safe, LLM generation streams tokens directly into a streaming TTS engine, and audio playback begins on the first synthesized chunk.
2. **Response Caching for Common Queries**: Cache full or partial responses for high-frequency, low-variance queries (store hours, standard policies) keyed on normalized intent+slots, bypassing the LLM generation step entirely for cache hits.
3. **Edge/Regional Deployment**: Deploy ASR/TTS/LLM inference in regions close to the user base to cut network round-trip contribution to latency, particularly impactful for globally distributed user bases hitting a single central region.

### Metrics
1. **end_to_end_latency_ms_p95**: Target: < 800ms; Alert threshold: > 1500ms
2. **llm_generation_latency_ms_p95**: Target: < 400ms; Alert threshold: > 1000ms
3. **filler_response_trigger_rate_percent**: Target: < 15% of turns; Alert threshold: > 40% (indicates systemic slowness, not occasional spikes)
4. **user_hello_or_repeat_rate_percent**: Target: < 5%; Alert threshold: > 15%

### Alerts
1. **P95 Latency Breach** (P1): Condition - end-to-end p95 latency exceeds 1500ms for 5+ minutes. Action: Page on-call, check LLM/backend service health and autoscaling, consider temporary model-tier downgrade for non-critical flows.
2. **Filler-Trigger Rate Spike** (P2): Condition - filler-response trigger rate exceeds 40% in a rolling window. Action: Identify slow pipeline stage via per-component latency breakdown, investigate recent deploys.
3. **User Frustration Signal Surge** (P2): Condition - "Hello?"/repeat rate exceeds 15% of conversations. Action: Correlate with latency metrics, prioritize latency fix for affected flow/region.

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Latency issues
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Response time
- [Voice UX Research](https://www.nngroup.com/articles/response-times/) - Timing expectations
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
