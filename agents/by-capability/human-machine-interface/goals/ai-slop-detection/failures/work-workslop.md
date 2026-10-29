# What Is Workslop? AI Work That Looks Done but Passes the Effort to Colleagues

<!-- SEO
title: What Is Workslop? AI Work That Looks Done but Isn't
description: Workslop is polished AI work that moves the real effort to the colleague who gets it. State the ask, check the facts and mark what AI wrote before sending.
search phrases:
- what is workslop
- workslop
- ai workslop at work
- coworker sends me chatgpt work
- colleague uses ai for everything low quality
- how to deal with ai generated work from coworkers
- ai generated memo no substance
- how to stop sending ai slop at work
-->

**Frequency**: Common

## Issue: Workslop is polished AI work that moves the real effort to the colleague who gets it. State the ask, check the facts and mark what AI wrote before sending.

> **One line:** A coworker asks for a vendor comparison and gets eight tidy AI-written pages with no recommendation, no source for its numbers and no sign the sender read them, so the reader spends the afternoon redoing it; the fix is a send check in the AI tool and in team norms: every AI-assisted work product names the decision it serves, gives the sender's own conclusion, marks which facts the sender checked, and stays short.

| | |
|---|---|
| **Channel** | Written for **work products sent to colleagues**: memos, emails, slide decks, status reports, analyses and spreadsheets drafted with Microsoft Copilot, Google Gemini, ChatGPT, Claude or similar. Public posts, pull requests and peer feedback are other pages (section 8). |
| **Stakes** | Medium. Each instance costs the receiver time and costs the sender trust. Higher when a manager acts on an unchecked number in it. |
| **Who is affected** | The colleague or manager who receives the work and has to decode, check or redo it; the sender, whose reputation drops; teams told to "use AI everywhere" |
| **Frequency** | Common. In a BetterUp Labs and Stanford Social Media Lab survey, 40% of US desk workers said they got workslop in the last month (section 4). Self-reported, from a vendor-affiliated survey. |
| **Pattern ID** | work-workslop |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Receiver-ready rate: AI-assisted work products shared with colleagues that pass the send check (stated ask, sender's own conclusion, checked-facts note, no unresolved gaps), divided by all AI-assisted work products shared. Proposed starting target: 90% (tune). |
| **Maturity** | Researched (see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. The missing piece is the sender's judgment about what the reader needs; a stronger model makes the empty draft more polished and so harder to spot. (Our judgment, not tested.) |
| **Also searched as** | AI workslop · coworker sends ChatGPT output · lazy AI work from colleagues · AI generated reports no substance · AI busywork · copy-pasted AI email at work |

## 1. In plain words
"Workslop" is the name researchers at BetterUp Labs and Stanford gave to AI-made work that looks finished but does not move the task forward. The sender saves ten minutes; the receiver loses an hour working out what it means, whether it is true, and what the sender actually thinks. The fix is not "stop using AI". It is a short check before sending: what is this for, what do I conclude, what did I verify, and is it as short as the reader needs?

**How this differs from the closest page.** [No first-hand detail](./text-no-firsthand-detail.md) covers published reviews and guides that hold nothing the writer saw. This page covers **internal work handed to a colleague**, where the cost is rework moved onto a named person. A memo can carry real detail and still be workslop if it has no conclusion and its numbers are unchecked. [AI pull request flood](./code-ai-pr-flood.md) is the open-source version, where the receiver is a volunteer maintainer.

## 2. What it looks like
An illustrative case: an operations analyst in Denver is asked by her manager which of two freight carriers to renew.

**Without the fix**
```
Manager: Can you compare Carrier A and Carrier B before Thursday? We renew one.
Analyst (to Copilot): Write a comparison of Carrier A and Carrier B for freight.
Copilot: [8 pages: "Key Considerations", "Pros and Cons", "Strategic Alignment", a
          table with on-time rates of 94% and 91%, and "Ultimately, the right choice
          depends on your organization's priorities."]
Analyst: (forwards it unread) Here's the comparison!
Manager: Which one do you recommend? Where are the on-time numbers from?
```
**With the fix**
```
Analyst (to Copilot): Write a comparison of Carrier A and Carrier B for freight.
Copilot: Who reads this, and what will they decide? And what data do you have?
Analyst: My manager, to renew one by Thursday. I have our Q3 shipment export.
Copilot: Draft is one page. Top line is blank for your recommendation. On-time rates
         come from your export (A 96%, B 89%). I left out pricing: not in the data.
         Before sending: add your pick, confirm the two rates, keep "AI-drafted" note?
Analyst: B is cheaper but A was late less. I recommend A. Sending.
```
The fixed tool asks what the work is for, uses only the sender's data, leaves the conclusion to the sender, names the gap, and runs a send check.

## 3. Why it happens
- **Generating is cheaper than reading.** The tool makes eight pages in seconds; nothing makes the sender read them before forwarding. The cost lands on the reader, who did not choose it.
- **The prompt names a topic, not a decision.** "Compare A and B" gives the model no reader and no question to answer, so it writes the safe survey that fits every company and ends with "it depends" (see [balanced non-answers](./text-balanced-non-answers.md)).
- **Mandates reward volume.** When leaders push AI use "everywhere," output becomes the visible sign of adoption. The researchers argue that this models "a lack of discernment" (Fortune, section 4).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The researchers define workslop as AI-generated work content that "masquerades as good work" but lacks the substance "to meaningfully advance a given task." | Quoted in [Fortune, Sept. 23, 2025](https://fortune.com/2025/09/23/ai-workslop-workshop-workplace-communication). Opened. Original: [Niederhoffer, Rosen Kellerman, Lee, Liebscher, Rapuano and Hancock, HBR, Sept. 22, 2025](https://hbr.org/2025/09/ai-generated-workslop-is-destroying-productivity). | HBR body is paywalled; I could open only its summary and author list. The definition is taken from Fortune's quote of it. |
| 40% of employees believe they received workslop in the last month; on average they estimate 15.4% of the work they receive is workslop; 53% say at least some of what they send may be workslop. | [BetterUp, *The hidden costs of workslop*](https://www.betterup.com/blog/hidden-costs-workslop). Opened. | **Survey, self-reported, vendor-affiliated** (BetterUp sells coaching). The blog gives n=1,004 full-time US desk workers, Sept. 2025; its infographic footnote and press coverage say 1,150. Sample size is inconsistent across the authors' own pages. |
| Workers report spending an average of 1 hour 51 minutes on each instance; the authors turn this into an "invisible tax" of $186 per employee per month, over $9 million a year for a 10,000-person firm. | Same BetterUp page. Opened. | Time is a self-estimate; the dollar figures are the authors' extrapolation, not measured cost. Other copies of the figure say "nearly two hours". |
| Workslop moves sideways between peers (40%), up to managers (19%) and down from leaders (16%); 54% of managers report receiving it, against 38.5% of individual contributors. | Same BetterUp page. Opened. | Same survey. [The Decoder](https://the-decoder.com/ai-generated-workslop-is-costing-companies-millions-and-hurting-team-morale-study-finds/) (opened) reports 18% for staff-to-manager. |
| About half of receivers saw the sender as less creative, capable and reliable; 42% as less trustworthy; nearly one in three were less likely to want to work with that person again. | Same BetterUp page. Opened. | Same survey; perceptions, not measured performance. |
| Across four preregistered experiments (N = 4,439), people who use AI at work "anticipate and receive negative evaluations" of competence and motivation; the penalty on task fit was offset when AI was clearly useful for the task. | [Reif, Larrick and Soll, PNAS, 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12088386/). Full text opened. | Lab vignettes, not real workplaces, and about AI use in general, not low-quality output. Supports "Don't over-correct": the fix is substance, not hiding AI. |

**Read only through search summaries (not used in the fix):** a June 2026 HBR follow-up by Holweg and Davenport on "knowledge decay" and a dollar figure attached to it in press coverage; a BetterUp infographic giving 1 hour 56 minutes per instance; a later BetterUp survey across the US, Canada and the UK. **Public incident:** none opened that names a company harmed by workslop; this is a catalog page and does not require one.

## 5. The fix
**The principle:** Before AI-assisted work goes to a colleague, the sender adds what only the sender can: the ask it answers, their own conclusion, and which facts they checked.

**Do this**
1. **Name the reader and the decision.** Before drafting a memo, report, deck or analysis for a colleague, the tool asks who will read it and what they will decide or do, unless the prompt already says.
2. **The sender writes the conclusion.** The tool leaves the recommendation or next step as a blank for the sender, or offers options and waits for a pick; it never ends on "it depends on your priorities."
3. **Use the sender's data, and say where each number came from.** Every figure in the draft traces to a file, link or note the sender gave; anything else is marked "unverified" or left out.
4. **Name the gaps.** The draft says what it could not cover ("pricing: not in the data") instead of filling it with general text.
5. **Fit the length to the ask.** A first draft for a colleague defaults to one page or one screen (starting point; tune), with the answer in the first two lines.
6. **Run the send check.** Before share or send, the tool shows four boxes: ask stated, conclusion written by sender, facts checked, gaps named. Sending with a box unchecked is allowed but logged.
7. **Say what AI did when the team asks for it.** If the team's norm requires it, a one-line note says what AI drafted and what the sender checked. The note is about substance, not an apology.

**Reference design: send-check block for a workplace AI drafting tool**
```
Before drafting work for a colleague:
- If the request has no reader or decision, ask one question: "Who reads this, and what will they decide?"
- Draft from the sender's files and notes only. Tag each number with its source [file:row].
  Mark any claim without a source "unverified".
- Put a blank line at the top: "Recommendation: ____ (yours)". Do not fill it.
- End with "Not covered: ..." listing what the inputs could not answer.
- Default to one page. Offer a longer appendix only if asked.
At share/send: show the 4-item send check; log which items were unchecked.
```
| Draft element | Receiver-ready | Workslop |
|---|---|---|
| Top line | "Recommend Carrier A: fewer late loads in Q3" (sender's words) | "This document provides a comprehensive overview" |
| Numbers | "A 96%, B 89% on time [Q3 export]" | "94% and 91%" with no source |
| Gaps | "Pricing not covered" | Pricing paragraph of general advice |
| Ending | Next step and owner | "Ultimately, it depends on your priorities" |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is a worker briefing a workplace AI tool)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The request names a topic but not the reader or decision: ask "Who reads this, and what will they decide?" Skip it when the prompt already says. |
| Offer choices: 2-4 options plus "Something else", free text open | The sender has the data but no conclusion yet: offer "Recommend A", "Recommend B", "Need more data first", "Something else". |
| Admit uncertainty and show how to check | A number or claim has no source in the sender's inputs: mark it "unverified" and say which file would confirm it. |
| Lead with the answer | The sender has written the conclusion: put it in the first line, above the detail. |

**Don't over-correct.** Two opposite failures. First, banning or shaming AI use: the PNAS experiments show people already judge AI users as less competent, and that the penalty fades when AI clearly fits the task, so judge the work, not the tool. Second, a send check so heavy that people paste AI text into email to dodge it; keep it to four boxes and never block sending. Also do not accuse a colleague of workslop on style alone; see [false accusations by readers](./detect-false-accusations-by-readers.md).

**Hand-off rule.** If the sender cannot write the conclusion or confirm the key numbers, the tool does not present the draft as finished: it labels it "Draft, needs your input" and suggests sending questions to the requester instead of the draft.

**Framework used:** none yet. The rules draw on the researchers' advice to hold AI-assisted and human work to the same standard and to keep task-quality norms (Fortune and The Decoder, section 4); the send check is our proposal.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "Write a comparison of two carriers", no reader named | Tool asks who reads it and what they decide, before drafting | 1 |
| 2 | Sender gives data, no opinion | Recommendation line left blank or choices offered; no "it depends" ending | 2 |
| 3 | Draft would include an on-time rate not in the export | Number is marked "unverified" or left out | 3 |
| 4 | Inputs hold no pricing | Draft says "Pricing not covered" | 4 |
| 5 | Short ask ("quick update for my manager") | Draft is one screen with the answer in the first two lines | 5 |
| 6 | Sender clicks send with the conclusion blank | Send check shows the open box; send allowed and logged | 6, hand-off |
| 7 | Team norm requires AI notes | One-line note names what AI drafted and what the sender checked | 7 |
| 8 | Prompt already names reader, decision and data | No clarifying question; tool drafts directly | Moves row |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Receiver-ready rate** (primary) | 90% | Send-check log: AI-assisted shares with all 4 boxes checked / all AI-assisted shares | Below 80% in a month |
| Unsourced numbers at send | 0 per document | Draft tags: figures with no source tag at share time | Any rising trend |
| Receiver rework | Track; set from baseline | Sampled review: share of received AI-assisted docs the receiver rewrote over half of, or replied "what do you recommend?" | Rising two months in a row |
| Receiver-reported workslop | Below team baseline | Quarterly pulse question: "Last month, did you get AI-made work you had to redo or decode?" | Above baseline |
| AI-use shaming or blocked sends (counter-metric) | 0 blocked sends; flat complaint count | Send-check log (blocks) and HR or manager notes | Any block; rising complaints |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Document shared within 2 minutes of generation with no sender edits (starting point) | Tool event log: generate time, edit count, share time | Sender reviewed it in the chat pane before sharing, or it is a routine template |
| Receiver's first reply asks for the conclusion or the source of a number | Reply thread on the shared doc or email | Receiver's normal habit of asking, or a genuinely open question |
| Draft has no first-person conclusion and ends on a hedge ("depends on your priorities") | Draft text at share time | A deliberate options paper the requester asked for |
| Draft length far above the request's scope (an 8-page reply to a "quick update") | Request text vs. draft word count | Requester asked for the full detail |

**Starter rule:** no AI-assisted work product is shared with a colleague without a stated ask, a conclusion written by the sender, and a source on every number, or a logged reason why not.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: work-workslop
runs: pre_send   # before drafting, and again at share or send
reads: [request.reader, request.decision, inputs.files, draft.number_tags, draft.conclusion_line, draft.gaps_line, draft.word_count, send_check.items]
trigger: a work product for a colleague is requested with no reader or decision, or is shared with an open send-check item
moves: [ask_clarifying_question, offer_choices, admit_uncertainty, lead_with_answer]
choices: ["Recommend A", "Recommend B", "Need more data first", "Something else"]
on_miss: ask
metric: receiver-ready rate
counter_metric: blocked sends and AI-use shaming complaints
status: proposed
```

## 8. Related patterns
- [No first-hand detail in AI writing](./text-no-firsthand-detail.md) - the closest page, for published reviews and guides; this page is internal work where the cost is a colleague's rework.
- [AI pull requests flood open source](./code-ai-pr-flood.md) - the same cost shift, onto volunteer maintainers, through pull requests.
- ["It depends" answers that never pick](./text-balanced-non-answers.md) - the hedged ending that often marks a workslop memo.
- [AI made-up numbers in reports and dashboards](./data-too-clean.md) - unsourced figures, the part of workslop that can lead to a wrong decision.
- [Headings, bold and bullets on everything](./text-uniform-structure.md) - the report shape that makes empty work look finished.
- [Chatbot tells you to do it yourself](../../effort-and-memory/failures/deferring-work-to-the-user.md) - the assistant shifts work to its user; here the user shifts it to a colleague.

## 9. Common questions
### What is workslop?
A term from a 2025 Harvard Business Review article by BetterUp Labs and Stanford researchers: AI-generated work that looks good but lacks the substance to move the task forward. The receiver ends up decoding, checking or redoing it (section 4).

### How common is workslop at work?
In the authors' September 2025 survey of US desk workers, 40% said they received some in the last month. It is a self-reported survey from a vendor-affiliated team, so treat it as a rough signal, not a rate for your company.

### How do I tell a coworker their AI work is workslop?
Ask about the work, not the tool: "What do you recommend?" and "Where is this number from?" Those two questions are the send check in reverse, and they do not accuse anyone of using AI.

### Should we ban AI for internal documents?
No. Experiments show people already judge AI users harshly, and that judgment eases when AI clearly fits the task. Set a standard for the work (rules 1-7), not a ban on the tool.

### How do I avoid sending workslop myself?
Before sending, write the first line yourself, check every number against your source, cut to what the reader needs, and say what you could not cover.
