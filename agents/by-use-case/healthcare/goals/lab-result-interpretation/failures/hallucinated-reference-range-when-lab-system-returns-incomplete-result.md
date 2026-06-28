# Hallucinated Reference Range When Lab System Returns Incomplete Result

## Issue: When the Lab-System Integration Returns a Result Value Without the Accompanying Reference Range or Units (a Malformed or Partial API Response), an Agent Interpreting the Result States a Specific Reference Range as If Retrieved From the Lab System, Fabricated to Complete a Plausible-Sounding Interpretation Rather Than Reflecting Actual Data, Potentially Mischaracterizing an Abnormal Result as Normal or Vice Versa

**Frequency**: Occasional

**Symptoms**
- The interpretation narrative states a specific reference range for a lab value that does not match the reference range actually on file in the lab system for that test, assay, and patient demographic when independently checked
- The lab-system integration call immediately preceding the interpretation, visible in the agent's trace, shows a partial response missing the reference-range or units field, rather than a complete result payload
- Re-running the same interpretation after the lab-system call returns a complete response produces an interpretation citing the genuinely correct reference range, isolating the fabrication to the prior incomplete response
- The fabricated reference range is a plausible, commonly cited textbook range for the test in question, making it indistinguishable from a real lab-system value without independently checking the actual result payload
- A result is characterized as within normal limits in the generated interpretation when the lab's actual assay-specific reference range (which can differ from textbook defaults due to assay method or patient demographic adjustments) would have flagged it as abnormal, or vice versa

**Root Cause**
When the lab-system integration returns an incomplete payload missing the reference-range field, the model can complete its expected interpretation by generating a plausible, commonly cited reference range for that test rather than explicitly reporting that the reference range was not returned and the result cannot be characterized as normal or abnormal without it. Lab reference ranges vary by assay method, instrument, and patient demographic in ways that a generic textbook range does not capture, so a fabricated range -- even a reasonable-sounding one -- is not equivalent to the actual range that should govern interpretation for this specific result.

**Example**
```
Agent retrieves a potassium result for a patient via the lab-system integration to support an interpretation
Lab-system response returns the value (5.3) but, due to a partial API response, omits the reference-range field that would normally accompany it
Agent's interpretation nonetheless states: "Potassium 5.3 mEq/L, within normal range (3.5-5.0 mEq/L)," citing a generic textbook reference range as if it were the lab's own reported range
The lab's actual assay-specific reference range for this test, on this instrument, is 3.5-5.1 mEq/L; even using the fabricated generic range, the agent's own arithmetic is inconsistent, since 5.3 exceeds even the cited 5.0 upper bound, yet the result is still characterized as normal
Clinician relying on the interpretation does not flag the result for follow-up, despite it being abnormal under both the fabricated and the actual reference range
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to fabricate plausible-sounding content to fill gaps left by incomplete tool or integration responses, a well-characterized hallucination subtype distinct from a reasoning error over complete data | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Multi-model assurance analysis shows large language models are highly vulnerable to fabricating clinically plausible but ungrounded content during clinical decision support, particularly when grounding data is incomplete | [Multi-model assurance analysis showing large language models are highly vulnerable to adversarial hallucination attacks during clinical decision support](https://www.nature.com/articles/s43856-025-01021-3) |
| Tiered oversight frameworks for healthcare AI agents specifically call for independent verification of any value used in a clinical interpretation against its actual source system record, rather than the model's own generated completion | [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482) |

**Contributing Factors**
- Interpretation-generation prompt implicitly rewards a complete, well-formatted interpretation, with no explicit instruction that reporting an incomplete lab-system response as a blocking gap is an acceptable output
- No automated step verifies that the reference range cited in a generated interpretation matches the reference range actually present in the lab-system response payload for that specific result
- Lab-system integration failures (partial payloads missing reference-range or units fields) are not surfaced prominently in the agent's output, so a clinician has no visible signal that the underlying data was incomplete

---

## Mitigation Strategies

1. **Mandatory Reference-Range Resolution Check**: Before an interpretation is finalized, automatically verify that the cited reference range matches the value actually present in the lab-system response payload, flagging any mismatch or absence for review
2. **Hard Stop on Incomplete Lab Response**: Require the agent to explicitly report a lab-system response missing the reference-range or units field as a blocking gap, rather than proceeding to generate an interpretation as if the response had been complete
3. **Internal Arithmetic Consistency Check**: Automatically verify that the interpretation's stated normal/abnormal characterization is arithmetically consistent with the cited reference range and value, catching cases where a fabricated range and a flawed characterization both appear together
4. **Retry-Before-Interpret Policy**: Require an incomplete lab-system response to be retried at least once, and escalated to a human if it continues to return incomplete, before the agent proceeds to interpretation generation

### Metrics
- Rate of finalized interpretations whose cited reference range does not match the value present in the logged lab-system response payload
- Number of interpretations proceeding to generation despite a logged incomplete lab-system response
- Rate of internal arithmetic inconsistencies (cited value falls outside the cited range but is characterized as normal, or vice versa) caught before clinician review

### Alerts
- A clinical interpretation is finalized with a reference range that fails resolution check against the logged lab-system response → P1
- An interpretation is generated despite a logged incomplete lab-system response with no retry → P1
- Reference-range fabrication rate across lab interpretations exceeds baseline for two consecutive reporting periods → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Multi-model assurance analysis showing large language models are highly vulnerable to adversarial hallucination attacks during clinical decision support](https://www.nature.com/articles/s43856-025-01021-3)
- [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482)
