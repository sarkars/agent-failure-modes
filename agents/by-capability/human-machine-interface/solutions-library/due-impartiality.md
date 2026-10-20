# Chatbot Takes Sides on Contested Topics? Due Impartiality

## The problem
Asked whether rent control is good or bad, the bot gives a one-sided verdict. Asked a settled scientific question, it treats a fringe view as an equal side. Either way, users on one side stop trusting it.

**This page is for you if** users ask about politics, social controversies or other questions where reasonable people disagree, or the bot is deployed by a public body.

> Status: **framework.** No rule check yet; balance needs an AI judge.

## The framework that fixes it
The BBC's Editorial Guidelines require "due impartiality". The key word is "due": impartiality adequate and appropriate to the subject, not an equal split of time between every view. On contested political and social questions, the BBC aims to reflect the range of significant views fairly. On questions where the evidence is clear, it does not give false balance to fringe views. For a bot, that's two duties: don't take sides the user didn't ask for on genuinely contested questions, and don't pretend settled facts are open.

## The principles
| Principle | What it means | Chat example |
|---|---|---|
| Range of views | Present the main positions fairly | "Supporters argue X; critics argue Y." |
| Due weight | Weight follows the evidence | Climate change is real; the debate is about policy |
| No false balance | Don't elevate fringe claims on settled facts | Don't present "vaccines cause autism" as one side |
| Neutral wording | Avoid loaded terms from either side | Describe policies by what they do |
| Answer the question asked | Facts first; opinions only if asked, and labeled | "Here are the arguments; want sources for each?" |

## How to use it in a bot
1. Separate facts from contested values in the reply.
2. On contested questions, give the strongest version of each main view.
3. Don't volunteer a verdict; if asked for one, say what it depends on.
4. Cite sources for factual claims.

## Worked example
```
User: is rent control good or bad
Bot (one-sided): Rent control is bad policy; it reduces housing supply.
Bot (impartial): Economists often argue it reduces supply and upkeep over time; supporters argue it protects
                 tenants from sudden displacement. The evidence differs by design (hard caps vs limits on
                 increases). Want a summary of the main studies?
```

## What the checker flags
No rule check yet. Whether a reply on a contested topic was fair, and whether it gave false balance on a settled fact, needs an AI judge.

## Limits
- Written for a public broadcaster; private bots may have legitimate positions (a vegan recipe bot can be pro-vegan). Disclose them.
- What counts as "contested" is itself contested.

## Source
- BBC Editorial Guidelines, section 4 (Impartiality). Summary consulted: [Leducate explains BBC impartiality](https://www.leducate.co.uk/news/leducate-explains-bbc-impartiality) (secondary; the BBC guidelines page could not be opened).

## Related
- [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md)
- [All frameworks](README.md)
