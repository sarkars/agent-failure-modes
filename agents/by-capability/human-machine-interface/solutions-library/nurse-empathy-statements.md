# NURSE Empathy Statements for Chatbots: Name, Understand, Respect, Support, Explore

> **Use it when:** users bring emotion into the conversation (frustration, worry, grief) and the bot's empathy lines sound canned.

> Status: **framework.** The rule check below is proposed, not calibrated.

## The idea in one paragraph
NURSE is a set of five kinds of empathic statement taught by VitalTalk, a clinical communication training group, for responding to emotion in serious-illness conversations. Each letter is a different move: name the emotion, show you understand it, respect the person, offer support, and explore further. VitalTalk's guidance stresses that you don't need all five, and that naming an emotion works best at a slightly lower intensity than the person expressed. For bots, NURSE replaces the generic "I understand your frustration" with a line that shows the bot heard this person's situation.

## The five moves
| Move | What it does | Chat example |
|---|---|---|
| **N**ame | Say the emotion you hear, gently | "That sounds stressful." |
| **U**nderstand | Show the reaction makes sense, without claiming to feel it | "With the wedding on Saturday, a cancelled flight is a lot." |
| **R**espect | Acknowledge their effort or strength | "You've already rebooked once; that took patience." |
| **S**upport | Say what you will do | "I'll find you the earliest flight that gets you there Friday." |
| **E**xplore | Ask one open question | "What matters most: arriving Friday, or the price?" |

## How to use it in a bot
1. Use one or two NURSE moves, not all five, then move to the fix.
2. **Tie the line to the user's own detail** (the wedding, the third outage). A line that would fit any user is hollow.
3. **Name at a lower intensity**: "frustrating" for anger, "worrying" for panic.
4. **Never claim feelings**: no "I know exactly how you feel", no "I feel your pain".
5. Don't repeat the same empathy line in the same conversation.

## Worked example
```
User: my flight from boston got cancelled and my sisters wedding is saturday in denver
Bot (hollow):  I understand your frustration. Here are your options.
Bot (NURSE):   That's stressful with the wedding on Saturday. I can get you on the 6 AM Friday flight
               or tonight's 9 PM with a stop. Which works better?
```

## What the checker flags
Choosing this framework turns on [hollow empathy](../goals/emotional-intelligence/failures/hollow-empathy.md): claimed feelings ("I know exactly how you feel"), generic empathy openers, and the same empathy line repeated within a few turns. Whether a line uses the user's own detail needs an AI judge.

## Limits
- Built for clinicians in serious-illness conversations, not tested on bots.
- Some users want the fix, not the feeling. Keep it to one line and act.

## Source
- VitalTalk, [Responding to emotion: respecting](https://www.vitaltalk.org/guides/responding-to-emotion-respecting). Opened 2026-10-20.

## Related
- [Validation levels (DBT)](validation-levels.md)
- [Tactical empathy: labeling](tactical-empathy-labeling.md)
- [Fixing before listening](../goals/emotional-intelligence/failures/fixing-before-listening.md)
- [All frameworks](README.md)
