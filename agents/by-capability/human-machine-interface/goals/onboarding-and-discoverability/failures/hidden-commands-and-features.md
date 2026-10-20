# Chatbot Feature Discoverability: Slash Commands and Features Users Never Find

<!-- SEO
title: Chatbot Feature Discoverability: Hidden Slash Commands
description: Why chatbot users never find slash commands, shortcuts and settings, and how to surface one feature in one line at the moment it would help.
search phrases:
- chatbot feature discoverability
- slash commands discoverability
- users don't know about slash commands
- how to make chatbot features discoverable
- contextual tips in chat assistant
- in-app feature discovery AI assistant
- chatbot help command /help
-->

**Frequency**: Common

## Issue: The assistant has a command, shortcut or setting that would save the user work right now, but it never mentions it, so the user keeps doing the job the slow way and the feature goes unused.

> **One line:** The user logs six receipts one at a time while a one-step import sits behind a "/import" command nobody told them about. The fix is to name the feature in one line, at the moment it would help, after doing what the user asked.

| | |
|---|---|
| **Channel** | Written for **chat** (text assistants with slash commands, buttons and settings). Voice commands are PLANNED and out of scope for this phase. |
| **Stakes** | Low per conversation. The cost is wasted effort, features that look like failures because nobody uses them, and users who decide the assistant "can't do that". |
| **Who is affected** | Regular users who settled into one way of working, and anyone who never opened the help page |
| **Frequency** | Common, in our judgment. One study of AutoCAD found the largest group of users used only 31 to 40 of its thousands of commands (section 4); I found no count for chat assistants. |
| **Pattern ID** | hidden-commands-and-features |
| **Family** | [Onboarding and discoverability](../README.md) |
| **Goal** | People know what the assistant can do and how to start, without needing to guess or to engineer prompts. |
| **Primary metric** | Share of active users who used a given feature, tracked per feature. Starting target: set from your own baseline, then track the lift after hints ship. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The model does not know the product's commands, what this user has already used, or when a hint is welcome unless the product tells it; that is a product decision. (Our judgment, not tested.) |
| **Also searched as** | hidden chatbot features · slash command menu not discoverable · users never use our new feature · chatbot shortcuts nobody knows · feature adoption in AI assistant · contextual tooltips for chat |

## 1. In plain words
Many assistants have more than a text box: slash commands, file import, saved templates, a setting that remembers preferences. They live in a menu that appears only when you type "/", or in a help page nobody reads. So the user does the work by hand, and the assistant helps them do it by hand. The fix is a short, well-timed "you can do this in one step" that appears when the user is doing exactly the thing the feature speeds up.

## 2. What it looks like
A bookkeeper at a plumbing company in Columbus, Ohio, logs expenses in an accounting app's assistant.

**Without the fix**
```
User: Log $42.18, Home Depot, 10/14, job supplies
Bot:  Logged: $42.18, Home Depot, Oct 14, Job supplies.
User: Log $16.50, Shell, 10/14, fuel
Bot:  Logged: $16.50, Shell, Oct 14, Fuel.
User: Log $88.00, Ferguson, 10/15, job supplies
Bot:  Logged: $88.00, Ferguson, Oct 15, Job supplies.
      (three more follow; the CSV export from her card sits on her desktop)
```

**With the fix**
```
User: Log $88.00, Ferguson, 10/15, job supplies
Bot:  Logged: $88.00, Ferguson, Oct 15, Job supplies.
      Tip: if these are on a card statement, type /import or drop the CSV here and I'll log them all at once.
      [Import a file] [Keep going here] [Something else]
User: Import a file
Bot:  Drop the CSV from your card. I'll show the rows before saving anything.
```
The fixed bot does the task first, then names one feature, how to call it, and lets her ignore it.

## 3. Why it happens
- **Features are added to a menu, not to the conversation.** A new command ships in the "/" list and the release notes. Nothing connects it to the moment a user is doing the slow version of the same job.
- **The assistant cannot see the user's habits.** It sees one message at a time, not "third manual entry in a row" or "never used /import", so it has no trigger for a hint.
- **Teams fear nagging.** Memories of "Tip of the Day" style interruptions push teams to say nothing at all, instead of saying one thing at the right time.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| NN/g separates "push revelations" (help not relevant to the user's goals) from "pull revelations" (contextual tips relevant to the task), says push revelations "are often ignored by users because they get in the way", and advises: "Favor pull over push revelations." It also says to keep proactive help short and make push help easy to dismiss. | [Kendrick, *Help and Documentation (Usability Heuristic #10)*, Nielsen Norman Group, Dec 13, 2020](https://www.nngroup.com/articles/help-and-documentation/). Opened and read. | General interface guidance, not chat, and not an experiment. |
| In AutoCAD, "the largest group of users only use between 31 and 40" of its thousands of commands; the authors name the user's awareness of relevant functionality as the core challenge. Their recommender showed new commands in a peripheral palette, chosen to avoid interrupting work. In a study with 36 AutoCAD users, 30.9% of item-based recommendations were "good" (new to the user and the user said they would use it), against 14.7% for an older method, the paper's "2.1 times". | [Matejka, Li, Grossman and Fitzmaurice, *CommunityCommands: Command Recommendations for Software Applications*, UIST 2009](https://www.research.autodesk.com/publications/communitycommands-command-recommendations-for-software-applications/). Abstract page and full-text PDF opened and read. | Desktop CAD software in 2009, from the vendor's own research lab. "Will use" is self-reported intent, not observed use. Single source for the 31 to 40 figure. |
| In a task-based study of 27 Android and iOS users, users had limited awareness of default features, and "Awareness of these features does not imply that a user can easily locate and adjust them when needed." | [Ramokapane, Mazeli and Rashid, *Skip, Skip, Skip, Accept!!!*, PoPETs 2019](https://www.petsymposium.org/popets/2019/popets-2019-0027.php). Abstract page opened and read. | Smartphone privacy settings, not chat. I read the abstract, not the full paper. |
| Mattermost's design page for slash command autocomplete says "many users don't necessarily know about slash commands at all", and that the helper menu disappears when the user presses the space bar, just as they need to remember the options. | [Mattermost, *Slash Command Autocomplete* overview (Confluence), last updated Dec 2, 2019](https://mattermost.atlassian.net/wiki/spaces/SCA/overview). Opened and read. | A vendor's own design page, not a study. |
| GitLab proposed replacing the last of four pre-written questions on its Duo Chat splash screen with the `/help` command so users learn it exists, and only after `/help` ships; a GitLab research issue lists "Do users discover the slash command menu" as a question to test. | [GitLab issue 472278](https://gitlab.com/gitlab-org/gitlab/-/issues/472278) and [GitLab UX research issue 3098](https://gitlab.com/gitlab-org/ux-research/-/issues/3098). Both opened and read. | Vendor issue trackers. The research page reports no findings in its text, so it shows the question, not an answer. No date shown in what I read. |

**Public incident.** No public incident found. My searches returned feature requests and design notes, not a dated, sourced event.

## 5. The fix

**The principle:** Name one feature, in one line, when the user is doing the slow version of what it does, after doing what they asked.

**Do this**
1. **Keep a feature map.** For each command, shortcut or setting, store: what it does, how to call it (the exact command and a button), and the trigger, meaning the user behavior it shortcuts (for example, "three manual expense entries in one session").
2. **Do the task first.** The hint comes after the answer or action in the same reply, never instead of it.
3. **Hint only on a trigger.** No unprompted feature tips at login or on an idle screen; that is a push revelation (section 4).
4. **One hint per reply, and one line.** Say what it does, how to call it, and stop. Starting cap: at most two unrequested hints per session (tune).
5. **Never hint a feature the user already uses, or one they dismissed.** A dismissed hint stays quiet for that user until the feature changes. CommunityCommands calls a useful suggestion the user already knows an "unnecessary recommendation".
6. **Hint only features that exist and are switched on for this user.** If one needs a plan upgrade, skip it or say so plainly in the hint (see [answers withheld behind an upgrade](../../embedded-copilots/failures/answers-withheld-behind-an-upgrade-unsaid.md)).
7. **Accept plain words too.** "Import my card statement" must work like `/import`; a hint never makes the command the only way in.
8. **Keep the full list findable on demand.** Typing "/" lists commands with one-line descriptions and their arguments, anywhere in the message; "what can you do here?" answers from the feature map.

**Reference design: feature map entry and hint rule**
```json
{ "feature_id": "expense_import",
  "does": "log many expenses at once from a CSV or card statement",
  "invoke": { "command": "/import", "button": "Import a file", "plain_words": ["import", "upload my statement"] },
  "trigger": { "event": "expense_logged_manually", "count_in_session": 3 },
  "eligible_if": ["feature_enabled", "plan_includes", "not_used_in_90_days", "not_dismissed"] }
```
```
After you complete the user's request, check the feature map. If one feature's trigger fired and the user is eligible,
add one line: what it does, the command, and a button. Never more than one feature per reply.
Do not mention features at the start of a chat, features the user already uses, or features they dismissed.
If the user asks "can you do this?" or "is there a faster way?", answer from the feature map. Treat plain-word requests like the command.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every reply where a hint fires: the requested task or answer comes first, the hint after it. |
| Offer choices: 2-4 options plus "Something else", free text open | Right after the hint: "Import a file", "Keep going here", "Something else". Do not offer them when the user is in a hurry or upset, when they already dismissed this feature, or when the request is a one-off with nothing left to speed up; then do the task and add no hint. |
| Admit uncertainty and show how to check | The feature depends on a setting or plan the assistant cannot confirm: say so and name where to check, instead of promising it works. |
| Hand off to a person | The user tried the feature twice and it failed, or cannot find the setting after the hint: offer support with the feature name and what they tried. |

**Don't over-correct.** A tip on every reply is the old "Tip of the Day" in a chat window and trains users to skip the line. Do not hint at the start of a conversation, do not stack two tips, and do not turn hints into upsells (see [help that becomes a sales pitch](../../embedded-copilots/failures/help-that-becomes-a-sales-pitch.md)). Do not stop doing the slow version: if the user chooses "Keep going here", keep logging one by one without comment.

**Hand-off rule.** If the feature fails twice for the user, or they cannot find a setting after the hint, offer a person and pass the feature name, the error and what they tried ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file exists yet for this pattern. Results: **Not yet run**.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | Third manual expense entry in a session | 1, 2, 3 | Entry logged first, then one line naming `/import` with a button |
| 2 | First message of a chat, no trigger | 3 | No feature tip |
| 3 | Trigger fires for two features in one reply | 4 | Only one feature is mentioned |
| 4 | User already used `/import` last week | 5 | No `/import` hint |
| 5 | User chose "Keep going here", then logs two more | 5 | No repeat hint; entries logged |
| 6 | Feature is off on the user's plan | 6 | Not hinted, or hinted with the plan stated plainly |
| 7 | User types "import my card statement" | 7 | Same result as `/import` |
| 8 | User types "/" mid-sentence, or asks "what can you do here?" | 8 | Command list with descriptions, from the feature map |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Share of active users who used a given feature** (primary) | Set from baseline per feature; track the lift | Distinct users with a `feature_used` event for the feature, divided by active users in the same window | Flat or falling four weeks after hints ship |
| Hint acceptance rate | Track; set from baseline | `feature_hint_shown` followed by `feature_used` for the same feature within the session | Falling two weeks in a row |
| Manual repeats after a trigger with no hint | Under 5% of fired triggers | Trigger events with no `feature_hint_shown` and an eligible user | Over 10% |
| Hints on already-used or dismissed features | 0 | `feature_hint_shown` where the user has `feature_used` (90 days) or `feature_hint_dismissed` | Any |
| Unrequested hints per session (counter-metric) | 2 or fewer | Count `feature_hint_shown` per session | Any session over 2 |
| Hint dismissal rate (counter-metric) | Track; set from baseline | `feature_hint_dismissed` divided by `feature_hint_shown` | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published. All are for text chat; voice and web-analytics signals are PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| The same manual action repeats past a feature's trigger count with no hint shown (rule 3) | Action events per session, joined to the feature map and `feature_hint_shown` | The user dismissed this hint before, so silence is correct |
| A feature's user share stays near zero while its trigger fires often (primary metric) | `feature_used` counts against trigger counts per feature | The feature is new or limited to a plan few users have |
| A user asks "is there a faster way" or "can you do these all at once" (rule 8) | Phrase match in the user turn | A question about a feature that does not exist; answered honestly |
| A hint appears in the first reply of a chat or with no trigger (rule 3, counter-metric) | `feature_hint_shown` with turn index 1 or no trigger id | A user who asked "what can you do?" |
| A hint names a feature the user already used or dismissed (rule 5) | `feature_hint_shown` joined to `feature_used` and `feature_hint_dismissed` history | A changed feature that was re-announced on purpose |

**Starter rule:** Name one feature, in one line, when the user is doing the slow version of what it does, after doing what they asked.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: hidden-commands-and-features
runs: post_turn
reads: [action_event.type, session.action_counts, feature_map.triggers, user.feature_used_history, user.feature_hint_dismissed, user.plan]
trigger: a feature's trigger fires for an eligible user after the requested task is done
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Import a file", "Keep going here", "Something else"]
on_miss: log
metric: share of active users who used a given feature
counter_metric: unrequested hints per session
status: proposed
```

## 8. Related patterns
- [Doesn't say what it can do](../../embedded-copilots/failures/doesn-t-say-what-it-can-do.md): the closest existing pattern. That page is about the first screen: an empty box with no word on what the assistant does. This page is mid-task: the user already uses the assistant, and one specific feature that would help right now stays hidden.
- [No likely-next-action suggestions](../../embedded-copilots/failures/no-likely-next-action-suggestions.md): what to do after a task ends. This page is about a faster way to do the task the user is doing now.
- [First-run tours that block use](first-run-tours-that-block-use.md): teaching everything up front, before the first question. This page is the opposite timing: teach one feature when it is needed, and never at the start.
- [Blank box: no hint what to ask](blank-box-no-hint-what-to-ask.md): the start of a chat; this page starts after it.
- [Starter suggestions that fail](starter-suggestions-that-fail.md): a suggested question that leads to a bad answer; a feature hint must pass the same test (rule 6).
- [Users must engineer prompts to get good results](users-must-engineer-prompts-to-get-good-results.md): rule 7 keeps plain words working, so the command is never the only way in.
- [Chat widget hard to find, or intrusive](chat-widget-hard-to-find-or-intrusive.md): when the whole assistant, not one feature, goes unnoticed.

## 9. Common questions
### How do I make chatbot slash commands discoverable?
Show the command list when the user types "/", with one-line descriptions and arguments, and mention one command in one line when the user is doing the slow version of its job. See [the fix](#5-the-fix).

### Why don't users use our chatbot's new features?
Often they never learn the feature exists. Studies outside chat found that users of large programs use a small share of the commands, and that knowing a feature exists is not the same as finding it ([section 4](#4-why-it-matters)).

### Should the chatbot show a tip of the day?
No. NN/g advises favoring contextual help over help pushed without regard to the user's task. Tie each tip to a trigger.

### Won't feature hints annoy users?
They can. Cap them per session, never repeat a dismissed one, and never show one for a feature the user already uses. Watch the dismissal rate.

---
## Technical section

### T1. Solution architecture
```
user turn -> task done -> action event logged (type, session count)
          -> hint selector: feature_map triggers x eligibility (enabled, plan, not used, not dismissed, session cap)
          -> at most one hint line + buttons appended -> log feature_hint_shown / used / dismissed
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Only mapped, enabled features are hinted | Hint selector reads the feature map | Diff map against shipped features in CI |
| One hint per reply; session cap | Hint selector | Count `feature_hint_shown` per reply and session |
| No hint for used or dismissed features | Eligibility check | Tests 4 and 5 |

### T3. Evals
- **Dataset:** 100 sessions from logs where a trigger fired, plus 30 with no trigger, labeled for "a hint would help here".
- **Judge rubric:** task done first; at most one hint; hint names the command and a button; no hint where none was due.
- **Metrics and starting thresholds:** no hint on used or dismissed features (0); unrequested hints per session 2 or fewer. Starting points to tune.
- **Release gate:** block a deploy if any hint names a feature absent from the feature map.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Hints on used or dismissed features | Any | Over 1% of hints | Check the eligibility join |

### T5. Trade-offs
- Usage history across sessions costs storage and a privacy review; a per-session trigger alone works but cannot honor "never hint what they already use".
- Each feature needs an owner who writes its trigger; features without one stay unhinted.

---
### Deep dive
- **Voice.** PLANNED and out of scope for this phase.
- **Open question.** I found no study of feature hints inside chat assistants. The evidence comes from general UI guidance, desktop software, smartphones, and vendor design notes.
- **Not used.** Search summaries mentioned a third-party mirror of a Claude Code feature request about a hard-to-reopen slash-command picker, an NN/g eye-tracking figure quoted on a vendor blog, and an untraced claim that most new features go unnoticed. I did not open their primary sources, so none is used.
- **References.** [NN/g, 2020](https://www.nngroup.com/articles/help-and-documentation/) (opened); [CommunityCommands, UIST 2009](https://www.research.autodesk.com/publications/communitycommands-command-recommendations-for-software-applications/) (opened, with full-text PDF); [PoPETs 2019](https://www.petsymposium.org/popets/2019/popets-2019-0027.php) (abstract opened); [Mattermost, 2019](https://mattermost.atlassian.net/wiki/spaces/SCA/overview) (opened); [GitLab 472278](https://gitlab.com/gitlab-org/gitlab/-/issues/472278) and [GitLab 3098](https://gitlab.com/gitlab-org/ux-research/-/issues/3098) (opened).
