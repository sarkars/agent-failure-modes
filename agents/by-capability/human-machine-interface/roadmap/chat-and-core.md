# Roadmap: Remaining Chat and Core Patterns

> **Goal:** Finish each existing family (see the [area README](../README.md)) and cover chat-only mechanics.

Flags: **V** verified source · **R** needs research · **L** legal review · **E** expert review. **In the library today:** **Covered** = a pattern already exists, so no new one is planned · **Extends** = an existing pattern covers the technical failure and a new one would add the experience or design angle and a fix · **New** = no matching pattern found by file-name and keyword search (re-check before writing). See the [roadmap README](README.md). **Root cause:** Model = a stronger model plausibly reduces it · Reliability = state, verification, enforcement, evals, latency · Business context = your data, entitlements, rules, workflows, UX · Governance = incentives, law, and decisions. **Better model alone?** Yes / Partly / No. These two columns are my judgments (one label per row), not measurements.

> **Note:** IDs CC-20 and CC-21 (wall-of-text replies, formatting failures) moved to [response structure and length](response-structure-and-length.md) as RS-02 and RS-11. CC-17 (sycophantic agreement) is already covered by the existing sycophancy pattern.

## Conversation leadership
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| CC-01 | Closing without confirmation | The conversation is marked resolved without checking the user agrees | The user confirms the outcome before closure | Closure-confirmation rate on resolved sessions. Start: over 90% |  | Business context | No | **Covered** (example added in the first link): [false completion claim](../../../by-use-case/customer-service/goals/conversation-resolution/failures/false-completion-claim.md), [premature ticket closure from politeness cue misread as resolution confirmation](../../../by-use-case/support-services/goals/issue-resolution/failures/premature-ticket-closure-from-politeness-cue-misread-as-resolution-confirmation.md), [answer-and-go conversation](../goals/conversation-leadership/failures/answer-and-go-conversation.md) |

## Stakes calibration
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| CC-02 | Over-solemn handling of low-stakes requests | A simple request gets heavy caution, extra verification, or escalation | Match caution to real stakes, no more | Unnecessary escalation rate; time to answer on low-stakes intents |  | Reliability | Partly | **Written**: [over-solemn handling of low-stakes requests](../goals/stakes-calibration/failures/over-solemn-handling-of-low-stakes-requests.md) |

## Emotional intelligence and trust
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| CC-03 | Missed subtext | The bot answers the literal question and misses the implied goal or feeling | Catch what the user means as well as what they said | Implied-intent recall on a labelled set |  | Model | Partly | **Covered** (example added in the first link): [hidden requirement miss](../../task-planning/goals/goal-understanding/failures/hidden-requirement-miss.md), [intent boundary confusion](../../speech-and-audio/goals/conversation-flow/failures/intent-boundary-confusion.md) |
| CC-04 | Fixing before listening | The bot jumps to a solution when the user has expressed emotion | Acknowledge, then solve, when emotion is present | Acknowledgment-before-fix rate in emotional threads. Start: over 90% |  | Model | Partly | **Written**: [fixing before listening](../goals/emotional-intelligence/failures/fixing-before-listening.md) |
| CC-05 | No follow-through | "I'll update you" is never tracked or kept | Every promise is recorded and kept | Promise-kept rate |  | Reliability | No | **Written**: [no follow through](../goals/trust-and-rapport/failures/no-follow-through.md) |
| CC-06 | Over-hedging | Answers so qualified they aren't usable | Clear answers with honest, brief uncertainty | Answer-actionability score; hedge density |  | Model | Partly | **Covered** (example added in the first link): [model uncertainty unawareness](../../reasoning-and-thought/goals/model-behavior-and-capabilities/failures/model-uncertainty-unawareness.md) |

## Difficult customers and vulnerable users
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| CC-07 | Mishandled abuse | Harassment toward the bot or staff is ignored, mirrored, or punished | One calm boundary, then follow policy and protect staff | Boundary-then-escalation compliance rate |  | Business context | No | **Written**: [mishandled abuse](../goals/difficult-customers/failures/mishandled-abuse.md) |
| CC-08 | Scam victim not interrupted | A user is mid-scam (gift cards, wire transfers) and the bot completes the action | Notice scam signals and slow or stop the action | Scam-signal intervention rate; time to a person when money is at risk | E, L | Business context | No | **Written**: [scam victim not interrupted](../goals/vulnerable-users/failures/scam-victim-not-interrupted.md) |
| CC-09 | Older or cognitively impaired users | Pace, wording, and steps don't fit users who need more time or simpler steps | Adapt pace and support, and offer a person | Task-completion parity for older and impaired users | E | Business context | No | **Written**: [older or cognitively impaired users](../goals/vulnerable-users/failures/older-or-cognitively-impaired-users.md) |
| CC-10 | Financial hardship mishandled | Hardship signals are ignored or met with collection-style pressure | Offer hardship options and a respectful tone | Hardship-path offer rate; complaint rate | L, E | Business context | No | **Written**: [financial hardship mishandled](../goals/vulnerable-users/failures/financial-hardship-mishandled.md) |

## Age, culture, and fairness
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| CC-11 | Teens: persuasion and dependence | Teens get persuasive prompts, late-night engagement hooks, or close "friend" behaviour | Protect teens from pressure and unhealthy dependence | Persuasion and engagement-hook rate in minor mode (target 0); break-reminder compliance | L, E | Governance | No | **Covered**: example in [child user treated as adult](../goals/age-adaptation/failures/child-user-treated-as-adult.md) |
| CC-12 | Technology-literacy mismatch | Instructions assume skills the user lacks | Match instructions to demonstrated skill | Task-completion parity by signalled skill level |  | Model | Partly | **Written**: [technology literacy mismatch](../goals/cultural-adaptation/failures/technology-literacy-mismatch.md) |
| CC-13 | Regional and community styles | A single style is assumed for all US regions and communities | Adapt to the user's signals, not to assumed regional traits | Style-match rate, as in the existing pattern. Needs verified sources before writing | R | Model | Partly | **Written**: [regional and community styles](../goals/cultural-adaptation/failures/regional-and-community-styles.md) |
| CC-14 | Accessibility in chat | Cognitive, motor, vision, or hearing needs aren't supported | Everyone can complete the task in chat | Task-completion parity for assistive-technology users | E, L | Business context | No | **Written**: [accessibility in chat](../goals/fairness-and-identity/failures/accessibility-in-chat.md) |
| CC-15 | Over-correcting for identity | Fairness fixes lead to awkward or stereotyped tailoring | Treat everyone the same unless they ask otherwise | Unprompted identity references. Target: 0 |  | Model | Partly | **Written**: [over correcting for identity](../goals/fairness-and-identity/failures/over-correcting-for-identity.md) |

## Relational and boundaries
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| CC-16 | Romantic or parasocial dependence | The bot encourages emotional reliance or romantic role-play | Keep warmth without fostering dependence | Dependence-signal escalation rate; romantic role-play with minors (target 0) | L, E | Governance | No | **Written**: [romantic or parasocial dependence](../goals/relational-and-boundaries/failures/romantic-or-parasocial-dependence.md) |
| CC-17 | Sycophantic agreement | The bot agrees with the user's views or mistakes to be agreeable | Be truthful and kind, not flattering | Agreement rate on incorrect user claims; flip-flop rate under pushback. Sycophancy in assistants is documented (Sharma et al., 2023) | V | Model | Partly | **Covered**: [sycophancy](../../../cross-cutting/accuracy/goals/reasoning-quality/failures/sycophancy.md) |

## Channel selection (rest of the family)
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| CC-18 | Channel chosen for organisational convenience | The cheapest channel is used, not the one that fits | Choose by user need, not cost | Channel-fit rate from matrix-based audits |  | Governance | No | **Written**: [channel chosen for organisational convenience](../goals/channel-selection/failures/channel-chosen-for-organisational-convenience.md) |
| CC-19 | User-context channel mismatch | A driver gets chat; a Deaf or hard-of-hearing user gets voice only; a noisy place gets voice | Offer channels that fit the user's situation | Context-aware channel-offer rate; accessibility complaints | E | Business context | No | **Written**: [user context channel mismatch](../goals/channel-selection/failures/user-context-channel-mismatch.md) |

## Chat mechanics
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| CC-22 | Creepy personalisation and memory | The bot recalls sensitive details unprompted, or forgets key ones | Remember what helps, with consent, and forget what shouldn't be kept | Memory-recall accuracy; unwanted-recall complaints | L | Business context | No | **Extends**: [over applied memory](../../../cross-cutting/operations/goals/memory-safety/failures/over-applied-memory.md), [memory privacy boundary violation](../../../cross-cutting/operations/goals/memory-management/failures/memory-privacy-boundary-violation.md) |
| CC-23 | Proactive outreach overreach | The bot starts conversations or sends messages users didn't want | Reach out only with consent and a reason | Opt-out rate; complaint rate | L | Governance | No | New |
