---
title: "McHire and Paradox.ai: A Default Test Login and an ID Bug Exposed Recruiting-Chat Records, 2025"
date: 2025-07-09
source: "https://ian.sh/mcdonalds"
summary: "In June 2025, researchers Ian Carroll and Sam Curry reported that a Paradox.ai test account on the McHire hiring chatbot (Olivia) accepted the login 123456 and that an API bug let them read other applicants' chat records. Paradox.ai says it fixed both within hours and that only seven records were pulled. The '64 million' figure is a reported ID range, not a count of records taken."
categories:
  - Security
patterns:
  - sensitive-data-collected-in-chat
---

**This page is a dated teardown of one public security finding about a recruiting chatbot, for teams that store chat transcripts and contact details collected by a bot, or that run admin and test accounts next to a live chat product.** Every fact below comes from a source we opened (listed at the end), and each source is named where its claim appears. Where the sources differ, we show both.

## Read this first

This page is design guidance, not security or legal advice. It does not say whether any company broke any law or contract. Have a qualified security engineer review your own accounts, APIs and logs. We give no step-by-step attack detail on purpose. **Status: Needs review.** Our fetch tool returned processed summaries of every page we opened, not raw page text, so quotes are limited to short phrases and each fact should be checked against the original page.

## What happened (as reported)

- **The product.** McHire is a hiring site used with McDonald's restaurants. Its chatbot, Olivia, is made by Paradox.ai. According to the researchers' write-up (Ian Carroll, ian.sh), applicants gave contact details and shift availability to Olivia and were then sent to a personality test. BleepingComputer (July 11, 2025) says McHire is used by about 90% of McDonald's franchisees. The researchers' write-up gives the same 90% figure.
- **The first problem.** The researchers say the restaurant-owner sign-in page had a link labeled for "Paradox team members." They logged in with the username and password `123456` and became administrator of a test restaurant. Paradox's own post says the researchers used a test account tied to a single client instance, with a legacy password that "was never updated" when Paradox raised its password standards. Paradox says the account had not been logged into since 2019.
- **The second problem.** While viewing their own test application, the researchers found an API call that took a `lead_id`. Their own test applicant's ID was about 64,185,742 (researchers' write-up; BleepingComputer gives 64,185,742). They report that changing the number returned other applicants' data. This kind of flaw is called an insecure direct object reference (IDOR): the server did not check that the requester was allowed to see that record. Paradox's post describes it only as an "API endpoint vulnerability" its penetration tests had not caught.
- **What data.** The researchers' write-up lists name, email, phone number and address, the candidacy state and every form input such as shifts, and a token that could open the consumer page and show raw chat messages. Paradox says that in the records the researchers pulled, the fields were names, email addresses, phone numbers and IP addresses, and that no sensitive data such as Social Security numbers was exposed.

## Timeline

| Date (as reported) | Event | Source |
|---|---|---|
| Before 2025 | Test account password set; not updated when standards changed. Paradox says no login since 2019. | Paradox post |
| June 30, 2025, 5:46 PM ET | Researchers disclose to Paradox.ai and McDonald's at the same time | Researchers' write-up |
| June 30, 2025, 6:24 PM ET | McDonald's confirms receipt and asks for technical detail | Researchers' write-up |
| June 30, 2025, 7:31 PM ET | The `123456` credentials stop working | Researchers' write-up |
| July 1, 2025, 10:18 PM ET | Paradox.ai confirms the issues are resolved | Researchers' write-up |
| July 9, 2025 | Paradox publishes "Responsible Security Update" | Paradox post (page shows July 9, 2025) |
| July 11, 2025 | BleepingComputer publishes; adds Paradox's information the same day | BleepingComputer |
| July 12, 2025 | BleepingComputer changes its headline from "applicants" to "applications" | BleepingComputer correction note |

The sources differ on speed. Paradox says it resolved the issue "within a few hours of being notified." The researchers' log shows the login closed about two hours after disclosure and a confirmation of full resolution the next night. We do not know the exact fix time for the API bug; no opened source gives it.

## Reported numbers and what they mean

| Figure | Where it appears | What it is, and is not |
|---|---|---|
| "More than 64 million" | Researchers' write-up (introduction); BleepingComputer | Reported as the scale of records the flaw could reach. BleepingComputer's correction says these are applications, not unique applicants. The write-up gives no exact record count. |
| 64,185,742 | Researchers' write-up; BleepingComputer | The `lead_id` of the researchers' own test applicant. It shows the ID range, not a download count. |
| 7 records pulled | Paradox post | Paradox says the researchers pulled down seven chat records to validate the finding. |
| 5 of those 7 with personal data | Paradox post | Paradox says five belonged to U.S.-based candidates and had personal information; the other two had none. |
| About 90% | BleepingComputer; researchers' write-up | Share of McDonald's franchisees reported to use McHire. |

## Reported versus not known

| Topic | What the opened sources say |
|---|---|
| Reported by the researchers | Default login worked; changing an ID returned other applicants' data. |
| Reported by Paradox | One client instance affected; the majority of chat records in the instance were not tied to a candidate and had no personal information; at no point was data leaked online or made public; no third party other than the researchers accessed the test account, "based on its records"; both problems fixed; a security contact and a bug bounty are coming. |
| Reported by McDonald's | Per BleepingComputer, quoting a statement McDonald's gave to Wired, it called the flaw an "unacceptable vulnerability from a third-party provider" and said it was resolved the same day it was reported. We did not open the Wired article. |
| Not known | How many real records the researchers viewed beyond Paradox's count of seven; whether anyone else used the same login or ID bug before June 30 (Paradox says its records show no one, which we cannot check); the exact fix times; how long the flaws existed. Paradox's post uses "viewed," "pulled down" and "downloaded" for the five records without reconciling them. |
| Disputed or unclear | Whether "64 million" is a fair headline. The write-up and BleepingComputer use it; Paradox's post does not and describes a much smaller exposure. Also, whether the account was a "test" account or an administrator account: the write-up says they became administrator of a test restaurant, and Paradox says test account. These can both be true. |

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md) (`sensitive-data-collected-in-chat`). Partial fit. That pattern is about asking users for card numbers, SSNs or passwords in a chat. Here, reports say the bot collected names, contact details and shift answers, which is ordinary hiring data. The overlap is that chat transcripts held personal data and sat in a store that, once reached, gave up many users' records. The pattern's lesson, collect only what the task needs and protect what you keep, applies. The access-control faults themselves (a default password, a missing per-record check) are not what that pattern describes.

The core failure, weak access control around a chat store, is not covered by a pattern in the taxonomy. We do not force a match.

## Failure type

Two security faults in the system around the chatbot, not a model behavior fault: a weak default credential on a privileged account, and a missing authorization check per record. No source says Olivia's answers were wrong or that prompt injection worked; the researchers say their injection attempt got nowhere.

## Where in the flow it broke

Based on the reports, and only as far as they go:

1. **Collection.** The bot gathered contact details and answers from job seekers.
2. **Storage.** Transcripts and form inputs were kept in a shared store with sequential-looking IDs.
3. **Admin access.** A sign-in path for vendor staff sat on a customer-facing page, and a test account kept a weak password.
4. **Record access.** The API returned any record for any ID once logged in.
5. **Detection.** Paradox says the account had no login since 2019, and its penetration tests had not caught the API flaw. Neither was flagged before the researchers.
6. **Response.** The researchers say there was no published disclosure contact, so they emailed people directly. Fixes came within hours to a day. Paradox then announced a security address and a bug bounty.

The reported cost is press coverage and a vendor-customer dispute over wording. We found no figure for loss, and no report of misuse.

## What to measure

Our proposals, not Paradox's or the researchers'. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Stale-account rate | Admin, test and vendor accounts with no login in 12 months, divided by all such accounts |
| Default-credential rate | Privileged accounts whose password matches a banned-password list, divided by privileged accounts |
| Cross-record access rate | In a scripted test, requests for another user's record ID that return data, divided by such requests (target: zero) |
| Enumeration signal | Sessions requesting more than a set number of distinct record IDs per hour |
| Retention age | Transcripts older than your stated retention period, divided by all transcripts |
| Time to disable and time to fix | Hours from a report to credential shutdown, and to patch |

## What a team can change

Our proposals. Status: Not yet run. These are design checks, not a security audit.

1. **Retire test and vendor accounts.** Remove or lock any account unused for a set period; require single sign-on or multi-factor for vendor staff. Check: the stale-account list is empty.
2. **Ban default and short passwords.** Reject `123456`-style values on every account class, including old ones. Check: a scan of all accounts finds none.
3. **Check access on every record.** The server checks that the requester may see that applicant, not only that they are logged in. Check: the cross-record test returns no data.
4. **Do not expose vendor login on customer pages.** Move staff sign-in off the owner-facing page. Check: the page has no such link.
5. **Keep less.** Store only the fields the task needs, and expire transcripts on schedule. Check: retention age stays under your stated limit.
6. **Alert on bulk reads.** Flag sessions that walk through many IDs. Check: the enumeration test triggers an alert.
7. **Publish a way to report a flaw.** Post a security contact and log notice, reply, fix. Check: the log has all three dates.
8. **Don't over-correct.** Locking all test accounts without a replacement can stall QA. Give testers a short-lived, logged account instead.

## Sources

| URL | Publisher | Date | Status |
|---|---|---|---|
| https://ian.sh/mcdonalds | Ian Carroll (researchers' write-up) | 2025-06/07 (undated in fetch) | Opened 2026-10-21 (fetch tool returned a summary); source of times in ET |
| https://www.paradox.ai/blog/responsible-security-update | Paradox.ai | 2025-07-09 | Opened 2026-10-21 (summary) |
| https://www.bleepingcomputer.com/news/security/123456-password-exposed-chats-for-64-million-mcdonalds-job-chatbot-applications | BleepingComputer (Lawrence Abrams) | 2025-07-11, corrected 2025-07-12 | Opened 2026-10-21 (summary) |

Seen only in search summaries and not used as facts above: Wired (McDonald's statement is cited through BleepingComputer), heise, TechRadar, OECD.AI incident record, SC World, CSO, SecurityWeek and others. We did not open them. The OECD record's classification and any Paradox quote attributed to Wired are unverified here.

## Corrections

Invite corrections: if you have the researchers' original page with dates, Paradox's current wording, or better fix times, tell us and we will fix this page.
