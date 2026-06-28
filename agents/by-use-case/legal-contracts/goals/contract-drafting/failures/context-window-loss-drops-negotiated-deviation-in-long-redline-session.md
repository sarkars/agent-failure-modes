# Context-Window Loss Drops Negotiated Deviation in Long Redline Session

## Issue: During a Long, Multi-Round Contract Redline Session Conducted as a Single Extended Conversation, a Deal-Specific Deviation From Standard Boilerplate Negotiated Early in the Session Falls Out of the Agent's Active Context Window as the Conversation Grows, and a Later-Round Redline Reverts the Clause to Standard Boilerplate Without the Agent or the Negotiating Party Noticing

**Frequency**: Occasional

**Symptoms**
- A liability cap, indemnification carve-out, or termination-notice period explicitly negotiated and agreed upon early in a long redline conversation reappears at its original boilerplate value in a later round, with no explicit instruction to revert it
- The agent's later-round redline summary describes the reverted clause as "unchanged from standard terms," contradicting the session's own earlier turns where the deviation was explicitly agreed
- Re-running the same later-round redline request with the early-session deviation re-stated explicitly in the prompt (rather than relying on it persisting from earlier turns) produces the correct, deviation-preserving redline, isolating context loss -- not drafting capability -- as the failure point
- The reversion concentrates in sessions with many rounds of back-and-forth markup, where the volume of intervening turns is largest relative to the model's effective context window
- Counterparty's legal team flags the reverted clause during their own review, or -- worse -- it is missed by both sides and only surfaces as a dispute after signature

**Root Cause**
Long redline sessions conducted as a single extended conversation accumulate enough turns that earlier-stated agreements can fall outside the portion of the conversation the model effectively attends to, whether due to hard context-window truncation or degraded attention to content placed far from the current turn. A negotiated deviation that exists only as a natural-language statement in an early turn -- rather than as a persistent, structured record the drafting step explicitly re-reads on every later round -- is exactly the kind of information this failure mode drops, even though the deviation was correctly captured and applied earlier in the same session.

**Example**
```
Round 3 of redlining: Counterparty proposes capping liability at 2x fees instead of the standard 1x; both sides agree in the conversation, and the agent updates the clause accordingly
Rounds 4 through 14: Eleven more rounds of unrelated clause negotiation (payment terms, SLAs, renewal language) extend the conversation substantially
Round 15: A minor, unrelated redline request triggers the agent to regenerate the full liability section as part of a broader formatting cleanup
Regenerated liability clause reverts to the standard 1x cap; the round-3 agreement is no longer present in the agent's effective context and is not re-applied
Neither party catches the reversion before signature; the cap discrepancy surfaces only when a claim is made and the executed contract shows 1x instead of the agreed 2x
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Long, multi-turn conversations with LLMs show measurable degradation in maintaining earlier-established facts and constraints as conversation length grows, even within nominal context-window limits | [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) |
| Persistent agent memory mechanisms are identified as a distinct architectural requirement precisely because relying on conversational context alone causes earlier-established facts to be dropped in long-running sessions | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |
| Version control and amendment tracking for legal documents is identified as a distinct technical requirement, since redline sessions accumulate state that plain conversational context does not reliably preserve | [Version Control for Legal Documents](https://arxiv.org/abs/2108.06421) |

**Contributing Factors**
- Negotiated deviations exist only as natural-language statements within the conversation, with no structured "locked terms" record that persists independently of conversation length
- Later-round redline or regeneration steps re-read the full conversation history rather than a structured, explicitly maintained list of already-agreed deviations
- No automated diff between a regenerated clause and the version actually agreed upon in an earlier round flags an unannounced reversion before the redline is sent

---

## Mitigation Strategies

1. **Structured Locked-Terms Ledger**: Maintain a structured, persistent record of every deal-specific deviation from boilerplate as it is agreed, separate from the conversational transcript, and require any clause regeneration step to check against this ledger rather than relying on conversational recall
2. **Pre-Send Diff Against Last Agreed Version**: Before any redline round is sent to the counterparty, automatically diff the regenerated clause against the last version both parties explicitly agreed to, and flag any unannounced reversion for human review
3. **Session Length Threshold Triggers Ledger Re-Injection**: Once a redline session exceeds a defined number of rounds, require the locked-terms ledger to be explicitly re-injected into the agent's context on every subsequent turn rather than relying on it persisting from earlier in the conversation
4. **Deviation Confirmation Restated at Session Milestones**: At natural milestones (final round before signature, after a long gap between rounds), require the agent to explicitly restate every locked deviation from boilerplate for human confirmation before the contract proceeds to execution

### Metrics
- Rate of redline rounds where a regenerated clause reverts to boilerplate despite an earlier-round explicit deviation agreement
- Number of rounds elapsed between a deviation being agreed and a later unannounced reversion, when it occurs
- Percentage of long (above-threshold) redline sessions with an active, explicitly maintained locked-terms ledger

### Alerts
- A redline round is sent to the counterparty with a clause reverted to boilerplate that contradicts the locked-terms ledger → P1
- Contract proceeds to signature with a clause that diffs against the locked-terms ledger and the diff was not resolved → P1
- A redline session exceeds the round-count threshold without a locked-terms ledger being re-injected into context → P2

---

## References

- [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
- [Version Control for Legal Documents](https://arxiv.org/abs/2108.06421)
