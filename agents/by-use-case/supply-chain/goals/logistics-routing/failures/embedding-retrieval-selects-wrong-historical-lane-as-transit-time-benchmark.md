# Embedding Retrieval Selects Wrong Historical Lane as Transit-Time Benchmark for New Route

## Issue: A Logistics-Routing Agent Estimating Transit Time for a New Origin-Destination Lane Retrieves the Most Similar Historical Lane via Embedding Similarity Over Route Descriptions, Selecting a Lane That Shares a Similar Region-Pair Label but Has a Materially Different Mode or Border-Crossing Profile, Producing a Transit-Time Estimate the Agent Then Commits to a Customer as an ETA

**Frequency**: Occasional

**Symptoms**
- A new lane's committed ETA is consistently missed by a margin consistent with a mode or border-crossing difference between the new lane and the historical lane its transit-time estimate was borrowed from
- Querying historical lanes by structured attributes (transport mode, number of border crossings, carrier type) rather than by route-description text similarity surfaces a different, more representative historical lane
- The retrieved benchmark lane's description text matches the new lane closely at the region-pair level (e.g., "Southeast Asia to Western Europe"), while differing in mode (ocean vs. air) or border-crossing count in ways the description text does not surface
- ETAs committed for new lanes whose transit-time benchmark was matched on structured mode and border-crossing attributes show a measurably lower miss rate than ETAs committed using a description-similarity-matched benchmark
- The mismatch concentrates on newly opened lanes connecting broad regions served by multiple route options (multiple ports, multiple possible transshipment points), where many structurally different historical lanes share similar region-pair description text

**Root Cause**
Selecting a transit-time benchmark via embedding similarity over route description text optimizes for similarity in how a lane is described, not for similarity in the structural attributes — transport mode, number of border crossings, transshipment points — that actually determine transit time. Two lanes can share near-identical region-pair description text while differing fundamentally in mode or routing structure, and description-embedding similarity has no mechanism to detect or penalize that divergence, since it never encodes the structural attributes the transit-time estimate actually depends on.

**Example**
```
A new ocean freight lane opens between a secondary Southeast Asian port and a Western European destination, with two intermediate border crossings
Logistics-routing agent retrieves the most similar historical lane via embedding similarity over route descriptions to benchmark expected transit time
Retrieved benchmark lane shares near-identical region-pair description text ("Southeast Asia to Western Europe") but is an air-freight lane with a single direct leg and no intermediate border crossings
Agent commits a customer ETA based on the air-freight lane's much shorter historical transit time
Actual ocean shipment, moving through two border crossings the benchmark lane never encountered, arrives well past the committed ETA, and the discrepancy is traced back to the mismatched benchmark lane's transport mode
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented systems are documented to exhibit a taxonomy of retrieval errors distinct from generation errors, including retrieving a topically similar but structurally unrepresentative record when similarity search is used without filtering for the attributes that determine the downstream estimate | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| LLMs applied to supply chain management are documented to require benchmarking against structurally matched historical operations data, rather than description-similarity retrieval alone, to maintain estimate reliability across route or lane variation | [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597) |
| Knowledge-oriented retrieval-augmented generation surveys identify retrieval over generic, recurring descriptive language as a distinct failure mode from retrieval over the rare, distinguishing structural attributes that determine a record's true behavior | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |

**Contributing Factors**
- Transit-time benchmark selection is implemented over route description text via embedding similarity rather than over structured mode, border-crossing-count, and transshipment-point fields
- No validation step confirms the retrieved benchmark lane's transport mode and routing structure match the new lane's actual structure before its transit time is borrowed
- Broad, multi-route regions are not flagged for mandatory structured-attribute matching before description-similarity retrieval is trusted as the basis for a customer-facing ETA commitment

---

## Mitigation Strategies

1. **Structured Mode and Routing-Structure Matching as Primary Path**: Require transit-time benchmark selection to match on transport mode, border-crossing count, and transshipment-point structure first, falling back to unscreened description similarity only when no structurally qualifying historical lane exists
2. **Multi-Lane Ensemble Rather Than Single-Lane Basis**: Require new-lane transit-time estimates to be built from an ensemble of multiple structurally matched historical lanes rather than the single most textually similar lane, reducing sensitivity to any one mismatched benchmark
3. **Confidence-Discounted ETA for Structurally Unconfirmed Benchmarks**: When no structurally confirmed benchmark exists and the estimate falls back to description-similarity retrieval, widen the committed ETA window to reflect the reduced confidence, rather than committing a point estimate
4. **Surface Benchmark Basis in ETA Commitment**: Require any customer-facing ETA commitment based on a single retrieved historical lane to record which lane it was based on and whether the match was structurally confirmed, so discrepancies can be traced back to the benchmark choice

### Metrics
- Rate of new-lane ETA commitments based on a single description-similarity-matched benchmark versus a structurally matched benchmark or ensemble
- ETA miss rate, segmented by structurally matched benchmark vs. description-similarity-matched benchmark
- Mode or border-crossing-count divergence between a benchmark lane and the new lane it was used to estimate, for lanes flagged after an ETA miss

### Alerts
- An ETA is committed for a new lane using a benchmark lane whose transport mode does not match the new lane's actual mode → P2
- ETA miss rate for description-similarity-matched-benchmark lanes exceeds the miss rate for structurally matched-benchmark lanes by more than the defined tolerance → P2
- A new lane connecting a broad, multi-route region has its ETA committed with no structural-attribute match attempted → P3

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
