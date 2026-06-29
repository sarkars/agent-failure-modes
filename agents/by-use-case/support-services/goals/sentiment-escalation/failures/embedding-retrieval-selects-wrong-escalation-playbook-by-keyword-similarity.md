# Embedding Retrieval Selects Wrong Escalation Playbook by Keyword Similarity

## Issue: A Sentiment-Escalation Agent That Selects an Escalation Playbook by Embedding Similarity Against a Playbook-Description Index, Rather Than Against the Structured Severity Tier the Conversation Actually Belongs To, Matches the Conversation to a Superficially Similar but Wrong Playbook, Routing It Through an Escalation Path That Does Not Match the Actual Risk Level

**Frequency**: Occasional

**Symptoms**
- A conversation involving a safety-adjacent complaint (a billing error the customer describes as making them unable to afford medication, a service failure they describe as endangering a dependent) is routed through a generic "frustrated customer" playbook rather than the higher-severity playbook the actual content warrants
- The conversation's free-text language uses emotionally similar vocabulary ("this is ruining my life," "I'm so angry") to a lower-severity playbook's description, while the structured severity tier the conversation should map to is never separately checked
- Cross-referencing the conversation's actual content against the severity-tier taxonomy, rather than matching transcript text to playbook descriptions, shows definitively which playbook should have been selected
- The misselect concentrates on playbooks with overlapping emotional-intensity vocabulary in their descriptions, since that vocabulary does not distinguish "customer is upset" from "customer's situation is high-risk"
- The misselect is caught only when a human reviewer audits the escalation after the fact and finds the playbook's response steps inadequate for the actual severity, by which point the response delay has already occurred

**Root Cause**
Selecting an escalation playbook by matching a conversation's free text against a playbook-description index via embedding similarity optimizes for textual and emotional-tone similarity to a playbook's description, not for confirming which structured severity tier the conversation's actual content belongs to. When emotionally intense vocabulary overlaps across playbooks designed for very different risk levels, the similarity signal cannot distinguish "this conversation sounds upset" from "this conversation describes a high-risk situation," especially when the structured severity classification, which would resolve the ambiguity directly, is never consulted.

**Example**
```
Customer writes: "This billing error has completely ruined my month, I can't believe how angry I am about this"
Escalation agent classifies the conversation via embedding similarity against the full playbook index, and the "frustrated-customer de-escalation" playbook scores as the closest textual and tonal match
Conversation routes through the standard de-escalation playbook
A later message in the same thread reveals the billing error left the customer unable to afford a medication refill this month, which maps to the "financial-hardship-risk" playbook requiring expedited resolution and a hardship-team handoff
Standard de-escalation playbook's response steps do not include expedited resolution, delaying the actual fix by two additional business days
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented and similarity-based classification systems are documented to surface a taxonomy of retrieval errors distinct from generation errors, including matching a topically similar but substantively wrong category when similarity search is used in place of structured-data confirmation | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Surveys of knowledge-oriented retrieval-augmented generation identify that similarity-based retrieval over free text systematically underperforms structured-attribute matching when the distinguishing factor is a categorical or severity attribute rather than topical content | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Hybrid AI-router research finds that routing decisions based on surface-level query similarity alone produce systematically different outcomes than routing decisions grounded in a structured classification of the underlying task, particularly when surface vocabulary overlaps across categories with different required handling | [Toward Super Agent System with Hybrid AI Routers](https://arxiv.org/pdf/2504.10519) |

**Contributing Factors**
- Playbook selection is performed via similarity search over playbook-description text rather than by cross-referencing a structured severity-tier classification of the conversation's actual content
- No validation step confirms the selected playbook's severity tier matches a structured classification of the conversation before the escalation proceeds
- Playbook pairs with overlapping emotional-intensity vocabulary in their descriptions are not flagged for mandatory structured-severity confirmation before similarity-based selection is trusted

---

## Mitigation Strategies

1. **Structured Severity-Tier Classification as Primary Path**: Require playbook selection to be driven by a structured severity-tier classification of the conversation's actual content first, restricting playbook-similarity matching to disambiguating within that tier rather than across the full, unrestricted playbook index
2. **Block Selection Across Severity-Tier Mismatch**: Prohibit a conversation from routing through a playbook whose severity tier does not match the structured classification, regardless of how closely the conversation's text matches that playbook's description
3. **Overlapping-Vocabulary Playbook Review**: Identify playbook pairs with high emotional-intensity vocabulary overlap but different severity tiers, and either disambiguate their descriptions or flag conversations potentially matching either for mandatory structured-severity confirmation before selection
4. **Surface Selection Basis in Escalation Output**: Require any playbook-selection decision to indicate whether it was confirmed against a structured severity classification or based on text-similarity alone, so reviewers can prioritize verification accordingly

### Metrics
- Rate of selected playbooks whose severity tier does not match a structured classification of the conversation's actual content
- Rate of escalations re-routed by a human reviewer due to the originally selected playbook's severity tier being inadequate
- Average added response delay attributable to severity-tier-mismatch re-routes

### Alerts
- A conversation routes through a playbook whose severity tier does not match a structured classification of its content → P2
- Severity-tier-mismatch re-route rate exceeds the defined threshold for a rolling window → P3
- Overlapping-vocabulary playbook pairs show a sustained elevated misselect rate after review → P3

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Toward Super Agent System with Hybrid AI Routers](https://arxiv.org/pdf/2504.10519)
