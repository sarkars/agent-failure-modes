# AI Images Published With No Approval Step: Anyone Who Generates an Image Can Post It

<!-- SEO
title: No Approval Step for AI Images: Who Can Post What Your Business Generates
description: The person, agency or ad platform that makes an AI image can also publish it, with no second person. How to split generate and publish rights and gate them.
search phrases:
- social media manager posted ai image without approval
- marketing agency posted offensive ai image apology
- how to set up approval workflow for social media posts
- google ads generated images turned on by default
- turn off google ads image enhancement performance max
- meta business suite give access without publish rights
- small business ai image backlash
- who should approve ai images before posting
-->

**Frequency**: Common

## Issue: The person, agency or ad platform that makes an AI image can also publish it, so nobody else sees it before customers do. Split "can generate" from "can publish", require a second named person to release any AI-made image, and give platform AI tools no publish rights until a person turns them on.

> **Read this first:** This page describes platform settings and company statements as the cited sources report them. It does not say what any law requires about approving or labeling AI images in ads. That needs review by a qualified person, such as an advertising lawyer, before anyone relies on it. The rules below are workflow and product choices, not legal conclusions.

> **One line:** An agency, an owner or a platform's AI tool makes an image and posts it in the same step, because whoever can create content can also publish it; the fix is a publish permission held by someone other than the generator, a release step for every AI-made image, and platform AI generation that starts with no right to run.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. Every opened source is about still images on social posts and ads. Google's automation list includes animated images made from other assets, but no opened incident involves video. |
| **Channel** | Business social accounts, ad accounts (Meta, Google Ads), agencies and freelancers with account access, and the platforms' own AI asset tools |
| **Stakes** | Medium to high. A post with an AI Jeffrey Epstein went out on a cafe's official account; a bagel shop drew public backlash; an AI ad ran for days before customers told the brand (section 4). |
| **Who is affected** | Customers who see the post, the business, its agency, and anyone shown in the image |
| **Frequency** | Common, by our reading: two small-business incidents in May 2026 and several brands in one January 2026 report (section 4). No opened source gives a rate. |
| **Pattern ID** | ai-images-published-with-no-approval-step |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | Businesses that use AI images and video in ads, listings and operations do not mislead customers, break platform or market rules, or get defrauded by fake images. |
| **Primary metric** | Self-released AI image rate: published AI-made or AI-edited images whose publisher was also the generator (person, agency or platform tool), divided by all published AI images sampled. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Who holds the publish button is an account permission, not a model output. A better model makes fewer odd images but cannot tell that a caption about Epstein is in bad taste for a cafe. (Our judgment, not tested.) |
| **Also searched as** | agency posted without approval · ai post deleted apology small business · google ads auto generated images · meta page access content permission |

Tests: [AI images published with no approval step test file](../../../tests/ai-images-published-with-no-approval-step.md).

## 1. In plain words
A bakery hires an agency to run its Instagram. The agency makes a joke post with AI images of famous "customers" and posts it from the bakery's account. Nobody at the bakery sees it first. In another shop the owner makes the AI images and posts them himself. On ad platforms, the platform's own AI tool can make new image versions and run them. In each case one party both made the image and released it.

## 2. What it looks like
The cafe, agency and people below are invented. The settings follow the sources in section 4.

**Without the fix**
```
Agency staffer: (in the scheduling tool) Generate 4 images: famous people eating at Elm Street Bakery, busy weekend vibe.
Tool:           4 images ready.
Agency staffer: Post image 3 to @elmstreetbakery now. Caption: "POV: it was a really busy weekend."
Tool:           Posted to @elmstreetbakery.
                (Two hours later, a customer comment)
Customer:       "Why is a convicted criminal in your bakery ad??"
Owner:          "Who posted this? I never saw it."
```
**With the fix**
```
Agency staffer: (in the scheduling tool) Generate 4 images: famous people eating at Elm Street Bakery, busy weekend vibe.
Tool:           4 images ready. They show real, recognizable people. AI-made images on
                @elmstreetbakery need release by the account owner. Choose one:
                1) Send image 3 to Dana Ruiz (owner) for release  2) Regenerate with no real people
                3) Something else
Agency staffer: 1.
Tool:           Sent. Status: waiting for release. Your role can draft but not publish AI images here.
Dana Ruiz:      Rejected: "No real people. Use our own photos."
```
In the fixed version the generator cannot publish, the tool names who can, and the owner's decision is logged.

## 3. Why it happens
- **Create and publish are one permission.** Meta's Page access lists a "Content" task as "Create, manage or delete posts" and an "Ads" task as "Create, manage and delete ads," with no separate approve step (read on a third-party mirror of Meta's help pages). Anyone given the task to make content can also post it.
- **The platform's AI is a generator that starts with run rights.** Google's API documentation lists image enhancement for Performance Max and design versions for Demand Gen ads as enabled by default. Advertisers told Business Insider that Meta's settings switched on again after they turned them off (Shopifreaks). The tool that makes the image is allowed to run it unless someone acts.
- **Small teams have no second person.** The Vermont bagel shop had no full-time marketing team, and the owner posted himself. The Sydney cafe's agency posted on the cafe's account. With one person or one outside party holding the login, there is nobody positioned to say no.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Non-US (Australia). Stoneground Bakery in Hunters Hill, Sydney, posted AI images of "patrons" including an AI Jeffrey Epstein on its official Instagram. The post was created by marketing agency Élever Media. The cafe called it a "breakdown in our processes," "in bad taste and insensitive," and said it removed the post "very quickly." | [PEDESTRIAN.TV, Tom Disalvo, May 20, 2026](https://www.pedestrian.tv/news/stoneground-bakery-sydney-cafe-jeffrey-eptein-post/). Opened and read. | Entertainment news site. It does not say which person posted or whether the cafe had any review step. |
| Myer's Bagels in South Burlington, Vermont, posted ads mixing real photos with AI images. The owner, Adam Jones, said it is "a small business with no full-time marketing team," took the AI photos down and apologized, and said he will post "in a much more well-managed way from my end." | [WCAX, Ike Bendavid, May 6, 2026](https://www.wcax.com/2026/05/06/south-burlington-bagel-shop-faces-backlash-over-ai-generated-advertisement/). Opened and read. | Local TV report. PetaPixel's follow-up (May 11, 2026) returned 403 and was not read. |
| Google's help page says "Google may also suggest generated images for you to review," "You're in control," and advertisers "should review any generated or suggested assets." Once an image is used in a campaign, "you won't be able to hide it." | [Google Ads Help, About generated images in Google Ads](https://support.google.com/google-ads/answer/14150986?hl=en). Opened and read. | The page does not say whether suggestions are on by default or how to turn them off. |
| Google's API reference lists image enhancement (Performance Max) and design versions for images (Demand Gen multi-asset ads) as "Enabled" by default; the account-level image extraction control "can only be configured in the Google Ads web interface." | [Google Ads API, Asset automation settings](https://developers.google.com/google-ads/api/docs/assets/asset-automation-settings). Opened and read. | Developer docs; the web interface may show these differently. Defaults may change by API version. |
| Advertisers said Meta's Advantage+ and "automatic adjustments" settings were auto-enabling. True Classic's marketing head denied being able to preview an AI ad before it went live. A Meta spokesperson said advertisers using its full image generation feature "have the opportunity to review the generated images." | [Shopifreaks, Paul Drecksler, Jan. 5, 2026](https://www.shopifreaks.com/meta-advantage-is-forcing-unwanted-ai-creative-on-brands/). Opened and read. | Summary of Business Insider reporting, which we did not open. |
| Meta's Page access lists six partial-access tasks; "Content" is "Create, manage or delete posts" and "Ads" is "Create, manage and delete ads for the Page." No approve-only task is listed. | [Mirror of Meta Business Help Center, About Page access](https://support.chatarchitect.com/books/meta-business-portfolio-setup/page/about-page-access). Opened and read. | A third-party copy, not facebook.com. Read through a mirror only; menus may differ. |

**No US intern or junior-staff case found.** A search for an intern or junior staffer posting an AI image without approval found no matching report; the cases above are an agency, an owner and platform tools.

## 5. The fix
**The principle:** Whoever makes an AI image is not the one who releases it, and a platform's AI tool is a generator with no right to run.

**Do this: businesses, agencies and the tools they use**
1. **Split generate from publish.** In the social, scheduling and ad tools, the roles that can generate or draft images cannot publish an AI-made or AI-edited image. Agencies and freelancers get draft rights by default.
2. **Name a releaser who is not the generator.** Every AI image needs release by a named person other than the one who made it. The log records generator, releaser and time.
3. **Show who can release at the block.** When a draft is blocked, the tool names the releaser and offers to send it, so the block does not become a workaround hunt.
4. **Treat the platform's AI as a generator.** Turn off platform image generation and enhancement (Google image enhancement, design versions; Meta enhancements) at account and campaign level. A setting turned on needs a named releaser for each generated image.
5. **Re-check run rights on every new campaign.** New and duplicated campaigns are checked for AI automation that is on by default before launch.
6. **Flag real people and sensitive subjects.** A recognizable real person, a crime, a tragedy or a politician in an AI image sends it to the owner, not a delegate.
7. **Give the one-person shop a delay.** When no second person exists, an AI image waits a set time, such as overnight, and the owner re-reads it from a phone preview before it posts.
8. **Write the agency contract to match.** The agency agreement says agency staff draft AI images and the business releases them, with a named contact.
9. **Audit access monthly.** List everyone and every agency with publish rights on each account; remove publish rights not tied to a releaser role.

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | A generator tries to post an AI image: send for release, regenerate, something else. Every option keeps the gate; never offer "post anyway." Do not offer choices when only one path exists, such as an agency with no releaser set; say who must set one up. |
| Ask one clarifying question | The tool cannot tell if an image is AI-made: "Was this made or edited with an AI tool?" |
| Admit uncertainty and show how to check | The tool cannot tell if a face is a real person; say so and send it to the owner |
| Hand off to a person | Real people, crimes, tragedies or politicians appear, or a released post draws complaints |

**Don't over-correct.** Real photos the business took do not need the AI release step. Resizing, cropping and color correction are not AI generation. The releaser can be fast: one tap from a phone. Do not take publish rights from the owner of a one-person shop; give them the delay in rule 7. Do not ban AI images; the failure is that nobody else looked.

**Hand-off rule.** An AI image with a real person or a sensitive subject, or any released post that draws a complaint, goes to the account owner with the image, prompt, generator and releaser. The post stays unpublished, or is hidden, until the owner decides.

**Framework used:** none. Rule 1 is the separation-of-duties idea applied to posting; rules 4 and 5 follow the Google and Meta sources; the rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-images-published-with-no-approval-step.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Agency draft role tries to publish an AI image | Blocked; releaser named | 1, 3 |
| 2 | Generator tries to release own image | Blocked | 2 |
| 3 | New Performance Max campaign with image enhancement on by default | Caught before launch | 4, 5 |
| 4 | AI image shows a recognizable real person | Goes to owner, not delegate | 6 |
| 5 | One-person shop posts an AI image | Delay and preview applied | 7 |
| 6 | Real shop photo, color corrected | Posts with no AI release | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Self-released AI image rate** (primary) | 0 (proposed) | Weekly sample of published AI images: generator equals releaser, or no releaser / all sampled | Any |
| Accounts where a draft or agency role can publish | 0 (proposed) | Monthly access export per account | Any |
| Live campaigns with platform AI generation on and no releaser | 0 (proposed) | Campaign settings export joined to release log | Any |
| Median time from release request to decision | Under 1 business day (proposed) | Release log timestamps | Over 2 business days |
| Real photos wrongly sent to AI release (counter-metric) | Under 5% of release requests (proposed) | Monthly review of requests | Over 15% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| The account that generated an image is the account that posted it | Tool audit log | The owner of a one-person shop posting after the delay |
| An agency login publishes directly, not through a release queue | Platform activity log | A real photo the agency was allowed to post |
| A new campaign has image enhancement or design versions on | Campaign settings export | The team turned it on and set a releaser |
| A post is deleted within hours of going live | Account activity log | A typo fix and repost |
| Comments name a real person or call the image AI | Comment feed | A joke about AI in general |

**Starter rule:** no AI-made or AI-edited image is published unless a named person other than its generator released it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-images-published-with-no-approval-step
runs: [pre_publish, campaign_launch, monthly_audit]
reads: [asset.ai_origin, asset.generator, asset.releaser, user.role, platform.asset_automation_settings, image.real_person_flag]
trigger: generator equals releaser, no releaser, draft role publishes, or platform generation on with no releaser
moves: [offer_choices, ask_clarifying_question, admit_uncertainty, hand_off]
choices: ["Send to the releaser", "Regenerate with no real people", "Something else"]
on_miss: block_publish
metric: self-released AI image rate
counter_metric: real photos wrongly sent to AI release
status: proposed
```

## 8. Related patterns
- [AI images in ads published without review](./ai-images-in-ads-published-without-review.md) - the closest existing page. It covers approving the exact version that runs, platform enhancements that change an approved file, and checking the live ad. This page covers who holds the publish button: create and publish bundled in one role, agencies posting directly, and platform AI tools that start with the right to run.
- [AI image mistakes in ads that go viral](./ai-image-mistakes-in-ads-go-viral.md) - what happens after release; this page is the gate before it.
- [AI scribe notes signed without review](../../../../human-machine-interface/goals/healthcare-agents/failures/notes-approved-without-being-read.md) - the same shape: the step that should be a second look is missing or a formality.

## 9. Common questions
### How do I stop my agency from posting without my approval?
Give the agency draft rights only, name yourself as releaser in the scheduling tool, and put the release step in the contract.

### Does Google Ads make images for my ads automatically?
Google's help page says it may suggest generated images to review. Its API docs list image enhancement for Performance Max as enabled by default. Check each campaign's asset settings.

### Can I give someone access to my Facebook Page without letting them post?
Meta's Page access, as copied on a third-party help mirror, bundles create and delete into one "Content" task. Use a scheduling tool with an approval queue if you need draft-only access.

### I run a one-person business. Who approves my posts?
Use a delay: wait overnight and re-read the post on your phone before it goes out. Ask a trusted person if it shows a real person or a sensitive subject.

### Is it illegal to post AI images without approval?
This page does not answer legal questions. Get review from a qualified person.
