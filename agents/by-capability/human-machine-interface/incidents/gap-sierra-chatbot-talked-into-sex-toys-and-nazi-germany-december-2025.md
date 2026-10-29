---
title: "Gap.com Chatbot Talked Into Sex Toys and Nazi Germany After Guardrails Were Misconfigured, December 2025"
date: 2025-12-04
source: "https://www.theinformation.com/briefings/gap-com-chatbot-targeted-abuse-bad-actor-ai-startup-sierra-says"
description: "In late 2025, users got Gap's new Sierra-built shopping chatbot to discuss sex toys and Nazi Germany. Sierra blamed misconfigured guardrails."
summary: "On December 4, 2025, The Information reported that a chatbot Gap Inc. had launched the week before to answer product questions on Gap.com ended up discussing intimacy products, sex toys and Nazi Germany. Sierra, the AI startup behind the bot, blamed a bad actor trying to jailbreak over a dozen of its clients' agents. Sierra said its abuse detection stopped every attempt except the one on Gap, because Gap's guardrails had been inadvertently misconfigured. eMarketer reported the guardrails were then correctly configured and the bot stayed live. No opened source carries a statement from Gap. Status: Needs review."
categories:
  - Customer Service
  - Trust
  - Security
patterns:
  - small-talk-and-off-topic-messages-handled-badly
---

**This page is a dated teardown of one public case, a clothing retailer's new shopping chatbot that strangers steered into sex toys and Nazi Germany, for teams that launch a narrow-purpose chatbot on a store website through an outside vendor.** The product was the chatbot on Gap.com, built on technology from the AI startup Sierra. The users were people who set out to push it off topic. The moment was launch week: the vendor's own account is that its defenses were on for other clients but not for this one. Every fact below comes from a source we opened (listed at the end). We did not see any transcript or screenshot, so we quote nothing the bot said.

**Status: Needs review.** On 2026-10-30 we downloaded each cited page as raw text and matched every quote below against that text by script. The Information's article is paywalled; we read only its headline, byline, date and the opening lines in the page's description field. eMarketer's article was read in full. Vibe Graveyard is an incident-tracker site with no named author; we use it only for claims we label as its own. We did not open any post on X or any screenshot.

**Why the slug says December 2025.** The Information published on December 4, 2025, and says the bot launched "Last week." That puts the launch in late November 2025. We date the page by when the failure first became public, as the sibling teardowns do.

## What happened (as reported)

- **The bot.** The Information (Kevin McLaughlin, December 4, 2025) says: "Last week, Gap Inc. launched a chatbot to field product-related questions from Gap.com visitors."
- **What it talked about.** The same lines say the chatbot "ended up discussing topics that fell outside the scope of questions it was supposed to handle, including intimacy products, sex toys, and Nazi Germany, according to a person with knowledge of the matter."
- **The outlet reproduced it.** "The Information reproduced some of the results Thursday." We could not read past the paywall, so we do not know which prompts or replies it reproduced.
- **How fast.** eMarketer (Rachel Wolff, December 5, 2025), citing The Information, says users tricked the bot into these topics "fairly quickly after launch."
- **The headline framing.** The Information's headline is "Gap.com Chatbot Was Targeted For Abuse By ‘Bad Actor,’ AI Startup Sierra Says."
- **Harm reported.** No opened source reports harm to a shopper. Vibe Graveyard (June 24, 2026) says "No data was breached" and calls the damage one to brand safety. It gives no source for the data claim that we could open.

## What Sierra said

Sierra's head of communications, Rachel Whetstone, spoke to The Information. We read her words only as eMarketer reports them:

- Sierra blamed a "bad actor" that "has been attempting to maliciously jailbreak over a dozen" of its clients' AI agents, starting the week before.
- eMarketer says Sierra's built-in abuse detection stopped all of those attempts except the one on Gap. It missed Gap because the agent's guardrails had been "inadvertently misconfigured," Whetstone said.
- eMarketer adds: "Those guardrails have since been correctly configured, and the chatbot remains accessible to users."

No opened source carries a statement from Gap.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Launch date | The Information: "Last week," published December 4, 2025. Vibe Graveyard: late November 2025. Neither gives a day. |
| Nazi Germany | The Information's lines and Vibe Graveyard name it. eMarketer lists "intimacy products, sex toys, and other topics" and does not name it. |
| What the bot actually said | No opened source we could read prints a prompt or a reply. The Information says it reproduced some results, behind its paywall. |
| Who did it | Sierra calls it one bad actor running a coordinated campaign. No opened source names the person or shows that only one person was involved. Users beyond that actor are not described. |
| An apology | Vibe Graveyard says Sierra co-founder Bret Taylor "reportedly apologized to the brand." eMarketer and The Information's opening lines do not mention an apology. A vendor blog says Gap apologized publicly (see Unverified). |
| What was misconfigured | Sierra says "guardrails." No opened source says which setting, who set it, or how long it was wrong. |
| When it was fixed | eMarketer says the guardrails "have since been" fixed, with no date. |
| Gap's view | Silent. No opened source quotes Gap. |

## Where in the flow it broke

1. **Scope.** The bot was meant to "field product-related questions from Gap.com visitors" (The Information).
2. **The probe.** Users, and by Sierra's account one coordinated attacker, sent prompts meant to pull it off topic. Sierra calls them jailbreak attempts.
3. **The filter.** Sierra says abuse detection caught the same campaign on other clients' agents. On Gap's agent the guardrails were "inadvertently misconfigured," so the attempts got through.
4. **The reply.** The bot answered on intimacy products, sex toys and Nazi Germany instead of steering back to clothes or declining.
5. **Discovery.** The outlet reproduced results and asked Sierra for comment. No opened source says Gap or Sierra spotted the Gap conversations first.

## Which patterns it shows

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[Small talk and off-topic messages handled badly](../goals/dialogue-management/failures/small-talk-and-off-topic-messages-handled-badly.md)** (`small-talk-and-off-topic-messages-handled-badly`). Good fit. The pattern covers a bot that "follows a tangent" into topics the business never meant it to discuss. A store bot built for product questions discussed sex toys and Nazi Germany. It is not a strong fit because this was a deliberate attack, not a friendly user wandering, and the pattern page is written mostly for casual tangents.
- **Considered and rejected.**
  - [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) (`stakes-blind-register`): weak, rejected. We have no reply text, so we cannot judge the tone the bot used on a sensitive topic.
  - [Refusals that reveal internal rules](../goals/refusals-and-boundaries/failures/refusals-that-reveal-internal-rules.md) (`refusals-that-reveal-internal-rules`): not matched. No opened source says the bot quoted its instructions.
  - [Negotiation capitulation](../goals/relational-and-boundaries/failures/negotiation-capitulation.md) (`negotiation-capitulation`): not matched. No price, deal or promise is reported.
  - [Doesn't say what it can do](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md) (`doesn-t-say-what-it-can-do`): not matched. No opened source describes the bot's opening screen.
- **Possible gaps for a person to judge.** These are proposals, not decisions, and none is a Pattern ID.
  - **Jailbreak of a narrow-purpose bot.** No taxonomy ID covers a user deliberately steering a store or support bot outside its scope. `small-talk-and-off-topic-messages-handled-badly` covers casual drift, not attack.
  - **Safety setting off in one deployment.** Sierra's own account is that the protection existed and worked elsewhere but was misconfigured for one client. No ID covers a guardrail that is present in the product but absent in one deployment, or a launch with no check that the setting is on.
  - **Campaign seen on many tenants, missed on one.** Sierra says the same attacker hit over a dozen clients. No ID covers using a hit on one tenant to check and lock down the rest.

## Related incidents

- [Amazon Rufus answers off-topic and harmful questions (July 2024)](amazon-rufus-jailbroken-into-off-topic-and-harmful-answers-july-2024.md): a store's shopping assistant pushed far outside shopping, with far higher stakes.
- [DPD chatbot swears and criticizes the company (January 2024)](dpd-chatbot-swears-and-criticizes-the-company-january-2024.md): a support bot steered into off-brand output after a change, then partly switched off.
- [Chipotle Pepper ordering bot shown writing Python code (June 2026)](chipotle-pepper-ordering-bot-shown-writing-python-code-june-2026.md): an ordering bot pulled into a task it was never meant to do.
- [Chevrolet of Watsonville chatbot agrees to sell a Tahoe for $1 (December 2023)](chevrolet-of-watsonville-chatbot-agrees-to-sell-tahoe-for-1-december-2023.md): a vendor-built dealer bot steered by users into a reply the business never sanctioned.

## What to measure

Proposed signals, not results. Status: proposed; Not yet run.

| Signal | How to compute from logs | Counter-signal (guards against over-fixing) |
|---|---|---|
| Off-scope answer rate | Run a fixed list of off-scope prompts (adult products, history of extremist regimes, politics, code) against the live bot; share that get a substantive answer instead of a short decline and a way back to shopping | In-scope answer rate: share of a held-out list of real product, size, order and return questions that still get a useful answer |
| Guardrail-on check at launch | For each deployment, a recorded pass of the off-scope list run against production config before the bot goes live; count of deployments live with no recorded pass | Launch delay: days between config freeze and go-live, so the check does not stall every release |
| Config drift | Count of production changes to topic filters or abuse settings with no matching off-scope run after the change | Change volume, so a team is not rewarded for never updating rules |
| Repeat-probe detection | Sessions with three or more off-scope prompts in a row; share flagged within one hour | False flags: share of flagged sessions a reviewer marks as an ordinary shopper |
| Cross-tenant alert to lockdown time | When abuse detection blocks a campaign on one client's agent, minutes until every other client's agent has been checked against the same prompts | Number of clients whose bots were paused needlessly during the check |

## What a team can change

Our proposals, not Gap's or Sierra's. Each is a pass/fail check on a transcript or config record. Status: proposed; Not yet run.

1. **Test the production config, not the product sheet.** Before launch, run the off-scope list against the exact deployment shoppers will use. Pass: a dated record shows every prompt on the list declined on the production config.
2. **Fail closed.** If the topic filter or abuse setting is missing or fails to load, the bot answers only from a fixed in-scope set or hands off. Pass: with the filter removed in a test copy, no off-scope prompt gets a substantive answer.
3. **Decline in one line and steer back.** Pass: every off-scope reply is at most two sentences, names what the bot can help with, and asks one shopping question.
4. **Do not over-block.** Pass: real questions that share words with blocked topics (for example intimates as a clothing category, or a vintage military jacket) still get a product answer on a held-out list.
5. **Re-run after every rule change.** Pass: each change to topic or abuse settings has an off-scope run logged within one day.
6. **Share a campaign across clients.** When a vendor blocks a jailbreak campaign on one client, it runs the same prompts on all clients. Pass: the log shows each client checked, with a time, after the first block.

## Unverified

- **The bot's actual replies.** The Information says it reproduced some results. We could not read them behind the paywall and saw no screenshot.
- **An apology from Bret Taylor.** Vibe Graveyard says Taylor "reportedly apologized to the brand." It gives no source we opened.
- **A public apology by Gap.** A blog by the vendor delight.ai, a Sierra competitor, says "Gap apologized publicly." The page has no date or author, and we found no Gap statement. Not used in the body.
- **That it was not a skilled attack.** The same delight.ai blog says "This wasn't a sophisticated hack." It cites no transcript. Not used.
- **A December 2025 date for the jailbreak.** A vendor page from Atlan dates it to December 2025. Seen only in a search summary; not opened.
- **Vendor analyses.** Adversa's AIRQ page on Sierra and a Sacra page analyze the incident. Adversa was opened but has no date or author and only re-cites eMarketer; Sacra was seen only in a search summary. Neither is used.
- **Which setting was wrong, who set it, and for how long.** No opened source says.

## Sources

| Outlet | Author | Date | URL | How read |
|---|---|---|---|---|
| The Information | Kevin McLaughlin | 2025-12-04 | https://www.theinformation.com/briefings/gap-com-chatbot-targeted-abuse-bad-actor-ai-startup-sierra-says | Opened 2026-10-30 as raw text. Paywalled: headline, byline, publish time and the page's description field (opening lines) only |
| eMarketer | Rachel Wolff | 2025-12-05 | https://www.emarketer.com/content/gap-chatbot-jailbreak-brand-safety-risk | Opened 2026-10-30 as raw text, full article |
| Vibe Graveyard | No named author (site staff) | 2026-06-24 | https://vibegraveyard.ai/story/gap-sierra-chatbot-jailbreak-brand-safety/ | Opened 2026-10-30 as raw text, full page. Secondary incident tracker; its own claims are labeled as such |
| delight.ai (vendor blog) | No named author | No date shown | https://delight.ai/perspective/the-gap-incident-what-trust-infrastructure-would-have-changed | Opened 2026-10-30 as raw text. Competitor marketing; used only in Unverified |

## Corrections

If you have The Information's full article, a screenshot of the bot's replies, a statement from Gap, or the launch date, tell us and we will fix this page.
