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

**Mitigation Strategies**
1. **Streaming responses**: Start TTS before full response ready
2. **Smaller models**: Use faster models for simple tasks
3. **Response caching**: Cache common responses
4. **Parallel processing**: Overlap ASR, NLU, TTS
5. **Filler responses**: "Let me check..." while processing
6. **Edge deployment**: Reduce network latency

**Detection**
- Measure end-to-end latency (p50, p95, p99)
- Track latency by component
- Monitor user "hello?" interruptions
- Correlate latency with abandonment
- A/B test latency optimizations

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Latency issues
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Response time
- [Voice UX Research](https://www.nngroup.com/articles/response-times/) - Timing expectations
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
