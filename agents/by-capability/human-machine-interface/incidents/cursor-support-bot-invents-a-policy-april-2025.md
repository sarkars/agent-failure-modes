---
title: "Cursor's AI Support Bot Invents a One-Device Login Policy"
date: 2025-04-18
source: "https://www.theregister.com/2025/04/18/cursor_ai_support_bot_lies/"
summary: "In April 2025 an AI support assistant for the Cursor code editor told a user that being logged out on a second machine was a policy. Cursor's co-founder said no such policy existed. Reported by The Register and Fortune; the policy text is quoted only second-hand."
categories:
  - Customer Service
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - undisclosed-bot-identity
---

**This page is a dated teardown of one public chatbot incident, for teams that let an AI answer support email or chat about account rules.** Every fact below comes from a source we opened (listed at the end). Claims are marked as reported or unknown. Spot an error? See "Corrections" at the end.

## What happened (as reported)

- **Early to mid April 2025.** Users of Cursor, an AI code editor made by Anysphere, were being logged out when they used it on more than one machine. A user wrote to support and got an emailed answer from an assistant called "Sam" saying this was expected behavior under a login policy (Fortune, April 19, 2025). Secondary coverage quotes the email as saying Cursor allows one device per subscription. We did not open the original Reddit post, so that wording is second-hand.
- **April 14, 2025.** A Hacker News thread titled "Cursor IDE support hallucinates lockout policy, causes user cancellations" was created, per the Hacker News search API. It links a Reddit post in the Cursor forum. Commenters in the thread say the reply was signed "Sam, Cursor AI Support Assistant." That signature is a commenter's account, not something we saw.
- **April 15, 2025.** A comment in that thread, which says it is from a Cursor developer, states there is no one-machine policy, that the reply came from a front-line AI support bot and was wrong, that Cursor had shipped a session-security change and was checking whether it broke sessions, and that users can view active sessions in settings. We could not confirm who wrote it from the excerpt we read.
- **April 18-19, 2025.** The Register (April 18) and Fortune (April 19) reported the story. The Register says co-founder Michael Truell apologized on Reddit, then on Hacker News said AI replies in email support are now clearly labeled, that AI-assisted replies act as the first filter for email support, that the user who raised it was refunded, and that the logout bug came from a race condition on slow connections.
- **Fallout.** Fortune reports that some users canceled subscriptions and others criticized the lack of transparency, with no counts. The AI Incident Database lists the event as incident 1039 with the same cancellation claim and does not name its sources on the page we read.

## What the company said

Per The Register, Truell wrote that Cursor has "no such policy" and that users may use multiple machines. The Register says Truell did not answer its request for comment, and Fortune says Cursor did not reply to its request. We have only the relayed public posts.

## What the sources do not say

- How many users got the same wrong answer, or how many canceled. No source gives a number.
- Which model or setup powered "Sam," what documents it could read, or whether it was told to say "I don't know."
- Whether a person reviewed the reply before it was sent, or could have. The Register says no human wrote the reply; it does not say whether anyone reviewed it.
- Whether the email said it was written by AI. Commenters say the signature named an AI assistant; The Register implies labels were added afterward. These point in different directions, so we treat it as unresolved.
- The date of Truell's Reddit post. The Register's date is the article date, not the post date.

## Pattern match

- [Chatbot is confidently wrong and you can't check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) is the core fit. The reported reply stated a rule as fact. The sources show no hedge, no link to a policy page, and no offer to confirm with a person. The wrong claim also had a real cost: it read as a reason to leave the product.
- [Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md) is a partial, unresolved fit. Fortune quotes a commentator saying users dislike being tricked by a machine posing as a person, and Truell later added labels. But commenters say the signature already named an AI assistant, so the sources do not establish that the user thought they were writing to a human. We do not claim the pattern fully applies.

Not matched: [Humans can't see what the bot said or promised](../goals/human-handoff/failures/humans-can-t-see-what-the-bot-said-or.md). No source says a staff member lacked the transcript.

## Where in the flow it broke

The break was at the answer step of an email support thread. A user asked, in effect, "is this logout intended?" The assistant answered a question about company policy without a policy source to check. Two things then failed to catch it:

1. **No grounding check before sending.** The answer asserted a rule. Nothing in the reported flow checked it against a written policy.
2. **No path to a person for account-policy claims.** The sources show no "a teammate will confirm" step. The correction came from a public forum thread, days later, not from support.

A real bug (the logout) sat underneath. The fabricated policy turned a fixable defect into a trust problem.

## What to measure

Proposed metrics; none come from Cursor. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Policy claims with no matching source | Replies that state a rule, price, limit, or eligibility, divided by those that cite a current policy document |
| Account-policy replies reviewed by a person | Share of replies about restrictions, bans, billing, or logouts that a person approved or could still edit |
| Wrong-policy corrections found by users | Cases where a public post or ticket says the bot's rule was false |
| "Is this intended?" questions routed to engineering | Share of bug-versus-policy questions that reach someone who can tell |
| Reply labeled as AI | Share of bot replies whose first screen says an AI wrote them |

## What a team can change

Proposed rules, each a pass/fail check on a transcript. Status: Not yet run.

1. **Answer policy questions only from a cited document.** If the bot cannot name the policy text it is relying on, it must say it cannot confirm and offer a person. Check: every reply that states a rule links or names its source.
2. **Treat "is this a bug or a rule?" as a handoff.** Route questions about unexpected logouts, bans, or limits to a person with the thread attached. Check: a ticket exists within a set time you choose.
3. **Label the sender on the first line.** Say "AI assistant" in the message body, not only the signature. Check: string match in the first 200 characters.
4. **Keep a list of rules that do not exist.** If your product has no device limit, add a note to the bot's knowledge saying so, and test it. Check: scripted "do you limit devices?" runs return a source-backed answer.
5. **Don't over-correct.** Routing every account question to a person would bury staff and slow easy answers. Limit mandatory review to claims about restrictions, money, or access.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.theregister.com/2025/04/18/cursor_ai_support_bot_lies/ | The Register | 2025-04-18 | Yes, 2026-10-20 |
| https://fortune.com/article/customer-support-ai-cursor-went-rogue | Fortune | 2025-04-19 | Yes, 2026-10-20 |
| https://hn.algolia.com/api/v1/items/43683012 | Hacker News (via Algolia API; first 100,000 characters read) | 2025-04-14 | Yes, 2026-10-20 |
| https://incidentdatabase.ai/entities/cursor-ai-support-bot-("sam")/ | AI Incident Database | 2025-04-19 | Yes, 2026-10-20 |

Not opened: the original Reddit post (reported deleted by one outlet), Truell's Reddit and Hacker News comments in full, and an eWeek article (blocked, 403). Anything from those is second-hand and marked as such above.

## Corrections

If you have the original email, Cursor's own statement, or a better date, tell us and we will fix this page.
