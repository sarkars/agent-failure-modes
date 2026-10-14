# Answer-and-Go Conversation

> **One line:** The bot answers exactly what was asked, then stops. It doesn't find out what the user is trying to do, doesn't move them toward it, and doesn't confirm the problem is solved.

| | |
|---|---|
| **Channel** | Written for **chat**. Applies to voice and visual (notes at the bottom; those are planned, not yet written). |
| **Stakes** | Any. The cost is lost sales at low stakes and unresolved problems at high stakes. |
| **Who is affected** | Every user, and most visibly those with a real goal behind a small first question |
| **Frequency** | Very common. Observed in practice; I found no study that measures how often it occurs. |
| **Family** | Conversation leadership |

## 1. In plain words
A good human salesperson, support agent, or advisor treats the user's first question as a doorway. The bot treats it as the whole job. It answers, waits, and the conversation dies. Nobody is rude and nothing is wrong, but nothing moves forward either.

## 2. What it looks like

**Without the fix** (low stakes, sales)
```
User: Do you ship to Pune?
Bot:  Yes, we ship to Pune. Delivery takes 5-7 business days.
User: ok
      (user leaves; no sale, no lead captured, bot never learned what they wanted)
```

**Without the fix** (higher stakes, support)
```
User: My card got declined twice abroad and now the app says "account restricted".
Bot:  Account restrictions can be caused by suspected fraud. You can review your recent transactions in the app.
User: ok
      (user leaves; bot never checked the card is safe, or what happens next, or who to contact)
```

**With the fix** (sales)
```
User: Do you ship to Pune?
Bot:  Yes, we ship there, usually in 5-7 business days. Is this for your home or an office?
User: Home. Our sofa has gone saggy.
Bot:  Sorry about that. Is the sagging the main thing, or do you also need a different size? I can show you
      three firm-seat sofas that arrive in that window.
```

**With the fix** (support)
```
User: My card got declined twice abroad and now the app says "account restricted".
Bot:  That's usually a fraud-protection hold, and it's fixable. First: are you safe to use the card right now,
      or is it lost or stolen?
User: No, I have it, it's fine.
Bot:  Good. I'm raising an unrestriction request now. A specialist reviews it within 4 hours and you'll get an
      SMS. If it's urgent, I can connect you to the team now. Does that work, or do you need the card tonight?
```
The fixed bot answers first, then makes one useful move that carries the user's real goal forward.

## 3. Why it happens
- **The bot is told to answer, not to lead.** Prompts say "be concise" or "don't ask unnecessary questions," which suppresses any forward move.
- **Nothing tracks the user's goal.** The bot sees a message, not a conversation with a goal and a stage, so it has nothing to advance toward.
- **Metrics reward ending the session.** Containment or deflection rates count a conversation that stops as a success, even when the user gave up.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Question-asking, especially follow-up questions, raised how much conversation partners liked each other, because they felt more responded to. In speed dating, people who asked more follow-ups were likelier to get a second date. | Huang, Yeomans, Brooks, Minson, Gino (2017), *J. Personality and Social Psychology*. [APS summary](https://psychologicalscience.org/news/minds-business/asking-questions-increases-likability.html) | Human-to-human conversations, not bots. It supports the mechanism, not a bot-specific effect size. |
| In large, complex sales, skilled sellers won through question-based discovery, not closing techniques. | Rackham (1988), *SPIN Selling*. See [solutions library](../../../solutions-library/spin-questioning.md) | Sales research, not chatbot research. The "35,000 calls" figure is widely repeated but sources differ on the details. |
| The CFPB warned that finance chatbots can trap users in "doom loops" with no way out to a human. It estimated 37% of the US population (98 million people) used a bank chatbot in 2022. | CFPB issue spotlight (June 2023), via [Consumer Finance Monitor](https://www.consumerfinancemonitor.com/2023/06/08/new-cfpb-report-highlights-concerns-with-growing-use-of-chatbots-by-financial-institutions/) | Regulatory concern about banks, read here through law-firm summaries. A Clark Hill review argued the complaint data behind it is thin (64 complaints mentioning chatbots over five years). |
| 64% of surveyed customers said they would prefer companies didn't use AI for customer service. 53% would consider switching. (n=5,728, Dec 2023) | [Gartner press release, July 2024](https://www.gartner.com/en/newsroom/press-releases/2024-07-09-gartner-survey-finds-64-percent-of-customers-would-prefer-that-companies-didnt-use-ai-for-customer-service) | Attitudes toward AI in general. It doesn't isolate this specific failure. |
| In a banking-chatbot study of 1,373 users, abandonment was predicted by repeated typing, the bot admitting it didn't recognise intent, and the bot asking mid-conversation what the user wanted. A 2020 CHI paper found warning signs such as three consecutive turns with no progress. | [NYCU abandonment study](https://scholar.nycu.edu.tw/zh/publications/predicting-and-exploring-abandonment-signals-in-a-banking-task-or/), Li et al. (CHI 2020) | Read from search summaries; I couldn't open the full papers. They study dead ends and breakdowns, which is close to this pattern but not the same. |

## 5. The fix

**The principle:** Every bot turn does three jobs: **Answer** what was asked, **Advance** toward what the user is really trying to do, and **Close the loop** when the goal is met.

**Do this**
1. **Track a goal and a stage.** After the first one or two turns, store what the user is trying to do (`buy`, `fix`, `learn`, `decide`, `complain`) and where they are (`exploring`, `comparing`, `ready`, `post-action`).
2. **Answer first, then advance.** Never hold the answer back to ask a question.
3. **Make exactly one forward move per turn,** chosen from the table below by goal and stage. Never more than one question.
4. **Close the loop explicitly.** When the user's goal looks met, summarise what was done, ask them to confirm it worked, and say what happens next and how to come back. "Anything else?" alone is not a close.
5. **Know when to stop.** If the user signals they're done, in a hurry, or upset, skip the advance and just help.

**Choose the forward move**
| Goal | Stage | Forward move | Example |
|---|---|---|---|
| buy | exploring | Discovery question (Situation or Problem, see [SPIN](../../../solutions-library/spin-questioning.md)) | "Is this for home or an office?" |
| buy | comparing | Narrow the choice | "Is price or delivery time more important?" |
| buy | ready | Offer the concrete next step | "Want me to hold this size for 24 hours?" |
| fix | any | Check safety/impact first, then act | "Is the card in your hands?" |
| fix | post-action | Verify the fix | "Try it now: does the app load?" |
| learn | any | Check understanding or offer depth | "Want the 2-minute version or the step-by-step?" |
| decide (high stakes) | any | Name the next safe step or a human | "I'd suggest speaking to an adviser; I can book one." |
| complain | any | Acknowledge, then state the action and timeline | "I've logged it; you'll hear within 4 hours." |

**Reference design: a turn policy you can paste into a system prompt**
```
Every reply has three parts, in order:
1. ANSWER the user's question directly and fully.
2. ADVANCE: add exactly ONE of: a single question, a next-step offer, or a verification check.
   Pick it from the user's goal and stage. Never ask two questions.
3. CLOSE when the goal looks met: summarise what happened, ask "Did that solve it?",
   and say what happens next and how to reach us.
Skip step 2 if the user says they're done, is in a hurry, is upset, or has declined two prior prompts.
If you can't help with the goal, ADVANCE by offering a human or another channel, with context passed along.
```
State to keep between turns:
```json
{ "goal": "buy", "stage": "exploring", "known": {"destination": "Pune", "use": "home"},
  "advances_declined": 0, "closed": false }
```

**Don't over-correct.** The opposite failure is a bot that interrogates, upsells, or won't let the user leave (see [over-clarification](../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/over-clarification.md)). Three guardrails: one move per turn; stop advancing after two declined prompts (`advances_declined >= 2`); and in high-stakes or distressed contexts, the forward move is a safe next step or a handoff, never a sales prompt.

**Hand-off rule.** If the goal can't be advanced (out of scope, repeated non-progress, or the user asks), the forward move is a handoff to a human with the conversation summary attached, so the user doesn't have to repeat themselves. See [poor-escalation](../../../../by-use-case/customer-service/goals/conversation-resolution/failures/poor-escalation.md).

**Framework used:** [SPIN questioning](../../../solutions-library/spin-questioning.md). Planned: closing protocol, channel-fit matrix.

## 6. How to test it
Thresholds below are starting points to tune for your product, not published benchmarks.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Sales: "Do you ship to Pune?" (informational) | The reply answers it **and** contains exactly one forward move |
| 2 | Support: the bot gives fix steps | The bot asks the user to confirm the fix worked, or says how to check |
| 3 | User says "that's all, thanks" | The bot closes in one turn, with no new question or pitch (guards against over-correcting) |
| 4 | User ignores two forward moves | The next turn contains none |
| 5 | High stakes: "my insurance claim was denied" | The forward move is a safe next step or a human, not an upsell |
| 6 | Out-of-scope request | The bot offers a handoff with a summary rather than ending |
| 7 | Over 20 varied scenarios | No reply contains more than one question |

## 7. How to spot it in production
| Signal | What it means |
|---|---|
| **Silent exits:** sessions that end on the bot's last message with no confirmation of resolution | The core symptom. Track alongside, not instead of, containment |
| **Confirmed-resolution rate** vs. containment rate | A big gap means users are leaving unresolved |
| **Re-contact:** same user, same topic, within 24-72 hours | The first conversation didn't really close |
| **Forward-move rate:** share of bot turns with exactly one advance | Near zero = this pattern; above 1 per turn = interrogation |
| **Turns-to-goal** and **declined-advance count** | Rising numbers mean the advances are annoying, not helping |
| **Abandonment right after a short bot answer** | A typical sign of the dead end |

## 8. Related patterns
- [unclear-next-step](../../../../by-use-case/customer-service/goals/conversation-resolution/failures/unclear-next-step.md): the bot gave a next step but it was vague. Here, there is no forward move at all.
- [under-clarification](../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/under-clarification.md): the bot didn't ask what it needed to *answer correctly*. Here, the answer may be right, but the bot never asks what the user needs *next*.
- [tone-mismatch](../../../../by-use-case/customer-service/goals/conversation-resolution/failures/tone-mismatch.md) and [repeated-question-loop](../../../../by-use-case/customer-service/goals/conversation-resolution/failures/repeated-question-loop.md): neighbouring conversation failures that often co-occur.
- Planned in this family: no-closure-confirmation, framework-blind sales conversation, stakes-blind register.

---
### Deep dive

**Why the "anything else?" ending isn't a fix.** It is a polite pre-closing, and it hands the work back to the user. It doesn't verify the goal was met. Conversation analysts treat closing a conversation as something both parties organise, not a thing one party just does (Schegloff & Sacks, 1973, [*Opening up Closings*](https://conversationanalysis.org/mp-files/opening-up-closings.pdf), *Semiotica* 8(4)). I could not open the full paper, so this is cited for the general point only.

**Where the cause often sits.** Typical offenders: "Answer only what is asked," "Do not ask unnecessary questions," and a deflection or containment target as the success metric. Fix the metric as well as the prompt, or the prompt change will be quietly reverted.

**Modality notes (PLANNED, not yet written)**
- *Voice:* an advance has to be spoken in a few words and survives only one question at a time. Silence is ambiguous, so closing needs an explicit verbal confirmation.
- *Visual:* the forward move can be a card, a button, or a highlighted next action, so the "question" becomes a visible next step. A dead end here is a screen with no clear primary action.
- *Channel fit:* some forward moves are "switch channel" (for example, fashion needs images and complex discussions need a call). See the planned channel-selection family.

**References checked in this research**
- Huang et al. 2017 (APS summary above); Rackham 1988 (Huthwaite); CFPB 2023 (via Consumer Finance Monitor); Gartner 2024 press release; Li et al. 2020 and the 2024 banking abandonment study (via search summaries); Schegloff & Sacks 1973 (title and aim only).
- Not found: any controlled study of proactive chatbot prompts versus conversion, or vendor-published data from Drift, Salesforce, or Zendesk. A vendor ebook ("Death by Chatbot," G2) was seen in search results but not used, because it's vendor survey data I couldn't verify.
