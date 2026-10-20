# Chatbot metrics: containment, fallback rate, handoff rate and drop-off, and how each one misleads

This page is for developers and product owners who run a chatbot and read a dashboard with containment, fallback, handoff and drop-off on it. It explains what each number counts, how to compute it from a conversation log, how it can look fine while users fail, and which pattern metrics to read beside it.

> **Status: proposed, 2026-10-20.** Field names are from the [conversation event schema v0.1](../roadmap/specs/conversation-event-schema-v0.1.md), which is a draft not yet checked against labeled conversations. Every field name below is **proposed**. This page gives no "good" values for any metric, because no source we opened gives one that fits your bot. Compare each number with your own trend.

For the 64 outcome measures the diagnosis page and `convocheck --outcomes` compute from transcripts, see [outcome metrics](conversation-outcome-metrics.md).

## How to read this page
- **Definitions** come from vendor documentation and glossaries we opened (listed at the end). Vendors differ, so the page says which one it is quoting.
- **Compute** lines name event fields. Replace them with your own log's names.
- **Pattern IDs** link to pages in this repository that have a metric or a detection signal for the same blind spot. The IDs are listed in the [failure taxonomy](../roadmap/specs/failure-taxonomy-v1.md).
- A pattern's metric is a way to look inside the rate. It is not proof that your bot has that failure.

## 1. Containment rate

**Definition.** The share of bot conversations that end without a handoff to a person. One vendor glossary defines it as the percentage of customer interactions that enter an automated channel and count as contained, and says the exact test for "contained" is a choice you make ([Decagon glossary](https://decagon.ai/glossary/what-is-chatbot-containment-rate), opened 2026-10-20, undated).

**Compute (proposed).**
1. Group events by `conversation_id`.
2. Contained = no event with `event_type = handoff` in the conversation.
3. Containment rate = contained conversations divided by all conversations that reached the bot.

**How it misleads.**
- A user who gives up and closes the window has no handoff event, so the conversation counts as contained. The same Decagon page says that counting every session that ended without escalation "overstates true containment" because it includes frustrated abandonments.
- A user who cannot find the way to a person is contained too. A bot that hides "talk to a human" raises containment.
- A user who got a wrong answer and believed it is contained.

**Counter-metric.** Read it with repeat-contact rate (section 6) and a confirmed-resolution rate: contained conversations where the user confirmed the problem was solved, or where no one came back about the same issue. The Decagon page suggests marking a no-escalation session as provisionally contained, then reclassifying it as unresolved if the same customer contacts again about the same issue within 24 hours. It does not say that 24 hours fits your product.

**Pattern metrics that feed or catch it.**
- [`talk-to-a-human-ignored-or-looped`](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md): human-request fulfillment rate, and abandonment after a request. These show contained conversations that were really blocked exits.
- [`dead-end-i-don-t-understand-replies`](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md): conversations with 3 or more consecutive no-progress turns.
- [`answer-and-go-conversation`](../goals/conversation-leadership/failures/answer-and-go-conversation.md): its table lists a confirmed-resolution rate against the containment rate, and a silent-exit rate. This is the closest match to the counter-metric above.
- [`confident-wrong-answer-with-no-way-to-check`](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): wrong answers stated without any uncertainty or source, from a labeled sample.
- [`no-reply-to-acknowledgments-and-closers`](../goals/response-structure/failures/no-reply-to-acknowledgments-and-closers.md): sessions closed on an unfinished task.

## 2. Fallback (no-match) rate

**Definition.** The share of turns, or of conversations, where the bot did not match what the user said to anything it can handle. Vendors name and count this differently:
- Google Dialogflow CX reports a "No match rate" per page, defined as the "percentage of total conversation turns that resulted in a no-match for the page." ([Dialogflow CX analytics](https://docs.cloud.google.com/dialogflow/cx/docs/concept/analytics), opened 2026-10-20, page shows "Last updated 2026-10-13 UTC").
- Amazon Lex V2 sorts each utterance as Detected or Missed, and marks a conversation failed if it "defaults to the AMAZON.FallbackIntent" ([Lex V2 key definitions](https://docs.aws.amazon.com/lexv2/latest/dg/analytics-key-definitions.html), opened 2026-10-20, undated). That is a conversation-level count, not a turn-level one.

So a turn-based rate and a conversation-based rate are different numbers for the same bot. Say which one you report.

**Compute (proposed).**
1. Turn rate = bot turns with `bot.is_fallback = true` divided by all bot turns.
2. Conversation rate = conversations with at least one `bot.is_fallback = true` turn divided by all conversations.
3. Break either one down by `context.page` or `context.entry_point`.

**How it misleads.**
- A low rate can mean the bot rarely fails, or that it answers everything with something plausible. A bot that guesses never falls back.
- A high rate on one page can be one badly worded menu, not weak language understanding.
- If the fallback message is the same each time, the rate hides how many users saw it repeated.
- A bot that routes every unclear message to a person has a low fallback rate and a high handoff rate. The two move together.

**Counter-metric.** Read it with the repeat-fallback run (how many fallbacks in a row) and wrong-answer rate from a labeled sample.

**Pattern metrics that feed or catch it.**
- [`dead-end-i-don-t-understand-replies`](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md): identical fallback twice in a row, abandonment within 2 turns of a fallback, and fallback-to-new-intent conversion.
- [`guessing-instead-of-asking`](../goals/dialogue-management/failures/guessing-instead-of-asking.md): wrong-guess rate on ambiguous test requests, the guessing side of a low fallback rate.
- [`missing-the-obvious-intent`](../goals/embedded-copilots/failures/missing-the-obvious-intent.md): a match to the wrong intent is not a no-match.

## 3. Handoff (escalation) rate

**Definition.** The share of conversations that move to a person. Dialogflow CX defines an escalation rate as the "percentage of sessions that requested human escalation," and counts "Live Agent Handoff" as conversations where human escalation was requested (same Dialogflow CX page as above). Note the word "requested": the count is of requests, not of users who reached a person.

**Compute (proposed).**
1. Requested = conversations with `user_label.request_for_person = true`, or a bot-side trigger.
2. Completed = conversations with `event_type = handoff` and a `handoff.destination` value.
3. Handoff rate = completed handoffs divided by conversations. Also report requested minus completed.

**How it misleads.**
- A low rate can mean the bot solves a lot, or that users cannot get out. Read it beside the human-request fulfillment rate.
- A high rate can mean the bot defers too much, or that the topics are the kind a person should handle. The rate alone cannot tell you which.
- A completed handoff is not a good handoff. If the person who picks up has no context, the user starts over.

**Counter-metric.** Read it with escalation precision and recall on a labeled sample, and with the re-ask rate after handoff.

**Pattern metrics that feed or catch it.**
- [`escalates-too-early-or-too-late`](../goals/human-handoff/failures/escalates-too-early-or-too-late.md): escalation precision, escalation recall, handoff lateness.
- [`talk-to-a-human-ignored-or-looped`](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md): human-request fulfillment rate, requests needing a second ask.
- [`cold-transfer`](../goals/human-handoff/failures/cold-transfer.md): re-ask rate after handoff, packet present at pickup.
- [`no-channel-switch-or-context-lost`](../goals/channel-selection/failures/no-channel-switch-or-context-lost.md): context lost across a channel switch.
- [`no-de-escalation-strategy`](../goals/difficult-customers/failures/no-de-escalation-strategy.md): handoff after 3 or more negative turns.

## 4. Drop-off (abandonment) rate

**Definition.** The share of conversations where the user stops responding before the task or the bot's own flow ends. Amazon Lex V2 calls a conversation Dropped when "the customer doesn't respond before the conversation is categorized as a success or failed," and uses the same word for intents and slots (Lex V2 page above). Dialogflow CX has an "End Interaction" category for conversations that were abandoned (Dialogflow CX page above). Neither says why the user stopped.

**Compute (proposed).**
1. Dropped = conversation with no `event_type = session_end` marked as finished and no later `speaker = user` turn within your idle timeout.
2. Locate the last bot turn (`bot.turn_type`) and `turn_index` before the drop. That is the place to look.
3. Optional on web: `web.abandon_after_open` for widgets opened and never used.

**How it misleads.**
- A user who got the answer and left looks the same as a user who gave up. A drop after "your order ships Friday" is success. A drop after "Something went wrong" is not.
- The idle timeout you pick changes the number. Lex ties its definition to a session timeout you set, so two teams can report different drop-off for the same behavior.
- A low drop-off can come from forcing users through a long flow with no exit.

**Counter-metric.** Split drops by the last bot turn type (answer, question, error, fallback, handoff offer). Read drops after an answer as a different group from drops after an error or fallback. Add a one-question exit check or a sampled review to tell success from giving up.

**Pattern metrics that feed or catch it.**
- [`generic-error-messages`](../goals/errors-and-recovery/failures/generic-error-messages.md): error-to-abandon rate (sessions ending within 1 turn of an error).
- [`silent-failure-and-timeout`](../goals/response-time/failures/silent-failure-and-timeout.md): silent-failure rate, and users who reload or leave after a request with no reply.
- [`silent-long-running-work`](../goals/response-time/failures/silent-long-running-work.md): users who leave while work runs with no status.
- [`doesn-t-say-what-it-can-do`](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md): first-task success rate for new users.
- [`generic-first-response`](../goals/embedded-copilots/failures/generic-first-response.md): a stock first message is a place to look for drops right after the first bot turn.
- [`answer-and-go-conversation`](../goals/conversation-leadership/failures/answer-and-go-conversation.md): silent-exit rate (sessions ending on a bot message with no confirmed resolution).

## 5. Handoff and drop-off together: the "exit" view
Containment hides the drop-off group, and handoff rate hides the blocked-exit group. Report one split of all conversations instead of separate rates: finished with confirmed result, finished without confirmation, handed off, dropped. The four groups add to the whole, so a rise in one has to come from another. This is a reading aid we propose, not a vendor standard.

## 6. Repeat-contact rate

**Definition.** The share of users who come back about the same issue within a window. None of the four sources we opened defines a repeat-contact rate on its own page. Two of them describe the same idea from the other side: Decagon reclassifies a no-escalation session as unresolved if the same customer contacts again about the same issue within 24 hours, and Macha says a first-contact-resolution window is "often 24-72 hours" (both linked in sections 1 and 7). The window and the rule for "same issue" are yours to set.

**Compute (proposed).**
1. Key on `user_ref` and an issue label (`user_label.intent`) from the first conversation.
2. A repeat = another conversation by the same `user_ref` with the same intent label inside your window, in any channel you log.
3. Rate = conversations followed by a repeat divided by all conversations. Also use `session.reopened_same_topic` for same-session returns.

**How it misleads.**
- It needs a stable user key. Anonymous chat users who return look new, so the rate reads low.
- Intent labels that are too broad count unrelated issues as repeats. Labels that are too narrow miss real repeats.
- A repeat can mean the first answer failed, or the user wanted something new about the same order.
- It lags: you learn about a bad answer days later.

**Counter-metric.** Read it with the containment rate and a sampled review of the conversations that precede a repeat.

**Pattern metrics that feed or catch it.**
- [`cold-transfer`](../goals/human-handoff/failures/cold-transfer.md): repeats after a handoff show up as re-explaining.
- [`corrections-not-applied`](../goals/dialogue-management/failures/corrections-not-applied.md): corrections still wrong two turns later.
- [`re-asks-for-known-information`](../goals/embedded-copilots/failures/re-asks-for-known-information.md): re-ask rate on known fields.
- [`no-reply-to-acknowledgments-and-closers`](../goals/response-structure/failures/no-reply-to-acknowledgments-and-closers.md): conversations reopened within 5 minutes of a close.

## 7. First-contact resolution (FCR)

**Definition.** The share of issues fully resolved in one interaction with no follow-up, callback, or reopened ticket. One glossary writes it as issues resolved on the first contact divided by total issues, times 100, notes that the same-issue window is "often 24-72 hours" with no single standard, and says teams differ on whether transfers count ([Macha glossary](https://www.getmacha.com/glossary/first-contact-resolution), opened 2026-10-20, undated; the page shows only a copyright year).

**Compute (proposed).**
1. Resolved = conversation ends with a result you can verify (`action.executed` true with `action.record_state_matches_claim` true, or a user-confirmed `session.csat_score` or confirmation turn).
2. No repeat for the same `user_ref` and intent inside your window (section 6).
3. FCR = resolved conversations with no repeat divided by all conversations with an issue.

**How it misleads.**
- It is the mirror of repeat-contact rate only if both use the same window, issue grouping and contact definition.
- "Resolved" is hard to log. Many teams use "no repeat" as the stand-in, so a user who gave up and never returned counts as resolved.
- Whether a transfer to a person counts as first-contact resolution is a choice. Without a stated rule, FCR cannot be compared across teams.

**Counter-metric.** Read it with drop-off split by last bot turn type, and with a sampled human check of "resolved" conversations.

**Pattern metrics that feed or catch it.**
- [`lazy-completion`](../goals/effort-and-memory/failures/lazy-completion.md) (completeness rate) and [`deferring-work-to-the-user`](../goals/effort-and-memory/failures/deferring-work-to-the-user.md) (deferral rate): the bot says done and the work is not.
- [`confident-wrong-answer-with-no-way-to-check`](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): resolved in the log, wrong in fact.
- [`obstructing-cancellation-downgrade-or-refund`](../goals/embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md): cancel requests completed in the conversation.

## Which pattern's metric catches which blind spot

| Headline metric | Blind spot | Pattern ID whose metric catches it | The metric to read |
|---|---|---|---|
| Containment rate | Users who could not reach a person | [`talk-to-a-human-ignored-or-looped`](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) | Human-request fulfillment rate |
| Containment rate | Silent exits counted as contained | [`answer-and-go-conversation`](../goals/conversation-leadership/failures/answer-and-go-conversation.md) | Silent-exit rate, and confirmed resolution against containment |
| Containment rate | Users who gave up after a dead end | [`dead-end-i-don-t-understand-replies`](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) | Conversations with 3 or more consecutive no-progress turns |
| Containment rate | Wrong answers believed | [`confident-wrong-answer-with-no-way-to-check`](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) | Wrong answers stated without any uncertainty or source |
| Fallback rate | Bot guesses instead of falling back | [`guessing-instead-of-asking`](../goals/dialogue-management/failures/guessing-instead-of-asking.md) | Wrong-guess rate on ambiguous test requests |
| Fallback rate | Same fallback repeated | [`dead-end-i-don-t-understand-replies`](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) | Identical fallback twice in a row |
| Handoff rate | Handoffs too early or too late | [`escalates-too-early-or-too-late`](../goals/human-handoff/failures/escalates-too-early-or-too-late.md) | Escalation precision and recall |
| Handoff rate | Handoff without context | [`cold-transfer`](../goals/human-handoff/failures/cold-transfer.md) | Re-ask rate after handoff |
| Drop-off | Quit after an error | [`generic-error-messages`](../goals/errors-and-recovery/failures/generic-error-messages.md) | Error-to-abandon rate |
| Drop-off | Quit during a silent wait | [`silent-failure-and-timeout`](../goals/response-time/failures/silent-failure-and-timeout.md) | Silent-failure rate |
| Drop-off | Quit at the first turn | [`doesn-t-say-what-it-can-do`](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md) | First-task success rate for new users |
| Repeat-contact rate | User repeats facts or corrections | [`corrections-not-applied`](../goals/dialogue-management/failures/corrections-not-applied.md) | Corrections still wrong two turns later |
| First-contact resolution | Bot claims done, work not done | [`lazy-completion`](../goals/effort-and-memory/failures/lazy-completion.md) | Completeness rate |

## How to start
1. **Log the events first.** Per turn: `conversation_id`, `user_ref`, `turn_index`, `speaker`, `event_type`, `bot.is_fallback`. Per conversation end: whether the user or the system closed it.
2. **Write each definition down.** For containment, say whether a drop counts. For FCR and repeat contact, say the window, the "same issue" rule, and whether transfers count. Keep the document with the dashboard.
3. **Add the exit split** from section 5 beside containment, so drop-offs are visible.
4. **Pick two pattern metrics** from the table above that match your biggest headline number, and compute them on a weekly labeled sample.
5. **Read each rate against your own earlier weeks.** Change one thing at a time, and re-read the counter-metric before you call a change an improvement.

## What this page does not show
- No benchmark, target or "good" value for any metric. Several vendor pages we found state benchmarks. We did not use them because we could not check how they were measured.
- No result from running these metrics on a real bot. The pattern metrics are proposed, not calibrated.
- The Decagon and Macha pages are vendor glossaries, not standards. Lex V2 and Dialogflow CX describe their own products only.

## Sources opened (all on 2026-10-20)
- [Amazon Lex V2 key definitions](https://docs.aws.amazon.com/lexv2/latest/dg/analytics-key-definitions.html): conversation, intent and utterance categories. Undated.
- [Dialogflow CX analytics](https://docs.cloud.google.com/dialogflow/cx/docs/concept/analytics): No match rate, escalation rate. Last updated 2026-10-13 UTC.
- [Decagon: chatbot containment rate](https://decagon.ai/glossary/what-is-chatbot-containment-rate): containment definition and the 24-hour reclassification idea. Undated.
- [Macha: first contact resolution](https://www.getmacha.com/glossary/first-contact-resolution): FCR definition and window caution. Undated.
