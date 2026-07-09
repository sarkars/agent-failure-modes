# Streaming ASR Instability

## Issue: Real-Time Transcription Changes Mid-Utterance

**Frequency**: Common

**Symptoms**
- Displayed text changes while user speaks
- Actions triggered on interim results
- Final transcription differs from interim
- Agent responds to partial utterance
- User sees "flickering" transcription

**Root Cause**
Streaming ASR provides real-time transcription updates as audio arrives, but early results are based on incomplete context. As more audio arrives, the transcription may change significantly. Applications that act on interim results or display them prominently can create confusing or incorrect behavior when the final result differs.

**Example**
```
Scenario: Voice assistant with real-time display

User says: "I want to cancel my subscription"

Streaming transcription timeline:
  T+0.3s: "I want"
  T+0.5s: "I want to can"
  T+0.8s: "I want to cancel"      ← Agent shows this
  T+1.0s: "I want to cancel mice" ← Flickering text
  T+1.2s: "I want to cancel my"
  T+1.5s: "I want to cancel my subscription"
  T+1.8s: [Final] "I want to cancel my subscription"

Problem scenario:
  T+0.8s: Agent acts on "I want to cancel"
  Action: Initiates cancellation flow
  T+1.8s: Final result: "I want to cancel my subscription"
  
  But agent already responded to partial intent
  User confused: "I didn't finish yet!"

Another example:
  Interim: "Turn on the lights"
  Final: "Don't turn on the lights"
  
  If acted on interim → wrong action taken
  
Stability analysis:
  Utterances with significant interim→final change: 23%
  Average revisions per utterance: 3.2
  Final differs from last interim: 8%
  Agent acted on wrong interim: 5% of interactions
```

**Key Statistics**
From Streaming ASR Research (2026):
- Interim-to-final change rate: 20-30%
- Significant meaning change: 5-10% of utterances
- User confusion from flickering: 15% report frustration
- Premature action errors: 3-8%
- Average revision count: 2-4 per utterance

**Instability Patterns**
| Pattern | Example | Risk |
|---------|---------|------|
| Negation flip | "don't" appears late | Action reversal |
| Entity change | "New York" → "Newark" | Wrong destination |
| Number revision | "fifteen" → "fifty" | Wrong quantity |
| Incomplete command | "cancel" → "cancel that order" | Premature action |
| Word boundary | "ice cream" → "I scream" | Meaning change |

**Contributing Factors**
- Acting on interim results
- No final result wait logic
- Displaying unstable transcription
- No change detection
- Short timeout before action
- Treating interim as final

## Mitigation Strategies

### Prevention
1. **Streaming Stability Gating Architecture**: Implement multi-stage streaming result pipeline. Stage 1: Collect raw interim results from ASR. Stage 2: Compute stability metrics (revision rate over last 200ms window, confidence score consistency, edit distance from previous). Stage 3: Classify result as stable/unstable. Stage 4: For actions, wait for 2+ consecutive stable results before executing. For display, only show results classified as stable (skip high-revision intermediates). Implement timeout: wait max 500ms for stability before using best-available result.
2. **Negation-Aware Interim Result Filtering**: Special handling for negation/modifier words that appear late in utterances. Pre-process interim results to detect negation words ("don't", "never", "cancel"). If negation detected after significant delay (e.g., at T+0.8s when interim was positive at T+0.3s), flag entire utterance as unstable. Implement negation-specific confidence penalty: penalize results without negations if negation phrases are likely (context mentions cancellation, opt-out). Require additional confirmation if negation appears after action-suggesting interim.
3. **Conservative Interim Result Usage**: Strict policy: interim results used only for UX feedback (visual display, early intent detection), never for actions. Only final results trigger state changes. Implement hard boundary: if critical action (payment, cancellation, booking), ignore all interim results, wait for final or timeout. For informational queries (weather, stock quotes), allow sooner interim response but with explicit "searching..." framing and disclaimer: "Still listening, might update".

### Detection & Response
1. **Interim-to-Final Divergence Tracking**: Compute difference between interim results and final result at T+0.5s, +1.0s, +1.5s. Measure: Levenshtein distance (edit distance), semantic similarity (via NLU), negation flip (does interim lack negation that appears in final?). Track rate of significant changes (edit distance >5, meaning flips, negation appearance). Alert if >10% of utterances show significant interim-to-final divergence. Segment by utterance length and domain.
2. **Premature Action Error Detection**: Implement logging of actions triggered and their timing relative to final ASR result. If action taken before final ASR result arrived, flag as premature. Correlate premature actions with user corrections/complaints. Target: 0 premature action errors on critical operations. Alert immediately if premature action occurs on payment, cancellation, booking. Monthly audit: sample 100 premature actions, analyze root cause (timeout too aggressive, interim confidence too high, etc.).
3. **Transcription Stability Metric Monitoring**: Calculate stability score per utterance: (1 - (total_revisions / utterance_length)). Target stability >0.8 (20% or less revisions). Track rolling 1-hour stability average. Alert if stability drops <0.7 in 1-hour window (indicates ASR degradation or noisy audio conditions).

### Architecture Patterns
1. **Stability-Gated Intent Detection**: Run interim results through NLU to detect intent, but mark intent confidence as "preliminary". Maintain confidence threshold for preliminary intent: 0.90 (higher than final 0.75) to require strong signal before early triggering. When final result arrives, re-run NLU on final. If final intent differs from preliminary, implement correction: explain to user "I was going to [preliminary action], but I actually heard [final intent]". Track how often preliminary vs. final intents differ.
2. **Confidence-Score-Based Result Gating**: Use streaming ASR confidence scores to gate when results can be used. Interim result only usable if: (1) confidence >0.85 AND (2) confidence stable (delta <0.05 from previous interim) AND (3) result hasn't changed >2 words from previous interim. Implement exponential backoff: if result changes frequently, require higher confidence and longer stability window before acting. For final results, use standard threshold (0.75).
3. **User-Correction Capture Loop**: After action taken on interim result, implement brief confirmation window (2-3 seconds): "I understood you want to [action]. Tell me if that's wrong." Listen for correction commands ("no", "wait", "cancel", "wrong"). If correction detected, immediately reverse action and wait for final result. Log corrections to measure how often interim results were actually wrong, feed into stability model retraining.

### Metrics
1. **interim_to_final_change_rate_percent**: Target: <15% of utterances show significant interim-to-final change (edit distance >5). Measure: (utterances_with_significant_change) / (total_utterances). Alert: >20%.
2. **negation_flip_rate_percent**: Target: <2% of utterances where interim lacks negation but final includes it. Measure: (negation_flips) / (utterances_with_negation). Alert: >5%, indicates interim results dangerously misleading.
3. **premature_action_error_rate**: Target: 0 (zero tolerance). Measure: (actions_taken_before_final_arrived) / (total_actions). Alert: >0.1%.
4. **transcription_stability_score**: Target: >0.8 (meaning ≤20% revisions per utterance). Measure: (1 - total_revisions / utterance_length). Alert: Rolling 1-hour average <0.7.
5. **final_result_wait_latency_ms**: Target: <800ms median, <1500ms p99 (time from speech end to final result). Measure: (final_result_timestamp - speech_end_timestamp). Alert: P99 >2000ms impacts user experience.

### Alerts
1. **Interim-Based Action Inconsistency** (P1): Condition - Action taken on interim result differs from what would be taken on final result (detected via logging + comparison). Action: Immediate alert, reverse action if possible, contact user, increase interim-to-final stability requirements, require all critical actions wait for final.
2. **Negation Flip Detection** (P1): Condition - Final result contains negation ("don't", "cancel") that wasn't in interim result causing action, OR interim contains negation absent in final. Action: Alert product team, immediately halt interim-triggered actions on negation-sensitive contexts, require confirmation for any cancellation/opt-out intents detected in interim.
3. **Stability Degradation** (P2): Condition - Streaming stability score drops >0.15 points from 7-day baseline in 1-hour window, indicating ASR model regression or systematic acoustic issues. Action: Investigate ASR model changes, check for audio quality degradation, consider reverting recent streaming changes.

---

## References

- [Google Cloud Streaming ASR](https://cloud.google.com/speech-to-text/docs/streaming-recognize) - Interim results handling
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Real-time issues
- [AWS Transcribe Streaming](https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html) - Stability handling
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Timing issues
