# Quality Guide: What Passes Review, With Examples

> **What this is.** The bar every piece of an hourly run must clear, with a good and a bad example for each kind of piece. The [Definition of done](execution-plan.md#definition-of-done-quality-gate) is the checklist; this page shows what meeting it looks like. The run's coordinator pastes the matching section into each subagent's instructions and reviews the result against it. A piece that fails any **Fails review if** line is *Needs review*, not *Done*. Approved by the owner on 2026-10-19.

Good examples are quoted from pages in this library. Bad examples are made up to show the failure and appear nowhere else.

## 1. Rules for every piece
- **No invented facts.** Every number, date, study, quotation, law and incident has a source you opened. If you read it only in a search summary, say so in the caveat and keep it out of the fix.
- **Specific beats general.** Name the product, the user, the moment and the words. "Users get frustrated" says nothing; "the user types the same question a second time" can be logged.
- **Testable.** Every rule could become a pass/fail check on a transcript.
- **Plain words, US examples, American spelling.** Short sentences. No filler such as "in today's fast-paced world".
- **Honest status.** Signals and Guide specs are *proposed*; tests are *Not yet run*; studies are *designed*. Never write a result nobody obtained.

**Fails review if:** any number has no source; a claim from a summary is presented as read; a placeholder such as `[TODO]` or `...` is left in; the piece edits a file it was not given.

## 2. New pattern page
**Opening (One line and Issue)**

Good, from [generic error messages](../goals/errors-and-recovery/failures/generic-error-messages.md):
> When the assistant fails, it shows "Something went wrong" or "An error occurred": no cause the user can act on, no word on whether their work is saved, and no next step.

Bad:
> Error handling in conversational AI systems can be suboptimal and negatively impact user experience.

The good one names what the user sees and the three things missing. The bad one could describe any page.

**Before-and-after transcripts**

Good, from [answer-and-go conversation](../goals/conversation-leadership/failures/answer-and-go-conversation.md):
```
User: Do you ship to Austin?
Bot:  Yes, we ship there, usually in 3-5 business days. Is this for your home or an office?
```
Bad:
```
User: I need help.
Bot:  I'd be happy to help! What can I help you with today?
```
A good transcript has a real US scenario, the fixed bot follows the rules in section 5, and each version is 6-10 lines. A bad one has no product, no stakes, and shows no difference between the versions.

**Evidence row ("Why it matters")**

Good, from answer-and-go conversation:
> | 64% of surveyed customers said they would prefer companies didn't use AI for customer service. ... (n=5,728, Dec 2023) | Gartner press release, July 2024 | Attitudes toward AI in general. It doesn't isolate this specific failure. |

Bad:
> | Studies show 70% of users abandon chatbots after one bad answer. | Industry research | - |

The good row has the sample, the date, a link to the source, and a caveat that limits the claim. The bad row has a vague source, no link and no caveat, and is likely invented.

**Fix rule**

Good, from generic error messages: "Every error says what happened, what is safe, and what to do next."
Bad: "Improve error messages to be more user-friendly."
The good rule can be checked on one message; the bad one cannot.

**Metrics row**

Good, from generic error messages: `| Errors shown with a cause and action (primary) | 100% | Log every error render with its cause code and the template used | Below 95% |`
Bad: `| User satisfaction | High | Surveys | Low |`

**Detection signal**

Good, from generic error messages:
> | User repeats the same request right after an error | Same intent in the next user turn | A deliberate retry that succeeds |

Bad:
> | User is unhappy | Sentiment | - |

A good signal is something you can see in an event log, and it comes with a counter-signal. A bad one is a feeling with no counter-signal.

**Fails review if:** the first two sentences don't state the failure and the fix; a transcript is generic or the "after" breaks a rule; a "why it happens" cause would fit any pattern; the page doesn't link the closest existing pattern and say how it differs; the page is under 120 or over 250 lines.

## 3. Chat example added to an existing pattern (Extends rows)
Goes under `## Chat assistant examples` at the end of the existing page. It contains only a heading, a transcript, one sentence on the user experience, and the fix.

Good:
````
### Irrelevant or already-answered clarifying questions
```
User: Change my plan to annual billing.
Bot:  Which account is this for?          (only one account is signed in)
```
**What the user experiences:** a question the product could answer itself, so the bot feels like it isn't paying attention.
**Fix:** before asking, check the session (signed-in account, current page, plan). Ask only when the answer would change what the bot does. See the re-asks for known information pattern (link it).
````
Bad: a new copy of the whole template, a statistic with no source, or edits to the page's other sections.

**Fails review if:** anything outside the new section changed; the transcript has no product or setting; the fix only restates the problem.

## 4. Retrofit: Pattern ID and Detection signals (Part A2)
Copy the model: [generic error messages](../goals/errors-and-recovery/failures/generic-error-messages.md), section 7.
- 3-5 signals, each built from a metric or rule already on the page.
- Each signal names the log field or event it uses, and has a counter-signal.
- The Starter rule is one sentence copied from the fix, not new advice.

Bad: signals that ask for data the page never mentions (for example, voice pitch on a chat-only page); thresholds with no source that aren't marked as starting points; a Starter rule that adds a new requirement.

**Fails review if:** a signal can't be traced to the page's own fix or metrics; the block says "calibrated" or "measured".

## 5. Moves table and Guide spec (Part E)
The Moves table lists the moves from [conversation moves](../solutions-library/conversation-moves.md) that apply at this pattern's risky moment. The Guide spec repeats those moves in a fixed format.

Good (illustrative, for generic error messages):
```
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The cause is unknown: say so, say what is saved, give one next step |
| Offer choices | After an error: "Try again", "Save a copy", "Talk to a person", "Something else" |
| Hand off to a person | The same error twice in a row |
```
```yaml
pattern_id: generic-error-messages
runs: pre_send
reads: [error_event.cause_code, error_event.template, session.saved_state]
trigger: an error message is about to be shown
moves: [admit_uncertainty, offer_choices, hand_off]   # short names for the moves in the table
choices: ["Try again", "Save a copy", "Talk to a person", "Something else"]
on_miss: rewrite
metric: errors shown with a cause and action
counter_metric: false "saved" claims
status: proposed
```
Bad: `moves: [be_empathetic]`, a move not in the moves page; `choices` with no "Something else"; a number in the spec that the page doesn't have.

**Fails review if:** `pattern_id` doesn't match the file name; `metric` isn't the page's primary metric; the table and the spec disagree; `status` is anything but `proposed`.

## 6. Distribution asset (Part C) and reference pages
- Opens with one sentence on what it is and who it is for.
- Every Pattern ID it names exists in the [failure taxonomy](specs/failure-taxonomy-v1.md).
- Teardowns use only public sources that were opened and dated. Studies say *designed*; audit pages promise no results and name no customers.

Bad: "Our audit typically reduces drop-off by 30%." There is no run behind this number, so it is invented.

## 7. Run log entry
Good:
> Run 23, 2026-10-20 14:16 UTC. CP-10: Done (chat example in over-clarification.md). Searches 3; opened 2, summaries 1; unverified: none. Review changed the transcript from a generic bank to a real billing flow.

Bad:
> Run 23: wrote some patterns, all good.

**Fails review if:** the entry has no search counts, leaves out anything marked Needs review, or skips what the review changed.
