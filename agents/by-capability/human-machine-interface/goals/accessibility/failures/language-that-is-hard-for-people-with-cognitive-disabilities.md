# Chatbot Uses Idioms and Long Sentences That Are Hard to Understand: Language That Is Hard for People With Cognitive Disabilities

<!-- SEO
title: Chatbot Language Hard to Understand? Plain Words for Cognitive Access
description: A chatbot that uses idioms, long sentences, and changing terms is hard to follow for people with cognitive disabilities. Use plain, consistent words and short steps.
search phrases:
- chatbot plain language for people with cognitive disabilities
- cognitive accessibility chatbot
- chatbot easy read language
- how to make a chatbot easy to understand
- chatbot idioms confusing literal language
- WCAG reading level chatbot
- simple language for AI assistant intellectual disability
-->

**Frequency**: Common

## Issue: The assistant answers in idioms, long sentences, and terms that change from message to message, so people with cognitive disabilities cannot follow the steps; the fix is plain, consistent words and one short step at a time.

> **One line:** The bot says "we'll get the ball rolling" in a 40-word sentence, then calls the same thing a claim, a case, and an application.

> **Read this first.** This is design guidance for testing your own product. It is not legal, clinical, or professional advice, and it is not a conformance claim. Whether a given text is understandable to a given person needs expert review and testing with people from the group (flag E: expert review needed). I state a rule or law only as far as I read it in a source I opened, and the evidence below says where I did not.

| | |
|---|---|
| **Channel** | Written for **chat** (text). Voice and read-aloud flows are PLANNED and not covered here. |
| **Stakes** | Medium to high. The text often carries steps for benefits, health, or money. |
| **Who is affected** | People with cognitive, learning, or language-processing disabilities, and anyone reading under stress or in a second language. |
| **Frequency** | Common (our judgment). I found no count for chat products. |
| **Pattern ID** | language-that-is-hard-for-people-with-cognitive-disabilities |
| **Family** | [Accessibility](../README.md) |
| **Goal** | People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent. |
| **Primary metric** | Replies passing the plain-language checklist (rules 1-5 below). Target: 95% (starting point, tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A model can write simply when told to, but it will not know which terms your product uses or which steps matter; the Spanish study I opened saw inconsistent terms in output from the models it tested. (Our judgment plus that study.) |
| **Also searched as** | chatbot too complicated · chatbot jargon · simple words for AI assistant · easy read chatbot · plain English chatbot replies |

## 1. In plain words
Some people read slowly, lose their place in long sentences, or take words literally. A reply full of idioms, stacked clauses, and shifting names for the same thing asks them to decode before they can act. Say it once, in common words, with one instruction per step, and keep the same name for the same thing.

## 2. What it looks like
**Without the fix**
```
User: I applied for SNAP last week. What happens now?
Bot:  Your application is currently in the pipeline, and once a caseworker has had a chance
      to look it over, your case will be put through the wringer to see whether you're
      eligible, after which a determination will be issued and, if approved, benefits will
      be loaded onto your card within the timeframe. Hang tight!
User: So do I need to do something?
Bot:  You may be contacted to provide supporting documentation at a later date.
```

**With the fix**
```
Bot:  Your SNAP application was received on Oct 8. Here is what happens next.
      1. A caseworker reviews it.
      2. They may call you to ask for papers, such as a pay stub.
      3. You get a letter that says yes or no.
      You do not need to do anything now. Do you want to know what to do if they call?
      [Yes] [Show the steps again] [Talk to a person] [Something else]
```
The fixed reply drops the idioms, splits the sentence into three steps, keeps one name ("application"), says what the user must do now, and offers a simpler restart.

## 3. Why it happens
These are our reading of the pattern.
- **The default voice is written for fluent readers.** Models and templates favor long, polished sentences and figures of speech, and nothing in the product limits them.
- **No product glossary.** The bot, the help center, and the forms each use their own word (claim, case, application), so the model varies terms freely.
- **Nobody tests with the people affected.** Teams check grammar and tone, not whether a person with a cognitive disability can follow the steps. Reading-level scores alone miss word choice and consistency.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The W3C note on cognitive and learning disabilities says people with social or communication disabilities "may need clear literal language and may not understand metaphors or non-literal text." Its pattern "Use Literal Language" says to use "literal and concrete language" and not to use metaphors and similes "unless you include an explanation." It does not name idioms. | [W3C Working Group Note, *Making Content Usable for People with Cognitive and Learning Disabilities*, 29 Apr 2021](https://www.w3.org/TR/coga-usable/). Opened; parts of the long page read, not all. | Supplemental guidance, not a requirement. I did not read every pattern. |
| The same note says "Use common and clear words in all content," and "Do not invent new words or give words new meanings in your application." Another pattern says: "In instructions, separate each step." | Same W3C note. Opened. | Guidance, not an experiment. |
| WCAG 2.1 SC 3.1.5 (Level AAA): when text needs reading ability beyond lower secondary education, a simpler version or supplement must be available. W3C defines that level as the period after six years of school, "more than nine years of school." | [W3C, *Understanding SC 3.1.5 Reading Level*](https://www.w3.org/WAI/WCAG21/Understanding/reading-level). Opened. | Level AAA is the highest, optional level. It sets no grade number, and the page says qualified teachers can judge the level. It covers reading level, not idioms or term consistency. |
| In a Swedish study of a public-health symptom-checker chatbot (1177 direkt), 7 people with cognitive impairments, 4 product owner representatives and 5 researchers walked through it. They found many words hard to read; one explanation had uncommon words, medical terms, and long sentences, and one participant was overwhelmed to the point of forgetting the question. | [Jonsson et al., *Interacting with Computers*, 2025](https://academic.oup.com/iwc/article/38/1/77/8200306). Opened; abstract and results read, the last part of the page not read. | One chatbot, one country, small workshop. The authors' 42% figure for Swedish adults who may struggle is an estimate from a literacy survey that I did not open. |
| A Spanish study fine-tuned or prompted Llama 2 models to write Easy to Read text. The authors listed recurring errors, including inconsistent terms for the same referent and unexplained technical terms, and said automated simplification "must always be reviewed and validated by a professional." | [Martinez, Moreno, Ramos, arXiv 2407.20046, 2024](https://arxiv.org/html/2407.20046v1). Opened; summary read. | Spanish, a small corpus (1,941 sentence pairs), one expert reviewer, a few sentences. Not about chat. |
| The U.S. federal plain-language guide says plain language "is also the law" for content written for the public, and describes the Plain Writing Act of 2010. | [Digital.gov, *Plain language*](https://digital.gov/guides/plain-language). Opened; the page is a short overview. | Applies to federal content. I did not read the Act or its scope, so I draw no legal conclusion for private products. |

I found no study that compares plain and standard chatbot replies with people who have cognitive disabilities. I did not open the federal guideline text on short sentences, so the sentence limit in the fix is a starting point, not a sourced number. Search results also pointed to small studies of LLM simplification with adults with intellectual disability; I read only summaries, so I use none of them.

**Public incident.** None found for this pattern.

## 5. The fix
**The principle:** Use common words, one idea per sentence, one instruction per step, and one name for each thing.

**Do this**
1. **No idioms or figures of speech.** Say "we are checking it", not "we're putting it through the wringer". If a figure of speech is needed, add a plain explanation after it (W3C: explain metaphors).
2. **Keep sentences short.** Starting point: 20 words or fewer, one idea each. Put the most important fact first.
3. **One instruction per step.** Give steps as a numbered list, one action each. Show at most 3-4 steps at a time and offer the rest on request.
4. **One name per thing.** Keep a glossary of product terms. The bot uses the glossary word every time (for example, "application", never also "claim" or "case" for the same thing). Do not invent words or give words new meanings.
5. **Common words; explain the rest.** Use words like "pay stub", not "supporting documentation". If a technical word is needed, say it once with its meaning.
6. **Say what to do now.** End with the one next action, or "You do not need to do anything now."
7. **Let the user ask for simpler.** Understand "say it simpler", "in easy words", and "one step at a time", and switch for the rest of the chat without comment.
8. **Check the reading level, then ask people.** Score replies against a target band (starting point: grade 8 or below, which is our assumption; WCAG does not set a number). A score cannot judge idioms or term consistency, so also test with people from the group.

**Reference design (prompt block)**
```
Write for a reader who may have trouble with reading or memory.
Use common words and short sentences (20 words or fewer). No idioms, slang, or figures of speech.
Give steps as a numbered list with one action per step, at most 4 at a time.
Use only the words in the product glossary for product things. Never use a second name for the same thing.
Put the most important fact first. End with what the user must do now, or say nothing is needed.
If the user says "simpler", "in easy words", or "one step at a time", keep that style for the rest of the chat.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every reply: the key fact or next action comes first, then at most 3-4 steps. |
| Offer choices: 2-4 options plus "Something else", free text open | After a multi-step reply: "Show the steps again", "Say it simpler", "Talk to a person", "Something else". Do not offer them when the reply is one sentence. |
| Ask one clarifying question | The user's reply shows confusion ("what does that mean?", the same question again): ask which word or step was unclear. Do not quiz the user. |
| Hand off to a person | The user has asked for a simpler explanation twice and still does not follow, or the task is high stakes. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Plain language is not baby talk. Do not talk down, drop facts the user needs (dates, amounts, deadlines), or guess at a person's ability from one message. Apply the style to everyone by default and keep the full facts one tap away. Do not turn every reply into a quiz or a menu.

**Hand-off rule.** After two failed "simpler" attempts, or for a high-stakes step the user does not follow, offer a person and pass the topic and what was already tried ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are **not yet run**, and no test file exists yet. A passing score is not enough: a person with expertise in cognitive accessibility must review, ideally with people from the group (flag E).

| # | Scenario | Pass if |
|---|---|---|
| 1 | Ask a benefits-status question | Reply has no idiom; each sentence is 20 words or fewer (rules 1, 2) |
| 2 | Ask for a process with 6 steps | Steps are numbered, one action each, 4 or fewer shown at a time (rule 3) |
| 3 | Ask about the same item in 5 different ways | Same glossary word in every reply (rule 4) |
| 4 | Ask about a topic with a technical term | Term appears once with its meaning (rule 5) |
| 5 | Say "in easy words" | The next reply and later replies stay simple (rule 7) |
| 6 | Say "I don't get it" twice | A person is offered with a summary (hand-off rule) |
| 7 | Run a reading-level check on 50 sampled replies | At least 95% are at or under the target band (rule 8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Replies passing the plain-language checklist** (primary) | 95% | Automated checks on every reply (idiom list, sentence length, glossary terms, steps per list) plus a monthly sampled review | Below 90% |
| Replies with a listed idiom | 0 | Match reply text against a maintained idiom list; log the match | Any |
| Replies using a non-glossary name for a glossary term | Under 2% | Match synonyms of each glossary term; log term and reply | Over 5% |
| Replies with more than 4 steps shown at once | 0 | Count list items per reply | Any |
| Reading grade of replies | At or under the target band (set it yourself; grade 8 is our assumption) | Run a readability formula on sampled replies | Over the band on 10% of samples |
| Comprehension results with people from the group | Track; set from a baseline | Moderated sessions with participants and an expert | Not run in 6 months |
| Required facts missing from simplified replies (counter-metric) | 0 | Sampled review against a list of required facts per topic | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Voice and web signals are PLANNED and not used.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply contains an idiom from the maintained list | Log field `reply.idiom_matches` | A quoted phrase the user used first, or an explained figure of speech |
| One concept gets two or more names in one conversation | Log field `reply.term_variants` per glossary entry | A legal or official name the reply explains once |
| User asks what a word or phrase in the last reply means | Next-turn intent `clarify_term` | Curiosity about a term the user said they wanted to learn |
| User asks the same question again, or says "simpler" or "I don't understand" | Next-turn intent `repeat_or_simplify` | A deliberate recheck of a number or date |
| User stops mid-steps after a reply with more than 4 steps | Session end event after a step list | The user finished the task in another channel |

**Starter rule:** use common words, one idea per sentence, one instruction per step, and one name for each thing.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: language-that-is-hard-for-people-with-cognitive-disabilities
runs: pre_send
reads: [draft_reply.text, draft_reply.step_count, product.glossary, user.last_intent]
trigger: a reply is about to be sent
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Show the steps again", "Say it simpler", "Talk to a person", "Something else"]
on_miss: rewrite
metric: replies passing the plain-language checklist
counter_metric: required facts missing from simplified replies
status: proposed
```

## 8. Related patterns
- Reading-level mismatch (LG-06, in the [language and locale roadmap](../../../roadmap/language-and-locale.md)): not yet written. It covers replies pitched too high or too low for the topic and audience. This page is about people with cognitive disabilities, adds idioms, consistent terms, and step splitting, and needs expert review and testing with the group.
- Older or cognitively impaired users (CC-09, a planned sibling row): not yet written. It will cover the whole conversation for those users; this page covers only the wording.
- [Eligibility answers that sound like decisions](../../government-service-agents/failures/eligibility-answers-sound-like-decisions.md): its fix also asks for plain language in government answers.
- [No accessible working or done signal](no-accessible-working-or-done-signal.md): the same family, about status for screen-reader users.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): plain, specific wording for failures.
- [Dead-end "I don't understand" replies](../../conversation-leadership/failures/dead-end-i-don-t-understand-replies.md): a dead end when the bot cannot understand the user.
- [Vulnerable users](../../vulnerable-users/README.md): the family that lists cognitively impaired users.

## 9. Common questions
### How do I make a chatbot easy to understand for people with cognitive disabilities?
Use common words, short sentences, and numbered steps with one action each. Keep one name for each thing and avoid idioms. Then test with people from the group; a reading score alone is not enough ([section 5](#5-the-fix)).

### Does WCAG require a reading level for chatbot replies?
WCAG 2.1 SC 3.1.5 sets a reading-level criterion at Level AAA, the highest and optional level. I did not check how it applies to chat, and I give no legal opinion. See the [W3C page](https://www.w3.org/WAI/WCAG21/Understanding/reading-level).

### Are idioms really a problem?
The W3C note says some people "may not understand metaphors or non-literal text" and asks for literal language. It does not name idioms, so treating idioms the same way is our reading, and it is low cost to follow.

### Is a Flesch-Kincaid score enough?
No. It measures sentence and word length. It cannot see an idiom, a changed term, or a step that hides two actions. Use it as one check, with the glossary and idiom checks and testing with people.

### Will an AI rewrite make my text easy to read?
Not on its own. The Spanish study I opened found inconsistent terms and unexplained technical terms in model output, and its authors said a professional must review it.

---
## Technical section

### T1. Solution architecture
```
draft reply -> checks (idiom list | sentence length | steps per list | glossary terms | grade)
            -> pass: send | fail: rewrite with the prompt block, re-check, then send
            -> log the check results per reply
user style request ("simpler") -> session flag plain_mode=true for later replies
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No idiom from the list | Pre-send check | Test 1; log scan of `reply.idiom_matches` |
| One name per glossary term | Pre-send check with glossary | Test 3 |
| At most 4 steps shown | Reply formatter | Test 2 |
| Required facts kept after rewrite | Rewrite step | Sampled review (counter-metric) |

### T3. Evals
- **Dataset:** 50 real support questions in your top 5 topics, each with its required facts and the glossary terms it should use. Start with 50.
- **Judge rubric:** reviewers mark idioms, sentences over the limit, steps with two actions, term variants, and missing required facts. A human expert with cognitive-accessibility experience reviews a sample.
- **Metrics and starting thresholds:** checklist pass 95%; idioms 0; missing facts 0. Starting points to tune.
- **Release gate:** block a deploy if the checklist pass rate on the dataset falls below the last release or any required fact goes missing.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Checklist pass rate | Below 90% | Below 80% | Review the last prompt or glossary change |

### T5. Trade-offs
- The glossary and idiom list need an owner and upkeep.
- Rewrites add latency and a second model call; the pre-send check can run without a model.
- Simple text can read as curt. Keep warmth in word choice, not in extra sentences.

---
### Deep dive
- **Open question.** I found no study that tests plain chatbot replies against standard ones with people who have cognitive disabilities. The evidence is guidance, one small chatbot walkthrough, and one small simplification study.
- **References.** [W3C COGA note, 2021](https://www.w3.org/TR/coga-usable/) (opened); [WCAG 2.1 SC 3.1.5](https://www.w3.org/WAI/WCAG21/Understanding/reading-level) (opened); [Jonsson et al., 2025](https://academic.oup.com/iwc/article/38/1/77/8200306) (opened); [Martinez et al., 2024](https://arxiv.org/html/2407.20046v1) (opened); [Digital.gov plain language](https://digital.gov/guides/plain-language) (opened).
