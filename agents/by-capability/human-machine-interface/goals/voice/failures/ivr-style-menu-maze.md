# Chatbot Menu Maze: IVR-Style "Press 1" Trees That Trap Users in Option Loops

<!-- SEO
title: Chatbot Menu Maze: Why Button Trees Trap Users and How to Fix Them
description: Why a chatbot that forces "choose one of these options" menus with no free-text path and no way to a person strands users, what the CFPB and NN/g say, and a copyable rule set.
search phrases:
- chatbot only gives me buttons, no way to type
- chatbot menu loop won't let me ask my question
- ivr style chatbot menu too many options
- chatbot keeps showing the same menu
- how to avoid phone tree menus in a chatbot
- chatbot decision tree dead end no human option
- press 1 for billing chatbot
- how many menu options should a chatbot show
-->

**Frequency**: Common

## Issue: The bot answers every message with a menu of fixed options ("Choose one of these 7 topics"), has no free-text path that works, and no visible way to reach a person, so the user taps through levels and loops back to the start.

> **One line:** A button tree is the chat version of a phone "press 1" menu: if the user's problem is not on a button, they cannot say so, and the only exit is to quit.

| | |
|---|---|
| **Channel** | Written for **chat** (button-and-menu trees, "choose one" lists, quick replies, no usable typing, no person route). Voice and phone IVR signals (keypress counts, call abandonment at the menu, "press 0" attempts, spoken "agent") are **planned**: the rules apply, but nothing below is measured from calls. |
| **Stakes** | Low to high. A store-hours menu costs a minute; a menu between a customer and a disputed charge or a due payment costs money. |
| **Who is affected** | Anyone whose problem is not one of the listed options, people who cannot log in, and people for whom picking from a long list is hard (see the [accessibility](../../accessibility/README.md) family) |
| **Frequency** | Common. No study was found that counts how often menu-only bots trap users. The evidence below is a regulator report, one small usability study, and design guidance. |
| **Pattern ID** | ivr-style-menu-maze |
| **Family** | [Voice](../README.md) |
| **Goal** | Get to the goal in few steps and keep an easy route to a person. |
| **Primary metric** | Steps to goal (taps and turns before the task is done or handed off), reported with the share of conversations where the user asks for a person. Starting target: set from baseline (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A model can read free text well, but whether the product shows a menu, accepts typing, and keeps a person reachable is a design and routing decision. (Our judgment, not tested.) |
| **Also searched as** | chatbot decision tree · phone tree in chat · chatbot buttons only · menu loop · bot sends me back to the main menu · IVR hell · can't skip the menu |

## 1. In plain words
A phone tree makes callers listen to options and press a key. Many chatbots recreate it in text: a greeting, a list of topics as buttons, a second list after each tap, and "Main menu" at the bottom. That works when the user's goal is on the list. When it is not, the user taps the nearest topic, gets a wrong answer, and ends up at the top again. The fix is to let the user say what they want, keep menus short and shallow, and keep a way to a person on every screen.

## 2. What it looks like

**Without the fix**
```
Bot:   Hi! Choose a topic: 1) Orders  2) Returns  3) Payments  4) Account  5) Shipping  6) Promotions  7) Other
User:  Payments
Bot:   Choose one: 1) Make a payment  2) Payment methods  3) Payment history  4) Back to main menu
User:  my card was charged twice for order 5521
Bot:   Please choose one of the options below.  1) Make a payment  2) Payment methods  3) Payment history  4) Back to main menu
User:  Payment history
Bot:   Here is how to view payment history: Account > Billing. Was this helpful?  [Yes] [No]  [Main menu]
```

**With the fix**
```
Bot:   Hi, I'm the order assistant. Tell me what you need, or pick: Track an order, Start a return, Billing problem. You can also ask for a person.
User:  Payments
Bot:   Payments covers a lot. What's going on: a charge you don't recognize, a failed payment, or something else?
User:  my card was charged twice for order 5521
Bot:   Two charges on order 5521 is a billing error until proven otherwise. I can open a refund review now, or connect you to billing (about 5 minutes). Which do you want?
```
The fixed bot accepts typed text beside the buttons, asks one narrowing question instead of re-showing the tree, answers the stated problem, and names a route to a person.

## 3. Why it happens
- **The tree was built from the support team's categories, not the user's words.** Each button maps to a department or article, so a problem that spans categories or fits none has nowhere to go.
- **Free text is off, or it only matches button labels.** The product treats typing as an error ("Please choose one of the options"), so the user must guess which label is closest ([quick-reply buttons that ignore typed answers](../../chat-interface/failures/quick-reply-buttons-that-don-t-match-what-was.md)).
- **Every dead end returns to the same menu.** A rule-based bot has a preset response per branch and a default of "main menu", which is cheap to build and invites loops. The person route sits deep in the tree, or behind a login, or not at all.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The CFPB says rule-based chatbots "use either decision tree logic or a database of keywords to trigger preset, limited responses", may "present the user with a set menu of options to select from", and that the user "is typically limited to predefined possible inputs." | [CFPB, *Chatbots in consumer finance* (June 2023)](https://files.consumerfinance.gov/f/documents/cfpb_chatbot-issue-spotlight_2023-06.pdf), section 2.1. Opened; text extracted from the PDF and read. | A description of how these bots work, in consumer finance. It is not a measurement of harm. |
| The same report says these bots "tend to be one-way streets", that they cannot respond to requests outside the scope of their inputs, and that automated responses may lead customers "in continuous loops of repetitive, unhelpful jargon or legalese without an offramp to a human customer service representative" ("doom loops"). | CFPB report, sections 3.1.1 ("one-way streets") and 3.1.3 ("doom loops"). Opened and read. | Regulator commentary on bank chatbots. It does not count how many complaints it reviewed. |
| One quoted complaint, dated July 2, 2022, says a card payment was due that day and the chat assistant "kept sending me in circles", "an endless loop with no way out". Another (June 24, 2020) describes "endless telephone prompts" by phone and then "loop after loop of the same questions" in chat, all redirecting to a login the person did not have. | CFPB report, footnotes 39 and 40. Opened and read. | Two individual complaints, quoted by the regulator. Anecdotes, not rates. See the [incident write-up](../../../incidents/cfpb-bank-chatbot-doom-loops.md). |
| In an NN/g usability study of chatbots (8 US participants: 5 mobile, 3 desktop), people appreciated predetermined buttons and "even expected them for common inputs", but bots that removed free text "restricted the paths that the user could explore". The authors conclude both input modes "should be both present." | [Budiu, "The User Experience of Chatbots," NN/g, Nov. 25, 2018](https://www.nngroup.com/articles/chatbots/). Opened and read. | Eight participants in 2018. It shows buttons help and free-text removal narrows paths. It does not measure abandonment. |
| NN/g's 2026 guidance on site AI chatbots says suggested prompts reduce effort and should be buttons, not text, and recommends one chatbot that "escalates questions to humans when it can't". It notes followups can annoy users when irrelevant or repetitive. | [Kenderova, Rosala and Kohler, NN/g, Apr. 24, 2026](https://www.nngroup.com/articles/ai-chatbots-design-guidelines/). Opened and read. | Guidance from observed users of AI chatbots; no sample size is given in the article. Written about AI chatbots, not rule-based trees. |
| Voice-UI authors list "[operator]" ("Transfer to an operator or customer service agent") among universal commands, say universals are for functions callers "can use to get out of trouble", and recommend a very small set that callers are taught. | Balogh, Cohen and Giangola, *Voice User Interface Design* (2004), [chapter 9](https://www.informit.com/articles/article.aspx?p=170792). Opened and read. | A 2004 phone-IVR design book, a recommendation not a result. |

No source opened gives a rate for how often menu-only bots trap users, or an optimal number of menu options. Treat the numbers in the fix as starting points. Vendor blog claims about abandonment at menus were seen only in search summaries and are not used.

## 5. The fix

**The principle:** A menu is a shortcut, never the only way in. Free text always works, every menu screen has a route to a person, and the user reaches their goal in as few steps as the task allows.

**Do this**
1. **Free text works on every screen that shows buttons.** A typed message is read for meaning and answered like the matching button, or like a new request. "Please choose one of the options" is never the reply to typed text.
2. **Show at most 4 buttons plus "Something else" and a person route.** Order by the most common goals first. The cap is a starting point to tune.
3. **Keep the tree shallow: at most 2 menu levels before the user gets an answer, a question that narrows it, or an offer of a person.** If the third menu screen would be shown, ask in words instead.
4. **Never re-show a menu the user has already seen without new information.** The same buttons twice in a row means the bot switches to a typed question or offers a person.
5. **Put "Talk to a person" on every menu screen as a visible option**, and honor a typed request for one ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)). Do not require a login to reach it.
6. **Answer the stated problem before offering a menu.** If the user typed a clear goal ("charged twice on order 5521"), respond to it. A menu is for when the goal is unknown.
7. **"Back", "Start over", and "Main menu" return to where the user was and keep what they entered** ([no way back in a flow](../../dialogue-management/failures/no-way-back-in-a-flow.md)). Returning to the top never discards typed details.
8. **Count and log steps.** Record each tap and typed turn until the task ends or hands off, so steps to goal can be computed.

**Reference design: menu policy**
```
screen:      buttons <= 4 + "Something else" + "Talk to a person"; free text accepted
on typed text:   classify intent; confident -> answer like the matching button; unsure -> one narrowing question
on button tap:   answer or show next level (max depth 2); depth 3 -> ask in words
on same menu twice in a row, or 3 turns without progress:  offer a person with the wait or route
on "Back"/"Start over":  restore prior state, keep entered details
log:         menu_depth, taps, typed_turns, person_requested, outcome
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user typed a clear goal. Answer or act on it before showing any buttons. Do not lead with a menu |
| Ask one clarifying question | The typed message fits two or more topics ("Payments" with no detail): ask one narrowing question in words. Do not ask when the goal is already clear |
| Offer choices: 2-4 options plus "Something else", free text open | The first message is vague or the user is new to the bot, or after one failed typed turn. Do not offer choices again after the same menu has already been shown, and do not offer them when the user has asked for a person |
| Hand off to a person | The user asks for one, or the same menu has been shown twice, or three turns pass without progress. Do not hand off when the user says they want to stay with the bot |

**Don't over-correct.** Do not remove buttons: NN/g participants wanted them for common inputs, and buttons help people who do not want to type. Do not replace the menu with an open prompt that gives no hint what the bot can do. Do not transfer every user who taps "Other"; one narrowing question comes first. Keep the person route visible without making it the only prominent button.

**Hand-off rule.** When the user is passed to a person, send the topic taps, the typed text, and the order or account number already entered, so they do not repeat them ([no channel switch or context lost](../../channel-selection/failures/no-channel-switch-or-context-lost.md)).

**Framework used:** none yet. The closest existing page is the [channel-fit matrix](../../../solutions-library/channel-fit-matrix.md).

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | User types a free-text goal while buttons are shown | The typed goal is answered, no "choose one of the options" reply (1, 6) |
| 2 | First menu screen | At most 4 buttons plus "Something else" and a person route (2, 5) |
| 3 | A topic that needs three taps to reach an answer | An answer, a typed question, or a person offer appears by the third screen (3) |
| 4 | User taps "Payments" then types a problem not on the buttons | The bot does not show the same menu again (4, 1) |
| 5 | User types "agent" on a menu screen | A route to a person with a wait or window, no menu (5) |
| 6 | User taps "Start over" after entering an order number | The order number is kept (7) |
| 7 | A finished session | Taps and typed turns are logged with the outcome (8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Steps to goal** (primary), with the share of conversations where the user asks for a person | Set from baseline; steps lower and person requests not rising | Count taps and typed turns from first message to resolved or handed off; label person requests with a classifier plus sampled review | Steps up 20% over baseline, or person requests rising two weeks in a row |
| Typed text answered while buttons are shown | 100% | Log typed turns on screens with buttons and whether the reply was a "choose an option" fallback | Below 98% |
| Conversations with the same menu shown twice in a row | Under 3% | Consecutive bot turns with identical button sets | Over 6% |
| Person route visible on menu screens | 100% | Check the screen template and sampled transcripts | Any screen without it |
| Conversations ending at a menu with no answer (counter-metric: forced transfers) | Track; set from baseline | Session end within 2 turns of a menu screen with no resolution or handoff | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Written for text chat; phone signals are PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| The same button set is shown in two consecutive bot turns | Bot turn type and button list before and after | A user who deliberately went back to compare options |
| The user types free text and the next bot turn is a "choose an option" fallback | Typed turn followed by a fallback template | A typed answer that was off topic or a test message |
| The user taps "Main menu" or "Start over" three or more times in one session | Count of reset events | A user who is exploring all topics on purpose |
| The user asks for a person after three or more menu screens | Person-request label with menu depth at that point | A user who wanted a person from the start |
| PLANNED for voice: a caller presses 0 or says "agent" repeatedly, or hangs up on a menu prompt | Needs keypress and call-abandon logs; not computable from chat transcripts | A caller who knows the number they want |

**Starter rule:** accept typed text on every menu screen, never show the same menu twice in a row, and keep a route to a person visible.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ivr-style-menu-maze
runs: conversation
reads: [turn.text, bot_turn.type, bot_turn.buttons, menu.depth, menu.repeat_count, user.person_request_label]
trigger: a menu is about to be shown, or a user turn arrives on a screen with buttons
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Track an order", "Start a return", "Billing problem", "Something else"]
on_miss: handoff
metric: steps to goal, with the share of conversations where the user asks for a person
counter_metric: forced transfers
status: proposed
```

## 8. Related patterns
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): the closest page. It starts when the user has already asked for a person and the bot ignores them; this page is the upstream design that makes the user need to ask, a menu tree with no typing path and no visible person route.
- [Quick-reply buttons that ignore typed answers](../../chat-interface/failures/quick-reply-buttons-that-don-t-match-what-was.md): one screen where buttons reject typing. This page covers the whole tree, its depth, its loops, and the missing exit.
- [Dead-end "I don't understand" replies](../../conversation-leadership/failures/dead-end-i-don-t-understand-replies.md): a reply with no next step. A menu maze has next steps, but they are the same ones.
- [CFPB report on bank chatbot doom loops](../../../incidents/cfpb-bank-chatbot-doom-loops.md): the dated public incident for the loop side.
- [No repeat or recap controls](no-repeat-or-recap-controls.md) and [repair failure](repair-failure.md): other voice-family pages that share the universal "back", "repeat", and "agent" controls.
- [Voice-only flows with no text alternative](../../accessibility/failures/voice-only-flows-with-no-text-alternative.md): the phone menu seen from deaf and hard-of-hearing callers.

## 9. Common questions
### Why does my chatbot keep showing the same menu?
Usually the default reply for a dead end is "main menu", and no rule tells the bot to try something else after the second showing. Add a repeat counter and switch to a typed question or a person offer.

### How many options should a chatbot menu show?
No source opened gives a proven number. This page starts at 4 buttons plus "Something else" and a person route, and asks you to tune it from your step counts.

### Should a chatbot let users type, or only tap buttons?
Both. In the NN/g study, people liked buttons for common inputs, and removing typing narrowed what they could do. Keep typing on, and treat it as the main way when the goal is not on a button.

### How do I get a real person out of a button-only chatbot?
As a user, try typing "agent" or "representative" and look for a "Talk to a person" link. As a builder, put that option on every menu screen ([see the fix](#5-the-fix)).

### Is a phone IVR menu the same problem?
The failure is the same: fixed options and no easy way to a person. This page is written for chat. Phone signals such as keypress counts and abandonment at the menu are planned, not measured.

---
## Technical section

### T1. Solution architecture
```
user turn -> intent classifier (typed text) -> answer | narrowing question
button tap -> menu manager (depth, repeat counter) -> answer | next level
menu manager -> repeat/depth/no-progress trigger -> person route (with context)
log: menu_depth, taps, typed_turns, outcome
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Typed text is never answered with "choose an option" | Dialogue manager | Tests 1 and 4 |
| Menu screens carry a person route | Screen template | Tests 2 and 5 |
| Depth and repeat limits trigger a different move | Menu manager | Tests 3 and 4 |

### T3. Evals
- **Dataset:** 100 labeled conversations with typed goals shown on button screens, goals missing from the menu, and repeated menu loops (starting point to tune).
- **Judge rubric:** did the typed goal get answered, did the same menu appear twice in a row, was a person route present?
- **Metrics and starting thresholds:** typed text answered 100%; repeated menus under 3%. Starting points to tune.
- **Release gate:** block a deploy if a menu screen ships with no person route or with free text disabled.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Repeated-menu rate | Over 6% | Over 12% | Check the default fallback branch and the repeat counter |

### T5. Trade-offs
- Free text needs an intent classifier, and a wrong guess is worse than a button. Ask one narrowing question when unsure.
- A visible person route may raise transfers. Measure steps to goal and person requests together.

---
### Deep dive
- **Voice.** Phone IVR keypress logs, call-abandon at the menu, and spoken "agent" attempts are PLANNED signals. No call data was used here.
- **Not opened.** The Consumerist IVR cheat-sheet post (Nov. 2005) returned HTTP 410 and vendor IVR design blogs were seen only in search summaries; neither is used above. A claim that menus of 20 options make callers hang up appeared only in a vendor summary and is not used. A proposed 2026 FCC rule on offshore call centers was seen only in search summaries and covers call-center location, not menus, so it is not used.
- **Open question.** No measurement was found of how many users abandon menu-only bots, or of the best menu width and depth.
- **References.** [CFPB, *Chatbots in consumer finance*](https://files.consumerfinance.gov/f/documents/cfpb_chatbot-issue-spotlight_2023-06.pdf) (opened, June 2023); [NN/g, The User Experience of Chatbots](https://www.nngroup.com/articles/chatbots/) (opened, 2018); [NN/g, 10 Guidelines for Designing Your Site's AI Chatbots](https://www.nngroup.com/articles/ai-chatbots-design-guidelines/) (opened, 2026); [Balogh, Cohen and Giangola](https://www.informit.com/articles/article.aspx?p=170792) (opened, 2004).
