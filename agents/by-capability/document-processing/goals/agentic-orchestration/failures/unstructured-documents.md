# Unstructured Documents

## Issue: Unstructured Document Confusion

**Frequency**: Common

**Symptoms**
- Agent cannot determine document structure
- Important information buried in narrative text
- No clear extraction schema applies

**Root Cause**
Agents work well on structured forms but struggle with free-form documents like correspondence, reports, or legal narratives where key information isn't in labeled fields.

**Example**
```
Input: Email chain discussing contract amendment

"...as we discussed on the call, we're okay with moving forward 
at the revised price of $475k instead of the original $500k, 
assuming delivery by end of Q2..."

Agent task: Extract contract value
Challenge: Value is in narrative, not labeled field
```

## Mitigation Strategies

### Prevention
1. **Question-answering reframing over field extraction**: Instead of prompting the agent to "extract the contract value" as if it were a labeled form field, frame the task as targeted questions against the document's actual content ("what price did the parties agree to, and where in the text is that stated?"), which better matches how the value actually appears in narrative text. Trade-off: Q&A framing produces answers that need a secondary step to normalize into structured fields for downstream systems.
2. **Named-entity and relation extraction as a pre-pass**: Run NER/relation-extraction models over unstructured sections first to surface candidate entities (amounts, dates, parties) and their relations before the agent attempts holistic extraction, giving it anchors rather than requiring it to parse narrative meaning unaided. Trade-off: general-purpose NER models may miss domain-specific relations (e.g., "revised price" vs. "original price") without fine-tuning.
3. **Hybrid rule-based anchoring + LLM interpretation**: Use deterministic pattern rules (currency regex, date patterns) to locate candidate values, then have the LLM interpret surrounding narrative context to determine which candidate is the operative one, combining the precision of rules with the contextual reasoning LLMs are better suited for. Trade-off: requires maintaining both a rule library and prompt logic, doubling maintenance surface versus a pure-LLM approach.

### Detection & Response
1. **No-schema-match flagging**: When the agent cannot map extracted content onto any expected field with reasonable confidence, explicitly flag "no clear structured value found" rather than silently returning a low-confidence guess or omitting the field without signal.
2. **Extraction confidence stratification by document structure**: Track extraction confidence separately for structured (form-like) vs. unstructured (narrative) documents/sections; a confidence gap between the two confirms unstructured content is the specific risk driver worth targeted mitigation.
3. **Sample-based narrative extraction audits**: Periodically have a human re-read narrative sections the agent processed and compare against the agent's extracted values, specifically checking for values that were present in the text but missed entirely (recall failures are harder to catch than wrong-value failures).

### Architecture Patterns
1. **Two-stage candidate-then-select extraction**: Stage one surfaces all candidate values/entities from the unstructured text (via NER, rules, or LLM scanning); stage two selects/reasons over which candidate is authoritative given surrounding context — decoupling "find possible values" from "pick the right one" makes each stage independently testable.
2. **Confidence-gated human review for narrative-sourced fields**: Route any field whose value was sourced from unstructured narrative text (as opposed to a labeled form field) through a lower confidence threshold for automatic acceptance, reflecting the genuinely higher difficulty of narrative extraction versus form-field reading.
3. **Domain-specific relation extraction fine-tuning**: For document types where unstructured extraction is a persistent bottleneck (e.g., correspondence, legal narratives), invest in fine-tuning or few-shot-calibrating extraction on labeled examples specific to that domain's narrative conventions rather than relying on generic extraction prompts.

### Metrics
1. **narrative_extraction_recall**: Target: > 90% of manually-confirmed-present values are also found by the agent; Alert if < 75%
2. **structured_vs_unstructured_confidence_gap**: Target: < 15 percentage points; Alert if > 30 points
3. **no_match_flag_rate**: Target: track as baseline per document type; Alert if it changes > 2x (signals either template drift or a genuine extraction capability regression)
4. **narrative_field_human_review_rate**: Target: < 20% of narrative-sourced fields require human review; Alert if > 40%

### Alerts
1. **Narrative Recall Drop** (P1): Condition - audit sampling shows narrative extraction recall below 75%. Action: Escalate document type to hybrid rule+LLM extraction path, flag recently processed documents of that type for re-review.
2. **Confidence Gap Widening** (P2): Condition - the structured/unstructured confidence gap exceeds 30 points for a document type. Action: Investigate whether narrative sections in that document type have shifted in style/format, requiring updated extraction prompts or rules.
3. **No-Match Flag Rate Anomaly** (P3): Condition - no-match flagging rate on a document type changes more than 2x from baseline. Action: Sample flagged documents to determine whether it's a genuine content change or a regression in extraction logic.

## References

- [AI Agents and Document Processing 2026](https://parsio.io/blog/ai-agents-document-processing-2026) - Unstructured document handling
- [Agentic Document Processing](https://www.llamaindex.ai/blog/agentic-document-processing) - Free-form extraction
- [Why OCR Alone Fails](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Narrative text challenges
