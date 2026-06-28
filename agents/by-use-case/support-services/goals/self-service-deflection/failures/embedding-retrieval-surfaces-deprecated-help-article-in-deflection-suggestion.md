# Embedding Retrieval Surfaces Deprecated Help Article in Deflection Suggestion

## Issue: A Self-Service Deflection Agent's RAG Step, Used to Suggest a Help Article to Resolve a Customer's Question Without Human Involvement, Retrieves a Lexically and Semantically Similar but Deprecated or Product-Version-Mismatched Article Instead of the Current Correct One, Deflecting the Customer With Stale Instructions Framed as the Solution

**Frequency**: Common

**Symptoms**
- The deflection agent suggests a help article whose instructions reference UI elements, settings names, or steps that no longer exist in the current product version, even though a current, correct article exists in the knowledge base
- The retrieved article and the correct current article share a near-identical title and overlapping topic vocabulary, differing mainly in a "last updated" date or a version tag the retrieval step does not use as a filter
- Re-running the same retrieval query with the product version or article-currency status included as an explicit filter (rather than relying on text similarity alone) returns the correct current article, isolating the failure to retrieval scope rather than the correct article being absent
- The mismatch concentrates on topics where the product has changed significantly since an older article was written, maximizing the gap between the deprecated article's instructions and current reality while textual similarity to the topic remains high
- Customer marks the deflection as unhelpful or re-contacts support after following the deprecated instructions without success, requiring a second support interaction that the deflection was meant to avoid

**Root Cause**
The deflection agent selects a help article by semantic similarity over article text rather than by a structured currency or version-applicability attribute, so an outdated article addressing the same topic in similar language can score as similar or more similar than the current, correct article, especially if the current article was rewritten with different phrasing during the product update. The agent has no signal distinguishing "describes a similar-sounding topic" from "is the article that actually applies to the current product version," because retrieval never constrains the candidate set by currency before ranking by similarity.

**Example**
```
Customer asks: "How do I export my account data?"
Knowledge base contains two articles on this topic: an older one written for the previous product version's export flow, and a current one reflecting a redesigned export flow introduced two releases ago
Deflection agent's retrieval returns the older article as the top match, because its phrasing happens to align more closely with the customer's exact wording than the rewritten current article
Customer follows the older article's steps, which reference a settings menu location that no longer exists in the current product version, and cannot complete the export
Customer re-contacts support, now frustrated, requiring a human agent to resolve what the deflection was meant to handle automatically
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval reliability research finds that semantically similar but substantively different (here, outdated) documents are frequently confused by similarity-only retrieval when structured filtering on currency is unavailable | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Tool-use calibration research notes that retrieval-grounded agent suggestions require independent verification against structured ground truth (such as version currency), not similarity scores alone | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Business-scenario evaluation of LLM agents in support contexts identifies self-service deflection quality as sensitive to knowledge-base currency, distinct from general retrieval accuracy | [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878) |

**Contributing Factors**
- Article retrieval ranks candidates by free-text semantic similarity without first filtering to articles tagged as current for the customer's product version
- Deprecated articles remain in the searchable knowledge base without a structured "superseded by" link to the current replacement article
- No automated check compares the retrieved article's last-verified date or version tag against the customer's current product version before the deflection is sent

---

## Mitigation Strategies

1. **Structured Currency Filter Before Semantic Ranking**: Require article retrieval to filter candidates by a structured currency or version-applicability tag, matched against the customer's actual product version, before ranking by semantic similarity over article text
2. **Mandatory Supersession Linking**: Require any article superseded by a product update to carry a structured "superseded by" link to its replacement, and exclude superseded articles from deflection retrieval entirely once the link exists
3. **Deflection Outcome Tracking by Article Currency**: Track customer-marked-unhelpful and re-contact rates segmented by whether the suggested article was current or outdated at the time of suggestion, surfacing outdated-article deflections as a distinct quality signal
4. **Scheduled Currency Audit on High-Traffic Articles**: Periodically audit the most frequently retrieved articles for currency against the current product version, prioritizing articles covering features that have changed recently

### Metrics
- Rate of deflection suggestions retrieving an article tagged as superseded or outdated for the customer's product version
- Re-contact rate within a defined window following a deflection, segmented by retrieved-article currency
- Percentage of superseded articles with a structured "superseded by" link in place

### Alerts
- A deflection suggestion is sent citing an article tagged as superseded, with no supersession link excluding it from retrieval → P2
- Re-contact rate following deflections using outdated articles exceeds baseline for two consecutive reporting periods → P2
- A high-traffic article's currency audit lapses past its scheduled review date with no supersession check completed → P3

---

## References

- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878)
