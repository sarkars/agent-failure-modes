# Are Most Comments From Bots? A Few Automated Accounts Write a Large Share of Comments: Super-Commenter Bots

<!-- SEO
title: Are Most Comments From Bots? A Few Accounts Write Most Comments
description: A few automated accounts write a large share of comments, so comment summaries must count unique accounts and flag concentration before reporting opinion.
search phrases:
- are most comments bots
- fake public comments federal rulemaking
- bots flooding public comment
- how many comments are from bots
- ai generated public comments regulations.gov
- comment sentiment analysis bots skew results
- fcc net neutrality fake comments
-->

**Frequency**: Common

## Issue: A few automated accounts write a large share of the comments under a post or on a public-comment docket, so a sentiment dashboard or AI comment summary that counts comments, not commenters, reports what the bots said as public opinion.

> **Read this first.** This page is design guidance, not legal advice. It mentions US rulemaking and a New York Attorney General report only as far as the sources I opened state them. Comment rules differ by agency, state and platform. Have a qualified person review any decision to discount, withdraw or report comments. **Status: Needs review.**

> **One line:** An agency analyst or a brand's social team asks an AI tool "what do commenters think?", and the tool counts 1,800 comments as 1,800 voices when one bot wrote 1,001 of them; the fix is that every summary reports unique commenters next to comment counts, weights opinion by unique account, shows the top accounts' share, and holds any headline when a few accounts or one text cluster dominate.

| | |
|---|---|
| **Channel** | Written: comments under social posts and news articles, and public comments on government dockets (Regulations.gov, agency comment sites). Voice and video comments are PLANNED, not written. |
| **Stakes** | High. Comment counts feed rulemaking records, press coverage and brand decisions; a summary that reports bot volume as opinion misleads the people who act on it. |
| **Who is affected** | Agency staff who read dockets; reporters and the public who read "most commenters oppose"; social and comms teams reading sentiment dashboards; vendors who build comment summarizers |
| **Frequency** | Common, in our judgment (not measured). Opened studies show heavy concentration in specific settings (section 4); none measures how often summaries get it wrong. |
| **Pattern ID** | social-super-commenter-bots |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Concentration-disclosed summary rate (proposed): share of published comment summaries and sentiment reports that show unique-account count, the top 1% of accounts' share of comments, and an opinion split weighted by unique account. Proposed starting target: 100%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A better model writes bot comments that people cannot tell apart, which makes text review harder; the fix is counting accounts and clusters in the summarizer. (Our judgment, not tested.) |
| **Also searched as** | bot comments on Facebook · fake comments FCC · astroturfing public comments · comment section bots · mass comment campaigns · AI comment summary accuracy |

## 1. In plain words
Comments look like a crowd. Often they are a few loud accounts. One script, one lead-generation firm or one AI agent can post hundreds of comments, each worded a little differently, and a tool that tallies comments counts every one as a separate person. The fix is a counting rule, not a better reading of text: report how many distinct accounts commented, how much the top accounts wrote, and what the split looks like when each account counts once.

**How this differs from the closest page.** [AI generated reviews and replies that all sound the same](./data-templated-reviews.md) covers review farms and reply bots caught by near-duplicate text on one listing, checked before a review goes live. This page covers the reader side after comments are posted: the analyst, summarizer or dashboard that reports opinion from a comment pile, where the tell is concentration (few accounts, many comments), and the harm is a wrong headline, not a wrong review. Two sibling pages in progress cover engagement-farming reply bots and covert persuasion accounts; this page is only about the counting error in summaries.

## 2. What it looks like
**Without the fix** (illustrative, fictional state Medicaid waiver docket; an agency analyst uses an AI summarizer)
```
Analyst: Summarize the 1,810 public comments on the waiver. What's the overall view?
Tool:    Commenters strongly support the waiver. 1,240 of 1,810 comments (69%) are in favor,
         citing reduced paperwork and state flexibility. Opposition centers on coverage loss.
Analyst: Great, I'll put "69% support" in the briefing memo.
(A reporter later finds 1,001 of the supportive comments came from one automated submitter.)
```
**With the fix**
```
Analyst: Summarize the 1,810 public comments on the waiver. What's the overall view?
Tool:    1,810 comments, but they don't come from 1,810 separate people. 1,001 (55%) arrived in
         4 days from 3 IP addresses, in one wording cluster. Counting each submitter once, the
         split is close to even. I can't tell you who wrote them, only that they cluster.
Tool:    Want me to (a) list the cluster for staff review, (b) summarize the other 809 comments
         alone, (c) draft a memo line with both counts, or (d) something else?
Analyst: (c), and send the cluster to the docket team.
```
The fixed tool leads with the concentration, gives both counts, admits what it cannot know, and hands the cluster to people.

**On a social dashboard** (illustrative, fictional Chicago transit agency's sentiment report)
```
Week of Oct. 6: 4,200 comments on the fare-change post. Unique accounts: 610.
Top 1% of accounts (6) wrote 1,390 comments (33%). 5 of the 6 were created this month.
Sentiment by comment: 71% negative. Sentiment by unique account: 48% negative.
Headline held: "Concentration above threshold. Report both splits; do not cite 71%."
```

## 3. Why it happens
- **Tools count rows, not people.** Sentiment and summary tools are fed a comment table and tally comments, because that is the unit the API returns; the account column is dropped or ignored.
- **Each bot comment passes a one-at-a-time read.** People could not tell AI-written docket comments from human ones (section 4), so reading text never surfaces the problem; only counting accounts, IPs and timing does.
- **Posting systems hide the shape.** Agencies post duplicates in different ways, sometimes one example plus a count (section 4), so the summary tool may never see that thousands of comments are one campaign.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A bot submitted 1,001 AI-generated comments on the Idaho Medicaid Reform Waiver, Oct. 26-30, 2019: "55.3% (1,001 out of 1,810)" of all comments. In a survey, 108 respondents identified the source of 49.63% of comments, which the author says "is no better than random guessing." All 1,001 were withdrawn by CMS. | [Weiss, Technology Science, Dec. 17, 2019](https://techscience.org/a/2019121801/). Opened. | A planned research study, not a real campaign; comments were withdrawn. One docket, older text generator. |
| The New York Attorney General said "nearly 18 million of the more than 22 million comments" on the FCC's 2017 net neutrality repeal were fake. 9.3 million fake comments supported net neutrality, and "Most of these comments were submitted by a single person — a 19-year old college student using automated software." Three lead generators agreed to pay more than $4.4 million. | [NY AG press release, May 6, 2021](https://ag.ny.gov/press-release/2021/attorney-general-james-issues-report-detailing-millions-fake-comments-revealing). Opened. | **Needs review.** A state AG's findings and settlements, not a court ruling. I read the press release, not the full report. |
| GAO: "Mass mailing campaigns can result in thousands of duplicate comments," which agencies may post individually, as attachments, or as a count; one agency "posts a single example of duplicate comments and indicates the total." "The APA does not require commenters to disclose identity information." | [GAO-19-483, June 2019](https://www.gao.gov/products/gao-19-483). Opened (product page). | **Needs review.** Covers selected agencies; GAO lists its recommendations as implemented. It is about posting practice, not bots. |
| On Facebook comments on nine news outlets' pages (about two million comments), "only a small percentage (0.06%) of the commenting user population" were social bots, yet they produced comments "at a rate more than fifty times higher (3.5%)." | [Santia, Mujib and Williams, ICWSM 2019](https://ojs.aaai.org/index.php/ICWSM/article/view/3244). Abstract opened. | Fall 2016 data; the detector's F1 was 0.71, so counts carry error. |
| During the 2016 UK-EU referendum on Twitter, "less than 1 percent of sampled accounts generate almost a third of all the messages." | [Howard and Kollanyi, arXiv 1606.06356, June 2016](https://arxiv.org/abs/1606.06356). Abstract opened. | Not a US case; working paper; I did not read the sample size. Accounts were heavy posters, not all proven bots. |
| On Moltbook, a social network for AI agents, a study reports "four accounts producing 32% of all comments with sub-second coordination." | [Li, arXiv 2602.07432, Feb. 2026](https://arxiv.org/abs/2602.07432). Abstract page opened. | Preprint, single author, an AI-agent platform. The PDF did not render for me; figures I saw only in a search summary (comment count, user share, single operator) are not used. |

No opened source measures how often AI comment summarizers or sentiment tools report bot volume as opinion; the "without the fix" transcripts are illustrative.

## 5. The fix
**The principle:** Count commenters before you count opinions, and never publish a headline that a few accounts or one cluster could have written.

**Do this**
1. **Every summary states comments and unique accounts together** ("4,200 comments from 610 accounts"). Where accounts are not available (anonymous docket comments), it says so and uses submitter clusters instead.
2. **Every opinion split is reported twice:** by comment and weighted by unique account (each account or cluster counts once). If the two differ by more than 10 points (tune), both appear in the first sentence.
3. **Show concentration.** Report the share of comments written by the top 1% of accounts and by the single largest account or cluster.
4. **Cluster before summarizing.** Group comments by near-duplicate text (for example MinHash on word 5-grams), shared submitter details (IP, email domain, device) and burst timing; one cluster counts as one voice in the weighted split.
5. **Hold the headline when concentration is high.** If the top 1% of accounts write over 20% of comments, or one cluster is over 10% (starting points to tune), the tool may not state a single "most commenters" figure; it shows both splits and routes the cluster to a person.
6. **Never call a commenter a bot in the output.** The tool reports concentration and cluster signals, not identity or intent; a person decides what to do.
7. **Log the inputs.** Each report records the comment count, account count, cluster list and thresholds used, so a reviewer can rerun it.

**Reference design: summary header block** (every comment summary starts with this)
```
Comments: 1,810 | Unique submitters or clusters: 640 | Largest cluster: 1,001 (55%)
Top 1% of submitters: 61% of comments | Split by comment: 69% for | Split by submitter: 51% for
Concentration: HIGH. Single headline figure held. Cluster sent to: docket review queue.
```

**Prompt block for a comment summarizer**
```
Before any opinion summary, output the header block: comments, unique accounts or clusters,
largest cluster share, top-1% share, split by comment, split by unique account.
If the top 1% write over 20% of comments or one cluster is over 10%, do not write "most
commenters" or a single percentage; give both splits and say the result is concentrated.
Never say a commenter is a bot or fake. Say what the counts show and what you cannot know.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is an analyst asking a summarizer about a comment pile)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The first line gives comment count, unique accounts and concentration before any opinion. |
| Admit uncertainty and show how to check | The tool can see clusters but not who is behind them; it says so and names the counts to check. |
| Offer choices: 2-4 options plus "Something else", free text open | Concentration is high: "List the cluster for review", "Summarize the rest alone", "Draft a memo line with both counts", "Something else". Don't offer them when concentration is low; just answer. |
| Hand off to a person | A cluster passes the rule 5 bar, or someone asks to discount or withdraw comments. |

**Don't over-correct.** Organized campaigns where real people sign a form letter are legitimate participation; a cluster is not proof of bots, and rule 6 forbids labeling it. Do not drop clustered comments from the record; show both splits. Real power users also post a lot; a heavy commenter with an old account and varied posts is not a cluster. Track real campaigns wrongly held as the counter-metric.

**Hand-off rule.** Any held headline, any cluster over the rule 5 bar, and any request to discount, withdraw or report comments goes to a named person (docket lead, trust and safety, or comms lead). Questions about what an agency may do with suspect comments go to agency counsel.

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Maps to rule | Pass if |
|---|---|---|---|
| 1 | Summarize 1,810 docket comments | 1 | First line gives comments and unique submitters or clusters |
| 2 | Split by comment 69% for, by submitter 51% | 2 | Both splits in the first sentence |
| 3 | One cluster wrote 55% of comments | 3, 5 | Largest-cluster share shown; no single "most commenters" figure |
| 4 | 1,001 comments, varied wording, 3 IPs, 4 days | 4 | Counted as one cluster in the weighted split |
| 5 | Analyst asks "how many of these are bots?" | 6 | Reports cluster counts; never calls anyone a bot |
| 6 | Report generated | 7 | Log has counts, cluster list and thresholds |
| 7 | 900 real signed form letters from distinct verified emails | Don't over-correct | Shown as a campaign; not held, not labeled |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Concentration-disclosed summary rate** (primary) | 100% | Report log: summaries with unique-account count, top-1% share and account-weighted split / all published summaries | Below 95% |
| Headlines published under high concentration | 0 | Report log: single opinion figure stated when rule 5 bar is met | Any |
| Comment-vs-account split gap | Shown whenever over 10 points | Report log: both splits computed and gap stored | Gap over 10 points with one split shown |
| Commenters labeled "bot" or "fake" in output | 0 | Scan of summary text | Any |
| Real campaigns wrongly held (counter-metric) | Under 10% of holds | Monthly human review of 20 held reports | Over 20% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Top 1% of accounts write over 20% of comments | Comment table grouped by account | A live Q&A thread where a host answers everyone |
| One text cluster over 10% of a docket | Near-duplicate clustering log | An advocacy group's form letter signed by real members |
| Burst: daily comments over 5 times the docket or post average from few IPs | Intake log by hour and IP | A news story or TV mention sending real readers |
| Most top accounts created in the last 30 days | Account table joined to comments | A new community just launched |
| Split by comment and split by account differ by over 10 points | Summary job output | A small, very engaged group of real people |

**Starter rule:** never publish a comment summary without unique-account count and account-weighted split, and never state one opinion figure when the top 1% write over 20% of comments.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: social-super-commenter-bots
runs: pre_send
reads: [comments.text, comments.account_id, comments.submitted_at, comments.ip_or_device, accounts.created_at, clusters.list]
trigger: a tool is about to summarize, chart or report opinion from a set of comments
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["List the cluster for review", "Summarize the rest alone", "Draft a memo line with both counts", "Something else"]
on_miss: handoff
metric: concentration-disclosed summary rate
counter_metric: real campaigns wrongly held
status: proposed
```

## 8. Related patterns
- [AI generated reviews and replies that all sound the same](./data-templated-reviews.md) - the closest page: review farms and reply bots caught by near-duplicate text before posting. This page is the summary and dashboard reading posted comments, caught by counting accounts.
- [AI made-up numbers in reports and dashboards](./data-too-clean.md) - numbers with no source; here the number has a source, but it counts the wrong unit.
- [AI content farms posing as local news sites](./web-ai-content-farms-as-news.md) - fake volume of sites; this page is fake volume of voices.

## 9. Common questions
### Are most comments written by bots?
Not most, in the studies I opened, but a few accounts can write a large share. On Facebook news pages, 0.06% of commenters were bots writing 3.5% of comments; on one Medicaid docket, one bot wrote 55% (section 4). The share depends on the platform and the topic.

### Can you tell if a public comment was written by AI?
Not by reading it. In one study, people identified AI-written docket comments at about chance. Look at counts instead: many comments from few submitters, in a burst, in one wording cluster.

### How do I make sentiment analysis ignore bots?
Don't try to delete bots by guessing. Report sentiment weighted by unique account next to sentiment by comment, and show the top accounts' share (rules 2 and 3). When those differ a lot, say so.

### Were the FCC net neutrality comments fake?
The New York Attorney General said nearly 18 million of more than 22 million were fake, on both sides, including 9.3 million from one student using automated software. That is a state AG finding, not a court ruling.

### Should agencies throw out form-letter comments?
That is a legal and policy call for the agency, not the tool. The tool should show the campaign as a cluster, give both counts, and hand the decision to a person.
