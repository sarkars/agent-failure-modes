# Channel-Fit Matrix (which channel for which job)

> **Use it when:** you're deciding where an interaction should happen (chat, voice, a visual interface, or a person), or deciding when a bot should offer to switch.

## Status of this guide
This is a **design heuristic**, not a validated model. It draws on media richness theory (Daft & Lengel, 1986), which holds that ambiguous tasks suit richer channels. Later studies found its empirical support weak, especially for computer-mediated communication (Dennis & Valacich, 1999), so treat the matrix as a starting point to test on your own users.

## The matrix
| Situation | Best channel | Why | Avoid |
|---|---|---|---|
| Simple lookup or status check | Chat or voice | Low ambiguity, quick | Making users navigate menus |
| Replenishing something the user already knows | Voice or chat | The user knows the item, so little needs showing | Long browsing flows |
| **Visual-first product** (apparel, furniture, art, paint, jewelry) | Visual interface (cards, photos, swatches, try-on), with chat to narrow choices | The decision depends on how it looks | Text-only or voice-only selling |
| **Dense or numeric information** (prices, terms, schedules, side-by-side comparisons) | Written or visual (table, email, PDF, screen) | Speech is transient and users can't scan or re-read it | Reading long lists aloud |
| **Ambiguous, multi-issue, or negotiable** (claims disputes, financial planning, technical troubleshooting) | A call, video, or a person, prepared by chat | Needs fast back-and-forth to settle meaning | A long text thread |
| **High emotion or high stakes** (bereavement, fraud, denied claim, distress) | A human by voice, or chat with a human present | People need to be heard by a person | Bot-only handling |
| **Sensitive data entry** (card number, SSN, passwords) | Secure form, hosted payment field, or masked keypad entry | Free-text chat is not a protected channel | Typing or speaking it into a chat or voice bot |
| Urgent or safety-related | Phone and a human | Fastest route to help | Text queues |
| Hands or eyes busy (driving, cooking) | Voice | Frees hands and eyes | Chat |
| Accessibility needs | **The user's choice** (for example, text for Deaf or hard-of-hearing users) | Needs differ and the user knows theirs | Forcing one channel |

## How to choose (in order)
1. **What must the user see, hear, or do?** If they must see it, pick a channel that shows it.
2. **How ambiguous is the topic?** The more open to interpretation, the richer the channel should be.
3. **How high are the stakes and the emotion?** Raise toward a human as they rise.
4. **Does it involve sensitive data?** If yes, never use free-text chat or speech for it.
5. **What does this user prefer, and what do they need?** Their stated preference and accessibility needs override everything above.
6. **Offer, don't force.** Say why ("this will be easier to compare on screen"), give one option, and carry the context across.

## Switching rules
- Offer a switch with a **reason and a specific next step** ("I can text you three options with photos. OK to send them to the number you're using now?").
- Pass a **summary of the conversation** so the user never repeats themselves.
- Ask permission before moving to a new channel such as text messages.

## Patterns that apply this guide
- [Visual products sold by chat or voice](../channel-selection/failures/visual-product-sold-by-text-or-voice.md)
- [Complex or emotional discussion forced into chat](../channel-selection/failures/complex-or-emotional-discussion-forced-into-chat.md)
- [No channel switch, or context lost on switch](../channel-selection/failures/no-channel-switch-or-context-lost.md)
- [Sensitive data collected in chat](../channel-selection/failures/sensitive-data-collected-in-chat.md)

## Sources
- Daft, R. L., & Lengel, R. H. (1986). Organizational information requirements, media richness and structural design. *Management Science*. Summary via [Wikipedia](https://en.wikipedia.org/wiki/Media_richness_theory); I could not read the full text.
- Dennis, A. R., & Valacich, J. S. (1999). Rethinking media richness. *HICSS*. [PDF](https://collablab.northwestern.edu/CollabolabDistro/nucmc/DennisAndValacich-RethinkingMediaRichness-HICSS-1999.pdf)
