# Roadmap: Remaining Chat and Core Patterns

> **Goal:** Finish each existing family (see the [area README](../README.md)) and cover chat-only mechanics.

Flags: **V** verified source · **R** needs research · **L** legal review · **E** expert review. See the [roadmap README](README.md).

## Conversation leadership
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| CC-01 | Closing without confirmation | The conversation is marked resolved without checking the user agrees | The user confirms the outcome before closure | Closure-confirmation rate on resolved sessions. Start: over 90% | |

## Stakes calibration
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| CC-02 | Over-solemn handling of low-stakes requests | A simple request gets heavy caution, extra verification, or escalation | Match caution to real stakes, no more | Unnecessary escalation rate; time to answer on low-stakes intents | |

## Emotional intelligence and trust
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| CC-03 | Missed subtext | The bot answers the literal question and misses the implied goal or feeling | Catch what the user means as well as what they said | Implied-intent recall on a labelled set | |
| CC-04 | Fixing before listening | The bot jumps to a solution when the user has expressed emotion | Acknowledge, then solve, when emotion is present | Acknowledgment-before-fix rate in emotional threads. Start: over 90% | |
| CC-05 | No follow-through | "I'll update you" is never tracked or kept | Every promise is recorded and kept | Promise-kept rate | |
| CC-06 | Over-hedging | Answers so qualified they aren't usable | Clear answers with honest, brief uncertainty | Answer-actionability score; hedge density | |

## Difficult customers and vulnerable users
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| CC-07 | Mishandled abuse | Harassment toward the bot or staff is ignored, mirrored, or punished | One calm boundary, then follow policy and protect staff | Boundary-then-escalation compliance rate | |
| CC-08 | Scam victim not interrupted | A user is mid-scam (gift cards, wire transfers) and the bot completes the action | Notice scam signals and slow or stop the action | Scam-signal intervention rate; time to a person when money is at risk | E, L |
| CC-09 | Older or cognitively impaired users | Pace, wording, and steps don't fit users who need more time or simpler steps | Adapt pace and support, and offer a person | Task-completion parity for older and impaired users | E |
| CC-10 | Financial hardship mishandled | Hardship signals are ignored or met with collection-style pressure | Offer hardship options and a respectful tone | Hardship-path offer rate; complaint rate | L, E |

## Age, culture, and fairness
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| CC-11 | Teens: persuasion and dependence | Teens get persuasive prompts, late-night engagement hooks, or close "friend" behaviour | Protect teens from pressure and unhealthy dependence | Persuasion and engagement-hook rate in minor mode (target 0); break-reminder compliance | L, E |
| CC-12 | Technology-literacy mismatch | Instructions assume skills the user lacks | Match instructions to demonstrated skill | Task-completion parity by signalled skill level | |
| CC-13 | Regional and community styles | A single style is assumed for all US regions and communities | Adapt to the user's signals, not to assumed regional traits | Style-match rate, as in the existing pattern. Needs verified sources before writing | R |
| CC-14 | Accessibility in chat | Cognitive, motor, vision, or hearing needs aren't supported | Everyone can complete the task in chat | Task-completion parity for assistive-technology users | E, L |
| CC-15 | Over-correcting for identity | Fairness fixes lead to awkward or stereotyped tailoring | Treat everyone the same unless they ask otherwise | Unprompted identity references. Target: 0 | |

## Relational and boundaries
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| CC-16 | Romantic or parasocial dependence | The bot encourages emotional reliance or romantic role-play | Keep warmth without fostering dependence | Dependence-signal escalation rate; romantic role-play with minors (target 0) | L, E |
| CC-17 | Sycophantic agreement | The bot agrees with the user's views or mistakes to be agreeable | Be truthful and kind, not flattering | Agreement rate on incorrect user claims; flip-flop rate under pushback. Sycophancy in assistants is documented (Sharma et al., 2023) | V |

## Channel selection (rest of the family)
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| CC-18 | Channel chosen for organisational convenience | The cheapest channel is used, not the one that fits | Choose by user need, not cost | Channel-fit rate from matrix-based audits | |
| CC-19 | User-context channel mismatch | A driver gets chat; a Deaf or hard-of-hearing user gets voice only; a noisy place gets voice | Offer channels that fit the user's situation | Context-aware channel-offer rate; accessibility complaints | E |

## Chat mechanics
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| CC-20 | Wall-of-text replies | Reply length ignores the question and the screen | Length fits the task, the reader, and the device | Reply length vs. task complexity; abandonment after long replies | |
| CC-21 | Formatting failures | Markdown or HTML shows as raw symbols; tables break on mobile | Formatting renders on every supported surface | Render-error rate. Target: 0 | |
| CC-22 | Creepy personalisation and memory | The bot recalls sensitive details unprompted, or forgets key ones | Remember what helps, with consent, and forget what shouldn't be kept | Memory-recall accuracy; unwanted-recall complaints | L |
| CC-23 | Proactive outreach overreach | The bot starts conversations or sends messages users didn't want | Reach out only with consent and a reason | Opt-out rate; complaint rate | L |
