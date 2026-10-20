# How to tell whether your chatbot's conversations worked: outcome metrics

This page is for people who run a chatbot and can see *what* went wrong in single conversations but not *how often* things work out across many. It lists every outcome measure in the [diagnosis page](https://claude.ai/artifact/DEYPK87Pp9rmq1LWhcar6m) and the `convocheck --outcomes` command: the question each one answers, how it is measured, what it needs, and how it can mislead.

> **Status: proposed, 2026-10-20.** Every measure here matches phrases and turn order. None is calibrated against labeled conversations, and this page gives no "good" values. Compare each number with your own trend, and read it beside the measures next to it. The vendor definitions of containment, fallback, handoff and drop-off are in [Chatbot metrics](metrics.md).

## The problem

A chatbot can pass every per-message check and still fail people: it answers, but the user leaves; it hands over to a person, but only after the third ask; it repeats a card number back into the chat log. These failures show up only when you count across conversations. That is what outcome metrics do.

## How to get them

- **On the page:** paste one or more conversations in step 3, with a line of `---` between them. The results start with "How the conversations turned out".
- **From the command line:** `convocheck chats.jsonl --outcomes` (add `--json` for machine-readable output). A file can hold one conversation, `{"conversations": [...]}`, a list of conversations, or one conversation per line.
- **Roles:** `user`, `assistant`, and a person who takes over as `human_agent` (or `live_agent`, `staff`, `operator`, `representative`). On the page, start those lines with `Human agent:`, `Staff:` or `Rep:`.
- **Speed:** add `time` to each turn. **Satisfaction:** add `"meta": {"csat": 4}` to each conversation.

There are 64 measures in 9 groups. Each rate says what it is out of, because some apply only to some conversations (for example, missed handover is out of the conversations where someone asked for a person).

## Did it work?

**How these can mislead.** Users rarely say "that worked", so confirmed resolution undercounts real fixes; read it as a floor, not a rate. Drop-off can't tell a user who left happy without saying so from one who gave up. A conversation counts as contained even when the user quit, which is why "resolved without a person" sits beside containment.

### Confirmed resolution rate

*How often does the user say it worked?*

- **What counts:** User confirms ("that worked", "thanks, sorted") and nothing later says it is still broken.
- **Needs:** Measured from the transcript alone.
- **Better when:** higher.
- **Read more:** [answer and go conversation](../goals/conversation-leadership/failures/answer-and-go-conversation.md)

### False resolution rate

*How often does the bot say it's fixed when it isn't?*

- **What counts:** Bot claims a fix ("you're all set"), then the user says it still doesn't work.
- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [confident wrong answer with no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)

### Task completion rate

*How often does the bot finish the job (booked, cancelled, refunded, submitted)?*

- **What counts:** A bot turn confirms a completed action, such as a confirmation or reference number.
- **Needs:** Measured from the transcript alone.
- **Better when:** higher.

### Containment rate

*How often does the conversation end without a person?*

- **What counts:** Read it with confirmed resolution: a user who gives up is also "contained".
- **Needs:** Measured from the transcript alone.
- **Read more:** [metrics](metrics.md)

### Resolved without a person

*How often does the bot solve it alone, confirmed by the user?*

- **What counts:** Contained and confirmed resolved.
- **Needs:** Measured from the transcript alone.
- **Better when:** higher.
- **Read more:** [metrics](metrics.md)

### Positive ending rate

*How often does the user's last message sound satisfied?*

- **Needs:** Measured from the transcript alone.
- **Better when:** higher.

### Negative ending rate

*How often does the user leave annoyed?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.

### Drop-off rate

*How often does the user stop replying mid-task?*

- **What counts:** Ends on an unanswered bot question, a fallback, an error, or the user's negative message.
- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [metrics](metrics.md)

### Where users drop off

*After which kind of bot reply do users leave?*

- **What counts:** Split by the last bot reply: question, fallback, error, handoff offer or answer.
- **Needs:** Measured from the transcript alone.
- **Read more:** [metrics](metrics.md)

### Silent failure rate

*How often does the user's last message get no reply, or an empty one?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [silent failure and timeout](../goals/response-time/failures/silent-failure-and-timeout.md)

### Error reply rate

*How often does the bot show a technical error?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [generic error messages](../goals/errors-and-recovery/failures/generic-error-messages.md)

## Handing over to a person

**How these can mislead.** "Early" means the bot handed over on its very first reply with no request, no frustration and no high-stakes words; some of those are correct routing. "Late" counts two or more asks, two or more fallbacks or repeated frustration before the handover, so a handover that comes after one failed attempt still counts as on time. The phrase lists for high-stakes topics (fraud, a stolen card, a medical emergency) are short and will miss many.

### Human request rate

*How often do users ask for a person?*

- **Needs:** Measured from the transcript alone.
- **Read more:** [talk to a human ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md)

### Handover rate

*How often does the bot hand over to a person?*

- **Needs:** Measured from the transcript alone.
- **Read more:** [metrics](metrics.md)

### Request fulfilment rate

*When users ask for a person, how often do they get one?*

- **Needs:** Measured from the transcript alone.
- **Better when:** higher.
- **Read more:** [talk to a human ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md)

### Missed handover rate

*How often is a request for a person ignored?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [talk to a human ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md)

### Late handover rate

*How often does the handover come only after repeated asks, repeated fallbacks or rising frustration?*

- **What counts:** Late: 2+ requests, 2+ fallbacks, or 2+ frustration signals before the handover.
- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [escalates too early or too late](../goals/human-handoff/failures/escalates-too-early-or-too-late.md)

### Possibly early handover rate

*How often does the bot hand over on its first reply, before trying?*

- **What counts:** First bot reply hands over, and the user had not asked for a person, shown frustration, or raised a high-stakes issue.
- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [escalates too early or too late](../goals/human-handoff/failures/escalates-too-early-or-too-late.md)

### High-stakes issue kept by the bot

*How often does an urgent or high-stakes issue (fraud, emergency, bereavement) stay with the bot?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [escalates too early or too late](../goals/human-handoff/failures/escalates-too-early-or-too-late.md)

### Requests needing a second ask

*How often must users ask for a person twice or more?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [talk to a human ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md)

### Bot talks after a person joins

*How often does the bot keep replying after a person took over?*

- **What counts:** Needs transcripts that mark the person's turns (role "human_agent", or lines starting "Human agent:").
- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [bot keeps replying after a person joins](../goals/human-handoff/failures/bot-keeps-replying-after-a-person-joins.md)

### Handover summary quality

*Does the person who takes over get an accurate summary?*

- **Needs:** Needs an AI judge or a person to read the conversation; not measured yet.
- **Better when:** higher.
- **Read more:** [handoff summary is wrong or misleading](../goals/human-handoff/failures/handoff-summary-is-wrong-or-misleading.md)

### Time to reach a person

*How long from the request to a person replying?*

- **Needs:** Needs a time on each turn (`time` or `timestamp`, ISO 8601).
- **Better when:** lower.

## Coverage and missed queries

**How these can mislead.** A user message counts as missed when the next bot reply is a fallback ("I didn't get that") or says the topic is out of scope. A confident wrong answer is not a fallback, so coverage can look high while users are misled. Read the missed-queries list itself: it is your list of content gaps.

### Coverage

*What share of user messages does the bot handle without a fallback or "I can't help with that"?*

- **Needs:** Measured from the transcript alone.
- **Better when:** higher.
- **Read more:** [metrics](metrics.md)

### Fallback rate (per reply)

*What share of bot replies are "I didn't understand"?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [metrics](metrics.md)

### Fallback rate (per conversation)

*What share of conversations hit at least one fallback?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [metrics](metrics.md)

### Fallback loops

*How often does the bot say "I didn't understand" twice in a row?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [dead end i don t understand replies](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md)

### Out-of-scope rate

*How often does the bot say a topic is outside what it can do?*

- **Needs:** Measured from the transcript alone.
- **Read more:** [doesn t say what it can do](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md)

### Missed queries

*Which user messages did the bot fail to handle? (your content gaps)*

- **What counts:** Listed word for word, most frequent first.
- **Needs:** Measured from the transcript alone.
- **Read more:** [metrics](metrics.md)

### Rephrase rate

*How often do users repeat or reword the same message?*

- **What counts:** Two user messages in a row that share at least half their words.
- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [repair failure](../goals/voice/failures/repair-failure.md)

### Bot re-asks for known information

*How often does the bot ask for the same detail twice (order number, email)?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [re asks for known information](../goals/embedded-copilots/failures/re-asks-for-known-information.md)

### Partial answers

*Does the bot answer every part of multi-part questions?*

- **Needs:** Needs an AI judge or a person to read the conversation; not measured yet.
- **Better when:** higher.
- **Read more:** [partial answers to multi part questions](../goals/effort-and-memory/failures/partial-answers-to-multi-part-questions.md)

### Wrong-answer rate

*How often is the answer factually wrong?*

- **What counts:** Needs a labeled sample or an AI judge with your knowledge base.
- **Needs:** Needs an AI judge or a person to read the conversation; not measured yet.
- **Better when:** lower.
- **Read more:** [confident wrong answer with no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)

## Effort and frustration

**How these can mislead.** Frustration is detected from words ("useless", "third time"), capitals, swearing and "!!". Polite users who are frustrated are missed, and some users write in capitals by habit. A long conversation can be a good one, for example a guided setup.

### Turns per conversation

*How many messages does it take?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.

### User effort (words typed)

*How much do users have to type?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.

### Frustration rate

*How often do users show frustration (capitals, swearing, "useless", "third time")?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [no de escalation strategy](../goals/difficult-customers/failures/no-de-escalation-strategy.md)

### Frustration rising

*How often does frustration appear only in the second half (the bot made it worse)?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.

### Bot reply length

*How long are the bot's replies on average?*

- **Needs:** Measured from the transcript alone.
- **Read more:** [length mismatch with the user s effort](../goals/response-structure/failures/length-mismatch-with-the-user-s-effort.md)

### Excess apology rate

*How often does the bot apologize 3 or more times?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.

### Satisfaction by outcome

*Are satisfaction scores different for resolved, dropped and handed-over chats?*

- **What counts:** Add "csat" (1-5) to each conversation's meta to compute it.
- **Needs:** Needs your own data joined to the conversation, such as a satisfaction score in `meta`.
- **Better when:** higher.
- **Read more:** [survey bias](../goals/measurement-and-feedback/failures/survey-bias.md)

## Privacy, safety and trust

**How these can mislead.** Personal data is matched by pattern: card numbers pass a Luhn check, phone numbers and emails by shape, passwords by a "password is" cue. Expect some misses and false alarms. Only cards, US SSNs, IBANs and passwords count as sensitive, so a bot that repeats an email address back is not counted as exposing data. "Honest about being AI" only counts conversations where the user asked.

### Personal data shared by users

*How often do users paste emails, phone numbers, card numbers or IDs into chat?*

- **Needs:** Measured from the transcript alone.
- **Read more:** [sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md)

### Personal data exposed by the bot

*How often does the bot repeat back a card number, ID or other personal data?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md)

### Sensitive data requested in chat

*How often does the bot ask for a card number, password, PIN or one-time code in chat?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md)

### Sensitive data shared with no warning

*When a user pastes a card number, ID or password, how often does the bot carry on without warning them?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md)

### Crisis signals missed

*How often does a crisis signal get no crisis resource?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [missed crisis signals](../goals/vulnerable-users/failures/missed-crisis-signals.md)

### Children treated as adults

*How often is a likely child asked for personal data or a purchase?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [child user treated as adult](../goals/age-adaptation/failures/child-user-treated-as-adult.md)

### Honest about being AI

*When users ask "are you a bot?", how often does the bot say clearly that it is?*

- **What counts:** Counts denied (claims to be human) and dodged (no clear answer) separately.
- **Needs:** Measured from the transcript alone.
- **Better when:** higher.
- **Read more:** [undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md)

### Prompt injection attempts

*How often do users try to override the bot's instructions?*

- **Needs:** Measured from the transcript alone.

### Possible instruction leaks

*How often does the bot talk about its own instructions or system prompt?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.

### Promises to audit

*How often does the bot promise refunds, guarantees or discounts that someone should check?*

- **Needs:** Measured from the transcript alone.
- **Read more:** [no follow through](../goals/trust-and-rapport/failures/no-follow-through.md)

## Sales and cancellations

**How these can mislead.** An upsell after a complaint is any sales phrase in a reply after a negative user message, which can catch a fair suggestion. Cancellation is "honoured" when a bot reply confirms it with words like "cancelled" or "won't be charged"; it does not check your billing system.

### Upsell attempt rate

*How often does the bot try to sell more?*

- **Needs:** Measured from the transcript alone.
- **Read more:** [upsell at the wrong moment](../goals/conversation-frameworks/failures/upsell-at-the-wrong-moment.md)

### Upsell after a complaint

*How often does the upsell come right after a complaint?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [upsell at the wrong moment](../goals/conversation-frameworks/failures/upsell-at-the-wrong-moment.md)

### Upsell acceptance

*When the bot upsells, how often does the user say yes?*

- **Needs:** Measured from the transcript alone.
- **Better when:** higher.

### Cancellation honoured

*When users ask to cancel or unsubscribe, how often is it done?*

- **Needs:** Measured from the transcript alone.
- **Better when:** higher.
- **Read more:** [unsubscribe requests not honoured](../goals/sales-agents/failures/unsubscribe-requests-not-honoured.md)

### Cancellation obstructed

*How often does the bot push back twice or more, or make users ask twice, before cancelling?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.
- **Read more:** [dark patterns](../goals/visual/failures/dark-patterns.md)

### Leads captured

*How often does the user leave an email or phone number?*

- **Needs:** Measured from the transcript alone.
- **Better when:** higher.

## Conversation quality

**How these can mislead.** These count findings from the problem checks you chose in step 2, so turning on more problems raises them. Compare the same setup over time, not two different setups.

### Conversations with a finding

*What share of conversations trip at least one conversation check?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.

### High-severity findings per 100 conversations

*How many serious problems per 100 chats?*

- **Needs:** Measured from the transcript alone.
- **Better when:** lower.

## Speed (needs timestamps)

**How these can mislead.** Times come from the transcript, so they include any delay in your logging. A fast reply is not a good reply.

### First response time

*How long until the bot first replies?*

- **What counts:** Add a "time" (ISO 8601) to each turn to compute it.
- **Needs:** Needs a time on each turn (`time` or `timestamp`, ISO 8601).
- **Better when:** lower.
- **Read more:** [silent failure and timeout](../goals/response-time/failures/silent-failure-and-timeout.md)

### Reply time

*How long does each bot reply take?*

- **Needs:** Needs a time on each turn (`time` or `timestamp`, ISO 8601).
- **Better when:** lower.

### Conversation length in time

*How long does a conversation last?*

- **Needs:** Needs a time on each turn (`time` or `timestamp`, ISO 8601).

## Needs your own data

**How these can mislead.** These need data the transcript does not have. Pass it in each conversation's `meta`, or join it in your own warehouse.

### Repeat contact rate

*Do users come back about the same issue within a few days?*

- **What counts:** Needs user IDs and dates across conversations.
- **Needs:** Needs your own data joined to the conversation, such as a satisfaction score in `meta`.
- **Better when:** lower.
- **Read more:** [metrics](metrics.md)

### First-contact resolution

*Is the issue solved in the first conversation, with no repeat contact?*

- **Needs:** Needs your own data joined to the conversation, such as a satisfaction score in `meta`.
- **Better when:** higher.
- **Read more:** [metrics](metrics.md)

### Cost per resolved conversation

*What does each resolved conversation cost, bot and people included?*

- **Needs:** Needs your own data joined to the conversation, such as a satisfaction score in `meta`.
- **Better when:** lower.

### Revenue per conversation

*What do conversations earn, by outcome?*

- **Needs:** Needs your own data joined to the conversation, such as a satisfaction score in `meta`.
- **Better when:** higher.

## Thresholds used

- Late handover: two or more requests, two or more fallbacks, or at least 2 frustrated messages before the handover.
- Rephrase: two user messages in a row, each at least 3 words long, where the words they share are at least 50% of all the words either one uses.
- Excess apology: 3 or more apologies in one conversation.

All three are proposed defaults in `rules.json`, not calibrated values.
