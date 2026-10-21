# Inconsistent Answers

## Issue: Agent gives different answers across turns.

**Frequency**: Occasional

**Symptoms**
- Contradictory responses for same fact/policy.
- Agent states a different policy value (return window, fee amount, SLA) later in the same conversation than it stated earlier, without acknowledging the change.
- Two independent sessions asking the identical policy question receive materially different answers, revealing retrieval or generation-level nondeterminism rather than a genuine policy change.

**Root Cause**
There is no single canonical source per policy topic, so retrieval can surface a different, overlapping, or outdated document depending on how a question happens to be phrased, and the knowledge base itself often contains duplicate or conflicting entries for the same policy that were never deduplicated. Rather than being grounded in one fixed retrieved passage, the model reconstructs each answer from weak parametric memory on every turn, and because the agent keeps no structured record of facts it has already asserted earlier in the conversation, nothing checks a new answer against what was already said before it goes out.

**Example**
```
Agent (turn 2): "Our return window is 30 days from the delivery date."
...
User (turn 9): "So just to confirm, how many days do I have to return this?"
Agent (turn 10): "You have 14 days from the delivery date to return it."
User: "Wait, you told me 30 days earlier in this same chat."
```

**Contributing Factors**
- No single canonical source per policy topic — retrieval surfaces different, overlapping, or outdated documents depending on query phrasing.
- Model reconstructs the answer from weak parametric memory each turn instead of being grounded in a fixed retrieved passage or deterministic lookup.
- No conversation-level memory of facts already asserted, so later turns don't check consistency against earlier ones before answering.
- Knowledge base contains duplicate or conflicting entries for the same policy that haven't been deduplicated.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Same-conversation policy repeat | Ask the same policy question (e.g., return window) once early and once late in a multi-turn conversation | Identical answer both times, grounded in the same retrieved source | Second answer contradicts the first |
| Cross-session variance | Ask a fixed canonical policy question across 20 independent sessions | All 20 sessions return the same value | Answers vary across sessions for a policy that hasn't changed |
| Duplicate knowledge-base entries | Knowledge base seeded with two conflicting versions of the same policy doc | Agent retrieves and cites the canonical/deduplicated entry consistently | Agent's answer depends on which duplicate entry retrieval happened to surface |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Cross-turn contradiction rate (eval set) | <1% | Percentage of multi-turn eval conversations where a later answer contradicts an earlier one on the same fact |
| Canonical policy answer variance (eval set) | <5% deviation | Deviation in answers to a fixed set of policy questions across repeated independent eval runs |
| Grounded response rate (eval set) | >95% | Percentage of factual/policy eval responses that cite a retrieved source rather than free-generating |

---

## Mitigation Strategies

### Prevention
1. **Single source-of-truth grounding**: require every factual/policy claim to be generated from a retrieved passage (RAG) rather than parametric memory, and cite the source, since inconsistency across turns stems from the model reconstructing an answer from weakly-grounded internal knowledge each time rather than reading the same canonical source. Trade-off: adds retrieval latency and requires the knowledge base to be comprehensive and current, or grounding fails silently.
2. **Conversation-level fact cache**: once a fact/policy answer is given in a conversation, cache it and reuse the cached value for the rest of the session instead of re-deriving it on each turn. Trade-off: if the cached fact was wrong, the error now persists consistently through the whole conversation instead of surfacing as a visible contradiction.
3. **Cross-turn consistency check before sending**: before finalizing a response, compare the new claim against prior claims in the same conversation and recently retrieved passages, resolving contradictions before responding. Trade-off: adds an extra model call's worth of latency and cost to every turn.

### Detection & Response
1. **Contradiction pair detection**: run an automated same-conversation contradiction detector (NLI-style entailment check between turns) over live transcripts to catch conflicting answers to the same question. Response: flag the conversation for review and, if confirmed, send the user a corrected/clarifying follow-up.
2. **Policy-drift monitoring across sessions**: sample answers to a fixed set of canonical policy questions across many independent sessions and check variance; high variance indicates ungrounded or stale-retrieval-driven inconsistency. Response: investigate whether the knowledge base has duplicate/conflicting entries.
3. **User-flagged contradiction reports**: detect user language like "you just said..." and route to a contradiction-review queue. Response: human confirms and patches the knowledge base or retrieval ranking.

### Architecture Patterns
1. **RAG with canonical single-document retrieval**: architect retrieval to prefer one canonical, deduplicated source per policy topic (versus multiple overlapping documents) so the same query reliably surfaces the same passage, removing a major source of turn-to-turn variance.
2. **Conversation-memory checkpointing of asserted facts**: maintain an explicit structured memory of facts/policies already asserted in the conversation and inject it into every subsequent generation call as a hard constraint, rather than relying on the model to recall its own prior turns from raw transcript context.
3. **Deterministic policy-lookup service**: move high-stakes, frequently-asked policy facts (pricing, refund windows, SLAs) out of free-form generation entirely into a deterministic lookup service the agent calls, eliminating generation-level inconsistency for the highest-impact facts.

### Metrics
1. **cross_turn_contradiction_rate**: Target: <1% of multi-turn conversations; Alert on >2.5% weekly
2. **canonical_policy_answer_variance**: Target: <5% deviation across sampled sessions for fixed test questions; Alert on >15%
3. **user_flagged_contradiction_rate**: Target: <0.5% of conversations; Alert on >1.5%
4. **grounded_response_rate**: Target: >95% of factual/policy claims cite a retrieved source; Alert on <90%

### Alerts
1. **Contradiction Rate Spike** (P2): Condition - cross_turn_contradiction_rate exceeds 2.5% over 24h. Action: sample flagged conversations, check for recent knowledge-base changes or retrieval regressions.
2. **Canonical Answer Variance** (P2): Condition - fixed-question eval shows >15% variance across sessions. Action: audit the knowledge base for duplicate/conflicting entries on the affected topic.
3. **User-Reported Contradiction Surge** (P3): Condition - user_flagged_contradiction_rate exceeds 1.5% weekly. Action: prioritize knowledge-base cleanup for the most-flagged topics.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| cross_turn_contradiction_rate | >2.5% weekly |
| canonical_policy_answer_variance | >15% |
| user_flagged_contradiction_rate | >1.5% weekly |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Contradiction Rate Spike | cross_turn_contradiction_rate exceeds 2.5% over 24h | Medium |
| Canonical Answer Variance | Fixed-question eval shows >15% variance across sessions | Medium |
| User-Reported Contradiction Surge | user_flagged_contradiction_rate exceeds 1.5% weekly | Low |

---

## Chat assistant examples

### Contradicts an earlier answer without saying so

*Illustrative transcript, not a real product log. "Trailhead Outfitters" is an invented US outdoor-gear retailer.*

```
Before:
User: (turn 2) How long do I have to return the Ridgeline tent?
Bot:  30 days from delivery.
      ... eight turns about shipping and sizing ...
User: (turn 10) So I have until the 20th to send it back?
Bot:  Yes, the return window is 14 days from delivery.
      (the 30-day answer was never mentioned again)

After:
Bot:  I need to correct what I told you earlier. I said 30 days, but our policy for camping gear is 14 days from delivery. Your window ends on Nov 3. Sorry for the mix-up.
```

**What the user experiences:** two answers to the same question in one chat, with no sign of which one to trust or why the answer changed.

**Fix:** before sending a fact already stated in the conversation, compare it with the earlier answer. If it differs, say so, say which one is right, and say why (for example, the first answer was wrong or the policy differs by item). See the [confident wrong answer with no way to check](../../../../../by-capability/human-machine-interface/goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) pattern.

### Different answers by session or regeneration

*Illustrative transcript, not a real product log. "Harbor Mutual" is an invented US auto insurer.*

```
Before:
User: (session 1) Does my policy cover a rental car after an accident?
Bot:  Yes, up to $40 per day for 30 days.
User: (session 2, same policy, same question, a few minutes later)
Bot:  Rental coverage is $30 per day for up to 20 days.

After:
Bot:  Your policy includes rental reimbursement of $40 per day for up to 30 days (Coverage Summary, rental section).
      (both sessions read the same policy record and give the same answer)
```

**What the user experiences:** asking again, or opening a new chat, changes the answer, so they cannot tell which number to rely on.

**Fix:** read policy facts such as limits and dates from one source of truth (the customer's policy record) and quote them, rather than letting the model generate them. The same question on the same data must return the same answer. See the [confident wrong answer with no way to check](../../../../../by-capability/human-machine-interface/goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) pattern.

### Agents contradict each other

*Illustrative transcript, not a real product log. "Pinecrest Home" is an invented US online furniture store whose assistant routes questions to a billing agent and a shipping agent.*

```
Before:
User: Where's my order and when will I be charged?
Bot (billing agent):  Your card was charged $412.60 on Oct 14.
User: So when does it arrive?
Bot (shipping agent): Your order hasn't shipped yet. You'll be charged when it ships.
User: But you just said I was already charged?

After:
Bot:  Your card was charged $412.60 on Oct 14, and the order is waiting to ship. The charge happened at checkout, not at shipping, so the shipping note was wrong. Expected ship date: Oct 22.
      (one reply, built after the two agents' answers were compared)
```

**What the user experiences:** one chat gives two incompatible answers about the same order, with no sign of which one to believe.

**Fix:** have one coordinating step collect the agents' answers and check them against the same order record before anything is sent; if they disagree, resolve it (or say what is uncertain) and reply once, in one voice. One vendor article describes this pattern as passing agents' outputs through a final step that settles disagreements before the reply goes out ([Cobbai](https://cobbai.com/blog/agent-orchestration-customer-service), opened; vendor source). See the [confident wrong answer with no way to check](../../../../../by-capability/human-machine-interface/goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) pattern.

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
