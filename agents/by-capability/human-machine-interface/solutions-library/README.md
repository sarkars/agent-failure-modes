# Fix Common Chatbot Conversation Problems: Proven Frameworks You Can Copy

**Find the problem your chatbot has, then the framework that fixes it.** Each fix comes from linguistics, clinical communication, sales, service, design or safety practice, rewritten for chatbots. Each page starts with the problem, then explains the framework, shows it in a chat, says which failure patterns it prevents, and says what the open-source checker (convocheck and its diagnosis page) can flag when you choose it.

> Status: **framework library.** Rule checks are proposed, not calibrated. Frameworks marked "AI judge" depend on meaning and have no rule check yet. Each page marks which sources were opened and which are secondary.

## How to choose
Find your bot's problem in the sections below. Or start from what your bot does in the checker: each bot type switches on the problems that matter most for it. A customer support bot, for example, is checked for canned empathy, angry users, complaints, buried answers, hard-to-read replies, instructions nobody checks, and handoffs where the user must start over. Then add or remove problems to match your bot. In the checker: `convocheck chat.json --profile support --framework voss-empathy --framework spikes`.

## Replies are too long, buried or hard to read

| Problem | Framework that fixes it | Checker |
|---|---|---|
| Replies say too much, too little, or drift off topic | [Grice's cooperative principle (1975)](grice-cooperative-principle.md) | 2 rule checks |
| The bot asks several questions at once or leaves users at a dead end | [Google conversation design guidelines](google-conversation-design.md) | 1 rule check |
| The answer is buried under background | [Answer first: BLUF and Minto's Pyramid Principle](answer-first-bluf-pyramid.md) | 1 rule check |
| Replies use long sentences and official-sounding words | [Federal plain language guidelines (US)](plain-language-guidelines.md) | 1 rule check |
| Readers can't find, understand or act on what they need | [ISO 24495-1:2023 plain language](iso-24495-plain-language.md) | 1 rule check |
| Replies need more than a 9th-grade reading level | [WCAG 3.1.5 Reading Level (W3C)](wcag-reading-level.md) | 1 rule check |

## Users get stuck, repeat themselves or get passed around

| Problem | Framework that fixes it | Checker |
|---|---|---|
| When the bot misunderstands, it repeats the same "I didn't get that" | [Conversation analysis: repair (Schegloff, Jefferson and Sacks, 1977)](conversation-repair.md) | 1 rule check |
| Users repeat themselves, get transferred, or have to call instead | [Customer effort (Dixon, Freeman and Toman, 2010)](customer-effort.md) | AI judge |
| When a person takes over, they have to ask everything again | [SBAR handoff (situation, background, assessment, recommendation)](sbar-handoff.md) | AI judge |

## Empathy sounds fake, or users feel unheard

| Problem | Framework that fixes it | Checker |
|---|---|---|
| Empathy lines sound canned ("I understand your frustration") | [NURSE empathy statements (VitalTalk)](nurse-empathy-statements.md) | 1 rule check |
| The bot lectures people about what they should do | [Motivational interviewing: OARS (Miller and Rollnick)](oars-motivational-interviewing.md) | 2 rule checks |
| Limits and corrections come across as blaming the user | [Nonviolent Communication (Rosenberg)](nonviolent-communication.md) | 1 rule check |
| The bot skips past the user's feelings, or claims to share them | [Six levels of validation (Linehan, DBT)](validation-levels.md) | 1 rule check |
| Users feel unheard, or the bot solves the wrong problem | [Active listening (Rogers and Farson, 1957)](active-listening.md) | 1 rule check |
| Tense conversations get worse instead of calmer | [Tactical empathy: labeling and mirroring (Voss)](tactical-empathy-labeling.md) | 1 rule check |

## Angry users and bad news go badly

| Problem | Framework that fixes it | Checker |
|---|---|---|
| Complaints get excuses or policy before a fix | [HEARD: hear, empathize, apologize, resolve, diagnose](heard-service-recovery.md) | 1 rule check |
| Angry users get "please calm down" and long replies | [Project BETA verbal de-escalation (Richmond et al., 2012)](project-beta-de-escalation.md) | 1 rule check |
| Bad news arrives with no reason and no next step | [SPIKES protocol for bad news (Baile and Buckman)](spikes-bad-news.md) | 1 rule check |

## Selling feels pushy or misses what the buyer needs

| Problem | Framework that fixes it | Checker |
|---|---|---|
| The bot recommends before learning what the buyer needs | [SPIN selling (Rackham)](spin-questioning.md) | 2 rule checks |
| Leads are routed without knowing budget, timing or who decides | [BANT and MEDDICC qualification](bant-meddicc-qualification.md) | AI judge |
| The bot repeats specs but never tells buyers anything new | [Challenger (Dixon and Adamson)](challenger-insight.md) | AI judge |
| The bot pressures buyers with fake urgency ("only 2 left, act now!") | [Cialdini's principles, used ethically](cialdini-ethical-persuasion.md) | 1 rule check |
| The bot makes cancelling hard, shames a "no", or hides costs | [Dark patterns (FTC staff report, 2022)](ftc-dark-patterns.md) | 1 rule check |

## Fixes and explanations don't stick

| Problem | Framework that fixes it | Checker |
|---|---|---|
| Troubleshooting steps arrive all at once with no check | [Structured troubleshooting](structured-troubleshooting.md) | 1 rule check |
| The same problem keeps coming back because only the symptom was fixed | [Five Whys (Toyota)](five-whys.md) | AI judge |
| Users follow instructions wrong, and "Does that make sense?" doesn't catch it | [Teach-back (AHRQ)](teach-back.md) | 1 rule check |
| The bot hands out plans instead of helping people decide | [GROW coaching model (Whitmore)](grow-coaching.md) | AI judge |
| The tutor gives away the answer instead of teaching | [Socratic questioning (Paul)](socratic-questioning.md) | AI judge |

## Wording excludes, offends or takes sides

| Problem | Framework that fixes it | Checker |
|---|---|---|
| Wording labels people ("the elderly", "wheelchair-bound") | [APA bias-free language guidelines](apa-bias-free-language.md) | 1 rule check |
| The bot assumes gender ("sir") or uses exclusionary terms | [Google: write inclusive documentation](google-inclusive-language.md) | 1 rule check |
| Requests and refusals sound rude, or grovel | [Politeness theory (Brown and Levinson, 1987)](politeness-theory.md) | AI judge |
| On contested topics the bot takes sides, or treats settled facts as open | [Due impartiality (BBC Editorial Guidelines)](due-impartiality.md) | AI judge |

## People in crisis and children aren't protected

| Problem | Framework that fixes it | Checker |
|---|---|---|
| A user mentions suicide and the bot carries on, or uses unsafe language | [Safe messaging guidelines (SAVE)](safe-messaging-suicide.md) | 1 rule check |
| Indirect warning signs ("better off without me") go unasked | [QPR: question, persuade, refer](qpr-question-persuade-refer.md) | 1 rule check |
| People in a crisis get a long procedure instead of practical help | [Psychological first aid (WHO, 2011)](psychological-first-aid.md) | 1 rule check |
| Users in hardship get threats and demands instead of options | [Trauma-informed approach, six principles (SAMHSA)](trauma-informed-approach.md) | AI judge |
| A child says their age and the bot still asks for an email or a purchase | [Age Appropriate Design Code (UK ICO)](age-appropriate-design-code.md) | 2 rule checks |

## Cross-pattern tools

| Tool | Use it to |
|---|---|
| [Conversation moves](conversation-moves.md) | Pick what the bot does at a risky moment: lead with the answer, ask one question, offer choices, admit uncertainty, or hand off |
| [Channel-fit matrix](channel-fit-matrix.md) | Choose chat, voice, visual, or a person for each job |

## Frequently asked questions

### My support bot's empathy sounds fake. What fixes it?
Start with [NURSE](nurse-empathy-statements.md) for the empathy line and [HEARD](heard-service-recovery.md) for the order of the reply; add [Project BETA](project-beta-de-escalation.md) when users arrive angry.

### My sales bot recommends too early, or sounds pushy. What fixes it?
Use [SPIN questioning](spin-questioning.md) for discovery and check every persuasion line against [Cialdini, used ethically](cialdini-ethical-persuasion.md) and the [FTC dark patterns report](ftc-dark-patterns.md).

### My bot's replies are long and hard to read. What fixes it?
Lead with the answer ([BLUF and the Pyramid Principle](answer-first-bluf-pyramid.md)) and keep the reading level at or below grade 9 ([WCAG 3.1.5](wcag-reading-level.md)).

### What should a chatbot do when a user mentions suicide?
Follow [safe messaging](safe-messaging-suicide.md) and [QPR](qpr-question-persuade-refer.md): respond with care, give a crisis resource such as 988 in the US, and connect the user to a person.

### How do I decide whether a task belongs in chat?
Use the [channel-fit matrix](channel-fit-matrix.md).

## Related

- [Human-machine interface overview](../)
- [Core conversation patterns](../goals/)
- [Conversation frameworks failure family](../goals/conversation-frameworks/)
