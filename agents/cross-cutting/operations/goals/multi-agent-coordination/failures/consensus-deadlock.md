# Consensus Deadlock

## Issue: Multi-Agent Voting or Agreement Fails to Resolve

**Frequency**: Occasional

**Symptoms**
- System unable to reach decision
- Agents repeatedly propose conflicting solutions
- Timeout on consensus operations
- Oscillation between options without convergence

**Root Cause**
Multi-agent systems often use voting, debate, or consensus mechanisms to make decisions. These can fail to converge due to balanced opposing views, strategic behavior, or incompatible evaluation criteria.

**Example**
```
Code Review Multi-Agent System:
Agent A (Security): "Reject - potential SQL injection"
Agent B (Performance): "Reject - inefficient query pattern"
Agent C (Readability): "Approve - clean, well-documented"
Agent D (Testing): "Approve - good test coverage"

Consensus rule: 3/4 majority required

Round 1: 2-2 split, no consensus
Round 2: Agents re-evaluate, same split
Round 3-10: Deadlock continues

Result: Code review never completes
```

**Deadlock Patterns**
- **Balanced opposition**: Equal votes for opposing options
- **Circular preferences**: A > B > C > A
- **Evaluation divergence**: Agents use incompatible criteria
- **Strategic blocking**: Agent holds out to force preferred outcome
- **Information asymmetry**: Agents make different assessments from different data

**Potential Effects**
- System hangs without decision
- Resource exhaustion from repeated deliberation
- Timeout with arbitrary or no decision
- User frustration with unresponsive system

## Mitigation Strategies

### Prevention
1. **Pre-declared tie-break weighting for the 3/4 majority rule**: The code review example deadlocks at a persistent 2-2 split because the 3/4 majority rule has no answer for an even split among 4 agents with orthogonal concerns (security, performance, readability, testing). Assign a pre-declared tie-break weight (e.g., Security agent's reject counts as 1.5 votes) so a structurally even-numbered panel can never produce a permanent tie. Trade-off: weighting one agent's vote higher institutionalizes a priority order that may not be right for every review.
2. **Deliberation round cap tied to the observed non-convergence pattern**: The example shows rounds 3-10 producing the identical 2-2 split with no new information — agents re-evaluate but reach the same conclusion, meaning further rounds are provably wasted. Cap deliberation at 2 rounds when the vote distribution is byte-for-byte identical across rounds, and treat a repeated identical split as an immediate escalation trigger rather than letting it run to round 10. Trade-off: capping too aggressively can cut off cases where an agent would genuinely change its mind on a slower timescale (e.g., after fetching more context).
3. **Criteria reconciliation before voting starts**: The deadlock stems from Agent A/B evaluating on objective code-quality risk (SQL injection, inefficiency) while Agent C/D evaluate on completeness (docs, tests) — these are evaluation-divergence votes, not disagreements about the same fact. Require agents to vote on decomposed sub-questions (is there a security issue? yes/no; is there a performance issue? yes/no) rather than a single approve/reject, so a security veto doesn't get diluted by unrelated readability approval. Trade-off: decomposing the vote adds process overhead and requires agreeing on the sub-question taxonomy up front.

### Detection & Response
1. **Identical-split repeat detector**: Since the failure signature in this file is the exact same 2-2 split recurring across 10 rounds, hash each round's vote distribution and flag immediately when round N's hash matches round N-1's — this is a stronger and faster signal than a generic round-count timeout.
2. **Blocking-agent identification**: When Agent A (Security) and Agent B (Performance) are consistently the reject votes with substantively different objections (SQL injection vs. inefficient query), log which agent(s) anchor each side of the deadlock so escalation to a human reviewer includes the specific unresolved objections, not just "no consensus."
3. **Deliberation-without-progress metric**: Track whether each round's vote rationale is materially different from the prior round's (via text diff/embedding) — the example's rounds 3-10 show agents "re-evaluate" but land on the same conclusion, meaning zero information gain per round, which is a stronger deadlock signal than round count alone.

### Architecture Patterns
1. **Escalation-to-human after bounded rounds with objection summary**: After 2 rounds of an identical split, auto-generate a summary of the specific competing objections (SQL injection risk vs. inefficiency vs. clean code) and route to a human reviewer with that summary attached, rather than a bare "consensus failed" notice. Deployment consideration: requires a human-in-the-loop channel and SLA for review turnaround, or the escalation itself becomes a new bottleneck.
2. **Weighted/quorum voting with domain-priority ordering**: Replace flat 3/4 majority with a quorum rule where a Security reject is a hard veto regardless of other votes (since SQL injection is a correctness/safety issue, not a style preference), while Readability/Testing objections require only a simple majority to override. Deployment consideration: must be calibrated per domain — a hard security veto is appropriate for code review but could be too rigid for lower-stakes decisions.
3. **Sequential/staged consensus instead of single-shot 4-way vote**: Resolve orthogonal concerns in priority order (security gate, then performance gate, then style/testing) instead of asking all 4 agents to vote simultaneously on one approve/reject — this avoids conflating "reject for security" with "reject for readability" into one deadlocked tally. Deployment consideration: increases latency since gates run sequentially rather than in parallel, and an early gate rejection means later agents' work may be wasted.

### Metrics
1. **consensus_round_count**: Target median < 2 rounds to resolution; Alert if p95 exceeds 4 rounds.
2. **identical_split_recurrence_rate**: Target 0% of tasks with 2+ consecutive rounds producing byte-identical vote distributions; Alert if > 5% of consensus tasks hit this.
3. **escalation_rate**: Target < 10% of consensus decisions requiring human escalation; Alert if > 25%, indicating the tie-break/quorum rules are miscalibrated.
4. **time_to_decision**: Target < 60 seconds median for automated consensus (excluding human escalation); Alert if p95 > 5 minutes.

### Alerts
1. **Deadlock Round Cap Reached** (P1): Condition - deliberation reaches the pre-declared round cap (e.g., 2 rounds) with an unresolved or repeated split. Action: auto-generate objection summary from all dissenting agents and escalate to human reviewer; do not allow further automated rounds.
2. **Identical Split Detected** (P2): Condition - vote distribution hash in round N matches round N-1 exactly. Action: skip remaining scheduled rounds and trigger escalation immediately rather than waiting for the round cap.
3. **Security/Safety Veto Overridden** (P1): Condition - a domain-critical objection (e.g., security reject) is outvoted by non-safety-related approvals under the quorum rule. Action: block merge/decision regardless of tally and require explicit human sign-off on the safety objection.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - System design issues including consensus
- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Multi-agent decision failures
- [Redis: Why Multi-Agent LLM Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Coordination deadlocks
