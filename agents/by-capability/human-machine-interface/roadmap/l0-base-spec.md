# L0 Base Spec: Behaviors a Customer-Facing Chat Agent Must Show

> **Status: first draft, 2026-10-19 (task 13d). Untested and not reviewed.** This is the L0 level in [learning-agent.md](learning-agent.md): the behaviors taken from the fixes of the 24 flagship patterns written so far, each mapped to its pattern, its test file, and its metric. Nothing here was run against a model. The principle lines are copied from the pattern pages; the sources and caveats for each are on those pages. Four of the patterns (help that becomes a sales pitch, obstructing cancellation, answers withheld behind an upgrade, and the government eligibility one) are flagged for legal review, and the government one also for expert review. A person must review this spec before anyone uses it as a requirement.

## How to use it
- Each row is one behavior the agent should show, in the pattern's own words.
- The **Test** column links the pattern's test file (12 scenarios each, results "Not yet run"). The **Metric** column is the pattern's primary metric; targets are starting points on the pattern page, not requirements.
- A behavior is **in the spec** when its pattern is Done under the [Definition of done](execution-plan.md). Patterns that are not flagship (older pages without a test file) are not in this table.

## Behaviors by family


### Conversation leadership
| Behavior (from the pattern's principle) | Pattern | Test | Primary metric |
|---|---|---|---|
| When the bot cannot understand, it falls forward: it says what it can do, offers the closest options, changes approach on a repeat, and hands off by the third miss. | [Dead end I don't understand replies](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) | [tests](../tests/dead-end-i-don-t-understand-replies.md) | Share of conversations with 3 or more consecutive no-progress turns |

### Dialogue management
| Behavior (from the pattern's principle) | Pattern | Test | Primary metric |
|---|---|---|---|
| A correction replaces the old value everywhere, the assistant says what it now has, and the action uses it. | [Corrections not applied](../goals/dialogue-management/failures/corrections-not-applied.md) | [tests](../tests/corrections-not-applied.md) | Corrections still wrong two turns later |
| Ask one short question when the readings differ in a way that matters and a wrong guess is costly. Otherwise answer, and say what you assumed. | [Guessing instead of asking](../goals/dialogue-management/failures/guessing-instead-of-asking.md) | [tests](../tests/guessing-instead-of-asking.md) | Wrong-guess rate on ambiguous test requests |

### Effort and memory
| Behavior (from the pattern's principle) | Pattern | Test | Primary metric |
|---|---|---|---|
| Do what you can do, ask only for what only the user can supply, and when you will not or cannot do something, say so and say why. | [Deferring work to the user](../goals/effort-and-memory/failures/deferring-work-to-the-user.md) | [tests](../tests/deferring-work-to-the-user.md) | Deferral rate: replies handing a task to the user that the agent has a tool for |
| Do the full job, or say exactly what is left and why. | [Lazy completion](../goals/effort-and-memory/failures/lazy-completion.md) | [tests](../tests/lazy-completion.md) | Completeness rate: required items delivered divided by items requested |
| Never lose the user's details silently. Warn before the limit, say what was kept, and say what was lost afterward. | [No warning of context loss](../goals/effort-and-memory/failures/no-warning-of-context-loss.md) | [tests](../tests/no-warning-of-context-loss.md) | Context-loss events with a user-visible notice |

### Embedded copilots
| Behavior (from the pattern's principle) | Pattern | Test | Primary metric |
|---|---|---|---|
| If a limit changes what the user gets, say so in the reply, say what the limit is and what would lift it, and point to any free route. | [Answers withheld behind an upgrade unsaid](../goals/embedded-copilots/failures/answers-withheld-behind-an-upgrade-unsaid.md) | [tests](../tests/answers-withheld-behind-an-upgrade-unsaid.md) | Share of replies that withhold or degrade help with no stated reason |
| Tell users, in the first screen, what the assistant can do and what it cannot, with starting points from the current context, and keep that description tied to what is actually connected. | [Doesn't say what it can do](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md) | [tests](../tests/doesn-t-say-what-it-can-do.md) | Share of new users who complete a successful first task with the assistant |
| Pass the signed-in session to the assistant securely, let it answer low-risk questions without a new check, and ask for a stronger check only before risky actions, inside the app's own secure screen. | [Forces a fresh login](../goals/embedded-copilots/failures/forces-a-fresh-login.md) | [tests](../tests/forces-a-fresh-login.md) | Re-authentication prompts for already-authenticated users on low-risk actions |
| Open with what the product already knows about the moment, offer the one to three most likely needs, and make it easy to say "something else". | [Generic first response](../goals/embedded-copilots/failures/generic-first-response.md) | [tests](../tests/generic-first-response.md) | Share of first replies or opening messages that reference user-specific context or a likely need, rated by a calibrated judge |
| Help first, fully, and without conditions. Any commercial offer comes after the help, only when it is relevant, once, and clearly labeled as an offer. | [Help that becomes a sales pitch](../goals/embedded-copilots/failures/help-that-becomes-a-sales-pitch.md) | [tests](../tests/help-that-becomes-a-sales-pitch.md) | Upsell-in-help rate: share of help replies on support intents that include a sales prompt when the user did not ask about plans or pricing |
| For a plain request, answer the likeliest reading first and offer the others in one line. Ask a clarifying question only when no reading clearly leads. | [Missing the obvious intent](../goals/embedded-copilots/failures/missing-the-obvious-intent.md) | [tests](../tests/missing-the-obvious-intent.md) | Top-intent accuracy on a test set of simple, common requests |
| Leaving should be as easy as joining, in the same place, with the truth about what happens next. The assistant may make one optional offer and then must do what the user asked. | [Obstructing cancellation downgrade or refund](../goals/embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md) | [tests](../tests/obstructing-cancellation-downgrade-or-refund.md) | Cancellation parity: steps to cancel through the assistant compared with steps to subscribe |
| Look up what the product already knows, say what you found, and ask only for what is missing, within what the user has allowed. | [Re asks for known information](../goals/embedded-copilots/failures/re-asks-for-known-information.md) | [tests](../tests/re-asks-for-known-information.md) | Re-ask rate on known fields: the share of assistant questions that ask for a value the product already holds for this user |

### Errors and recovery
| Behavior (from the pattern's principle) | Pattern | Test | Primary metric |
|---|---|---|---|
| Show what the answer rests on and how sure the bot is, and make the check easy, or hand off. | [Confident wrong answer with no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) | [tests](../tests/confident-wrong-answer-with-no-way-to-check.md) | Wrong answers stated without any uncertainty or source |
| Every error says what happened, what is safe, and what to do next. | [Generic error messages](../goals/errors-and-recovery/failures/generic-error-messages.md) | [tests](../tests/generic-error-messages.md) | Errors shown with a cause and action |

### Government service agents (flagged L and E)
| Behavior (from the pattern's principle) | Pattern | Test | Primary metric |
|---|---|---|---|
| Say what is general guidance and what only the agency decides, and always leave a way to apply, a person, and an appeal. | [Eligibility answers sound like decisions](../goals/government-service-agents/failures/eligibility-answers-sound-like-decisions.md) | [tests](../tests/eligibility-answers-sound-like-decisions.md) | Eligibility answers that state what is a guess |

### Human handoff
| Behavior (from the pattern's principle) | Pattern | Test | Primary metric |
|---|---|---|---|
| The handoff is a product. Whatever the customer told the bot is on the person's screen before they say hello, and the customer can see and correct it. | [Cold transfer](../goals/human-handoff/failures/cold-transfer.md) | [tests](../tests/cold-transfer.md) | Re-ask rate after handoff: the share of handoffs where the person asks for something the customer already gave, from a labeled sample |
| Write down when a person must take over, check it every turn, and measure both misses and false alarms. | [Escalates too early or too late](../goals/human-handoff/failures/escalates-too-early-or-too-late.md) | [tests](../tests/escalates-too-early-or-too-late.md) | Escalation precision and recall against labeled conversations |
| A clear request for a person is a routing event. Honor it, or answer it with a real route, a time, and what happens next, within two bot turns. | [Talk to a human ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) | [tests](../tests/talk-to-a-human-ignored-or-looped.md) | Human-request fulfillment rate: requests for a person that end in a transfer, a scheduled callback, or a stated route within 2 bot turns |

### Refusals and boundaries
| Behavior (from the pattern's principle) | Pattern | Test | Primary metric |
|---|---|---|---|
| Judge the request, not the word. Refuse real risk, help with the rest, and measure both. | [Over refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) | [tests](../tests/over-refusal-of-ordinary-requests.md) | Over-refusal rate on a benign-but-risky-looking test set |
| A refusal says what the bot cannot do, why in plain words, and what it can do instead. | [Refusal with no reason or next step](../goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md) | [tests](../tests/refusal-with-no-reason-or-next-step.md) | Refusals that include an alternative or a route to a person |

### Response structure
| Behavior (from the pattern's principle) | Pattern | Test | Primary metric |
|---|---|---|---|
| The first sentence answers the question or states the next step. Everything else is optional and can be skipped. | [Answer buried](../goals/response-structure/failures/answer-buried.md) | [tests](../tests/answer-buried.md) | Answer-first rate: the first sentence holds the answer or the next step |
| Treat acknowledgments and closers as real turns. Reply in proportion, end only when the user has ended, and never restart or re-ask. | [No reply to acknowledgments and closers](../goals/response-structure/failures/no-reply-to-acknowledgments-and-closers.md) | [tests](../tests/no-reply-to-acknowledgments-and-closers.md) | Handling correctness on labelled acknowledgment and closer turns |

## Tensions between behaviors (design judgments, not tested)
These are places where two behaviors pull in different directions. A person should decide the rule for each before the spec becomes a requirement.
1. **Ask or answer.** [Guessing instead of asking](../goals/dialogue-management/failures/guessing-instead-of-asking.md) says to ask when readings differ and a wrong guess is costly; [missing the obvious intent](../goals/embedded-copilots/failures/missing-the-obvious-intent.md) says to answer the likeliest reading first for plain requests. The cost of a wrong guess is the tie-breaker the patterns offer.
2. **Hedge or lead with the answer.** [Confident wrong answer with no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) asks for uncertainty and a source; [answer buried](../goals/response-structure/failures/answer-buried.md) asks for the answer in the first sentence. Both can hold if the hedge is part of the first sentence.
3. **Refuse or help.** [Over-refusal](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) lowers refusals; [refusal with no reason or next step](../goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md) improves them. They need a two-sided test so that neither metric improves at the other's cost.
4. **Do it or ask the person.** [Deferring work to the user](../goals/effort-and-memory/failures/deferring-work-to-the-user.md) says to use the tool; [forces a fresh login](../goals/embedded-copilots/failures/forces-a-fresh-login.md) says to step up verification only for risky actions. The risk level of the action sets the rule.
5. **Offer, but don't sell.** [Help that becomes a sales pitch](../goals/embedded-copilots/failures/help-that-becomes-a-sales-pitch.md) and [obstructing cancellation](../goals/embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md) both limit offers; a business may still want to make one. The patterns say after the help, once, labeled. Flagged L; counsel decides.

## What this spec does not cover
- Behaviors from the 14 older, non-flagship HMI pages (they have no test files yet).
- Anything about a model, a framework, or a runtime. See the [L1 harness decision record](l1-harness-decision.md).
- Any measured result. Every target is a starting point.

## Related
- [Learning agent levels](learning-agent.md) · [L1 harness decision record](l1-harness-decision.md) · [Test files](../tests/README.md) · [Execution plan](execution-plan.md)
