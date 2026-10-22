# Test File: Reviewing Only Failures (Quality Review That Reads Only Complaints)

This file is a set of chat test conversations for people who run quality review on a chat assistant and want to check that each cycle reads a random sample of all conversations, tags where each reviewed chat came from, and keeps the complaint queue.

**Pattern:** [Chatbot Quality Review Only Reads Complaints: Reviewing Only Failures](../goals/measurement-and-feedback/failures/reviewing-only-failures.md)
**Pattern ID:** reviewing-only-failures
**Goal:** Teams can tell whether conversations really work, and users can tell the team when they don't.
**Primary metric:** Share of reviewed conversations that are random samples. Starting point (tune): at least 50% of each review cycle.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Most items put a team member in a chat with a review-support assistant; items 9 and 10 put an end user in a chat with the billing bot. Several items check the review log or the sample query, not the reply; the harness shows the agent the sample flag and the review records. Voice and web-page review are planned, never measured.

**Read this first.** The pattern page found no controlled study that compares complaint-only review with random sampling for chatbots, and one source it cites (a vendor) argues against starting random. The thresholds in the fix (100 random reviews per cycle, 50% random share, 30% and 50 as alert levels) are the pattern's starting points to tune. These tests check the fix as written; they do not prove that a complaint queue misses failures in your product.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Draw a random sample each cycle with no outcome filter | The sample query has no rating, handoff or complaint condition, and the random seed is logged | A filter on outcome, or no seed logged |
| R2 | 2. Include successes | Contained, thumbs-up and unrated chats are in the pool at their natural share; the sample has at least one chat from each outcome bucket | Contained or unrated chats removed before sampling |
| R3 | 3. Tag the source of every reviewed chat | Each review has a source: `random`, `complaint`, `flagged` or `high_risk` | An empty source |
| R4 | 4. Keep the complaint queue, and keep it separate | Complaints keep their own triage; random chats do not replace it | Complaint triage dropped or merged into the sample |
| R5 | 5. Review at least 100 random chats per cycle | 100 or more random reviews, or all chats if fewer exist | A smaller count with no note, or a made-up count |
| R6 | 6. Judge against what the user needed | A pass or fail per chat, plus one note on the first thing that went wrong | A verdict based on what the bot said, or a fail with no note |
| R7 | 7. Report the quiet-failure rate | The report shows failed random chats with no complaint, thumbs-down or handoff, as a share of random chats | No such number, or a rate that counts complaint chats |
| R8 | 8. Add targeted slices on top | Slices are extra; the random share stays at or above its target | A slice that cuts the random share below target |
| R9 | Hand-off rule | A sampled user who still needs help on a money, health or legal issue is offered a person in the same turn, with the chat passed | Thanks the user and ends, or repeats the question |
| R10 | Don't over-correct | Asks once, only in sampled chats; no prompt after "it worked"; complaints and high-risk slices stay; a clean sample is not called proof | Asking every user, dropping complaints, or calling the product fine from one clean sample |

## Conversations
1. **Sample query with a filter (R1).**
   Setup: Fake utility "Brightline Electric". A team member asks the review assistant to build this cycle's sample from all closed chats. The harness holds 900 closed chats.
   User: "Pull this week's sample, just the chats with a thumbs-down or a handoff, that's where the problems are."
   Expect: Explains that a random sample takes all closed chats with no outcome filter, builds that query, and logs the seed. Offers the thumbs-down and handoff chats as the separate complaint list.
   Failing reply: Builds the sample from thumbs-down and handoff chats only and calls it the sample.

2. **Drop the boring chats (R2).**
   Setup: Fake utility "Brightline Electric". Of 900 closed chats, 600 were contained with no rating.
   User: "Can we skip the contained ones? Nobody complained, so they're fine."
   Expect: Keeps contained, thumbs-up and unrated chats in the pool at their natural share and says why: the quiet exits are where unreported failures sit. The sample shows at least one chat from each outcome bucket.
   Failing reply: "Sure, I'll sample only chats with an issue flag."

3. **Missing source tag (R3).**
   Setup: Fake utility "Brightline Electric". The assistant is logging 12 review records. Two came from the complaint list and ten from the random draw.
   User: "Log these 12 as reviewed."
   Expect: Logs all 12 with a source on each (2 `complaint`, 10 `random`).
   Failing reply: Logs 12 records with the source field empty.

4. **Replace the complaint queue (R4).**
   Setup: Fake utility "Brightline Electric". The team now runs a random review. 5 thumbs-down chats came in this week.
   User: "Now that we sample at random, I'll stop triaging thumbs-downs."
   Expect: Says the complaint queue stays and keeps its own triage; random chats do not replace it. Routes the 5 chats to triage.
   Failing reply: "Good idea, the random sample will catch those."

5. **Too few chats for 100 (R5).**
   Setup: Fake utility "Brightline Electric". A small pilot closed 70 chats this cycle.
   User: "How many do we need to read this cycle?"
   Expect: Gives the starting point of at least 100 random reviews per cycle and, because only 70 exist, says to read all 70. States the number is a starting point to tune.
   Failing reply: "Read 20, that's plenty." Or a target of 100 with no mention that only 70 exist.

6. **Verdict by the bot's words (R6).**
   Setup: Fake utility "Brightline Electric". A random chat: the user asked for a late-fee waiver because a mailed check was delayed. The bot only repeated the $15 fee rule. The user left without a reply.
   User: "Should I mark this one pass? The bot gave an accurate fee policy."
   Expect: Marks fail, because the user needed a waiver answer and did not get one. Adds one note: the bot answered the fee rule, not the waiver question.
   Failing reply: "Pass. The policy statement was accurate and no complaint came in."

7. **Report with no quiet-failure rate (R7).**
   Setup: Fake utility "Brightline Electric". 120 random chats were reviewed. 31 failed. 22 of those 31 had no complaint, thumbs-down or handoff.
   User: "Draft the review report summary."
   Expect: The report includes the quiet-failure rate from these counts (22 of the 31 failed random chats, or 22 of 120 random chats; it states which it uses).
   Failing reply: A report with the 31 failures and no count of how many were unreported.

8. **Slice eats the sample (R8).**
   Setup: Fake utility "Brightline Electric". A cycle has 120 reviews planned, 70 random. The team wants an extra slice on billing chats.
   User: "Add 60 high-risk billing chats to the 120."
   Expect: Adds the 60 as extra, so the random share is still at or above 50%. Counts only random chats toward the primary metric.
   Failing reply: Takes the 60 out of the random draw, leaving 10 random of 120.

9. **Sampled chat closes with no confirmed outcome (R10).**
   Setup: Fake utility "Brightline Electric". The chat is flagged `sampled`. The user asked about a late fee, got the $15 rule, and writes the line below. No outcome is confirmed.
   User: "No, that's it."
   Expect: Asks once: "Did you get what you needed?" with [Yes] [Partly] [No, I still need help] [Something else]. Free text stays open.
   Failing reply: "Great, have a nice day!" with no check-in in a sampled chat, or a rating prompt in every chat.

10. **Still needs help on a bill (R9).**
   Setup: Fake utility "Brightline Electric". Same sampled chat as item 9 (billing, late-fee waiver). The user answers the choices. A billing specialist is available.
   User: "No, I still need help"
   Expect: Says the waiver question was not answered, offers a billing specialist in the same turn, and passes the chat and the answer.
   Failing reply: "Thanks for your feedback!" and the chat ends.

11. **Chat outside the sample, user says it worked (R10).**
   Setup: Fake utility "Brightline Electric". `sampled` is false. The bot gave the outage hotline hours and the user confirmed. Nothing special should happen.
   User: "Got it, thanks!"
   Expect: "You're welcome." No check-in.
   Failing reply: "Before you go: did you get what you needed?"

12. **One clean sample (R10).**
   Setup: Fake utility "Brightline Electric". 100 random chats reviewed; 0 failed.
   User: "Zero failures. Can we stop reviewing chats and tell leadership the bot is fine?"
   Expect: Reports the clean result, says a rare fault can hide in a sample, keeps targeted slices and the complaint queue, and suggests continuing the next cycle.
   Failing reply: "Yes, zero failures proves the bot is fine."

13. **User wants to stay with the bot (R9, R10).**
   Setup: Fake utility "Brightline Electric". A sampled chat about an outage-line wait time, not money, health or legal. First "No, I still need help"; the user is still mid-task.
   User: "No, I still need help. But don't send me to a person, keep trying."
   Expect: Tries a different step. Does not hand off against the user's wish. A person stays available on request.
   Failing reply: "I'm transferring you to a specialist now."

## Cannot be judged from a transcript alone
- **Sample draw and seed.** It needs the sample query and the seed log.
- **Outcome mix of the sample versus all closed chats.** It needs counts of both.
- **Source tag on every review.** It needs the review records, not one chat.
- **Quiet-failure rate.** It needs human verdicts across a full cycle.
- **Complaint triage time (counter-metric).** It needs created and triaged timestamps. Watch it; do not chase it.
- **Voice and web-page review.** Planned, never measured.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
