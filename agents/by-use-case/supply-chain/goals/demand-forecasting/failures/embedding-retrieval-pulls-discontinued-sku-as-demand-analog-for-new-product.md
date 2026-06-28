# Embedding Retrieval Pulls Discontinued SKU as Demand Analog for New Product

## Issue: A Demand-Forecasting Agent Generating a Cold-Start Forecast for a New Product by Retrieving the Most Similar Historical SKU via Embedding Similarity Over Product Descriptions Selects a Past SKU That Reads as Similar in Category and Description but Was Discontinued for Demand Reasons Specific to That Product, Producing a Forecast That Inherits a Demand Pattern Unrelated to the New Product's Actual Market

**Frequency**: Occasional

**Symptoms**
- The new product's forecast closely mirrors a specific historical SKU's demand curve, but that SKU's demand pattern was driven by circumstances -- a defect recall, a pricing error, a short-lived promotional spike -- that have no bearing on the new product
- Querying the product catalog by category, price tier, and target segment, rather than by description similarity, surfaces a different historical SKU that is a more representative demand analog
- The retrieved analog SKU's own historical record shows it was discontinued, but the forecasting agent's retrieval did not weight discontinuation reason as a factor in similarity ranking
- The mismatch concentrates on product categories with generic, recurring description language (e.g., "wireless earbuds, mid-range"), where many SKUs across very different actual demand trajectories share similar text
- The forecast is presented with full confidence and no indication that its basis was a single retrieved analog rather than a broader category-level demand model

**Root Cause**
Selecting a demand analog via embedding similarity over product descriptions optimizes for textual or topical similarity, not for similarity in actual demand drivers or confirmation that the retrieved SKU's historical demand pattern reflects normal market behavior rather than an anomalous event specific to that product. When a retrieved analog's demand history was shaped by a cause unrelated to general category demand -- a recall, a pricing error -- the similarity signal driving retrieval has no mechanism to detect or exclude that anomaly, since it ranks purely on description text.

**Example**
```
Demand-forecasting agent generates a cold-start forecast for a new mid-range wireless earbud model launching next quarter
Agent retrieves the most similar historical SKU via embedding similarity over product descriptions, surfacing a discontinued mid-range earbud model from two years earlier
That discontinued model's demand history shows a sharp spike followed by a steep decline, driven by a now-resolved supply-chain pricing error that triggered a temporary deep discount, not normal category demand
Forecast for the new product inherits a demand curve shaped like the discontinued analog's anomalous spike-and-decline pattern
Initial production and inventory commitments are sized to the anomalous curve rather than the new product's actual, more gradual adoption pattern, resulting in early-cycle overstock
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented systems are documented to surface a taxonomy of retrieval errors distinct from generation errors, including retrieving a topically similar but substantively unrepresentative record when similarity search is used without filtering for anomalous source data | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Multi-agent consensus-seeking research in supply-chain contexts identifies grounding demand-forecast analogs in confirmed, representative historical data, rather than description-similarity retrieval alone, as a distinct reliability requirement | [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184) |
| Knowledge-oriented retrieval-augmented generation surveys identify retrieval over generic, recurring descriptive language as a distinct failure mode from retrieval over rare, distinguishing product attributes | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |

**Contributing Factors**
- Demand-analog retrieval is implemented over product description text via similarity search rather than over structured category, price-tier, and target-segment fields combined with a check of the analog's discontinuation or anomaly status
- No validation step confirms a retrieved analog's historical demand pattern reflects normal category demand rather than an anomalous, product-specific event before the forecast is built on it
- Categories with generic, recurring description language are not flagged for mandatory structured-field matching or anomaly screening before similarity matching is trusted

---

## Mitigation Strategies

1. **Structured Category and Anomaly-Screened Matching as Primary Path**: Require demand-analog selection to match on structured category, price-tier, and target-segment fields first, and to exclude any candidate analog whose historical record shows a known demand anomaly, falling back to unscreened description similarity only when no qualifying analog exists
2. **Discontinuation-Reason Check Before Analog Use**: Before using a discontinued SKU as a demand analog, require confirmation of its discontinuation reason, excluding analogs discontinued due to recalls, pricing errors, or other anomalous events unrelated to general category demand
3. **Multi-Analog Ensemble Rather Than Single-SKU Basis**: Require cold-start forecasts to be built from an ensemble of multiple qualifying analogs rather than the single most similar SKU, reducing sensitivity to any one analog's anomalous history
4. **Surface Analog Basis in Forecast Output**: Require any cold-start forecast to indicate which historical SKU or SKUs it was based on and their discontinuation status, so planners can sanity-check the basis before committing inventory

### Metrics
- Rate of cold-start forecasts based on a single discontinued analog SKU with a known demand anomaly
- Rate of analog-matching retrievals falling back to unscreened description similarity due to no qualifying structured-field match
- Early-cycle inventory variance (overstock or understock) for new products forecast using a single-analog basis versus an ensemble basis

### Alerts
- A cold-start forecast is built on an analog SKU whose discontinuation reason is a known demand anomaly → P2
- A new product's early-cycle actual demand deviates from its analog-based forecast beyond the defined tolerance → P2
- Single-analog-basis forecasts as a share of total cold-start forecasts exceed the defined threshold for a rolling window → P3

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
