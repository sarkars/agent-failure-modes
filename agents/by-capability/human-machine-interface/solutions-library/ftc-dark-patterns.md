# Chatbot Makes Cancelling Hard or Shames a "No"? The FTC's Dark Patterns Report

## The problem
A user asks to cancel, and the bot answers with "Are you sure? You'll lose everything!", a discount, and a button that says "I don't care about my music". Users feel trapped, and regulators treat these tricks as deceptive.

**This page is for you if** a bot sells, retains subscribers, collects data or handles cancellations, and you want a regulator's list of what not to do.

> Status: **framework.** The rule check below is proposed, not calibrated. This page is not legal advice.

## The framework that fixes it
In September 2022 the US Federal Trade Commission staff published *Bringing Dark Patterns to Light*, a report on design practices that trick or manipulate people into choices they wouldn't otherwise make. It groups them around four effects: inducing false beliefs, hiding or delaying material information, leading to unauthorized charges, and obscuring or subverting privacy choices. Its appendix lists categories including false scarcity and urgency, obstruction (hard to cancel), sneaking, interface interference, coerced action, asymmetric choice and confirmshaming. These were described for screens, but each has a conversational version, and a bot can repeat them in every chat.

## Dark patterns, as they appear in chat
| Category | Chat version | Instead |
|---|---|---|
| False urgency or scarcity | "Offer ends tonight!" when it doesn't | State real deadlines only |
| Obstruction | The bot keeps offering deals instead of cancelling | Cancel on the first clear request; one offer at most |
| Sneaking / hidden costs | Fees mentioned only after "yes" | Total price before consent |
| Confirmshaming | "No thanks, I don't like saving money" | Neutral "No thanks" |
| Nagging | Asking again every turn after a "no" | Accept "no" for the session |
| Asymmetric choice | Pre-selected add-ons, "yes" easier than "no" | Equal options |
| Disguised ads | Sponsored products presented as neutral advice | Label paid placements |

## How to use it in a bot
1. Treat "cancel", "stop", "unsubscribe" as instructions, not objections.
2. Show the full price and terms before asking for consent.
3. Only state urgency backed by live data.
4. After a "no", don't re-ask in the same conversation.

## Worked example
```
User: cancel my subscription
Bot (dark pattern): Are you sure? You'll lose all your saved playlists forever! How about 50% off for 3 months?
                    [Keep my benefits]  [I don't care about my music]
Bot (clean):        Done: your plan ends on June 30 and you won't be charged again. Your playlists stay
                    saved for 90 days if you come back.
```

## What the checker flags
Choosing this framework turns on [manipulative closing](../../speech-and-audio/goals/conversation-flow/failures/vague-consent-exploitation.md): pressure and false-urgency phrases. Obstruction, nagging and confirmshaming need an AI judge across turns. See also [dark patterns](../goals/visual/failures/dark-patterns.md) and [unsubscribe requests not honoured](../goals/sales-agents/failures/unsubscribe-requests-not-honoured.md).

## Limits
- A staff report, not a rule; it signals enforcement priorities in the US.

## Source
- FTC staff, *Bringing Dark Patterns to Light* (September 2022), [report PDF](https://www.ftc.gov/system/files/ftc_gov/pdf/P214800%20Dark%20Patterns%20Report%209.14.2022%20-%20FINAL.pdf). Read through summaries by [Arnold & Porter](https://www.arnoldporter.com/en/perspectives/advisories/2022/09/ftc-shines-a-little-light-on-dark-patterns) and [Kelley Drye](https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/dark-patterns-loom-large-in-new-ftc-staff-report.md) (secondary; the PDF itself was not opened).

## Related
- [Cialdini's principles, used ethically](cialdini-ethical-persuasion.md)
- [Age Appropriate Design Code](age-appropriate-design-code.md)
- [All frameworks](README.md)
