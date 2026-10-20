# Five Whys for Chatbots: Fix the Cause, Not Only the Symptom

> **Use it when:** users come back with the same problem because the bot fixed the symptom, or an internal help desk bot needs to log causes.

> Status: **framework.** No rule check yet; finding the root cause needs an AI judge.

## The idea in one paragraph
Five Whys is a questioning technique from Toyota. It is credited to Sakichi Toyoda, and Taiichi Ohno, architect of the Toyota Production System, described it as a basis of Toyota's scientific approach. You ask why a problem happened, then why that happened, and so on (about five times) until you reach a cause you can fix. It has well-known limits: people stop at symptoms, find only causes they already know, and pick one cause when there are several. For a bot, a light version helps: after fixing a problem, ask one or two "why" questions to see whether it will come back.

## How it runs
| Why? | Answer | Chat version |
|---|---|---|
| Why can't the user print? | The printer is offline | "The printer shows offline." |
| Why is it offline? | It lost its network address | "It dropped off Wi-Fi." |
| Why did it lose it? | The router reassigns addresses nightly | "Did this start after the router was replaced?" |
| Why does that break printing? | The printer has no reserved address | |
| Fix | Reserve an address for the printer | Fixes it for good, not just today |

## How to use it in a bot
1. Fix the immediate problem first; users want to print now.
2. Then ask one cause question: "Has this happened before? When did it start?"
3. If it's recurring, offer the lasting fix or escalate with the chain of whys.
4. Log the cause, not just "resolved".

## Worked example
```
User: printer offline again
Bot (symptom):   Turn the printer off and on. That should fix it.
Bot (root cause): Restarting will get it back for now. Since it's "again": does it go offline mostly in
                  the mornings? If so, it's likely losing its network address overnight, and IT can make
                  that permanent. Want me to open that ticket?
```

## What the checker flags
No rule check yet. Whether the bot found the root cause needs an AI judge. Library pattern: [symptom fixed, root cause missed](../goals/conversation-frameworks/failures/symptom-fixed-root-cause-missed.md).

## Limits
- Criticized as too simple for complex failures; a former Toyota executive called it too basic for deep root cause analysis. Use it as a habit, not a method of record.

## Source
- [Five whys, Wikipedia](https://en.wikipedia.org/wiki/Five_whys) (secondary; Ohno's writing was not opened).

## Related
- [Structured troubleshooting](structured-troubleshooting.md)
- [All frameworks](README.md)
