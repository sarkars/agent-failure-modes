---
title: "Taco Bell Rethinks Voice AI at the Drive-Thru After Viral Order Glitches"
date: 2025-08-30
source: "https://restauranttechnologynews.com/2025/08/how-taco-bells-ai-drive-thru-became-a-viral-sensation-for-the-wrong-reasons/"
summary: "In late August 2025, trade and tech outlets reported viral clips of Taco Bell's voice AI drive-thru ordering, including a prank order for 18,000 cups of water. A Taco Bell executive said the company was rethinking where to use it. Accuracy figures were not published in the sources we opened."
categories:
  - Customer Service
patterns:
  - order-mix-ups-at-the-speaker
---

**This page is a dated teardown of one public voice-agent incident, for teams that put a voice or chat agent in front of an ordering step.** Every fact below comes from a source we opened (listed at the end). We could not open the Wall Street Journal article that most coverage relies on, or Taco Bell's own statements, so every company quote here is secondhand.

## What happened (as reported)

- **March 19, 2025.** Fortune reports that Yum! Brands, parent of Taco Bell, KFC and Pizza Hut, announced a partnership with Nvidia to bring AI into ordering, including taking drive-thru and call orders, and plans to reach 500 locations by the end of the year. Fortune's article does not describe a Taco Bell pilot.
- **Rollout.** Cyber Daily (September 2, 2025) and Restaurant Technology News (August 30) both say the voice AI ran at "more than 500" locations. The sources disagree on the start: the AI Incident Database page says since 2023, and Gigazine (August 31) says starting in 2024. We do not pick one.
- **Late August 2025.** Restaurant Technology News says the system was "dutifully processing prank orders like 18,000 cups of water" and that it kept pestering customers to add more drinks. Cyber Daily says one customer reportedly ordered 18,000 water cups to force staff to override the AI. Gigazine reports the order as a request to disrupt the system. The AI Incident Database page says the clip showed the system crashing; no other source we opened says that, so we treat the crash as unconfirmed.
- **Customer complaints.** Gigazine says social media posts described glitches and slow responses. Cyber Daily says results were inconsistent and that when the AI hits a problem, a person takes over the order.
- **What the executive said.** Cyber Daily, Gigazine and the AI Incident Database page attribute comments to Dane Mathews, Taco Bell's chief digital and technology officer, speaking to the Wall Street Journal. Cyber Daily quotes him: "Sometimes it lets me down, but sometimes it really surprises me." Cyber Daily and Gigazine report he said the company was learning a lot, was still deciding where to use voice AI, and that very busy locations with long lines may be better served by a person. The sources differ on scope: the AI Incident Database page says Taco Bell would be more selective, including not using it at drive-thrus, while Cyber Daily and Gigazine do not report that. Restaurant Technology News paraphrases him as calling results uneven. We do not claim the company stopped using the system.
- **Volume.** Gigazine says the system had gathered more than 2 million customer orders of data; the AI Incident Database page says about two million orders were processed successfully. The sources do not say what "successfully" means or what share of orders needed a person.
- **Guidance to franchisees.** Restaurant Technology News says franchise teams were advised to treat voice AI as "a sometimes tool," watch it closely, and pair it with staff during busy hours. It does not name who gave the advice.

## What the sources do not say

- Any measured order accuracy, error rate, or share of orders handed to staff.
- Whether the 18,000-water order was charged, fulfilled, or cut off. Cyber Daily frames it as an attempt to force a human override, which suggests it was stopped; no source confirms what happened.
- What the "drinks" prompting looked like in a real transcript. Restaurant Technology News describes it in one phrase; we have not seen the clips.
- The cause of any glitch, which speech or language model was used, and whether the company changed the system afterward.
- Whether the system had a readback or on-screen order. None of the sources describe either.

## Pattern match

- [Order mix-ups at the speaker](../goals/drive-thru-agents/failures/order-mix-ups-at-the-speaker.md) (Pattern ID `order-mix-ups-at-the-speaker`). The pattern covers a runaway or wrong order that a customer cannot check before paying. The 18,000-water order is the extreme case of its "total jumps" scenario. Our reading: sources show that a nonsensical quantity was accepted into the system and that people stepped in, which fits the missing "runaway cap". They do not show a wrong order reaching a customer, so the fit is partial.
- What the pattern's fix would have changed (our reading, untested): a pause-and-confirm on a quantity far above normal would turn the prank into one confirmation question, and a fast handoff would put staff in earlier than a customer-forced override.
- Considered and not matched. [Over-confirmation](../goals/dialogue-management/failures/over-confirmation.md) and [silent failure and timeout](../goals/response-time/failures/silent-failure-and-timeout.md): the sources report the opposite of too many confirmations and give no sign of a silent error. "Slow responses" is one phrase from Gigazine, not enough for the second. We do not force either.

## Where in the flow it broke

Based on the reports, the weak points were at order entry and at the upsell step, not at payment:

1. **No visible limit on quantity.** A request for 18,000 of an item was reportedly handled as an ordinary order (Restaurant Technology News).
2. **Repeated drink prompts.** The system reportedly kept asking for more drinks (Restaurant Technology News). Whether this was a script rule or a fault is not stated.
3. **Override depended on staff noticing or the customer forcing it.** Cyber Daily says a person takes over when the AI has problems; it does not say what triggers that.

The reported cost is reputational, plus a public rethink of where to deploy it. No source reports a loss or an injury.

## What to measure

Proposed metrics; none come from Taco Bell. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Orders with an item quantity far above the usual | Orders where any item count exceeds a set cap, divided by all orders |
| Orders handed to staff | Handoffs divided by all orders, split by busy and quiet hours |
| Orders changed by crew after the agent took them | Crew edits to agent entries, divided by orders |
| Repeat prompts for the same upsell | Times the agent asks for add-ons after the customer declined |

## What a team can change

Proposed rules, each a pass/fail check on a test script. Status: Not yet run.

1. **Quantity cap with confirm.** Any item count over a set limit triggers one question ("That's 18,000 waters. Is that right?") and does not enter the order until answered. Check: scripted extreme orders never reach the kitchen screen unconfirmed.
2. **One upsell, then stop.** After a "no" to add-ons, the agent does not ask again. Check: zero repeat prompts in a scripted decline set.
3. **Handoff trigger.** Two failed fixes or an absurd quantity routes to staff with the order on screen. Check: handoff fires in the scripted cases.
4. **Don't over-correct.** Ordinary large family orders must pass without a pause. Test rule 1 against realistic big orders too.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://fortune.com/2025/03/19/nvidia-yum-brands-taco-bell-fast-food-ai-drive-thru-partnership | Fortune (Sasha Rogelberg) | 2025-03-19 | Yes, 2026-10-20 |
| https://restauranttechnologynews.com/2025/08/how-taco-bells-ai-drive-thru-became-a-viral-sensation-for-the-wrong-reasons/ | Restaurant Technology News (Dustin Stone) | 2025-08-30 | Yes, 2026-10-20 |
| https://gigazine.net/gsc_news/en/20250831-taco-bell-rethinks-voice-ai-drive-through | Gigazine | 2025-08-31 | Yes, 2026-10-20 |
| https://www.cyberdaily.au/digital-transformation/12583-taco-bell-weighs-up-ai-rollback-as-drive-through-ordering-delivers-mixed-results | Cyber Daily (Daniel Croft) | 2025-09-02 | Yes, 2026-10-20 |
| https://incidentdatabase.ai/reports/6654 | AI Incident Database, carrying a report that cites the BBC | 2025 (year only) | Yes, 2026-10-20 |

Not opened: the Wall Street Journal article (the original source of the Mathews comments) and the BBC article (our fetch tool could not open it). No Taco Bell or Yum! Brands primary statement was opened, so all company comments are relayed by the outlets above.

## Corrections

If you have the original WSJ text, a Taco Bell statement, or a better date, tell us and we will fix this page.
