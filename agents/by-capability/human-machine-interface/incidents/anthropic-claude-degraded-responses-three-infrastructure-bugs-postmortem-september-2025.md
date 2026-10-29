---
title: "Three Infrastructure Bugs Quietly Degrade Claude's Answers for Weeks"
date: 2025-09-17
source: "https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues"
summary: "Between August and early September 2025, users of Claude and Claude Code reported worse answers. On September 17, 2025, Anthropic published a postmortem naming three overlapping infrastructure bugs: misrouted requests, a TPU misconfiguration that produced stray tokens, and a compiler bug in token selection. It said its evaluations did not capture what users reported. Status: Needs review."
categories:
  - Trust
  - Accuracy
  - Model and Prompt Changes
patterns:
  - tone-changes-shipped-with-no-regression-test
  - clean-lab-testing
  - no-way-to-report-bad-behaviour
  - reviewing-only-failures
---

**This page is a dated teardown of one public incident, for teams that ship a chat or coding assistant on a model they serve or buy, and need to know when its answers quietly get worse.** Every fact below comes from a source we opened (listed at the end). Where sources disagree on dates, we say so. Spot an error? See "Corrections" at the end.

**Status: Needs review.** All sources were opened on 2026-10-30. All six were then re-read as raw page text, and every quote and number below was matched against that text.

## What happened (as reported)

- **August 5, 2025.** Per Anthropic's postmortem (September 17), some Sonnet 4 requests were "misrouted to servers configured for the upcoming 1M token context window." This first affected 0.8% of requests.
- **August 25-26, 2025.** Two more deployments went out. One was a TPU server misconfiguration that "caused an error during token generation." The other changed how Claude selects tokens and triggered "a latent bug in the XLA:TPU compiler," confirmed for Claude Haiku 3.5.
- **August 29, 2025.** A "routine load balancing change" sent more short-context requests to the wrong servers. At the worst hour, on August 31, 16% of Sonnet 4 requests were affected.
- **August 30, 2025.** Simon Willison relayed an Anthropic status note: Opus 4.1 quality dropped for some requests from 17:30 UTC on August 25 to 02:00 UTC on August 28, caused by "a rollout of our inference stack."
- **September 9, 2025.** The Decoder reported weeks of complaints on Reddit, X and YouTube. The same day, Anthropic's status page listed two resolved bugs and an open check on Opus 4.1.
- **September 12, 2025.** The status page said root causes were found and "mitigations for each" were deployed, and added Opus 3 to the second issue.
- **September 17, 2025.** Anthropic published the postmortem, and the status incident was marked resolved.

## What the user saw

- **Stray characters and broken code.** The output bug was "producing Thai or Chinese characters in response to English prompts," or obvious syntax errors in code (postmortem).
- **A coding agent that seemed less careful.** The Decoder quotes a Reddit user saying Claude "ignored its own plan and messed up the code," and others saying it would "lie about the changes it made to code."
- **Lower intelligence, malformed replies, tool-call problems.** These are the symptoms the August status note listed for Claude Code (via Willison).
- **Bad luck that stuck.** The postmortem says once a request hit the wrong server, "subsequent follow-ups were likely" to go the same way. It says about 30% of Claude Code users who made requests in the period had at least one message misrouted.
- **No way to tell.** Nothing in the reply told the user which server or setting had served it. The user could only compare against memory of better answers.

## What the company said

- On load: "We never reduce model quality due to demand, time of day, or server load" (postmortem).
- On detection: "The evaluations we ran simply didn't capture the degradation users were reporting," partly because "Claude often recovers well from isolated mistakes."
- On user data: privacy controls "limit how and when engineers can access user interactions," which kept engineers from examining the problem chats.
- On linking reports to changes: it had reports but "lacked a clear way to connect these to each of our recent changes." Each bug showed different symptoms on different platforms at different rates.
- Changes it lists: evaluations that "more reliably differentiate between working and broken implementations," run "continuously on true production systems"; detection tests for unexpected character output in deployment; a switch from approximate to exact top-k; and tooling to debug community feedback without giving up privacy. It asks users to report via `/bug` in Claude Code or the thumbs-down button.
- InfoQ (October 3, 2025) quotes Todd Underwood, Anthropic's head of reliability: "It's been a rough summer for us, reliability wise."

## Where in the flow it broke

The chat layer itself was not changed. The break was underneath it, in serving, and three things failed to catch it:

1. **Release checks did not tell broken from working.** The postmortem says validation relied on benchmarks, safety evaluations, performance metrics, spot checks and small "canary" groups. None flagged the bugs.
2. **Tests ran in a cleaner place than production.** The routing bug grew only after a load-balancing change, and the fix the company names is running evaluations on true production systems.
3. **User reports arrived but could not be acted on.** Reports started, per the postmortem, in early August. Engineers could not easily read the chats, and could not tie a report to a deployment. The investigation opened in late August.

## Pattern match

- [Tone changes shipped with no regression test](../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md) — **good fit.** Same mechanism: a change ships, and no fixed before-and-after check catches what users then notice. Here the change was infrastructure, not a prompt, and the drop was in quality, not tone.
- [Clean-lab testing](../goals/measurement-and-feedback/failures/clean-lab-testing.md) — **partial fit.** Tests looked fine while production failed. The library page is about clean versus messy user messages; here the gap was test setup versus live routing and hardware.
- [No way to report bad behaviour](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md) — **partial fit.** Report buttons existed, so this is not the core failure. But reports could not be read or linked to a cause, which is close to a thumbs-down that "goes to no one."
- [Reviewing only failures](../goals/measurement-and-feedback/failures/reviewing-only-failures.md) — **partial fit.** Claude "often recovers well from isolated mistakes," so many bad turns drew no complaint. A review that waits for complaints misses those turns.
- [Outage updates generic or late](../goals/travel-and-utility-agents/failures/outage-updates-generic-or-late.md) — **partial, mostly a counterexample.** The September 9 status note named models, date ranges and a next update time. It is not listed in the front matter.

Not matched: [Silent sandbagging](../goals/refusals-and-boundaries/failures/silent-sandbagging.md) (no source says the model chose to give less) and [Lazy completion](../goals/effort-and-memory/failures/lazy-completion.md) (no source shows partial work left with placeholders).

**Possible gaps for a person to review.** No library page covers (a) a serving or model change that lowers answer quality with no sign to the user, or (b) one bad route that sticks to a user's whole session. Candidate IDs, not yet in the taxonomy: `silent-serving-quality-regression`, `sticky-degraded-session`.

## What to measure

Proposed metrics; none come from Anthropic. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Wrong-script rate | Share of replies to English prompts that contain characters from an unrelated script (for example Thai or Han), per model and serving pool |
| Code that does not parse | Share of code blocks in replies that fail a parser for their stated language, per deployment |
| Fixed-set score before and after each deploy | Same prompt set, scored on the live path before and after each serving change |
| Quality reports per deployment | Thumbs-down and `/bug` reports per 1,000 requests, grouped by the deploy that served them |
| Sticky bad sessions | Share of sessions where two or more turns hit the same flagged server or config |
| Time from first report to linked cause | Hours from the first matching user report to a named deployment |

## What a team can change

Proposed rules, each a pass/fail check. Status: Not yet run.

1. **Gate every serving change, not just model changes.** Routing, sampling, compiler and hardware changes run the same fixed prompt set on the live path. Check: a deploy record has a before and after score.
2. **Test on production, continuously.** Send fixed probe prompts through real load balancers every hour. Check: a probe log exists per serving pool per hour.
3. **Tag every reply with what served it.** Log model version, serving pool and config hash per turn, so a report can be linked to a deploy. Check: no logged turn is missing the tag.
4. **Make a report carry its own evidence.** When a user flags a reply, ask to attach that turn with consent. Check: share of reports with an attached turn.
5. **Watch report rates by deploy.** Alert when reports per 1,000 requests for one deploy exceed the prior week's rate by a threshold you set. Check: an alert fires on a replayed spike.
6. **Don't over-correct.** Not every "it got dumber" post is a bug; Willison notes such complaints often prove unfounded. Pair report alerts with the fixed-set score before rolling back.

## Where sources disagree

- **When reports began.** The postmortem says early August; The Decoder says complaints piled up mainly from late August.
- **Bug dates.** The status page (September 9) gives the second issue as August 26 to September 5. The postmortem dates the token-selection change to August 25, a sampling rewrite to August 26, and the Haiku 3.5 rollback to September 4. The status page ends the routing bug on September 4; the postmortem says the fix was deployed September 4 and rollout finished by September 16 (first-party, Vertex AI) and September 18 (Bedrock).

## What we could not verify

- Search summaries mention Gigazine, implicator.ai and a Substack post; we did not open them and use nothing from them.
- How many users saw bad replies overall. The postmortem gives shares per bug and platform, not a total.
- Reports that problems continued after the fixes appeared only in search summaries; we make no claim about them.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues | Anthropic | 2025-09-17 | Yes, 2026-10-30 (raw text) |
| https://status.claude.com/incidents/72f99lh1cj2c | Anthropic status page | 2025-09-09 to 2025-09-17 | Yes, 2026-10-30 (raw text) |
| https://the-decoder.com/anthropic-confirms-technical-bugs-after-weeks-of-complaints-about-declining-claude-code-quality/ | The Decoder (Maximilian Schreiner) | 2025-09-09 | Yes, 2026-10-30 (raw text) |
| https://simonwillison.net/2025/Aug/30/claude-degraded-quality/ | Simon Willison's Weblog | 2025-08-30 | Yes, 2026-10-30 (raw text) |
| https://simonwillison.net/2025/Sep/17/anthropic-postmortem/ | Simon Willison's Weblog | 2025-09-17 | Yes, 2026-10-30 (raw text) |
| https://www.infoq.com/news/2025/10/anthropic-infrastructure-bugs/ | InfoQ (Renato Losio) | 2025-10-03 | Yes, 2026-10-30 (raw text) |

## Corrections

If you have the raw postmortem text, a more exact timeline, or a dated user report from early August, tell us and we will fix this page.
