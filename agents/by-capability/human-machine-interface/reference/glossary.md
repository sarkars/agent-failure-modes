# Chatbot analytics glossary: containment, drop-off, handoff recall, Pattern ID and more

This page is a plain-word glossary of the conversation-analytics terms this library uses, for developers and product owners who read its pages or run a chatbot dashboard.

> **Status: draft, 2026-10-20.** Each definition restates how a page in this library defines the term, and links to that page. Where a term is the library's own, the entry says "our usage". The library's schema, signals and Guide specs are proposed, not calibrated against labeled conversations. This page gives no benchmark or "good" value for any metric.

## How to use this page
- Entries are alphabetical. Each ends with a link to the page that defines the term.
- Vendor wording (Amazon Lex V2, Dialogflow CX) is used only as [metrics.md](metrics.md) reports it. Vendors differ, so say which definition you use.
- Field names such as `bot.is_fallback` come from the [conversation event schema v0.1](../roadmap/specs/conversation-event-schema-v0.1.md) and are proposed.

## A to C

### Confirmed resolution
Our usage. A conversation where the user confirmed the problem was solved, or where no one came back about the same issue. It is read beside containment to show how many contained conversations actually worked. Defined in [metrics.md, section 1](metrics.md) and used as the primary metric in [answer-and-go-conversation](../goals/conversation-leadership/failures/answer-and-go-conversation.md).

### Containment rate
The share of bot conversations that end without a handoff to a person. The exact test for "contained" is your choice, and a user who gives up or cannot find a person still counts as contained, so it can overstate real success. Defined in [metrics.md, section 1](metrics.md).

### Counter-metric
Our usage. A second number you read beside a headline metric to catch what the headline hides, such as confirmed resolution beside containment. Defined in [metrics.md](metrics.md), where every metric section names one.

### Counter-signal
Our usage. For each detection signal, the innocent explanation that could produce the same log data, for example a user who left because the task was already finished. It stops a signal from being read as proof. Shown in the signals table of [generic-error-messages](../goals/errors-and-recovery/failures/generic-error-messages.md).

## D to F

### Detection signal
Our usage. A proposed pattern in a conversation event log that suggests a failure, listed on a pattern page with its counter-signal. Signals are proposed until checked against human-labeled conversations. Defined in [generic-error-messages](../goals/errors-and-recovery/failures/generic-error-messages.md) and counted in the [failure taxonomy](../roadmap/specs/failure-taxonomy-v1.md).

### Drop-off (abandonment)
The share of conversations where the user stops responding before the task or the bot's own flow ends. Lex V2 calls a conversation Dropped when the customer does not respond before it is categorized as a success or failure; neither vendor says why the user stopped. A drop after an answer differs from a drop after an error. Defined in [metrics.md, section 4](metrics.md).

### Escalation
The library's second word for handoff: a conversation moving to a person. Dialogflow CX counts escalation by sessions that requested it, so a request is not the same as reaching a person. Defined in [metrics.md, section 3](metrics.md); see also handoff.

### Escalation precision
Of the handoffs that happened, the share that reviewers or agents label as needed. It is read with handoff recall on a labeled sample. Defined in [escalates-too-early-or-too-late](../goals/human-handoff/failures/escalates-too-early-or-too-late.md).

### Fallback
A bot turn that says it did not understand or makes no progress, logged as `bot.is_fallback = true`. The fallback rate is counted per turn or per conversation, and the two are different numbers. A bot that guesses never falls back. Defined in [metrics.md, section 2](metrics.md).

### First-contact resolution (FCR)
The share of issues fully resolved in one interaction with no follow-up. The same-issue window and whether transfers count are choices you must write down. It mirrors repeat contact only if both use the same window. Defined in [metrics.md, section 7](metrics.md).

## G to M

### Guide spec
Our usage. A block at the end of a pattern's metrics section that records, in a fixed format meant for later code, which moves apply, where the check runs and what to do on a miss. It is marked `status: proposed`. Defined in [conversation-moves](../solutions-library/conversation-moves.md); example in [generic-error-messages](../goals/errors-and-recovery/failures/generic-error-messages.md).

### Handoff
A conversation moving from the bot to a person. The handoff rate is completed handoffs divided by conversations, and requested minus completed shows users who asked and did not get through. A completed handoff is not a good one if the person has no context. Defined in [metrics.md, section 3](metrics.md); see also [cold-transfer](../goals/human-handoff/failures/cold-transfer.md).

### Handoff recall
Our usage, called escalation recall on the pattern page. Of the conversations labeled "a person was needed", the share that reached a person. The page gives a starting target to tune, not a standard. Defined in [escalates-too-early-or-too-late](../goals/human-handoff/failures/escalates-too-early-or-too-late.md).

### Maturity
Our usage. How far a page's claims have been checked. The schema, detection signals, Guide specs and pattern metrics here are draft or proposed, and none is calibrated. Stated in the status lines of the [failure taxonomy](../roadmap/specs/failure-taxonomy-v1.md) and the [event schema](../roadmap/specs/conversation-event-schema-v0.1.md).

### Move
Our usage. One of five short things a bot should do at the moment a known failure usually happens: lead with the answer, ask one clarifying question, offer choices, admit uncertainty and show how to check, or hand off to a person. Each move says when to use it and when to avoid it. Defined in [conversation-moves](../solutions-library/conversation-moves.md).

## P to S

### Pattern ID
Our usage. The file name of a failure pattern page without `.md`, such as `cold-transfer`. It never changes, so you can cite it in a spec, ticket or test result. Defined in the [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

### Repeat contact
The share of users who come back about the same issue within a window. No vendor page opened defines it directly; the window and the "same issue" rule are yours to set. It needs a stable user key and lags the first bad answer. Defined in [metrics.md, section 6](metrics.md).

### Silent exit
Our usage. A session that ends on a bot message with no user reply and no confirmed resolution. A rising silent-exit rate suggests containment is counting giving up as success. Defined in [answer-and-go-conversation](../goals/conversation-leadership/failures/answer-and-go-conversation.md).

### Starter rule
Our usage. One sentence on a pattern page that states the smallest rule a bot could follow to avoid the failure, for example that every error names what failed, whether work was saved and one next step. Shown in [generic-error-messages](../goals/errors-and-recovery/failures/generic-error-messages.md).

## Related
- [Chatbot metrics: how each one misleads](metrics.md)
- [Failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md)
- [Conversation event schema v0.1](../roadmap/specs/conversation-event-schema-v0.1.md)
- [Chat analytics plan](../roadmap/chat-analytics-plan.md)
