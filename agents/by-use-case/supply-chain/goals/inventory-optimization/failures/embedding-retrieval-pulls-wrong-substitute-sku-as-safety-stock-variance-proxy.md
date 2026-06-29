# Embedding Retrieval Pulls Wrong Substitute SKU as Safety-Stock Variance Proxy

## Issue: To Calculate Safety Stock for a New SKU Lacking Sufficient Sales History, an Inventory-Optimization Agent Retrieves the Most Similar Existing SKU via Embedding Similarity Over Product Descriptions to Borrow Its Demand-Variance Profile, but Selects a SKU That Is Textually Similar Yet Has a Fundamentally Different Volatility Pattern, Producing a Safety-Stock Level Calibrated to the Wrong Risk Profile

**Frequency**: Occasional

**Symptoms**
- A new SKU's safety stock is set using a demand-variance figure borrowed from a retrieved "similar" SKU, but that SKU's actual demand pattern (e.g., a steady staple item) is far less volatile than the new SKU's real market behavior (e.g., a trend-driven, promotion-sensitive item), or vice versa
- Querying the catalog by structured attributes (category, price tier, demand-driver type — staple vs. seasonal vs. promotional) rather than by description-text similarity surfaces a different, more representative substitute SKU
- The retrieved substitute's own historical coefficient of variation differs sharply from the new SKU's realized coefficient of variation once enough sales history accumulates, but the safety-stock calculation never re-evaluates the substitute choice after the borrowed-variance period ends
- Stockouts (when the substitute understated volatility) or chronic overstock (when the substitute overstated volatility) cluster specifically among new SKUs whose safety stock was set from a single retrieved substitute, versus new SKUs whose safety stock used a category-level variance benchmark
- The substitute-SKU selection step provides no indication that variance, rather than category or price tier, drove the match, so a downstream reviewer cannot easily tell the substitute was chosen on textual similarity alone

**Root Cause**
Selecting a variance-proxy SKU via embedding similarity over product description text optimizes for topical or descriptive similarity, not for similarity in the underlying demand-driver type that actually determines volatility. Two SKUs can share near-identical description text (same category, similar price point) while having entirely different demand-driver profiles — one a steady staple, one a promotion- or trend-sensitive item — and description-embedding similarity has no mechanism to distinguish them, since it never encodes the demand-driver classification that determines variance.

**Example**
```
A new SKU launches with no sales history: a limited-run, trend-driven sneaker colorway
Inventory-optimization agent retrieves the most similar existing SKU via embedding similarity over product descriptions to borrow a demand-variance estimate for the safety-stock formula
Retrieved substitute is a core, year-round sneaker model that shares near-identical description text (same brand, same shoe category, similar price) but is a steady staple with low demand variance
Safety stock for the new colorway is calculated using the staple SKU's low variance, producing a thin buffer
New colorway sells out within days of a social-media-driven demand spike the staple SKU's history gave no indication of, and the thin safety stock buffer is exhausted immediately
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented systems are documented to exhibit a taxonomy of retrieval errors distinct from generation errors, including retrieving a topically similar but substantively unrepresentative record when similarity search is used without filtering for the attribute that actually drives the downstream calculation | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Knowledge-oriented retrieval-augmented generation surveys identify retrieval over generic, recurring descriptive language as a distinct failure mode from retrieval over the rare, distinguishing attributes that determine a record's true behavior | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| LLM-based supply chain management research identifies inventory-policy parameters borrowed from a single retrieved analog, rather than a category-level or attribute-screened benchmark, as a documented source of miscalibrated stocking decisions | [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597) |

**Contributing Factors**
- Variance-proxy SKU selection is implemented over product description text via embedding similarity rather than over structured demand-driver classification (staple vs. seasonal vs. promotional vs. trend-driven)
- No validation step confirms the retrieved substitute's demand-driver type matches the new SKU's expected demand-driver type before its variance is borrowed
- Safety-stock formula does not re-evaluate or replace the borrowed-variance estimate once enough of the new SKU's own sales history accumulates to compute a direct estimate

---

## Mitigation Strategies

1. **Demand-Driver Classification as Primary Match Criterion**: Require variance-proxy selection to match on a structured demand-driver classification (staple, seasonal, promotional, trend-driven) first, falling back to unscreened description similarity only when no qualifying substitute exists within the new SKU's expected classification
2. **Category-Level Variance Benchmark as Default**: Where a confidently classified single substitute is unavailable, default to a category-level variance benchmark (computed across multiple SKUs sharing the new SKU's demand-driver type) rather than a single retrieved analog
3. **Mandatory Re-Evaluation Once Real History Accumulates**: Require the safety-stock calculation to replace the borrowed-variance estimate with a directly computed estimate as soon as the new SKU accumulates a defined minimum number of sales periods, rather than continuing to rely on the substitute indefinitely
4. **Surface Substitute Basis in Output**: Require any safety-stock calculation using a borrowed-variance substitute to indicate which SKU was used and its demand-driver classification, so planners can sanity-check the basis before committing to the resulting stock level

### Metrics
- Rate of new-SKU safety-stock calculations based on a single description-similarity-retrieved substitute versus a demand-driver-classified or category-level benchmark
- Divergence between a substitute SKU's demand-driver classification and the new SKU's eventual realized classification, once history accumulates
- Stockout and overstock incidence among new SKUs with borrowed-variance safety stock, segmented by substitute-selection method

### Alerts
- A new SKU's safety stock is calculated from a substitute SKU whose demand-driver classification has not been confirmed to match → P2
- A new SKU's realized coefficient of variation, once sufficient history accumulates, diverges from its borrowed-variance substitute's by more than the defined tolerance → P2
- Borrowed-variance safety stock remains in effect past the defined minimum-history threshold without being replaced by a directly computed estimate → P3

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597)
