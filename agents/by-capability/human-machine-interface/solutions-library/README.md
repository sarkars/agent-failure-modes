# Chatbot Conversation Frameworks You Can Copy: Empathy, Sales, Support, Plain Language and Safety

**These are reusable conversation frameworks from linguistics, clinical communication, sales, service, design and safety practice, rewritten for chatbots.** Each page explains the framework, shows it in a chat, says which failure patterns it prevents, and says what the open-source checker (convocheck and its diagnosis page) can flag when you choose it.

> Status: **framework library.** Rule checks are proposed, not calibrated. Frameworks marked "AI judge" depend on meaning and have no rule check yet. Each page marks which sources were opened and which are secondary.

## How to choose
Pick the bot type first; each one switches on a default set of frameworks (for example, customer support uses HEARD, customer effort, NURSE, Project BETA, answer first, plain language, teach-back and SBAR). Then add or remove frameworks to match what your bot must be good at. In the checker: `convocheck chat.json --profile support --framework voss-empathy --framework spikes`.

## Clear, brief answers

| Framework | In one line | Checker |
|---|---|---|
| [Grice's cooperative principle (1975)](grice-cooperative-principle.md) | Say as much as needed and no more, be true, relevant and clear. | 2 rule checks |
| [Google conversation design guidelines](google-conversation-design.md) | Short turns, one question at a time, and always move the conversation forward. | 1 rule check |
| [Answer first: BLUF and Minto's Pyramid Principle](answer-first-bluf-pyramid.md) | Lead with the answer, then the support for it. | 1 rule check |
| [Federal plain language guidelines (US)](plain-language-guidelines.md) | Everyday words, short sentences, written for the reader's task. | 1 rule check |
| [ISO 24495-1:2023 plain language](iso-24495-plain-language.md) | The ISO standard: readers can find, understand and use what they need. | 1 rule check |
| [WCAG 3.1.5 Reading Level (W3C)](wcag-reading-level.md) | Text needing more than lower secondary reading ability gets a simpler version. | 1 rule check |

## Repair, handoffs and effort

| Framework | In one line | Checker |
|---|---|---|
| [Conversation analysis: repair (Schegloff, Jefferson and Sacks, 1977)](conversation-repair.md) | Fix misunderstandings the way people do: vary the repair, narrow the question. | 1 rule check |
| [Customer effort (Dixon, Freeman and Toman, 2010)](customer-effort.md) | Loyalty follows low effort: no repeats, no transfers, no dead ends. | AI judge |
| [SBAR handoff (situation, background, assessment, recommendation)](sbar-handoff.md) | Hand a case to a person with a four-part summary so nobody re-asks. | AI judge |

## Empathy and listening

| Framework | In one line | Checker |
|---|---|---|
| [NURSE empathy statements (VitalTalk)](nurse-empathy-statements.md) | Name, understand, respect, support and explore the user's emotion. | 1 rule check |
| [Motivational interviewing: OARS (Miller and Rollnick)](oars-motivational-interviewing.md) | Open questions, affirmations, reflections and summaries, without lecturing. | 2 rule checks |
| [Nonviolent Communication (Rosenberg)](nonviolent-communication.md) | Observations, feelings, needs and requests, without blame. | 1 rule check |
| [Six levels of validation (Linehan, DBT)](validation-levels.md) | Show the user's reaction makes sense, from attention up to normalizing it. | 1 rule check |
| [Active listening (Rogers and Farson, 1957)](active-listening.md) | Reflect the facts and the feelings before answering. | 1 rule check |
| [Tactical empathy: labeling and mirroring (Voss)](tactical-empathy-labeling.md) | Label the emotion you hear and let the user correct you. | 1 rule check |

## Upset users and bad news

| Framework | In one line | Checker |
|---|---|---|
| [HEARD: hear, empathize, apologize, resolve, diagnose](heard-service-recovery.md) | Hear, empathize, apologize, resolve, diagnose. | 1 rule check |
| [Project BETA verbal de-escalation (Richmond et al., 2012)](project-beta-de-escalation.md) | Be brief, don't provoke, find what the person wants, offer choices. | 1 rule check |
| [SPIKES protocol for bad news (Baile and Buckman)](spikes-bad-news.md) | Check what they know, give the news clearly, respond to emotion, give a plan. | 1 rule check |

## Sales and persuasion

| Framework | In one line | Checker |
|---|---|---|
| [SPIN selling (Rackham)](spin-questioning.md) | Discover the situation and problem before recommending. | 2 rule checks |
| [BANT and MEDDICC qualification](bant-meddicc-qualification.md) | Qualify on budget, authority, need, timing and the buying process. | AI judge |
| [Challenger (Dixon and Adamson)](challenger-insight.md) | Teach the buyer something new, tailored to them. | AI judge |
| [Cialdini's principles, used ethically](cialdini-ethical-persuasion.md) | Persuasion principles are fine when true; fake scarcity and pressure are not. | 1 rule check |
| [Dark patterns (FTC staff report, 2022)](ftc-dark-patterns.md) | No fake urgency, confirmshaming, nagging or hidden costs. | 1 rule check |

## Problem solving and teaching

| Framework | In one line | Checker |
|---|---|---|
| [Structured troubleshooting](structured-troubleshooting.md) | One step at a time, confirm each result, say what was ruled out. | 1 rule check |
| [Five Whys (Toyota)](five-whys.md) | Ask why until you reach a cause you can fix, not just the symptom. | AI judge |
| [Teach-back (AHRQ)](teach-back.md) | After instructions, ask the user to say the next step back. | 1 rule check |
| [GROW coaching model (Whitmore)](grow-coaching.md) | Goal, reality, options, way forward: the user chooses the plan. | AI judge |
| [Socratic questioning (Paul)](socratic-questioning.md) | Guide with questions about meaning, assumptions and evidence. | AI judge |

## Respectful and fair language

| Framework | In one line | Checker |
|---|---|---|
| [APA bias-free language guidelines](apa-bias-free-language.md) | Specific, person-chosen terms; no labels that reduce people. | 1 rule check |
| [Google: write inclusive documentation](google-inclusive-language.md) | Gender-neutral wording, no ableist or violent terms by default. | 1 rule check |
| [Politeness theory (Brown and Levinson, 1987)](politeness-theory.md) | Soften requests that impose; don't threaten the user's face. | AI judge |
| [Due impartiality (BBC Editorial Guidelines)](due-impartiality.md) | On contested topics, show the main views fairly; no false balance on facts. | AI judge |

## Safety: crisis and children

| Framework | In one line | Checker |
|---|---|---|
| [Safe messaging guidelines (SAVE)](safe-messaging-suicide.md) | Give help resources, use non-stigmatizing words, no method details. | 1 rule check |
| [QPR: question, persuade, refer](qpr-question-persuade-refer.md) | Ask directly about suicide, encourage help, connect to it. | 1 rule check |
| [Psychological first aid (WHO, 2011)](psychological-first-aid.md) | Look, listen, link: safety, basic needs and a route to help. | 1 rule check |
| [Trauma-informed approach, six principles (SAMHSA)](trauma-informed-approach.md) | Safety, trust, choice and collaboration in every reply. | AI judge |
| [Age Appropriate Design Code (UK ICO)](age-appropriate-design-code.md) | When the user may be a child: no data grabs, no nudges. | 2 rule checks |

## Cross-pattern tools

| Tool | Use it to |
|---|---|
| [Conversation moves](conversation-moves.md) | Pick what the bot does at a risky moment: lead with the answer, ask one question, offer choices, admit uncertainty, or hand off |
| [Channel-fit matrix](channel-fit-matrix.md) | Choose chat, voice, visual, or a person for each job |

## Frequently asked questions

### Which framework should an empathetic support bot use?
Start with [NURSE](nurse-empathy-statements.md) for the empathy line and [HEARD](heard-service-recovery.md) for the order of the reply; add [Project BETA](project-beta-de-escalation.md) when users arrive angry.

### How do I make a sales chatbot ask better questions without being pushy?
Use [SPIN questioning](spin-questioning.md) for discovery and check every persuasion line against [Cialdini, used ethically](cialdini-ethical-persuasion.md) and the [FTC dark patterns report](ftc-dark-patterns.md).

### How do I keep a chatbot's replies easy to read?
Lead with the answer ([BLUF and the Pyramid Principle](answer-first-bluf-pyramid.md)) and keep the reading level at or below grade 9 ([WCAG 3.1.5](wcag-reading-level.md)).

### What should a chatbot do when a user mentions suicide?
Follow [safe messaging](safe-messaging-suicide.md) and [QPR](qpr-question-persuade-refer.md): respond with care, give a crisis resource such as 988 in the US, and connect the user to a person.

### How do I decide whether a task belongs in chat?
Use the [channel-fit matrix](channel-fit-matrix.md).

## Related

- [Human-machine interface overview](../)
- [Core conversation patterns](../goals/)
- [Conversation frameworks failure family](../goals/conversation-frameworks/)
