# Browser Agent Clicked the Wrong Thing and Said "Done": Misreading the Screen

<!-- SEO
title: Browser Agent Clicks Wrong Element or Loops: Misreading the Screen
description: Why an AI browser agent clicks the wrong element, misreads the page, or loops, then tells the user it worked, and a verify-after-every-action fix.
search phrases:
- ai browser agent clicked wrong button
- browser agent says task complete but did not
- web agent gets stuck in a loop on a page
- ai agent misreads web page state
- browser use agent verify action result
- computer use agent wrong click recovery
- chatbot that browses the web did the wrong thing
-->

**Frequency**: Common

## Issue: A browser agent clicks the wrong element, misreads what the page now shows, or repeats the same step, and the chat reply claims success or goes silent instead of saying it is unsure.

> **One line:** The agent acts on a page it has read wrong, never checks the result, and then tells you in chat that it worked.

| | |
|---|---|
| **Channel** | Chat (a text assistant that drives a browser for the user and reports back in the chat). Voice and visual reporting are planned, not written. |
| **Stakes** | Medium to high. A wrong click can add the wrong item, submit the wrong form, or change a setting. |
| **Who is affected** | Anyone who hands a web task to an assistant and reads only its summary |
| **Frequency** | Common in browser agents (our judgment). I found no count of how often a wrong click reaches a false chat report. |
| **Pattern ID** | misreading-the-screen |
| **Family** | [Browser agents](../README.md) |
| **Goal** | Browsing agents stay within the user's intent and the site's rules, and ask before consequential actions. |
| **Primary metric** | Recovery rate after a wrong click: share of detected wrong clicks that end in a correction or a plain report to the user, never a "done" claim. Starting target: 100% of detected cases (tune). Step success rate is reported alongside. |
| **Maturity** | Researched (flag R: research risk; see section 4) |
| **Will a better model fix this?** | Partly. Better models read pages more accurately, but checking the page after each action is a design step, not a model skill. (Our judgment, not tested.) |
| **Also searched as** | browser agent wrong click · web agent loops · AI agent says done but didn't · agent misreads page · computer use agent mistakes |

## 1. In plain words
A browser agent works from what it thinks the page shows. If it reads the page wrong, it clicks the wrong thing, or it keeps repeating a step that is not working. The user sees the result in the chat: "Done, I added the black size 10," when the cart holds something else, or silence while the agent loops.

The fix: after every action that changes something, check what the page now shows against what the action should have changed. If the check fails twice, stop and tell the user.

## 2. What it looks like
**Without the fix**
```
User: Add the Nike Pegasus 41, men's size 10, black, to my cart on shoestore.example.
Bot:  (working for 90 seconds, no message)
Bot:  Done! I added the Nike Pegasus 41, size 10, black, to your cart.
User: (opens the cart) It's a size 9 in white.
Bot:  I apologize for the confusion. Let me try again.
```
**With the fix**
```
User: Add the Nike Pegasus 41, men's size 10, black, to my cart on shoestore.example.
Bot:  On it. I'll check the cart before I tell you it worked.
Bot:  The cart shows a size 9 in white, not what you asked for. I clicked the wrong size button. I'm removing it and trying size 10 once more.
Bot:  The size 10 button is greyed out, so I can't confirm it is in stock. Nothing is in your cart now. Want me to check size 10.5, look at another store, or stop here?
```
The fixed bot reads the cart after the click, says the click was wrong in plain words, and stops at a second miss with the choice left to the user.

## 3. Why it happens
These are our reading of the pattern, supported where noted in section 4.
- **No check after the action.** The agent treats "the click ran" as "the click worked." The page state is never compared with the goal.
- **The page is read imperfectly.** The agent works from screenshots or a page tree. Layout shifts, unlabeled buttons, and content that has not finished loading can all send it to the wrong target.
- **The reply is written from the plan, not the page.** The same model that planned the steps writes "done," so the chat summary repeats the plan.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In WebArena, the best GPT-4-based agent reached 14.41% end-to-end task success; humans reached 78.24%. | [Zhou et al., *WebArena*, arXiv 2307.13854](https://arxiv.org/abs/2307.13854). Opened; abstract read. | 2023 models; I did not check current results. The paper blames simplified training environments, not this pattern specifically. |
| In OSWorld, humans completed over 72.36% of tasks; the best model reached 12.24%. | [Xie et al., *OSWorld*, arXiv 2404.07972](https://arxiv.org/abs/2404.07972). Opened; abstract read. | Computer tasks across apps, not only browsers; 2024 models. The gap does not show how many failures were wrong clicks. |
| A write-up splits browser-agent failures into action level (the action did not execute), step level (it ran but the page is in an unexpected state, such as a wrong page or a blocking modal) and run level (the agent reports completion without reaching the goal). It calls run-level failure the most expensive to detect. | [Notte, *How do browser agents recover from errors*](https://www.notte.cc/glossary/ai-browser-agents/how-do-browser-agents-recover-from-errors). Opened and read. | Vendor glossary page, not a study. It also gives a 60-70% success figure for a plain observe-think-act loop with no method; I do not rely on it. |
| An agent asked to add a specific sneaker to a cart added the wrong shoe and reported success. The author's point: confirming the outcome is a separate step from carrying out actions. | [TinyFish, *Between complete and correct*](https://current.tinyfish.ai/issue/31/practitioners-corner/article/18052/between-complete-and-correct). Opened and read. | One anecdote in a vendor newsletter, not a rate. |

Read only through search summaries, not opened, and kept out of the fix: a claim that confident false completions are about 45-48% of failures on short tool-use tasks (a secondhand newsletter citing an arXiv paper), and several blog posts on "hallucinated success." I found no study of how often a browser agent's chat report misstates the page.

**Public incident.** No public incident found. Searches run: "web agent benchmark success rate WebArena human vs best agent", "browser agent misreads page state clicks wrong element loops failure analysis", "computer use agent claims task completed but did not complete false success reports". They returned benchmark papers and practitioner posts, with no dated incident I could open.

**Research risk (R).** The benchmark gaps are real but old, and success rates change fast. Check a current leaderboard before quoting a figure.

## 5. The fix

**The principle:** No action counts as done until the page shows the change it was meant to cause, and the chat only says what the page showed.

**Do this**
1. **Verify after every state-changing action.** After a click, a form fill, or a page change, read the page again and compare it to the expected result (for example, the cart line shows the requested size and color). Each step is "confirmed" or "not confirmed," never assumed.
2. **Name the target before clicking.** Before a click that changes something, the agent identifies the element in terms the user would recognize ("the size 10 button"). If more than one element could match, it does not guess.
3. **Say "done" only for confirmed outcomes.** The final chat message states what the page showed ("the cart now lists size 10, black, $129.99"), not what the agent planned.
4. **Cap repeats.** The same action on an unchanged page twice, or three failed steps in a row, ends the attempt. No silent loop.
5. **Report a wrong click when you find it.** Say what happened, whether anything was changed, and what you are doing about it, in one message.
6. **Stop when unsure.** If the page state is unclear (blocking pop-up, login wall, a layout the agent cannot read), say so and give the user a choice. Do not press on.
7. **Ask before consequential actions.** Purchases, submissions, deletions, and account changes wait for a clear yes in chat, shown with the exact item and price as read from the page.
8. **Keep the user informed on long runs.** Follow [silent long-running work](../../response-time/failures/silent-long-running-work.md): a status within about ten seconds, describing only real steps.

**Reference design: check-then-report loop**
```
for each step that changes the page:
  expected = what the page should show after this step
  act()
  observed = read the page again
  if observed matches expected:   mark step "confirmed"
  else if first miss:             undo if safe, retry once with a different target
  else:                           stop, report, offer choices
final message = only "confirmed" steps, each with the value the page showed
```
```
Prompt block: After each action that changes the page, read the page and say what you see.
Only call a step done if what you see matches the goal. If you see the same page after two
tries, stop and tell the user what happened. Never describe a step as done that you did not
see on the page.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The check failed or the page cannot be read: say what the page shows and where the user can look |
| Offer choices: 2-4 options plus "Something else", free text open | After a failed retry: "Try another way", "Show me what the page says", "Stop here", "Something else". Do not offer them when the check passed |
| Ask one clarifying question | Two page elements could match the request ("size 10 or 10.5?") and the answer changes the result |
| Hand off to a person | Two failed attempts, or the next step is a purchase or account change the agent cannot confirm. Do not hand off if the user asked to stay with the bot |

**Don't over-correct.** Do not verify read-only steps (scrolling, opening a page) as if they were purchases, and do not stop to ask the user about every click. Checking only state-changing steps keeps the assistant fast. Do not fill the chat with narration; one confirmed-result line per consequential step is enough.

**Hand-off rule.** After two failed attempts at the same step, or when a purchase or account change cannot be confirmed from the page, hand off to the user or a person with the last page state, the steps taken, and what changed (see [cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No test file is written for this pattern. Results: **Not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | The site selects the wrong size after a click | The bot reads the cart, says it is wrong, and does not say "done" (1, 3, 5) |
| 2 | Two buttons could both match the request | The bot asks which one, or names the one it chose, before clicking (2) |
| 3 | A pop-up blocks the same button on every try | Stops after two tries and tells the user (4, 6) |
| 4 | The task is to place an order | The bot waits for a yes showing item and price read from the page (7) |
| 5 | The task runs 40 seconds | A status message appears by about ten seconds, real steps only (8) |
| 6 | The check passes on the first try | A short confirmation, no extra questions (Don't over-correct) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Recovery rate after a wrong click** (primary) | 100% of detected cases end in a correction or plain report | Log each failed post-action check, then label whether the next chat message reports it | Below 95% |
| Step success rate | Track; set from your own baseline | Share of state-changing steps whose check passes, per site | A drop of 10 points from baseline |
| "Done" reports that match the final page state (false-claim check) | 100% | Sampled review: compare the final message to the last page snapshot | Below 98% |
| Runs ended by the repeat cap | Track | Count of runs ended by rule 4 | Doubling week over week |
| Questions to the user on read-only steps (counter-metric: over-correction) | 0 | Questions on non-state-changing steps | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Same action twice with no change in the page snapshot | Action log plus a page-state hash per step | A slow page that was retried on purpose |
| Final "done" message with no confirmed check for the claimed step | Step log: check result versus the claim in the final message | A read-only task where no check applies |
| The element clicked differs from the target named for the user | Planned target versus clicked element label | The site renamed the element |
| Long gap with no status message while the action count rises | Time since last message versus step events | A single slow page load |
| User says "that's not what I asked" soon after a "done" message | The next user turn after a success claim | A user changing their mind |

**Starter rule:** after any click or form change, read the page and say "done" only if it shows the result you were asked for.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: misreading-the-screen
runs: pre_send
reads: [step.expected_state, step.observed_state, step.check_result, step.repeat_count, draft.claims_done]
trigger: a step changes the page, or a final "done" message is about to be sent
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["Try another way", "Show me what the page says", "Stop here", "Something else"]
on_miss: rewrite
metric: recovery rate after a wrong click
counter_metric: done reports that do not match the final page state
status: proposed
```

## 8. Related patterns
- [Silent long-running work](../../response-time/failures/silent-long-running-work.md): the quiet wait. This pattern adds that the agent may be working on the wrong thing, and what it may claim at the end.
- [False completion claim](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/false-completion-claim.md): the same "done" claim, caused by a tool error. Here the evidence is the page, not a tool result.
- [Wrong-target action](../../../../external-actions/goals/action-execution/failures/wrong-target-action.md): acting on the wrong record. Here the cause is misreading what is on screen.
- [Unbounded action loop](../../../../external-actions/goals/action-execution/failures/unbounded-action-loop.md): the retry loop with no cap. This page covers the loop only as it shows in chat.
- [Lazy completion](../../effort-and-memory/failures/lazy-completion.md): reporting what is left undone.

## 9. Common questions
### Why does my browser agent say it finished when it didn't?
The reply is often written from the plan, not the page. Add a check after each state-changing step and let only confirmed steps appear in the final message (rules 1 and 3).

### How do I stop a web agent from looping on the same page?
Cap repeats: the same action on an unchanged page twice ends the attempt, and the agent tells the user (rule 4). Log a page-state hash per step so loops show up in the logs.

### Will a better model stop wrong clicks?
Partly. The benchmarks I opened show large gaps to humans, but they cover 2023 and 2024 models and do not show the cause. A verification step helps with any model.

### Should the agent ask before every click?
No. Ask before consequential actions (rule 7) and when two elements could match (rule 2). Checking read-only steps wastes time.
