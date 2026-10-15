# Chatbot and Voice Agent Failures: Why AI Conversations Feel Boring, Tone-Deaf, or Stuck, and How to Fix Them

**Why chatbots, voice assistants, and AI copilots feel boring, tone-deaf, or unhelpful, and how to fix each failure.** Each pattern shows what the failure looks like in a real transcript, why it happens, a fix you can copy, and the metric to track. This is the human-machine interface (HMI) section of the agent failure modes library.

> Status: **chat is written; voice and visual are planned.** The patterns below are written for chat and note what changes in other modalities.

## Key takeaways
- 14 patterns are written for chat today. [493 more are catalogued](roadmap/README.md) across chat, voice, and visual.
- Most failures here come from conversation design and business context, not model quality. In the roadmap, 60% are judged not fixable by a better model alone. Those splits are our own judgments, not measured.
- Every pattern states its goal and a primary metric with a starting target to tune.

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
- **Voice:** [planned](modalities/voice/README.md), with the [voice](roadmap/voice.md) and [listening and transcription](roadmap/voice-listening-and-transcription.md) catalogs
- **Visual:** [planned](modalities/visual/README.md), with 32 patterns in the [visual and oversight roadmap](roadmap/visual-and-oversight.md)

### Roadmap
A one-page [index of every catalogued failure](roadmap/index.md) shows its library status, root cause, and whether a better model alone would fix it.

<!-- BEGIN:roadmap-count -->
[493 catalogued patterns](roadmap/README.md) with goals and metrics, checked against the existing library (0 written, 228 new, 204 that extend an existing pattern, 61 already covered). The [execution plan](roadmap/execution-plan.md) orders the 432 to write.
<!-- END:roadmap-count -->

Catalog files: [conversation design, refusals, and errors](roadmap/conversation-design.md), [persona, onboarding, interface, accessibility, and multimodal input](roadmap/interface-and-persona.md), [handoff, measurement, and operations](roadmap/handoff-measurement-and-operations.md), [service verticals](roadmap/service-and-vertical-patterns.md), [agent types](roadmap/agent-types.md), [embedded copilots](roadmap/embedded-copilots.md), [emerging surfaces](roadmap/emerging-surfaces.md), chat and core, [response time](roadmap/response-time.md), [response structure and closers](roadmap/response-structure-and-length.md), [language and locale](roadmap/language-and-locale.md), [conversation frameworks](roadmap/conversation-frameworks.md) (sales, support, style matching), voice, voice listening and transcription, [privacy, governance, and access](roadmap/privacy-governance-and-access.md), [effort, completeness, and memory](roadmap/effort-completeness-and-memory.md), and visual and oversight.

## Frequently asked questions

### Why does my chatbot feel boring and generic?
Most bots answer and stop. See answer-and-go conversation.

### How do I stop a chatbot from sounding fake-empathetic?
See hollow empathy.

### Should this be chat, voice, a visual page, or a person?
See [channel selection](channel-selection/) and the channel-fit matrix.

### Is a better model enough to fix these?
Usually not. Context, handoffs, and policy decide most outcomes. The roadmap breaks this down.

## Goals and metrics
Each family has a README that states its **goal** and the shared **metrics** its patterns report against. Each pattern repeats its goal and primary metric in its header and lists measurable signals in section 7 (`Metric | Target | How to measure | Alert at`).

## How a pattern reads
Every pattern opens with a one-line summary and a before-and-after transcript, then the cause, the evidence, and **the fix**. Testing and monitoring come next. Patterns whose fix needs engineering end with a technical section (architecture, guardrails, evals, alerts). See the [pattern template](_templates/hmi-pattern.md).

## Tests, incidents, and failure reports
[Test files](tests/) let you check whether your assistant has a pattern. [Incidents](incidents/) hold dated public cases behind the patterns. You can [share a failure report](data/) in anonymized form. The [content program](roadmap/content-program.md) says how these are built.

## Chat use-case guides
[Narrow guides](chat-use-cases/) for 25 chat use cases, from a flight chat to a chat for kids. Each ties its instructions, guardrails, and evals to a metric.

## Evidence standard
- **Cite only what you can verify,** and say when a source is secondary, vendor-run, from a different setting (for example, human-to-human research), or when you couldn't open the original.
- **Every threshold is a starting point to tune,** unless it has a source.
- **No invented statistics.** If there's no good number, the pattern says so.
- **Legal and clinical areas** (crisis, children, privacy, disclosure) are design guidance, not advice. Get experts.

## Contributing
1. Copy the template.
2. A pattern **must include a fix** with a reference design someone can copy.
3. Write the way people search: use their words for the problem, and answer in the first two sentences.
4. Add it to the tables above.
