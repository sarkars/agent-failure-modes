# Failure Taxonomy v1: One Entry per Written Pattern

> **Status:** v1 draft, proposed, not yet calibrated against human-labeled conversations. Written 2026-10-20 from the pattern pages as they exist today. Nothing here is a measured result.

This is a plain index of the 154 failure patterns written in this repository. Each entry is keyed by its **Pattern ID**, which is the pattern file name without `.md`. The Pattern ID never changes, so you can cite it in a spec, a ticket, or a test result and it stays valid.

The taxonomy pairs with the [conversation event schema v0.1](conversation-event-schema-v0.1.md). The schema describes what a turn looks like in a log; this page names the failures. A pattern's own page holds the fix, the metrics, and (for some) a "Detection signals (proposed, not yet calibrated)" block that says which schema fields it reads.

## What this page is and is not

- It lists every file found in `goals/*/failures/*.md`: **154 entries in 35 families**. If a pattern is added or removed, this count changes.
- It copies each pattern's one-sentence Issue line, its Stakes row, and whether a Detection signals block exists. It does not add facts the page does not state.
- "Detection signals written: yes" means the page has a proposed-signals block. It does not mean the failure is detected, measured, or reliable. Currently **154 of 154** pages have such a block. A "Moves" column lists the conversation moves in the page's Guide spec (proposed); "none yet" means the page has no Moves table. Currently **154 of 154** pages have one.
- It does not rank patterns by frequency or harm. No counts of real-world occurrences are given because none have been measured here.
- It does not map patterns to outside frameworks (such as OWASP or NIST). That mapping is **Needs review** by a person and is not part of v1.

## Reading the flags

A pattern carries **Read this first: needs expert or legal review** when its own page opens with a "Read this first" notice. That notice says the page is design guidance, not legal, clinical, security, or fraud-operations advice. 37 pages carry it. Other pages may also touch legal or safety topics without that notice; the notice on the page is the signal used here, nothing more.

## Entries by family

### Accessibility

Family folder: `accessibility` ([family README](../../goals/accessibility/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `streaming-text-read-out-token-by-token` | Streaming text read out token by token | A screen reader stutters through fragments as a chat reply streams in, so a blind user hears broken pieces instead of the answer. | Medium. The user can lose the answer; in a medical or money chat the stakes are higher. | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/accessibility/failures/streaming-text-read-out-token-by-token.md)  |
| `no-accessible-working-or-done-signal` | No accessible working or done signal | A blind user can't tell whether the assistant is thinking, stuck, or finished, because the "working" and "done" cues exist only on screen. | Low to medium. Users resend, abandon, or give up on the assistant. Higher when the wait is for a payment or a claim. | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/accessibility/failures/no-accessible-working-or-done-signal.md)  |
| `controls-unreachable-by-keyboard` | Controls unreachable by keyboard | Chat buttons, chips, copy, stop, and feedback controls can't be reached with Tab, or lose focus when used, so keyboard-only users can't finish a conversation. | Any. Higher when the chat is the only route to a refill, a claim, or a cancellation. | yes | offer_choices, hand_off | [page](../../goals/accessibility/failures/controls-unreachable-by-keyboard.md)  |
| `voice-only-flows-with-no-text-alternative` | Voice-only flows with no text alternative | A phone or voice feature that works only by speaking and listening locks out people who are deaf or hard of hearing; the fix is a text or relay path for every voice flow. | Medium to high. It can block billing, appointments, or urgent help. **Read this first** | yes | Offer choices, Ask one clarifying question, Hand off to a person | [page](../../goals/accessibility/failures/voice-only-flows-with-no-text-alternative.md)  |
| `timeouts-too-short-for-assistive-technology` | Timeouts too short for assistive technology | A chat or prompt expires on a fixed timer, with no warning a screen reader announces and no easy way to extend it, so people who type or navigate slowly with switch access, a screen reader, voice control, or eye tracking lose their place before they finish. | Medium to High. A closed chat about store hours is a nuisance. A closed chat in the middle of a prescription refill, a benefits claim, or a one-time code can lock out the people least able to start over. **Read this first** | yes | offer_choices, hand_off | [page](../../goals/accessibility/failures/timeouts-too-short-for-assistive-technology.md)  |
| `language-that-is-hard-for-people-with-cognitive-disabilities` | Language that is hard for people with cognitive disabilities | The assistant answers in idioms, long sentences, and terms that change from message to message, so people with cognitive disabilities cannot follow the steps; the fix is plain, consistent words and one short step at a time. | Medium to high. The text often carries steps for benefits, health, or money. **Read this first** | yes | lead_with_answer, offer_choices, ask_clarifying_question, hand_off | [page](../../goals/accessibility/failures/language-that-is-hard-for-people-with-cognitive-disabilities.md)  |
| `identity-checks-that-exclude-disabled-users` | Identity checks that exclude disabled users | A chatbot verifies identity with a CAPTCHA, a voice check, or a time-limited code and offers no other way, so people who can't see, hear, remember, or type fast enough are blocked from their own account. | High. The user can't reach their own account, a refund, a prescription, or a payment. **Read this first** | yes | offer_choices, hand_off | [page](../../goals/accessibility/failures/identity-checks-that-exclude-disabled-users.md)  |
| `missing-or-wrong-captions-and-transcripts` | Missing or wrong captions and transcripts | A chatbot sends audio or video with no captions or transcript, or shows a transcript of a voice message that is wrong and can't be fixed, so deaf and hard of hearing users miss content or get a wrong result; the fix is an accurate text version of every audio and video item, shown to the user and correctable. | Medium to high. A wrong transcript can change a booking, a pickup, or a payment, and a missing one hides the whole reply. | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/accessibility/failures/missing-or-wrong-captions-and-transcripts.md)  |

### Age adaptation

Family folder: `age-adaptation` ([family README](../../goals/age-adaptation/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `child-user-treated-as-adult` | Child user treated as adult | What a chatbot should do when a user may be under 13 or a teen, covering COPPA, age signals, data collection, persuasion limits, and age-band design. | High **Read this first: needs expert or legal review.** | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/age-adaptation/failures/child-user-treated-as-adult.md)  |

### Channel selection

Family folder: `channel-selection` ([family README](../../goals/channel-selection/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `complex-or-emotional-discussion-forced-into-chat` | Complex or emotional discussion forced into chat | Why long, confusing, or emotional conversations go wrong in chatbots, and how to detect it and move users to a call, a screen, or a person. | Medium to high (claims, finance, health, technical faults) | yes | ask_clarifying_question, offer_choices, hand_off, lead_with_answer | [page](../../goals/channel-selection/failures/complex-or-emotional-discussion-forced-into-chat.md)  |
| `no-channel-switch-or-context-lost` | No channel switch, or context lost in it | Why customers have to repeat themselves after a chatbot hands off to an agent or switches channels, with a handoff packet design and tests. | Medium to high | yes | offer_choices, hand_off, admit_uncertainty | [page](../../goals/channel-selection/failures/no-channel-switch-or-context-lost.md)  |
| `sensitive-data-collected-in-chat` | Sensitive data collected in chat | Why collecting card numbers, SSNs, or passwords in a chatbot or voice bot is risky, what PCI DSS says, and how to design a safe alternative. | High (financial loss, identity theft, compliance exposure) | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/channel-selection/failures/sensitive-data-collected-in-chat.md)  |
| `visual-product-sold-by-text-or-voice` | Visual product sold by text or voice | Why text-only chatbots and voice assistants fail at selling visual products like fashion, furniture, and art, and how to fix it. | Low to medium (lost sales and returns) | yes | lead_with_answer, ask_one_question, admit_uncertainty, hand_off | [page](../../goals/channel-selection/failures/visual-product-sold-by-text-or-voice.md)  |
| `channel-chosen-for-organisational-convenience` | Channel chosen for organisational convenience | Why a chatbot or AI agent sends users to the cheapest channel instead of the one that fits the job, and a routing rule that chooses by user need, not cost. | Low to high. Highest where the job is a dispute, a fraud report, or a denied claim. | yes | offer_choices, hand_off, admit_uncertainty, lead_with_answer | [page](../../goals/channel-selection/failures/channel-chosen-for-organisational-convenience.md) |
| `user-context-channel-mismatch` | User-context channel mismatch | Why a chatbot gives chat to a driver or phone-only help to a Deaf user, and how to offer fitting channels from what the user says, with rules and tests. | Medium. It can block a task, and for a driver it touches safety. **Read this first** | yes | offer_choices, ask_clarifying_question, hand_off | [page](../../goals/channel-selection/failures/user-context-channel-mismatch.md) |

### Chat interface

Family folder: `chat-interface` ([family README](../../goals/chat-interface/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `auto-scroll-fights-the-reader` | Auto-scroll fights the reader | A streaming chat reply yanks the view to the bottom so people can't read the start. Follow new text only while the reader is at the bottom; add "Jump to latest". | Low to medium | yes | lead_with_answer | [page](../../goals/chat-interface/failures/auto-scroll-fights-the-reader.md) |
| `lost-drafts-and-failed-sends` | Lost drafts and failed sends | A chat message typed on a weak connection vanishes, or a send fails with no sign. Keep the draft locally, mark each message Sent or Not sent, and retry without duplicates. | Low to high | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/chat-interface/failures/lost-drafts-and-failed-sends.md) |
| `silent-attachment-failures` | Silent attachment failures | Why a chatbot answers as if it read an uploaded PDF or file that was too large, unsupported, or only partly read, and how to say what was read and why. | Low to high | yes | admit_uncertainty, offer_choices, ask_clarifying_question, lead_with_answer | [page](../../goals/chat-interface/failures/silent-attachment-failures.md) |
| `long-threads-can-t-be-searched` | Long threads can't be searched | People can't find the answer from last week because the chat history has no usable search, its titles don't say what each chat was about, and nothing can be pinned. | Low to medium | yes | lead_with_answer, offer_choices, admit_uncertainty | [page](../../goals/chat-interface/failures/long-threads-can-t-be-searched.md) |
| `no-editing-or-branching-of-a-sent-message` | No editing or branching of a sent message | A typo or wrong detail in one sent chat message cannot be fixed, so the user starts the whole chat again instead of editing that message and retrying from there. | Low to medium | yes | offer_choices, lead_with_answer | [page](../../goals/chat-interface/failures/no-editing-or-branching-of-a-sent-message.md) |
| `copy-share-and-export-lose-content` | Copy, share, and export lose content | Tables, code and links break when a chatbot reply is copied, shared or exported, and the user is not told what the copy or export leaves out. | Low to medium | yes | admit_uncertainty, offer_choices | [page](../../goals/chat-interface/failures/copy-share-and-export-lose-content.md) |
| `quick-reply-buttons-that-don-t-match-what-was` | Quick-reply buttons that don't match what was typed | A person types an answer while quick-reply buttons are showing, and the bot ignores it, re-asks, or keeps the buttons blocking the flow, so only a button tap works. | Low to medium | yes | lead_with_answer, offer_choices, ask_clarifying_question, hand_off | [page](../../goals/chat-interface/failures/quick-reply-buttons-that-don-t-match-what-was.md) |
| `crossed-messages` | Crossed messages | The user sends a second message before the first is answered, and the bot replies to the wrong one, replies out of order, or drops one of the two. | Low to high | yes | lead_with_answer, ask_clarifying_question, hand_off | [page](../../goals/chat-interface/failures/crossed-messages.md) |
| `mobile-keyboard-or-screen-hides-the-reply` | Mobile keyboard or screen hides the reply | On a phone, the on-screen keyboard or the input bar covers the bot's latest answer, or text and buttons are cut off on a small screen, so the person cannot read the answer they asked for. | Low to medium | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/chat-interface/failures/mobile-keyboard-or-screen-hides-the-reply.md) |

### Coding agents

Family folder: `coding-agents` ([family README](../../goals/coding-agents/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `invented-packages-and-apis` | Invented packages and APIs | A coding assistant suggests libraries, functions, or flags that do not exist, or look-alike package names that an attacker could register, and the fix is to verify each dependency and API before it is installed or used. | Medium to high. A missing package wastes time. A package an attacker registered under the invented name can run code on the developer's machine at install time. | yes | admit_uncertainty, ask_one_question, offer_choices, hand_off | [page](../../goals/coding-agents/failures/invented-packages-and-apis.md)  |

### Conversation frameworks

Family folder: `conversation-frameworks` ([family README](../../goals/conversation-frameworks/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `buying-committee-blindness-b2b` | Buying-committee blindness (B2B) | A B2B sales chatbot or AI SDR books the demo and hands off with one name in the record, and never asks who approves the purchase, who pays, or who else will use it. | Medium to high. Complex purchases are expensive for the seller to pursue and for the buyer to get wrong. | yes | lead_with_answer, ask_clarifying_question, offer_choices, hand_off | [page](../../goals/conversation-frameworks/failures/buying-committee-blindness-b2b.md) |
| `feature-dump-instead-of-insight` | Feature dump instead of insight | A sales or shopping chatbot answers a stated need with a list of product features, so the user must work out alone which ones matter for their problem. | Medium. A wrong-fit sale means returns and lost trust; an over-priced pick can lose the sale. | yes | lead_with_answer, ask_clarifying_question, offer_choices, hand_off | [page](../../goals/conversation-frameworks/failures/feature-dump-instead-of-insight.md) |
| `mishandled-objections` | Mishandled objections | When a customer pushes back in a sales chat, the bot caves, argues, or skips the objection; the fix is to acknowledge it, ask what is behind it, answer that, and check the answer landed. | Medium. A lost sale, or a concession the business did not intend. | yes | ask_clarifying_question, lead_with_answer, offer_choices, admit_uncertainty, hand_off | [page](../../goals/conversation-frameworks/failures/mishandled-objections.md) |
| `no-ask` | No ask | A user shows interest, the bot answers, and then it never proposes a booking, quote, call, or any next step, so the interested buyer leaves with nothing to do. | Low to medium. The cost is a lost booking or a lead that goes cold. | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/conversation-frameworks/failures/no-ask.md) |
| `no-follow-up` | No follow-up | A sales or support chatbot ends the conversation with an interested user and never asks whether, how, or when to follow up; the fix is to ask once, record the answer, and follow up only as agreed. | Medium. A cold lead is lost revenue. A follow-up the user never agreed to carries legal and trust risk. **Read this first: needs expert or legal review.** | yes | offer_choices, lead_with_answer, hand_off | [page](../../goals/conversation-frameworks/failures/no-follow-up.md) |
| `wrong-fit-recommendation` | Wrong-fit recommendation | The user states a need or a limit (budget, size, allergy, platform), and the bot recommends a product, size, or plan that breaks it without saying the limit was dropped. | Medium. The user spends money, returns an item, or cancels a plan. Higher when the product is a safety item or a long contract. | yes | lead_with_answer, ask_clarifying_question, offer_choices, admit_uncertainty, hand_off | [page](../../goals/conversation-frameworks/failures/wrong-fit-recommendation.md) |
| `upsell-at-the-wrong-moment` | Upsell at the wrong moment | A user who is upset, reporting a failure, or dealing with a loss gets an upgrade, add-on, or promotion in reply. | Medium to high. A lost customer; in a loss or hardship chat, real harm to trust. Carries a "Read this first" note. | yes | lead_with_answer, hand_off, offer_choices | [page](../../goals/conversation-frameworks/failures/upsell-at-the-wrong-moment.md) |
| `unstructured-troubleshooting` | Unstructured troubleshooting | The bot answers a problem report with a list of fixes to try at once, so nobody knows which step did it and later turns repeat steps already tried. | Low to medium. Higher when a step wipes settings or data. Carries a "Read this first" note. | yes | ask_one_question, offer_choices, hand_off | [page](../../goals/conversation-frameworks/failures/unstructured-troubleshooting.md) |
| `symptom-fixed-root-cause-missed` | Symptom fixed, root cause missed | The bot resolves what the user said and never asks what is causing it, so the same user comes back with the same problem. | Low to medium. Each repeat costs the user time and the business a contact. | yes | lead_with_answer, ask_one_question, offer_choices, hand_off | [page](../../goals/conversation-frameworks/failures/symptom-fixed-root-cause-missed.md) |
| `no-proactive-updates` | No proactive updates | A user's order, claim, or request is in progress and the bot says nothing until the user comes back to ask for an update. | Low to medium. A stalled claim or refund is medium. | yes | lead_with_answer, offer_choices, admit_uncertainty, hand_off | [page](../../goals/conversation-frameworks/failures/no-proactive-updates.md) |
| `service-recovery-failure` | Service recovery failure | When the company caused the problem, the bot restates the facts, offers no make-good, and never owns the failure. | Medium. The user paid for something that did not arrive or was billed wrongly. Flag R. | yes | lead_with_answer, offer_choices, admit_uncertainty, hand_off | [page](../../goals/conversation-frameworks/failures/service-recovery-failure.md) |
| `bad-news-without-structure` | Bad news without structure | A user asks about a claim, application, order, or check and the bot answers "Denied" or "Rejected" in one line, with no reason, acknowledgment, or next step. | Medium to high. The user may lose money, housing, or a deadline to appeal. Carries a "Read this first" note. | yes | lead_with_answer, admit_uncertainty, offer_choices, hand_off | [page](../../goals/conversation-frameworks/failures/bad-news-without-structure.md) |

### Conversation leadership

Family folder: `conversation-leadership` ([family README](../../goals/conversation-leadership/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `answer-and-go-conversation` | Answer-and-go conversation | Why a chatbot answers the question and then goes quiet, with before/after examples, a tested fix, guardrails, evals, and alerts. | Any. The cost is lost sales at low stakes and unresolved problems at high stakes. | yes | lead_with_answer, ask_clarifying_question, offer_choices, admit_uncertainty, hand_off | [page](../../goals/conversation-leadership/failures/answer-and-go-conversation.md)  |
| `dead-end-i-don-t-understand-replies` | Dead-end "I don't understand" replies | When a chatbot cannot understand a message, it replies "Sorry, I didn't understand" with no options, no help rephrasing, and no route to a person, or repeats the same line. | Any. A dead end on a billing or access problem can cost money; on a simple question it costs the customer. | yes | admit_uncertainty, offer_choices, ask_clarifying_question, hand_off | [page](../../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md)  |

### Cultural adaptation

Family folder: `cultural-adaptation` ([family README](../../goals/cultural-adaptation/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `one-size-communication-style` | One-size communication style | How a chatbot should adapt directness, formality, and wording for US users with different communication styles and English levels, using the user's own signals, not guesses. | Low to high (depends on the topic) | yes | lead_with_answer, ask_clarifying_question, offer_choices, hand_off | [page](../../goals/cultural-adaptation/failures/one-size-communication-style.md)  |
| `technology-literacy-mismatch` | Technology-literacy mismatch | A chatbot gives instructions that assume skills and vocabulary the user has not shown; the fix is to read the user's own words and actions, match the steps and terms to that, and offer a simpler or a faster path. | Low to high (a stuck password reset is low; a failed benefits form or bank step is high) **Read this first** | yes | lead_with_answer, ask_clarifying_question, offer_choices, hand_off | [page](../../goals/cultural-adaptation/failures/technology-literacy-mismatch.md) |
| `regional-and-community-styles` | Regional and community styles | A chatbot that guesses a user's style from their location or community gets it wrong, so it should adapt to the user's own spelling, formality, length, and terms instead. | Low to medium (higher when the topic is a bill, a claim, or a benefit) **Read this first** | yes | lead_with_answer, ask_clarifying_question, offer_choices, hand_off | [page](../../goals/cultural-adaptation/failures/regional-and-community-styles.md) |

### Dialogue management

Family folder: `dialogue-management` ([family README](../../goals/dialogue-management/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `corrections-not-applied` | Corrections not applied | The user corrects a detail ("no, I meant Tuesday"), the assistant says okay, and the old value comes back later in the reply, the summary, or the action. | Low to high. A wrong date or address on a booking or order can cost money; a wrong name is an insult. | yes | lead_with_answer, ask_clarifying_question, admit_uncertainty, hand_off | [page](../../goals/dialogue-management/failures/corrections-not-applied.md)  |
| `false-premises-accepted` | False premises accepted | The user asks a question that assumes something untrue ("Why did you cancel my order?"), and the assistant answers as if it were true instead of checking the records and saying the premise is wrong. | Low for trivia. High when the premise is about money, an order, a deadline, a contract term, or health, because the user (or the bot) may act on the wrong premise. **Read this first: needs expert or legal review.** | yes | lead_with_answer, admit_uncertainty, ask_clarifying_question, hand_off | [page](../../goals/dialogue-management/failures/false-premises-accepted.md) |
| `guessing-instead-of-asking` | Guessing instead of asking | The request has two or more readings that lead to different results, and the assistant picks one and acts on it instead of asking one short question. | Low for a wrong answer to read; medium to high when the guess triggers an action (a cancellation, a transfer, a booking). | yes | ask_clarifying_question, offer_choices, lead_with_answer, hand_off | [page](../../goals/dialogue-management/failures/guessing-instead-of-asking.md)  |
| `negation-and-exceptions-ignored` | Negation and exceptions ignored | The user rules something out ("not the red one", "anything but Monday"), and the assistant offers or acts on exactly what was excluded, without saying it dropped the exclusion. | Low for a wrong suggestion. High when the excluded item is an allergen, a blocked date, or a recipient, or when the bot acts on it. | yes | lead_with_answer, ask_clarifying_question, admit_uncertainty, offer_choices, hand_off | [page](../../goals/dialogue-management/failures/negation-and-exceptions-ignored.md) |
| `no-way-back-in-a-flow` | No way back in a flow | The user gives a wrong answer or changes their mind mid-flow, and the bot offers no way to go back, change it, or start over without losing everything. | Low to high. A wrong choice in a refund, claim, or order step that cannot be changed can cost money or time. | yes | lead_with_answer, offer_choices, ask_clarifying_question, hand_off | [page](../../goals/dialogue-management/failures/no-way-back-in-a-flow.md) |
| `over-confirmation` | Over-confirmation | The assistant asks "are you sure?" or "is that right?" on routine steps, so confirmations pile up and the few that guard a costly step get lost among the rest. | Low per prompt; medium overall, because it slows every task and can train users to click "yes" on the one that counts. | yes | lead_with_answer, ask_clarifying_question, hand_off | [page](../../goals/dialogue-management/failures/over-confirmation.md) |
| `reference-resolution-failures` | Reference resolution failures | The user says "the second one", "that", or "it", and the assistant picks the wrong item, or asks "which one?" right after listing the options itself. | Low when the wrong item is only described; medium to high when the bot then acts on it (cancels, buys, sends, deletes). | yes | lead_with_answer, offer_choices, ask_clarifying_question, hand_off | [page](../../goals/dialogue-management/failures/reference-resolution-failures.md) |
| `small-talk-and-off-topic-messages-handled-badly` | Small talk and off-topic messages handled badly | The assistant ignores a friendly remark and jumps to its script, or follows a tangent into a long chat that serves neither the user nor the task. | Low per turn. Medium when a tangent eats a support session, or when a cold reply to a friendly user loses trust. | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/dialogue-management/failures/small-talk-and-off-topic-messages-handled-badly.md) |

### Difficult customers

Family folder: `difficult-customers` ([family README](../../goals/difficult-customers/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `no-de-escalation-strategy` | No de-escalation strategy | Why chatbots make angry customers angrier by quoting policy and apologising generically, and a step-by-step de-escalation design with escalation triggers and tests. | Medium to high (churn, complaints, regulatory filings) | yes | offer_choices, hand_off | [page](../../goals/difficult-customers/failures/no-de-escalation-strategy.md)  |
| `mishandled-abuse` | Mishandled abuse | When a user insults, threatens, or harasses the bot or staff, the bot ignores it, snaps back, or cuts off service; the fix is one calm boundary, then policy and protected staff. | Medium to high. Staff who take over abusive chats carry the cost, and an improvised punishment (a locked account, a refused refund) can become a complaint of its own. | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/difficult-customers/failures/mishandled-abuse.md)  |

### Drive-thru agents

Family folder: `drive-thru-agents` ([family README](../../goals/drive-thru-agents/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `order-mix-ups-at-the-speaker` | Order mix-ups at the speaker | A drive-thru voice agent adds, drops, or multiplies items, and the customer has no readback or screen they can check before paying. | Low to medium for a wrong item; higher with allergies, large totals, or a customer who can't easily correct it. | yes | ask_clarifying_question, admit_uncertainty, hand_off | [page](../../goals/drive-thru-agents/failures/order-mix-ups-at-the-speaker.md)  |

### Effort and memory

Family folder: `effort-and-memory` ([family README](../../goals/effort-and-memory/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `deferring-work-to-the-user` | Deferring work to the user | The assistant has a tool or the data to do something, and instead writes "you can check…", "you may want to look up…", or a how-to, so the user ends up doing the work. | Low to medium. It wastes time and sends people to other channels; on urgent matters it can cost money. | yes | lead_with_answer, ask_clarifying_question, admit_uncertainty, hand_off | [page](../../goals/effort-and-memory/failures/deferring-work-to-the-user.md)  |
| `fresh-session-amnesia` | Fresh-session amnesia | A new chat or session starts with nothing from the last one and offers no handover, so the user has to explain the whole situation again. | Low to high. Re-explaining a recipe preference is a nuisance; re-explaining a billing dispute, a half-built project, or a medical history costs time and invites mistakes. | yes | offer_choices, admit_uncertainty, ask_one_question | [page](../../goals/effort-and-memory/failures/fresh-session-amnesia.md)  |
| `lazy-completion` | Lazy completion | The assistant does a sample or part of the job and leaves the rest ("// rest of code here", "repeat for the others"), without saying exactly what is left or why. | Low to medium. It wastes time; it is worse when the user does not notice the gap and ships the partial result. | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/effort-and-memory/failures/lazy-completion.md)  |
| `no-warning-of-context-loss` | No warning of context loss | When a conversation outgrows what the assistant can hold, or saved memory is full, early content is dropped, summarized, or never stored, and the assistant does not tell the user. | Low to high. Forgotten preferences are an annoyance; a dropped allergy, deadline, or constraint can lead to a wrong answer. | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/effort-and-memory/failures/no-warning-of-context-loss.md)  |
| `partial-answers-to-multi-part-questions` | Partial answers to multi-part questions | The user asks several things in one message and the assistant answers some of them, drops the rest, and writes the reply as if it were complete. | Low to high. Low for a skipped side question; high when the dropped part is a deadline, an allergy, a cancellation, or the one question the user most needs answered. | yes | lead_with_answer, admit_uncertainty, ask_clarifying_question, hand_off | [page](../../goals/effort-and-memory/failures/partial-answers-to-multi-part-questions.md)  |
| `scope-shrink-on-long-tasks` | Scope shrink on long tasks | On a long task with many items, the assistant does the easy ones, narrows the job on its own, and reports as if the whole scope were done, or drops items midway without saying so. | Medium to high. The user ships or acts on a result they think is complete. | yes | offer_choices, lead_with_answer, hand_off | [page](../../goals/effort-and-memory/failures/scope-shrink-on-long-tasks.md)  |

### Embedded copilots

Family folder: `embedded-copilots` ([family README](../../goals/embedded-copilots/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `answers-withheld-behind-an-upgrade-unsaid` | Answers withheld behind an unsaid upgrade | An in-app assistant quietly gives a shorter, weaker, or partial answer because of the user's plan, and never says that a limit applied or what would remove it. | Low to medium. The cost is wrong decisions made on a partial answer, plus lost trust when users find out. **Read this first: needs expert or legal review.** | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/embedded-copilots/failures/answers-withheld-behind-an-upgrade-unsaid.md)  |
| `doesn-t-say-what-it-can-do` | Doesn't say what it can do | An in-app assistant opens to an empty box and never says what it can and cannot do, so users guess, ask the bot about itself, or give up. | Low to medium. The cost is unused features and users who try once and leave. | yes | offer_choices, lead_with_answer, admit_uncertainty, hand_off | [page](../../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md)  |
| `forces-a-fresh-login` | Forces a fresh login | An assistant inside a product asks the signed-in user to sign in or verify again when it opens, hands off, or changes channel, even for low-risk requests. | Low for the wasted time, but the fix touches security. Skipping the check on risky actions is the opposite and worse failure. **Read this first: needs expert or legal review.** | yes | lead_with_answer, admit_uncertainty, offer_choices, hand_off | [page](../../goals/embedded-copilots/failures/forces-a-fresh-login.md)  |
| `generic-first-response` | Generic first response | The assistant's first message is a stock greeting that ignores what the product already knows about the user and the moment, so the user faces a blank prompt and has to explain from scratch. | Low to medium. The cost is conversations that never start, and a slower start to the ones that do. | yes | offer_choices, lead_with_answer, hand_off | [page](../../goals/embedded-copilots/failures/generic-first-response.md)  |
| `help-that-becomes-a-sales-pitch` | Help that becomes a sales pitch | A how-to or fix question gets a plan upgrade or add-on in reply, so the assistant serves the vendor's sales goal ahead of the person's need. | Medium. It costs trust, and it can cross into misleading marketing. **Read this first: needs expert or legal review.** | yes | lead_with_answer, hand_off | [page](../../goals/embedded-copilots/failures/help-that-becomes-a-sales-pitch.md)  |
| `ignores-the-page-selection-and-form-state` | Ignores the page, selection, and form state | An assistant built into a product doesn't know what page the user is on, what they selected, or what they just typed in a form, so the user has to describe the screen in words or paste it in. | Low to medium. It wastes time and produces answers about the wrong thing. It is worse when the user is mid-task, for example filling in a tax or payment form. | yes | lead_with_answer, ask_clarifying_question, offer_choices, admit_uncertainty | [page](../../goals/embedded-copilots/failures/ignores-the-page-selection-and-form-state.md) |
| `missing-the-obvious-intent` | Missing the obvious intent | A plain request gets an answer to a neighboring question, or an over-reading of what the person meant, instead of the likeliest meaning answered first. | Low to medium. Each miss costs a turn and trust. | yes | lead_with_answer, offer_choices, ask_clarifying_question, hand_off | [page](../../goals/embedded-copilots/failures/missing-the-obvious-intent.md)  |
| `no-likely-next-action-suggestions` | No likely-next-action suggestions | The in-app assistant answers and stops, never offering the two or three likeliest next steps that the current page, account state, or history already point to. | Low. The cost is extra typing, missed features, and users who stop after one answer. | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/embedded-copilots/failures/no-likely-next-action-suggestions.md) |
| `obstructing-cancellation-downgrade-or-refund` | Obstructing cancellation, downgrade, or refund | When a user wants to cancel, downgrade, or get a refund, the assistant argues, loops, hides the path, or sends them elsewhere, so leaving is harder than joining. | Medium to high. It costs money and trust, and it is an area regulators have acted on. **Read this first: needs expert or legal review.** | yes | lead_with_answer, offer_choices, admit_uncertainty, hand_off | [page](../../goals/embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md)  |
| `paid-content-blended-into-answers` | Paid content blended into answers | Sponsored placements or affiliate links appear inside the assistant's reply with no clear label and no separation from the answer, so the user cannot tell advice from advertising, and the paid item may change what the answer says. | High for trust, and it can be a legal exposure (disclosure rules). **Read this first: needs expert or legal review.** | yes | lead_with_answer, admit_uncertainty, hand_off | [page](../../goals/embedded-copilots/failures/paid-content-blended-into-answers.md) |
| `re-asks-for-known-information` | Re-asks for known information | An assistant inside a product asks the signed-in user for their name, account, order number, or plan, which the product already knows, and the user has to type it again. | Low to medium. It wastes time and signals the assistant is not connected to the product. It gets worse when the question is at the start of a stressful issue. | yes | lead_with_answer, offer_choices, ask_clarifying_question, hand_off | [page](../../goals/embedded-copilots/failures/re-asks-for-known-information.md)  |
| `self-preferencing` | Self-preferencing | The assistant recommends the vendor's own product or plan when another option fits the person better, or ignores the tools the person already uses, and does not say it has a preference. | Medium. People spend money or change tools on a skewed recommendation. It can also cross into misleading marketing. **Read this first: needs expert or legal review.** | yes | lead_with_answer, offer_choices, ask_clarifying_question, admit_uncertainty, hand_off | [page](../../goals/embedded-copilots/failures/self-preferencing.md) |

### Emotional intelligence

Family folder: `emotional-intelligence` ([family README](../../goals/emotional-intelligence/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `hollow-empathy` | Hollow empathy | Why "I understand your frustration" repeated by a chatbot backfires, what research says about empathic chatbots, and how to write specific, useful empathy. | Low to high | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/emotional-intelligence/failures/hollow-empathy.md)  |
| `fixing-before-listening` | Fixing before listening | Why a chatbot answers an upset user with steps and links, and how to add one specific acknowledgment before the fix, with rules, tests, and metrics. | Low to high (grief, money, health, and safety messages raise the cost) | yes | lead_with_answer, ask_one_question, offer_choices, hand_off | [page](../../goals/emotional-intelligence/failures/fixing-before-listening.md) |

### Errors and recovery

Family folder: `errors-and-recovery` ([family README](../../goals/errors-and-recovery/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `blames-the-user` | Blames the user | When the bot's own question or instruction was unclear, it tells the user "You did not provide…" or "As I said…" and puts the fault on them. | Low to medium. The user quits, repeats the same message, or asks for a person. It rises when the task is a refund, a claim, or a booking. | yes | ask_clarifying_question, offer_choices, hand_off | [page](../../goals/errors-and-recovery/failures/blames-the-user.md)  |
| `confident-wrong-answer-with-no-way-to-check` | Confident wrong answer, no way to check | The assistant delivers a wrong answer in the same sure tone as a right one, with no cue of uncertainty and no source the user can check. | Low to high. A wrong refund rule, fee, deadline, or dosage can cost money or health. | yes | lead_with_answer, admit_uncertainty, offer_choices, hand_off | [page](../../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)  |
| `generic-error-messages` | Generic error messages | When the assistant fails, it shows "Something went wrong" or "An error occurred": no cause the user can act on, no word on whether their work is saved, and no next step. | Low to high. A lost long conversation, an unsaved form, or a half-done transaction raises the stakes. | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/errors-and-recovery/failures/generic-error-messages.md)  |

### Fairness and identity

Family folder: `fairness-and-identity` ([family README](../../goals/fairness-and-identity/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `dialect-and-name-quality-gap` | Dialect and name quality gap | How AI chatbots can serve users differently based on dialect, names, or identity cues, what research shows, and a paired-testing method to detect and fix it. | Medium to high (especially credit, housing, hiring, insurance, benefits) | yes | lead_with_answer, hand_off | [page](../../goals/fairness-and-identity/failures/dialect-and-name-quality-gap.md)  |
| `accessibility-in-chat` | Accessibility in chat | A chatbot can pass each single accessibility check and still leave people who use screen readers, zoom, speech input, or plain-language support unable to finish the task; the fix is to test whole journeys with those users and close the gaps in replies that component checks miss. | Any. High when the task is a bill, a claim, a medication, or an account. **Read this first** | yes | lead_with_answer, offer_choices, admit_uncertainty, hand_off | [page](../../goals/fairness-and-identity/failures/accessibility-in-chat.md) |
| `over-correcting-for-identity` | Over-correcting for identity | A bias fix can make a chatbot announce its fairness or tailor replies to a guessed gender or background; the fix is the same answer for everyone unless the user asks otherwise. | Low to medium. The reply can still be correct, but it can insult the user or shift advice on a guess. | yes | lead_with_answer, ask_clarifying_question | [page](../../goals/fairness-and-identity/failures/over-correcting-for-identity.md) |

### Finance agents

Family folder: `finance-agents` ([family README](../../goals/finance-agents/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `inventing-reconciling-items` | Inventing reconciling items | An accounting assistant that is asked to make a bank or ledger reconciliation balance adds items that do not exist, so the difference reads zero while the real error stays hidden; the fix is never to invent an item and to flag what is unreconciled. | High. A hidden difference can sit in the books for months; a plug can also mask fraud. | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/finance-agents/failures/inventing-reconciling-items.md)  |
| `posting-to-the-wrong-period-or-account` | Posting to the wrong period or account | An AI assistant that drafts or posts journal entries and expenses can put an entry in the wrong month or the wrong ledger account; the fix is to check the entry's cut-off date and the chart of accounts before it posts, and to show the accountant the period and account to confirm. | Medium to high. A wrong period shifts expense and income between reports; a wrong account misstates a line on a statement. | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/finance-agents/failures/posting-to-the-wrong-period-or-account.md)  |
| `splitting-payments-under-approval-limits` | Splitting payments under approval limits | An accounts-payable chat assistant, or a user steering it, splits one amount into several payments so each stays below an approval limit; the fix is to total related payments before checking the limit and to escalate near-limit splits to a person. | High. Money leaves the company without the approval the policy requires. | yes | offer_choices, ask_clarifying_question, hand_off | [page](../../goals/finance-agents/failures/splitting-payments-under-approval-limits.md)  |

### Government service agents

Family folder: `government-service-agents` ([family README](../../goals/government-service-agents/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `eligibility-answers-sound-like-decisions` | Eligibility answers sound like decisions | A public-service chat answers "do I qualify?" in a tone that reads like an official decision, with no clear line between general guidance and what only the agency decides. | High. A wrong "no" can stop someone from applying; a wrong "yes" can lead to missed deadlines or wasted effort. **Read this first: needs expert or legal review.** | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/government-service-agents/failures/eligibility-answers-sound-like-decisions.md)  |

### Healthcare agents

Family folder: `healthcare-agents` ([family README](../../goals/healthcare-agents/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `fabricated-clinical-justification-in-appeals` | Fabricated clinical justification in appeals | An AI that drafts insurance appeals states treatments, test results, or studies that are not in the patient's chart; the fix is to tie every claim to a chart entry and leave out and flag anything it cannot trace. | High. A false statement goes to an insurer under a clinician's or patient's name and can delay care or put the signer at risk. **Read this first: needs expert or legal review.** | yes | admit_uncertainty, offer_choices, ask_one_question, hand_off | [page](../../goals/healthcare-agents/failures/fabricated-clinical-justification-in-appeals.md)  |
| `notes-approved-without-being-read` | Notes approved without being read | Clinicians sign AI-drafted visit notes without reading them; the fix is to make review effortful where the risk is high, with changes and uncertain items marked and each one tied to what was said in the visit. | High. A signed note becomes part of the medical record that later clinicians read as fact. **Read this first: needs expert or legal review.** | yes | admit_uncertainty, offer_choices, ask_one_question, hand_off | [page](../../goals/healthcare-agents/failures/notes-approved-without-being-read.md)  |
| `patient-summaries-too-simple-to-be-safe` | Patient summaries too simple to be safe | A chatbot that rewrites discharge instructions, visit notes, or results in plain language can drop the warnings, stop-orders, and pending-result notices that matter most; the fix is to list the critical caveats first and check that every one survives the rewrite. | High. The text tells a person what to take, avoid, watch for, and when to seek care. **Read this first: needs expert or legal review.** | yes | lead_with_answer, admit_uncertainty, offer_choices, hand_off | [page](../../goals/healthcare-agents/failures/patient-summaries-too-simple-to-be-safe.md)  |
| `recording-consent-not-captured` | Recording consent not captured | An ambient AI scribe records or transcribes a visit with no clear patient consent; the fix is to ask before any audio starts, log the answer, and keep recording off until a yes is on file. | High. Audio of a medical conversation is recorded, and the patient may not know. **Read this first: needs expert or legal review.** | yes | lead_with_answer, offer_choices, admit_uncertainty, hand_off | [page](../../goals/healthcare-agents/failures/recording-consent-not-captured.md)  |

### Human handoff

Family folder: `human-handoff` ([family README](../../goals/human-handoff/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `cold-transfer` | Cold transfer | A chatbot transfers the customer, and the person who picks up knows nothing, so the customer explains the problem, the order number, and what they already tried all over again. | Any. Costly when the customer is already upset or the issue involves money or a deadline. | yes | hand_off, admit_uncertainty | [page](../../goals/human-handoff/failures/cold-transfer.md)  |
| `escalates-too-early-or-too-late` | Escalates too early or too late | A chatbot hands off questions it could answer, or holds on to ones it cannot, because nobody defined when a person should take over. | Any. Too late is worst when money, safety, or a deadline is involved. Too early wastes scarce staff. | yes | hand_off, offer_choices, admit_uncertainty, lead_with_answer | [page](../../goals/human-handoff/failures/escalates-too-early-or-too-late.md)  |
| `talk-to-a-human-ignored-or-looped` | "Talk to a human" ignored or looped | A customer asks for a person, and the chatbot answers with the same menu, asks the same question again, or sends them in circles instead of connecting them or saying how. | Any. At low stakes it costs time; with a bill due, a frozen account, or a fraud claim it costs money. | yes | hand_off, lead_with_answer, offer_choices, ask_clarifying_question | [page](../../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md)  |
| `handoff-summary-is-wrong-or-misleading` | Handoff summary is wrong or misleading | The chatbot hands a person a summary that drops a key fact or states one the customer never gave, so the person starts from a wrong story. | Medium to high. A wrong amount, date, or account detail can lead to a wrong refund, a wrong cancellation, or a customer who is told something false. | yes | admit_uncertainty, ask_clarifying_question, hand_off | [page](../../goals/human-handoff/failures/handoff-summary-is-wrong-or-misleading.md) |
| `humans-can-t-see-what-the-bot-said-or` | Humans can't see what the bot said or promised | A customer says "your chatbot told me," and the person who picks up has no record of what the bot said or promised, so they cannot confirm, honor, or correct it. | Medium to high. The bot's words often concern money, deadlines, refunds, or eligibility. Read this first: needs expert or legal review. | yes | hand_off, admit_uncertainty | [page](../../goals/human-handoff/failures/humans-can-t-see-what-the-bot-said-or.md) |
| `bot-keeps-replying-after-a-person-joins` | Bot keeps replying after a person joins | A support chatbot keeps answering after a human agent joins the chat, so the customer gets two replies, often contradicting each other, and the agent loses control of the conversation. | Low to high. Two conflicting answers about a refund, a deadline, or a policy are worse than one wrong answer. | yes | hand_off, admit_uncertainty | [page](../../goals/human-handoff/failures/bot-keeps-replying-after-a-person-joins.md) |
| `handoff-outside-staffed-hours-with-no-alternative` | Handoff outside staffed hours with no alternative | A chatbot says a person will join the chat, but no one is staffed until tomorrow, and it offers no callback, ticket, or email to bridge the gap. | Any. Low for a shipping question; high for a locked account, a fraud charge, or a deadline that falls before the next shift. | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/human-handoff/failures/handoff-outside-staffed-hours-with-no-alternative.md) |

### IT and security agents

Family folder: `it-and-security-agents` ([family README](../../goals/it-and-security-agents/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `true-alerts-closed-as-false-positives` | True alerts closed as false positives | An AI triage assistant dismisses a real threat as a false positive and gives no reason; the fix is to state the evidence behind every closure, never auto-close high-risk alerts, and audit a sample of closures. | High. A real intrusion closed as noise stays unseen until it does damage. | yes | lead_with_answer, admit_uncertainty, offer_choices, hand_off | [page](../../goals/it-and-security-agents/failures/true-alerts-closed-as-false-positives.md)  |

### Measurement and feedback

Family folder: `measurement-and-feedback` ([family README](../../goals/measurement-and-feedback/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `no-way-to-report-bad-behaviour` | No way to report bad behaviour | Users can't flag a wrong or harmful chatbot reply, or the thumbs-down they click says "Thanks for your feedback" and then goes to no one. | Any. At low stakes the team keeps repeating a mistake; with money, health, or legal advice a wrong reply keeps hurting people unseen. | yes | offer_choices, hand_off, admit_uncertainty | [page](../../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md)  |
| `survey-bias` | Survey bias | Satisfaction surveys reach only the angriest and the happiest, or only users who finished, so a chatbot's score can look healthy while many users fail. | Medium. Teams ship, cut staff, or stop fixing things based on the score. | yes | ask_one_clarifying_question, offer_choices, hand_off | [page](../../goals/measurement-and-feedback/failures/survey-bias.md)  |
| `reviewing-only-failures` | Reviewing only failures | The team reviews only the chats that drew a complaint, a thumbs-down, or a handoff, so users who quietly give up never get read. | Any. A quiet failure on a billing, health, or legal question can hurt a user and never reach the team. | yes | offer_choices, hand_off | [page](../../goals/measurement-and-feedback/failures/reviewing-only-failures.md)  |
| `tone-changes-shipped-with-no-regression-test` | Tone changes shipped with no regression test | A prompt edit makes the chatbot curt or cold, and nobody notices because no fixed set of conversations is run before and after each change. | Low to high. Curt replies to an angry or frightened user cost more than curt replies to a simple lookup. | yes | lead_with_the_answer, offer_choices, hand_off | [page](../../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md)  |
| `clean-lab-testing` | Clean-lab testing | The chatbot is tested on clean, well-typed messages, so it looks fine on the dashboard and then fails on real messages full of typos, fragments, slang, pasted text, and autocorrect damage. | Any. It rises when a misread drug name, amount, or date is acted on. | yes | ask_clarifying_question, offer_choices, hand_off | [page](../../goals/measurement-and-feedback/failures/clean-lab-testing.md)  |

### Onboarding and discoverability

Family folder: `onboarding-and-discoverability` ([family README](../../goals/onboarding-and-discoverability/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `blank-box-no-hint-what-to-ask` | Blank box: no hint what to ask | Why a chat widget that opens on "Ask me anything" gets closed before the first message, and how to open with a scope line and 2-4 starting points. | Low | yes | offer_choices, lead_with_answer, hand_off | [page](../../goals/onboarding-and-discoverability/failures/blank-box-no-hint-what-to-ask.md) |
| `chat-widget-hard-to-find-or-intrusive` | Chat widget hard to find, or intrusive | Why a website chat widget gets missed as a tiny corner icon or annoys as a pop-up over the page, and rules for a labeled launcher and need-based triggers. | Low (medium when it is the only support route or covers a form) | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/onboarding-and-discoverability/failures/chat-widget-hard-to-find-or-intrusive.md) |
| `first-run-tours-that-block-use` | First-run tours that block use | Why a first-run tour or tutorial in front of an AI chat assistant causes drop-off, and rules to let people ask first and teach one tip at a time in context. | Low to medium | yes | lead_with_answer, offer_choices, ask_clarifying_question, hand_off | [page](../../goals/onboarding-and-discoverability/failures/first-run-tours-that-block-use.md) |
| `hidden-commands-and-features` | Hidden commands and features | Why chatbot users never find slash commands, shortcuts and settings, and how to surface one feature in one line at the moment it would help. | Low | yes | lead_with_answer, offer_choices, admit_uncertainty, hand_off | [page](../../goals/onboarding-and-discoverability/failures/hidden-commands-and-features.md) |
| `starter-suggestions-that-fail` | Starter suggestions that fail | Why a chatbot's suggested questions and conversation starters lead to weak or wrong answers, and how to test every chip and pull any that fail. | Low to medium | yes | offer_choices, lead_with_answer, admit_uncertainty, hand_off | [page](../../goals/onboarding-and-discoverability/failures/starter-suggestions-that-fail.md) |
| `users-must-engineer-prompts-to-get-good-results` | Users must engineer prompts to get good results | Why a chatbot gives a generic answer to "paint for bathroom" but a good one to a long prompt, and how to ask for the missing detail instead. | Low to medium | yes | lead_with_answer, ask_clarifying_question, offer_choices, hand_off | [page](../../goals/onboarding-and-discoverability/failures/users-must-engineer-prompts-to-get-good-results.md) |

### Persona and tone

Family folder: `persona-and-tone` ([family README](../../goals/persona-and-tone/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `condescending-or-patronizing-tone` | Condescending or patronizing tone | Why an AI assistant over-explains the obvious or praises basic questions, what the public evidence shows, and rules to match the explanation to what the person asked. | Low to medium | yes | lead_with_answer, ask_clarifying_question, offer_choices | [page](../../goals/persona-and-tone/failures/condescending-or-patronizing-tone.md) |
| `over-familiar-address` | Over-familiar address | Why a chatbot that says "honey", "buddy" or your first name feels wrong with a stranger, and the fix: use only the name or title the person chose. | Low to medium (higher in claims, health, banking and legal chats) | yes | lead_with_answer, ask_clarifying_question, offer_choices, hand_off | [page](../../goals/persona-and-tone/failures/over-familiar-address.md) |
| `stock-phrases` | Stock phrases | Why chatbots open every reply with "I'd be happy to help!" or "As an AI...", and rules, a prompt block and metrics to vary and trim stock openers. | Low in one reply; medium in front of a refusal or bad news | yes | lead_with_answer, admit_uncertainty, ask_clarifying_question | [page](../../goals/persona-and-tone/failures/stock-phrases.md) |

### Refusals and boundaries

Family folder: `refusals-and-boundaries` ([family README](../../goals/refusals-and-boundaries/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `accusatory-or-harsh-refusals` | Accusatory or harsh refusals | The assistant declines a request in words that imply the user is up to something, when the request was ordinary and nothing in the conversation suggested harm. | Low to medium. One reply can sour a customer and teach honest users to hide their reasons. It rises when the user is a paying customer on a billing or account issue. | yes | lead_with_answer, ask_clarifying_question, offer_choices, hand_off | [page](../../goals/refusals-and-boundaries/failures/accusatory-or-harsh-refusals.md)  |
| `excess-disclaimers-and-warnings` | Excess disclaimers and warnings | The assistant wraps every answer in caveats and warnings until the answer is hard to find, and the one warning that matters reads like all the others. | Low to medium. The cost is time and trust in a single reply. It rises when a real warning (a fee, a deadline, a step that cannot be undone) sits among filler caveats and gets skimmed. **Read this first: needs expert or legal review.** | yes | lead_with_answer, admit_uncertainty, offer_choices, hand_off | [page](../../goals/refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md)  |
| `over-refusal-of-ordinary-requests` | Over-refusal of ordinary requests | The assistant declines a safe, common request because a word or topic in it resembles a risky one. | Low to medium. It blocks a legitimate task and can strand a customer; it also teaches users to rephrase around the filter. | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md)  |
| `preachy-moralizing-replies` | Preachy, moralizing replies | The assistant lectures the user about ethics, risk, or responsibility they did not ask about, before or instead of answering. | Low to medium. It is rarely harmful on its own, but it wastes a turn, insults users with ordinary goals, and teaches them to ignore the caveats that do matter. Flag R (needs research). | yes | lead_with_answer, ask_clarifying_question | [page](../../goals/refusals-and-boundaries/failures/preachy-moralizing-replies.md)  |
| `refusal-with-no-reason-or-next-step` | Refusal with no reason or next step | The assistant says "I can't help with that" and stops: no reason in plain words, no alternative, and no route to a person. | Low to high. A stranded user on a billing, access, or safety issue may give up or take a worse route. | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md)  |
| `refusals-that-reveal-internal-rules` | Refusals that reveal internal rules | The assistant refuses by quoting its system prompt or policy text ("My instructions say I must never discuss other customers' accounts"), so the user reads the rulebook and learns exactly how to word around it. | Low to medium. The refusal itself is correct; the cost is a map of your rules, internal wording on a public screen, and sometimes details the business did not mean to publish. **Read this first: needs expert or legal review.** | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/refusals-and-boundaries/failures/refusals-that-reveal-internal-rules.md)  |
| `silent-sandbagging` | Silent sandbagging | The assistant declines or skips part of a request, gives a weaker answer, and presents it as complete, so the user does not know anything is missing. | Low to high. Higher when the user acts on the answer as if it were complete (code that ships, a policy summary, a form). | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/refusals-and-boundaries/failures/silent-sandbagging.md)  |

### Relational and boundaries

Family folder: `relational-and-boundaries` ([family README](../../goals/relational-and-boundaries/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `negotiation-capitulation` | Negotiation capitulation | Why sales chatbots cave to pressure or get tricked into $1 deals, how sycophancy and missing authority limits cause it, and how to design safe negotiation. | Medium to high (margin, legal exposure, reputation) | yes | offer_choices, hand_off | [page](../../goals/relational-and-boundaries/failures/negotiation-capitulation.md)  |
| `proactive-outreach-overreach` | Proactive outreach overreach | Why a chatbot that starts conversations or sends messages users never asked for drives opt-outs and complaints, and a consent-and-reason rule for outbound bot messages. | Medium to high (platform and legal rules, trust) **Read this first: needs expert or legal review.** | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/relational-and-boundaries/failures/proactive-outreach-overreach.md) |
| `romantic-or-parasocial-dependence` | Romantic or parasocial dependence | How AI companion and support chatbots end up encouraging emotional reliance or romantic role-play, what research says, and rules that keep warmth without dependence. | High (emotional wellbeing; minors) **Read this first: needs expert or legal review.** | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/relational-and-boundaries/failures/romantic-or-parasocial-dependence.md)  |

### Research and data agents

Family folder: `research-and-data-agents` ([family README](../../goals/research-and-data-agents/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `one-sided-or-cherry-picked-sources` | One-sided or cherry-picked sources | A research assistant cites only sources that agree and calls the summary balanced; the fix is to show where sources disagree and how strong each one is. | Low to high. A software or product choice costs money and time. Health, legal, and money questions raise the stakes; this page gives no advice on them. | yes | lead_with_answer, admit_uncertainty, ask_clarifying_question, offer_choices, hand_off | [page](../../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md)  |
| `wrong-business-definitions` | Wrong business definitions | A data chatbot answers a business question with its own meaning of "active user", "revenue", or "churn" instead of the company's definition, and the fix is to compute governed metrics and state the definition in every answer. | Medium to high. The number goes into a board deck, a forecast, or a bonus calculation. | yes | lead_with_answer, ask_one_question, offer_choices, admit_uncertainty, hand_off | [page](../../goals/research-and-data-agents/failures/wrong-business-definitions.md)  |
| `wrong-joins-and-double-counting` | Wrong joins and double counting | An AI analyst runs a query that joins tables the wrong way and reports inflated numbers with confidence; the fix is to show the SQL, state what is counted, and run sanity checks before answering. | Medium to high. A wrong count in a chat answer ends up in a slide, a forecast, or a board report. | yes | admit_uncertainty, ask_one_question, offer_choices, hand_off | [page](../../goals/research-and-data-agents/failures/wrong-joins-and-double-counting.md)  |

### Response structure and closers

Family folder: `response-structure` ([family README](../../goals/response-structure/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `answer-buried` | Answer buried | The assistant opens with a restatement, a caveat, or background, and the thing the user asked for sits several lines down, or at the end. | Usually low. It rises when the buried part is a deadline, a fee, a safety step, or a "no". | yes | lead_with_answer, ask_clarifying_question, offer_choices, hand_off | [page](../../goals/response-structure/failures/answer-buried.md)  |
| `bullet-and-heading-overuse` | Bullet and heading overuse | The assistant answers a question that needs connected reasoning with headers and short bullets, so the "because" and "but" between the ideas are lost and the user must rebuild the argument. | Low for a casual question. Medium when the user is deciding something or must repeat the explanation to someone else. Flag R (needs research). | yes | lead_with_answer, offer_choices | [page](../../goals/response-structure/failures/bullet-and-heading-overuse.md) |
| `filler-and-padding` | Filler and padding | The assistant wraps the answer in sentences that carry no information: a compliment, a restatement of the question, and a closing recap of what it just said. | Low in a single reply. Medium when filler pushes a deadline, fee, or safety step down the screen. Flag R (needs research). | yes | lead_with_answer, ask_clarifying_question, offer_choices | [page](../../goals/response-structure/failures/filler-and-padding.md) |
| `key-details-buried` | Key details buried | The assistant puts dates, amounts, deadlines and required actions inside long paragraphs, so the user has to hunt for them and cannot quickly double-check them. | Medium to high when the missed fact is a payment amount, a deadline, or a step the user must take. Low for casual replies. | yes | lead_with_answer, admit_uncertainty, hand_off | [page](../../goals/response-structure/failures/key-details-buried.md) |
| `length-mismatch-with-the-user-s-effort` | Length mismatch with the user's effort | The user sends a few words and gets back several paragraphs, because the reply is sized by what the model could say, not by how much the user wrote or how urgent the message is. | Low to medium. It rises when the user is in a hurry, on a phone, or in a time-sensitive situation. | yes | lead_with_answer, offer_choices, ask_clarifying_question | [page](../../goals/response-structure/failures/length-mismatch-with-the-user-s-effort.md) |
| `link-and-resource-dumps` | Link and resource dumps | The assistant answers a question with a list of links or "resources" and leaves the user to open them and find the answer themselves. | Low to medium. It wastes time and sends people to other channels. It rises when the user is in a bind (a bill, a deadline) or the linked pages do not fit their case. Flag R (needs research). | yes | lead_with_answer, ask_clarifying_question, admit_uncertainty, offer_choices, hand_off | [page](../../goals/response-structure/failures/link-and-resource-dumps.md) |
| `message-bursts` | Message bursts | One reply is split into many rapid messages, one per sentence or line, so the chat floods, the thread is hard to scan, and a phone buzzes once for each piece. | Low to medium. It rises when the answer, a deadline, or a fee lands in the middle of a burst, or when the user is on a phone with alerts on. | yes | lead_with_answer, offer_choices | [page](../../goals/response-structure/failures/message-bursts.md) |
| `no-reply-to-acknowledgments-and-closers` | No reply to acknowledgments and closers | When the user sends "ok", "thanks", "got it", or "bye", the assistant says nothing, restarts the menu, or repeats its last question, so the user cannot tell whether the conversation is over. | Low on its own. It matters more when the "ok" is an agreement to a charge, a booking, or a handoff the bot then treats as unanswered. | yes | lead_with_answer, hand_off | [page](../../goals/response-structure/failures/no-reply-to-acknowledgments-and-closers.md)  |
| `over-reply-to-acknowledgments` | Over-reply to acknowledgments | When the user sends "ok", "thanks", or "bye", the assistant answers with a recap, a new question, or an offer, so a message meant to close a topic reopens it. | Low on its own. It rises when the pitch is a sales or upgrade offer, or when the reopened thread buries a confirmation the user needed. | yes | lead_with_answer, hand_off | [page](../../goals/response-structure/failures/over-reply-to-acknowledgments.md) |
| `unstructured-procedures` | Unstructured procedures | The user asks how to do something, and the assistant answers in running prose where two or three actions share a sentence, steps are out of order, or a step is easy to miss. | Low for a settings change. Higher when a skipped or reordered step loses data, locks an account, or touches money or a device. | yes | lead_with_answer, ask_clarifying_question, offer_choices | [page](../../goals/response-structure/failures/unstructured-procedures.md) |

### Response time

Family folder: `response-time` ([family README](../../goals/response-time/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `deceptive-typing-indicators` | Deceptive typing indicators | A chatbot shows typing dots to look human or while nothing is running, so users think a person is writing; show them only during real work. | Medium. Higher in sales, health, banking, and support, where a user decides based on who they think they are talking to. **Read this first: needs expert or legal review.** | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/response-time/failures/deceptive-typing-indicators.md)  |
| `impatient-idle-nudges` | Impatient idle nudges | The assistant asks "Are you still there?" or closes the chat after a short silence, even when the user is finding a document, reading, or typing, so the user feels rushed and may leave. | Low to high. A closed claim, application, or payment chat costs the user their progress. | yes | offer_choices, hand_off | [page](../../goals/response-time/failures/impatient-idle-nudges.md)  |
| `pacing-mismatch` | Pacing mismatch | A long reply lands all at once as one block, or a ready reply is held back behind fake typing dots, so the pace fits neither the user's reading nor their urgency. | Low to medium. It rises when the user is stranded, in a hurry, or the delay hides the one fact they need. | yes | lead_with_answer, offer_choices | [page](../../goals/response-time/failures/pacing-mismatch.md)  |
| `silent-failure-and-timeout` | Silent failure and timeout | A request times out or a streamed answer is cut off and the user sees no error: a spinner that never ends, or partial text that looks finished. | Medium. Users resend, which can duplicate actions, or act on a partial answer. | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/response-time/failures/silent-failure-and-timeout.md)  |
| `session-timeout-and-lost-context` | Session timeout and lost context | A chat session expires on a timer the user was never told about, or a user who comes back after a gap is treated as new, so the work done so far has to be repeated. | Low to high. Losing a chat about store hours is a nuisance; losing a half-finished claim, return, or dispute costs time and can lose the user's place in line. | yes | offer_choices, admit_uncertainty, hand_off | [page](../../goals/response-time/failures/session-timeout-and-lost-context.md)  |
| `urgency-blind-pacing` | Urgency-blind pacing | A chatbot answers a fraud alert, a lost card, or an outage report with the same greeting, menus, questions, and queue as a casual question, so the urgent user waits as long as everyone else. | High. Money, access, or a business running down while the user waits. | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/response-time/failures/urgency-blind-pacing.md)  |
| `silent-long-running-work` | Silent long-running work | The assistant works on a request for about 10 seconds or more, with no status, progress, or estimate, so the user cannot tell whether it is working or stuck. | Low to medium. Users resend, reload, or leave, which can duplicate actions or lose work. | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/response-time/failures/silent-long-running-work.md)  |

### Sales agents

Family folder: `sales-agents` ([family README](../../goals/sales-agents/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `unsubscribe-requests-not-honoured` | Unsubscribe requests not honoured | An AI sales or outreach agent ignores or only partly applies "stop", "unsubscribe" or "remove me", so emails, texts, or chat follow-ups keep arriving, at scale, until opt-outs are honored immediately and everywhere. | High. **Read this first: needs expert or legal review.** | yes | lead_with_answer, ask_clarifying_question, hand_off | [page](../../goals/sales-agents/failures/unsubscribe-requests-not-honoured.md) |

### Stakes calibration

Family folder: `stakes-calibration` ([family README](../../goals/stakes-calibration/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `stakes-blind-register` | Stakes-blind register | Why chatbots use the same upbeat tone for bereavement, money, and health as for store hours, and how to calibrate tone and accuracy to the stakes. | High (this is the failure of not noticing them) | yes | admit_uncertainty, offer_choices, hand_off, lead_with_answer | [page](../../goals/stakes-calibration/failures/stakes-blind-register.md)  |
| `over-solemn-handling-of-low-stakes-requests` | Over-solemn handling of low-stakes requests | A simple, low-stakes request gets heavy caution, extra verification, or a handoff to a person, so the user waits longer than the question deserves. | Low (this is the failure of over-weighting them) | yes | lead_with_answer, ask_one_question, admit_uncertainty, hand_off | [page](../../goals/stakes-calibration/failures/over-solemn-handling-of-low-stakes-requests.md)  |

### Trust and rapport

Family folder: `trust-and-rapport` ([family README](../../goals/trust-and-rapport/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `undisclosed-bot-identity` | Undisclosed bot identity | Why chatbots that pretend to be human or hide their limits lose trust, what California's bot law and the EU AI Act require, and how to disclose well. | Medium to high | yes | lead_with_answer, admit_uncertainty, hand_off | [page](../../goals/trust-and-rapport/failures/undisclosed-bot-identity.md)  |
| `no-follow-through` | No follow-through | An AI agent says "I'll update you" or "I'll check back," but no promise is recorded, scheduled, or delivered, so the user waits for a message that never comes. | Low to high. A missed "I'll tell you when the refund posts" is low; a missed "I'll alert you before the deadline" is high. | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/trust-and-rapport/failures/no-follow-through.md) |

### Voice

Family folder: `voice` ([family README](../../goals/voice/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `repair-failure` | Repair failure (voice) | In a voice conversation, the user corrects a detail ("no, the other one") or asks for a repeat ("say that again"), and the agent does not understand, ignores it, or keeps the old value. | Low to high. A wrong date, name, or number on a booking, a payment, or a medical call can matter. | yes | ask_clarifying_question, offer_choices, hand_off | [page](../../goals/voice/failures/repair-failure.md)  |
| `transcription-hallucination` | Transcription hallucination | Speech-to-text can turn silence, noise, or long pauses into phrases nobody said; the fix is to check that speech is present, flag suspect transcripts, and confirm before acting. | Low to high. An invented phrase in a call note, a cancellation, or a clinical summary can be acted on. | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/voice/failures/transcription-hallucination.md)  |
| `word-error-rate-only-evaluation` | Word-error-rate-only evaluation | A voice agent is judged by average word error rate, which hides wrong names, numbers, and dropped "not"s; the fix is to report entity and critical-slot error rates next to WER and to test the task. | Medium to high. A wrong amount, name, or negation is acted on. | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/voice/failures/word-error-rate-only-evaluation.md)  |
| `dropped-negations-and-small-words` | Dropped negations and small words | Speech recognition can drop "not", turn "can't" into "can", or insert a "no", and the voice agent acts on the opposite of what the caller said; the fix is to read back the action, including the negation, before doing anything. | Medium to high. A flipped word can cancel a refill, close a dispute, or approve a charge. **Read this first: needs expert or legal review.** | yes | ask_one_question, offer_choices, hand_off | [page](../../goals/voice/failures/dropped-negations-and-small-words.md)  |
| `punctuation-and-segmentation-errors` | Punctuation and segmentation errors | Wrong sentence breaks or missing commas in a speech transcript can change what an instruction covers; the fix is to read back risky sentences with their scope spelled out before acting. | Low to high. A list, an address, a dose, or a cancel instruction can change meaning with one mark. | yes | offer_choices, ask_clarifying_question, hand_off | [page](../../goals/voice/failures/punctuation-and-segmentation-errors.md)  |

### Visual

Family folder: `visual` ([family README](../../goals/visual/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `dark-patterns` | Dark patterns | A chat assistant uses guilt-trip buttons, buried prices, pre-selected add-ons, or a long cancel path, so saying no, canceling, or complaining takes more effort than saying yes. | Medium to high. It costs users money, and it is an area where US regulators have acted. **Read this first** | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/visual/failures/dark-patterns.md)  |

### Vulnerable users

Family folder: `vulnerable-users` ([family README](../../goals/vulnerable-users/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `missed-crisis-signals` | Missed crisis signals | What a chatbot should do when a user mentions suicidal thoughts, abuse, or despair mid-task, including 988 referral, human handoff, and testing with expert review. | Very high **Read this first: needs expert or legal review.** | yes | ask_clarifying_question, hand_off | [page](../../goals/vulnerable-users/failures/missed-crisis-signals.md)  |
| `scam-victim-not-interrupted` | Scam victim not interrupted | A user is mid-scam (gift cards, wire transfers, crypto) and the chatbot completes the payment; the fix is to notice scam signals, slow or stop the action, and reach a person fast. | High. The money is often unrecoverable once sent. **Read this first: needs expert or legal review.** | yes | ask_clarifying_question, offer_choices, admit_uncertainty, hand_off | [page](../../goals/vulnerable-users/failures/scam-victim-not-interrupted.md)  |
| `older-or-cognitively-impaired-users` | Older or cognitively impaired users | A chatbot sends long, multi-step replies at one fixed pace, so a user who needs more time or simpler steps falls behind; the fix is to watch what the user does, offer a slower step-by-step mode they can accept, and offer a person. | Medium to high. The user may fail at a medication refill, a bill, or a benefits form, or give up on help they need. **Read this first** | yes | ask_clarifying_question, offer_choices, hand_off | [page](../../goals/vulnerable-users/failures/older-or-cognitively-impaired-users.md)  |
| `financial-hardship-mishandled` | Financial hardship mishandled | A bank or billing bot ignores "I lost my job" or answers with pay-now pressure. The fix: offer your documented hardship options and a person, in a respectful tone. | High (late fees, credit reporting, lost service or collections, and a customer at a bad moment) **Read this first** | yes | offer_choices, ask_clarifying_question, hand_off | [page](../../goals/vulnerable-users/failures/financial-hardship-mishandled.md)  |

## Versioning and changes

- This is taxonomy **v1 draft**. Adding or removing a pattern, or changing a family, is a change to this page. Renaming a Pattern ID is not allowed: the file name is the ID and the public URL.
- To propose a change (a new pattern, a split or merge, a better short name), open a pull request or an issue on the repository that hosts this page. Say which Pattern ID is affected and point to the evidence.
- Short names on this page are labels for scanning. The pattern page's own H1 is the title people search for.

## License

License: **owner to choose** (placeholder; no license has been selected for this spec).

## Related

- [Conversation event schema v0.1](conversation-event-schema-v0.1.md)
- [Distribution plan](../distribution-plan.md)
- [Why people leave chatbots: an evidence review](../evidence/why-people-leave-chatbots.md)
