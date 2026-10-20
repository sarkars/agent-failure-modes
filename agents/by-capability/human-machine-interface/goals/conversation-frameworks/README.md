# Conversation Frameworks: Goal, Metrics, and Patterns

> **Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.

## Why this family exists
Human sales and support teams learn structures: find the need before pitching, handle an objection in steps, ask for a next step, follow up only as agreed. A chatbot that improvises each exchange skips them. It lists features, argues with "too expensive", or lets an interested buyer leave with nothing to do. These are design and business-rule problems, so a better model alone does not fix them.

## How the frameworks are used here
The frameworks (SPIN, Challenger, BANT and MEDDICC, objection-handling steps) come from human-to-human practice. None has been tested on chatbots in the sources found. Each page treats a framework as a hypothesis to test, not a proven fix. See the [framework register](../../roadmap/README.md#framework-and-source-register) for what was verified.

## How we measure it
Each pattern page defines its own primary metric. Targets are starting points to tune on your own data and are proposed, not measured.
| Metric | Defined in |
|---|---|
| Share of recommendations that cite the user's stated need (judge). Start: over 90% | [feature dump instead of insight](failures/feature-dump-instead-of-insight.md) |
| Share of objections followed by continued conversation or a next step | [mishandled objections](failures/mishandled-objections.md) |
| Next-step proposal rate in qualified chats. Start: over 90% | [no ask](failures/no-ask.md) |
| Consented-follow-up completion rate; opt-out rate | [no follow-up](failures/no-follow-up.md) |
| Stakeholders captured per qualified deal | [buying-committee blindness (B2B)](failures/buying-committee-blindness-b2b.md) |
| Recommendation-fit rate (judge); return and cancel rate | [wrong-fit recommendation](failures/wrong-fit-recommendation.md) |
| Upsell-during-negative-sentiment rate. Target: 0 | [upsell at the wrong moment](failures/upsell-at-the-wrong-moment.md) |
| Repeated-step rate; steps to resolution | [unstructured troubleshooting](failures/unstructured-troubleshooting.md) |
| Repeat-contact rate for the same root cause | [symptom fixed, root cause missed](failures/symptom-fixed-root-cause-missed.md) |
| "Where is my X?" contact rate | [no proactive updates](failures/no-proactive-updates.md) |
| Recovery-offered rate on company-fault issues | [service recovery failure](failures/service-recovery-failure.md) |
| Structure-compliance rate on bad-news replies (judge) | [bad news without structure](failures/bad-news-without-structure.md) |
| Comprehension-check rate (start over 80%) | [instructions without comprehension checks](failures/instructions-without-comprehension-checks.md) |
| Reflection-to-question ratio (start at or above 1.0) | [behaviour-change talk without listening skills](failures/behaviour-change-talk-without-listening-skills.md) |
| Verbatim-repeat rate (start under 2%) | [over-mirroring](failures/over-mirroring.md) |
| Hostility-echo rate. Target: 0 | [mirroring hostility](failures/mirroring-hostility.md) |
| Dialect-imitation incidents. Target: 0 | [imitating dialect or errors](failures/imitating-dialect-or-errors.md) |
| Paraphrase present on complex requests (start over 80%) | [no reflective listening](failures/no-reflective-listening.md) |
| Label confirmation rate (start over 70%) | [misused tactical empathy](failures/misused-tactical-empathy.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Feature dump instead of insight](failures/feature-dump-instead-of-insight.md) | The bot lists features and leaves the user to work out which ones fit their problem. |
| [Mishandled objections](failures/mishandled-objections.md) | The bot caves, argues, or skips the objection instead of acknowledging, asking, answering, and checking. |
| [No ask](failures/no-ask.md) | An interested user gets answers but no proposed next step. |
| [No follow-up](failures/no-follow-up.md) | The chat ends and the lead goes cold; follow up only as the user agreed. Carries a "Read this first" note. |
| [Buying-committee blindness (B2B)](failures/buying-committee-blindness-b2b.md) | The bot records one contact and never asks who else decides. |
| [Wrong-fit recommendation](failures/wrong-fit-recommendation.md) | The bot recommends a product that breaks a limit the user stated. |
| [Upsell at the wrong moment](failures/upsell-at-the-wrong-moment.md) | A complaining or grieving user gets a sales offer. Carries a "Read this first" note. |
| [Unstructured troubleshooting](failures/unstructured-troubleshooting.md) | Many fixes at once, so no one knows which worked. Carries a "Read this first" note. |
| [Symptom fixed, root cause missed](failures/symptom-fixed-root-cause-missed.md) | The bot solves what was said, not what keeps causing it. |
| [No proactive updates](failures/no-proactive-updates.md) | The user has to chase for status. |
| [Service recovery failure](failures/service-recovery-failure.md) | A company-caused problem gets no ownership or make-good. |
| [Bad news without structure](failures/bad-news-without-structure.md) | A denial arrives in one line with no reason or next step. Carries a "Read this first" note. |
| [Instructions without comprehension checks](failures/instructions-without-comprehension-checks.md) | Steps are listed and nobody checks they were understood. Carries a "Read this first" note. |
| [Behaviour-change talk without listening skills](failures/behaviour-change-talk-without-listening-skills.md) | A user's struggle gets a lecture instead of a reflection and a question. Carries a "Read this first" note. |
| [Over-mirroring](failures/over-mirroring.md) | The bot parrots the user's own words, which sounds like mockery. Carries a "Read this first" note. |
| [Mirroring hostility](failures/mirroring-hostility.md) | The bot copies an angry or sarcastic tone back. Carries a "Read this first" note. |
| [Imitating dialect or errors](failures/imitating-dialect-or-errors.md) | The bot copies slang or learner-English mistakes back. Carries a "Read this first" note. |
| [No reflective listening](failures/no-reflective-listening.md) | A many-part request is acted on without restating it. Carries a "Read this first" note. |
| [Misused tactical empathy](failures/misused-tactical-empathy.md) | A feeling is named as fact or the user's words are echoed as a "reflection". Carries a "Read this first" note.

## Chat examples in existing pages
These catalog rows have no page of their own. Each has a short chat example inside the closest existing pattern.
| Row | Example in |
|---|---|
| FW-S02 No qualification | [qualification flow violations](../../../speech-and-audio/goals/conversation-flow/failures/qualification-flow-violations.md) |
| FW-S06 Manipulative closing | [vague consent exploitation](../../../speech-and-audio/goals/conversation-flow/failures/vague-consent-exploitation.md) |
| FW-S07 Discount-first selling | [negotiation capitulation](../relational-and-boundaries/failures/negotiation-capitulation.md) |
| FW-S12 Lead handoff without qualification | [sdr to ae handoff drops unstructured disqualifying signal](../../../../by-use-case/sales-crm/goals/pipeline-forecasting/failures/sdr-to-ae-handoff-drops-unstructured-disqualifying-signal.md) |
| FW-C01 No triage or severity check | [high effort ticket misrouting](../../../../by-use-case/support-services/goals/ticket-routing/failures/high-effort-ticket-misrouting.md) |
| FW-C04 High customer effort | [conversation length explosion](../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/conversation-length-explosion.md) |
| FW-C06 No learning loop | [feedback not incorporated](../../../../cross-cutting/operations/goals/human-oversight-reliability/failures/feedback-not-incorporated.md) |
| FW-M01 No style matching | [response adaptation failure](../../../speech-and-audio/goals/conversation-flow/failures/response-adaptation-failure.md) |
| FW-M06 Style whiplash | [conversation mood whiplash](../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/conversation-mood-whiplash.md) |
| FW-O01 Cooperation violations | [conversation depth mismatch](../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/conversation-depth-mismatch.md) |

## Planned (not yet written)
The rest of the catalog (supporting, matching style, delivering hard news) is listed in the [roadmap](../../roadmap/conversation-frameworks.md).

## Related
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md) · [Sales agents](../sales-agents/README.md)
