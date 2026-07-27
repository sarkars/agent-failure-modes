# Repetitive Degenerate Generation

## Issue: A single generation call falls into repeated phrases, loops, or degenerate text (distinct from repeating tool-call actions across turns) because no repetition/frequency penalty or diversity control is applied to open-ended output.

**Frequency**: Occasional

**Symptoms**
- A single response contains the same phrase, sentence, or clause repeated multiple times within one generation, rather than across separate turns
- Long-form outputs (summaries, reports, stories) devolve into a short loop of near-identical sentences toward the end of the generation, especially near the token/length limit
- Streaming output visibly gets "stuck" reiterating a list item, transition phrase, or filler clause several times before eventually continuing or truncating
- Automated repetition-detection metrics (n-gram repetition rate, distinct-n) spike on a subset of outputs while human spot checks confirm the text reads as genuinely degenerate rather than intentionally repetitive (e.g., a refrain)
- Truncated/cut-off responses at the max-token boundary disproportionately show repeated content in the last portion of the output compared to the first portion

**Root Cause**
A single generation call falls into repeated phrases, loops, or degenerate text because no repetition/frequency penalty or diversity control is applied to open-ended output.

**Example**
```
A meeting-notes-summarization agent for a video-conferencing product generates a long-form
summary of a 90-minute cross-team planning call, invoked with default decoding settings and no
repetition penalty because the team assumed the summarization prompt's structure would keep
output naturally bounded. For calls with a large number of near-duplicate discussion points
(the same action item restated by different speakers), the generation loop latches onto a
phrasing pattern and produces a summary whose final third repeats a near-identical sentence
("The team agreed to revisit the timeline next week.") six times with only minor wording
variation, instead of consolidating the point once. The summary is auto-emailed to all call
participants. Several recipients reply-all asking if the notes are broken, and the team has to
manually regenerate and re-send corrected notes for that call, damaging confidence in the
auto-generated notes feature enough that adoption drops for the following two weeks.
```

**Contributing Factors**
- No repetition/frequency penalty configured for long, open-ended generation tasks (long-form writing, extended summaries)
- Sampling temperature is set very low (near-greedy decoding) for perceived consistency/determinism, which increases susceptibility to repetition loops in exactly the open-ended, long-output tasks where diversity controls matter most
- No max-length or repetition-aware early-stopping check runs on the output before it's returned, so a loop that starts near the token limit ships uncaught
- Repetition is more likely on inputs with redundant source content (multiple speakers restating the same point, or a source document with duplicated sections), which biases the model's next-token distribution toward echoing what it just generated

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Redundant-source long-form generation | A long source document/transcript with deliberately duplicated or near-duplicate sections | Output consolidates redundant content without verbatim sentence repetition | Same sentence/clause appears 3+ times near-verbatim in a single output |
| Near-max-length generation stress test | A prompt designed to push generation close to the max-token limit | Output remains non-repetitive up to truncation | Repetition rate rises measurably in the final portion of the output vs. the first portion |
| Low-temperature long-output regression | Long-form generation request at the production default temperature/sampling settings | Distinct-n-gram ratio stays within normal range | Distinct-n-gram ratio drops sharply compared to short-output baseline, indicating loop-prone decoding settings |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| N-gram repetition rate (e.g., 4-gram repetition) | <2% of generated outputs flagged above threshold | Compute repeated n-gram fraction per output on a rolling production sample |
| Distinct-n ratio (distinct-4) | >=0.85 on long-form outputs | Measure ratio of distinct 4-grams to total 4-grams per output, tracked by output-length bucket |
| Repetition-triggered regeneration rate | <1% of long-form generations require an automatic retry due to detected repetition | Track how often the repetition-detection guard fires and triggers regeneration |

---

## Mitigation Strategies

### Prevention
1. **Repetition/frequency penalty tuning by task type**: Configure a repetition or frequency penalty (and/or presence penalty) specifically for long, open-ended generation tasks, tuned separately from short-form or structured-output tasks where the default settings were chosen.
2. **Diversity-aware decoding for long-form tasks**: Use decoding strategies suited to open-ended long-form generation (nucleus/top-p sampling with a non-trivial temperature, or locally typical sampling) rather than near-greedy decoding, specifically for tasks known to run long.
3. **Redundant-input pre-consolidation**: For inputs known to contain redundant content (multi-speaker transcripts, documents with duplicate sections), de-duplicate or summarize redundancy in the input before generation to reduce the model's exposure to the pattern that triggers repetition loops.

### Detection & Response
1. **Post-generation repetition scan and auto-regenerate**: Run an n-gram repetition check on every long-form output before returning it; if the score exceeds threshold, automatically regenerate with adjusted sampling parameters (higher penalty/temperature) rather than shipping the degenerate output.
2. **Streaming repetition circuit breaker**: For streamed generation, detect an in-progress repetition loop (same n-gram recurring within a short token window) and abort/restart the generation early rather than letting it run to the token limit.

### Architecture Patterns
1. **Repetition-gated output pipeline**: A post-generation guard stage that scores repetition before an output is accepted, with automatic regeneration on failure, analogous to a deterministic linter for decoding-level quality.
2. **Length-aware sampling schedule**: Decoding parameters (penalty strength, temperature) that adapt based on target output length, since repetition risk rises with generation length.
3. **Redundancy-normalizing input preprocessor**: A preprocessing stage that collapses near-duplicate source content before it reaches the generation prompt, reducing the surface area for the model to loop on.

### Metrics
1. **ngram_repetition_rate**: Target: <2%; Alert threshold: >8%
2. **distinct_4gram_ratio**: Target: >=0.85; Alert threshold: <0.65
3. **repetition_triggered_regeneration_rate**: Target: <1%; Alert threshold: >5%

### Alerts
1. **Repetition Rate Spike** (P3 - Info): Condition - n-gram repetition rate across a rolling sample of long-form outputs exceeds 8%. Action: review recent decoding-parameter or prompt changes and check whether penalty settings regressed.
2. **Distinct-N Ratio Drop** (P3 - Info): Condition - distinct-4gram ratio on long-form outputs falls below 0.65. Action: investigate the affected task type's sampling configuration and consider tightening penalties.
3. **Regeneration Rate Elevated** (P2 - Warning): Condition - automatic repetition-triggered regeneration rate exceeds 5% of long-form generations in a day. Action: treat as a systemic decoding-config issue rather than isolated cases; escalate for a sampling-parameter review.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| N-gram repetition rate (long-form outputs) | >8% |
| Distinct-4gram ratio | <0.65 |
| Repetition-triggered regeneration rate | >5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Repetition rate elevated | Rolling repetition rate exceeds 8% on long-form outputs | Low |
| Distinct-n ratio degraded | Distinct-4gram ratio drops below 0.65 | Low |
| Regeneration rate elevated | Auto-regeneration due to repetition exceeds 5%/day | Medium |

---

## Related Patterns

- [Step Repetition](../../../../operations/goals/cost-efficiency/failures/step-repetition.md) - the distinct multi-turn action/tool-call repetition failure; this pattern is repetition within a single generation's text output, a decoding-level issue rather than a state-tracking one
- [Verbose Reasoning](../../../../operations/goals/cost-efficiency/failures/verbose-reasoning.md) - a related but distinct output-bloat failure (excessive length without necessarily repeating content verbatim)

## References

- [Decoding Strategies: How LLMs Choose The Next Word](https://www.assemblyai.com/blog/decoding-strategies-how-llms-choose-the-next-word) - repetition penalty, temperature, top-k, and top-p as decoding-level controls over degenerate/repetitive output
- [Advancing Decoding Strategies: Enhancements in Locally Typical Sampling for LLMs](https://arxiv.org/pdf/2506.05387) - locally typical sampling as a technique balancing diversity and coherence to avoid degenerate repetition
