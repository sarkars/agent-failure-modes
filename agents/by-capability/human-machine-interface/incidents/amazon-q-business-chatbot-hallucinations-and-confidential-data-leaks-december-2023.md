---
title: "Amazon Q Preview: Employees Report \"Severe Hallucinations\" and Leaked Confidential Data, December 2023"
date: 2023-12-01
source: "https://www.platformer.news/amazons-q-has-severe-hallucinations/"
summary: "Three days after AWS launched its Amazon Q work assistant in preview, Platformer reported leaked internal documents saying Q was hallucinating and leaking confidential data such as AWS data center locations. Amazon said Q had not leaked confidential information. All sources were read through fetch summaries."
categories:
  - General-Purpose Assistants
  - Security
  - Governance
patterns:
  - confident-wrong-answer-with-no-way-to-check
---

**This page is a dated teardown of one public incident, for teams that connect a work assistant to company documents and promise it will only show each user what they may see.** It is built from Platformer's report, AWS's launch post and press coverage, not from a test of Amazon Q. Every fact below comes from a source we opened (listed at the end).

**Status: Needs review.** Every source was read through a fetch-tool summary, not as a full page. Each quote below was checked in a second fetch of the same page. Platformer's article reports leaked internal documents that we have not seen. Amazon disputes the leak claim. Details seen only in search summaries are kept out of the claims and listed under "What we could not verify."

## What happened (as reported)

- **Launch, November 28, 2023.** AWS's News Blog (Antje Barth) says "Amazon Q is available today in preview in AWS Regions US East (N. Virginia) and US West (Oregon)." TechCrunch (Kyle Wiggers, same day) says it was unveiled at re:Invent in Las Vegas, is "now in public preview," and costs "starting at $20 per user per month."
- **The access promise.** The AWS post says "Amazon Q can adapt its interactions to each individual user based on the existing identities, roles, and permissions of your business." TechCrunch quotes AWS CEO Adam Selipsky: "Q understands and respects your existing identities, your roles and your permissions." TechCrunch also says "Q indexes all connected data and content" from apps such as Salesforce, Jira and Gmail.
- **Sources promised.** The AWS post says Q "provides citations and references to the original sources for fact-checking and traceability."
- **December 1, 2023, Platformer.** Zoë Schiffer and Casey Newton write: "Three days after Amazon announced its AI chatbot Q, some employees are sounding alarms about accuracy and privacy issues." Per leaked documents, Q was "experiencing severe hallucinations and leaking confidential data." The report says the leaked items included AWS data center locations, "internal discount programs," and unreleased features.
- **Severity.** Platformer says an employee marked the incident "sev 2," a level that means paging engineers at night and weekend work to fix it.
- **Internal wording.** Platformer quotes an internal document: "Amazon Q can hallucinate and return harmful or inappropriate responses." Its subtitle says some hallucinations could "potentially induce cardiac incidents in Legal."
- **Amazon's response.** A spokesperson told Platformer: "Some employees are sharing feedback through internal channels and ticketing systems, which is standard practice at Amazon," and "No security issue was identified as a result of that feedback." After publication Amazon added: "Amazon Q has not leaked confidential information." Futurism (Victor Tangermann, Dec. 4, 2023) repeats both statements.
- **Selipsky's framing.** Futurism says Selipsky told the New York Times: "Amazon built Q to be more secure and private than a consumer chatbot." We did not open the Times article.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Did Q leak data? | Platformer reports internal documents saying it did. Amazon says "Amazon Q has not leaked confidential information." Neither shows a transcript. |
| Who saw the leaked data | Platformer's sources are employees. No opened source says whether the answers reached outside customers or only Amazon staff testing Q. |
| How it happened | No opened source names the prompts, the data source, or whether a permission check failed. |
| The hallucinations | No opened source prints an example of a wrong answer. Amazon's later statement addresses leaks, not accuracy. |

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). One pattern fits, and only partly. The core reported failure, an assistant showing a user company data they should not see, has no pattern of its own in this taxonomy.

- **[Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)** (`confident-wrong-answer-with-no-way-to-check`). Partial fit. The reported "severe hallucinations" are wrong answers from a tool sold with citations "for fact-checking and traceability." But no opened source shows one wrong answer or its tone, so we cannot say whether a cue or a source was missing.
- **No pattern: permission-scoped answers.** AWS promised answers limited to each user's "identities, roles, and permissions." The reported leak of data center locations and discount programs, if true, breaks that promise. No taxonomy entry covers an assistant revealing internal business data across an access boundary.
- **Considered, not a fit.** [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (`third-party-data-shared-by-users`) is about a user pasting someone's private details into a bot; here the data reportedly came from Q itself. [Refusals that reveal internal rules](../goals/refusals-and-boundaries/failures/refusals-that-reveal-internal-rules.md) (`refusals-that-reveal-internal-rules`) is about a refusal quoting policy text; no opened source describes a refusal.

## Where in the flow it broke

Based on the reports, in order. Steps 3 and 4 are reported by Platformer and disputed by Amazon.

1. **Broad indexing.** Q indexes "all connected data and content" behind one chat box.
2. **Access promise.** Each answer is meant to respect the asking user's permissions.
3. **Answer step.** Q reportedly returned internal facts (data center locations, discount programs, unreleased features) in answers.
4. **Accuracy.** Q reportedly gave hallucinated answers that worried staff.
5. **Detection.** Employees caught it through internal tickets, after launch, at "sev 2."

## What to measure

Proposed metrics; none come from Amazon. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Cross-permission answer rate | Share of answers that cite a document the asking user cannot open |
| Restricted-term leak rate | Share of answers containing a term from a restricted list (site names, discount program names, codenames) to users outside the allowed group |
| Uncited claim rate | Share of factual answers with no citation, or with a citation that does not contain the claim |
| Post-launch sev tickets | Count of high-severity tickets per week tagged to the assistant |

## What a team can change

Proposed rules, each a pass/fail check on a transcript. Status: Not yet run.

1. **Two-user test.** Ask the same question as a user with access and a user without. Pass: the second answer contains no fact found only in the restricted document.
2. **Canary documents.** Plant a document with a unique fake codename, readable by one group. Pass: zero answers to other users contain the codename.
3. **Check at answer time.** Pass: every cited document is re-checked against the asker's permissions before the answer is shown.
4. **Claim must match source.** Pass: each factual sentence links to a source passage that states it; otherwise the answer says it is not sure.
5. **Red-team before preview.** Pass: a staff test with prompts for locations, prices and unreleased products finds no restricted facts before public preview opens.

These rules are our proposals. The sources do not say what Amazon changed.

## What we could not verify

- The leaked internal documents themselves, and any example prompt or answer. Platformer describes them; we did not see them.
- The full sentence around the "cardiac incidents in Legal" phrase. Two fetches disagreed on its wording, so we quote only the phrase from Platformer's subtitle.
- Data center context from DatacenterDynamics, including a 2018 WikiLeaks publication of AWS sites. Seen only in a search summary; the page returned HTTP 403.
- Business Insider's and IT Brew's coverage. Seen only in search results; Business Insider redirected and IT Brew returned HTTP 403.
- That the OECD AI incident database logged this case. Seen only in a search summary.
- Whether Amazon changed Q before Amazon Q Business became generally available (April 30, 2024, per the AWS post's update note).

## Sources

All opened 2026-10-22 (UTC).

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.platformer.news/amazons-q-has-severe-hallucinations/ | Platformer (Zoë Schiffer and Casey Newton) | 2023-12-01 | Yes, fetch-tool summary (one fetch reported paywall truncation) |
| https://platformer.substack.com/p/amazons-q-has-severe-hallucinations | Platformer, Substack copy | 2023-12-01 | Yes, fetch-tool summary |
| https://aws.amazon.com/blogs/aws/introducing-amazon-q-a-new-generative-ai-powered-assistant-preview | AWS News Blog (Antje Barth) | 2023-11-28 | Yes, fetch-tool summary |
| https://techcrunch.com/2023/11/28/amazon-unveils-q-an-ai-powered-chatbot-for-businesses | TechCrunch (Kyle Wiggers) | 2023-11-28 | Yes, fetch-tool summary |
| https://futurism.com/the-byte/amazon-ai-severe-hallucinations | Futurism (Victor Tangermann) | 2023-12-04 | Yes, fetch-tool summary |
| https://datacenterdynamics.com/en/news/amazons-q-generative-ai-chatbot-leaks-location-of-aws-data-centers | DatacenterDynamics | Not known | No. HTTP 403 |
| https://www.itbrew.com/stories/2023/12/08/q-amazon-s-new-generative-ai-is-reportedly-experiencing-severe-hallucinations | IT Brew | 2023-12-08, per URL | No. HTTP 403 |
| https://www.businessinsider.nl/amazons-ai-chatbot-q-might-be-in-the-throes-of-a-mental-health-crisis | Business Insider | Not known | No. Redirected to the home page |
| https://oecd.ai/en/incidents/2023-12-02-5a27 | OECD AI incident monitor | Not known | No. Search summary only |
| New York Times interview with Adam Selipsky | The New York Times | Not known | No. Quoted only via Futurism |

## Corrections

If you have Platformer's full article, the internal documents, or Amazon's account of what was fixed, tell us and we will fix this page.
