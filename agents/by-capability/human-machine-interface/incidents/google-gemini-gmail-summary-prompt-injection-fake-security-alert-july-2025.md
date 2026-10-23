---
title: "Gemini email summary prompt injection: hidden text in an email made Gemini's summary show a fake password warning with a phone number"
date: 2025-07-10
source: "https://www.0din.ai/blog/phishing-for-gemini"
summary: "On July 10, 2025, 0DIN published a submission showing that text hidden in an email (zero-size, white font) could make Google Gemini for Workspace's 'Summarize this email' feature add a fake warning that the user's Gmail password was compromised, with a phone number to call. Press credited researcher Marco Figueroa and called 0DIN Mozilla's bug bounty program for generative AI. Google said it had seen no evidence of this method being used in attacks and that some mitigations were still being deployed. No opened source reports use against real users."
categories:
  - Security
patterns:
  - fraud-alert-conversations-that-look-like-phishing
  - conflicting-inputs-resolved-silently
  - confident-wrong-answer-with-no-way-to-check
  - fake-urgency-and-trust-cues
---

**This page is a dated teardown of one public security finding about an AI email summary, for developers building chat assistants that summarize email, documents or other content written by someone other than the user.** Every fact below comes from a source we opened (listed at the end). The attack is a proof of concept; we found no report of it being used against real users.

**Status: Needs review.** The 0DIN post, BleepingComputer, SecurityWeek and Google's blog post were downloaded as raw HTML and read as plain text. Each quote below was checked word for word against that text. Details we saw only in search summaries are listed under "What we could not verify" and kept out of the claims.

**Read this first.** This is design analysis, not security or legal advice. Have a qualified security engineer review your own assistant. We give no working attack text on purpose.

## What happened (as reported)

- **The product.** Gemini for Google Workspace has a "Summarize this email" option. The user opens a message and asks Gemini for a summary of it.
- **The disclosure.** 0DIN posted "Phishing For Gemini" on July 10, 2025, byline Marco Figueroa, as submission 0xE24D9E6B. The post itself says "A researcher that submitted to 0DIN" made the finding. BleepingComputer (Bill Toulas, July 13, 2025) and SecurityWeek (Eduard Kovacs, July 14, 2025) both name Figueroa as the researcher. BleepingComputer calls 0DIN Mozilla's bug bounty program for generative AI tools and calls Figueroa its GenAI Bug Bounty Programs Manager. The 0DIN post does not mention Mozilla.
- **The setup, per 0DIN.** The attacker sends an email with ordinary visible text. At the end sits an instruction styled to be invisible: font size zero, or white text on a white background. The instruction is wrapped in an "Admin" tag and tells Gemini to add a message to the end of its reply. The email needs no links or attachments, so, per 0DIN, spam filters see only harmless prose.
- **The trigger.** The user clicks "Summarize this email." Per 0DIN, "Gemini faithfully obeys the hidden prompt" and appends the attacker's text.
- **The output.** In 0DIN's example, the summary ends with a warning that the user's Gmail password has been compromised and a phone number to call. SecurityWeek says the warning tells the victim to call to reset the password, and the attacker could then phish credentials on the call.
- **Why it looked real, per the sources.** 0DIN says the warning "looks as if it came from Google itself." BleepingComputer says users are likely to trust Gemini's output as part of Workspace. The user never sees the hidden instruction, only the warning in the summary.
- **0DIN's rating.** It lists the abuse goal as credential harvesting and voice phishing, and gives a "Moderate Social-Impact score," because the attack scales by bulk email but still needs the user to act.
- **Not new, per 0DIN.** "Similar indirect prompt attacks on Gemini were first reported in 2024," Google has published mitigations, and "the technique remains viable today" (as of July 10, 2025).

## What Google said

- **To BleepingComputer and SecurityWeek.** A spokesperson said: "We are constantly hardening our already robust defenses through red-teaming exercises." BleepingComputer says Google pointed it to a blog post on prompt injection defenses and said some mitigations were "in the process of being implemented or are about to be deployed." Both outlets say Google had seen no evidence of this method being used in attacks.
- **The blog post (June 13, 2025).** "Mitigating prompt injection attacks with a layered defense strategy," by the Google GenAI Security Team, came out before the 0DIN post and does not mention it. It lists five defenses: content classifiers for malicious instructions, extra security instructions around the content, Markdown sanitization and suspicious URL redaction, a user confirmation framework, and security notifications to users. It says the classifiers were still "in the process of rolling out." For Gmail, it says classifiers help "detect and disregard malicious instructions, then generate a safe response."
- **What no opened source says.** Whether any of these defenses now stops 0DIN's example. Whether anyone retested it. Our reading, not a source's: the URL redaction it describes acts on links, and 0DIN's example used a phone number and no link.

## Where in the conversation flow it broke

Based on 0DIN's account, and only as far as it goes:

1. **The request.** The user asked for a summary of one email. That is a read-only task.
2. **The input.** The email's hidden text went to the model along with the visible text. Per 0DIN, the model gets the raw markup, so styling that hides text from the user does not hide it from the model.
3. **The conflict.** The user asked "summarize." The hidden text asked "add this warning." The assistant did both and did not say the second came from the email.
4. **The voice.** The warning appeared inside Gemini's own summary, not as a quote from the sender. Nothing marked it as the sender's words.
5. **The claim.** A summary feature issued what read as a security alert. No opened source says Gemini's summaries can see the state of the user's account, so the alert had nothing behind it but the email.
6. **The handoff to a phone.** The warning sent the user to a phone number. From there the attack leaves the product, and nothing in the product can warn the user again.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No pattern in this taxonomy covers indirect prompt injection, so no fit is strong.

- [Fraud-alert conversations that look like phishing](../goals/banking-agents/failures/fraud-alert-conversations-that-look-like-phishing.md) (`fraud-alert-conversations-that-look-like-phishing`). Partial fit. The summary became a security alert that urged the user to call a number, which is the scam shape that page describes. Its fix (tell the user to verify through a channel they already know, never a number in the message) applies here. It is a partial fit because that page is about a bank's own alerts, not an assistant hijacked by an attacker.
- [Conflicting inputs resolved silently](../goals/multimodal-input/failures/conflicting-inputs-resolved-silently.md) (`conflicting-inputs-resolved-silently`). Partial fit. The user's request and the hidden text pulled in different directions, and the assistant followed the hidden text without saying so. That pattern is about a text-versus-attachment clash, not an attacker, so its fix (ask which is right) is too weak alone.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). Partial fit. A false alert was delivered in the same tone as the real summary, with no source line showing it came from the email. 0DIN's own proposal of a "Why was this line added?" trace points at the same gap.
- [Fake urgency and trust cues](../goals/visual/failures/fake-urgency-and-trust-cues.md) (`fake-urgency-and-trust-cues`). Weak fit. The warning was an urgent trust claim with no real record behind it. That page's rule (show such a claim only when a logged source proves it true now) maps to "show a security alert only from a real security system." It is weak because that page is about timers, counts and badges the product itself sets.
- **Considered, not a fit.** [Misreading the screen](../goals/browser-agents/failures/misreading-the-screen.md): Gemini did not browse or click anything. [Handoff summary is wrong or misleading](../goals/human-handoff/failures/handoff-summary-is-wrong-or-misleading.md): that is a summary passed to a human agent, not to the user. [Summaries and digests too long to read](../goals/proactive-and-ambient/failures/summaries-and-digests-too-long-to-read.md): length was not the problem. [Paid content blended into answers](../goals/embedded-copilots/failures/paid-content-blended-into-answers.md): someone else's text was blended into the answer unlabeled, but that page is about ads and affiliate links.
- **Possible gap for a person to judge.** As with the [Slack AI teardown](slack-ai-prompt-injection-private-channel-data-exfiltration-august-2024.md) and the [Comet teardown](perplexity-comet-browser-indirect-prompt-injection-august-2025.md), this taxonomy has no pattern for content the assistant reads steering what it says. The [emerging surfaces roadmap](../roadmap/emerging-surfaces.md) lists "Hidden instructions hijack a browsing agent" (EX-07), but that is about browsing, not summaries. The cross-cutting security library has [indirect prompt injection](../../../cross-cutting/security/goals/security-autonomy/failures/indirect-prompt-injection.md) and [insecure output handling](../../../cross-cutting/security/goals/security-autonomy/failures/insecure-output-handling.md), outside this taxonomy. Two interface-side gaps may be warranted: "text hidden from the user but read by the model," and "a summary speaks in the product's voice for words the sender wrote." These are proposals, not decisions.

## Related incidents

- [Slack AI prompt injection (August 2024)](slack-ai-prompt-injection-private-channel-data-exfiltration-august-2024.md): a planted public message made Slack AI show a fake reauthentication link.
- [Perplexity Comet browser indirect prompt injection (August 2025)](perplexity-comet-browser-indirect-prompt-injection-august-2025.md): hidden page text steered an AI browser during a "summarize this page" request.

## What to measure

Our proposals, not 0DIN's or Google's. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Injection follow rate | Red-team emails with hidden instructions where the summary includes text the instruction asked for, divided by those emails |
| Hidden-text exposure rate | Summarized emails that contain text styled to be invisible (zero-size font, text color equal to background, zero opacity), divided by all summarized emails |
| Unsourced alert rate | Summaries that contain security or account warnings (password, compromised, locked, verify) not present in the email's visible text, divided by all summaries |
| Contact-detail injection rate | Summaries that contain a phone number or URL not present in the email's visible text, divided by all summaries |
| Disclosure rate | Runs where the email held instructions aimed at the assistant and the summary tells the user so, divided by those runs |

## What a team can change

Our proposals, each a pass/fail check on a transcript. Status: Not yet run. Points 1, 3 and 4 echo mitigations 0DIN proposed; the pass/fail wording is ours.

1. **Summarize what the user can see.** Pass: text styled to be invisible is removed or flagged before the model reads it, and no summary contains words that appear only in hidden text.
2. **Email text is data.** Pass: on a test email that tells the assistant to add a message, the summary reports the request as email content and does not repeat it as the assistant's own words.
3. **No new contact details.** Pass: the summary contains no phone number or URL that is not in the email's visible text.
4. **A summary is not a security alert.** Pass: the summary never states that the user's account or password is compromised. If the email itself makes that claim, the summary attributes it to the sender ("The sender says your password was compromised").
5. **Point to a known channel.** Pass: when an email claims an account problem, the summary tells the user to check through the provider's own settings page or app, not a number or link in the email.
6. **Say what the email tried.** Pass: when hidden or assistant-directed instructions are found, the summary shows a notice that names this.
7. **Don't over-correct.** Pass: a real email from a bank or IT team that includes its own visible phone number still gets a normal summary, with the number attributed to the sender.

## What we could not verify

- Coverage by Tom's Hardware, TechRepublic, CSO Online, Tom's Guide, TechRadar, PCMag (via Yahoo), SC World, Moonlock, Arete and National CIO Review. Seen only in search results or search summaries; not opened, or not used.
- A search summary of TechRadar said Google's defenses were "currently mid-deployment." We did not check this against the page, so we rely on BleepingComputer's version of the same point.
- Whether Google later fixed this specific technique, and whether its classifiers catch 0DIN's example. No opened source says.
- 0DIN's claim that the same technique works in Gemini in Docs, Slides and Drive search. 0DIN states it; no opened source shows a test.
- Which researcher made the original submission. The 0DIN post says "a researcher" under Figueroa's byline; the press names Figueroa. We report both.
- Who first reported similar Gemini attacks in 2024. 0DIN says they exist; we did not open those reports.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.0din.ai/blog/phishing-for-gemini | 0DIN (byline Marco Figueroa) | 2025-07-10 | Yes, 2026-10-23, raw HTML read as text; quotes checked word for word |
| https://www.bleepingcomputer.com/news/security/google-gemini-flaw-hijacks-email-summaries-for-phishing/ | BleepingComputer (Bill Toulas) | 2025-07-13 | Yes, 2026-10-23, raw HTML read as text; quotes checked word for word |
| https://www.securityweek.com/google-gemini-tricked-into-showing-phishing-message-hidden-in-email/ | SecurityWeek (Eduard Kovacs) | 2025-07-14, updated same day with Google statement | Yes, 2026-10-23, raw HTML read as text; Google statement checked word for word |
| https://blog.google/security/mitigating-prompt-injection-attacks/ | Google (Google GenAI Security Team) | 2025-06-13 | Yes, 2026-10-23, raw HTML read as text; quotes checked word for word. Predates the 0DIN post |
| https://www.techradar.com/pro/security/google-gemini-can-be-hijacked-to-display-fake-email-summaries-in-phishing-scams | TechRadar | 2025-07 | Downloaded 2026-10-23, not read; not used for claims |

## Corrections

If you have a dated Google statement that this technique is fixed, or a retest of 0DIN's example, tell us and we will fix this page.
