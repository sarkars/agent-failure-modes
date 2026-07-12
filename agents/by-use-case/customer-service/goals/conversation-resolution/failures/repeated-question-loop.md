# Repeated Question Loop

## Issue: Agent asks for information already provided.

**Frequency**: Occasional

**Symptoms**
- Same slot requested multiple times.
- [Add more specific symptoms]

**Root Cause**
Agent asks for information already provided.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Structured slot-memory store**: maintain an explicit key-value slot store per conversation, rather than relying on the model to re-read raw transcript history, that is checked before generating any information request, since the failure stems from the model failing to reliably extract already-provided values from unstructured conversation history on every turn. Trade-off: requires a reliable slot-extraction step on every user turn, which itself can fail — extraction errors just move the bug upstream.
2. **Pre-question deduplication check**: before emitting any question, check the slot store and conversation history for whether that specific piece of information has already been given, blocking the question if so. Trade-off: adds a validation step and risks false-positive blocking when the user's earlier answer was ambiguous or partial.
3. **Entity extraction at ingestion, not generation time**: extract and persist named entities/slots from each user message as it arrives, not on-demand when the model decides it needs a value, since waiting until generation time is when transcript-reading failures occur. Trade-off: extraction happens even for information that turns out to be irrelevant, adding processing overhead.

### Detection & Response
1. **Same-slot-multiple-requests scanning**: scan transcripts for the agent asking semantically equivalent questions (same slot) more than once in a conversation, the direct signature of this failure. Response: flag for review and check whether the slot store correctly captured the first answer.
2. **User-repetition-frustration detection**: detect user phrases like "I already told you" or the user re-pasting the same answer verbatim, both strong behavioral signals. Response: auto-inject the already-given value into context and suppress the duplicate question in the live conversation if caught in real time.
3. **Slot-store miss-rate audit**: periodically compare slot-store contents against ground-truth manual annotation of a transcript sample to measure how often the extraction pipeline actually failed to persist a provided value. Response: retrain/patch the extraction step for the most common miss patterns.

### Architecture Patterns
1. **Conversation-memory checkpointing**: persist extracted slots as a structured checkpoint updated after every turn and always injected into the next generation call as ground truth, rather than depending on the model's own attention over long raw transcripts to "remember."
2. **Question-generation gated by slot-store lookup**: architect question generation so it can only ask about a slot if a lookup against the slot store returns empty, making "ask for known info" structurally unreachable rather than a prompting-level hope.
3. **Idempotent slot-fill pipeline with conflict resolution**: when a new message appears to update a previously filled slot, route through explicit conflict-resolution logic (confirm which value is current) rather than either blindly overwriting or blindly re-asking.

### Metrics
1. **duplicate_slot_request_rate**: Target: <1% of multi-turn conversations; Alert on >3% weekly
2. **user_already_told_you_phrase_rate**: Target: <2%; Alert on >4%
3. **slot_extraction_miss_rate**: Target: <5% (from audit sampling); Alert on >12%
4. **conversation_length_inflation_from_repeats**: Target: <5% of conversations extended by a repeated question; Alert on >10%

### Alerts
1. **Duplicate Slot Request Spike** (P2): Condition - duplicate_slot_request_rate exceeds 3% over 7 days. Action: audit the slot-extraction pipeline for a recent regression, sample flagged transcripts.
2. **Live "Already Told You" Detected** (P3): Condition - real-time detector matches a user-frustration phrase for repeated info. Action: inject the already-known value into context, suppress the duplicate question for the remainder of the conversation.
3. **Slot Extraction Miss Rate High** (P2): Condition - audit sampling shows slot_extraction_miss_rate exceeds 12%. Action: prioritize the extraction-pipeline fix for the most frequently missed slot types.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
