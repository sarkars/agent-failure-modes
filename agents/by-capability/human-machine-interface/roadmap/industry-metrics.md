# Industry-Specific Metrics for Chatbots and AI Agents

> **Status: first draft, 2026-10-19.** For each industry this file separates three things: **(1) metrics a source I opened actually reports or recommends**, **(2) metrics vendors commonly name** (read through search summaries, not verified), and **(3) metrics I propose**, built from this library's patterns. Proposed metrics are my design, not an industry standard, and none has been validated by a practitioner or run against real data. Insurance, healthcare, and any regulated use need review by someone who works in that field.

## How to read it
- **Opened** = I read the page or abstract on 2026-10-19. **Summary only** = it appeared in a search summary and I did not open it.
- A **proposed** metric always has a definition, the data it needs, and a **counter-metric** that catches the way it can be gamed.
- Each proposed metric links to the pattern it comes from, and so to that pattern's test file.

## What search suggestions say about this topic
I tried about 250 industry-phrased seeds across 20 industries (for example "banking chatbot kpi", "insurance chatbot accuracy") in Google autocomplete and got almost no suggestions back. So industry-metric phrasings are **not** visible search entry points. The general phrasings are ("chatbot kpi metrics", "chatbot evaluation metrics", "chatbot containment rate"). The practical use of this file is therefore as **sections inside the general metrics page**, not as separate pages per industry. See [developer-search-plan.md](seo/developer-search-plan.md).

## 1. Consumer banking and finance
**What I opened:** the CFPB's June 2023 report, *Chatbots in consumer finance*. It says chatbots have a limited ability to solve complex problems, that scripted chatbots can fail to recognize a dispute (for example, "only specific words or syntax may trigger the recognition of a dispute"), that customers can be stuck in "doom loops" with no off-ramp to a human, and that harms include wasted time, inaccurate information, and paying more in junk fees. It does not publish metrics or thresholds.
**Summary only:** a vendor blog arguing that regulator exams focus on factual accuracy, policy consistency, and harm prevention.

| Proposed metric | Definition | Data needed | Counter-metric | Pattern |
|---|---|---|---|---|
| Dispute-recognition recall | Of conversations labeled as the customer raising a dispute or error, the share where the agent starts the dispute path or hands off within 2 turns | A labeled sample of conversations | False dispute-path rate (non-disputes routed there) | [Talk to a human ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md), [When a bot should hand off](../goals/human-handoff/failures/escalates-too-early-or-too-late.md) |
| Fee and payment answer accuracy | Answers about fees and payments that match the current fee schedule, on a test set written from that schedule | The fee schedule and a test set | Refusal rate on fee questions | [Confident wrong answer with no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) |
| Off-ramp turns | Turns from a request for a person to a stated route to one (target: 2 or fewer, the library's starting point) | Conversation logs | Handoffs the customer did not ask for | [Talk to a human ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) |

Law is involved; counsel must review any claim that a metric shows compliance.

## 2. Healthcare triage and symptom checking
**What I opened:** a 2026 medRxiv preprint comparing a government symptom checker with six LLM configurations on 45 vignettes. It reports triage accuracy, emergency sensitivity, under-triage, and critical misses, with the checker at 48.9% accuracy and LLMs at 73.3% to 86.7%, no critical misses across 270 LLM evaluations, and most systems over-triaging self-care cases. It is a preprint on vignettes, not real users. **Summary only:** an earlier JMIR vignette study that I could not open.

| Proposed metric | Definition | Data needed | Counter-metric | Pattern |
|---|---|---|---|---|
| Critical-miss count | Cases in a red-flag vignette set where the agent fails to recommend emergency care (target 0 on the set, a design goal, not a standard) | A clinician-labeled vignette set | Over-triage rate (emergency advice for non-emergencies) | [Missed crisis signals](../goals/vulnerable-users/failures/missed-crisis-signals.md) |
| Emergency sensitivity | Share of true emergencies the agent sends to emergency care | Same set | Over-triage rate | Same |
| Handoff on distress | Share of distress or crisis messages that reach a person or a crisis route | Labeled sample | Needless escalations | Same |

Clinical review is required before any use. These metrics are measures of a design, not clinical validation.

## 3. Retail and e-commerce support
**What I opened:** the τ-bench paper. It scores an agent by comparing the final database state with a goal state, reports `pass^k` (success on all k attempts), and finds that a function-calling GPT-4o agent falls below 25% on `pass^8` in retail. Its failure analysis found wrong arguments and wrong decisions (missing domain rules such as "one exchange per order") among agent failures.

| Proposed metric | Definition | Data needed | Counter-metric | Pattern |
|---|---|---|---|---|
| Wrong-action rate | Refunds, exchanges, or cancellations that the written policy did not allow, divided by all such actions, from an end-state audit | Order database and the policy | Refusal of allowed requests | [Confident wrong answer with no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md), [Corrections not applied](../goals/dialogue-management/failures/corrections-not-applied.md) |
| Consistency (`pass^k`) | The same task repeated k times and succeeding every time | A repeatable task set | Latency and cost of repeated runs | τ-bench definition |
| Confirmed-write rate | State-changing actions preceded by a readback and an explicit yes | Logs | Added turns per task | [Corrections not applied](../goals/dialogue-management/failures/corrections-not-applied.md) |

## 4. Airlines and travel
**Summary only:** a task in the τ-bench airline family (read through a search result, not opened) shows rules such as listing action details and obtaining an explicit "yes" before updating a booking, and one tool call at a time. I did not open it. The Air Canada case on the site shows what a wrong policy answer can cost.

| Proposed metric | Definition | Data needed | Counter-metric | Pattern |
|---|---|---|---|---|
| Policy-statement accuracy | Answers about fare, refund, and change rules that match the current policy document, on a test set from it | Policy documents | Over-hedged answers | [Confident wrong answer with no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) |
| Source-shown rate | Policy answers that show the supporting passage and its date | Logs | Answers padded with citations that do not support the claim | Same |

## 5. Government and public services
**What I opened:** two GOV.UK Chat posts from the Government Digital Service. The 2024 findings said answers did not reach the highest accuracy level, a few cases of hallucination appeared, and some users underestimated the risk because of the brand. The 2026 post lists six evaluation criteria: groundedness, relevance and answer rate, factual accuracy, factual completeness, reliability, and reputational safety. **Summary only:** reported scores (76% to 90% internal benchmarking) and accessibility concerns raised by charities.

| Proposed metric | Definition | Data needed | Counter-metric | Pattern |
|---|---|---|---|---|
| Guessing flagged | Eligibility answers that say the agency decides and name what could change the result | Labeled sample | Over-hedged answers | [Eligibility answers sound like decisions](../goals/government-service-agents/failures/eligibility-answers-sound-like-decisions.md) |
| Path-to-person rate | Eligibility or benefits answers that include the application link and a way to reach a person | Logs | Needless handoffs | Same |
| Accessibility outcome | I found no published accessibility metric for government chat; a candidate is task success for users of assistive tech, measured in testing | Usability tests | n/a | Gap, not yet designed |

Flagged for legal and expert review.

## 6. Telecom
**Summary only (vendor blogs, not opened):** first contact resolution with a validated "resolved" definition (customer did not return about the same issue within 7 to 30 days), repeat-contact rate, and counting a chat-to-phone move as one failed contact. Vendor claims about churn and billing disputes were not verified.

| Proposed metric | Definition | Data needed | Counter-metric | Pattern |
|---|---|---|---|---|
| Cross-channel repeat rate | Customers who contact again on the same issue in another channel within a fixed window | Customer and issue identifiers across channels | Contacts merged wrongly | [No channel switch or context lost](../goals/channel-selection/failures/no-channel-switch-or-context-lost.md), [Cold transfer](../goals/human-handoff/failures/cold-transfer.md) |
| Re-ask rate after handoff | Handoffs where the person asks for something already given | Labeled sample | Time added by summaries | [Cold transfer](../goals/human-handoff/failures/cold-transfer.md) |

## 7. Insurance
**Summary only:** vendor pages list CSAT, first response time, channel deflection, and after-hours resolution; they describe straight-through processing and first-notice-of-loss accuracy qualitatively and give no standard definitions. One source cites a J.D. Power claims study (average 44 days to final payment after first notice for property claims), which I did not open.

| Proposed metric | Definition | Data needed | Counter-metric | Pattern |
|---|---|---|---|---|
| Urgent-case escalation recall | Share of urgent claims (for example an injury) that reach a person quickly | Labeled sample | Needless escalations | [When a bot should hand off](../goals/human-handoff/failures/escalates-too-early-or-too-late.md) |
| Intake field accuracy | Fields captured at intake that match an adjuster-reviewed record | Adjuster review sample | Intake time | [Corrections not applied](../goals/dialogue-management/failures/corrections-not-applied.md) |

Needs review by someone in claims before use; these definitions are mine.

## 8. Developer and SaaS support
**Summary only:** vendor posts argue that deflection alone is weak and should be paired with resolution quality, repeat contact, and satisfaction. They quote hallucination-rate figures (under 1%; under 5%) without independent sources, so I do not use them. **Opened:** the GOV.UK criteria above (groundedness, completeness) apply equally here, and the citation audit by Liu et al. (51.5% of sentences fully supported; 74.5% of citations support their sentence) is a documented reference point.

| Proposed metric | Definition | Data needed | Counter-metric | Pattern |
|---|---|---|---|---|
| Confirmed-resolution rate | Conversations where the user confirmed the problem is solved, or did not return on the same issue within a window | Logs and a confirmation prompt | Survey fatigue | [The answer-and-go conversation](../goals/conversation-leadership/failures/answer-and-go-conversation.md) |
| Citation support rate | Shown sources that support the claim they are attached to | Human or judge review | Review cost | [Confident wrong answer with no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) |
| Containment gap | Containment rate minus confirmed-resolution rate | Both measures | None; the gap is the signal | [The answer-and-go conversation](../goals/conversation-leadership/failures/answer-and-go-conversation.md) |

## 9. Food service and drive-thru (voice ordering)
**Opened:** Restaurant Business on McDonald's ending its test; The Drive's report of an 86% Wendy's accuracy figure (secondary; not verified). No independent accuracy audit found.

| Proposed metric | Definition | Data needed | Counter-metric | Pattern |
|---|---|---|---|---|
| Order accuracy at pickup | Orders handed over that match what was said, from a sample | Audio, entered order, handover check | Order time | [Order mix-ups at the speaker](../goals/drive-thru-agents/failures/order-mix-ups-at-the-speaker.md) |
| Adds after stop | Items added after the customer said stop or no | Order event log | None (target 0) | Same |
| Correction success | Corrections that end with the right value in the final order | Labeled sample | Added call time | [Repair failure](../goals/voice/failures/repair-failure.md) |

## What would make these real
1. **A practitioner review per industry,** especially insurance, healthcare, and banking.
2. **A real data run:** each metric needs a labeled sample from a real deployment; none has been computed.
3. **Sources for benchmarks:** this file gives no target values except the library's starting points. Vendor benchmark ranges should only be quoted once the source is opened.

## Related
- [Developer search plan](seo/developer-search-plan.md) · [L0 base spec](l0-base-spec.md) · [Agent-type gap analysis](agent-type-gap-analysis.md) · [Content program](content-program.md)
