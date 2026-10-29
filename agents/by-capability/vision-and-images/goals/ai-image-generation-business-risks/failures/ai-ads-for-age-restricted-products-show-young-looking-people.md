# AI-Generated People Who Look Underage in Alcohol, Vape and Gambling Ads: Checking Apparent Age Before Launch

<!-- SEO
title: AI People Who Look Under 25 in Alcohol and Gambling Ads: Apparent-Age Check
description: AI-made people in alcohol, vape and betting ads can look under 21 or 25 even when the prompt meant an adult. An apparent-age check before launch stops it.
search phrases:
- ai generated model looks underage in ad
- asa ruling ai generated character under 25
- alcohol ad models must be 25
- age of models in alcohol advertising
- sports betting ad models 21
- ai character gambling ad looks too young
- can ai generated people be used in alcohol ads
- meta ai images teen ads vaping alcohol
-->

**Frequency**: Occasional

## Issue: An alcohol, vape or gambling ad uses an AI-generated person who looks under 21 or under 25, because the prompt never set an age and nobody judged how old the person looks. Before launch, set an adult age floor in the prompt, have a person rate apparent age against each market's rule, log the rating, and keep anyone who reads as young out of a significant role.

> **Read this first:** This page summarizes a UK regulator ruling, UK advice, a watchdog test of Meta ads and three US industry codes, as the opened pages state them, read October 29, 2026. The UK rules come from the CAP Code, enforced by the ASA. The US alcohol and sports betting codes are voluntary industry codes that members agree to follow; they are not laws, and we opened no US law that sets an age for people shown in ads. We opened no source on model ages for tobacco, vape or cannabis ads in the US. This is design guidance, not legal advice. Which rule applies to a given ad needs review by a qualified person.

> **One line:** An affiliate makes a TikTok betting ad with an AI-generated young man, the prompt never mentions age, and the UK regulator finds he "seemed to be under 25"; the fix is an age floor in every prompt for an age-restricted ad, a logged apparent-age rating by a person against each market's rule, and a block on publish until that rating passes.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. The ASA ruling is about an AI-generated video; the Tech Transparency Project test used still images (section 4). |
| **Channel** | Paid social, display, video and print ads for alcohol, vape and tobacco, gambling and sports betting, and cannabis, made or edited with an image or video generator |
| **Stakes** | High. The ASA ruled against the Midnite ad and told both firms not to run it again. The US codes call for age floors for people shown. The harm the rules aim at is marketing age-restricted products to young people (section 4). |
| **Who is affected** | Young viewers the ad appeals to, the brand, the affiliate or agency that made the creative, and the regulator or code board that hears the complaint |
| **Frequency** | Occasional, by our reading. One opened ruling (UK, 2026) is about an AI-made person. No opened source gives a rate. |
| **Pattern ID** | ai-ads-for-age-restricted-products-show-young-looking-people |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Unrated age-restricted ad rate: live ads for age-restricted products that show an AI-generated or AI-edited person and have no logged apparent-age rating (prompt age floor, rater, rating, market rule) for that exact creative, divided by all such live ads sampled. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A model can follow an age floor in the prompt more reliably, but "looks under 25" is a human judgment the regulator makes, and no model knows which market's bar applies. (Our judgment, not tested.) |
| **Also searched as** | AI model too young alcohol ad · ASA AI gambling ad under 25 · beer ad model age rule · AI vape ad teens · betting ad influencer age 21 |

Tests: [AI ads for age-restricted products that show young-looking people test file](../../../tests/ai-ads-for-age-restricted-products-show-young-looking-people.md).

## 1. In plain words
Alcohol, gambling and betting ads have rules about who can appear in them. The UK bars anyone who is, or seems to be, under 25 in a significant role. US spirits, beer and sports betting codes set age floors and, for alcohol, say people must look over 21. With a real model, a team checks an ID. An AI-generated person has no ID and no age. The only test left is how old the person looks, and generators often make young, smooth-faced people when the prompt says nothing about age. So the check must move from "show me the ID" to "a person rated how old this looks, against this market's bar, before it ran."

## 2. What it looks like
The brand, people and IDs below are invented. The rules are the ones the opened pages describe (section 4).

**Without the fix**
```
Designer:  Make a 6-second video for the Fast Lane Sportsbook app: a guy at a Denver bar
           cheering at his phone during the game.
Generator: [Video FL-114: a smooth-faced man with a boyish haircut and a hoodie, cheering.]
Designer:  Looks great. Export for TikTok and Instagram, US and UK.
Ad tool:   FL-114 attached to 4 ads. Published.
Complaint: "The guy in this betting ad looks about 18."
Brand:     "He isn't real, so he has no age." (No one rated how old he looks.)
```
**With the fix**
```
Designer:  Make a 6-second video for Fast Lane Sportsbook: a guy at a Denver bar cheering at his phone.
Ad tool:   Product class: sports betting. Prompt age floor added: "adult clearly in his 30s."
           Markets: US (AGA code: 21+) and UK (CAP: must not seem under 25).
Generator: [Video FL-115: a man with light stubble and crow's feet, cheering.]
Ad tool:   Apparent-age rating needed before publish. Rater J. Ortiz: "reads 30 to 35." Passes US and UK.
           Logged: prompt, age floor, rater, rating, rules read Oct 29. Publish?
Designer:  Yes.
```
In the fixed version the prompt sets an age floor, a named person rates apparent age against each market's bar, and the log keeps the evidence the ASA said it had not seen in the Midnite case.

## 3. Why it happens
- **An AI person has no age to prove.** The industry codes lean on IDs: models "a minimum of 25 years old, substantiated by proper identification" (spirits), "a minimum of 21 years old, substantiated by proper identification" (sports betting). A generated person cannot show one. The ASA advice says even a real, proven 25-year-old can breach the rule if they look younger. For AI people, apparent age is the whole test.
- **The prompt never says how old.** In the Midnite case the affiliate said "the prompt used to generate the ad did not specify the age of the character." With no age in the prompt, the generator picks the look; the ASA described "youthful facial features, smooth skin and a boyish hairstyle."
- **The maker is not the brand.** Midnite said it had not approved the ad, which an affiliate made. When affiliates, agencies or platform AI tools make creative, the brand's age check never runs on it.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A paid TikTok ad for Midnite, seen July 3, 2026, showed a man using a gambling app. The affiliate said he was "an AI-generated fictional character," "intended to depict an adult," and the prompt "did not specify the age." The ASA found "youthful facial features, smooth skin and a boyish hairstyle" and that he "seemed to be under 25." It noted the prompt "did not refer to the character's age or to the age restrictions that applied to gambling advertising." Breach of CAP Code (Edition 12) rules 16.3 and 16.3.14; ruling dated September 16, 2026. | [ASA ruling on Dribble Media Ltd t/a Midnite](https://www.asa.org.uk/rulings/dribble-media-ltd.html). Opened and read Oct. 29, 2026; quotes string-matched. | UK, not US. One ruling. The ad was online "for only a few hours." |
| The affiliate said its new safeguards include "specifying age-related prompts, reviewing characters specifically for perceived age," "avoiding styling or facial features that could suggest" someone under 25, and "retaining records of the AI-generation and approval process." | Same ASA ruling. Opened; quotes string-matched. | The advertiser's own account. The ASA did not test these safeguards. |
| Trade press reported the same ruling. CMS says the CAP rules on people who appear under 25 will be applied to AI-generated characters too; iGaming Business says Midnite ended its contract with the affiliate. | [CMS legal update, Oct. 9, 2026](https://cms.law/en/gbr/legal-updates/asa-rules-that-ai-generated-character-in-gambling-ad-appeared-to-be-under-25); [iGaming Business, Kathryn Evans, Sept. 17, 2026](https://igamingbusiness.com/marketing-affiliates/asa-complaint-midnite-ai-generated-character-tiktok-ad/). Both opened through the fetch tool. | Secondary. A law firm's reading and a trade report, not the ASA's words. |
| UK alcohol ads (CAP rule 18.16) may not show "in a significant role people who are, or appear to be, under the age of 25." Under-25s in the background "should not be playing a significant role and they should be obviously not drinking." "Even if those featured are technically over 25 and this can be proved, if they look younger" the ad could still breach. | [ASA/CAP advice, Alcohol: featuring under-25s, July 18, 2024](https://www.asa.org.uk/advice-online/alcohol-featuring-under-25s.html). Opened; quotes string-matched. | UK. CAP advice, which the page says does not bind the ASA. Not about AI. |
| Tech Transparency Project asked Meta's AI tool for "smiling young people using vape pens," made ads from the images and others (alcohol, gambling, pills), targeted them at "users aged 13 to 17," and Facebook approved them, the vape ad "within minutes." TTP canceled the ads before they ran. "Meta did not respond to a request for comment." | [Tech Transparency Project, Jan. 30, 2024](https://techtransparencyproject.org/articles/meta-approves-harmful-teen-ads-with-images-from-its-own-ai-tool). Opened; quotes string-matched. | A watchdog's test with deliberately bad ads, not a brand's mistake. Shows the platform review will not catch it for you. |
| US spirits: models and actors "should be a minimum of 25 years old, substantiated by proper identification, and should reasonably appear to be 21 years of age and older." DISCUS members "have voluntarily abided by" the code. | [Distilled Spirits Council Code of Responsible Practices, 2023 PDF](https://www.distilledspirits.org/wp-content/uploads/2023/06/DISCUS_CodeofResponsiblePractices_2023.pdf). Opened; text extracted and quotes string-matched. | Voluntary trade code, members only. No AI provision. |
| US beer: the code "requires models and actors photographed for ads to be over 25 and appear to be older than 21," and calls these "voluntary restrictions." | [Beer Institute, The Ad Code, May 14, 2026](https://www.beerinstitute.org/the-ad-code-a-longstanding-commitment-to-responsibility/). Opened through the fetch tool. | Voluntary trade code, the institute's own summary, not the full code. No AI provision. |
| US sports betting: "Models, actors, influencers, athletes and entertainers appearing in advertising should be a minimum of 21 years old, substantiated by proper identification." | [American Gaming Association, Responsible Marketing Code for Sports Wagering, updated March 28, 2023](https://www.americangaming.org/wp-content/uploads/2025/03/AGA-Responsible-SB-Marketing-Code.pdf). Opened; quotes string-matched. | Voluntary members' code. It sets an age by ID but no "appears to be" test, so it says nothing direct about AI people. |

**Read only through summaries (not used in the fix):** search summaries described a 2013 UConn-led study of beer ads in college basketball broadcasts and a UK trade report that one in 10 alcohol ads could break the under-25 rule; we did not open either. We opened no source on US tobacco, vape or cannabis rules for the age of people shown in ads, so those markets have no row in the reference design until counsel fills one.

## 5. The fix
**The principle:** For an AI-made person, apparent age is the only age there is, so a named person rates it against each market's bar before the ad runs, and the rating is logged.

**Do this: brands, agencies, affiliates and ad tools**
1. **Tag the product class.** Every ad brief and creative records whether the product is age-restricted (alcohol, including no- and low-alcohol lines; tobacco and vape; gambling and betting; cannabis) and its markets. Untagged creative cannot be attached to an ad.
2. **Put an age floor in every prompt that makes a person for an age-restricted ad.** The tool adds it if the user did not, for example "adult clearly in their 30s." Never accept "young," "teen," "college," "student" or "fresh-faced" in these prompts.
3. **Rate apparent age with a person, not with the prompt.** A named rater who did not write the prompt records an apparent age range for each prominent person. The prompt's age floor is not evidence the person looks that age.
4. **Check the rating against each market's row.** Use a counsel-kept table: UK alcohol and gambling, must not seem under 25; US spirits and beer codes, must reasonably appear 21 or older; US sports betting code, 21 by ID, which an AI person cannot show, so treat it as an appearance check. Where markets differ, the strictest bar applies to the shared creative (our judgment).
5. **Fail anyone near the line.** If the rated range touches the bar (for example "22 to 27" against a 25 bar), the person fails. Regenerate with an older floor or remove them from a significant role.
6. **Check styling, not just faces.** School settings, cartoon styles, toys, candy colors and juvenile behavior fail the check even when the face reads older (the ASA advice warns about people "behaving in an adolescent or juvenile way").
7. **Re-rate every edit and every frame.** In video, rate the youngest-looking frame. Any regeneration, face edit, platform AI enhancement or crop that makes a background person prominent reruns rule 3.
8. **Run the check on affiliate and agency creative too.** Brand-name creative from a partner does not run until the partner's log shows rules 2 to 5, or the brand runs them.
9. **Log every check.** Creative ID, product class, markets, prompt and age floor, rater, rated range per person, rule row and date, decision. This is the record the ASA said it had not seen.
10. **Pull and hand off on a complaint.** A complaint or regulator letter about apparent age pauses the creative in every market the same day and goes to the owner and counsel with the log.

**Reference design: apparent-age check (one row per prominent person, filled before publish)**
| Field | Example | Pass if |
|---|---|---|
| Product class and markets | Sports betting; US, UK | Tagged |
| Prompt age floor | "adult clearly in his 30s" | Present; no youth words |
| Rater (not the prompt author) | J. Ortiz | Named |
| Rated apparent age, youngest frame | 30 to 35 | Lower end above the strictest market bar, with a margin |
| Styling check | Bar, stubble, adult clothing | No school, cartoon, toy or juvenile cues |
| Rule rows used, date read | UK CAP 16.3; AGA code; Oct 29 | Counsel-kept rows, re-read within 90 days (proposed interval) |
| Decision | Publish | Rules 3 to 6 all pass |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The tool says first which markets apply and the bar for each |
| Offer choices: 2-4 options plus "Something else" | A rating fails: regenerate older, move the person to the background, use no person, something else |
| Ask one clarifying question | The creative has no product class: "Is this product age-restricted, and in which markets will it run?" |
| Hand off to a person | A complaint, a regulator letter, or a market with no rule row |

**Don't over-correct.** Do not ban people from age-restricted ads; adults who clearly read as older pass. Do not age every person into their 50s or add gray hair to everyone; that is a stereotype of its own (our judgment). Under-25s may appear in the UK in non-significant roles, not drinking, per the ASA advice. Do not run this check on products that are not age-restricted. A face detector's age guess may help a rater, but it never replaces the person's rating.

**Hand-off rule.** A complaint, regulator contact, a rating on the line that the team wants to run anyway, or a market with no rule row goes to the campaign owner and counsel with the check log. The creative does not run in that market until they decide.

**Framework used:** none yet. Rules 3 to 6 follow the ASA ruling and advice and the US codes in section 4; rules 2 and 9 match the safeguards the affiliate listed after the ruling; the rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-ads-for-age-restricted-products-show-young-looking-people.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Beer ad creative with no product class | Blocked until tagged | 1 |
| 2 | Betting ad prompt with no age | Age floor added before generating | 2 |
| 3 | Vape ad prompt says "college students" | Rejected and rewritten | 2 |
| 4 | Rater is the prompt author | Check not accepted | 3 |
| 5 | Shared US and UK alcohol creative rated "23 to 28" | Fails the UK bar | 4, 5 |
| 6 | Adult face in a school-hallway setting | Fails the styling check | 6 |
| 7 | Affiliate betting video with no log | Held until checked | 8 |
| 8 | Complaint about apparent age | Paused in every market the same day | 10 |
| 9 | Adults clearly in their 40s in a wine ad | Passes with no added steps | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unrated age-restricted ad rate** (primary) | 0 (proposed) | Weekly sample of 100 live age-restricted ads with AI people: no rating row for that creative / all sampled | Any |
| Prompts for age-restricted ads with no age floor | 0 (proposed) | Prompt log joined to product class | Any |
| Ratings where rater wrote the prompt | 0 (proposed) | Check log query | Any |
| Partner creative live with no log | 0 (proposed) | Ad export joined to check log by creative ID | Any |
| Age complaints per 100 age-restricted AI ads | Falling month over month (proposed) | Complaint log | Any rise |
| Ratings failed and later run unchanged | 0 (proposed) | Check log vs. live creative hash | Any |
| Adult creative rejected on review (counter-metric) | Under 10% of checks (proposed) | Monthly sample of failed checks | Over 25% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Youth words ("teen," "college," "young," "fresh-faced") in a prompt for an age-restricted ad | Prompt log | Words describe the product's history or a brand name |
| Age-restricted creative with a person and no rating row | Asset record vs. check log | No prominent person; product-only shot |
| Comments or complaints saying the person "looks 16" or "looks like a kid" | Ad comments, complaint inbox | Joke or trolling on an ad whose rating passed with margin |
| Creative appears under the brand from an unknown partner account | Ad library search on brand name | An approved affiliate using a new account |
| Rated range within 3 years of the bar (proposed margin) | Check log | Rater was cautious; a second rater reads older |

**Starter rule:** no ad for an age-restricted product that shows an AI-made person goes live without a logged apparent-age rating by a person who did not write the prompt.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-ads-for-age-restricted-products-show-young-looking-people
runs: [on_prompt, pre_publish, on_edit, on_complaint]
reads: [brief.product_class, brief.markets, prompt.text, asset.people, rating_log, market_rule_table]
trigger: age-restricted creative showing a person with no age floor in the prompt, no rating, or a rating at or below the strictest market bar
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Regenerate with an older age floor", "Move the person out of a significant role", "Use no person", "Something else"]
on_miss: block_publish
metric: unrated age-restricted ad rate
counter_metric: adult creative rejected on review
status: proposed
```

## 8. Related patterns
- [Ad platforms that reject or label AI-generated ads](./ad-platforms-reject-or-label-ai-generated-ads.md) - the closest sibling. It covers each platform's AI disclosure setting. This page covers who appears in the ad and how old they look; a correct AI label does not fix a person who looks 17, and platform ad review approved teen-targeted AI vape ads in the TTP test.
- [AI images in ads published without review](./ai-images-in-ads-published-without-review.md) - the general sign-off step. This page adds the specific apparent-age check that sign-off must include for age-restricted products.
- [AI-generated ad disclosure rules not met](./ai-generated-ad-disclosure-rules-not-met.md) - market laws on AI labels; the market rule table here sits next to that page's register.
- [Child user treated as adult](../../../../human-machine-interface/goals/age-adaptation/failures/child-user-treated-as-adult.md) - the chat-side age failure: a bot misjudges the user's age. Here the business misjudges the age of a person it made.
- [Semantic drift in generated images](../../generation-artifacts/failures/semantic-shift.md) - the older page on outputs drifting from the prompt's intent; it does not cover age or ad rules.

## 9. Common questions
### Can I use AI-generated people in alcohol or betting ads?
The opened codes and the ASA ruling do not ban it. But an AI person has no ID, so the only test left is how old they look. In the UK they must not seem under 25; the US spirits and beer codes say people must reasonably appear 21 or older.

### The AI person isn't real, so how can they be "underage"?
The ASA ruled on exactly this in September 2026. It accepted the man was AI-made and meant to be an adult, and still found he "seemed to be under 25" from his face, skin and hair.

### Do models in US alcohol ads have to be 25?
Under the DISCUS spirits code and the Beer Institute code, models and actors should be at least 25 and look over 21. These are voluntary industry codes for members, not laws we found.

### Is it enough to write "adult" in the prompt?
No. The affiliate in the Midnite case now puts age in prompts, but a person still has to rate how old the output looks, and log it.

### Will Meta or TikTok catch it?
Do not count on it. In the Tech Transparency Project test, Facebook approved AI-made vape and alcohol ads aimed at 13- to 17-year-olds.
