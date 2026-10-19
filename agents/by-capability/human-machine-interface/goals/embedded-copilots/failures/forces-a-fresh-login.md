# Support Chatbot Makes Me Log In Again: Forces a Fresh Login

<!-- SEO
title: Chatbot Asks Me to Log In Again: Why and How to Fix It
description: Why a help chatbot makes signed-in users log in again, when a fresh login is justified, and how to share the session and step up only for risky actions.
search phrases:
- chatbot asks me to log in again
- support chat makes me sign in again even though I'm logged in
- how to share login session with chatbot widget
- step up authentication chatbot sensitive actions
- chatbot loses session when transferred to agent
- do I need to verify my identity again with the chatbot
- authenticated chatbot best practices
-->

**Frequency**: Common

## Issue: An assistant inside a product asks the signed-in user to sign in or verify again when it opens, hands off, or changes channel, even for low-risk requests.

> **Read this first.** This page is design guidance, not security or legal advice. Which actions need a fresh check, and how strong it must be, is a security decision for your team. Have a security professional review any policy before use.

> **One line:** The user is already signed in, and the help assistant treats them as a stranger.

| | |
|---|---|
| **Channel** | Written for **chat** inside a product. Phone transfers have the same problem (voice is planned, not yet written). |
| **Stakes** | Low for the wasted time, but the fix touches security. Skipping the check on risky actions is the opposite and worse failure. |
| **Who is affected** | Signed-in users, especially those who open help in the middle of a task |
| **Frequency** | Common. I found no study of how often it happens; the evidence below is about how sessions and widgets work. |
| **Pattern ID** | forces-a-fresh-login |
| **Family** | [Embedded copilots](../README.md) |
| **Goal** | An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs. |
| **Primary metric** | Re-authentication prompts for already-authenticated users on low-risk actions. Starting target: near 0, while keeping step-up for high-risk actions. |
| **Maturity** | Tests written (see [the test file](../../../tests/forces-a-fresh-login.md); not yet run). Needs expert (security) review before use. |
| **Will a better model fix this?** | No. It is session plumbing and a risk policy, not language. (Our judgment, not tested.) |
| **Also searched as** | chatbot makes me log in again · support widget not logged in · chat widget loses my session · re-authenticate in chat · verify identity again chatbot |

## 1. In plain words
You sign in to an app, open its help chat, and the chat asks you to sign in or prove who you are. Sometimes that is right: you want to change your bank details. More often you asked "what are your hours?" and it still wants your password. Help widgets are often built separately from the app, so they do not share your session.

## 2. What it looks like

**Without the fix**
```
(User is signed in and viewing their invoice)
User: Why is this invoice higher this month?
Bot:  To help with your account I need to verify your identity. Please sign in: [link]
      (the link opens a login page; the chat is gone after sign-in)
User: I'm already signed in...
```

**With the fix**
```
User: Why is this invoice higher this month?
Bot:  This invoice includes a one-time $15 setup fee added on October 3 and your usual $40 plan.
      Want me to explain the fee or see how to remove it?
User: Remove the fee
Bot:  Changing charges needs a quick check. I'm sending a code to the phone ending 21. (Your chat stays open.)
```
The fixed assistant used the signed-in session for a low-risk question, and stepped up once for a risky one, without losing the chat.

## 3. Why it happens
These are our reading of the pattern; the sources below report mechanisms, not causes.
- **The widget is separate from the app.** It starts a new anonymous session instead of receiving the user's identity from the app.
- **A blanket rule.** "Verify everyone" is easier than deciding which actions are risky.
- **State is lost on handoff or channel change.** The verified result does not travel with the conversation.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A chat widget vendor documents that anonymous, non-verified, and verified visitors are handled differently, and that if a user sometimes loads the widget verified and sometimes not, the history experience will not be the same. | [Open.cx, *Conversation Sessions*](https://docs.open.cx/widget/conversation-sessions.md). Opened and read. | Vendor documentation describing one product, not a study. It shows the mechanism: the widget needs to be told who the user is. |
| NIST's digital identity guidelines (SP 800-63B-4, Authentication Assurance Levels) describe session timeouts. At AAL2 the overall reauthentication timeout should be no more than 24 hours and the inactivity timeout no more than 1 hour; after an inactivity timeout, the verifier may allow reauthentication with only a password or biometric together with the session secret. At AAL3 the limits are 12 hours and 15 minutes. | [NIST SP 800-63B-4, AAL section](https://pages.nist.gov/800-63-4/sp800-63b/aal). Opened and read. | A benchmark for federal digital identity systems, not a rule for every product. Use it as a reference point, and check which assurance level, if any, applies to you. |

**Public incident.** No public incident found. My searches for chatbots forcing a second login returned vendor documentation and forum posts, not a dated, sourced case.

## 5. The fix

**The principle:** Pass the signed-in session to the assistant securely, let it answer low-risk questions without a new check, and ask for a stronger check only before risky actions, inside the app's own secure screen.

**Do this**
1. **Pass the session to the assistant** with a server-side identity exchange when the widget loads, so the assistant knows who is signed in. Do not ask the user to type a password into the chat.
2. **Classify actions by risk, in writing.** Low: read-only answers about the user's own data. Higher: anything that moves money, changes contact or login details, exposes sensitive records, or cannot be undone. Your security team sets the list.
3. **No new check for low-risk actions** when the session is valid.
4. **Step up only for higher-risk actions.** Say why ("Changing charges needs a quick check"), use the strongest method your policy requires, and run it in the app's secure UI, not in chat.
5. **Keep the conversation across any check.** After step-up or sign-in, return to the same chat with its state.
6. **Carry the result on handoff or channel change.** Pass "verified at turn N by method M" so the next person or channel does not ask again (see [cold transfer](../../human-handoff/failures/cold-transfer.md)).
7. **If the session has expired,** say so plainly and offer a one-step sign-in that returns to the chat.
8. **Never collect passwords, codes, or card numbers in chat.** See [sensitive data collected in chat](../../channel-selection/failures/sensitive-data-collected-in-chat.md).

**Reference design: a risk table the policy layer reads**
| Request | Risk | Check |
|---|---|---|
| "What are your hours?" | None | None |
| "Why is my invoice higher?" (own data, read-only) | Low | Valid session |
| "Resend my receipt" | Low | Valid session |
| "Change my email" | Higher | Step-up in the app |
| "Remove this charge" or "refund me" | Higher | Step-up in the app |
| "Show my full card number" | Never in chat | Decline; point to the app |
| Session expired | Any | One-step sign-in, return to chat |

```
You know who the user is only if the app tells you. Use that identity for questions about their own data.
Before any action that changes money, contact details, login, or sensitive records, tell the user a quick check is needed,
and start the app's secure check. Never ask for a password, code, or card number in the chat.
If the check passes, continue the same conversation. Record that the user was verified, when, and how.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | A low-risk, read-only question arrives in a valid session: answer it with no sign-in or verification prompt |
| Admit uncertainty and show how to check | A higher-risk request needs a check, or the session has expired: say plainly why ("Changing charges needs a quick check") and start the check in the app |
| Offer choices | The session has expired: "Sign in and return to this chat", "Talk to a person", "Something else", with free text open. Do not offer them for a low-risk question in a valid session; answer it |
| Hand off to a person | Verification fails: route to a person with a stated reason and pass the verification result and method |

**Don't over-correct.** Remove the step-up for risky actions and you invite account takeover. A valid session on a shared device is not proof the person typing is the account owner for high-risk actions. Do not extend session lifetimes to avoid prompts without your security team's agreement.

**Hand-off rule.** On handoff, pass the verification result and its method so the person does not repeat it. If verification fails, route to a person with a stated reason.

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/forces-a-fresh-login.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Signed-in user asks a read-only question | No sign-in or verification prompt |
| 2 | Same user asks to change their email | A step-up prompt in the app, with a stated reason |
| 3 | Step-up completes | The same chat continues |
| 4 | Handoff after verification | The person does not ask to verify again |
| 5 | Session expired | The assistant says so and offers a one-step sign-in |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Re-auth prompts on low-risk actions for authenticated users** (primary) | Near 0 (under 2%) | Log: prompts shown where the session was valid and the action was classed low-risk | Over 5% |
| Step-up on higher-risk actions (counter-metric) | 100% | Log: higher-risk actions completed with a step-up event | Any miss |
| Conversations that survive a check | Over 95% | Chats that continue after sign-in or step-up | Below 90% |
| Credentials typed in chat | 0 | Pattern scan of stored transcripts for passwords and codes | Any |
| Verification repeated after handoff | Under 3% | Handoffs where the person re-verified | Over 8% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A sign-in or verification prompt is shown while the session is valid and the action is low-risk | Prompt event with `session.valid` and `action.risk_class` | The action was higher-risk in the written risk table, or the session had expired |
| The chat does not continue after a sign-in or step-up | No user or bot turn in the same chat after the sign-in or step-up event | The user finished their task before the check |
| A password, code, or card number appears in a user turn | Pattern scan of stored user turns | A reference number that only looks like a code |
| The user says they are already signed in, right after a prompt | User turn text following a prompt event, with `session.valid` true | The user was not signed in |
| A person or channel asks to verify again after a handoff | Verification prompt after a handoff event, with `handoff.verification_result` present | Verification had failed, so the result was passed as failed |

**Starter rule:** No new check for low-risk actions when the session is valid.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: forces-a-fresh-login
runs: pre_send
reads: [session.valid, action.risk_class, reauth_prompt_event, stepup_event, handoff.verification_result]
trigger: a sign-in or verification prompt is about to be shown to a signed-in user
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Sign in and return to this chat", "Talk to a person", "Something else"]
on_miss: rewrite
metric: re-authentication prompts for already-authenticated users on low-risk actions
counter_metric: step-up on higher-risk actions
status: proposed
```

## 8. Related patterns
- [Re-asks for known information](re-asks-for-known-information.md): asking for details the product holds. This page is about proof of identity.
- [Sensitive data collected in chat](../../channel-selection/failures/sensitive-data-collected-in-chat.md): why credentials do not belong in chat.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): losing verification across a handoff.
- Planned in the [privacy, governance and access roadmap](../../../roadmap/privacy-governance-and-access.md): identity verification (GV-09), the other side of the trade-off.

## 9. Common questions
### Why does the support chat ask me to log in when I already am?
The widget was probably built separately and did not receive your session. The product should pass it to the assistant (rule 1).

### When is it right for a chatbot to ask for verification?
Before actions that move money, change contact or login details, or expose sensitive records. Your security team defines the list. See the table in [section 5](#5-the-fix).

### Is it safe for the chatbot to know I'm logged in?
It can be, if the app passes the identity over a server-side exchange and the assistant only sees what you are allowed to see. A security review should confirm the setup.

### How long should a session last before asking again?
That is a policy choice. NIST's guidelines give reference limits by assurance level (for example 24 hours overall and 1 hour of inactivity at AAL2), which may not apply to your product ([section 4](#4-why-it-matters)).

---
## Technical section

### T1. Solution architecture
```
app (signed in) -> server issues short-lived assistant token -> widget -> assistant
assistant action -> policy layer (risk table) -> low: proceed | higher: start step-up in the app -> resume chat
```
The token carries identity and verification state, is short-lived, and is scoped to this user. The policy layer, not the model, decides the check.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Higher-risk actions require a step-up event | Policy layer | Log join of actions to step-up events |
| No credentials accepted in chat | Input filter | Scan and block; test 10 |
| Assistant token scoped to one user | Token service | Access test with two accounts |

### T3. Evals
- **Dataset:** 150 requests across the risk table, with valid, expired, and missing sessions.
- **Judge rubric:** was a check requested exactly when the policy requires one?
- **Metrics and starting thresholds:** unnecessary prompts under 2%; missed step-ups 0%. Starting points to tune.
- **Release gate:** block a deploy on any missed step-up.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Missed step-up | Any | Any | Disable the affected action path and review |

### T5. Trade-offs
- Passing identity into the widget widens the attack surface; review tokens, scopes, and logging.
- Fewer prompts help usability but raise the cost of a stolen session; set the risk table with security.

---
### Deep dive
- **Voice.** Voice lines often ask for identity again at every transfer; the same split of low and higher risk applies (voice is planned, not yet written).
- **Open question.** I found no study of how often users are forced to log in again for help chat. Everything here is mechanism, not frequency.
- **References.** [Open.cx](https://docs.open.cx/widget/conversation-sessions.md) (opened); [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b/aal) (opened).
