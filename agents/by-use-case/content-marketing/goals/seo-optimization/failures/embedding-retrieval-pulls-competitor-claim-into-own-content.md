# Embedding-Retrieval Pulls Competitor Claim into Own Content

## Issue: A Content-Generation Agent's RAG Step, Used to Ground Marketing Copy in "Similar High-Performing Content" Retrieved from a Crawled Corpus, Pulls in a Factual or Comparative Claim from a Competitor's Published Content Because It Is Embedding-Similar to the Target Topic, and the Agent Incorporates That Claim into the Brand's Own Copy as If It Were a Verified, Brand-Owned Fact

**Frequency**: Occasional

**Symptoms**
- Published marketing copy contains a specific statistic, comparative claim, or product capability statement that traces back, on investigation, to a competitor's blog post or product page in the agent's retrieval corpus rather than to any internal, brand-verified source
- The retrieved source document is topically and lexically similar to the target content's subject (same product category, overlapping keywords) but is not actually one of the brand's approved reference sources
- Legal/compliance review catches the issue only after publication, when a comparative claim attributed implicitly to the brand's own product turns out to be a competitor's marketing claim about their own product, not a substantiated fact about the brand's offering
- The pattern recurs across multiple pieces of generated content sharing the same topic cluster, since the same competitor source remains in the retrieval corpus and continues to surface as a high-similarity match for related future content requests
- Disabling retrieval from the general crawled corpus and restricting it to an approved internal source list eliminates the issue, isolating the retrieval source -- not the generation step -- as the point of failure

**Root Cause**
The content-generation agent's retrieval step ranks candidate source documents by embedding similarity to the target topic across a broadly crawled corpus that was not curated to exclude competitor content, and the agent's generation prompt does not distinguish between "this retrieved passage is an approved, brand-verified source" and "this retrieved passage is merely topically similar." Because a competitor's claim about their own product can be highly similar in embedding space to the brand's own target topic, the retriever surfaces it as a relevant grounding source, and the generation step incorporates its substance without flagging that the source's claim was never about the brand's product at all.

**Example**
```
Content agent is asked to draft a comparison-style blog post about a product feature, and its RAG step retrieves "similar high-performing content" from a corpus that includes competitor blog posts crawled for topical research
A competitor's blog post claiming "industry-leading 40% faster processing" for their own product is retrieved as a top-similarity match because it shares dense topical vocabulary with the requested post
Generated draft includes the phrase "delivering up to 40% faster processing" in a paragraph describing the brand's own product, without the generation step distinguishing that the retrieved figure was the competitor's claim about their own offering, not a verified internal benchmark
Post is published; a customer who attempts to verify the figure against the brand's actual published benchmarks finds no support for it, and legal flags the unsubstantiated and inadvertently competitor-sourced claim after the fact
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLMs used for customized marketing content generation at scale require explicit grounding and evaluation controls, since unconstrained generation is documented to produce unsubstantiated or misattributed claims when retrieval sources are not curated | [LLMs for Customized Marketing Content Generation and Evaluation at Scale](https://arxiv.org/html/2506.17863v1) |
| Most-similar retrieved passages are not necessarily the most relevant or appropriate source for a given generation task, a structural limitation of similarity-ranked retrieval that does not account for source provenance or ownership | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Pulling supporting content from the wrong source document undermines the validity of generated output even when the retrieved text is locally well-formed and topically relevant | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |

**Contributing Factors**
- Retrieval corpus includes broadly crawled competitor and third-party content alongside approved internal sources, with no provenance tag distinguishing the two at retrieval time
- Generation prompt does not require the agent to verify that a retrieved factual or comparative claim is attributable to an approved, brand-owned source before incorporating it into copy
- No automated post-generation check cross-references published claims against the brand's internal benchmark/fact repository before content goes live

---

## Mitigation Strategies

1. **Provenance-Tagged Retrieval Corpus**: Tag every document in the retrieval corpus with its source type (approved internal source, competitor content, general third-party content) and exclude or strongly down-weight non-approved sources from retrieval used to ground factual or comparative claims
2. **Mandatory Source-Attribution Check Before Incorporation**: Require the generation step to explicitly verify that any specific statistic or comparative claim it incorporates traces to an approved internal source, rejecting or flagging claims sourced from competitor or unverified third-party content
3. **Automated Fact-Claim Cross-Reference Before Publication**: Run an automated check comparing every specific statistic or comparative claim in generated copy against the brand's internal benchmark/fact repository before publication, blocking publication on an unverified match
4. **Exclude Competitor Domains from the Research Corpus by Default**: Maintain an explicit exclusion list of competitor domains for any retrieval corpus used to ground first-party marketing claims, reserving competitor content retrieval for clearly labeled competitive-research workflows only

### Metrics
- Rate of published content found, on audit, to contain a claim traceable to a non-approved or competitor source
- Percentage of generation requests where retrieval surfaced at least one non-approved-source document above the relevance threshold
- Time between publication and detection of a misattributed or unsubstantiated claim, by detection method (automated check vs. manual/legal review)

### Alerts
- Automated fact-claim cross-reference finds a published claim with no match in the internal benchmark repository and a match in a competitor-domain source → P1
- Generation request retrieves a competitor-domain document as a top grounding source for first-party marketing copy → P2
- Retrieval corpus is updated or re-crawled without refreshing the source-provenance tagging or competitor-domain exclusion list → P3

---

## References

- [LLMs for Customized Marketing Content Generation and Evaluation at Scale](https://arxiv.org/html/2506.17863v1)
- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
