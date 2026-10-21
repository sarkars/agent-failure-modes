# Chatbot Shows Too Many Options at Once: Cognitive Overload

<!-- SEO
title: Chatbot Shows Too Many Options at Once: Cognitive Overload
description: A chatbot that shows too many buttons, cards, or choices at once makes users stall or quit. Cap options, lead with a pick, and ask one decision per message.
search phrases:
- chatbot too many options
- chatbot too many buttons overwhelming
- chatbot carousel too many cards
- how many quick replies should a chatbot show
- chatbot choice overload
- chatbot users abandon after menu of options
- progressive disclosure chatbot
- chatbot recommend one option instead of a list
-->

**Frequency**: Common

## Issue: A chat assistant shows too many options, cards, buttons, or lines of text in one message, so the user stalls, picks at random, or leaves without acting.

> **Read this first.** The research here is mixed. A well-known meta-analysis found an average choice-overload effect of virtually zero, with large differences between studies. This page treats the number of choices in one message as something to test with your own users, not as a proven law.

> **One line:** The assistant puts the whole menu on screen at once, so the user has to compare everything before doing anything; the fix is to cap the choices per message, lead with a recommended one, and ask one decision at a time.

| | |
|---|---|
| **Channel** | Written for **chat** (text messages, quick-reply buttons, and cards in a text assistant). Voice and web-page variants are PLANNED, not written. |
| **Stakes** | Low to medium for browsing. Medium to high when the choice is a plan, a payment, or a health or benefits option, because a stall there costs the user money or time. |
| **Who is affected** | Anyone asked to pick among options, most of all first-time users, people on a phone, and people choosing under stress or time pressure |
| **Frequency** | Common as a design habit. I found no count of how often chat assistants overload users. |
| **Pattern ID** | cognitive-overload |
| **Family** | [Visual](../README.md) |
| **Goal** | What an agent shows is clear, honest, accessible, and appropriate to the stakes. |
| **Primary metric** | Time to first action: seconds from the options message to the user's first reply that moves the task forward. Starting point: set the target from your own baseline and user tests; I found no source for a universal number. |
| **Maturity** | Researched. No test file yet; the scenarios in section 6 are designs and are **Not yet run**. |
| **Will a better model fix this?** | Partly. A better model can pick a sensible default, but how many options appear in one message is set by the prompt, the product catalog, and the UI template. (Our judgment, not tested.) |
| **Also searched as** | choice overload chatbot · too many quick replies · decision paralysis chatbot · overwhelming menu · wall of options · analysis paralysis AI assistant |

## 1. In plain words
The assistant shows everything it could offer in one message: seven plans, each with six features and three buttons. The user has to read and compare all of it before doing anything, so many just stop. The fix is to show a few options, say which one fits, and ask one question at a time.

## 2. What it looks like
**Without the fix** (illustrative scenario, fictional carrier "Brightline Mobile")
```
User: I need a phone plan for me and my wife.
Bot:  Here are our plans! [7 cards: Basic 1GB, Basic 5GB, Plus 10GB, Plus Unlimited, Family 2-line, Family 4-line,
      Business], each card with 6 feature bullets and buttons [Compare] [Details] [Select].
      Also: add a device protection plan? Add international calling? Want paperless billing? Which plan do you prefer?
User: (no reply for 90 seconds, then closes the chat)
```
**With the fix**
```
User: I need a phone plan for me and my wife.
Bot:  For two people, most couples pick Family 2-line: $60 a month, unlimited talk and text, 15 GB each.
      [Family 2-line (recommended)] [Show other plans] [Something else]
User: Family 2-line.
Bot:  Good. Do you want to keep your current numbers? [Yes, keep them] [No, new numbers]
```
The fixed version leads with one recommended plan and its price, caps the choices at three buttons, holds the other plans behind "Show other plans", and asks one question per message. (The "most couples pick" line is part of the invented scenario; use it only if your own data supports it.)

## 3. Why it happens
- **The reply template renders the whole catalog.** A product search or knowledge-base query returns 7 items, and the template turns all 7 into cards with every field, because showing less would mean writing a ranking rule.
- **Nobody counts options per message.** Each card passes review alone. The overload shows only when you count elements on the screen, and in a text conversation that count is not logged.
- **Fear of looking pushy or leaving something out.** Teams add choices to seem neutral and complete, and forget that "which one do you recommend?" is the question the user is actually asking.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A meta-analysis of 63 conditions from 50 published and unpublished experiments (N = 5,036) found "a mean effect size of virtually zero" with considerable variance between studies. It reports several possible preconditions for choice overload but no sufficient conditions. | [Scheibehenne, Greifeneder & Todd, *Can There Ever Be Too Many Options?*, Journal of Consumer Research, 2010](https://edoc.unibas.ch/entities/publication/1cd7cefa-8ab9-4be8-9a0f-5412feb5350d). Opened the abstract page only. | **Mixed evidence.** On average, more options did not reduce satisfaction or motivation in these studies. That does not show overload never happens; the abstract says it varies a lot. Consumer experiments, not chat. |
| Across three studies, people were more likely to buy jams or chocolates, and to start an optional essay, when shown a limited set of 6 options than an extensive set of 24 or 30; those who chose from the small set also reported more satisfaction. | [Iyengar & Lepper, *When Choice Is Demotivating*, Journal of Personality and Social Psychology 79(6), 2000](https://business.columbia.edu/faculty/research/when-choice-demotivating-can-one-desire-too-much-good-thing). **Read through a search summary only**; the paper and abstract pages would not open (the PDF was a scan). | **Not used in the fix.** Lab and store settings, not chat. The 2010 meta-analysis above is the counterweight. |
| Hick's law: "The time it takes to make a decision increases with the number and complexity of choices." It comes from a 1952 study by Hick and Hyman of how the number of stimuli affects reaction time. Its design takeaways include minimizing choices when response time matters and highlighting recommended options. | [Laws of UX, Hick's Law](https://lawsofux.com/hicks-law/). Opened and read. | A design-guidance site, not the 1952 paper. The original task was reaction time to stimuli, not choosing a plan. |
| Cognitive load theory says working memory is "limited in both capacity and duration"; overload can leave learners confused, frustrated and less motivated. Its recommendations include removing unnecessary information and "chunking new information and presenting the material bit by bit". | [Application of Cognitive Load Theory to Health and Behavior Change Programs, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12246501/). Opened and read. | Written for learning and program design. The article notes "critical opinions exist" on the theory's methodological rigor. |
| NN/g advises 5 or fewer frames in a carousel, "as it's unlikely users will engage with more than that", and says swiping through many frames "can be taxing" on a phone. It warns that "some people will only see the first frame or none at all". | [NN/g, Carousel Usability](https://www.nngroup.com/articles/designing-effective-carousels/). Opened and read. | About web carousels, not chat. I use it only as a reference point for a cap on cards. |
| NN/g defines progressive disclosure as showing only "a few of the most important options" first and deferring the rest to a secondary screen. It warns that designs beyond 2 disclosure levels "typically have low usability". | [NN/g, Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/). Opened and read. | Interface-design guidance, not a chat study. |

**What the evidence does not show.** I found no study that measures choice overload in a chat assistant, and no source for a best number of buttons. The cap in section 5 is a starting point to test. Blog posts that credit NN/g with chatbot quick-reply advice appeared in my search results; I did not open an NN/g chatbot page, so I do not use that advice.

**How this differs from the closest pages.** [Bullet and heading overuse](../../response-structure/failures/bullet-and-heading-overuse.md) is about formatting that breaks up reasoning. [Link and resource dumps](../../response-structure/failures/link-and-resource-dumps.md) is about handing over links instead of an answer. [Filler and padding](../../response-structure/failures/filler-and-padding.md) is about empty sentences. [Answer buried](../../response-structure/failures/answer-buried.md) is about where the answer sits in the message. This page is about the number of choices and elements the user must weigh before acting. A short message with nine buttons fails here and passes all four of those.

## 5. The fix

**The principle:** Show the user the few choices they need now, say which one fits, and ask one thing at a time.

**Do this**
1. **Lead with a recommendation when you have a reason.** Put the one best-fit option first, marked as recommended, with the reason in one clause. If you have no basis to recommend, ask one question to find out (rule 3) instead of listing everything.
2. **Cap choices per message.** Show at most 4 option buttons or cards plus "Something else". This cap is a starting point to tune with user tests; NN/g's carousel limit of 5 frames is the only published reference I found.
3. **Ask one decision per message.** One question, then wait. Do not stack a plan choice, an add-on, and a billing setting in one reply.
4. **Hold the rest behind one "Show more" step.** Extra options appear on request, one level only. Do not nest a second level.
5. **Disclosure must stay honest.** Price, fees, renewal terms, and anything that changes the decision stay in the first message, never behind "Show more" ([dark patterns](dark-patterns.md)).
6. **Keep each option short.** Name and one deciding fact (price or the key difference). Full detail comes after the user picks.
7. **Keep free text open.** A typed answer always works, and "Something else" asks "What are you looking for?"

**Reference design: choice message**
| Part | Content |
|---|---|
| Recommendation | One option first, marked, with a one-clause reason |
| Choices | Up to 4 buttons or cards, plus [Show other options] and [Something else] |
| Question | Exactly one decision |
| Facts | Name plus one deciding fact per option; price always visible |

```
When the user must pick, lead with the best-fit option and say why in one clause.
Show at most 4 options plus "Something else", ask one decision per message, and keep free text open.
Put extra options behind one "Show more" step. Never hide price, fees, or terms behind it.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user needs a pick: put the recommended option first, with its reason |
| Offer choices | A real choice remains: 2-4 options plus "Something else", free text open. Do not offer choices when the answer is clear, or when the options would trap the user in a menu |
| Ask one clarifying question | You cannot recommend yet: ask the one fact that narrows the options (for example, how many lines) |
| Hand off to a person | The user says "I can't decide" twice, or the choice is high-stakes and complex |

**Don't over-correct.** Do not hide the options a user needs to compare, force a single path with no way out, or cut so much that the user cannot see price or trade-offs. A user who types "show me everything" gets everything, in groups. An expert or a returning user may want the full list at once; let them ask for it.

**Hand-off rule.** If the user stalls on the same choice twice, or the options involve money, health, or benefits that you cannot explain in a few lines, offer a person or a call with a summary of what was narrowed down ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists yet. The scenarios below are designs. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "I need a phone plan for two" with 7 plans in the catalog | The first reply names one recommended plan with a reason | 1 |
| 2 | Same request | No more than 4 option buttons or cards, plus "Something else" | 2 |
| 3 | A reply that needs a plan, an add-on, and a billing choice | Only one decision is asked; the others wait | 3 |
| 4 | User taps "Show other plans" | The rest appear in one step, with no second "Show more" level | 4 |
| 5 | User asks "what's the total?" after the first message | Price and fees were already in the first message, not behind "Show more" | 5 |
| 6 | Read every option label | Each has a name plus at most one deciding fact | 6 |
| 7 | User types "show me everything" or a free-text answer | The reply handles it; buttons do not block the flow | 7 |
| 8 | "I can't decide" sent twice | An offer of a person or a call within the next reply | Hand-off rule |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data and user tests, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Time to first action** (primary) | Falls against your baseline after the fix; no universal number | Seconds from the options-message render to the next user event that advances the task (tap or typed answer) | Median rises against baseline |
| Options per message | At most 4 plus "Something else" (starting point) | Count button and card elements per rendered assistant message | Any message above the cap |
| Decisions asked per message | 1 | Count questions or required inputs per message | Above 1 |
| Abandonment after an options message | Falls against baseline | Share of sessions that end within one turn of an options message with no advancing event | Rising |
| Recommendation shown first | 100% of choice messages where a rule has data to recommend | Check a `recommended` flag on the first option | Any miss |
| "Show more" taps and "show me everything" requests (counter-metric) | Track; do not push to zero | Count taps and matched phrases | High rate: the first set may be wrong |
| Changed pick within 3 turns, or returns (counter-metric) | Track; set from baseline | Choice events followed by a different choice, or return and refund tags | Rising: the recommendation may steer wrongly |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. They are written for chat text and button events; none has been measured. Voice and web-analytics signals are PLANNED and not listed.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A message renders more than 4 option buttons or cards (rule 2) | Count of `option` elements in the render event | The user asked for the full list |
| A message asks two or more separate questions (rule 3) | Question count per message | Fields of one short form that belong together |
| A user's next message after an options message is "which one?" or "what do you recommend?" (rule 1) | Intent match on the next user turn | A sincere request to compare |
| The session ends within one turn of an options message, with no advancing event (abandonment) | Session-end event after an options render | The user got what they needed from the options text |
| The first option is not marked recommended although the product has data to rank (rule 1) | `recommended` flag missing on the first option | A catalog where no option is better for most users |

**Starter rule:** when the user must pick, lead with the best-fit option and a reason, show at most four options plus "Something else", and ask one decision per message.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: cognitive-overload
runs: pre_send
reads: [reply.option_count, reply.question_count, reply.options.recommended, reply.options.price, session.last_user_intent]
trigger: a reply that asks the user to choose among options is about to be sent
moves: [lead_with_answer, offer_choices, ask_one_question, hand_off]
choices: ["Family 2-line (recommended)", "Show other plans", "Something else"]
on_miss: rewrite
metric: time to first action
counter_metric: changed pick within 3 turns
status: proposed
```

## 8. Related patterns
- [Bullet and heading overuse](../../response-structure/failures/bullet-and-heading-overuse.md): formatting that fragments reasoning; this page counts choices, not formatting.
- [Link and resource dumps](../../response-structure/failures/link-and-resource-dumps.md): links handed over in place of an answer.
- [Filler and padding](../../response-structure/failures/filler-and-padding.md): empty sentences around an answer.
- [Answer buried](../../response-structure/failures/answer-buried.md): the answer sits too far down the message.
- [Quick-reply buttons that don't match what was typed](../../chat-interface/failures/quick-reply-buttons-that-don-t-match-what-was.md): buttons that block typed answers; this page is about how many buttons.
- [No likely next-action suggestions](../../embedded-copilots/failures/no-likely-next-action-suggestions.md): the opposite gap, no suggestions at all.
- [Feature dump instead of insight](../../conversation-frameworks/failures/feature-dump-instead-of-insight.md): a feature list instead of the one that matters.
- [Dark patterns](dark-patterns.md): hiding terms; the honesty limit on trimming options in rule 5.

## 9. Common questions
### How many options should a chatbot show at once?
I found no source for one right number. Start with at most four plus "Something else" and test it with your users; NN/g's only published limit I opened is 5 frames for a carousel. Time to first action and abandonment tell you whether your cap works (section 7).

### Is the paradox of choice real?
The evidence is mixed. A 2010 meta-analysis of 50 experiments found a mean effect of virtually zero with large differences between studies. Earlier studies with 6 versus 24 or 30 options found overload, according to a summary I could not check against the paper. Treat it as a risk to test.

### Should I show one recommended option or a list?
Lead with one recommended option when you have a reason for it, and keep the others one tap away. Hick's law, as summarized by Laws of UX, suggests highlighting recommended options. If you have no basis to recommend, ask one question first.

### Isn't it manipulative to recommend one option?
It can be if you hide price or terms, or steer to the costliest choice. Rule 5 keeps price, fees, and terms in the first message, and the "changed pick" counter-metric checks whether recommendations send users the wrong way. See [dark patterns](dark-patterns.md).

### Is a carousel of cards bad in chat?
Not by itself. NN/g says people often miss content beyond the first frame and advises 5 or fewer frames, but that is web guidance. In chat, test a cap of four and watch what share of users tap past the first card.
