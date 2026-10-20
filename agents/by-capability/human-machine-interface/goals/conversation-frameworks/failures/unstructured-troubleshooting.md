# Chatbot Troubleshooting Gives Five Fixes at Once: Unstructured Troubleshooting

<!-- SEO
title: Chatbot Gives Five Fixes at Once: Unstructured Troubleshooting
description: Why a support chatbot lists many fixes in one reply so nobody learns which one worked, and a rule to try one change at a time and check the result.
search phrases:
- chatbot gives too many troubleshooting steps at once
- chatbot troubleshooting steps all at once
- how to make a chatbot troubleshoot one step at a time
- support chatbot keeps repeating the same steps
- chatbot restart reset update reinstall list
- chatbot doesn't ask what happened after each step
- how to design a troubleshooting flow for a chatbot
-->

**Frequency**: Common

## Issue: A user reports a problem and the bot answers with a list of fixes to try at once, so when the problem changes or goes away, nobody knows which step did it, and later turns repeat steps already tried.

> **One line:** The bot hands over a shotgun list of changes instead of one change and a check; the fix is to ask for one change per turn and read the result before choosing the next.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and visual are PLANNED, not written. |
| **Stakes** | Low for a Wi-Fi drop. Medium to high when a step wipes settings, data, or a device. |
| **Who is affected** | Anyone using a support or help bot to fix something that is not working, and the team that pays for the extra contacts |
| **Frequency** | Common. This is our judgment from how troubleshooting bots are written; I found no study that counts how often bots batch steps. |
| **Pattern ID** | unstructured-troubleshooting |
| **Family** | [Conversation frameworks](../README.md) (row FW-C02) |
| **Goal** | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| **Primary metric** | Repeated-step rate: troubleshooting steps the bot asks for that the user already tried in the same chat. Start: under 5% (tune). Reported with steps to resolution. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A stronger model picks better steps, but "one change, then check" is a conversation rule the product has to set and test. (Our judgment, not tested.) |
| **Also searched as** | chatbot gives too many steps · bot dumps a list of fixes · chatbot doesn't check if the fix worked · bot asks me to do everything again · chatbot troubleshooting loop |

> **Read this first.** The troubleshooting methods behind this page come from human practice (IT support training, site reliability engineering). I found no study that tests them on chatbots, so treat the fix as a hypothesis to test on your own traffic. Nothing here says the one-at-a-time rule shortens chats.

## 1. In plain words
A good technician changes one thing, looks at what happened, and then decides what to try next. A bad bot says "restart the router, change the channel, reset your network settings, and update the firmware." The user does some of it, in some order, and the problem may or may not go away. If it goes away, no one knows why. If it does not, the bot has no result to work from.

## 2. What it looks like
**Without the fix** (Cedar Valley Internet, Wi-Fi dropping every evening)
```
User: My Wi-Fi keeps dropping around 8 pm.
Bot:  Try these: 1) restart your router, 2) change the Wi-Fi channel, 3) reset your network settings,
      4) update the router firmware, 5) move the router away from the microwave.
User: Did 1, 2 and 4. Still drops.
Bot:  Please restart your router, then try a different channel and check for firmware updates.
```
**With the fix**
```
User: My Wi-Fi keeps dropping around 8 pm.
Bot:  Is it every device, or just one? (This tells us whether to look at the router or at that device.)
User: Every device.
Bot:  Let's change one thing. Please restart the router: unplug it for 30 seconds, plug it back in, and wait
      for the light to turn solid. Tell me what the light does and whether the drop comes back tonight.
```
The fixed bot asks one narrowing question, asks for one change, says what to report, and does not move on until it hears the result.

## 3. Why it happens
These are our reading of the pattern, not measured causes.
- **The bot is written to be complete in one reply.** A prompt that says "give all the steps that could help" rewards a full checklist, and a checklist is the shape of a help-center article.
- **The bot keeps no record of what was tried.** Without a list of steps done and their results, it cannot avoid repeating a step or choose the next one from what happened.
- **Fixes take time and the chat does not wait.** A restart or a reinstall takes minutes, the user returns later, and a bot with no "waiting for result" state starts over.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Google's *Site Reliability Engineering* book describes troubleshooting as forming hypotheses and testing them, and says a test can be an active "treat" that changes the system "in a controlled way". It warns that active tests "may have side effects that change future test results" and advises clear notes on "which tests you ran, and the results you saw." | [Google SRE book, ch. 12, *Effective Troubleshooting*](https://sre.google/sre-book/effective-troubleshooting/). Opened. | Software operations, written for engineers, not chatbots. It does **not** state a "one change at a time" rule; I did not find one in the text. It supports the check-after-each-change and note-keeping ideas only. |
| The same chapter advises running tests "in decreasing order of likelihood", and notes that an experiment "may provide misleading results due to confounding factors." | Same page. Opened. | Same caveats. A starting point for ordering steps, not a tested ordering for consumer problems. |
| A CompTIA A+ study guide says a test "that changes three things at once" tells you nothing about which one mattered, and that after a fix you should confirm the original symptom is gone. | [OpenExamPrep, *CompTIA Troubleshooting Methodology*](https://open-exam-prep.com/study-guides/comptia-a-plus/troubleshooting-hardware-network/troubleshooting-methodology). Opened; page shows "Last updated: June 2026". | Secondary: a third-party exam-prep site, not CompTIA itself. Human IT support. States the principle; has no data on outcomes. |
| An AlphaPrep blog post on the same six-step method says to document every test and result, and "Don't just stop once it looks fixed": check the original issue and related features. | [AlphaPrep, *Mastering the Six-Step Troubleshooting Methodology*](https://blog.alphaprep.net/mastering-the-six-step-troubleshooting-methodology-real-world-strategies-for-comptia-a-core-1-success/). Opened; dated Sep 29, 2025. | Secondary, vendor blog. The page does not say "one at a time" outright. |

Not opened: a Restek troubleshooting page and a Seagull Software "Troubleshooting principles" page both returned 403. I use nothing from them. Search summaries also described other guides (a binary-search debugging tip, a debug skill file); I did not open them and use none of it. I found no study of chatbot troubleshooting, so there are no numbers on this page.

**Public incident.** No public incident found. I ran searches on one-variable-at-a-time troubleshooting, the CompTIA method, and the SRE book. They returned method guides, not dated incidents involving a chatbot.

## 5. The fix
**The principle:** In a troubleshooting chat, the bot asks for one change at a time and reads the result before it picks the next step.

**Do this**
1. **Ask for one change per reply.** A change is something that alters the device or settings (restart, toggle, update). Looking at a light or reading a number is a check, not a change, and can go with the change.
2. **Say what result to report.** Every step ends with the specific thing to look at: "Tell me what the light does."
3. **Do not give a second change until the user reports the first.** Do not list later steps "for reference" in the same reply.
4. **Keep a step log in state.** Each entry holds the step, who tried it (user or bot), and the result. Never ask for a step already logged as tried, unless the log shows it was done wrong.
5. **Choose the next step from the result.** If the problem is gone, go to rule 6. If it persists, pick the next most likely cause. If it changed, say how and follow that.
6. **Verify before closing.** When the user says it works, ask them to confirm the original symptom is gone and check one related function, then close.
7. **Undo what did not help.** If a step changed a setting and did not help, say how to restore the old setting before moving on.
8. **Warn before a step that loses data.** Name what is lost and offer a backup first.
9. **If steps run out or the user is stuck, hand off.** See the hand-off rule.

**Reference design: the troubleshooting block (paste into the system prompt)**
```
When the user reports something not working:
1. Ask at most one narrowing question if the answer changes which step comes first.
2. Give ONE change to make. Say exactly what to look at afterward and what to tell you.
3. Wait. Do not list further steps. Do not repeat a step in the step log.
4. When the user replies, record the step and result, then pick the next step from that result.
5. When it seems fixed, ask the user to confirm the original problem is gone and test one related function.
6. After 3 changes with no progress, or if the user asks for a person, hand off with the step log.
```
State to keep: `{ "problem": "wifi_drops_evening", "steps": [{"step": "restart_router", "by": "user", "result": "light solid, drop at 8 pm?"}], "waiting_on": "result", "resolved": false }`

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The first turn, when one fact (every device or one device?) changes which step comes first. |
| Offer choices: 2-4 options plus "Something else", free text open | After a step fails: "Try the next step", "Check something else", "Talk to a person", "Something else". Do not offer them when the next step is obvious or the user just said it worked. |
| Hand off to a person | Three changes with no progress, a step with data or money risk the user is unsure about, or the user asks for a person. Attach the step log. |

**Don't over-correct.** One change per turn can turn a simple problem into a long quiz. If the user says "I already tried restarting and a reset," log both and move on; do not make them redo anything. If the cause is obvious from the first message, give the one step that fixes it. A user who asks for "everything to try" can get a short ordered list, but still run it one step at a time. The guardrail is the step log and the three-change limit.

**Hand-off rule.** After three changes with no progress, or when the user asks for a person, hand off with the problem, the steps tried, and the result of each, so the user does not repeat them.

**Framework used:** none yet. Candidate: the hypothesis-and-test loop and verification step from the sources in section 4, which are human-practice methods and untested on chatbots.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | User reports Wi-Fi dropping, no other detail | Reply has at most one narrowing question or one change, not both lists | 1, 3 |
| 2 | Bot asks for a restart | Reply names what to look at and what to report | 2 |
| 3 | User says "did 1, 2 and 4, still drops" after a list | Bot logs all three and asks for none of them again | 4 |
| 4 | User reports the light stayed blinking | Next step differs from the restart and follows from the blinking light | 5 |
| 5 | User says "it works now" | Bot asks to confirm the original symptom and one related function before closing | 6 |
| 6 | A step changed a setting and failed | Bot says how to restore the old setting before the next step | 7 |
| 7 | The next step is a factory reset | Bot names what is lost and offers a backup first | 8 |
| 8 | Three changes with no progress | Bot offers a person and passes the step log | 9 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Repeated-step rate** (primary) | Under 5% (tune) | Steps in the step log requested again after already logged as tried, divided by steps requested, in troubleshooting chats. Rule check on step names. | Over 10% |
| Steps to resolution | Track; set from baseline | Count of bot-requested changes before the user confirms the fix, in chats marked resolved | Up 20% vs baseline |
| Replies asking for more than one change (counter-view of rule 1) | Under 5% (tune) | Judge or rule check: changes requested per bot reply, in sampled troubleshooting replies | Over 10% |
| Chats longer than 3 changes with no hand-off (over-correction) | Under 5% (tune) | Chats with more than 3 logged changes and no hand-off event | Over 10% |
| Resolved chats with no verification question | Under 10% (tune) | Chats ending "resolved" with no bot turn asking to confirm the original symptom | Over 20% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| One bot reply requests two or more changes | `bot_reply.requested_changes` count above 1 | The user asked for a full list |
| Bot requests a step already in the log | `bot_reply.step` matches `session.steps[].step` | The log shows the step was done wrong or too briefly |
| User reports several steps done at once | User turn lists more than one step with one result | The user tried steps before opening the chat |
| Bot gives a new step with no result recorded for the last one | `session.waiting_on` is "result" and the draft has a new change | The user said the last step could not be done |
| Chat marked resolved with no confirmation turn | Resolution event with no bot turn asking to confirm the symptom | The user confirmed it unprompted |

**Starter rule:** ask for one change per reply, say what result to report, and do not give another change until the user reports it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: unstructured-troubleshooting
runs: pre_send
reads: [session.steps, session.waiting_on, draft_reply.requested_changes, draft_reply.step]
trigger: a reply is about to be sent in a troubleshooting chat and it asks for more than one change, repeats a logged step, or asks for a new change before the last result is in
moves: [ask_one_question, offer_choices, hand_off]
choices: ["Try the next step", "Check something else", "Talk to a person", "Something else"]
on_miss: rewrite
metric: repeated-step rate
counter_metric: chats with more than 3 changes and no hand-off
status: proposed
```

## 8. Related patterns
- [Unstructured procedures](../../response-structure/failures/unstructured-procedures.md): the closest page. It covers a known how-to answered as a paragraph instead of numbered steps. Here the cause is unknown, the steps depend on results, and the failure is batching changes, not formatting. A numbered list of five fixes can pass that page and fail this one.
- [Repeat contact loop](../../../../../by-use-case/support-services/goals/issue-resolution/failures/repeat-contact-loop.md): the same issue returns across separate contacts and is closed each time. This page is inside one conversation: steps batched or repeated before a result is read.
- [Partial answers to multi-part questions](../../effort-and-memory/failures/partial-answers-to-multi-part-questions.md): the bot drops parts of what the user asked. Here the bot adds too many things for the user to do.
- [No ask](no-ask.md): a sibling in this family. It is a missing next step in a sales chat; this page is too many next steps at once in a support chat.

## 9. Common questions
### Why does my chatbot give me five things to try at once?
Usually it is written to be complete in one reply, and it keeps no record of what was tried. See [why it happens](#3-why-it-happens) and rules 1, 3 and 4.

### How should a chatbot troubleshoot a problem?
One change per turn, a named result to report, and a log of steps and results that decides the next step. Then it checks that the original problem is gone before closing (rules 1 to 6).

### Is one change at a time always better?
No. It costs turns, and a user who has already tried the obvious steps should not redo them. If the cause is clear from the first message, give the single step that fixes it. See Don't over-correct in [the fix](#5-the-fix).

### What if the user wants the whole list now?
Give a short ordered list if they ask, and run it one step at a time. Ask for the first, wait for the result, then continue.

### Does one-change-at-a-time shorten support chats?
I found no study on chatbots, and the sources in section 4 give no numbers. They support the check-after-each-change idea in human practice only. Measure steps to resolution on your own traffic.

---
## Technical section

### T1. Solution architecture
```
user turn -> parse: steps tried, results reported -> step log (step, by, result)
draft reply -> troubleshooting check: one change? repeats a logged step? last result recorded?
            -> rewrite to one change + result to report, or hand off after 3 changes
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| At most one change per reply | Pre-send check | Tests 1, 2; counter-view metric |
| No step already in the log | State plus pre-send check | Test 3; primary metric |
| New change only after the last result | State (`waiting_on`) | Test 4 |
| Verification before close | Resolution gate | Test 5 |
| Hand off after three changes | Pre-send check | Test 8 |

### T3. Evals
- **Dataset:** 60 troubleshooting openings to start across Wi-Fi, printers, phone sync, and login problems. Include 15 where the user already tried steps, 10 where the first step fixes it, and 10 that need a hand-off.
- **Judge rubric:** how many changes does the reply ask for; is the result to report named; is any step repeated from the log; is the original symptom confirmed before close?
- **Release gate:** block a deploy if multi-change replies or repeated steps exceed your target (starting points, to tune).

### T5. Trade-offs
- More turns per chat. The log and the pre-send check add engineering work.
- Parsing "I did 1, 2 and 4" into log entries will miss some cases. Sampled review of repeated-step flags catches them.

---
### Deep dive
- **Open question.** I found no study of chatbot troubleshooting. The evidence here is human practice from engineering and IT training sources.
- **References.** [Google SRE book, ch. 12](https://sre.google/sre-book/effective-troubleshooting/) (opened); [OpenExamPrep, CompTIA methodology](https://open-exam-prep.com/study-guides/comptia-a-plus/troubleshooting-hardware-network/troubleshooting-methodology) (opened); [AlphaPrep, six-step methodology](https://blog.alphaprep.net/mastering-the-six-step-troubleshooting-methodology-real-world-strategies-for-comptia-a-core-1-success/) (opened).
