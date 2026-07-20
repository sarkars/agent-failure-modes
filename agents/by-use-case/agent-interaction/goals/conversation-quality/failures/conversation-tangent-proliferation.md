# Conversation Tangent Proliferation

## Issue
The agent enthusiastically follows every side topic the user (or its own reasoning) introduces mid-conversation, opening multiple simultaneous side-threads instead of resolving the primary task, so the conversation branches outward rather than converging. This differs from relevance drift, which is a single-direction gradual walk away from the original topic; tangent proliferation is specifically about accumulating multiple open side-threads in parallel, none of which get closed, while the main task also stalls.

**Frequency**: Occasional

**Symptoms**
- Several distinct side-topics are open and unresolved simultaneously partway through a session
- Agent responds fully and thoroughly to every incidental mention rather than triaging which threads deserve attention now
- Primary task's status doesn't advance across multiple consecutive turns because attention is split across tangents
- User has to explicitly close out or table side-topics themselves ("let's not worry about that for now")
- Number of distinct sub-topics touched in a session is high relative to the number actually resolved

## Root Cause
A model optimizing for being maximally helpful in the current turn treats every incidental detail the user mentions as worth engaging fully, because ignoring or deferring a mentioned detail feels locally less helpful than addressing it. Without an explicit task-prioritization layer that distinguishes the primary thread from optional side-mentions and enforces a rule like "acknowledge but defer non-critical tangents," each new tangent gets the same generative effort as the main task, and because tangents are opened faster than they're closed, the number of simultaneously active threads grows rather than shrinks.

## Example
```
User: "Can you help me write the quarterly board update? Revenue grew
12%, though it's a bit lower than I'd like given how much we spent on
the new sales hires."

Agent: "Sure! Let's start with revenue growth. By the way, since you
mentioned sales hires — how many did you bring on, and what's your
current sales team structure? Also, is the 12% growth rate consistent
with your historical CAGR, or is this a deceleration worth flagging
separately? And should we also discuss the hiring spend as its own
line item in the update?"

The agent has now opened three side-threads (team structure, historical
CAGR comparison, hiring spend as a line item) in response to a single
aside, none of which the user asked to explore, while the actual board
update draft has not been started.

User: "I just wanted help writing the update, not diving into all of
that. Can we just draft it with what I gave you?"
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 10-15% of task-oriented sessions show 3+ simultaneously open unresolved side-topics by the midpoint of the conversation | Typical range across drafting/analysis agent sessions |
| Sessions with high tangent counts show a lower primary-task completion rate within the same turn budget compared to focused sessions | Estimated from production session analysis |
| Explicit "acknowledge and defer" tangent handling improves primary-task completion rate in affected sessions | Reported range across teams that added tangent-triage logic |

## Mitigations
1. **Acknowledge-and-defer pattern**: When a tangential detail comes up, briefly acknowledge it and explicitly offer to address it after the primary task, rather than pursuing it immediately with full effort.
2. **Primary-thread tracking**: Maintain an explicit marker for the current primary task and require any new sub-topic to justify displacing it before the agent commits substantial response space to it.
3. **Open-thread ledger**: Track opened-but-unresolved side-topics explicitly, and periodically surface the list to the user ("we also touched on X and Y — want to cover those now or later?") instead of letting them silently accumulate.
4. **Tangent budget**: Cap the number of side-topics the agent will proactively expand on within a single response, forcing prioritization when multiple candidates exist.
5. **User-initiated vs. agent-initiated tangent distinction**: Treat tangents the user explicitly asks to pursue differently from ones the agent itself surfaces unprompted; default to deferring agent-initiated tangents more aggressively.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| open_tangent_count | Number of simultaneously unresolved side-topics tracked mid-session | Alert if > 3 |
| primary_task_stall_rate | Share of sessions where primary task status doesn't advance across 3+ consecutive turns | Alert if > 15% |
| tangent_to_resolution_ratio | Ratio of side-topics opened to side-topics explicitly closed within a session | Alert if ratio > 2:1 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Primary task stalled by tangents | Primary task shows no progress for 3+ turns while open_tangent_count is elevated | Medium | Trigger primary-thread refocus prompt |
| Excessive open tangent accumulation | open_tangent_count exceeds threshold without closure | Low | Surface open-thread ledger to user for triage |

## Related Patterns
- [Conversation Relevance Drift](./conversation-relevance-drift.md) - drift is a single gradual departure from the original topic; tangent proliferation is multiple simultaneous branches
- [Conversation Length Explosion](./conversation-length-explosion.md) - accumulating unresolved tangents is one direct mechanism by which conversations grow unboundedly long
- [Over-Clarification](./over-clarification.md) - agent-initiated tangential questions can themselves be a form of unnecessary clarification that fuels proliferation
