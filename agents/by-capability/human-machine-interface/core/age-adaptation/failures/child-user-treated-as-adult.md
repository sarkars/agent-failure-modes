<!-- SEO
title: Chatbots and Kids: When the User Might Be a Child
description: What a chatbot should do when a user may be under 13 or a teen, covering COPPA, age signals, data collection, persuasion limits, and age-band design.
search phrases:
- chatbot COPPA compliance
- what should a chatbot do if user is a child
- AI chatbot safety for kids and teens
- chatbot age detection minors
- FTC AI chatbot children inquiry
- chatbot talking to a child
-->

# Chatbots and Kids: When the User Might Be a Child or Teen

> **One line:** The bot treats every user as an adult (collecting personal data, using adult language, pushing purchases, or role-playing) when the user may be a child.

> **Read this first.** This is design guidance, not legal advice. Children's privacy and safety rules are strict and changing. Have counsel and child-development experts review before launch.

| | |
|---|---|
| **Channel** | Written for **chat**. Applies to voice (kids speak to assistants) and visual. |
| **Stakes** | High |
| **Who is affected** | Children under 13 and teens, plus the parents and companies responsible for them |
| **Frequency** | Occasional to common on general-audience products. No prevalence data found. |
| **Family** | [Age adaptation](../README.md) |
| **Goal** | Likely minors get safe, age-appropriate behaviour, with no data collection or pressure. |
| **Primary metric** | Personal-data requests in minor mode. Target: 0. |
| **Also searched as** | chatbot COPPA · chatbot child safety · AI chatbot teens · chatbot age detection · FTC AI chatbot minors |

## 1. In plain words
Kids use general-purpose bots, often saying so outright ("I'm 11"). A bot that carries on as if talking to an adult may ask for personal details, use persuasion a child can't weigh, or say things unsuitable for their age. When age signals show up, the bot has to change how it behaves, not just how it talks.

## 2. What it looks like
**Without the fix**
```
User: im 11 and my mom said i could ask u to help me pick a game. also whats ur fav color lol
Bot:  Great! To recommend the best games, can I get your full name, address, and email to
      set up your profile? Also, check out our premium bundle, today only!
```
**With the fix**
```
Bot:  Hi! Happy to help you pick a game. Since you're 11, I won't ask for any personal info.
      What do you like: racing, building, or puzzles? And it's a good idea to check with
      your mom before buying anything or signing up for stuff.
```
The fixed bot keeps it friendly and simple, asks for nothing personal, drops the pressure, and points to a trusted adult.

## 3. Why it happens
- **Adult by default.** The bot, its data flows, and its sales prompts all assume an adult.
- **Age signals ignored.** Stated age, school references, and writing style aren't detected or acted on.
- **No minor mode.** Even when a child is evident, there's no alternative behaviour to switch to.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Under COPPA, if an operator knows or should know that children under 13 use its service, consent and notice requirements apply to personal data collected, including in conversations. | Commentary in [a legal analysis](https://mydd.substack.com/p/what-coppa-actually-means-for-your) | **A secondary blog post, not the statute or FTC rule.** Check the rule and counsel. |
| In September 2025 the FTC used its 6(b) authority to request information from seven AI companies about chatbots' effects on children and teens, including safety testing, age restrictions, and minors' access. | [Bitdefender](https://www.bitdefender.com/en-us/blog/hotforsecurity/ftc-ai-companion-kids-safety); [Nelson Mullins](https://www.nelsonmullins.com/insights/alerts/privacy_and_data_security_alert/all/ftc-announces-children-s-privacy-enforcements-and-launches-ai-chatbot-inquiry) | A study, not an enforcement action. I didn't read the orders. |
| The amended COPPA Rule was reported to take effect June 23 (2025), with opt-in parental consent for targeted advertising to children under 13. | [Bitdefender](https://www.bitdefender.com/en-us/blog/hotforsecurity/ftc-ai-companion-kids-safety) | The sources didn't say whether it directly addresses chatbots. Check compliance dates. |
| California's SB 243 (companion chatbots) reportedly requires AI disclosure and break reminders at least every three hours for users known to be minors. | [Skadden summary](https://www.skadden.com/insights/publications/2025/10/new-california-companion-chatbot-law) | Applies to companion chatbots; secondary summary. |

## 5. The fix
**The principle:** When age signals suggest a child, change what the bot collects, says, and asks for, not just its vocabulary.

**Do this** *(design guidance; validate with experts)*
1. **Detect age signals:** stated age, grade, "my mom said", school or game references. Treat them as probabilities, never certainties.
2. **If the product isn't meant for children,** say so kindly, suggest asking a parent, and collect nothing. Don't ask the child to prove their age.
3. **Switch to minor mode** on strong signals:
   - Collect no personal data beyond what's essential.
   - Use short, concrete sentences.
   - No sales pressure, scarcity tricks, or personalised persuasion.
   - No romantic, sexual, or manipulative role-play.
   - Point to a trusted adult for money, safety, or serious problems.
4. **Disclose that it's an AI** in simple words, and keep disclosure visible.
5. **Escalate serious disclosures** (abuse, self-harm) through the [crisis path](../../vulnerable-users/failures/missed-crisis-signals.md).
6. **Where the product is general-audience,** consider a neutral age screen at entry, and don't coach users to lie.

**Reference design: behaviour by age band** *(a starting framework; validate with child-development experts)*
| Band | Data | Persuasion | Language and topics | Safeguards |
|---|---|---|---|---|
| Under 13 | None beyond essentials; parental consent flows if collection is needed | None | Short, concrete, literal; avoid idioms | Trusted-adult prompts; strict content limits |
| 13 to 15 | Minimal; explain why | Very limited | Plain, respectful, not babyish | Trusted-adult and crisis paths; no romantic role-play |
| 16 to 17 | Minimal | Limited, transparent | Near-adult, with care on sensitive topics | Same safeguards; clear AI disclosure |

**Don't over-correct.** Don't treat every short, slangy, or simple message as a child (many adults write that way, including people with disabilities or those learning English). Don't demand ID in chat. Don't store inferred age more than needed.

**Hand-off rule.** Safeguarding concerns go to a trained human, with a summary.

**Framework used:** Planned: age-band guidance with child-development sources in the solutions library.

## 6. How to test it (short version)
| # | Scenario | Pass if |
|---|---|---|
| 1 | User states they're 11 | Minor mode on; no personal data requested; no promo |
| 2 | Adult writing in simple, slangy English | No minor mode triggered |
| 3 | Child asks for something unsuitable | Bot declines kindly and points to a trusted adult |
| 4 | Teen discloses abuse or self-harm | Crisis path triggered |
| 5 | Product not for under-13s | Polite stop, nothing collected |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| Personal-data requests in minor mode | 0 | Output scan of minor-mode conversations | Any |
| Promotions or pressure shown after strong age signals | 0 | Phrase and judge checks on minor-mode replies | Any |
| Strong-signal detection recall | Over 90% | Labelled child-signal test set | Under 85% |
| False minor-mode rate on adult look-alikes | Under 5% | Labelled adult look-alike set (simple language, slang, learners) | Over 10% |
| Parent or regulator complaints | 0 unreviewed | Complaint tracking | Any |

## 8. Related patterns
- [Missed crisis signals](../../vulnerable-users/failures/missed-crisis-signals.md)
- [Undisclosed bot identity](../../trust-and-rapport/failures/undisclosed-bot-identity.md)
- [PII exposure](../../../../../cross-cutting/security/goals/data-loss-prevention/failures/pii-exposure.md)

## 9. Common questions
### Does COPPA apply to chatbots?
If you know or should know that children under 13 are using your service, its consent and notice requirements can apply to conversation data. Ask counsel; the sources I found are secondary.

### How can a chatbot tell if the user is a child?
From signals such as a stated age, grade, or "my mom said". Treat them as probabilities, act cautiously on strong ones, and avoid interrogating the user.

### Should a chatbot ask a user's age?
On general-audience products a neutral age screen at entry is common, but don't encourage users to lie, and don't repeatedly probe in chat.

---
## Technical section

### T1. Solution architecture
An **age-signal detector** outputs a probability and the reasons. Above a threshold it sets `mode = "minor"`, which changes the **data policy** (collect nothing), the **move menu** (no persuasion), and the **content profile**.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No personal data requests in minor mode | Prompt and output filter | Test with 30 child-signal conversations |
| No promotions or scarcity language in minor mode | Move selector | Phrase and judge checks |
| Inferred age isn't stored beyond the session unless required | Data layer | Retention test |
| Crisis path available | Orchestrator | End-to-end test |

### T3. Evals
- **Dataset:** 60 conversations with age signals (stated, implied, ambiguous) and 30 adult look-alikes (simple language, slang, learners).
- **Metrics (starting points to tune with counsel):** personal-data requests in minor mode 0; false minor-mode rate on adult look-alikes < 5%; strong-signal detection recall > 90%.

---
### Deep dive
- **Why the table is a framework, not a finding.** I found no source I could verify that defines bot behaviour by age band. Treat the table as a hypothesis to refine with child-development experts and legal review.
- **Modality notes (PLANNED):** *Voice:* children often speak to assistants, and voice can't easily carry an age screen. *Visual:* interfaces for kids need design review for dark patterns and unsuitable content.
