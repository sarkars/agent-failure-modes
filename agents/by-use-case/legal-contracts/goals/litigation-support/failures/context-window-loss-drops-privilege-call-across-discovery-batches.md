# Context-Window Loss Drops Privilege Call Across Discovery Batches

## Issue: A Litigation-Support Agent Reviewing Discovery Documents in Sequential Batches Correctly Determines a Document Is Attorney-Client Privileged in an Early Batch, but When a Near-Duplicate or Forwarded Copy of the Same Email Thread Appears in a Later Batch Processed as a Fresh Context, the Agent Has No Memory of the Earlier Determination and Reviews It Inconsistently

**Frequency**: Common

**Symptoms**
- The same email thread (or a forwarded/near-duplicate copy of it) is marked privileged in one discovery batch and non-responsive-but-not-privileged, or produced outright, in a different batch reviewed earlier or later in the same matter
- Inconsistent privilege determinations cluster around documents with duplicate or near-duplicate family members split across separate review batches, rather than appearing as random review error
- Re-reviewing the inconsistent document pair together, in a single context that includes both the original privilege determination and the duplicate, produces a consistent result, isolating the failure to cross-batch memory loss rather than an unclear privilege question
- Privilege log generated at the end of review shows gaps where a document family has some members logged as privileged and others absent from the log entirely
- Opposing counsel or the court flags the inconsistency during a privilege challenge, since inconsistent treatment of near-duplicate documents is a common signal used to challenge privilege claims

**Root Cause**
Each discovery batch is typically processed as its own agent invocation or context window for throughput reasons, so a privilege determination made while reviewing one batch exists only within that batch's context and is not automatically available when a duplicate or near-duplicate document is encountered in a different batch's separate context. Without an explicit, persistent privilege-determination record that batches consult before re-deciding, the agent has no way to know that a document it is currently reviewing for the first time in its own context has, in fact, already been ruled on elsewhere in the same matter.

**Example**
```
Batch 14 (processed in its own context): Agent reviews an email thread between in-house counsel and the VP of Engineering discussing a product defect, correctly marks it privileged
Batch 47 (processed in a separate context, days later): The same email thread appears again, forwarded to an additional internal recipient as part of a different custodian's mailbox
Agent in Batch 47 has no access to the Batch 14 determination, reviews the forwarded copy fresh, and -- without the surrounding context that made privilege clear in the original thread -- marks it non-responsive rather than privileged
Production set includes the Batch 47 copy of a document that was correctly withheld as privileged in Batch 14, creating an inadvertent disclosure and a potential privilege waiver
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Persistent memory mechanisms for autonomous LLM agents are identified as a distinct architectural need precisely because per-invocation context does not carry determinations across separately processed work units | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |
| Multi-agent and multi-batch LLM workflows are documented to lose state at the boundary between separately invoked processing units unless an explicit shared record is maintained | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Surveys of LLMs in legal applications flag consistency of determinations across large discovery sets as a specific evaluation gap, distinct from per-document accuracy | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |

**Contributing Factors**
- Discovery batches are processed as independent agent invocations with separate context windows, with no shared privilege-determination record consulted across batches
- Near-duplicate and forwarded-copy detection (e.g., email-thread family grouping) runs as a separate deduplication step that is not integrated with the privilege-review step's decision record
- No automated consistency check compares privilege determinations across documents identified as members of the same email thread or document family

---

## Mitigation Strategies

1. **Persistent Cross-Batch Privilege Ledger**: Maintain a structured, persistent record of every privilege determination keyed to document-family identifiers (thread ID, near-duplicate cluster ID), and require every batch to check this ledger before issuing a fresh determination on a document that matches an existing family
2. **Family-Level Consistency Check Before Production**: Before finalizing the production set, automatically check that all documents identified as belonging to the same email thread or near-duplicate cluster received consistent privilege determinations, flagging any inconsistency for attorney review
3. **Route Duplicate-Family Members to the Original Reviewer Context**: When deduplication identifies a document as a near-duplicate or family member of an already-reviewed document, route it to be reviewed with the original determination explicitly provided as context, rather than reviewing it cold in a new batch
4. **Privilege Log Completeness Check**: Automatically verify that every document family with at least one privileged-determination member has a corresponding privilege log entry, and flag any family where some members are logged and others are silently absent

### Metrics
- Rate of document families (thread/near-duplicate clusters) with inconsistent privilege determinations across batches
- Number of family-level consistency check flags resolved before production versus discovered after production
- Percentage of duplicate-family members routed with the original determination provided as context versus reviewed cold

### Alerts
- Production set finalized with an unresolved family-level privilege inconsistency flag → P1
- A document inadvertently produced is later found to be a near-duplicate of a document marked privileged in a different batch → P1
- Privilege log completeness check finds a document family with partial logging → P2

---

## References

- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
