# Embedding Retrieval Pulls Wrong Analog Supplier's Risk Profile by Name Similarity

## Issue: A Supplier-Risk Agent, Lacking Sufficient Direct History on a New or Thinly-Documented Supplier, Retrieves a Semantically or Lexically Similar Supplier's Risk Profile as an Analog to Inform Its Risk Score, but the Retrieved Analog Is Selected by Name or Description Similarity Rather Than the Structured Attributes (Industry Code, Ownership Structure, Geography, Tier) That Actually Determine Comparable Risk

**Frequency**: Occasional

**Symptoms**
- A new supplier's risk score and narrative closely track an existing, unrelated supplier whose name or business description is textually similar, despite the two suppliers operating in different industries, geographies, or ownership structures
- Inspecting the retrieval step shows the analog was selected by embedding or keyword similarity over free-text company descriptions, not by matching structured fields such as industry classification code, country of incorporation, or supplier tier
- Re-running the retrieval with the free-text description withheld and only structured attributes available surfaces a different, genuinely comparable analog supplier
- The gap is most visible for new suppliers whose name or product description happens to closely resemble an unrelated, larger, or more risk-flagged supplier already in the system, since those are the cases where lexical similarity diverges most from structural similarity
- Risk analysts who do not check the structured attributes behind a cited analog adopt an inappropriately elevated (or inappropriately low) risk score carried over from an unrelated supplier

**Root Cause**
Embedding- or keyword-based retrieval over free-text supplier descriptions ranks candidates by semantic or lexical proximity, which frequently diverges from the structured attributes -- industry code, ownership structure, country, supplier tier -- that actually determine whether two suppliers are genuinely comparable for risk-analog purposes. When the retrieval step is not constrained to filter or weight by these structured fields before ranking by textual similarity, a textually similar but structurally unrelated supplier can outrank a textually dissimilar but structurally appropriate one.

**Example**
```
New supplier "Meridian Polymer Solutions" has no direct risk history, so the supplier-risk agent retrieves an analog supplier's risk profile to inform its initial score
Retrieval, run over free-text company descriptions, surfaces "Meridian Specialty Coatings" as the closest match, based on shared name token and similar-sounding industry description
The two suppliers differ in industry classification code, country of incorporation, and ownership structure, with no genuine risk-relevant similarity beyond the shared name token
Agent's risk score for the new supplier inherits an elevated risk narrative from Meridian Specialty Coatings' history of past delivery disruptions, despite no structural basis for the comparison
Procurement deprioritizes the new supplier based on a risk score that has no grounding in its actual industry or geography risk profile
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Taxonomies of retrieval-augmented generation errors document embedding- and lexical-similarity retrieval selecting a structurally inappropriate match when surface-level textual similarity diverges from the structured attributes that determine genuine relevance | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Surveys of knowledge-oriented retrieval-augmented generation note that retrieval quality depends on aligning the similarity metric with the task's actual relevance criteria, and that free-text similarity alone is frequently insufficient when structured fields determine true comparability | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Research on agentic LLMs in the supply chain identifies supplier-comparability judgments as requiring structured attribute matching distinct from general semantic-similarity retrieval used elsewhere in agentic workflows | [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184) |

**Contributing Factors**
- Retrieval over supplier records ranks candidates primarily by free-text description similarity, with no mandatory pre-filter on structured fields such as industry code, country, ownership structure, or supplier tier
- No automated check compares the structured attributes of a retrieved analog supplier against the target supplier before the analog's risk profile is used to inform a score
- Risk analysts reviewing a new supplier's score typically see the analog's name and risk narrative without an explicit structured-attribute comparison alongside it

---

## Mitigation Strategies

1. **Structured-Attribute Pre-Filter Before Similarity Ranking**: Require retrieval of an analog supplier to first filter candidates by matching structured fields (industry code, country, ownership structure, tier) before ranking by free-text similarity within that filtered set
2. **Structured-Comparability Score Alongside Textual Similarity**: Present any retrieved analog supplier with an explicit structured-attribute comparability score, separate from textual similarity, so analysts can see whether the match is structurally grounded
3. **Mandatory Analog-Disclosure on Inherited Risk Scores**: Require any risk score informed by an analog supplier to disclose which specific attributes of the analog were used and whether they were structurally or only textually matched
4. **Analyst Review Gate for Low-Comparability Analogs**: Route any new-supplier risk score relying on an analog with low structured-attribute comparability to mandatory analyst review before the score is finalized

### Metrics
- Rate of analog-informed risk scores where the retrieved analog's structured attributes diverge from the target supplier's on industry code, country, or ownership structure
- Score delta between analog-informed risk scores and revised scores after structured-attribute-filtered re-retrieval
- Analyst override rate when a low-comparability analog flag is raised

### Alerts
- An analog-informed risk score is finalized with a retrieved analog that diverges from the target supplier on industry code or country, with no comparability flag resolved → P2
- A new-supplier risk score inherits a risk narrative from an analog later found to share only name-token similarity → P2
- Low-comparability analog rate across all new-supplier risk scores exceeds the defined threshold for a rolling window → P3

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184)
