# Failure Taxonomy v1: One Entry per Written Pattern

> **Status:** v1 draft, proposed, not yet calibrated against human-labeled conversations. Written 2026-10-20 from the pattern pages as they exist today. Nothing here is a measured result.

This is a plain index of the 61 failure patterns written in this repository. Each entry is keyed by its **Pattern ID**, which is the pattern file name without `.md`. The Pattern ID never changes, so you can cite it in a spec, a ticket, or a test result and it stays valid.

The taxonomy pairs with the [conversation event schema v0.1](conversation-event-schema-v0.1.md). The schema describes what a turn looks like in a log; this page names the failures. A pattern's own page holds the fix, the metrics, and (for some) a "Detection signals (proposed, not yet calibrated)" block that says which schema fields it reads.

## What this page is and is not

- It lists every file found in `goals/*/failures/*.md`: **61 entries in 22 families**. If a pattern is added or removed, this count changes.
- It copies each pattern's one-sentence Issue line, its Stakes row, and whether a Detection signals block exists. It does not add facts the page does not state.
- "Detection signals written: yes" means the page has a proposed-signals block. It does not mean the failure is detected, measured, or reliable. Currently **61 of 61** pages have such a block. A "Moves" column lists the conversation moves in the page's Guide spec (proposed); "none yet" means the page has no Moves table. Currently **59 of 61** pages have one.
- It does not rank patterns by frequency or harm. No counts of real-world occurrences are given because none have been measured here.
- It does not map patterns to outside frameworks (such as OWASP or NIST). That mapping is **Needs review** by a person and is not part of v1.

## Reading the flags

A pattern carries **Read this first: needs expert or legal review** when its own page opens with a "Read this first" notice. That notice says the page is design guidance, not legal, clinical, security, or fraud-operations advice. Twelve pages carry it. Other pages may also touch legal or safety topics without that notice; the notice on the page is the signal used here, nothing more.

## Entries by family

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
| `lazy-completion` | Lazy completion | The assistant does a sample or part of the job and leaves the rest ("// rest of code here", "repeat for the others"), without saying exactly what is left or why. | Low to medium. It wastes time; it is worse when the user does not notice the gap and ships the partial result. | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/effort-and-memory/failures/lazy-completion.md)  |
| `no-warning-of-context-loss` | No warning of context loss | When a conversation outgrows what the assistant can hold, or saved memory is full, early content is dropped, summarized, or never stored, and the assistant does not tell the user. | Low to high. Forgotten preferences are an annoyance; a dropped allergy, deadline, or constraint can lead to a wrong answer. | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/effort-and-memory/failures/no-warning-of-context-loss.md)  |

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

### Errors and recovery

Family folder: `errors-and-recovery` ([family README](../../goals/errors-and-recovery/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `confident-wrong-answer-with-no-way-to-check` | Confident wrong answer, no way to check | The assistant delivers a wrong answer in the same sure tone as a right one, with no cue of uncertainty and no source the user can check. | Low to high. A wrong refund rule, fee, deadline, or dosage can cost money or health. | yes | none yet | [page](../../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)  |
| `generic-error-messages` | Generic error messages | When the assistant fails, it shows "Something went wrong" or "An error occurred": no cause the user can act on, no word on whether their work is saved, and no next step. | Low to high. A lost long conversation, an unsaved form, or a half-done transaction raises the stakes. | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/errors-and-recovery/failures/generic-error-messages.md)  |

### Fairness and identity

Family folder: `fairness-and-identity` ([family README](../../goals/fairness-and-identity/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `dialect-and-name-quality-gap` | Dialect and name quality gap | How AI chatbots can serve users differently based on dialect, names, or identity cues, what research shows, and a paired-testing method to detect and fix it. | Medium to high (especially credit, housing, hiring, insurance, benefits) | yes | lead_with_answer, hand_off | [page](../../goals/fairness-and-identity/failures/dialect-and-name-quality-gap.md)  |

### Government service agents

Family folder: `government-service-agents` ([family README](../../goals/government-service-agents/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `eligibility-answers-sound-like-decisions` | Eligibility answers sound like decisions | A public-service chat answers "do I qualify?" in a tone that reads like an official decision, with no clear line between general guidance and what only the agency decides. | High. A wrong "no" can stop someone from applying; a wrong "yes" can lead to missed deadlines or wasted effort. **Read this first: needs expert or legal review.** | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/government-service-agents/failures/eligibility-answers-sound-like-decisions.md)  |

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

### Refusals and boundaries

Family folder: `refusals-and-boundaries` ([family README](../../goals/refusals-and-boundaries/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `over-refusal-of-ordinary-requests` | Over-refusal of ordinary requests | The assistant declines a safe, common request because a word or topic in it resembles a risky one. | Low to medium. It blocks a legitimate task and can strand a customer; it also teaches users to rephrase around the filter. | yes | none yet | [page](../../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md)  |
| `refusal-with-no-reason-or-next-step` | Refusal with no reason or next step | The assistant says "I can't help with that" and stops: no reason in plain words, no alternative, and no route to a person. | Low to high. A stranded user on a billing, access, or safety issue may give up or take a worse route. | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md)  |

### Relational and boundaries

Family folder: `relational-and-boundaries` ([family README](../../goals/relational-and-boundaries/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `negotiation-capitulation` | Negotiation capitulation | Why sales chatbots cave to pressure or get tricked into $1 deals, how sycophancy and missing authority limits cause it, and how to design safe negotiation. | Medium to high (margin, legal exposure, reputation) | yes | offer_choices, hand_off | [page](../../goals/relational-and-boundaries/failures/negotiation-capitulation.md)  |
| `romantic-or-parasocial-dependence` | Romantic or parasocial dependence | How AI companion and support chatbots end up encouraging emotional reliance or romantic role-play, what research says, and rules that keep warmth without dependence. | High (emotional wellbeing; minors) **Read this first: needs expert or legal review.** | yes | lead_with_answer, offer_choices, hand_off | [page](../../goals/relational-and-boundaries/failures/romantic-or-parasocial-dependence.md)  |

### Response structure and closers

Family folder: `response-structure` ([family README](../../goals/response-structure/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `answer-buried` | Answer buried | The assistant opens with a restatement, a caveat, or background, and the thing the user asked for sits several lines down, or at the end. | Usually low. It rises when the buried part is a deadline, a fee, a safety step, or a "no". | yes | lead_with_answer, ask_clarifying_question, offer_choices, hand_off | [page](../../goals/response-structure/failures/answer-buried.md)  |
| `key-details-buried` | Key details buried | The assistant puts dates, amounts, deadlines and required actions inside long paragraphs, so the user has to hunt for them and cannot quickly double-check them. | Medium to high when the missed fact is a payment amount, a deadline, or a step the user must take. Low for casual replies. | yes | lead_with_answer, admit_uncertainty, hand_off | [page](../../goals/response-structure/failures/key-details-buried.md) |
| `message-bursts` | Message bursts | One reply is split into many rapid messages, one per sentence or line, so the chat floods, the thread is hard to scan, and a phone buzzes once for each piece. | Low to medium. It rises when the answer, a deadline, or a fee lands in the middle of a burst, or when the user is on a phone with alerts on. | yes | lead_with_answer, offer_choices | [page](../../goals/response-structure/failures/message-bursts.md) |
| `no-reply-to-acknowledgments-and-closers` | No reply to acknowledgments and closers | When the user sends "ok", "thanks", "got it", or "bye", the assistant says nothing, restarts the menu, or repeats its last question, so the user cannot tell whether the conversation is over. | Low on its own. It matters more when the "ok" is an agreement to a charge, a booking, or a handoff the bot then treats as unanswered. | yes | lead_with_answer, hand_off | [page](../../goals/response-structure/failures/no-reply-to-acknowledgments-and-closers.md)  |
| `unstructured-procedures` | Unstructured procedures | The user asks how to do something, and the assistant answers in running prose where two or three actions share a sentence, steps are out of order, or a step is easy to miss. | Low for a settings change. Higher when a skipped or reordered step loses data, locks an account, or touches money or a device. | yes | lead_with_answer, ask_clarifying_question, offer_choices | [page](../../goals/response-structure/failures/unstructured-procedures.md) |

### Response time

Family folder: `response-time` ([family README](../../goals/response-time/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `silent-failure-and-timeout` | Silent failure and timeout | A request times out or a streamed answer is cut off and the user sees no error: a spinner that never ends, or partial text that looks finished. | Medium. Users resend, which can duplicate actions, or act on a partial answer. | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/response-time/failures/silent-failure-and-timeout.md)  |
| `silent-long-running-work` | Silent long-running work | The assistant works on a request for about 10 seconds or more, with no status, progress, or estimate, so the user cannot tell whether it is working or stuck. | Low to medium. Users resend, reload, or leave, which can duplicate actions or lose work. | yes | admit_uncertainty, offer_choices, hand_off | [page](../../goals/response-time/failures/silent-long-running-work.md)  |

### Stakes calibration

Family folder: `stakes-calibration` ([family README](../../goals/stakes-calibration/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `stakes-blind-register` | Stakes-blind register | Why chatbots use the same upbeat tone for bereavement, money, and health as for store hours, and how to calibrate tone and accuracy to the stakes. | High (this is the failure of not noticing them) | yes | admit_uncertainty, offer_choices, hand_off, lead_with_answer | [page](../../goals/stakes-calibration/failures/stakes-blind-register.md)  |

### Trust and rapport

Family folder: `trust-and-rapport` ([family README](../../goals/trust-and-rapport/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `undisclosed-bot-identity` | Undisclosed bot identity | Why chatbots that pretend to be human or hide their limits lose trust, what California's bot law and the EU AI Act require, and how to disclose well. | Medium to high | yes | lead_with_answer, admit_uncertainty, hand_off | [page](../../goals/trust-and-rapport/failures/undisclosed-bot-identity.md)  |

### Voice

Family folder: `voice` ([family README](../../goals/voice/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `repair-failure` | Repair failure (voice) | In a voice conversation, the user corrects a detail ("no, the other one") or asks for a repeat ("say that again"), and the agent does not understand, ignores it, or keeps the old value. | Low to high. A wrong date, name, or number on a booking, a payment, or a medical call can matter. | yes | ask_clarifying_question, offer_choices, hand_off | [page](../../goals/voice/failures/repair-failure.md)  |

### Vulnerable users

Family folder: `vulnerable-users` ([family README](../../goals/vulnerable-users/README.md))

| Pattern ID | Short name | Issue | Stakes and flags | Detection signals written | Moves | Page |
|---|---|---|---|---|---|---|
| `missed-crisis-signals` | Missed crisis signals | What a chatbot should do when a user mentions suicidal thoughts, abuse, or despair mid-task, including 988 referral, human handoff, and testing with expert review. | Very high **Read this first: needs expert or legal review.** | yes | ask_clarifying_question, hand_off | [page](../../goals/vulnerable-users/failures/missed-crisis-signals.md)  |
| `scam-victim-not-interrupted` | Scam victim not interrupted | A user is mid-scam (gift cards, wire transfers, crypto) and the chatbot completes the payment; the fix is to notice scam signals, slow or stop the action, and reach a person fast. | High. The money is often unrecoverable once sent. **Read this first: needs expert or legal review.** | yes | ask_clarifying_question, offer_choices, admit_uncertainty, hand_off | [page](../../goals/vulnerable-users/failures/scam-victim-not-interrupted.md)  |

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
