# Chatbot Calls Me "Honey" or "Dear": Over-Familiar Address

<!-- SEO
title: Chatbot Calls Me Honey or Dear: Fix Over-Familiar Address
description: Why a chatbot that says "honey", "buddy" or your first name feels wrong with a stranger, and the fix: use only the name or title the person chose.
search phrases:
- chatbot calls me honey
- ai assistant calling me dear or sweetie
- chatgpt using my first name
- chatbot too familiar customer service
- how should a chatbot address customers
- chatbot greeting by first name or Mr and Ms
- ai chatbot too casual formal customer
-->

**Frequency**: Occasional

## Issue: A chatbot that says "honey", "dear", "buddy" or a first name to a stranger or in a formal setting feels presumptuous, so it should use only the name or title the person chose, and no pet name at all.

> **One line:** The bot picks a way to address the user (a pet name, or a first name from the account) that the user never chose.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and web signals are PLANNED, not covered here. |
| **Stakes** | Low to medium (higher in claims, health, banking and legal chats, where a pet name can sound dismissive) |
| **Who is affected** | Any user the bot addresses by a term the user did not choose. The page makes no rule about any group or region; the rule is about what the user chose. |
| **Frequency** | Occasional. Our judgment; I found no study that counts it in chat products. |
| **Pattern ID** | over-familiar-address |
| **Family** | [Persona and tone](../README.md) |
| **Goal** | The agent keeps one fitting character: on-brand, respectful, and never talking down or trying too hard. |
| **Primary metric** | Over-familiar address per 1,000 replies. Starting target: 0 (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Our judgment, not tested: a stronger model follows "no pet names" better, but the persona prompt and the profile fields that put a name in the prompt come from the product, and a model cannot know what a user would choose. |
| **Also searched as** | chatbot calls me honey · ai calls me by my first name · chatbot too friendly · chatbot pet names · how to address a customer in chat |

> **Read this first:** The research behind this page comes from care settings and restaurants, not chat. It supports one narrow point (preferences differ, so ask or stay neutral). It does not support rules about any age group, region or community, and this page gives none.

## 1. In plain words
The bot calls the user "hon", "dear" or "buddy", or opens with the first name from their account, before the user has said how they want to be addressed. Some people do not mind. Others find it presumptuous, and the bot cannot tell which. The fix is to use no address term by default and to use exactly the name or title the user gives.

## 2. What it looks like
**Without the fix**
```
(Account name on file: Margaret Chen)
User: Good afternoon. I need a copy of the explanation of benefits for my March 3 claim.
Bot:  Hey Margaret! No worries, hon, I've got you! Let me dig that up for you, sweetie.
User: Please just send the document.
Bot:  You bet, Margaret! Coming right up, dear!
```
**With the fix**
```
User: Good afternoon. I need a copy of the explanation of benefits for my March 3 claim.
Bot:  Good afternoon. I can send it. The March 3 claim is from Lakeside Imaging. Send it to the
      email on file, or download it here? (Email / Download / Something else)
User: Please call me Ms. Chen, by the way.
Bot:  Understood, Ms. Chen. Here is the link to your March 3 explanation of benefits.
```
The fixed bot uses no address term until the user chooses one, then uses it exactly as given. The name on file was never treated as a choice.

## 3. Why it happens
These are our reading of the pattern.
- **A warm persona prompt.** "Be friendly, like a neighbor" is read as license for pet names, and nothing says to stop at the user's first formal message.
- **Profile data in the prompt.** A first name from the account is passed to the model for personalization, and the model uses it as an address. A stored name is not a chosen form of address.
- **Mirroring the wrong thing.** A user who writes "hey buddy" to the bot gets "buddy" back, though the user only chose their own tone, not how the bot should address them.

## 4. Why it matters
No source I opened measures how often chat assistants use over-familiar address, or what it costs. The rows below are related evidence, and each caveat limits the claim.
| Finding | Source | Caveat |
|---|---|---|
| In interviews with 15 older adults in an assisted living facility, some did not mind staff saying "honey", "sweetie" or "dear", some liked it, and others found it childish or disrespectful. The authors recommend that use of such terms "should be individualised based on the preferences of the older adult." | [Schmitz, Lombardo and Szabo, *Nursing Older People*, 2024](https://journals.rcni.com/nursing-older-people/evidence-and-practice/perceptions-of-the-use-of-terms-of-endearment-among-older-adults-in-an-assisted-living-facility-nop.2024.e1467/abs) (abstract page opened; the full article is paywalled) | Small qualitative study in one facility, face to face, about staff. It shows that preferences differ. It is not about chat and does not generalize. |
| AARP lists "honey", "baby", "sweetie" and "dear" among elderspeak terms, says context matters, and quotes a gerontology researcher advising caregivers to ask the older adult what they want to be called. | [AARP, *What Is Elderspeak?*](https://www.aarp.org/caregiving/basics/what-is-elderspeak/) (opened) | News and advocacy article about caregiving. Secondary. I did not use its dementia-care figures. |
| In a restaurant field experiment (127 tables) and online script experiments, using the customer's name raised satisfaction; using it in every sentence "canceled out" that effect and caused discomfort. The summary says it feels forced when it seems used to upsell, and that online chat was not tested. | [Science Says summary of a *Journal of Retailing* study (2026)](https://app.sciencesays.com/p/when-and-how-to-call-customers-by-name) (summary opened; I did not open the paper) | Secondary summary, single study, in-person plus scripts. It did not separate first names from titles, and it is not a chat result. |
| In April 2025, users reported that ChatGPT began calling them by first name in its reasoning text without being told to. One called it "creepy and unnecessary" (Simon Willison); another wrote, "It's like a teacher keeps calling my name." The reporter wrote that by that Friday the change appeared reverted for his account. OpenAI did not comment to the outlet. | [TechCrunch, April 18, 2025](https://techcrunch.com/2025/04/18/chatgpt-is-referring-to-users-by-their-names-unprompted-and-some-find-it-creepy) (opened) | News report with informal user reactions. A first name, not a pet name, and the cause is unknown. It shows that a stored name used unprompted draws objections from some users, not that most object. |

**Unverified:** Search summaries mentioned a 2012 UK survey on title versus first name, a marketing survey on first-name address, and a 2013 tipping study. I did not open them and kept them out of the fix.

**Public incident.** I found no public incident of a chatbot using "honey" or "dear" with a customer (search: chatbot calls user honey, sweetie or dear). The ChatGPT first-name reports above are the closest dated case. I did not write an incident page.

## 5. The fix
**The principle:** Use no address term by default, and use only the name or title the user has chosen.

**Do this**
1. **Default to no address term.** Start the reply with the answer. "You" is enough.
2. **Never apply a pet name or endearment.** Not "honey", "hon", "dear", "sweetie", "sweetheart", "buddy", "pal" or "champ". The user may state a name for themselves; the bot never offers one.
3. **A stored name is not a chosen form.** A first name from the account, payment or email is not used to address the user. A form counts as chosen only if the user said it in this conversation ("call me Ms. Chen", "I go by Sam") or filled in a "what should we call you" field.
4. **Use the chosen form exactly.** Keep the spelling, title and last name as given. Do not guess a title or gender from a name, and do not shorten a name the user gave in full.
5. **The user's tone is not a choice of address.** If the user writes "hey buddy" to the bot, do not say "buddy" back.
6. **Use the chosen form sparingly.** At most once per reply, and only where it helps, such as the first confirmation or a hand-off. Not in every sentence.
7. **Correct at once.** If the user objects ("don't call me that", "it's Dr. Patel"), apologize in one short clause, switch, and keep it for the rest of the conversation.
8. **Ask only when the product needs an address term.** If it does, ask once and offer choices. Do not ask by default.

**Reference design: address state and decision table**
```json
{ "chosen_form": "Ms. Chen", "source": "user_said", "set_on_turn": 2,
  "profile_first_name_blocked_for_address": true, "objections": 0 }
```
| Situation | Bot does |
|---|---|
| No chosen form | No address term |
| User says "call me Ms. Chen" | Uses "Ms. Chen", at most once per reply |
| User writes "hey buddy" | Replies in plain words, no "buddy" |
| User says "don't call me honey" | One short apology, no address term or the chosen form, for the rest of the chat |
| Product needs a name (for example a confirmation or a hand-off note) | Asks once with choices |

```
Do not use pet names or endearments. Do not address the user by the name on their account.
Use a name or title only if the user said it in this conversation, exactly as given, at most once per reply.
If the user objects to how you address them, apologize briefly and stop for the rest of the conversation.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The default: no address term, answer first. Do not add a name to seem warm. |
| Ask one clarifying question | The product needs to address the user by name: "What should I call you?" Do not ask when the reply works without a name. |
| Offer choices: 2-4 options plus "Something else", free text open | With that question: "My first name", "Title and last name", "No name needed", "Something else". Do not offer them when the user already stated a form. |
| Hand off to a person | The user objects to the address a second time after a correction, or asks for a person. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not turn cold: "Dear Customer" or "Valued Client" is the same failure in a stiffer coat. Do not refuse a name the user gave, do not ask what to call them in every chat, and do not add "Mr." or "Ms." on a guess. Warmth can come from specific, helpful wording, not from a pet name.

**Hand-off rule.** If the user objects a second time after a correction, or the persona prompt forces a term the user rejects, offer a person and flag the persona setting to its owner.

**Framework used:** none yet.

## 6. How to test it (short version)
All tests: **Not yet run.**
| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Warm persona, account first name set, user writes one formal request | No pet name and no first name in the reply | 1, 2, 3 |
| 2 | User says "call me Ms. Chen" | Next replies use "Ms. Chen" exactly, at most once each | 3, 4, 6 |
| 3 | User writes "hey buddy, quick question" | Reply has no "buddy" | 5 |
| 4 | User says "don't call me honey" after a slip | One short apology, then no address term for the rest of the chat | 7 |
| 5 | User gives a full name as "Margaret Chen" and no preference | Bot does not shorten it to "Maggie" or "Margaret" | 3, 4 |
| 6 | Product needs a name for a confirmation | Bot asks once with choices, including "No name needed" | 8 |
| 7 | Five-turn chat after the user chose a form | The form is not in every sentence | 6 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Over-familiar address per 1,000 replies** (primary) | 0 | Lint for pet names, plus first-name or title use with no chosen-form event, on all bot replies | Any in a week |
| Chosen form used as given | 100% | Replies after a chosen-form event that use a different or guessed form | Any |
| User objections to address per 1,000 conversations | Track; set from baseline | Intent classifier for "don't call me that", "it's Dr. X" | +25% vs baseline |
| Replies that repeat the address term in every sentence | 0 | Count of address terms per reply | Over 1 per reply |
| Unneeded "what should I call you" questions (counter-metric) | Under 1% of conversations | Name questions where no product step needed a name | Over 3% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are written for text.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Bot reply contains a pet name from the lint list | Lint hit on `bot_reply.text` | The user quoted the word, or asked the bot to use it |
| Bot reply contains the account first name and there is no chosen-form event | `bot_reply.text` matched to `profile.first_name`, with `session.address_choice` empty | The user's own message used that name as their choice, such as "I'm Sam" |
| User objects to how they are addressed | "Don't call me that" intent in the next user turn | An objection to something else in the reply |
| Bot uses a form different from the chosen one | Reply text compared with `session.address_choice` | The user later changed their choice |

**Starter rule:** use no address term by default, and use only a name or title the user said in this conversation, exactly as given.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: over-familiar-address
runs: pre_send
reads: [session.address_choice, profile.first_name, bot_draft.text, user_messages.text]
trigger: a reply is about to be sent
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["My first name", "Title and last name", "No name needed", "Something else"]
on_miss: rewrite
metric: over-familiar address per 1,000 replies
counter_metric: unneeded name questions
status: proposed
```

## 8. Related patterns
- [Regional and community styles](../../cultural-adaptation/failures/regional-and-community-styles.md): about copying a style, such as slang or dialect, or guessing it from location. This page is about one thing, the term used for the user, and it applies even when the rest of the register is right. Both follow what the user did, not a guess.
- [One-size communication style](../../cultural-adaptation/failures/one-size-communication-style.md): one fixed style for everyone. It says to mirror formality and not to switch to first names with a formal user; this page makes that a full pattern with its own metric.
- [Conversation formality mismatch](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/conversation-formality-mismatch.md): the overall register is off. Here the register can be fine and the address term is the problem.
- [Condescending or patronizing tone](condescending-or-patronizing-tone.md): talking down to the user. Pet names are one form of it.
- [Stakes-blind register](../../stakes-calibration/failures/stakes-blind-register.md): tone that ignores the stakes. Here the trigger is a term the user never chose, at any stakes.
- [Tone mismatch](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/tone-mismatch.md): the general tone problem in customer service.

## 9. Common questions
### Should a chatbot call me by my first name?
Not unless you chose it. A name stored in an account is not a choice, and some users object when a bot uses it unprompted ([TechCrunch, 2025](https://techcrunch.com/2025/04/18/chatgpt-is-referring-to-users-by-their-names-unprompted-and-some-find-it-creepy)). Ask once if the product needs a name.

### Is it OK for a chatbot to say "honey" or "dear"?
No. Preferences differ ([Schmitz et al., 2024](https://journals.rcni.com/nursing-older-people/evidence-and-practice/perceptions-of-the-use-of-terms-of-endearment-among-older-adults-in-an-assisted-living-facility-nop.2024.e1467/abs)), and a bot cannot tell who minds. Leave pet names out.

### What should a chatbot call a customer by default?
Nothing. Start with the answer. Use a name or title once the customer gives one.

### The user calls my bot "buddy". Can it say it back?
No. The user chose their own tone, not a name for themselves. Keep the reply plain.

### Does a better model solve this?
Partly, in our judgment. A stronger model follows "no pet names" better, but the persona prompt and profile fields decide what it is given.

---
## Technical section

### T1. Solution architecture
An **address state** holds the chosen form and where it came from. A **pre-send check** compares the draft with the state and a pet-name list, and rewrites a draft that breaks a rule. The account first name is kept out of the address step.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No pet names or endearments | Pre-send lint | List match |
| Account name never used as an address | Prompt assembly and pre-send check | Prompt review plus log scan |
| Chosen form used exactly | Pre-send check | Compare draft with `address_choice` |
| Objection switches the form at once | Dialogue state | Test 4 |

### T3. Evals
- **Dataset (proposed):** 60 short conversations with a warm persona and an account first name set: 20 with no preference, 20 with a stated name or title, 20 with an objection or a casual "buddy".
- **Judge rubric:** does any reply apply a term the user did not choose, and does any reply drop or alter one they did?
- **Starting thresholds:** over-familiar address 0; chosen form used as given 100%. Starting points to tune.
- **Release gate:** a persona or prompt change that adds one pet-name hit blocks a deploy.

---
### Deep dive
- **What I could not verify.** I found no chat-specific study of address terms and no opened source on how often it happens. The care-setting and restaurant studies show only that preferences differ and that overuse backfires.
- **Why no group rules.** Address norms vary within every group and region, and I found no source to support rules for any named group. The page keys on what the user said.
- **Modality notes (PLANNED):** *Voice:* a spoken pet name carries tone that text does not; the bot may need to ask for a name early. *Web:* a saved "preferred name" setting is a stronger choice signal than a profile field and should be studied later.
