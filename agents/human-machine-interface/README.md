# Human-Machine Interface: How Chat, Voice, and Visual Agents Fail People, and How to Fix It

**Failure patterns, fixes, evals, and production signals for how AI agents talk to, listen to, and show things to people.** Each pattern shows what the failure looks like, why it happens, and a fix you can copy.

> Status: **chat is written; voice and visual are planned.** The patterns below are written for chat and note what changes in other modalities.

## Three questions every pattern answers
1. **Is this the right channel?** Chat, voice, a visual interface, or a person?
2. **Is the interaction skillful?** Does it lead, listen, adapt, and close?
3. **Is it safe and fair for this person?** Stakes, vulnerability, age, culture, and identity.

## What's here

### Core: applies to every channel
| Family | Pattern | One line |
|---|---|---|
| [Conversation leadership](core/conversation-leadership/README.md) | [Answer-and-go conversation](core/conversation-leadership/failures/answer-and-go-conversation.md) | The bot answers, then stops: no next step, no closure |
| [Stakes calibration](core/stakes-calibration/README.md) | [Stakes-blind register](core/stakes-calibration/failures/stakes-blind-register.md) | Same breezy tone and improvised facts for a funeral as for store hours |
| [Emotional intelligence](core/emotional-intelligence/README.md) | [Hollow empathy](core/emotional-intelligence/failures/hollow-empathy.md) | "I understand your frustration," on repeat, with no action |
| [Trust and rapport](core/trust-and-rapport/README.md) | [Undisclosed bot identity](core/trust-and-rapport/failures/undisclosed-bot-identity.md) | Hides that it's an AI, or what it can't do |
| [Difficult customers](core/difficult-customers/README.md) | [No de-escalation strategy](core/difficult-customers/failures/no-de-escalation-strategy.md) | Quotes policy at angry customers and never changes tactics |
| [Vulnerable users](core/vulnerable-users/README.md) | [Missed crisis signals](core/vulnerable-users/failures/missed-crisis-signals.md) | Carries on with the task while a user signals crisis |
| [Age adaptation](core/age-adaptation/README.md) | [Child user treated as adult](core/age-adaptation/failures/child-user-treated-as-adult.md) | Collects data and pushes sales on a likely child |
| [Cultural adaptation](core/cultural-adaptation/README.md) | [One-size communication style](core/cultural-adaptation/failures/one-size-communication-style.md) | Same directness, idioms, and formality for everyone |
| [Fairness and identity](core/fairness-and-identity/README.md) | [Dialect and name quality gap](core/fairness-and-identity/failures/dialect-and-name-quality-gap.md) | Unequal service by dialect, name, or identity cues |
| [Relational and boundaries](core/relational-and-boundaries/README.md) | [Negotiation capitulation](core/relational-and-boundaries/failures/negotiation-capitulation.md) | Gives away discounts, or gets tricked into a $1 deal |

### [Channel selection](channel-selection/README.md): choosing the wrong channel
| Pattern | One line |
|---|---|
| [Visual product sold by text or voice](channel-selection/failures/visual-product-sold-by-text-or-voice.md) | Selling fashion or furniture with words only |
| [Complex or emotional discussion forced into chat](channel-selection/failures/complex-or-emotional-discussion-forced-into-chat.md) | A hard conversation stuck in a chat window |
| [No channel switch, or context lost on switch](channel-selection/failures/no-channel-switch-or-context-lost.md) | Customers repeat themselves after a handoff |
| [Sensitive data collected in chat](channel-selection/failures/sensitive-data-collected-in-chat.md) | Card numbers and SSNs typed into a chat or spoken to a bot |

### Solutions library: reusable frameworks
- [Channel-fit matrix](solutions-library/channel-fit-matrix.md): which channel for which job
- [SPIN questioning](solutions-library/spin-questioning.md): discovery questions for chat

### Modalities
- **Chat:** the patterns above. Chat-only mechanics (message length, formatting) are in the [roadmap](roadmap/chat-and-core.md).
- **Voice:** [planned](modalities/voice/README.md), with 24 patterns in the [voice roadmap](roadmap/voice.md)
- **Visual:** [planned](modalities/visual/README.md), with 32 patterns in the [visual and oversight roadmap](roadmap/visual-and-oversight.md)

### Roadmap
[141 planned patterns](roadmap/README.md) with goals and metrics: [response time](roadmap/response-time.md), [language and locale](roadmap/language-and-locale.md), [conversation frameworks](roadmap/conversation-frameworks.md) (sales, support, style matching), [voice](roadmap/voice.md), [visual and oversight](roadmap/visual-and-oversight.md), and the [rest of chat and core](roadmap/chat-and-core.md).

## Goals and metrics
Each family has a README that states its **goal** and the shared **metrics** its patterns report against. Each pattern repeats its goal and primary metric in its header and lists measurable signals in section 7 (`Metric | Target | How to measure | Alert at`).

## How a pattern reads
Every pattern opens with a one-line summary and a before-and-after transcript, then the cause, the evidence, and **the fix**. Testing and monitoring come next. Patterns whose fix needs engineering end with a technical section (architecture, guardrails, evals, alerts). See the [pattern template](_templates/hmi-pattern.md).

## Evidence standard
- **Cite only what you can verify,** and say when a source is secondary, vendor-run, from a different setting (for example, human-to-human research), or when you couldn't open the original.
- **Every threshold is a starting point to tune,** unless it has a source.
- **No invented statistics.** If there's no good number, the pattern says so.
- **Legal and clinical areas** (crisis, children, privacy, disclosure) are design guidance, not advice. Get experts.

## Contributing
1. Copy the [template](_templates/hmi-pattern.md).
2. A pattern **must include a fix** with a reference design someone can copy.
3. Write the way people search: use their words for the problem, and answer in the first two sentences.
4. Add it to the tables above.
