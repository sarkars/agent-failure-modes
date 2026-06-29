# Retention Agent Fabricates Manager-Conversation Detail Not Present in Any Source Note

## Issue: A Retention-Prediction Agent Asked to Produce a Narrative Justification for a High-Attrition-Risk Flag Generates a Specific, Plausible-Sounding Detail About a Recent One-on-One Conversation Between the Employee and Their Manager (e.g., "The Employee Told Their Manager They Were Frustrated With the Lack of Promotion Timeline") That Does Not Appear in Any Manager Note, Survey Response, or HRIS Record the Agent Had Access To, and HR Acts on the Fabricated Detail as if It Were Documented Evidence

**Frequency**: Occasional

**Symptoms**
- The narrative justification attached to a risk flag cites a specific conversational detail, quote, or sentiment attributed to a named manager-employee interaction
- Searching the actual manager's 1:1 notes, engagement-survey responses, and HRIS comment history for the cited employee turns up no record of that conversation or sentiment ever being logged
- The fabricated detail is specific enough (a near-quote, a named timeframe) that HR treats it as documented fact and references it in a retention-intervention conversation with the employee, who is confused because they never said any such thing
- The underlying numeric risk score may be defensible from real signals (tenure, compensation percentile, manager-change history), but the narrative the agent generated to explain it invents supporting color not present in the input data
- Re-running the same prompt against the same real input data produces a differently worded but similarly fabricated conversational detail, indicating the narrative-generation step is not grounded in any specific retrievable source

**Example**
```
Retention-prediction agent computes a high-risk score for an employee from real signals:
18 months since last promotion, below-median recent performance-review percentile, two
manager changes in the past year
HR asks the agent to "explain the risk drivers in plain language for the manager 1:1"
Agent's narrative: "In their last 1:1, [employee] expressed frustration to their manager
about the lack of a clear promotion timeline and mentioned exploring external options"
No such 1:1 note, survey comment, or HRIS log entry exists for this employee -- the
real input data contained only the three structured signals above, no free-text manager
notes were retrieved or referenced
HR manager opens the retention conversation referencing "what you told your manager last
month," and the employee has no idea what is being referred to, damaging trust in the
conversation HR was trying to use to retain them
Audit of the agent's retrieved context confirms zero free-text source documents were
actually fetched for this employee at generation time
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey research on LLM-agent hallucination documents agents generating specific, plausible-sounding details -- including attributed quotes and event descriptions -- that are not grounded in any retrieved or provided source material | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Execution-provenance research argues that without a traceable link from a generated claim back to a specific source document, neither the agent nor a human reviewer can distinguish a grounded detail from a fabricated one before it is acted on | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Broader failure-mode research on LLM systems in production finds narrative or explanatory generation steps layered on top of a structured model output are a common point where unsupported detail is introduced, even when the underlying structured output itself is sound | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |

**Contributing Factors**
- The narrative-generation step is prompted to produce a "plain language explanation" without being constrained to cite only fields and documents actually present in the retrieved context
- No requirement that every specific factual claim in the narrative (a quote, a named event, a conversation) be traceable to a specific source document ID
- The structured risk score and the free-text narrative are generated in the same pass, so a confident, fluent tone on the real structured part carries over to the fabricated narrative part with no visible distinction
- HR reviewers treat agent-generated narratives as a summary of real records rather than as a generated text that requires independent source verification before being repeated to the employee

---

## Mitigation Strategies

1. **Citation-Required Narrative Generation**: Require every specific factual claim in a risk-flag narrative (quotes, named conversations, dated events) to carry an inline citation to an actual source document ID; strip or block any claim that cannot be cited
2. **Source-Empty Guardrail**: If no free-text manager notes or survey comments were retrieved for an employee, explicitly instruct the agent to state that the explanation is based solely on structured signals (tenure, comp, review percentile) rather than inventing qualitative color
3. **Pre-Conversation Verification Step**: Require an HR reviewer to confirm each cited source document exists and says what the narrative claims before using the narrative in an employee-facing retention conversation
4. **Separate Structured and Narrative Confidence**: Surface the structured risk score and the free-text narrative with independent confidence/grounding indicators so a fluent narrative cannot borrow credibility from a well-grounded score

### Metrics
- Rate of risk-flag narratives containing a specific quote, conversation, or named event with no matching source document
- Number of retention conversations where the employee disputes a detail the agent's narrative attributed to them
- Percentage of narratives generated with zero free-text source documents actually retrieved

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Uncitable factual claim in narrative | Narrative contains a quote or specific event with no matching source document ID | P1 | Block narrative from HR-facing use; regenerate with citation constraint |
| Zero-source narrative generation | Narrative generated for an employee with no free-text source documents retrieved | P2 | Restrict narrative to structured-signal language only |
| Employee disputes cited detail | Employee states in a retention conversation that a cited detail is inaccurate or unfamiliar | P1 | Audit source-citation pipeline for that flag; issue correction |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
