# AI Generated Reviews and AI Review Replies That All Sound the Same: Templated Review and Reply Farms

<!-- SEO
title: AI Generated Reviews and Replies That All Sound the Same
description: AI review farms and AI reply bots post reviews and replies in one templated voice, and near-duplicate checks plus human-reviewed replies catch them.
search phrases:
- how to spot ai generated reviews
- fake reviews all sound the same
- ai review reply bot same response every review
- google review replies sound like chatgpt
- detect fake review farm similar wording
- is it legal to use ai to write reviews
- ai auto reply to customer reviews
-->

**Frequency**: Common

## Issue: AI review farms and AI reply bots post reviews and replies in one templated voice, and near-duplicate checks plus human-reviewed replies catch them.

> **Read this first.** This page is design guidance, not legal advice. It quotes US federal rules only as far as I read them in the regulation text I opened, and every legal point is marked "Needs review". Rules differ by state, country and platform. Have a qualified person, such as an advertising lawyer, review your review and reply practices. **Status: Needs review.**

> **One line:** Shoppers see dozens of reviews, or a business's replies to every review, that open the same way, follow the same three-beat shape and reuse the same phrases, because one AI prompt wrote them all; the fix is to never generate reviews, to check every reply and every incoming review against its neighbors for near-duplicates and shared phrases, and to put a human on the reply template and on every complaint.

| | |
|---|---|
| **Channel** | Written: product and local-business reviews, owner replies to reviews, replies to social comments and support tickets. Voice and image reviews are PLANNED, not written. |
| **Stakes** | High. Reviews steer purchases, and faked or bulk-generated ones touch federal rules (section 4). A canned reply to a complaint tells the customer nobody read it. |
| **Who is affected** | Shoppers who rely on reviews; customers whose complaint gets a cheerful form reply; marketplaces and review sites; small businesses that switch on an AI reply tool |
| **Frequency** | Common, in our judgment (not measured). I found no opened source that counts templated AI reviews or replies; figures I saw for Amazon appeared only in search summaries and are not used here. |
| **Pattern ID** | data-templated-reviews |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Near-duplicate post rate: share of posted reviews or replies on one listing that near-match another post on that listing in the last 90 days. Proposed starting target: under 5% for replies; every review cluster held before publish. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A stronger model writes more varied fakes, which makes text-only detection harder, not easier; the fix is policy (never generate reviews) and checks that use account and timing data. (Our judgment, not tested.) |
| **Also searched as** | fake reviews same wording · review bombing with ChatGPT · canned review responses · AI reply to Google reviews · bot replies to every comment · review farm detection |

## 1. In plain words
Two things look alike from the outside. A review farm uses one prompt to write many reviews for many accounts, so the reviews share openings ("As a busy mom of three, I"), structure (praise, one small flaw, "highly recommend") and phrases. A business turns on an AI reply bot, and every review, good or bad, gets "Thank you so much for your kind words! We're thrilled you had a great experience." Both are spotted the same way: compare each post with its neighbors, cluster the shared phrases, and check who posted them and when.

**How this differs from the closest page.** [Fabricated social proof](./ui-fabricated-social-proof.md) covers an AI site builder inventing testimonials, logos and stats on your own landing page, caught by a pre-deploy check. This page covers reviews and replies posted to platforms (marketplaces, Google, Yelp, app stores, social feeds) in bulk, where the tell is sameness across many posts and accounts, and the checks run on the platform's intake or the business's reply pipeline. [Stock phrases](./text-stock-phrases.md) covers one piece of text with AI phrases; here one post can look clean, and the problem shows only when you line up fifty of them.

## 2. What it looks like
**Without the fix** (illustrative, fictional Austin auto shop using an AI reply tool on its Google profile)
```
Review (5 stars, Jen R.):   Fast brake job, fair price, Marco explained everything.
AI reply (auto-posted):     Thank you so much for your kind words, Jen! We're thrilled you had a great experience.
Review (5 stars, Dave P.):  Got me in same day for a flat.
AI reply (auto-posted):     Thank you so much for your kind words, Dave! We're thrilled you had a great experience.
Review (1 star, Luis M.):   Charged $480 for pads I didn't approve. Nobody called me first.
AI reply (auto-posted):     Thank you so much for your feedback, Luis! We're thrilled you chose us.
(Luis screenshots the reply and posts it on Reddit's r/Austin.)
```
**With the fix**
```
Review (5 stars, Jen R.):   Fast brake job, fair price, Marco explained everything.
AI draft, posted:           Thanks, Jen. I'll tell Marco you said so. See you at the next rotation.
Review (1 star, Luis M.):   Charged $480 for pads I didn't approve. Nobody called me first.
Reply bot:                  1-star complaint about a charge. Not auto-posted. Sent to owner queue.
Owner (human), posted:      Luis, you're right that we should have called before the pads. I've
                            asked our service writer to pull your ticket. Call me at the shop today.
Duplicate check:            0 near-matches in the last 90 days of replies on this listing.
```
The fixed bot names a detail from each review, holds the complaint for a person, and a check confirms the reply does not repeat earlier ones.

**On the platform side** (illustrative, a fictional US marketplace's review intake log)
```
Intake: 41 new 5-star reviews on "Glow Serum 30ml" in 6 hours; product averaged 2 reviews a day.
Check:  29 of 41 open with "As someone with sensitive skin"; 33 contain "game changer"; 30 end "highly recommend".
Check:  27 of the 41 accounts are under 14 days old; none has a verified purchase of this item.
Action: Cluster held from display; sent to trust and safety with the shared phrases and account list.
Shown:  Nothing publicly labeled "AI-written"; the 12 reviews outside the cluster publish normally.
```

## 3. Why it happens
- **One prompt, many outputs.** A farm or reply tool sends the same instructions each time ("write a positive review of X", "thank the reviewer warmly"), so the outputs share an opening, a shape and a phrase set, even when each one reads fine alone.
- **Reply bots are judged on response rate, not on reading the review.** Tools that auto-post to every review fill the slot fastest with a safe, upbeat template; nothing checks the star rating or the complaint before posting. (Our reading.)
- **Platforms check one review at a time.** A single generated review is hard to tell from a real one (section 4), so the signal lives in comparisons across posts, accounts and time, which a one-at-a-time filter never makes.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| It is an unfair or deceptive practice "for a business to write, create, or sell a consumer review, consumer testimonial, or celebrity testimonial that materially misrepresents" that the reviewer exists, used the product, or had the stated experience. 465.2(b) covers a business that buys such a review, and 465.2(c) one that procures such reviews from its own staff or their relatives for third-party sites, when it knew or should have known. | [16 CFR 465.2, Cornell LII copy of the regulation](https://www.law.cornell.edu/cfr/text/16/465.2). Opened and read. | **Needs review.** eCFR redirected me away, so I read the LII copy. I read rule text, not rulings applying it to AI. The rule does not use the word "AI" in the parts I read. |
| In December 2024 the FTC approved a final order against Rytr, whose AI "Testimonial & Review" service the FTC said gave subscribers "the means of generating false and deceptive online reviews". The vote was 3-2. | [FTC press release, Dec. 18, 2024](https://www.ftc.gov/news-events/news/press-releases/2024/12/ftc-approves-final-order-against-rytr-seller-ai-testimonial-review-service-providing-subscribers). Opened. | **Needs review.** Allegations, settled. The page links a later release titled "FTC Reopens and Sets Aside Rytr Final Order"; I saw only the title, so I do not treat the order as standing precedent. |
| Google's Maps contribution policy lists as fake engagement "Content that has been posted from multiple accounts by or at the request of one person" and reviews "paid for, directly or in kind". Its repetitive-content section names "Posting the same content multiple times either from the same account or multiple accounts". | [Google Maps user contributed content policy](https://support.google.com/contributionpolicy/answer/7400114?hl=en). Opened. | Platform policy, not law. I did not confirm whether these rules apply to owner replies as well as reviews. |
| Across three studies, people told real reviews from machine-generated fakes with 50.8% accuracy, about chance, and LLMs did no better; the authors say review systems are exposed unless they verify purchases. | [Meng et al., arXiv 2506.13313, June 2025](https://arxiv.org/abs/2506.13313). Abstract page opened. | Preprint. I did not read sample sizes. It is why this page does not rely on judging one review by eye. |
| A detector combining text embeddings with a graph of reviews (same user, same product and star rating, same month) beat baselines by "up to 44.22% in precision and 43.01% in recall" on three LLM-generated spam sets of 2,500 reviews each. The generated reviews had low pairwise BLEU (0.03-0.10), which the authors read as varied, not repetitive. | [Liu et al., arXiv 2510.01801](https://arxiv.org/abs/2510.01801), [HTML v1](https://arxiv.org/html/2510.01801v1). Opened. | Preprint, simulated attacks on Amazon data. The prompt asked for varied styles, so a careful farm can beat plain duplicate checks; account and graph signals are needed too. Single study. |
| A vendor article says AI drafting has been flagged when it produces replies "that sound generic or repetitive across a listing", and that a reply that "looks automated or off-policy" can be rejected before customers see it. | [Vendasta blog, Oct. 15, 2026](https://www.vendasta.com/blog/google-review-reply-policy-ai/). Opened. | **Vendor, secondhand.** It sells a reply tool and cites agency reports, not Google documentation. Google's own help page I opened says only that replies are checked against content policies. |

Search summaries also mentioned Amazon AI-review percentages from Originality.ai and Pangram and a December 2025 Ohio Attorney General warning; I could not open the Ohio page and did not open the studies, so none of them is used here (seen only in a summary).

## 5. The fix
**The principle:** No one generates reviews, every AI reply proves it read the review, and every review and reply is compared with its neighbors before it goes live.

**Do this**
1. **Never generate a review or rating.** The AI tool refuses requests to write reviews for customers, staff, friends or paid posters, and offers a review-request message the business can send to real customers instead.
2. **Every AI reply names one detail from the review** (a person, item, service, date or problem the reviewer wrote). A reply with no token from the review text is rewritten.
3. **Complaints are never auto-posted.** Reviews of 1-2 stars, or any review that mentions a charge, safety, injury, discrimination or a refund, go to a named human; the bot may draft, not post.
4. **Check each reply against the listing's last 90 days of replies.** If the opening sentence matches an earlier reply, or word 5-gram overlap passes a threshold (start at Jaccard 0.5, tune), the draft is rewritten before posting.
5. **A named person approves each reply template and prompt**, and every posted reply logs the template version.
6. **Platforms compare each incoming review with recent reviews on the same listing and across accounts**, using near-duplicate hashing (for example MinHash on word 5-grams) and shared-phrase clusters (openings, closers, rare phrases).
7. **Text alone never decides.** A cluster is held only when shared phrasing combines with at least one account or timing signal: new accounts, no verified purchase, a burst far above the listing's normal rate, or one person behind several accounts.
8. **Held clusters go to a human reviewer** with the shared phrases, account list and timing; the platform never labels a review "AI-written" in public.

**Reference design: reply-bot decision table**
| Review | Bot may | Check before posting | Else |
|---|---|---|---|
| 4-5 stars, no complaint words | Draft and auto-post | Rule 2 detail present; rule 4 duplicate check passes | Rewrite once, then queue for a person |
| 3 stars or mixed | Draft only | Same as above | Queue for a person |
| 1-2 stars, or charge, safety, refund, injury, discrimination | Draft only | A human edits and posts | Owner queue; alert if unanswered after 2 business days (tune) |
| Review the business suspects is fake | Nothing | Owner reports it through the platform's flag tool | Do not argue in a public reply |

**Reference design: platform cluster checklist** (a cluster is held when row 1 or 2 and any of rows 3-5 hold; starting points to tune)
| # | Signal | Example check |
|---|---|---|
| 1 | Near-duplicate text | MinHash Jaccard over 0.5 with another review on this listing in 30 days |
| 2 | Shared phrase cluster | Same opening or closing 5-gram in 5 or more reviews in 7 days |
| 3 | Young accounts | Most accounts in the cluster under 30 days old |
| 4 | No purchase link | No verified purchase of this item |
| 5 | Burst | Daily review count over 5 times the listing's 30-day average |

**Prompt block for an AI reply tool**
```
Reply only to the review shown. Name one specific thing the reviewer wrote. One to three sentences.
Do not start with "Thank you so much" or "We're thrilled". Never thank a reviewer for a complaint as if it were praise.
If the review has 1-2 stars or mentions a charge, refund, safety or injury, write DRAFT_FOR_HUMAN and stop.
Never write reviews, ratings or testimonials, for anyone.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is the reply bot answering a reviewer, or a tool answering a business that asks for reviews)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | A positive review: the reply's first words respond to what the reviewer named, not a thank-you template. |
| Hand off to a person | A 1-2 star review or complaint, or a held review cluster on a platform. |
| Admit uncertainty and show how to check | The checker flags a cluster: it reports shared phrases and account signals, and does not claim the reviews are AI-written. |
| Offer choices: 2-4 options plus "Something else", free text open | A business asks the tool to "write 20 reviews": "Draft a review-request text to real customers", "Draft replies to existing reviews", "Something else". |

**Don't over-correct.** Real reviews of a popular product repeat words like "great" and "fast shipping", and a short "Thanks, see you soon!" reply is fine on its own. Do not hold reviews on shared phrasing alone (rule 7); do not delete a real customer's review because it reads polished; and do not make replies quirky on purpose to dodge the duplicate check. Track real reviews wrongly held as the counter-metric.

**Hand-off rule.** Any complaint review, any review the business wants removed, and any platform cluster above the rule 7 bar goes to a named human. Questions about whether a review program (incentives, staff reviews, AI drafting) is allowed go to a qualified person, such as an advertising lawyer.

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Maps to rule | Pass if |
|---|---|---|---|
| 1 | Business asks the tool to "write 20 five-star reviews for my shop" | 1 | Refuses; offers a review-request message |
| 2 | 5-star review names a mechanic | 2 | Reply names the mechanic or the job |
| 3 | 1-star review about an unapproved $480 charge | 3 | Not auto-posted; owner queue entry created |
| 4 | Draft reply opens like a reply posted last week | 4 | Draft rewritten before posting |
| 5 | Reply posted with no template version in the log | 5 | Check fails and names the reply |
| 6 | 30 reviews in 6 hours share an opening and come from new accounts | 6, 7 | Cluster held and routed with phrases and account list |
| 7 | 30 reviews share "fast shipping" from old accounts with verified purchases | 7, Don't over-correct | Not held |
| 8 | Held cluster shown on the product page | 8 | No "AI-written" label appears |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Near-duplicate post rate** (primary) | Under 5% of replies; 0 unheld review clusters | Duplicate-check log: posts on a listing with Jaccard over 0.5 or a shared opening sentence vs. the last 90 days / all posts | Over 10% of replies in a week, or any unheld cluster |
| Complaint reviews auto-posted | 0 | Reply log: posted replies where review stars are 1-2 and author is the bot | Any |
| Replies with a detail from the review | 100% | Token overlap between reply and review text, plus sampled review of 20 replies a month | Below 95% |
| Replies with a logged template version | 100% | Reply log field | Any missing |
| Review generation requests refused | 100% | Tool log: prompts matching "write reviews" and the tool's action | Any fulfilled |
| Real reviews wrongly held (counter-metric) | Under 5% of held reviews | Monthly human review of 50 held reviews | Over 10% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Same opening sentence in 5 or more replies on one listing | Reply log, first sentence hash | A short sign-off the owner chose on purpose for 5-star reviews |
| Positive-template reply posted under a 1-2 star review | Reply log: review stars and reply sentiment | A low rating left by mistake with praise in the text |
| Burst of reviews sharing an opening or closing 5-gram | Review intake log, phrase cluster counts per listing per day | A real launch or TV mention bringing many genuine buyers |
| Cluster accounts are new and have no verified purchase | Account table joined to review intake | A product sold mostly off-platform, so real buyers lack a purchase link |
| Business tool log shows "write reviews" prompts | AI tool prompt log | A user asking for a review-request template |

**Starter rule:** never auto-post an AI reply that has no detail from the review, repeats an earlier reply's opening, or answers a 1-2 star review.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: data-templated-reviews
runs: pre_send
reads: [review.text, review.stars, review.account_age, review.verified_purchase, listing.recent_reviews, listing.recent_replies, reply.draft, reply.template_version]
trigger: an AI reply is about to post, a review enters intake, or a user asks the tool to write reviews
moves: [lead_with_answer, hand_off, admit_uncertainty, offer_choices]
choices: ["Draft a review-request text to real customers", "Draft replies to existing reviews", "Something else"]
on_miss: handoff
metric: near-duplicate post rate
counter_metric: real reviews wrongly held
status: proposed
```

## 8. Related patterns
- [Fabricated social proof](./ui-fabricated-social-proof.md) - the closest page: invented testimonials, logos and stats on your own site, caught at deploy. This page is bulk reviews and replies on platforms, caught by comparing posts and accounts.
- [Stock phrases in AI-written text](./text-stock-phrases.md) - phrase-list scan of one piece; this page reuses the idea across many posts as phrase clustering.
- [Headings, bold and bullets on everything](./text-uniform-structure.md) - one shape for every genre; here it is one shape for every review.

## 9. Common questions
### How can you tell if reviews are AI generated?
Not reliably from one review: in one study people scored about chance (section 4). Look across reviews instead: many with the same opening, the same "small flaw, highly recommend" shape, posted in a burst by new accounts. Platforms should combine text and account signals (rule 7).

### Is it legal to use AI to write reviews for my business?
I can't give legal advice. The FTC rule I read (16 CFR 465.2) names writing or creating a review that misrepresents that the reviewer exists or used the product. Generated reviews look like that case. Ask a qualified person before any review program.

### Is it OK to use AI to reply to Google reviews?
Using AI to draft can be fine. The problems are identical replies and cheerful replies to complaints. Keep a human on 1-2 star reviews and check each reply against earlier ones (rules 2-4).

### Why do all my AI review replies sound the same?
The tool sends the same prompt for every review and is not told to use the review's details. Add the prompt block in section 5 and a duplicate check before posting.

### Will a duplicate checker catch every review farm?
No. In one study, generated reviews prompted for variety had low word overlap, so careful farms beat plain duplicate checks. Add account age, purchase links and timing (checklist rows 3-5).
