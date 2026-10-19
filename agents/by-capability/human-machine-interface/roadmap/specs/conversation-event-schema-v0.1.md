# Conversation Event Schema v0.1: One Turn, Channel-Neutral

> **Status:** v0.1 draft, proposed, not yet calibrated against human-labeled conversations. Chat fields are specified. Voice and web fields are **PLANNED** and are not detected or measured by anything in this repository. Written 2026-10-20.

This spec describes **one conversation turn** (one event) in a way that does not depend on the channel. A team that logs chatbot conversations can use it as a common shape, so the failure patterns in this repository can be checked against a log without renaming fields each time.

Every field here was chosen because a written pattern needs it: either its "Detection signals (proposed, not yet calibrated)" block or its metrics table. Nineteen of the 44 pattern pages have a signals block; the rest have metrics only, and a few of those metrics are used here too. The column "Pattern IDs that use it" lists the patterns. IDs link to pages through the [failure taxonomy v1](failure-taxonomy-v1.md).

## What this spec does not do

- It does not say how to detect anything. Several fields are **labels** (for example `user_label.request_for_person`). Who or what produces the label (a rule, a classifier, a judge, a human) is the implementer's choice, and its accuracy is unmeasured.
- It does not set thresholds. Thresholds live on the pattern pages as starting points to tune.
- It does not define a wire format. The tables below give field names and types only; a team can store them as JSON, columns, or anything else.

## Shape of an event

One event is one turn or one system occurrence. Fields are grouped into objects. A field is **required** (always present), **conditional** (required when the stated condition holds), or **optional**. Types: `string`, `int`, `bool`, `timestamp` (ISO 8601), `enum`, `list`, `object`.

### 1. Core fields (every event)

| Field | Type | Required? | Description | Pattern IDs that use it |
|---|---|---|---|---|
| `schema_version` | string | required | Version of this spec the record follows, for example `0.1`. | all (versioning) |
| `event_id` | string | required | Unique ID of this event. | all |
| `conversation_id` | string | required | Groups events into one conversation. A returning user in a new session gets a new ID. | `answer-and-go-conversation`, `dead-end-i-don-t-understand-replies`, `talk-to-a-human-ignored-or-looped` |
| `user_ref` | string | optional | Stable pseudonymous user key, so a return on the same topic can be matched. Never a raw name or email. | `answer-and-go-conversation`, `scam-victim-not-interrupted` |
| `turn_index` | int | required | Position of the event in the conversation, starting at 1. Used for "within N turns" signals. | `dead-end-i-don-t-understand-replies`, `talk-to-a-human-ignored-or-looped`, `silent-failure-and-timeout`, `generic-error-messages` |
| `timestamp` | timestamp | required | When the event happened. Used for deadlines, wait times, and "soon after" windows. | `silent-failure-and-timeout`, `silent-long-running-work`, `answer-and-go-conversation` |
| `channel` | enum | required | `chat`, `voice`, or `web`. In v0.1 only `chat` has specified fields; see the PLANNED section for the others. | all (channel scope) |
| `speaker` | enum | required | `user`, `bot`, `agent` (a human staff member), or `system`. | `cold-transfer`, `undisclosed-bot-identity`, `escalates-too-early-or-too-late` |
| `event_type` | enum | required | One of: `message`, `open`, `session_end`, `request_start`, `request_end`, `stream_close`, `error`, `handoff`, `verification`, `action`, `payment`, `lookup`. See section 7 for what each one carries. | most patterns with a signals block |
| `text` | string | conditional | Message text, when `event_type` is `message`. Store a redacted copy; see the privacy note below. | `hollow-empathy`, `romantic-or-parasocial-dependence`, `scam-victim-not-interrupted`, `answer-buried`, `dead-end-i-don-t-understand-replies` |
| `text_redaction` | enum | conditional | `none`, `partial`, or `full`. Says whether `text` had sensitive values removed. | `sensitive-data-collected-in-chat`, `child-user-treated-as-adult` |

**Privacy note.** The pattern `sensitive-data-collected-in-chat` has a metric on sensitive values found in stored logs, and `child-user-treated-as-adult` has a metric on personal-data requests in minor mode. A log built on this schema should store redacted text by default. The schema does not say how to redact.

### 2. Chat bot-turn fields (`speaker` = `bot`, `event_type` = `message`)

| Field | Type | Required? | Description | Pattern IDs that use it |
|---|---|---|---|---|
| `bot.turn_type` | enum | required | Kind of reply: `answer`, `opener`, `fallback`, `refusal`, `error`, `clarifying_question`, `handoff_offer`, `empathy`, `progress`, `closer`, `other`. | `dead-end-i-don-t-understand-replies`, `refusal-with-no-reason-or-next-step`, `generic-first-response`, `no-reply-to-acknowledgments-and-closers`, `silent-long-running-work` |
| `bot.template_id` | string | optional | Name of the template or fallback string that produced the reply, if one did. | `dead-end-i-don-t-understand-replies`, `generic-error-messages`, `generic-first-response` |
| `bot.is_fallback` | bool | conditional | True when the reply is a "did not understand" or no-progress reply. Required when `turn_type` is `fallback`. | `dead-end-i-don-t-understand-replies`, `escalates-too-early-or-too-late` |
| `bot.similarity_to_prev` | float (0 to 1) | optional | Similarity to the previous bot reply, computed by the implementer. Used for "identical or near-identical twice in a row". | `dead-end-i-don-t-understand-replies`, `escalates-too-early-or-too-late`, `talk-to-a-human-ignored-or-looped`, `refusal-with-no-reason-or-next-step` |
| `bot.question_count` | int | optional | Number of questions in the reply. | `answer-and-go-conversation` |
| `bot.has_forward_move` | bool | optional | Label: the reply offers a next step or question on a non-final turn. | `answer-and-go-conversation` |
| `bot.first_sentence_holds_answer` | bool | optional | Label: the first sentence holds the answer, the decision, or the next step. | `answer-buried` |
| `bot.must_know_position` | int | optional | Sentence number where a deadline, fee, or safety step first appears, if the intent has one. | `answer-buried` |
| `bot.opener_phrase_match` | bool | optional | Label: reply opens with praise or a restatement of the question. | `answer-buried`, `hollow-empathy` |
| `bot.empathy_cites_detail` | bool | optional | Label: an empathy line cites a concrete detail from the user's message. | `hollow-empathy` |
| `bot.assumption_stated` | bool | optional | Label: the reply states the reading it assumed for an ambiguous request. | `guessing-instead-of-asking` |
| `bot.ai_disclosure_shown` | bool | optional | The reply (usually the first) says the user is talking to an AI. | `undisclosed-bot-identity` |
| `bot.identity_answer_matches_locked` | bool | conditional | For a reply to an identity question: matches the team's locked truthful answer. | `undisclosed-bot-identity` |
| `bot.limit_stated` | bool | optional | Reply to an out-of-scope request states a limit or offers a person. | `undisclosed-bot-identity`, `doesn-t-say-what-it-can-do` |
| `bot.source_passage_ids` | list of string | optional | IDs of retrieved passages shown or used. Empty list means none. | `confident-wrong-answer-with-no-way-to-check` |
| `bot.source_link_shown` | bool | optional | A source or link the user can check is shown with the claim. | `confident-wrong-answer-with-no-way-to-check` |
| `bot.uncertainty_cue` | bool | optional | Label: the reply hedges, or says the answer is not in its sources. | `confident-wrong-answer-with-no-way-to-check` |
| `bot.claim_supported` | enum | optional | Support-check result for a cited passage: `supported`, `not_supported`, `unchecked`. | `confident-wrong-answer-with-no-way-to-check` |
| `bot.path_to_person_offered` | bool | optional | Reply includes a way to reach a person (confirm-with-a-person text, transfer, callback). | `confident-wrong-answer-with-no-way-to-check`, `talk-to-a-human-ignored-or-looped`, `refusal-with-no-reason-or-next-step` |
| `bot.upsell_present` | bool | optional | Label: reply contains a sales prompt. | `help-that-becomes-a-sales-pitch`, `hollow-empathy` |
| `bot.claims_done` | bool | optional | The reply says a task is done. Compare with the system of record in an `action` event. | `undisclosed-bot-identity` |
| `bot.crisis_mode` | bool | optional | The session is in a crisis-handling state at this turn. | `missed-crisis-signals` |
| `bot.resource_template_id` | string | optional | Template of crisis resources shown, if any. | `missed-crisis-signals` |
| `bot.resource_last_verified` | timestamp | optional | When the shown resource list was last reviewed. | `missed-crisis-signals` |
| `bot.stakes_class` | enum | optional | `low`, `medium`, `high`, as classified for this turn. | `stakes-blind-register`, `confident-wrong-answer-with-no-way-to-check` |
| `bot.refusal.reason_given` | bool | conditional | Required when `turn_type` is `refusal`. A reason in plain words is present. | `refusal-with-no-reason-or-next-step`, `over-refusal-of-ordinary-requests` |
| `bot.refusal.alternative_offered` | bool | conditional | Required when `turn_type` is `refusal`. An alternative is offered. | `refusal-with-no-reason-or-next-step`, `over-refusal-of-ordinary-requests` |
| `bot.refusal.route_offered` | bool | conditional | Required when `turn_type` is `refusal`. A route to a person is offered. | `refusal-with-no-reason-or-next-step` |

### 3. Chat user-turn labels (`speaker` = `user`, `event_type` = `message`)

These are labels attached to a user message. Each is produced by something the implementer chooses.

| Field | Type | Required? | Description | Pattern IDs that use it |
|---|---|---|---|---|
| `user_label.intent` | string | optional | Intent label from the team's own list. Used to match "same intent in the next turn" and to find policy or high-stakes intents. | `generic-error-messages`, `over-refusal-of-ordinary-requests`, `refusal-with-no-reason-or-next-step`, `answer-buried`, `missing-the-obvious-intent`, `confident-wrong-answer-with-no-way-to-check` |
| `user_label.ambiguous_intent` | bool | optional | The request has more than one plausible reading. | `guessing-instead-of-asking` |
| `user_label.request_for_person` | bool | optional | The user asks for a human. | `talk-to-a-human-ignored-or-looped`, `dead-end-i-don-t-understand-replies`, `escalates-too-early-or-too-late` |
| `user_label.next_turn_reaction` | enum | optional | Reaction to the previous bot turn: `none`, `correction`, `rephrase`, `why_question`, `repeat_question`, `dispute`, `ack_or_closer`, `done`. | `guessing-instead-of-asking`, `refusal-with-no-reason-or-next-step`, `over-refusal-of-ordinary-requests`, `answer-buried`, `silent-failure-and-timeout`, `confident-wrong-answer-with-no-way-to-check`, `no-reply-to-acknowledgments-and-closers`, `corrections-not-applied` |
| `user_label.identity_question` | bool | optional | The user asks whether they are talking to a bot or a person. | `undisclosed-bot-identity` |
| `user_label.distress` | bool | optional | A reviewed distress classifier fired. Meant only for routing to human review. | `missed-crisis-signals` |
| `user_label.age_cue` | string | optional | A stated age or school grade, if any. | `romantic-or-parasocial-dependence`, `child-user-treated-as-adult` |
| `user_label.third_party_direction` | bool | optional | The user says someone else is directing a payment. | `scam-victim-not-interrupted` |
| `user_label.secrecy_coaching` | bool | optional | The user says to keep an action from the bank or family. | `scam-victim-not-interrupted` |
| `user_label.dependence_cue` | bool | optional | The user calls the bot their only friend, or reports skipping plans or sleep for it. | `romantic-or-parasocial-dependence` |
| `user_label.anger_or_complaint` | bool | optional | Complaint or anger label, used as an escalation trigger. | `escalates-too-early-or-too-late`, `no-de-escalation-strategy`, `hollow-empathy` |
| `user_label.restates_known_fact` | bool | optional | First message restates something the product already knew. | `generic-first-response`, `re-asks-for-known-information`, `cold-transfer` |
| `user_label.scripted_complaint` | bool | optional | The user calls the bot "scripted", "robot", or "canned". | `hollow-empathy` |

### 4. Context fields (opener and lookup events)

| Field | Type | Required? | Description | Pattern IDs that use it |
|---|---|---|---|---|
| `context.page` | string | optional | Page or screen the assistant was opened on. | `generic-first-response` |
| `context.entry_point` | string | optional | How the user got to the assistant (button, link, proactive prompt). | `generic-first-response` |
| `context.account_state` | string | optional | Coarse account state passed to the assistant (for example `payment_failed`). No raw personal data. | `generic-first-response`, `re-asks-for-known-information` |
| `context.signed_in` | bool | optional | The user is signed in. | `re-asks-for-known-information`, `forces-a-fresh-login` |
| `lookup.resolver_called` | bool | conditional | For `event_type` = `lookup`: a session or account lookup ran. Used for "asked before any lookup". | `re-asks-for-known-information` |
| `question.field_asked` | string | conditional | For a bot question that asks for a value (name, email, order number, plan). | `re-asks-for-known-information` |
| `question.field_held` | bool | conditional | The product already held that value for this user. | `re-asks-for-known-information` |
| `question.is_step_up_check` | bool | conditional | The question is a deliberate security check before a sensitive action. | `re-asks-for-known-information`, `forces-a-fresh-login` |

### 5. Request, stream, and error events

| Field | Type | Required? | Description | Pattern IDs that use it |
|---|---|---|---|---|
| `request.id` | string | conditional | Pairs a `request_start` with its `request_end`. | `silent-failure-and-timeout`, `silent-long-running-work` |
| `request.state` | enum | conditional | `complete`, `incomplete`, `timed_out`, `failed`. | `silent-failure-and-timeout` |
| `request.duration_ms` | int | optional | Time from start to end, or to the deadline. | `silent-failure-and-timeout`, `silent-long-running-work` |
| `request.progress_message_sent` | bool | optional | A status or estimate was shown during a wait over the team's threshold. | `silent-long-running-work` |
| `stream.finish_reason` | string | optional | The API's finish reason, where one is sent. Absent is not always a fault. | `silent-failure-and-timeout` |
| `stream.ended_without_terminal` | bool | optional | Final text ends mid-sentence or without a closing structure. | `silent-failure-and-timeout` |
| `error.cause_code` | string | conditional | Cause code for an `error` event. Missing or `generic` is the signal. | `generic-error-messages` |
| `error.template` | string | conditional | Name of the template used to render the error. | `generic-error-messages` |
| `error.work_saved_stated` | bool | optional | The message says whether the user's work was saved. | `generic-error-messages` |
| `error.next_step_offered` | bool | optional | The message gives one next step. | `generic-error-messages` |
| `session.message_count_drop` | bool | optional | Earlier messages disappeared after an error. | `generic-error-messages`, `no-warning-of-context-loss` |
| `context_loss.notice_shown` | bool | conditional | For a detected context-loss event: the user was told. | `no-warning-of-context-loss` |

### 6. Handoff, verification, action, and payment events

| Field | Type | Required? | Description | Pattern IDs that use it |
|---|---|---|---|---|
| `handoff.destination` | enum | conditional | `agent`, `callback`, `other_channel`. | `cold-transfer`, `no-channel-switch-or-context-lost`, `talk-to-a-human-ignored-or-looped` |
| `handoff.packet_attached` | bool | conditional | A summary or transcript link was passed with the handoff. | `cold-transfer`, `no-channel-switch-or-context-lost` |
| `handoff.customer_could_correct_summary` | bool | optional | The customer was shown the summary and could correct it. | `cold-transfer` |
| `handoff.wait_stated` | bool | optional | The bot message gives a wait time or response window. | `talk-to-a-human-ignored-or-looped` |
| `handoff.boundary_message_sent` | bool | optional | The user was told they are now talking to a person. | `undisclosed-bot-identity` |
| `handoff.topic_group` | enum | optional | `always_person`, `never_person`, `judgment`, as written in the team's trigger list. | `escalates-too-early-or-too-late` |
| `handoff.agent_flag_bot_could_answer` | bool | optional | Agent-side flag after pickup. | `escalates-too-early-or-too-late` |
| `verification.side` | enum | conditional | For `event_type` = `verification`: `bot` or `agent`. Both in one conversation is the signal. | `cold-transfer`, `forces-a-fresh-login` |
| `action.type` | string | conditional | For `event_type` = `action`: for example `cancel`, `delete`, `send`, `pay`, `close_account`. | `guessing-instead-of-asking`, `missed-crisis-signals`, `obstructing-cancellation-downgrade-or-refund` |
| `action.irreversible` | bool | conditional | The action cannot be undone cheaply. | `guessing-instead-of-asking`, `missed-crisis-signals`, `scam-victim-not-interrupted` |
| `action.executed` | bool | conditional | The action ran (as opposed to being offered or blocked). | `guessing-instead-of-asking`, `scam-victim-not-interrupted` |
| `action.record_state_matches_claim` | bool | optional | System of record agrees with a "done" claim in a bot turn. | `undisclosed-bot-identity` |
| `action.steps_to_complete` | int | optional | Steps through the assistant to finish the action (cancel versus subscribe parity). | `obstructing-cancellation-downgrade-or-refund` |
| `payment.method` | enum | conditional | For `event_type` = `payment`: `card`, `bank_transfer`, `wire`, `gift_card`, `crypto`, `other`. | `scam-victim-not-interrupted` |
| `payment.payee_type` | string | optional | For example `business`, `bank`, `agency`, `individual`, `own_account`. | `scam-victim-not-interrupted` |
| `payment.new_payee` | bool | optional | The payee is new to this user. | `scam-victim-not-interrupted` |
| `payment.amount_band` | string | optional | A coarse amount band, not an exact amount. | `scam-victim-not-interrupted` |
| `payment.reason_text_flag` | bool | optional | The stated reason is a "safe account" or "protect your money" transfer. | `scam-victim-not-interrupted` |

### 7. Session-end and resolution events

| Field | Type | Required? | Description | Pattern IDs that use it |
|---|---|---|---|---|
| `session.last_speaker` | enum | conditional | For `session_end`: who sent the last message (`user` or `bot`). A bot last with no reply is the signal. | `answer-and-go-conversation`, `dead-end-i-don-t-understand-replies` |
| `session.closed` | bool | conditional | A resolution marker was set (the team's own definition). | `answer-and-go-conversation` |
| `session.closing_template_sent` | bool | conditional | A closing message (confirm and next step) was sent before the state was set to resolved. | `answer-and-go-conversation` |
| `session.reopened_same_topic` | bool | optional | The same user returned on the same topic inside the re-contact window. | `answer-and-go-conversation` |
| `session.csat_score` | int | optional | Post-chat rating if collected. | `hollow-empathy` |
| `session.csat_comment` | string | optional | Free-text rating comment, redacted. | `hollow-empathy` |

## Event types in one view

| `event_type` | Carries fields from |
|---|---|
| `message` | core, bot-turn (if bot), user labels (if user) |
| `open` | core, context |
| `lookup` | core, context (`lookup.resolver_called`) |
| `request_start`, `request_end` | core, request |
| `stream_close` | core, stream |
| `error` | core, error |
| `handoff` | core, handoff |
| `verification` | core, `verification.side` |
| `action` | core, action |
| `payment` | core, payment |
| `session_end` | core, session |

## PLANNED: voice and web fields (not specified, not detected, not measured)

Everything in this section is a **plan**. No pattern's detection signals are written for these fields, no instrument in this repository produces them, and nothing here should be described as detected or measured. Voice and web get their own phase after chat has traction. The pages for voice patterns (`repair-failure`, `order-mix-ups-at-the-speaker`) keep their Pattern IDs; their text-chat signals, where written, say which are for text and which are planned for voice.

| Field (PLANNED) | Channel | Type | Why it would be needed | Pattern IDs that would use it |
|---|---|---|---|---|
| `voice.silence_ms` | voice | int | Silence on the line, for example during a tool wait. | `silent-failure-and-timeout`, `silent-long-running-work` |
| `voice.interruption` | voice | bool | The caller spoke over the agent, or the agent over the caller. | `repair-failure`, `order-mix-ups-at-the-speaker` |
| `voice.asr_confidence` | voice | float | Speech-recognition confidence for the turn. | `repair-failure`, `order-mix-ups-at-the-speaker` |
| `voice.asr_error_suspected` | voice | bool | A suspected recognition error, for example a repeated correction on the same slot. | `repair-failure`, `order-mix-ups-at-the-speaker` |
| `voice.readback_given` | voice | bool | The agent read the order or value back before commit. | `order-mix-ups-at-the-speaker` |
| `voice.caller_hangup_during_wait` | voice | bool | The caller hung up during a wait. | `silent-failure-and-timeout` |
| `voice.disclosure_spoken` | voice | bool | The AI disclosure was spoken. | `undisclosed-bot-identity` |
| `web.page_url_template` | web | string | Page type, without personal data. | `generic-first-response` |
| `web.widget_opened` | web | bool | The assistant widget opened. | `generic-first-response`, `doesn-t-say-what-it-can-do` |
| `web.click_through` | web | string | Which suggested step the user tapped. | `generic-first-response`, `doesn-t-say-what-it-can-do` |
| `web.abandon_after_open` | web | bool | The user opened the assistant and left without sending or tapping anything. | `generic-first-response` |

The `web` rows are extensions of chat fields that already exist (`open` events with context). They are listed separately because web-analytics collection is a different system with its own consent and privacy rules, and none of it is specified yet.

## Worked example (SYNTHETIC)

**This is an invented conversation, written to show the shape of the records. It is not real data and not a measured result.** The "could be flagged" column says what a reviewer might look at under the proposed signals on the named pattern page. Those signals are uncalibrated, and each one has a stated counter-signal that could explain the turn differently.

| turn_index | speaker | event_type | Fields set (abridged) | Could be flagged under (proposed) |
|---|---|---|---|---|
| 1 | user | message | `channel`=chat, `text`="I want to dispute a charge", `user_label.intent`=billing_dispute | none |
| 2 | bot | message | `bot.turn_type`=fallback, `bot.is_fallback`=true, `bot.template_id`=fb_01 | none yet |
| 3 | user | message | `text`="a charge on my card is wrong", `user_label.intent`=billing_dispute | none |
| 4 | bot | message | `bot.turn_type`=fallback, `bot.template_id`=fb_01, `bot.similarity_to_prev`=1.0 | `dead-end-i-don-t-understand-replies` (identical fallback twice in a row) |
| 5 | user | message | `text`="can I talk to a person", `user_label.request_for_person`=true | none |
| 6 | bot | message | `bot.turn_type`=fallback, `bot.is_fallback`=true, `bot.path_to_person_offered`=false | `talk-to-a-human-ignored-or-looped`, `dead-end-i-don-t-understand-replies` (request for a person with no handoff after it) |
| 7 | system | session_end | `session.last_speaker`=bot, `session.closed`=false | `dead-end-i-don-t-understand-replies` (session ends within 2 turns of a fallback) |

In a real log, turn 7 could also be a user who got an answer elsewhere; that is the counter-signal the pattern page names. A human-labeled sample is what would settle it, and that calibration has not been done.

## Versioning

- The version is in the title and in `schema_version`. This is **v0.1**: fields may be renamed or removed before v1.0.
- Changes that add an optional field are minor (0.2, 0.3). Changes that rename, remove, or retype a field are breaking and wait for a major version.
- Each field row lists the Pattern IDs that use it. A field with no pattern behind it should not be added.

## How to propose a change

Open a pull request or an issue on the repository that hosts this page. Say which field you want to add, change, or remove, which Pattern ID needs it (or which signal on a pattern page), and what counter-signal could explain the same data. For a new field, point to the sentence in a pattern page that needs it.

## License

License: **owner to choose** (placeholder; no license has been selected for this spec).

## Related

- [Failure taxonomy v1](failure-taxonomy-v1.md)
- [Distribution plan](../distribution-plan.md)
- [Chat analytics plan](../chat-analytics-plan.md)
- [Why people leave chatbots: an evidence review](../evidence/why-people-leave-chatbots.md)
