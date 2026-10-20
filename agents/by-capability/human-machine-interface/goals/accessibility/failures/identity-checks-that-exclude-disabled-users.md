# Chatbot CAPTCHA or Verification Code Blocks Disabled Users: Identity Checks That Exclude Disabled Users

<!-- SEO
title: Chatbot CAPTCHA Blocks Disabled Users: Accessible Identity Checks
description: Chatbots that verify identity with a CAPTCHA, a voice check, or a timed code lock out people who can't use them. Offer an accessible alternative for every check.
search phrases:
- chatbot captcha accessibility
- captcha blocks blind users
- accessible identity verification chatbot
- verification code expires too fast accessibility
- WCAG accessible authentication chatbot
- voice verification deaf users alternative
- chatbot verify identity without captcha
-->

**Frequency**: Common

## Issue: A chatbot verifies identity with a CAPTCHA, a voice check, or a time-limited code and offers no other way, so people who can't see, hear, remember, or type fast enough are blocked from their own account.

> **Read this first.** This page is design guidance, not legal, security, or clinical advice. It states WCAG 2.2 success criterion 3.3.8 only as far as the W3C page I opened says it; I did not verify how any law (the ADA, Section 508, or a state rule) applies to your product. Ask counsel which standard binds you, and ask a security professional to approve which alternative checks are strong enough for each action.

> **One line:** The only way to prove who you are is a test the user can't take, and the bot has no second route.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice-check and phone flows are PLANNED, not written or measured here. |
| **Stakes** | High. The user can't reach their own account, a refund, a prescription, or a payment. |
| **Who is affected** | People who are blind or have low vision, are deaf or hard of hearing, have memory, reading, or attention limits, or type slowly or with switch or voice input |
| **Frequency** | Common. WebAIM's survey (below) ranks CAPTCHA the top problem for screen reader users; I found no count for chat identity checks. |
| **Pattern ID** | identity-checks-that-exclude-disabled-users |
| **Family** | [Accessibility](../README.md) |
| **Goal** | People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent. |
| **Primary metric** | Completion rate of identity checks by access need. Target: gap under 5 percentage points between people who use the accessible path and everyone else (a starting point to tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The check is a product and security decision, not language. (Our judgment, not tested.) |
| **Also searched as** | captcha impossible to solve · captcha for blind users · verification code timed out · can't verify identity over the phone deaf · bot says I'm not a human |

## 1. In plain words
To protect an account, the chatbot asks for a CAPTCHA, a spoken passphrase, or a six-digit code that expires. Each one assumes the user can see, hear, remember, or type within a short window. When one of those fails, the bot has no other path, so the user is locked out of the very help they came for. The fix is a second, equally strong way to pass every check, offered before the user gets stuck.

## 2. What it looks like
**Without the fix**
```
Bot:   To verify it's you, select all squares with traffic lights.
User:  I'm blind and use a screen reader. I can't do the image test.
Bot:   Please complete the verification to continue.
User:  Is there an audio one?
Bot:   Verification failed. Please try again.
```
**With the fix**
```
Bot:   Before I show your balance, I need to verify it's you. Pick a way:
       [Text a code to my phone] [Email me a link] [Use my passkey] [Talk to a person] [Something else]
User:  I need more time, I type with a switch.
Bot:   No problem. The code stays valid for 15 minutes and I can send a new one. Want it by text?
User:  Yes.
```
The fixed bot offers several checks up front, doesn't make the user explain a disability, and lets them extend the time.

## 3. Why it happens
- **A vendor widget is the whole design.** The team drops in a CAPTCHA or voice-biometric step for fraud control and never builds a second path, so one sense or one skill is required.
- **Security rules were written without an accessibility path.** "Code expires in 60 seconds" or "say this phrase" sits in a policy, and nobody owns the exception.
- **Testing uses typical users.** Fraud and QA test with fast, sighted, hearing users, so the lockout never appears in a test run.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| CAPTCHA was "the most (by a notable margin) problematic item" for respondents; respondents with disabilities were twice as likely as those without to rank it as problematic. Survey ran December 2023 to January 2024; 1,539 valid responses overall. | [WebAIM Screen Reader User Survey #10](https://webaim.org/projects/screenreadersurvey10/). Opened; the page I read did not give the CAPTCHA percentage. | Self-selected screen reader users, not all disabled people. About web CAPTCHAs, not chat. |
| The W3C says the CAPTCHA task "inherently excludes many people with disabilities, resulting in a denial of service to these users." It says audio CAPTCHAs often lack an easy replay, that voice-only authentication "cannot serve deaf and hard of hearing users properly", and it prefers "two-step or multi-device verification" to image tests. | [W3C, *Inaccessibility of CAPTCHA*, Group Draft Note, 16 December 2021](https://www.w3.org/TR/turingtest/). Opened and read. | A draft note that W3C says is "not endorsed" by W3C or its members. It is about CAPTCHAs, so I apply it to chat by analogy. |
| WCAG 2.2 success criterion 3.3.8 (Level AA) says a cognitive function test, "such as remembering a password or solving a puzzle", is not required for any step in authentication unless an alternative method, an assisting mechanism, object recognition, or personal-content recognition applies. | [W3C, *Understanding SC 3.3.8: Accessible Authentication (Minimum)*](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html). Opened and read. | A web content criterion; I did not verify that it covers a chat widget or that any law adopts it for your product. The object-recognition exception means some image CAPTCHAs may pass 3.3.8 yet still exclude blind users. |
| The W3C note cites an average of 32 seconds per CAPTCHA and argues disabled people likely spend more time. | Same W3C note, section 1.2. Opened. | The note's own figure; I did not trace its original study. |

I found no study of identity checks inside chatbots. The evidence is about web CAPTCHAs and authentication generally. I did not find a sourced public incident for this pattern and did not search for lawsuits.

## 5. The fix
**The principle:** Every identity check has a second route that needs a different ability, offered up front.

**Do this**
1. **Offer at least two checks that rely on different abilities.** For example a texted code (no image or audio test; readable by a screen reader) and a passkey or emailed link (nothing to memorize or retype). A CAPTCHA alone, or a voice check alone, never counts as the only route.
2. **Show the options before the first attempt.** The user chooses; the bot never asks whether they have a disability, and never demands proof of one.
3. **Never make a CAPTCHA, a voice check, or a puzzle the only route to a person.** A "Talk to a person" choice is always present on the check screen.
4. **Let timed steps be extended.** A code or link can be resent, and its time can be lengthened on request without asking why. State the time in the message ("valid for 15 minutes").
5. **Let people paste and use a password manager.** Don't block paste into a code or password field.
6. **Fail with a way forward.** After one failed check, name what failed and offer the other routes; never repeat only "verification failed".
7. **Keep the session.** If the user switches check or goes to a person, the conversation and what they already said carry over.

```
Before any identity check, offer at least two methods that need different abilities, plus "Talk to a person". Never ask the user to explain a disability.
Say how long a code lasts, let it be resent or extended on request, and allow paste. If a check fails, name the other routes.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | Before the first check: "Text a code", "Email me a link", "Use my passkey", "Talk to a person", "Something else". Don't offer a choice that is not available for this account. |
| Hand off to a person | The user says they can't complete any listed check, or one check has failed twice. Don't hand off if the user asked to stay with the bot and another check works. |

**Don't over-correct.** An alternative that is weaker than the main check becomes the attackers' route. Every route must meet the same assurance level your security team set for the action, and risky actions can still step up. Don't make everyone pick a method for a low-risk question either; verify only when the action needs it.

**Hand-off rule.** If the user can't pass any offered check, route to a person with the verification state and the user's request, so they don't repeat it ([cold transfer](../../human-handoff/failures/cold-transfer.md); [talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)). The person needs an accessible way to verify too.

**Framework used:** none yet.

## 6. How to test it (short version)
Tests: **Not yet run.** Test with disabled participants where you can; a checklist alone won't find the gaps.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Open an identity check with a screen reader | Two or more methods and a person route are announced before any test (1, 2, 3) |
| 2 | The user says "I can't do the image test" | The bot offers another method and does not ask about disability (2, 6) |
| 3 | The user needs more time for a code | The code is resent or extended and the new time is stated (4) |
| 4 | Paste a code from a message or password manager | The paste is accepted (5) |
| 5 | Fail a check once | The reply names the other routes (6) |
| 6 | Switch from the check to a person | The person sees the request and verification state (3, 7) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Identity-check completion rate by access need** (primary) | Gap under 5 points vs. others | Log check start and result with the method used and an opt-in access flag (the accessible path chosen, or a user setting). Don't infer disability | Gap over 10 points |
| Checks that offer 2+ methods and a person route | 100% | Log the methods shown on each check render | Below 100% |
| Failed checks followed by an alternative offer | 100% | Failure event followed by a bot turn naming other routes | Below 95% |
| Time-extended or resent codes completed | Track; set from baseline | Resend or extend event followed by success | Falling |
| Weaker-route fraud rate (counter-metric) | No higher than the main route | Fraud flags by method, reviewed by security | Any gap |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A check starts and ends with no completion and no other method tried | `verification.started` with no `verification.passed` and no second `verification.method` before session end | The user decided they didn't need the account action after all |
| The user says they can't do the check ("can't see", "can't hear", "no time") | Intent label on the user turn right after `verification.started` | A user asking how the check works |
| Two failures on one method | Count of `verification.failed` per `method` | Typos in a code |
| A code expires before use | `verification.code_expired` after `verification.code_sent` | The user left on purpose |
| The user asks for a person right after a check | Handoff request within 2 turns of `verification.started` | A routine request for a person |

**Starter rule:** before any identity check, offer at least two methods that need different abilities, plus a person.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: identity-checks-that-exclude-disabled-users
runs: pre_send
reads: [verification.started, verification.methods_offered, verification.method, verification.failed, verification.code_expired]
trigger: an identity check is about to be shown or has just failed
moves: [offer_choices, hand_off]
choices: ["Text a code", "Email me a link", "Use my passkey", "Talk to a person", "Something else"]
on_miss: rewrite
metric: identity-check completion rate by access need
counter_metric: weaker-route fraud rate
status: proposed
```

## 8. Related patterns
- [Sensitive data collected in chat](../../channel-selection/failures/sensitive-data-collected-in-chat.md): about where secrets are typed and stored. This page is about whether the user can pass the check at all.
- [Forces a fresh login](../../embedded-copilots/failures/forces-a-fresh-login.md): about re-verifying an already signed-in user. This page is about how the check itself is built, for anyone.
- [Voice-only flows with no text alternative](voice-only-flows-with-no-text-alternative.md): the same "one sense only" cause for voice features; voice checks are one case here.
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): the person route must actually work.
- A pattern on timeouts that are too short for assistive technology is being written separately and is not linked here. This page covers only the timing of identity codes.

## 9. Common questions
### Is a CAPTCHA accessible?
Not on its own. The W3C note says the task itself excludes many disabled people, and WebAIM's survey ranks CAPTCHA the top problem for screen reader users. If you keep one, offer another route (section 5, rule 1).

### Does WCAG require an alternative to a code or password?
Success criterion 3.3.8 asks that no authentication step require a cognitive function test unless an alternative, an assisting mechanism, or an exception applies (see the table above). Whether it binds your product depends on your law and contracts; ask counsel.

### Can I ask the user if they have a disability?
Don't make it a gate. Offer the same choices to everyone and let people pick. Logging a choice is fine; inferring a disability is not.

### Is an emailed or texted code accessible?
Often better than an image test, and the W3C note describes text-message codes as a dual-factor option. It still fails people with no phone or a short window, so allow resend and extension and keep a second route.

---
## Technical section

### T1. Solution architecture
```
action needs verification -> policy (assurance level) -> methods that meet it, >= 2 abilities
                          -> render choices + person route -> verify -> log method and result
failure or timeout -> offer other routes, resend or extend, then person
```

### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Every action's policy lists 2+ methods that need different abilities | Verification policy config | Config lint; test 1 |
| A person route exists on every check screen | Check renderer | Test 6 |
| Extension and resend never ask why | Code service | Test 3 |

### T3. Evals
- **Dataset:** 30 scripted check flows (blind, deaf, switch-input, memory-limited, slow typist) written with disabled testers, run on each method.
- **Judge rubric:** did the bot offer another route, avoid asking about disability, and keep context?
- **Release gate:** block a deploy if any check can't be completed by a route that needs a different ability.

### T5. Trade-offs
- More methods raise the attack surface; each must meet your security team's bar.
- Passkeys and codes need a phone or device; keep the person route for users with neither.
- Any access flag in logs is sensitive data; keep it opt-in and minimal.

---
### Deep dive
- **Open question.** I found no measurement of identity-check failure by disability in chat products.
- **Voice (PLANNED).** Voice-biometric and phone-verification checks are not written or measured here. The W3C note says voice-only authentication cannot serve deaf and hard of hearing users properly.
- **References.** [W3C, *Inaccessibility of CAPTCHA*, 2021](https://www.w3.org/TR/turingtest/) (opened); [W3C, *Understanding SC 3.3.8*](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html) (opened); [WebAIM Survey #10](https://webaim.org/projects/screenreadersurvey10/) (opened).
