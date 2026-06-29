# Context-Window Loss Drops Related-Party Finding Across Long Document-Review Session

## Issue: A Due-Diligence Agent Reviewing a Target Company's Document Set in a Single Long Conversation Establishes Early in the Session That a Counterparty Entity Named in Several Contracts Is Actually a Related Party (a Founder-Controlled Affiliate, an Entity Sharing Common Ownership With the Target) Requiring Heightened Scrutiny, but as the Session Grows Across Dozens of Subsequent Document Reviews, That Related-Party Determination Falls Out of the Agent's Effective Context and Later Contracts Involving the Same Counterparty Are Reviewed as Ordinary Arm's-Length Agreements

**Frequency**: Occasional

**Symptoms**
- Early in the diligence session, the agent correctly flags a counterparty as a related party and notes that all agreements with that entity require related-party-transaction scrutiny (fairness of terms, required disclosures, board approval requirements)
- Dozens of documents later in the same session, a new contract with the identical counterparty entity is reviewed and summarized as a standard arm's-length vendor or customer agreement, with no related-party flag attached, even though the entity name is unchanged
- The related-party determination is present verbatim earlier in the session transcript but does not appear in the agent's later-stage outputs or reasoning, consistent with the original finding having fallen out of effective context rather than being explicitly reversed
- Re-presenting the same later contract in a fresh, short context that explicitly includes the related-party finding causes the agent to correctly flag it, confirming the lapse was a context-availability issue rather than a substantive disagreement about the entity's status
- The final diligence memo, compiled from the session's running notes, treats some agreements with the related party as flagged and others as unflagged depending solely on how far into the session each document was reviewed

**Example**
```
Diligence agent begins reviewing target company's contract portfolio in one long session; document 4 of approximately 80 is a services agreement that reveals the counterparty, "Meridian Advisory LLC," is wholly owned by the target's founder -- agent correctly flags this as a related party requiring heightened scrutiny on all agreements with that name
Session continues through dozens of unrelated vendor, customer, and lease agreements
Document 57 is a separate consulting agreement, also with "Meridian Advisory LLC," involving materially above-market consulting fees -- a textbook related-party-transaction red flag
Agent's review of document 57 summarizes it as a standard consulting arrangement with no related-party note, because the document-4 finding establishing Meridian's related-party status is no longer within the agent's effective attention despite technically being earlier in the same context
Final diligence memo flags the document-4 services agreement as a related-party item but lists the document-57 consulting agreement under ordinary vendor contracts; the above-market consulting fee is never escalated for fairness review
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Model performance on tasks requiring retrieval of information from earlier in a long context degrades significantly as relevant content moves away from the beginning or end of the context window, even when the information remains technically present | [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) |
| Failure-mode taxonomies for LLM systems identify context-window degradation over long sessions as a distinct mechanism by which earlier-established facts or corrections are silently dropped without an explicit reversal | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |
| Hallucination surveys of LLM-based agents note that information loss across long working sessions can produce outputs inconsistent with earlier, correct determinations made in the same session, without any signal distinguishing a forgotten fact from a deliberate revision | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |

**Contributing Factors**
- The diligence review is conducted as one continuous, growing session rather than discrete batches with an explicitly carried-forward findings ledger
- Related-party status, once established, is not promoted to a structured, persistently-injected fact (e.g., a standing "flagged entities" list re-included in every subsequent prompt) and instead relies on the model's own attention over the full transcript
- Document review volume (dozens of contracts) is large enough that early findings are many turns removed from later documents involving the same counterparty by the time they would need to be recalled
- No automated cross-reference step checks each new document's counterparty name against a running list of previously flagged related parties independent of the model's in-context recall

---

## Mitigation Strategies

1. **Persistent Flagged-Entity Ledger**: Maintain a structured, external list of related parties and other standing findings established during the session, and re-inject that list into the prompt for every subsequent document review rather than relying on the model's recall of its own earlier output
2. **Deterministic Counterparty Cross-Check**: Run an automated, non-LLM check of each new document's counterparty name against the flagged-entity ledger before or alongside the agent's own review, independent of context-window recall
3. **Session Chunking With Explicit Carry-Forward**: Break long document-review sessions into smaller batches, each opened with an explicit summary of standing findings (flagged entities, open exceptions) from prior batches, rather than one continuously growing conversation
4. **Final-Memo Consistency Audit**: Before finalizing the diligence memo, run an automated check that every document involving a previously flagged related party is consistently flagged in the memo, rather than trusting the session's own narrative consistency

### Metrics
- Rate of documents involving a previously flagged related party that are not flagged as such later in the same session
- Position in the session (document number / token distance) at which related-party flagging consistency begins to degrade
- Number of sessions using a persistent flagged-entity ledger versus relying solely on in-context recall

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Flagged-entity inconsistency | A document's counterparty matches the flagged-entity ledger but the agent's review does not include a related-party flag | P1 | Block memo finalization; re-review flagged document with ledger explicitly injected |
| Long session without ledger re-injection | Session exceeds a defined document-count or token threshold without a standing-findings re-injection | P2 | Trigger session chunking and carry-forward summary |
| Final-memo flagging gap | Consistency audit finds a related-party agreement listed as unflagged in the final memo | P1 | Escalate for manual related-party-transaction fairness review before deal close |

---

## References

- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
