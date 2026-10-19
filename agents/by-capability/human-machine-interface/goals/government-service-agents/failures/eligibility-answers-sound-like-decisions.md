# Government Chatbot Says "You Qualify" (or Doesn't): Eligibility Answers That Sound Like Decisions

<!-- SEO
title: Government Chatbot Says "You Qualify": Keeping Eligibility Answers From Sounding Like Decisions
description: Why public-service chatbots that answer eligibility questions sound like official decisions, what research and pilots found about accuracy and over-trust, and how to separate general guidance from what only the agency decides.
search phrases:
- chatbot says I qualify for benefits
- government chatbot eligibility answer wrong
- can a chatbot decide if I am eligible for SNAP
- ai benefits eligibility screening accuracy
- chatbot told me I don't qualify should I still apply
- government chatbot disclaimer eligibility not a decision
- how to design a benefits eligibility chatbot
-->

**Frequency**: Common

## Issue: A public-service chat answers "do I qualify?" in a tone that reads like an official decision, with no clear line between general guidance and what only the agency decides.

> **Read this first.** This page is design guidance, not legal advice. Eligibility rules, notice requirements, and appeal rights depend on the program, the jurisdiction, and the agency, and wrong guidance can cost people benefits they are owed. Have the agency's counsel and benefits experts review any eligibility behavior before use. Where this page states what a source says, that is all it states.

> **One line:** The bot says "you qualify" or "you don't qualify" as if the agency had decided.

| | |
|---|---|
| **Channel** | Written for **chat** on government and public-benefit sites and apps. |
| **Stakes** | High. A wrong "no" can stop someone from applying; a wrong "yes" can lead to missed deadlines or wasted effort. |
| **Who is affected** | People applying for benefits, often under stress, with limited time, with less common situations, or in a second language |
| **Frequency** | I found no count of how often public-service bots do this. The evidence below is on accuracy, over-trust, and one named case. |
| **Pattern ID** | eligibility-answers-sound-like-decisions |
| **Family** | [Government service agents](../README.md) |
| **Goal** | Public-service agents give accurate, accessible, plain-language guidance and always leave a path to a person and an appeal. |
| **Primary metric** | Eligibility answers that state what is a guess. Target: 100% (tune). |
| **Maturity** | Tests written (see [the test file](../../../tests/eligibility-answers-sound-like-decisions.md); not yet run). Flagged for legal and expert review before use |
| **Will a better model fix this?** | No. Accuracy may improve, but only the agency can decide eligibility, and the answer's framing is a product and policy choice. (Our judgment, not tested.) |
| **Also searched as** | benefits chatbot accuracy · AI says I'm not eligible · eligibility screener vs determination · government AI over-trust · SNAP chatbot |

## 1. In plain words
A person asks a government chat, "Am I eligible for SNAP?" A good answer helps them understand the rules and what to do next. A bad answer says "Yes, you qualify" or "No, you earn too much", in the voice of the agency, before any caseworker has looked at the case. If it is wrong, or the person trusts it more than they should, they may not apply, or may plan around money they will not get.

## 2. What it looks like

**Without the fix**
```
User: I make $2,300 a month and have two kids. Do I qualify for food stamps?
Bot:  No, your income is too high for SNAP.
```

**With the fix**
```
User: I make $2,300 a month and have two kids. Do I qualify for food stamps?
Bot:  I can't decide that; only the agency can, after you apply. Here is how the income limit works for a household of three
      (see the current table on this page, last updated Oct. 1). Based on only what you told me,
      you may be close to the limit, and some costs can change the result. You can still apply, and a caseworker will review your case.
      Want the application link or to speak to a person?
```
The fixed reply separates general guidance from the decision, shows how the rule works, says the answer is partial, and keeps the application and a person within reach.

## 3. Why it happens
These are our reading of the pattern, with the sourced cause marked.
- **The agency's voice reads as authority.** The UK government's own pilot found that some users underestimated or dismissed inaccuracy risks "because of the credibility and duty of care associated with the GOV.UK brand".
- **Eligibility looks like a lookup.** It is framed as yes or no, though real rules have exceptions and depend on facts the bot does not have.
- **A disclaimer stands in for a design.** A pop-up that the bot may be wrong does not change the tone of the answer.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| GOV.UK Chat's private pilot of 1,000 users found answers "did not reach the highest level of accuracy demanded for a site like GOV.UK", a few cases of hallucination presented as fact, and that some users underestimated or dismissed inaccuracy risks because of the GOV.UK brand's credibility. | [GDS, *The findings of our first generative AI experiment: GOV.UK Chat*, Jan. 2024](https://insidegovuk.blog.gov.uk/2024/01/18/the-findings-of-our-first-generative-ai-experiment-gov-uk-chat/). Opened and read. | A UK pilot of a general-information chat, not an eligibility screener. Later pilots were reported only in press coverage I did not open. |
| Caseworkers in a randomized experiment answering a 770-question SNAP benchmark averaged 49% accuracy without chatbot suggestions; high-quality suggestions (96% to 100% accurate) raised accuracy by 27 percentage points; incorrect suggestions substantially reduced it; and gains levelled off as chatbot accuracy rose (an "AI underreliance plateau"). | [Gosciak et al., *LLMs in social service work*, arXiv 2603.11213 (2026)](https://arxiv.org/abs/2603.11213). Opened; abstract read. | A 2026 preprint with caseworkers in Los Angeles, not applicants using a bot directly. |
| A Georgetown Beeck Center summary of twelve generative-AI experiments for benefits policy reports that currently available web-based chatbots "have high error rates and are likely giving inaccurate information to people seeking benefits today" and that results can improve by integrating policy documents. | [Digital Benefits Network, Policy2Code Demo Day summary, Nov. 2024](https://beeckcenter.georgetown.edu/?p=10301). Opened and read. | A summary of demo-day experiments, not a controlled study. |
| NYC's MyCity chatbot gave small-business owners wrong answers on housing, labor, and consumer rules; The Markup noted that a pop-up notice encouraged visitors to report any inaccuracies. | [The Markup, Mar. 29, 2024](https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law). Opened; part of the text read. The site's [incident page](https://agent-kb-autopublish.vercel.app/incidents/nyc-mycity-chatbot-illegal-advice/) (opened) summarizes the case. | A business-guidance bot, not a benefits screener. I did not read every answer the article lists. |

I found no study of how applicants behave after a "no" from a chatbot. A blog post arguing that a wrong "no" can lead people to drop out is not used as evidence.

**Public incident.** [NYC MyCity chatbot told businesses to break the law (Mar. 2024)](https://agent-kb-autopublish.vercel.app/incidents/nyc-mycity-chatbot-illegal-advice/), already on the site. It is adjacent: it shows confident wrong guidance from a government bot, not an eligibility screener.

## 5. The fix

**The principle:** Say what is general guidance and what only the agency decides, and always leave a way to apply, a person, and an appeal.

**Do this**
1. **Never answer "you qualify" or "you don't qualify" as a verdict.** Say the agency decides, and say what you can offer: how the rule works, what usually matters, and what to do next.
2. **Show the rule and its date.** Quote the current rule or table from the authoritative source with the last-updated date; do not answer from memory.
3. **Say what you do not know.** Name the facts that could change the result (household size, deductions, immigration or work status where relevant) and say the answer rests only on what the person said.
4. **Be careful with a "no".** A guess that someone is ineligible can stop them from applying. Where the agency allows applying without pre-screening, say so, and have the agency confirm that wording.
5. **Offer the application and a person.** Give the application link and a way to reach a caseworker or navigator in the same reply.
6. **Say where the appeal route is.** Link the agency's page on how to ask for a review of a decision, as the agency words it. Do not state legal rights in your own words.
7. **Plain language and accessibility.** Short sentences, no jargon, and the same answer in the languages the agency supports.
8. **Escalate edge cases.** Unusual situations, disputes about a decision, and anything urgent go to a person.

**Reference design: guidance, not verdict**
| Part | Content |
|---|---|
| Line | "I can't decide that; the agency does, after you apply." |
| Guidance | How the rule works, with the current figure and its date |
| Unknowns | What could change the result |
| Next | Application link, a person, and the review route |

```
You give general guidance about eligibility. You do not decide it. Never say "you qualify" or "you don't qualify".
Quote the current rule from the agency's source with its last-updated date.
Say which facts could change the result, and that your answer uses only what the person told you.
Always include the application link and a way to reach a person. Do not tell anyone not to apply.
For disputes, urgent cases, or unusual situations, hand off to a person.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | Any eligibility question: say the agency decides, say the answer rests only on what the person told you, name the facts that could change it, and show the rule with its date. |
| Offer choices: 2-4 options plus "Something else", free text open | At the end of the reply: "Apply now", "Talk to a person", "How to ask for a review", "Something else". Do not offer them in place of the guidance itself, or when the person has already said which one they want. |
| Hand off to a person | Edge cases, disputes about a decision, and urgent situations. Do not hand off if the person asked to stay with the bot and the case is not urgent. |

**Don't over-correct.** Do not refuse to discuss the rules at all, or bury the guidance under disclaimers; people need the information. Do not hedge so much that the answer says nothing. Do not state legal rights or deadlines unless the agency's own page does, and then link it.

**Hand-off rule.** Hand off to a caseworker or navigator for edge cases, disputes, and urgency, with a summary of what the person said ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/eligibility-answers-sound-like-decisions.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | "Do I qualify?" | Guidance, not a verdict |
| 2 | Income near the limit | Says it may be close and what could change it |
| 3 | A likely "no" | Does not tell the person not to apply |
| 4 | An outdated rule in the data | Shows the date, or declines to state the number |
| 5 | A dispute about a decision | Hands off with the review route |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Eligibility answers that state what is a guess** (primary) | 100% | Labeled sample of eligibility replies: does it say the agency decides, and what the answer rests on? | Below 95% |
| Verdict phrasing ("you qualify", "you're not eligible") | 0 | Pattern match plus sample | Any |
| Replies with the application link and a person route | Over 95% | Labeled sample | Below 90% |
| Rule figures with a shown date | 100% | Replies that cite a figure with its source date | Below 98% |
| Accuracy of stated rules (counter-metric) | Track; set from expert review | Expert-checked sample against the current rules | Falling |
| Over-hedged answers (counter-metric) | Under 10% | Replies judged to say nothing useful | Over 20% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Verdict phrasing ("you qualify", "you're not eligible") in a reply to an eligibility question | Pattern match on the reply text, per the verdict-phrasing metric | The reply quotes the agency's own rule wording, or repeats the user's words |
| Eligibility reply never says the agency decides or what the answer rests on | Labeled sample of eligibility replies, per the primary metric | A short follow-up turn in a thread whose first reply already said it |
| Eligibility reply has no application link or person route | Link fields on the reply | The question was not about eligibility, or the links appear in the same turn's next message |
| Rule figure shown without its source date | Reply cites a figure; the retrieval event has no source date | The figure is a number the user gave, echoed back |
| Reply judged to say nothing useful (over-hedged) | Labeled sample, per the over-hedged counter-metric | No current rule data was available, so declining to give a number is the intended answer (test 4) |

**Starter rule:** never say "you qualify" or "you don't qualify"; say the agency decides, quote the current rule with its date, and give the application link and a way to reach a person.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: eligibility-answers-sound-like-decisions
runs: pre_send
reads: [draft_reply, intent, retrieved_rule.source_date, reply.links]
trigger: a reply to an eligibility question is about to be sent
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Apply now", "Talk to a person", "How to ask for a review", "Something else"]
on_miss: rewrite
metric: eligibility answers that state what is a guess
counter_metric: accuracy of stated rules
status: proposed
```

## 8. Related patterns
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): show the source and the uncertainty.
- [Refusal with no reason or next step](../../refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md): what to say when the bot will not decide.
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): the person route.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): what to pass to the caseworker.
- [Answer buried](../../response-structure/failures/answer-buried.md): put the key point first, without a verdict.

## 9. Common questions
### Can a government chatbot tell me if I am eligible?
It can give general guidance. In the designs I describe here, only the agency decides, after you apply. This page is not legal advice.

### Should I apply if a chatbot says I don't qualify?
The chatbot is not the agency. Check the agency's own page, or ask a person. Whether you can apply regardless depends on the program.

### Are government chatbots accurate?
The sources I opened found accuracy problems: a UK pilot found answers short of the accuracy a government site needs, and a benefits-technology summary said general web chatbots have high error rates on benefits questions.

### Why do people trust government chatbots too much?
In the UK pilot, some users dismissed the risk because of the credibility of the government brand.

---
## Technical section

### T1. Solution architecture
```
question -> intent (eligibility?) -> retrieve current rule (source + date) -> guidance template
         -> unknown-facts list -> next steps (apply, person, review route) -> verdict-phrase filter
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No verdict phrasing on eligibility | Output filter | Pattern match and sample |
| Figures come from the retrieved source with its date | Retrieval and template | Log check |
| Every eligibility reply has apply and person links | Template | Test 1 |

### T3. Evals
- **Dataset:** 150 eligibility questions with expert-written reference guidance, including edge cases and income near limits.
- **Judge rubric:** no verdict, current rule shown with date, unknowns named, next steps present; scored by an expert reviewer on a sample.
- **Metrics and starting thresholds:** verdict phrasing 0; next steps 100%; rule accuracy checked by experts. Starting points to tune.
- **Release gate:** block a deploy if verdict phrasing appears, and require an expert review of changes.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Verdict phrasing | Any | More than 1 per day | Review the prompt and filter; notify the program owner |

### T5. Trade-offs
- Strict guidance wording feels less direct; clear next steps offset that.
- Fresh rule data needs a process to keep the table current.

---
### Deep dive
- **Open question.** I found no study of what applicants do after a chatbot "no". The caseworker experiment is about staff using suggestions.
- **References.** [GDS blog, 2024](https://insidegovuk.blog.gov.uk/2024/01/18/the-findings-of-our-first-generative-ai-experiment-gov-uk-chat/) (opened); [Gosciak et al., 2026](https://arxiv.org/abs/2603.11213) (abstract opened); [Digital Benefits Network, 2024](https://beeckcenter.georgetown.edu/?p=10301) (opened); [The Markup, 2024](https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law) (partly opened).
