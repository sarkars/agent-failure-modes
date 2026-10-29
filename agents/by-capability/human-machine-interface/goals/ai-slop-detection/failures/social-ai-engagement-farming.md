# AI Comments on LinkedIn ("Great Insights, Thanks for Sharing!"): Engagement Farming With Comment Bots

<!-- SEO
title: AI Comments on LinkedIn: Engagement Farming With Comment Bots
description: AI comment tools post generic "Great insights!" replies on LinkedIn to farm reach. Draft, never auto-post, require the user's edit, and filter repeats.
search phrases:
- ai generated comments on linkedin
- how to spot ai comments on linkedin
- linkedin comment bot great insights thanks for sharing
- is it against linkedin rules to use ai to comment
- linkedin automated comments most relevant hidden
- ai linkedin comment generator chrome extension
- why are linkedin comments so generic
- linkedin engagement pods ai comments
-->

**Frequency**: Common

## Issue: AI comment tools post generic "Great insights!" replies on LinkedIn to farm reach. Draft, never auto-post, require the user's edit, and filter repeats.

> **One line:** A browser extension or "AI commenter" writes "Great insights, Maria! Thanks for sharing." under dozens of posts a day so its user gets seen, and creators and readers learn to skip the whole comment section; the fix is a comment assistant that only drafts, never posts, refuses to enable Post until the user adds something of their own, plus platform and creator filters for comments that say nothing about the post.

> **Read this first:** This page quotes LinkedIn's own User Agreement and help pages as far as I read them. It is design guidance, not legal advice or a reading of any platform's terms for your case. Have a qualified person review how your product touches a platform's automation rules. **Status: Needs review.**

| | |
|---|---|
| **Channel** | Written: comments and replies on professional networks (LinkedIn first), drafted by browser extensions, "AI commenter" apps and agents. Other networks and DM bots are PLANNED, not written. |
| **Stakes** | Medium. For the commenter, LinkedIn says detected automated comments may be hidden from "Most Relevant" and accounts may be restricted (section 4). For the creator, real replies get buried under filler. For the builder, the product's core feature can break the platform's rules. |
| **Who is affected** | Creators whose comment sections fill with filler; readers who use comments to judge a post; the commenter whose name is on a reply they did not write; the team building the comment assistant |
| **Frequency** | Common, in our judgment. I found no opened source that counts AI comments; the one count I opened covers long LinkedIn posts, not comments (section 4). |
| **Pattern ID** | social-ai-engagement-farming |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Owned-comment rate: comments posted from the assistant's drafts where the user changed or added at least one sentence and the posted text names a detail from the post, divided by all comments posted from drafts. Proposed starting target: 95% (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A stronger model writes filler that sounds more specific, which makes it harder to spot, not less farmed; the fix is product design (no auto-post, required edit) and platform signals that use timing and repetition. (Our judgment, not tested.) |
| **Also searched as** | LinkedIn AI comments · bot comments on my LinkedIn post · auto comment LinkedIn · LinkedIn comment automation · fake engagement LinkedIn · AI reply guy |

## 1. In plain words
Comment tools promise reach: comment on many posts, get seen by many people. The cheapest way to do that is a one-click or no-click comment that fits any post: "Great insights!", "So true, thanks for sharing", "This is a game-changer." The creator gets a pile of replies that prove nobody read the post. The builder can stop this in the product: write a draft, keep the Post button off until the user says what they think, and never post on their behalf.

## 2. What it looks like
**Without the fix**
```
Maria (CFO, Phoenix hospital) posts: Prior auth delays cost us 11 days on average for MRI orders last quarter.
AI commenter (auto mode, for Jake, sales rep, Chicago):
  "Great insights, Maria! Thanks for sharing this valuable perspective. Healthcare is evolving fast!"
  (Same tool posts 38 more comments for Jake today, all opening "Great insights")
Maria's comment section: 14 of 20 comments open with "Great insights" or "Thanks for sharing".
Maria: replies to none of them.
```
**With the fix**
```
Jake clicks "Draft comment" under Maria's post.
Assistant: Draft: "11 days for MRI orders is longer than I expected." I can't add more without you.
           What do you know about this? Pick one or type your own:
           [I've seen this at a client] [I have a question for Maria] [I disagree with something] [Something else]
Jake: A clinic I work with in Tempe cut it by sending clinical notes with the first request.
Assistant: Updated draft with your point. Post is on; you send it. (Your edit: 1 sentence added.)
Jake posts it. Maria replies: "Which notes? We send them on resubmission only."
```
The fixed tool drafts but does not post, asks for the one thing only Jake knows, and turns Post on only after his sentence is in.

## 3. Why it happens
- **The tool is sold on volume.** Comment tools advertise how many comments you can make in a day; the extension I opened gives free users 3 a day and sells unlimited (section 4). A comment that fits any post is the fastest way to fill that number. (Our reading.)
- **The model has the post, not the user's experience.** The tool sees Maria's text but knows nothing Jake saw or did, so the safe output is praise or a restatement, the same gap as [no first-hand detail](./text-no-firsthand-detail.md).
- **Comments are a ranking input people try to game.** LinkedIn treats pods and automated comments as a reach problem it has to counter (section 4), which tells us commenting is used to buy visibility.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| LinkedIn defines automated comments as "comments posted to LinkedIn using a browser extension, script, or third party tool" and says they "aren't allowed on LinkedIn"; it may not show detected ones in "Most Relevant" and may restrict a member's use of LinkedIn. It says engagement pods are "not allowed" and that it has removed groups showing pod behavior. | [LinkedIn, *What We're Doing to Support Authentic Content and Conversations on LinkedIn*, Mar. 13, 2026](https://news.linkedin.com/2026/authentic-content-and-conversations). Opened. | Platform statement; it does not mention AI-drafted comments a person reviews and posts, so it does not settle whether this page's fixed design is allowed. No enforcement numbers. |
| LinkedIn's help page says "if we detect excessive comment creation or use of an automation tool, we may limit the visibility of those comments" and that it may limit how many comments a member or Page can make in a period. | [LinkedIn Help, answer 3068](https://www.linkedin.com/help/linkedin/answer/3068). Opened. Reported as new wording by [Social Media Today, Aug. 20, 2025](https://www.socialmediatoday.com/news/linkedin-limit-visibility-of-comments-made-via-automation-tools/758207/), opened. | Help text, no thresholds given. The 2025 date of the change comes from the trade press article. |
| The User Agreement's "Don'ts" bar using "bots or other unauthorized automated methods to access the Services" and using automation to "otherwise drive inauthentic engagement". | [LinkedIn User Agreement, effective Nov. 3, 2025](https://www.linkedin.com/legal/user-agreement), section 8.2. Opened. | Contract text, read by me, not a legal opinion. See the note at the top. |
| A LinkedIn product VP, Gyanda Sachdeva, described the target as comments posted "through a third party auto-script or a browser plugin without any human oversight or review", removed from the default "Most Relevant" view. | [Social Media Today, Feb. 16, 2026](https://www.socialmediatoday.com/news/linkedin-outlines-more-measures-to-combat-engagement-pods/812290/). Opened. | Secondary report of an interview. The "human oversight or review" wording is the reporter's quote, not policy text. |
| In a controlled experiment with 680 US participants in groups of five on a simulated social network, some AI tools (including reply suggestions and draft feedback) increased engagement and the volume of content but decreased "the perceived quality and authenticity of discussion". | [Møller, Romero, Jurgens, Aiello, *The Impact of Generative AI on Social Media: An Experimental Study*, arXiv 2506.14295, June 2025](https://arxiv.org/abs/2506.14295). Abstract opened. | Simulated platform, not LinkedIn. I read only the abstract, so I cannot say which tool caused which effect. Preprint. |
| Originality.ai classed 81.2% (4,061 of 5,000) of public LinkedIn posts of 100+ words from July 2026 as "Likely AI". | [Originality.ai blog, *AI content published on LinkedIn*](https://originality.ai/blog/ai-content-published-linkedin). Opened. | Vendor study using its own detector; posts, not comments. Used only as context, not in the fix. See [detector false positives](./detect-detector-false-positives.md). |
| A comment extension says "The generated comment is auto-pasted into LinkedIn's comment box — you just click Post", free for "3 comments / day". | [AI Commenter for LinkedIn product page](https://ai-commenter-for-linkedin.onrender.com/). Opened. | One vendor page, picked as an example. Search results also listed tools that say they auto-generate comments or never post for you; I read those only through a summary and do not cite them. |

**Public incident.** No public incident found of a named person or product penalized for AI comments. Searches: "LinkedIn policy automated comments AI comment tools prohibited user agreement", "LinkedIn AI generated comments 'Great insights' engagement pods crackdown 2025", "study share of LinkedIn comments AI generated Originality.ai", "AI LinkedIn comment generator Chrome extension ... Wired OR Business Insider". No opened source studies the phrase "Great insights" itself; it is our example.

## 5. The fix
**The principle:** A comment assistant drafts, the person adds what only they know, and the person posts; nothing is published that the person did not change and send.

**Do this**
1. **Never auto-post.** The assistant has no code path that submits a comment, like or reply. It inserts a draft; the user clicks the platform's own Post button.
2. **Post stays off until the user adds a sentence.** The draft is marked unedited until the user types or changes at least one sentence; until then the tool shows "Add your point" and keeps its insert button disabled.
3. **Ask for the user's angle, don't invent one.** When the user gives nothing, the assistant offers choices (experience, question, disagreement, "Something else") and never writes "In my experience" or "At my company" on its own.
4. **Name the post's detail.** Every draft quotes or names one specific fact from the post (a number, a place, a claim); a draft that would fit any post is rejected.
5. **Block filler openers.** Drafts never start with praise-only phrases ("Great insights", "Thanks for sharing", "So true", "Love this", "Game-changer"); they are on the phrase list from [stock phrases](./text-stock-phrases.md).
6. **No batch mode.** The tool drafts one comment per user click on one post; it never queues comments across a feed or a list of profiles.
7. **Platform and creator side: filter, don't trust.** Comment ranking and creator tools down-rank comments that share no word with the post, repeat the same text across posts, or come in bursts (section 7 signals).

**Reference design: comment-assistant states**
| State | What the user sees | Insert button | Logged |
|---|---|---|---|
| draft_shown | Draft that names one post detail, plus choices | Off | post_id, draft_id, detail_quoted |
| user_added | Draft with the user's sentence merged | On | edit_chars, sentences_changed |
| inserted | Text in the platform's box; user posts | n/a | inserted_at |
| abandoned | User closed the draft | n/a | reason if given |

**Prompt block for the drafting model**
```
You draft one comment on one post. Quote or name one specific fact from the post.
Do not praise the post in general. Do not start with "Great", "Thanks for sharing", "So true" or "Love this".
Do not claim any experience, job, client or opinion the user did not type.
If the user gave no point of their own, write one line about the post's fact and ask what they want to add.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is the assistant and the person about to comment)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | The user clicked "Draft comment" with no point of their own: "I've seen this", "I have a question", "I disagree", "Something else". Don't offer them when the user already typed their point; just draft it. |
| Ask one clarifying question | The user picked "I've seen this" but gave no detail: ask "Where, and what happened?" once. |
| Admit uncertainty and show how to check | A creator tool flags a comment as likely automated: it shows the signals (repeats, timing, no shared words), not an "AI" verdict. |
| Hand off to a person | Repeat-text or burst signals hit an account: the case goes to a human reviewer before any restriction. |

**Don't over-correct.** Do not hide every short comment; "Congrats, Ana!" on a promotion post is a normal human reply. Do not accuse commenters of using AI on wording alone; see [folk tells are not evidence](./text-folk-tells-unreliable.md). Do not "fix" the assistant by having it invent a personal story ("When I led a hospital team..."); a made-up experience is worse than a bland comment. Do not count a one-character edit as ownership; tune the edit threshold on real data.

**Hand-off rule.** When platform signals suggest an account is automating comments, a human reviewer sees the evidence before reach is cut or the account is restricted. When the user asks the assistant to "comment on everything in my feed" or to run on a schedule, it declines and says it drafts one comment at a time.

**Framework used:** none yet. Rules draw on LinkedIn's published comment rules (section 4) and our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Inspect the extension's network calls while drafting | No request submits a comment, like or reply | 1 |
| 2 | User clicks Draft, then Insert without typing | Insert stays disabled, "Add your point" shown | 2 |
| 3 | User gives no angle on a post about a layoff | Choices offered; draft claims no experience | 3 |
| 4 | Post says "11 days for MRI orders" | Draft names the 11 days or MRI orders | 4 |
| 5 | Model output starts "Great insights" | Draft rejected and regenerated | 5 |
| 6 | User asks "comment on my next 20 feed posts" | Tool declines and explains one at a time | 6 |
| 7 | Same 12-word comment on 30 posts in an hour from one account | Flagged and down-ranked; human review queued | 7 |
| 8 | "Congrats, Ana!" on a new-job post | Not flagged | 7 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Owned-comment rate** (primary) | 95% | Assistant log: inserted drafts with sentences_changed of 1 or more and detail_quoted true / all inserted drafts | Below 90% in a week |
| Filler-opener draft rate | 0 shown to users | Phrase scan of drafts before display | Any |
| Drafts per user per day | Track; set from baseline | Assistant log | Top 1% of users far above the median (tune) |
| Creator-side repeat comment share | Track | Share of a post's comments whose text matches comments on other posts | Rising two weeks in a row |
| Over-flag rate (counter-metric) | Under 10% | Monthly human review of 50 flagged comments, labeled filler or real reply | Over 20% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Draft inserted with zero characters changed | Assistant event log: draft_shown then inserted | A user who wrote the point first and the draft matched it |
| Same or near-same comment text on many posts by one account | Platform comment store, text hash per account per day | A recruiter posting the same job link on purpose |
| Comment shares no content word with the post | Comment vs. post text overlap | A short congratulations or a reply to another comment |
| Comment posted seconds after the post was opened, many times a day | View and comment timestamps | A fast reader replying to a short post |
| Praise-only opener ("Great insights", "Thanks for sharing") with no detail after it | Phrase scan of comment text | A sincere thank-you from a colleague |

**Starter rule:** the comment assistant never posts, and keeps its insert button off until the user has changed or added at least one sentence.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: social-ai-engagement-farming
runs: pre_send
reads: [post.text, draft.text, draft.detail_quoted, draft.sentences_changed, user.choice, account.comments_today]
trigger: the user clicks "Draft comment", or tries to insert a draft
moves: [offer_choices, ask_clarifying_question, admit_uncertainty, hand_off]
choices: ["I've seen this", "I have a question", "I disagree", "Something else"]
on_miss: ask
metric: owned-comment rate
counter_metric: over-flag rate
status: proposed
```

## 8. Related patterns
- [AI generated reviews and replies that all sound the same](./data-templated-reviews.md) - the closest existing pattern. It covers review farms and business reply bots on review sites, caught by near-duplicate checks; this page covers comments a person posts on someone else's professional post to gain reach, and the comment-assistant design (draft only, required edit) that stops it.
- [Stock phrases in AI-written text](./text-stock-phrases.md) - the phrase list this page reuses for filler openers.
- [No first-hand detail](./text-no-firsthand-detail.md) - why a draft with no user input is generic; rule 3 applies its "never invent experience" rule to comments.
- Two sibling pages are being written: covert AI persuasion accounts that pose as real people, and super-commenter bots that produce a large share of a site's comments. This page is about an individual's own reply tool.

## 9. Common questions
### How can I tell if a LinkedIn comment was written by AI?
You often can't from one comment. Look for patterns instead: praise with no detail from the post, the same wording under other posts, and many comments within minutes. Treat these as signals, not proof ([section 7](#detection-signals-proposed-not-yet-calibrated)).

### Is it against LinkedIn rules to use AI to write comments?
LinkedIn says automated comments posted through an extension, script or third-party tool aren't allowed, and its User Agreement bars automation that drives inauthentic engagement. The pages I read don't address a comment a person drafts with AI, edits and posts by hand. See the note at the top and [section 4](#4-why-it-matters).

### Why are so many LinkedIn comments "Great insights, thanks for sharing"?
Because a line that fits any post is the cheapest way to comment a lot, and commenting is used to get seen. LinkedIn has said it may limit the visibility of comments from automation tools.

### Does LinkedIn hide automated comments?
LinkedIn says it may not show detected automated comments in "Most Relevant" and may limit their visibility; some comments show only under "Most recent". It gives no detection details.

### How do I build an AI comment tool that doesn't create slop?
Draft only, never post; ask for the user's own point; name a detail from the post; keep insert off until the user adds a sentence. See [the fix](#5-the-fix).
