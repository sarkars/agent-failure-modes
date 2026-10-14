# Roadmap: Response Time Failures

> **Family goal:** Replies arrive at a pace that fits the channel and the user's urgency, and waits are never silent.

**Grounding (verified):** Miller (1968), restated by Nielsen (1993): about 0.1 s feels instant, about 1 s keeps the user's flow of thought, about 10 s is the limit for holding attention. Beyond that, show when it will finish. Feedback matters most when delays vary. Source: [Nielsen Norman Group](https://nngroup.com/articles/response-times-3-important-limits). I found **no verified chat-specific benchmark**, so chat targets below are starting points.

Flags: **V** verified source · **R** needs research · **L** legal review · **E** expert review. See the [roadmap README](README.md).

| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| RT-01 | Slow first response | The user waits with no acknowledgment | First feedback arrives fast enough that the user knows it's working | p90 time to first feedback (token or status). Start: under 1 s for acknowledgment, under 3 s for first content | V, R |
| RT-02 | Silent long-running work | The agent works for 10 s or more with no status | Waits over about 1 s show status, and over about 10 s show progress or an estimate | Share of waits over 10 s with a progress or ETA message. Start: over 95% | V |
| RT-03 | Unpredictable latency | Reply times swing widely, so users can't tell if it's stuck | Delays are predictable, or flagged when unusual | p95 / p50 latency ratio. Start: under 3 (tune) | V |
| RT-04 | Pacing mismatch | Long replies appear instantly and feel canned, or are slowed artificially | Pacing suits reading speed and context without deception | User-rated naturalness; share of replies delayed on purpose (target 0 unless disclosed) | R |
| RT-05 | Deceptive typing indicators | An indicator implies a person typing, or shows while nothing is happening | Indicators reflect real processing, and never imply a human | Indicator accuracy: shown only while processing. Target: 100% | L |
| RT-06 | Silent failure and timeout | The request fails or times out and the user gets nothing, or "something went wrong" | Every failure says what happened and what to do next | Silent-failure rate (target 0); share of error messages with a next step (target 100%) | |
| RT-07 | Queue wait with no ETA | Users wait for a person with no position or estimate | Waits come with an honest estimate and options | Share of queue waits showing an ETA; ETA accuracy within 20%; abandonment during queue | |
| RT-08 | Missed async promises | "We'll reply within 24 hours" by SMS or email isn't met | Promised response times are kept | Promised-time-met rate. Start: over 95% | |
| RT-09 | Session timeout and lost context | The session expires too soon, or a returning user starts from scratch | A user returning after a gap resumes where they left off | Context-resume success rate; timeout-related complaints | |
| RT-10 | Impatient idle nudges | "Are you still there?" arrives too fast, pressuring the user | Nudges respect how long a person reasonably needs to reply | Nudge-then-abandon rate (lower is better) | |
| RT-11 | Urgency-blind pacing | A fraud alert or outage gets the same speed and path as a casual question | Urgent intents get a fast path to action or a person | Time to action or human for urgent intents. Start: under 2 min (tune) | |
| RT-12 | Streaming that rewrites itself | Streamed text changes or contradicts itself as it arrives | Streamed output is stable enough to read | Rate of mid-stream corrections shown to users | |
| RT-13 | Guardrail and hop latency | Each check or agent hop adds seconds | Safety and quality checks fit a latency budget | Share of replies over the latency budget; latency by component | |
| RT-14 | Fast replies, slow resolution | First replies are quick but the user needs many turns and channel switches | Resolution takes little effort, not just quick replies | Customer effort score and turns to resolution. Grounded in Dixon, Freeman & Toman (HBR 2010); critics say it overreaches. Set from baseline | V |
