# Spurious Causal Narrative from Unrelated News Event in Risk-Score Justification

## Issue: A Supplier-Risk Agent Generating a Free-Text Justification for an Elevated Risk Score Constructs a Plausible-Sounding Causal Narrative Linking a Co-Occurring but Unrelated News Event -- a Regional News Item That Mentions the Supplier's Country or Region Without Mentioning the Supplier Itself -- to the Score, and Risk Analysts Adopt the Fabricated Causal Story as the Real Driver Rather Than Recognizing It as the Model's Own Rationalization

**Frequency**: Occasional

**Symptoms**
- Risk-score justification cites a specific news event (a regional labor dispute, a regulatory announcement, a regional weather event) as the reason for an elevated score, but the cited event makes no mention of the supplier, its facility, or its direct customers
- The actual drivers of the score change, when the underlying risk-model features are inspected directly, are unrelated to the cited news event (e.g., a payment-delay signal or a delivery-performance metric that moved independently)
- Re-generating the justification with the news event explicitly excluded from the agent's available context produces a justification citing the real, feature-based drivers instead, isolating the news event as a spurious narrative rather than a genuine contributing factor
- Risk analysts who read only the justification text, without independently checking the underlying risk-model features, begin tracking the cited news event as if it were a validated leading indicator for this supplier
- A supplier-risk mitigation plan is built around monitoring the wrong signal (the unrelated news event) while the actual driver of the elevated score goes unaddressed

**Root Cause**
When asked to generate a human-readable justification for a risk score, the model tends to construct a coherent causal narrative connecting available contextual information -- including a news event that happens to co-occur in time and geography with the score change -- even when the underlying risk-scoring features have no actual dependency on that event. The model's justification-generation step is not the same computation as the risk-scoring step itself, so a fluent, plausible-sounding story can be generated that has no grounding in the features that actually drove the score, and nothing in the default workflow forces the justification to cite only verified, feature-level drivers.

**Example**
```
Supplier-risk agent's underlying model flags Supplier X with an elevated risk score, driven by a feature-level signal: three consecutive late payment-confirmation cycles to its own upstream raw-material vendor, surfaced through standard financial-data monitoring
Justification-generation step, given the score and general regional context, produces: "Risk elevation is consistent with the recent labor unrest reported in [Supplier X's region], which likely disrupted operations"
The cited labor unrest report does not mention Supplier X, its facility, or its direct supply chain, and the actual score driver (payment-confirmation delays) is unrelated to it
Risk analysts adopt the labor-unrest narrative, begin monitoring regional labor-news feeds for this supplier, and do not investigate or escalate the actual payment-delay signal that drove the score
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to construct plausible-sounding causal narratives connecting merely co-occurring elements of available context, a hallucination subtype distinct from a factual error in the underlying analysis | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Business-scenario evaluation of LLM agents finds that free-text justifications generated alongside a structured decision frequently diverge from the actual decision-driving features, particularly when contextual information unrelated to the decision is available to the model | [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878) |
| Calibration research in tool-using and decision-support agents notes that the fluency and confidence of a generated explanation is not correlated with its grounding in the actual decision-relevant evidence | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |

**Contributing Factors**
- Justification-generation step has access to broad contextual information (regional news) that is not itself an input feature to the underlying risk-scoring model, creating an opportunity to narrate a connection that does not exist
- No automated check verifies that every causal claim in a generated justification corresponds to an actual feature used by the risk-scoring model
- Risk analysts typically consume the justification text directly rather than independently inspecting the underlying model's feature attribution for each score

---

## Mitigation Strategies

1. **Feature-Grounded Justification Requirement**: Require every causal claim in a generated risk-score justification to cite a specific, named feature from the underlying risk model's actual feature attribution, rejecting any justification that cites contextual information not used as a model input
2. **Automated Justification-to-Feature Consistency Check**: Before a justification is presented to analysts, automatically verify that the cited driver(s) match the top feature-attribution results from the scoring model, flagging any justification that cites an unattributed factor
3. **Separate Display of Feature Attribution and Narrative Context**: Present analysts with the model's actual feature attribution as a structured, separate element from any narrative context, rather than blending them into a single prose justification that obscures which is which
4. **Analyst Training on Narrative-vs-Attribution Distinction**: Train risk analysts to treat any narrative justification as a hypothesis requiring confirmation against feature attribution, not as a validated causal finding on its own

### Metrics
- Rate of generated justifications citing a causal factor not present in the underlying model's feature attribution
- Number of supplier-risk mitigation plans built around a justification-cited factor versus the model's actual top-attributed feature
- Analyst override or correction rate when justification-to-feature consistency checks flag a mismatch

### Alerts
- A risk-score justification is presented to analysts citing a factor not in the model's feature attribution, with no consistency-check flag resolved → P2
- A supplier-risk mitigation plan is built citing a justification factor that fails the feature-grounding check → P2
- Justification-to-feature mismatch rate across supplier-risk scores exceeds baseline for two consecutive reporting periods → P3

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
