# LLM Paraphrase-Normalization Drops Legal-Entity Suffix During Canonicalization

## Issue: When an Agent Is Used to Canonicalize Free-Text Counterparty or Issuer Names Into a Standard Form, Its Generative Rewriting Silently Drops or Alters a Legal-Entity Suffix (Ltd, LLC, GmbH, Inc, N.V.) That Materially Changes Which Legal Entity — and Therefore Which Counterparty-Risk Profile — the Record Refers To

**Frequency**: Occasional

**Symptoms**
- A free-text counterparty or issuer name enters the pipeline with a specific legal-entity suffix, and the agent's canonicalized output for the same record either omits the suffix, substitutes a different one, or normalizes two distinct legal entities that share a base name but differ only by suffix into the same canonical form
- The two suffix variants (e.g., "Meridian Capital Ltd" vs. "Meridian Capital LLC") correspond to genuinely different legal entities in the counterparty master, with different jurisdictions, credit ratings, or netting agreements, not to a formatting inconsistency that should be collapsed
- Comparing the agent's canonicalized output against a deterministic string-normalization pipeline (case-folding, whitespace, punctuation only, no generative rewriting) on the same input shows the deterministic version preserves the suffix distinction while the agent's version does not
- Downstream counterparty-risk aggregation or netting calculations combine exposure from what are actually two separate legal entities under a single canonical name, understating single-entity concentration or misapplying a netting agreement that only covers one of the two entities
- The drop is inconsistent across otherwise-identical inputs — the same base name with the same suffix is canonicalized correctly in some records and incorrectly in others, consistent with a generative model occasionally "smoothing over" what it treats as a minor formatting variation rather than a systematic, ruleset-driven omission

**Root Cause**
Canonicalization implemented as an LLM paraphrase or rewrite task ("normalize this name to standard form") treats the legal-entity suffix as one more stylistic element of the name to be smoothed toward a common pattern, the same way it might standardize capitalization or abbreviate "Corporation" to "Corp." A deterministic normalization pipeline treats the suffix as a distinct, semantically load-bearing token governed by an explicit rule (preserve exactly, map only within a controlled equivalence set). Because a generative rewrite has no structural guarantee of token preservation, and because entity suffixes are exactly the kind of low-salience-looking variation a paraphrase model is trained to smooth over for readability, the suffix can be dropped or altered without the model "intending" any semantic change — the failure is a byproduct of using open-ended generation for a task that requires exact, rule-governed token handling.

**Example**
```
Input counterparty names from two separate trade confirmations:
  "Meridian Capital Partners Ltd"   (UK entity, jurisdiction: England & Wales)
  "Meridian Capital Partners LLC"   (US entity, jurisdiction: Delaware)

Agent canonicalization output for both:
  "Meridian Capital Partners"

Reality: these are two distinct legal entities in the counterparty master 
with different jurisdictions, different credit terms, and no shared netting 
agreement. The canonicalized form is now ambiguous between them.

Counterparty exposure aggregation, keyed on the canonical name, combines 
both entities' exposure into a single concentration figure and applies the 
UK entity's netting agreement to trades that were actually booked against 
the separate US entity.
```

**Key Statistics**
| Finding | Context |
|---|---|
| Financial statement verification benchmarks for LLMs highlight that generative normalization or rewriting steps introduce calibration and validity risks distinct from deterministic parsing, particularly where token-level precision (exact identifiers, entity distinctions) is required rather than semantic approximation | [FinVerBench: Benchmark Validity and Calibration in Large Language Model Financial Statement Verification](https://arxiv.org/pdf/2605.29586) |
| Taxonomies of retrieval-augmented and generative-pipeline errors classify information-loss during generative rewriting as a distinct error type from retrieval failure, occurring even when the correct source information was fully available to the model | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Two entities sharing a base name, different suffixes | "Meridian Capital Partners Ltd" and "Meridian Capital Partners LLC" as separate inputs | Canonicalized forms remain distinct and separately traceable to their legal entities | Both inputs canonicalize to the same suffix-free form |
| Genuine formatting variant, same entity | "Meridian Capital Partners, Ltd." and "Meridian Capital Partners Ltd" (same entity, punctuation variant) | Canonicalize to the same form | N/A (control case, should always pass) |
| Suffix substitution | Input suffix "GmbH" canonicalized output shows a different suffix (e.g., "AG") | Output preserves the original suffix exactly | Output suffix differs from input suffix without a defined equivalence rule |
| Rule-governed canonicalization | Same two-entity case, processed through a deterministic suffix-preserving normalizer | Canonical forms remain distinct | N/A (mitigation validation case) |

### Evaluation Dataset
- **Source**: Counterparty/issuer name pairs drawn from the counterparty master, including known suffix-differentiated entity pairs and known genuine formatting-variant pairs (same entity, different punctuation/capitalization only)
- **Size**: 100+ name pairs, stratified by whether the pair represents distinct legal entities or a genuine formatting variant of one entity
- **Key variations**: common-suffix-family entities (Ltd/LLC/Inc pairs sharing a base name) vs. entities distinguished by jurisdiction-specific suffixes (GmbH/AG, S.A./S.p.A.)

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Entity-distinction preservation rate | 100% | % of known distinct-entity suffix pairs that canonicalize to distinguishable forms |
| Formatting-variant consolidation rate | 100% | % of known same-entity formatting variants that canonicalize to the same form |
| Counterparty exposure aggregation accuracy | 100% match to entity-level ground truth | % of aggregated exposure figures that correctly separate distinct legal entities sharing a base name |

### Automated Checks
```python
def check_for_failure(input_name_a, input_name_b, canonical_a, canonical_b, same_entity_ground_truth):
    """Flag canonicalization that collapses two distinct legal entities
    into the same canonical form, or fails to collapse genuine variants
    of the same entity.
    """
    canonicalized_as_same = (canonical_a == canonical_b)

    incorrectly_merged = canonicalized_as_same and not same_entity_ground_truth
    incorrectly_split = (not canonicalized_as_same) and same_entity_ground_truth

    return {
        "canonicalized_as_same": canonicalized_as_same,
        "ground_truth_same_entity": same_entity_ground_truth,
        "incorrectly_merged_distinct_entities": incorrectly_merged,
        "incorrectly_split_same_entity": incorrectly_split,
    }
```

---

## Mitigation Strategies

### Prevention
1. **Deterministic Suffix Preservation Rule**: Canonicalize legal-entity suffixes through an explicit, deterministic equivalence table (e.g., "Ltd." and "Limited" map to a single canonical suffix token; "Ltd" and "LLC" never map to each other), rather than generative paraphrase.
2. **Entity-Master-Anchored Canonicalization**: Resolve free-text names against the counterparty/issuer master by exact or controlled-fuzzy match on the full name including suffix, rather than generating a canonical form independent of the master.
3. **Suffix-Change Flagging in Any Generative Step**: If a generative rewrite step is used elsewhere in the pipeline (e.g., for display formatting), require it to flag or refuse any transformation that changes the legal-entity suffix token, rather than silently smoothing it.

### Detection & Response
1. **Suffix-Diff Audit on Every Canonicalization**: Automatically compare the suffix token in the input against the suffix token in the canonicalized output; flag any case where they differ outside the defined equivalence table.
2. **Counterparty Concentration Anomaly Detection**: Monitor for counterparty concentration figures that shift materially when canonicalization logic changes, as a signal that entity distinctions may be getting collapsed.
3. **Netting Agreement Applicability Cross-Check**: Before applying a netting agreement keyed on canonical name, verify the underlying trades' original (pre-canonicalization) legal-entity names all match the agreement's actual counterparty.

### Architecture Patterns
- **Rule-Table-Driven Canonicalization Service**: A deterministic, versioned equivalence-table service handles all suffix normalization; any generative component in the pipeline operates only on non-suffix portions of the name.
- **Entity-Master Resolution as the Canonicalization Step**: Canonical form is defined as "the matched entity master record's official name," resolved via exact/controlled-fuzzy lookup, not generated independently by a model.
- **Suffix-Preserving Audit Trail**: Every canonicalization event logs the original suffix token alongside the canonical suffix token, enabling systematic post-hoc auditing of suffix drift.

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| `suffix_drift_rate_percent` | % of canonicalized names whose suffix differs from the input outside the defined equivalence table | > 0% |
| `distinct_entity_collision_count` | Count of known-distinct legal entities canonicalizing to the same form | > 0 |
| `netting_misapplication_count_per_month` | Count of netting agreements applied across trades later found to involve genuinely distinct legal entities | > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Distinct Entities Collapsed to Same Canonical Form | Suffix-diff audit finds two known-distinct entities sharing a canonical form | P1 | Freeze affected netting/aggregation calculations; manual counterparty-risk review; correct canonicalization mapping |
| Suffix Drift Outside Equivalence Table | A canonicalization event changes the suffix token in a way not covered by the defined equivalence table | P2 | Review and correct the affected record; audit the canonicalization path for systematic drift |
| Concentration Figure Shift on Logic Change | Counterparty concentration metrics shift materially after a canonicalization logic update | P2 | Investigate whether the change altered entity-distinction handling |

---

## References
- [FinVerBench: Benchmark Validity and Calibration in Large Language Model Financial Statement Verification](https://arxiv.org/pdf/2605.29586)
- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
