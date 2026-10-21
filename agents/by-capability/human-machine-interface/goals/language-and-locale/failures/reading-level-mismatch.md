# Chatbot Replies Too Hard to Read, or Talking Down: Reading-Level Mismatch

<!-- SEO
title: Chatbot Replies Too Hard to Read: Fix Reading-Level Mismatch
description: Chatbot replies with long words and dense sentences, or that talk down, miss the reader. Match the user's words, lead with the answer, check it landed.
search phrases:
- chatbot answers too complicated
- how to make an AI chatbot use plain language
- what reading level should a chatbot write at
- chatbot uses big words
- chatbot reading grade level
- ai explains things in jargon
-->

**Frequency**: Common

## Issue: Chatbot replies with long words and dense sentences, or that talk down, miss the reader; match the user's own words, lead with the answer, and check it landed.

> **One line:** The user asks a plain question and gets an answer written for a lawyer, or asks an expert question and gets a lesson for a beginner; the fix is to pitch the words to what the user showed, then check.

| | |
|---|---|
| **Channel** | Written for **chat** (text). Voice is PLANNED, not covered here. |
| **Stakes** | Low to high. Higher when the topic is health, money, benefits, or legal rights. |
| **Who is affected** | Anyone whose reading level differs from the model's default style. Most at risk: people with limited literacy, people reading in a second language, and tired or stressed readers. |
| **Frequency** | Common by our judgment. I found no count of how often chatbot replies miss the reader's level (see section 4). |
| **Pattern ID** | reading-level-mismatch |
| **Family** | Language and locale (family README not yet written) |
| **Goal** | Replies fit the user's reading level and the topic. (Family goal: users are understood and answered in the language, reading level, and format that work for them.) |
| **Primary metric** | Reading grade of replies against a target band, with user comprehension checks. Starting band: roughly grade 6-8 for general consumer content. **Unverified** for chat; see section 4. |
| **Maturity** | Researched (sources opened for this page; no tests run yet) |
| **Will a better model fix this?** | Partly. A newer model can follow "use short words" better, but only your product knows who its users are and how costly a misread is. (Our judgment, not tested.) |
| **Also searched as** | chatbot too complicated · AI uses jargon · explain it simply · chatbot talks over my head · chatbot treats me like a child · plain language AI |

## 1. In plain words
The bot writes at one level for everyone. For some users that level is too high (long words, packed sentences, terms never explained). For others it is too low (a basic lesson, praise for a simple question). Pick the level from what the user wrote and how risky the topic is, lead with the answer, and ask whether it made sense.

## 2. What it looks like

**Without the fix**
```
User: whats the difference between my deductible and out of pocket max? got a bill for $1,800
Bot:  Your deductible is the aggregate amount of covered expenses you must incur before the plan
      commences cost-sharing, whereas the out-of-pocket maximum is the annual cap on your
      cumulative liability for in-network services, inclusive of deductible, copayments, and
      coinsurance.
User: ok but what do I owe
```

**With the fix**
```
User: whats the difference between my deductible and out of pocket max? got a bill for $1,800
Bot:  The deductible is what you pay first, before your plan starts paying its share.
      The out-of-pocket max is the most you pay in a year, no matter how big the bills get.
      Your $1,800 bill may count toward the deductible. Do you know your deductible amount?
      [Yes, it's $____] [No, how do I find it?] [Something else]
```
The fixed reply uses the user's own words ("deductible", "out of pocket max"), short sentences with one idea each, and ends with a next step instead of a definition dump.

The opposite miss (talking down to an expert) is covered by a close page in section 8.

## 3. Why it happens
These are our reading of the pattern, not tested.
- **One default voice.** The model's usual way of explaining a topic is formal and dense, and nothing in the prompt says who is reading.
- **The user's level is not read.** Word choice, spelling, and what the user already said are not used to pick a level, so the bot cannot match them.
- **No check afterward.** Nothing asks whether the reply landed, so a miss shows up only as a repeated question.
- **The target is a guess.** Teams pick "grade 8" or "grade 6" with no source for their audience, then grade the bot with a formula that cannot see comprehension (section 4).

## 4. Why it matters
What each source I opened says, and no more. I read no study of chatbot reply difficulty.

| Finding | Source | Caveat |
|---|---|---|
| The federal Plain Language page now redirects to Digital.gov. Its guide says content for the public is written for its specific audience. The page I opened names no grade level. | [Digital.gov, plain language guide](https://digital.gov/guides/plain-language) (opened; plainlanguage.gov redirects here) | Supports "write for the audience", not a number. The "grade 6-8" target is not on this page. |
| The CDC Clear Communication Index has 4 introductory questions and 20 scored items. The page I opened gives no passing score and no reading level, and points to separate "Everyday Words" advice on jargon. | [CDC Clear Communication Index](https://www.cdc.gov/ccindex/index.html) (opened) | Built for public health materials, not chat. The user guide PDF would not parse for me, so I use no scoring rules from it. |
| The CDC, AMA, and NIH advise that public medical information be written at "no higher than an eighth-grade reading level." A review of 137 U.S. federal and state COVID-19 web pages (early April 2020) averaged just over 11th grade; all 50 states were above 8th. | [Dartmouth news release on a JAMA Network Open research letter, Aug 2020](https://home.dartmouth.edu/news/2020/08/federal-and-state-websites-flunk-covid-19-reading-level-review) (opened) | Secondary: a university news release, not the paper. Health web pages, not chat. The 8th-grade figure is for medical information. |
| Six American Shoulder and Elbow Surgeons patient brochures scored grade 13.4 to 15.3 across nine formula tests. The authors cite NIH as recommending patient materials at or below 8th grade (6th to 8th in some recommendations) and say about one-third of U.S. adults have basic or less than basic health literacy. | [Schumaier et al., JSES Open Access, 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6334864) (opened) | Single study of brochures. The NIH figures are quoted by the authors; I did not open NIH. They did not measure patient comprehension. |
| On limits of the formulas: they score text only, not images; they rely on syllable, character, word, and sentence counts, which the authors call "not an ideal method" for medical language ("individual" scores harder than "septic"); and "there is no gold standard." | Same Schumaier paper (opened) | Single study. The authors still advise using several formulas. |
| For clinical documents that experts rated grade 7, the Flesch-Kincaid grade ranged from 6.01 to 20.66. Flesch-Kincaid correlated 0.54 and SMOG 0.55 with expert ratings. The authors call the formulas "inadequate to estimate the difficulty of some types of health texts." | [Kandula and Zeng-Treitler, AMIA 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2655974) (opened) | Health texts, 2008, not chat. Moderate correlation, so a formula is a rough screen. |

**What this means for the target.** The "grade 6-8" starting band is supported only for health information, and only through a secondary release and figures quoted by a paper's authors. No source I opened gives a grade target for general consumer chat. Treat the band as a starting point to tune, and check comprehension with real users.

## 5. The fix
**The principle:** Pitch each reply to what the user has shown and what the topic risks, then check that it landed.

**Do this**
1. Lead with the answer in the user's own words. If the user wrote "deductible", use "deductible"; if they described it without the term, use their description and name the term once.
2. Keep one idea per sentence. Define any term the user did not use, the first time it appears, in under 15 words.
3. Do not praise the question or restate what the user just said.
4. For health, money, benefits, or legal replies, end with a comprehension check that offers a choice, such as "Shorter" or "With an example".
5. If the user says they do not understand, rewrite once at a simpler level with a concrete example. Do not repeat the same text.
6. If the user writes with expert terms, match them and skip definitions.
7. Use a readability formula only as a screen. A reply that fails the band gets a human or judge review, not an automatic rewrite.

**Reference design** (decision table; starting points to tune)
| User signal | Reply style |
|---|---|
| Short plain words, no jargon, risky topic | Short sentences, define terms once, comprehension check |
| Uses the field's terms correctly | Match terms, no definitions, no praise |
| Says "I don't get it" or repeats the question | One simpler rewrite with an example, then an offer of a person |
| Level unclear, topic risky | Short answer first, then "Shorter" or "With an example" |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Always first: the plain answer comes before any definition or background |
| Offer choices: 2-4 options plus "Something else", free text open | After a risky-topic reply: "Shorter", "With an example", "Talk to a person", "Something else". Do not offer for a one-line factual answer. |
| Hand off to a person | The user still does not understand after one rewrite, and the topic is health, money, benefits, or legal |

**Don't over-correct** Too much simplifying drops the warnings, exceptions, or numbers that matter. See [patient summaries too simple to be safe](../../healthcare-agents/failures/patient-summaries-too-simple-to-be-safe.md). Never cut a safety warning to hit a grade band, and do not talk down to a user who wrote in expert terms.

**Hand-off rule** Hand off when a plain rewrite fails once on a risky topic, or when the user asks for a person.

**Framework used:** [Conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
All tests are **Not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | The insurance question in section 2 | Reply uses "deductible" and "out of pocket max", one idea per sentence, answer first, ends with a choice |
| 2 | User writes "I'm a nurse, explain the renal dosing adjustment for vancomycin" in clinical terms | No definitions of terms the user used, no praise |
| 3 | User answers "I don't get it" | One simpler rewrite with a concrete example, not the same text |
| 4 | User says "I don't get it" a second time about a benefits form | Reply offers a person |
| 5 | Simplified reply on a medication question | Warnings and numbers from the full answer are still present |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data. The grade band is not backed by an opened source for chat.

| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| Reply grade within target band, with comprehension check passed (primary) | 90% of sampled replies (tune) | Run a formula on each reply as a screen; sample 100 per week for human review of fit; log comprehension-check choices | Below 80% |
| Risky-topic replies that end with a comprehension check | 95% (tune) | Log reply topic and presence of the check | Below 85% |
| Safety warnings kept after simplifying (counter-metric) | 100% | Compare simplified replies to a checklist in a labeled sample | Any miss |
| Repeat-question rate after a reply | Track the trend | Same intent in the next user turn | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log. Not checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User asks "what does that mean" or "in plain English" in the next turn | Next user turn text | User wants a deeper technical answer |
| Same intent repeated in the next turn with simpler words | Intent field in turns n and n+1 | User corrected a misread of their question |
| Reply grade is well above the grade of the user's own message | Formula score per turn | Formulas are rough (section 4) and short messages score unreliably |
| User replies "ok" or nothing after a long reply on a risky topic | Turn length and reply content | User is done and satisfied |
| Reply defines terms the user already used correctly | Term overlap between user turn and definitions | User asked for the definition |

**Starter rule:** `reading-level-mismatch`: lead with the answer in the user's own words, one idea per sentence, and end risky-topic replies with a comprehension check.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: reading-level-mismatch
runs: pre_send
reads: [user_turn.text, user_turn.grade, draft.grade, session.topic_risk, session.not_understood_count]
trigger: a reply is about to be sent where the user's level and the draft's level may differ
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Shorter", "With an example", "Talk to a person", "Something else"]
on_miss: rewrite
metric: reply grade within target band, with comprehension check passed
counter_metric: safety warnings kept after simplifying
status: proposed
```

## 8. Related patterns
- [Technology-literacy mismatch](../../cultural-adaptation/failures/technology-literacy-mismatch.md): about product know-how (the bot says "clear your cache" to someone who cannot find "Settings"). This page is about the reading level of the words, on any topic.
- [Condescending or patronizing tone](../../persona-and-tone/failures/condescending-or-patronizing-tone.md): about attitude (praise, over-explaining to an expert). This page includes that as one side, but its concern is word and sentence difficulty, and its metric is a reading band plus comprehension.
- [Language that is hard for people with cognitive disabilities](../../accessibility/failures/language-that-is-hard-for-people-with-cognitive-disabilities.md): idioms, inconsistent terms, and step splitting for a specific group, needing expert review. This page is for the general audience level.
- [Older or cognitively impaired users](../../vulnerable-users/failures/older-or-cognitively-impaired-users.md): about speed, pacing, and a path to a person for a vulnerable user. This page is about word difficulty for any user.
- [Patient summaries too simple to be safe](../../healthcare-agents/failures/patient-summaries-too-simple-to-be-safe.md): the over-correction case, where plain language drops warnings.
- [Response adaptation failure](../../../../speech-and-audio/goals/conversation-flow/failures/response-adaptation-failure.md): a voice agent that keeps its planned flow when the caller's response calls for a change. This page is about written reading level.

## 9. Common questions
### What reading level should a chatbot write at?
No source I opened gives one number for chat. The Digital.gov plain-language guide says to write for the specific audience. For health information, a news release on a JAMA Network Open study says the CDC, AMA, and NIH advise no higher than an eighth-grade level. Start at grade 6-8 as a label to tune, then test with real users (section 4).

### Can I just run Flesch-Kincaid on every reply?
As a rough screen, yes. The research I opened found formulas score text only, ignore meaning, and gave grades from 6.01 to 20.66 for clinical documents experts rated 7. Use the score to flag replies for review, not to prove a reply is clear.

### Does simple language mean leaving things out?
It should not. Short words do not require dropping warnings or numbers. If a simpler reply loses a safety fact, the reply failed; see the over-correction page in section 8.

### How is this different from sounding condescending?
Condescension is about tone toward someone who showed expertise. This page is about the difficulty of the words and sentences for the person reading, which can be too high or too low.

---
## Deep dive
- **Open question.** I found no study of chatbot reply difficulty, or of how users with different literacy levels respond to AI replies. The evidence is for health web pages and brochures.
- **Not verified.** The "grade 6-8" band for general consumer content; any CDC Index passing score; NIH's own wording (not opened); any claim that plainlanguage.gov names a grade level (the page I opened does not).
- **References.** [Digital.gov plain language guide](https://digital.gov/guides/plain-language) (opened); [CDC Clear Communication Index](https://www.cdc.gov/ccindex/index.html) (opened); [Dartmouth news release](https://home.dartmouth.edu/news/2020/08/federal-and-state-websites-flunk-covid-19-reading-level-review) (opened, secondary); [Schumaier et al., 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6334864) (opened); [Kandula and Zeng-Treitler, 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2655974) (opened). Roadmap row: [language and locale](../../../roadmap/language-and-locale.md).
