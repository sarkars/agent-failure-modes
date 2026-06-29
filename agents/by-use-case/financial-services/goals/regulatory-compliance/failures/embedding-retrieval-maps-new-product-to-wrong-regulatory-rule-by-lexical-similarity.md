# Embedding Retrieval Maps New Product to Wrong Regulatory Rule by Lexical Similarity

## Issue: A Compliance Agent Classifying a Newly Launched Financial Product Against the Applicable Regulatory Rule Set Selects the Rule Whose Description Is Most Lexically or Embedding-Similar to the Product's Marketing Description, Rather Than Matching on the Product's Structured Regulatory Classification Code, Applying the Wrong Rule Set to a Structurally Different Product

**Frequency**: Occasional

**Symptoms**
- A newly launched product is screened and cleared against a regulatory rule set whose description closely resembles the product's marketing language, while the rule set that actually applies to the product's structured regulatory classification is never consulted
- The agent's rule-set selection is driven by similarity matching over the product's free-text marketing description, not by matching the product's structured regulatory classification code or registration category
- Auditing the selected rule set against the product's actual structured classification shows a mismatch, with a different rule set's disclosure, suitability, or reporting requirements applying instead
- Products with novel or hybrid marketing descriptions show a materially higher rate of rule-set mismatch than products whose marketing language closely tracks their structured classification, since novel descriptions produce a weaker classification-specific similarity signal
- The mismatch is discovered only when a regulator's examination or a structured post-launch audit re-classifies the product correctly, by which point the product has been marketed and sold under the wrong disclosure regime

**Root Cause**
Selecting an applicable regulatory rule set by similarity matching over a product's marketing description optimizes for the most textually similar rule description, not for confirming that the product's structured regulatory classification actually falls under that rule set's scope. When a product's marketing language uses terminology that overlaps with a different rule category's typical description -- common for novel or hybrid products designed to appeal to a broad audience -- the similarity signal driving the rule-set selection does not distinguish a coincidental lexical match from the product's true, structurally determined classification.

**Example**
```
Compliance agent classifies a newly launched structured product whose marketing materials describe it as offering "principal protection with market-linked upside"
Agent's similarity match selects the rule set governing traditional fixed-deferred annuities, whose standard description uses closely matching language about principal protection and market-linked returns
Product's actual structured regulatory classification is a market-linked structured note, which falls under a different disclosure and suitability rule set with materially different risk-disclosure requirements
Product is marketed and sold for several months under the annuity rule set's disclosure requirements, omitting structured-note-specific risk disclosures the correct rule set would have required
Mismatch is discovered during a regulatory examination that re-classifies the product correctly, triggering a retroactive disclosure remediation for all sales made under the wrong rule set
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented and similarity-based matching systems are documented to surface a taxonomy of retrieval errors distinct from generation errors, including matching a topically or lexically similar but substantively unrelated record when similarity search is used in place of classification-code-based lookup | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Research using large language models for legal-rule retrieval over large datasets identifies structured-attribute or classification-code matching, rather than free-text similarity, as a distinct requirement for reliable rule-set selection | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Research on agentic AI applied to financial-services modeling and model-risk-management tasks identifies product-classification resolution as a distinct reliability requirement separate from the accuracy of downstream compliance-rule application | [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439) |

**Contributing Factors**
- Regulatory rule-set selection for newly launched products is performed via marketing-description similarity rather than structured regulatory classification code
- No validation step confirms the selected rule set's scope actually covers the product's structured classification before the rule set is applied
- Novel or hybrid product descriptions are not flagged for mandatory classification-code-based verification before a similarity-matched rule set is trusted

---

## Mitigation Strategies

1. **Classification-Code Matching as Primary Path**: Require regulatory rule-set selection to match on the product's structured regulatory classification code first, falling back to marketing-description similarity only when no classification code is yet assigned, and flagging that fallback explicitly
2. **Mandatory Classification Confirmation Before Rule-Set Application**: Before applying a selected rule set to a new product, require confirmation that the product's structured classification falls within that rule set's defined scope, rather than relying on description similarity alone
3. **Novel-Product Flagging for Mandatory Secondary Review**: Maintain a flag for products with novel or hybrid marketing descriptions and require any rule-set selection for those products to undergo mandatory secondary classification-code verification
4. **Surface Selection Method in Output**: Require any product compliance clearance to indicate whether the rule set was selected by classification code or by description similarity, so reviewers can prioritize verification of similarity-based selections

### Metrics
- Rate of product rule-set selections established by description similarity rather than classification-code match
- Rate of similarity-matched rule-set selections that fail a classification-code verification check when audited
- Number of disclosure-remediation events later found to trace back to a rule-set selection error

### Alerts
- A product clearance used to launch sales has no classification-code confirmation of the applied rule set → P1
- A similarity-matched rule-set selection fails classification-code verification on audit after the product has already launched → P1
- Description-similarity fallback rate for rule-set selection exceeds the defined threshold for a rolling window → P2

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
