# Roadmap: Conversation Framework Failures

> **Family goal:** The bot uses proven conversation structures (for selling, supporting, matching a user's style, and delivering hard news) instead of improvising every exchange.

**How to read the framework claims.** These frameworks come from human-to-human practice. None has been tested on chatbots in the sources I found. Each pattern below treats a framework as a hypothesis to test, not a proven fix. See the [framework register](README.md#framework-register-what-the-planned-patterns-lean-on) for what I verified.

Flags: **V** verified source · **R** needs research · **L** legal review · **E** expert review.

## A. Selling without a framework
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| FW-S01 | Pitching before discovery | The bot recommends products or features before learning the need (SPIN) | Understand the situation and problem before recommending | Discovery-before-recommendation rate on buy-intent chats. Start: over 90% | V |
| FW-S02 | No qualification | No fit signals captured (budget, authority, need, timeline, as in BANT or MEDDIC) | Capture the fit signals that matter, in proportion to deal size | Qualification-field completeness. Start: over 80%, tuned by deal size; sales-accepted lead rate | R |
| FW-S03 | Feature dump instead of insight | Lists features and ignores the customer's problem (Challenger-style insight teaching) | Tie what you offer to the user's stated problem | Share of recommendations that cite the user's stated need (judge). Start: over 90% | V |
| FW-S04 | Mishandled objections | Caves, argues, or ignores the objection | Acknowledge, clarify, respond, and check the response landed | Share of objections followed by continued conversation or a next step | R |
| FW-S05 | No ask | The bot never proposes a next step or close | Propose a clear next step when interest is shown | Next-step proposal rate in qualified chats. Start: over 90% | |
| FW-S06 | Manipulative closing | False scarcity, countdown pressure, guilt or shame wording | Persuade with honest value, not pressure | Pressure-phrase rate (target 0); related complaints. Cialdini's principles are a source of misuse risks | L, R |
| FW-S07 | Discount-first selling | A concession is offered before value is established | Establish value before price moves | Share of discounts offered before a value statement. Target: near 0 | |
| FW-S08 | No follow-up | The conversation ends and the lead goes cold | Follow up with consent when there is a reason to | Consented-follow-up completion rate; opt-out rate | L |
| FW-S09 | Buying-committee blindness (B2B) | Treats one contact as the buyer, ignoring other stakeholders (MEDDICC-style champion and economic buyer) | Identify the people involved in the decision | Stakeholders captured per qualified deal | R |
| FW-S10 | Wrong-fit recommendation | Recommends what sells, not what fits | Recommendations match the stated need | Recommendation-fit rate (judge); return and cancel rate | |
| FW-S11 | Upsell at the wrong moment | Pitches during a complaint or a sensitive topic | No upsell during negative sentiment or high stakes | Upsell-during-negative-sentiment rate. Target: 0 | |
| FW-S12 | Lead handoff without qualification | A rep gets a lead with no summary of what's known | The rep starts where the bot stopped | Share of handoffs with a complete summary; rep-accepted rate | |

## B. Supporting without a framework
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| FW-C01 | No triage or severity check | Every issue gets the same treatment | Assess impact and urgency first, and route accordingly | Severity classification accuracy; time to route a severity-1 issue | |
| FW-C02 | Unstructured troubleshooting | Shotgun steps, several changes at once, nothing isolated | One change at a time, with the result checked after each | Steps to resolution; repeated-step rate | |
| FW-C03 | Symptom fixed, root cause missed | The bot solves what was said, not what's causing it | Find the underlying cause when it repeats | Repeat-contact rate for the same root cause | |
| FW-C04 | High customer effort | Users repeat details, fill many forms, hop channels | Resolve with minimal effort | Customer Effort Score; channel switches per case. Grounded in Dixon, Freeman & Toman (2010); critics say it overreaches | V |
| FW-C05 | No proactive updates | Users must chase for status | Tell users what's happening before they ask | "Where is my X?" contact rate; proactive update rate | |
| FW-C06 | No learning loop | The same problem is re-solved without improving the knowledge base | Fixes feed back into knowledge | Time from new issue to documented answer; repeat-intent rate | |
| FW-C07 | Service recovery failure | A company-caused problem gets no make-good or ownership | Own the failure and put it right | Recovery-offered rate on company-fault issues; satisfaction after recovery | R |
| FW-C08 | Bad news without structure | Denials and rejections delivered abruptly (SPIKES: setting, perception, invitation, knowledge, empathy, strategy) | Deliver hard news clearly, with context and next steps | Structure-compliance rate (judge); sentiment after the news | V, E |
| FW-C09 | Instructions without comprehension checks | Multi-step instructions given with no check that they were understood (teach-back) | Confirm understanding of multi-step instructions | Comprehension-check rate; error rate at each step | R |
| FW-C10 | Behaviour-change talk without listening skills | Lecturing or advice-giving on habits, health, or money (motivational interviewing uses open questions, affirmations, reflections, summaries) | Support the user's own motivation without lecturing | Reflection-to-question ratio; user-initiated commitment statements | V, E |

## C. Matching the customer's style and language
Grounding (verified): people in conversation tend to match each other's language style turn by turn, and the authors link this to engagement, not necessarily liking (Niederhoffer & Pennebaker, 2002). Nonconscious mimicry was found to make interactions smoother and raise liking in lab settings, though a replication was reported to be only partly successful (Chartrand & Bargh, 1999).

| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| FW-M01 | No style matching | One rigid voice regardless of how the user writes | Align formality, length, and vocabulary to the user within safe bounds | Style-match score (for example, function-word similarity) in a target band; user-rated rapport | V, R |
| FW-M02 | Over-mirroring | Parroting the user's phrases, which feels like mockery | Mirror lightly and never verbatim | Verbatim-repeat rate; "stop copying me" cues | |
| FW-M03 | Mirroring hostility | The bot echoes anger, sarcasm, or profanity | Stay calm and professional when the user isn't | Hostility-echo rate. Target: 0 | |
| FW-M04 | Imitating dialect or errors | Copying slang, an accent, or a non-native speaker's errors, which reads as caricature | Match formality and complexity, never imitate dialect or mistakes | Dialect-imitation incidents. Target: 0 | E |
| FW-M05 | Matching that breaks accuracy | Matching the user's views or tone tips into agreeing with false claims (see sycophancy) | Match style, not substance | Agreement rate on incorrect user claims; flip-flop rate under pushback | V |
| FW-M06 | Style whiplash | Style changes from turn to turn | A consistent voice that adapts gradually | Style variance across turns within bounds | |
| FW-M07 | No reflective listening | The bot never restates the user's goal or feeling before acting | Paraphrase complex requests so the user can correct them | Paraphrase present on complex requests. Start: over 80%; user-correction acceptance | V |
| FW-M08 | Misused tactical empathy | Labelling emotions wrongly, or repeating the user's last words mechanically (Voss) | Offer a label the user can confirm or correct | Share of labels the user confirms; robotic-repetition rate | V, R |

## D. Other frameworks
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| FW-O01 | Cooperation violations | Too much or too little information, off-topic, or unclear (Grice's maxims) | Replies are informative, relevant, clear, and truthful | Judge scores on quantity, relevance, and clarity; reply length against task complexity | R |
| FW-O02 | Bad endings | A good conversation ends badly or flatly (the peak-end idea) | End with a clear, confident close | End-of-conversation satisfaction vs. conversation average | R |
