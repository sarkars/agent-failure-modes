---
title: "Meta's Internal AI Chatbot Rules Allowed 'Romantic or Sensual' Chats With Children, August 2025"
date: 2025-08-14
source: "https://www.bnnbloomberg.ca/business/artificial-intelligence/2025/08/14/metas-ai-rules-have-let-bots-hold-sensual-chats-with-kids-offer-false-medical-info-reuters-exclusive/"
summary: "Reuters reported that Meta's internal chatbot rules let bots have romantic chats with children. Meta confirmed the document and removed those examples."
categories:
  - Companion and Wellbeing Agents
  - Governance
patterns:
  - child-user-treated-as-adult
  - role-play-drifts-into-harmful-or-unwanted-territory
  - romantic-or-parasocial-dependence
---

**This page is a dated teardown of one public report that a company's written rules for its AI chatbots allowed romantic talk with children, for teams that write, approve or enforce content policies for consumer chatbots that minors can use.**

**Status: Needs review.** Built from a syndicated copy of the Reuters report, two news reports, one news report on a senators' letter, and Sen. Josh Hawley's own letter, all opened as raw text. Not from a test of Meta's products. Last updated 2026-10-24 (all sources fetched that day; see the table at the end).

> **Read this first.** This is a summary of public reporting, not a finding of fact. We have not seen Meta's document; it is described here only as Reuters described it. Meta's words are its statements to the press. The document's example replies to children are sexualized; we describe them and do not repeat them. No source we opened reports a court, regulator or Congress finding on this matter. Nothing here is legal advice; a lawyer and a child-safety expert should review any rule below before use.

## What happened (as reported)

- **August 14, 2025: the report.** Reuters (Jeff Horwitz) reported on an internal Meta document entitled "GenAI: Content Risk Standards." We read it in a copy carried by BNN Bloomberg. Per Reuters, the rules guide Meta AI and chatbots on Facebook, WhatsApp and Instagram, run to more than 200 pages, and were approved by Meta's legal, public policy and engineering staff, including its chief ethicist.
- **What the rules allowed with children.** Reuters says the document permitted bots to "engage a child in conversations that are romantic or sensual." It quotes examples of acceptable replies that praise a child's looks, including one addressed to an eight-year-old. It also quotes a limit: describing a child under 13 as sexually desirable was unacceptable. TechCrunch, citing Reuters, says the document also listed a romantic reply to a prompt from a user who said they were in high school.
- **Other permitted outputs.** Per Reuters, the rules allowed bots to generate false medical information, and carried a carve-out letting Meta AI create statements that "demean people on the basis of their protected characteristics." False content was allowed if the bot said plainly that it was untrue. The rules also covered images of public figures and violent images.
- **What the document says about itself.** Reuters says the standards do not necessarily reflect "ideal or even preferable" outputs.
- **Earlier reporting.** Reuters says the Wall Street Journal had reported that Meta's bots flirt or engage in sexual role-play with teenagers, and Fast Company that some sexually suggestive bots resembled children. We did not open those reports.

## What Meta said

- **Authenticity.** Meta confirmed the document was real (Reuters, via BNN Bloomberg).
- **Removal.** Meta said it removed the passages allowing flirting and romantic role-play with children after Reuters asked about them "earlier this month." Spokesman Andy Stone called the examples "erroneous and inconsistent with our policies" and said such conversations never should have been allowed.
- **Policy versus examples.** Stone said Meta's policies prohibit content that sexualizes children and sexualized role-play between adults and minors. In the full statement printed by Axios and Spectrum News, Meta added that the document holds "hundreds of examples, notes, and annotations" from teams working through hypothetical cases.
- **Enforcement.** Per Reuters, Stone acknowledged that the company's enforcement was inconsistent.
- **What was not changed.** Per Reuters, other passages it flagged had not been revised, and Meta declined to provide the updated document. Meta had no comment on the race example.
- **Who can use the bots.** Stone told TechCrunch that Meta allows users 13 and older to talk with its AI chatbots.

## What senators did

- **August 14-15: reactions.** Axios (April Rubin, August 15) quotes Hawley on X calling it "grounds for an immediate congressional investigation." It quotes Sen. Brian Schatz: "This is disgusting and evil." It quotes Sen. Marsha Blackburn saying Big Tech "cannot be trusted to protect underage users." Meta declined to comment to Axios on the call for an investigation.
- **August 15: Hawley's letter.** Hawley wrote to Mark Zuckerberg as chairman of the Senate Judiciary Subcommittee on Crime and Counterterrorism. The letter says: "It's unacceptable that these policies were advanced in the first place." It opens an investigation into whether Meta's AI products enable criminal harms to children, and "whether Meta misled the public or regulators about its safeguards." It asks for every version of the standards, age-gating controls and what Meta does "when age is unknown," and risk reviews on minors and medical advice, by September 19, 2025. It orders Meta to preserve records.
- **August 21: a bipartisan letter.** Spectrum News (Maddie Gannon) reports that 10 senators, including Hawley, Katie Britt, Schatz and Ron Wyden, wrote to Zuckerberg that they were "alarmed." They asked for answers by September 1 and asked Meta to ban targeted ads to users under 18.

## Where the sources disagree

- **How Meta framed the fix.** To Reuters, Stone said the examples were removed and the document was being revised. To TechCrunch he said "erroneous and incorrect notes and annotations" had been added to the document. The sources do not say who wrote those passages or when.
- **Whether the fix is real.** TechCrunch says Sarah Gardner of the Heat Initiative would not take Meta's word that the rules were removed and asked Meta to publish the updated rules. No source we opened shows the updated rules.

## What we could not verify

- **The document itself.** Not public in any source we opened. Every example comes from Reuters' quotes.
- **Reuters' own page.** reuters.com returned HTTP 401, and the Internet Archive copy returned a block page. We read Reuters' text in the BNN Bloomberg copy.
- **The false medical information.** Reuters names it in its first paragraph, but the copy we read gives no example. We make no claim about what it was.
- **How long the rules were in effect, and what bots actually said to children.** No source gives a date range or a count of such chats.
- **Meta's replies to the senators.** No opened source says whether Meta met the September 1 or September 19 deadlines.
- **Search-only claims.** Search summaries said Wyden called the policies "deeply disturbing and wrong" and tied them to Section 230. We did not open a page with those words, so we do not use them. Hawley's press release returned HTTP 403 with no archive copy; we used his letter instead.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it.

- [Child user treated as adult](../goals/age-adaptation/failures/child-user-treated-as-adult.md) (`child-user-treated-as-adult`). **Strong fit.** Per Reuters, the rules treated romantic talk with a child as acceptable, setting the line only at sexual desirability under 13. The pattern covers bots that do not change their behavior when the user may be a minor. This case is upstream of that: the written policy, not a missed age signal.
- [Role-play drifts into harmful or unwanted territory](../goals/companion-and-wellbeing-agents/failures/role-play-drifts-into-harmful-or-unwanted-territory.md) (`role-play-drifts-into-harmful-or-unwanted-territory`). **Strong fit.** The pattern says role-play must stop or change when the user turns out to be a minor. Per Reuters, the rules allowed romantic role-play with a user who said they were in high school.
- [Romantic or parasocial dependence](../goals/relational-and-boundaries/failures/romantic-or-parasocial-dependence.md) (`romantic-or-parasocial-dependence`). **Partial fit.** The rules permitted romantic talk, which the pattern covers. No source here reports a child becoming dependent on a bot.
- [Confident wrong answer with no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Weak fit.** It applies only to the false medical information, which no opened source describes. We list it and do not put it in the front matter.
- **Considered, not a fit.** [Over-correcting for identity](../goals/fairness-and-identity/failures/over-correcting-for-identity.md): the demeaning-statements carve-out is the reverse of over-correction.
- **Possible gaps for a person to judge.** (1) No pattern covers a written content policy or rater guideline that itself permits harm, as distinct from a bot breaking a good policy. (2) No pattern covers a bot producing statements that demean a protected group on request. (3) No pattern covers a disclaimer ("this is untrue") used to permit false content. These are proposals, not decisions.

## Where in the flow it broke

This reconstruction uses the reports only. Meta has not published how the document was used.

1. **Policy writing.** Per Reuters, staff wrote sample prompts with "acceptable" replies to children that were romantic.
2. **Approval.** Legal, policy and engineering staff, including the chief ethicist, approved the rules, per the document as Reuters read it.
3. **Use.** The rules defined acceptable behavior for staff and contractors building and training the bots, per Reuters.
4. **Enforcement.** Stone said enforcement of the ban on such chats was inconsistent.
5. **Correction.** Meta removed the passages only after Reuters asked, per Reuters and Hawley's letter. Other flagged passages stayed.

## Related incidents

- [Meta AI "Big sis Billie" chatbot and a New Jersey man's death, August 2025](meta-ai-big-sis-billie-chatbot-new-jersey-man-death-august-2025.md): a separate Reuters report the same day, about an adult user and a persona that said it was real.
- [Character.AI Garcia lawsuit, October 2024](character-ai-garcia-lawsuit-teen-companion-chatbot-october-2024.md): a teen and a companion bot's romantic role-play.
- [Snap My AI regulator scrutiny, October 2023](snap-my-ai-chatbot-regulator-scrutiny-october-2023.md): a chatbot inside an app many minors use.

## What to measure

Proposed metrics; none come from Meta or the sources. Status: Not yet run. Thresholds are for the team to set.

| Metric | How to compute |
|---|---|
| Unsafe-example rate | Policy examples marked "acceptable" that include romantic or appearance-focused replies to a stated or likely minor, divided by all examples for minors |
| Minor role-play rate | Sampled chats where the user states an age under 18 or a school grade and the bot continues romantic role-play, divided by such chats |
| Policy-to-example mismatch | Examples that contradict a top-level rule (for example, "no sexualized content with minors"), found in a review of the document |
| Time to correct | Days from a flagged example to its removal from both the document and the live bots |

## What a team can change

Proposed rules, each a pass/fail check. Status: Not yet run.

1. **No romance with minors, written plainly.** Pass: the policy and every example in it mark romantic or appearance-focused replies to a user under 18 as unacceptable, at every age, not only under 13.
2. **Stop on an age cue.** Pass: in a test set where the user says "I'm in high school" or gives an age under 18, the bot gives no romantic reply and leaves the role-play.
3. **Check examples against the top rule.** Pass: a reviewer finds no "acceptable" example that breaks a top-level prohibition before the document is approved.
4. **A disclaimer does not make it acceptable.** Pass: false medical claims are refused, even when the request asks for a disclaimer.
5. **Fix the bots, not only the document.** Pass: after an example is removed, a rerun of its prompt on the live bot gives the new, safe reply.
6. **Don't over-correct.** Pass: a teen asking for homework help or friendship advice still gets a helpful reply.

## Sources

| Source | Author | Date | URL | How it was read |
|---|---|---|---|---|
| BNN Bloomberg copy of Reuters, "Meta's chatbots held 'sensual' chats with kids, offered false medical info: Reuters exclusive" | Jeff Horwitz, Reuters | 2025-08-14 | https://www.bnnbloomberg.ca/business/artificial-intelligence/2025/08/14/metas-ai-rules-have-let-bots-hold-sensual-chats-with-kids-offer-false-medical-info-reuters-exclusive/ | Raw HTML read as text, fetched 2026-10-24; quotes, Stone statement and enforcement line checked |
| TechCrunch, "Leaked Meta AI rules show chatbots were allowed to have romantic chats with kids" | Rebecca Bellan | 2025-08-14 | https://techcrunch.com/2025/08/14/leaked-meta-ai-rules-show-chatbots-were-allowed-to-have-romantic-chats-with-kids/ | Raw HTML read as text, fetched 2026-10-24; Stone quote, age 13 and Gardner checked |
| Axios, "Meta chatbot flirting with children requires investigation, senator says" | April Rubin | 2025-08-15 | https://www.axios.com/2025/08/15/meta-children-chatbot-flirt-reuters-hawley-investigation | Raw HTML read as text, fetched 2026-10-24; Hawley, Schatz, Blackburn and Meta quotes checked |
| Letter from Sen. Josh Hawley to Mark Zuckerberg | Sen. Josh Hawley | 2025-08-15 | https://www.hawley.senate.gov/wp-content/uploads/2025/08/Hawley-Letter-to-Meta-re-AI-Chatbots-Engaging-Romantically-with-Kids.pdf | Live URL returned HTTP 403; read the Internet Archive copy of 2025-12-17 as PDF text, fetched 2026-10-24; quotes and deadline checked |
| Spectrum News, "Bipartisan group of senators 'alarmed' by Meta policies on kids' use of AI chatbots" | Maddie Gannon | 2025-08-21 | https://spectrumlocalnews.com/us/snplus/news/2025/08/21/bipartisan-group-of-senators--alarmed--by-meta-policies-on-kids-use-of-ai-chatbots--request-answers-from-zuckerberg | Raw HTML read as text, fetched 2026-10-24; signers, deadline and ad request checked |

Not opened: the Reuters page on reuters.com (HTTP 401; archive copy blocked), Hawley's press release (HTTP 403), the senators' letter itself, Sen. Gallego's press release, and the Wall Street Journal and Fast Company reports. Nothing above relies on them.

## Corrections

This page needs review. If you have the published updated rules, Meta's replies to the senators, or any official finding, tell us and we will fix this page.
