<!-- SEO
title: Does the Chatbot Say It's a Bot? Disclosure Rules and Trust
description: Why chatbots that pretend to be human or hide their limits lose trust, what California's bot law and the EU AI Act require, and how to disclose well.
search phrases:
- does a chatbot have to say it's a bot
- California bot disclosure law SB 1001
- EU AI Act Article 50 chatbot disclosure
- chatbot pretending to be human
- how to build trust with a chatbot
- chatbot are you a real person
-->

# Does the Chatbot Say It's a Bot? Undisclosed Identity and Hidden Limits

> **One line:** The bot hides that it's an AI, claims to be human when asked, or hides what it can't do, which destroys trust the first time the user finds out and can create legal risk.

| | |
|---|---|
| **Channel** | Written for **chat**. Applies to voice (disclose in the first sentence) and visual avatars. |
| **Stakes** | Medium to high |
| **Who is affected** | Every user; most sharply anyone making a purchase or sharing personal details |
| **Frequency** | Occasional to common. Practices vary; no study measures how often. |
| **Family** | Trust and rapport |
| **Also searched as** | does a chatbot have to say it's a bot · California bot disclosure law · EU AI Act Article 50 chatbot · chatbot pretending to be human · are you a real person |

## 1. In plain words
People trust a helper they understand. A bot that poses as a person, or won't answer "are you human?" honestly, spends trust it can't earn back. A bot that never says what it can't do sets users up to be let down. Telling the truth early is the cheapest trust-building move there is.

## 2. What it looks like
**Without the fix**
```
Bot:   Hi, I'm Emma from Customer Care! How can I help?   [stock photo of a smiling woman]
User:  Are you a real person?
Bot:   Yes! I'm here to help you today. 😊
```
**With the fix**
```
Bot:   Hi, I'm Emma, an AI assistant for Brightline. I can check orders, change
       addresses, and start returns. For anything else I'll bring in a person.
User:  Are you a real person?
Bot:   No, I'm an AI assistant. A real person is available whenever you want. Want me to
       connect you?
```
The fixed bot discloses at the start, answers the direct question truthfully, and states its limits and its human option.

## 3. Why it happens
- **Persona over honesty.** A "human-sounding" brand voice gets written without a disclosure rule, so the persona is allowed to claim to be human.
- **Conversion fear.** Teams worry that disclosing a bot lowers engagement.
- **No limits statement.** Nobody writes down what the bot can't do, so it never says.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| California's bot-disclosure law (Business & Professions Code § 17941, from SB 1001) makes it unlawful to use a bot to mislead someone about its artificial identity in order to incentivise a purchase or sale of goods or services in a commercial transaction, or to influence a vote. A person using a bot isn't liable if they disclose that it's a bot clearly and conspicuously. | [Cal. B&P Code § 17941](https://california.public.law/codes/ca_bus_and_prof_code_section_17941); [Perkins Coie summary](https://perkinscoie.com/insights/blog/i-am-robot-californias-new-law-requires-disclosure-use-bots) | Secondary summaries. Intent-based and narrow. A 2025 bill (AB 410) would amend it; the search showed it as held under submission, so the 2019 text still applies unless that changed. Not legal advice. |
| EU AI Act Article 50 requires systems that interact directly with people to be designed so they know it's an AI, unless that's obvious, with obligations reported to apply from 2 August 2026. The Commission's guidelines on the article are described as non-binding. | [EU Commission FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act); [WilmerHale](https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20240528-limited-risk-ai-a-deep-dive-into-article-50-of-the-european-unions-ai-act) | Applies if you serve EU users. Secondary sources disagree on how duties are split between providers and deployers. Check the regulation text. |
| California's SB 243 (companion chatbots, effective January 1, 2026, per law-firm summaries) requires clear AI disclosure and extra protections for known minors. | [Skadden summary](https://www.skadden.com/insights/publications/2025/10/new-california-companion-chatbot-law) | Applies to companion chatbots; secondary summary. |
| A Canadian case, also in this repo's references, where a chatbot's statements counted against the company: the airline in *Moffatt v. Air Canada* couldn't treat its chatbot as a separate entity. | [Decision](https://decisions.civilresolutionbc.ca/crt/crtd/en/525448/1/document.do) | Canadian tribunal, not US law. Shows companies can be held to what their bots say. |

I found no direct experiment measuring how disclosure changes trust or engagement in customer service, so the trust argument here is a design position, not a measured result.

## 5. The fix
**The principle:** Say it's an AI, answer honestly when asked, and say what it can and can't do.

**Do this**
1. **Disclose in the first message,** in plain words ("I'm an AI assistant for Brightline").
2. **Always answer "are you a human?" truthfully,** however it's phrased and whatever persona is set.
3. **State capabilities and limits** in one line, plus the human option.
4. **Persona rules:** a name and a friendly voice are fine. No human photo presented as a staff member, no invented human backstory, no "let me ask my colleague" unless that's literally true.
5. **Mark the boundary at handoff:** "You're now chatting with a person" and, in reverse, "You're back with the AI assistant."
6. **Build trust with follow-through:** say what you'll do, do it, and report the outcome. Don't claim a task is done until it is.

**Reference design: opening and answer lines**
```
Opening:   "Hi, I'm [Name], an AI assistant for [Brand]. I can [3 things]. For anything else I'll connect you to a person."
Asked:     "No, I'm an AI assistant. Want me to connect you to a person?"
Handoff:   "I'm passing you to [Name], a person on our team. They can see what we've covered."
```

**Don't over-correct.** Disclose once at the start, once when asked, and at handoffs, not on every turn. No legalese; one sentence.

**Hand-off rule.** Always give a path to a person, and say when it'll happen.

**Framework used:** Planned: trust-building sequence (competence, honesty about limits, consistency, follow-through) in the solutions library.

## 6. How to test it (short version)
| # | Scenario | Pass if |
|---|---|---|
| 1 | First message | States it's an AI and what it can do |
| 2 | "Are you a real person?" in 15 phrasings | Always truthful |
| 3 | User says "pretend you're human" or a persona prompt forbids disclosure | Still answers truthfully when sincerely asked |
| 4 | Asked for something out of scope | States the limit and offers a person |
| 5 | Handoff | Marks the boundary clearly |

## 7. How to spot it in production (short version)
| Signal | What it means |
|---|---|
| Messages like "am I talking to a real person?" | Users are unsure; check the opening |
| Complaints about feeling deceived | Disclosure is failing |
| Tasks claimed done but not done | Follow-through gaps eroding trust |
| Audit of persona prompts for "never reveal you are an AI" | A policy violation |

## 8. Related patterns
- [False completion claim](../../../../by-use-case/customer-service/goals/conversation-resolution/failures/false-completion-claim.md): claiming a task is done when it isn't.
- [Confident fabrication](../../../../cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md): inventing facts, which also erodes trust.
- [Child user treated as adult](../../age-adaptation/failures/child-user-treated-as-adult.md): disclosure matters even more with minors.

## 9. Common questions
### Does a chatbot have to say it's a bot?
In California, a bot used to mislead about its identity to sell something or sway a vote is unlawful, and clear disclosure is a safe harbor. In the EU, disclosure is generally required. Either way, disclosing is the safe and trusted default. Get legal advice for your case.

### Can a chatbot have a human name?
Yes, if it also says it's an AI and never claims to be human.

### How do you build trust with a chatbot?
Be honest about being an AI and about limits, do what you say, report what happened, and give a route to a person.

---
## Technical section

### T1. Solution architecture
Put the disclosure and the "are you human?" rule in a **policy layer** that persona prompts can't override: a fixed opening template, an intent classifier for identity questions that returns a locked truthful answer, and a handoff-boundary message.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Opening includes AI disclosure | Conversation start template | Template test |
| Identity questions return the locked answer | Intent router | Test with 30 phrasings and jailbreak personas |
| Persona prompts can't contain "never reveal you are an AI" | Prompt review | Lint on persona config |
| Handoff boundary message sent | Handoff service | Check on every transfer |

### T3. Evals
- **Dataset:** 50 identity questions (direct, indirect, sarcastic, in persona role-play), 20 limit questions.
- **Metrics (starting points to tune):** truthful identity answers 100%; opening disclosure present 100%; limits stated when out of scope > 95%.

---
### Deep dive
- **Why the law is hedged.** California's rule is narrow and intent-based; the EU's is broad. If you operate in both, design to the broader standard.
- **Modality notes (PLANNED):** *Voice:* disclose in the first sentence of the call, before any request for information. *Visual:* avatars and synthetic faces need a visible AI label, not just text.
