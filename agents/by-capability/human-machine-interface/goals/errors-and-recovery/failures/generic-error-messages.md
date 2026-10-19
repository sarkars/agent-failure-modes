# Chatbot Says "Something Went Wrong" and Nothing Else: Generic Error Messages

<!-- SEO
title: "Something Went Wrong": How to Write Chatbot Error Messages That Help
description: Why a chatbot or AI assistant that fails with "Something went wrong" leaves users stuck, what usability research says about generic error messages, and a template that says what happened, what is saved, and what to do next.
search phrases:
- chatbot something went wrong error
- hmm something seems to have gone wrong chatgpt
- how to write good error messages for a chatbot
- ai assistant error message best practices
- chatbot network error lost my conversation
- generic error message ux
- what to say when the chatbot fails
-->

**Frequency**: Very Common

## Issue: When the assistant fails, it shows "Something went wrong" or "An error occurred": no cause the user can act on, no word on whether their work is saved, and no next step.

> **One line:** It broke, and the message says nothing the user can use.

| | |
|---|---|
| **Channel** | Written for **chat** interfaces and assistants (web, app, in-product). |
| **Stakes** | Low to high. A lost long conversation, an unsaved form, or a half-done transaction raises the stakes. |
| **Who is affected** | Anyone who hits a failure, which is every user eventually |
| **Frequency** | Very common. A usability benchmark found 98% of the e-commerce sites it tested used generic messages for validation errors; I found no count for chat products. |
| **Family** | [Errors and recovery](../README.md) |
| **Goal** | When something goes wrong, the agent says what happened, owns it, fixes it, and does not repeat it. |
| **Primary metric** | Errors shown with a cause and action. Target: 100% (tune). |
| **Maturity** | Tests written (see [the test file](../../../tests/generic-error-messages.md); not yet run) |
| **Will a better model fix this?** | No. Error text comes from the product and its failure handling, not from model quality. (Our judgment, not tested.) |
| **Also searched as** | error occurred try again · network error in chat · chat disappeared after error · unhelpful error message · retry loop |

## 1. In plain words
Errors happen: a timeout, a model outage, a tool failure, a message too long. The failure that hurts is the message. "Something went wrong" does not say whether to retry, wait, shorten the message, or give up, and it does not say whether the conversation is safe.

## 2. What it looks like

**Without the fix**
```
User: (sends a long message in a long chat)
Bot:  Something went wrong. Please try again.
User: (retries three times; the same message appears; the chat then vanishes on reload)
```

**With the fix**
```
Bot:  I couldn't send that reply: the service timed out. Your message and this chat are saved.
      Try again in a minute, or send it in two shorter parts. If it keeps failing, contact support and quote code A7K2.
      [Retry] [Copy my message]
```
The fixed message says what happened, what is safe, what to do, and gives a reference for support.

## 3. Why it happens
These are our reading of the pattern.
- **One catch-all handler.** Every failure maps to one string, so the cause is lost.
- **The cause is technical.** Timeouts, rate limits, and tool errors are written for engineers, so teams hide them behind a generic line.
- **No state about what was saved.** The interface does not know whether the user's message or the chat survived, so it cannot say.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| NN/g says error messages should be plainspoken and precise: "Generic messages such as An error occurred lack context", and merely stating the problem is not enough, so offer constructive advice and preserve the user's input. | [Neusesser and Sunwall, *Error-Message Guidelines*, NN/g, 2023](https://www.nngroup.com/articles/error-message-guidelines/). Opened and read. | Guidance for interfaces generally, not chat in particular. |
| In large-scale checkout testing, in the worst cases participants could not resolve the issue "due solely to vague or generic error messages" and abandoned the process; 98% of the sites in the benchmark did not use messages targeted at the exact problem. | [Baymard Institute, *Improve Validation Errors with Adaptive Messages*, Dec. 2023](https://baymard.com/research-articles/adaptive-validation-error-messages). Opened; the first part of the article read. | Practitioner research on checkout forms, not chat. Observed sessions, not a controlled comparison. |
| A guideline from the German UPA lists heuristics for error messages: constructive, comprehensible, concise, and empathic. | [German UPA, *Guideline for Error Messages*](https://germanupa.de/sites/default/files/2024-10/leitfaden-fehlermeldungen-v1.02-en_0.pdf). Opened; the contents and foreword read. | A design guide, not an experiment. |
| A user on OpenAI's developer forum reported in August 2024 that after sending a message in a long chat they received errors ("network error" on PC; "hmm… something seems to have gone wrong" with a retry button on iPhone), retries did nothing, and the conversation vanished after the error. | [OpenAI Developer Community thread](https://community.openai.com/t/i-cant-keep-chatting-my-chat-disappears-after-getting-error-messages/913982). Opened and read. | One user's report; the thread I read has no OpenAI reply. |

I found no controlled study that compares generic with specific error messages in chat products. A search turned up a 2000 conference paper on web error pages that I could not open (a bot check blocked it), so I do not use it.

**Public incident.** No public incident found for generic error messages as such. My searches found outage coverage and forum reports, which I did not treat as a sourced, dated incident about the message text.

## 5. The fix

**The principle:** Every error says what happened, what is safe, and what to do next.

**Do this**
1. **Say what happened in plain words.** "The reply timed out", "Your message is too long", "The order system isn't responding".
2. **Say what is saved.** State whether the user's message and the conversation survived.
3. **Give the next step.** Retry now, wait, shorten the message, use another route, or contact a person, whichever fits the cause.
4. **Preserve the input.** Keep the user's text in the box and offer to copy it (NN/g: preserve the user's input).
5. **Match the message to the cause.** Separate at least: temporary outage, too long, rate limit, permission, and tool failure.
6. **Add a reference code for support.** Show a short code the user can quote; keep technical detail behind it.
7. **Don't blame the user, and don't joke.** Neutral tone; no "invalid" or "illegal" for ordinary input.
8. **Offer a person when retries fail.** After a repeat failure, offer a route to a person ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Reference design: error message parts**
| Part | Content |
|---|---|
| What | "I couldn't send that reply: [cause in plain words]." |
| Safe | "Your message and this chat are saved." (only if true) |
| Next | "Try again in a minute, or [specific alternative]." |
| Help | "Quote code [A7K2] to support" or a person route |

```
When something fails, tell the user what happened in plain words, whether their message and conversation are saved, and what to do next. Keep their message in the input box.
Use a different message for outage, too-long input, rate limit, permission, and tool failure.
Never show only "Something went wrong". After a repeated failure, offer a person and a reference code.
```

**Don't over-correct.** Do not show stack traces or raw error codes as the message. Do not claim "your work is saved" unless the product has confirmed it. Do not write a paragraph; a short, specific message beats a long one.

**Hand-off rule.** After two failures of the same kind, offer a person and pass the reference code and the user's message ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/generic-error-messages.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | A timeout | Cause, saved state, and next step |
| 2 | A message over the length limit | Says it is too long and offers a split |
| 3 | A failed save | Does not claim it is saved |
| 4 | Two failures in a row | Offers a person and a reference code |
| 5 | A reload after an error | The user's text is not lost |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Errors shown with a cause and action** (primary) | 100% | Log every error render with its cause code and the template used | Below 95% |
| Generic fallback used | Under 5% of errors | Count renders of the catch-all template | Over 10% |
| Retry success after an error | Track; set from baseline | Retries that succeed within 2 minutes | Falling |
| Conversations lost after an error | 0 | Sessions where messages vanish after an error event | Any |
| Error-to-abandon rate | Track; set from baseline | Sessions ending within 1 turn of an error | Rising two weeks in a row |
| False "saved" claims (counter-metric) | 0 | "Saved" messages with no confirmed write | Any |

## 8. Related patterns
- [No warning of context loss](../../effort-and-memory/failures/no-warning-of-context-loss.md): telling the user what was lost.
- [Dead-end "I don't understand" replies](../../conversation-leadership/failures/dead-end-i-don-t-understand-replies.md): a dead end when the bot cannot understand.
- [Refusal with no reason or next step](../../refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md): a dead end when the bot will not help.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): what to pass on when sending the user to a person.
- [Missing the obvious intent](../../embedded-copilots/failures/missing-the-obvious-intent.md): misreads that look like errors.

## 9. Common questions
### What should a chatbot say when it fails?
What happened in plain words, whether the user's message is saved, and what to do next.

### Why does ChatGPT say "something went wrong"?
It is a catch-all message. I found no OpenAI explanation of its causes in the sources I opened.

### Should error messages include an error code?
Show a short reference code for support, but keep the message itself in plain words (NN/g says to show codes for technical diagnosis only).

### Is "please try again" enough?
Not by itself. It does not say whether trying again will help or whether the work is safe.

---
## Technical section

### T1. Solution architecture
```
failure event -> classifier (outage | too long | rate limit | permission | tool | unknown)
              -> state check (message saved? chat saved?) -> template (what, safe, next, code)
              -> render + log (cause code, template)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No render of the catch-all without a cause code | Error renderer | Log scan |
| "Saved" only after a confirmed write | Persistence layer | Test 3 |
| User input preserved on error | Client | Test 5 |

### T3. Evals
- **Dataset:** 100 injected failures (timeouts, size limits, rate limits, tool failures, permission denials) with expected cause categories.
- **Judge rubric:** does the message name the cause class, state what is saved correctly, and give a next step?
- **Metrics and starting thresholds:** cause and action 100%; false "saved" 0. Starting points to tune.
- **Release gate:** block a deploy if a new failure path renders the catch-all.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Catch-all renders | Over 10% of errors | Over 25% | Find the unclassified failure path |

### T5. Trade-offs
- Specific messages cost upkeep as failure types change; test them (the German UPA guide notes this).
- A reference code helps support but should not replace the message.

---
### Deep dive
- **Open question.** I found no chat-specific study of error wording. The evidence is general interface guidance and checkout testing.
- **References.** [NN/g, 2023](https://www.nngroup.com/articles/error-message-guidelines/) (opened); [Baymard, 2023](https://baymard.com/research-articles/adaptive-validation-error-messages) (opened); [German UPA guideline](https://germanupa.de/sites/default/files/2024-10/leitfaden-fehlermeldungen-v1.02-en_0.pdf) (opened); [OpenAI Developer Community thread, 2024](https://community.openai.com/t/i-cant-keep-chatting-my-chat-disappears-after-getting-error-messages/913982) (opened).
