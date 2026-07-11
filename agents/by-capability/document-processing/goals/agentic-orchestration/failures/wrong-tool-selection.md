# Wrong Tool Selection

## Issue: Wrong Tool Selection for Document Type

**Frequency**: Common

**Symptoms**
- Agent uses generic OCR on specialized document
- Handwriting processed with print-text tool
- Table extraction skipped on tabular documents

**Root Cause**
Tool selection depends on document understanding. Misclassification of document type or content leads to suboptimal tool choices.

**Example**
```
Input: Medical form with handwritten patient notes

Agent decision: Use standard OCR tool
Result: Handwritten sections return garbled text

Better: Detect handwritten regions, route to handwriting recognition tool
```

**Tool Orchestration Pattern**
A single agent can use OCR for printed text, handwriting recognition for annotations, table extraction for line items, and NLP for contract clause identification. The agent orchestrates these tools rather than running them in a fixed pipeline.

## Mitigation Strategies

### Prevention
1. **Mandatory classification-before-routing step**: Require a document (and page-region) classification step to run and produce a confident content-type label (printed text, handwriting, table, form field) before any extraction tool is invoked, rather than letting the agent guess a tool from a first impression of the whole document. Trade-off: adds a classification pass and its own failure mode (misclassification) as a new upstream dependency.
2. **Region-level tool routing over document-level routing**: Route different regions of the same page to different specialized tools (handwriting recognizer for annotations, table extractor for line items, standard OCR for printed body text) instead of picking one tool for the entire document, since real documents are frequently mixed-content. Trade-off: requires reliable region segmentation first, adding pipeline complexity.
3. **Precise, differentiated tool capability descriptions**: Write tool descriptions that clearly and narrowly state what content type each tool is built for and its known failure modes (e.g., "for machine-printed text only; do not use on handwritten content — will produce garbled output"), since vague tool descriptions are a documented driver of wrong-tool selection by agents choosing between similarly-named tools. Trade-off: requires disciplined maintenance of tool descriptions as new tools are added.

### Detection & Response
1. **Output-plausibility checks per tool type**: After a tool executes, run a lightweight plausibility check specific to that tool's expected output (e.g., OCR output on a handwriting-heavy region should trigger a garbled-text detector — high proportion of non-dictionary tokens) to catch wrong-tool-selection after the fact even when classification missed it upfront.
2. **Tool failure/low-confidence correlation with content type**: Track tool failure and low-confidence rates segmented by detected region content type; a specific tool consistently underperforming on a specific content type is a signal that routing logic — not the tool itself — needs fixing.
3. **Fallback chain triggering on quality signals, not just hard failure**: Trigger fallback to an alternative tool not only on hard tool errors but also when output quality signals (garbled text ratio, empty table extraction) suggest the tool was wrong for the content, even though the tool call itself "succeeded."

### Architecture Patterns
1. **Classify-then-route orchestration**: Architect the pipeline so classification is a distinct, independently-testable stage whose sole output is a routing decision, keeping tool-selection logic separate from and auditable apart from the extraction tools themselves.
2. **Fallback chain with escalating specialization**: Define an ordered fallback chain per content type (e.g., specialized handwriting model → general OCR with post-processing → human transcription) so a failed or low-confidence primary tool automatically escalates rather than silently returning poor output as final.
3. **Multi-tool ensemble with plausibility-based selection**: For ambiguous regions, run more than one candidate tool and select the output that best passes plausibility checks (dictionary match rate, expected format match) rather than committing to a single tool choice upfront when classification confidence is low.

### Metrics
1. **classification_confidence_before_routing**: Target: > 90% of regions classified with high confidence before tool routing; Alert if < 75%
2. **wrong_tool_output_plausibility_failure_rate**: Target: < 3% of tool outputs fail post-hoc plausibility checks; Alert if > 8%
3. **fallback_chain_invocation_rate**: Target: track as baseline per content type; Alert if it exceeds 2x baseline (signals primary tool/routing degradation)
4. **content_type_specific_tool_failure_rate**: Target: < 5% per content-type/tool pairing; Alert if any pairing exceeds 15%

### Alerts
1. **Plausibility Failure Spike** (P2): Condition - post-hoc plausibility failure rate for a tool exceeds 8% on a document source. Action: Sample failed outputs to confirm wrong-tool-selection vs. genuine content difficulty, adjust routing rules or tool descriptions accordingly.
2. **Low Classification Confidence Trend** (P2): Condition - region classification confidence before routing drops below 75% for a document type. Action: Review recent document samples for new mixed-content patterns the classifier wasn't trained/tuned for.
3. **Content-Type/Tool Failure Concentration** (P3): Condition - a specific tool's failure rate on a specific content type exceeds 15%. Action: Remove that tool from the routing table for that content type pending investigation, rely on fallback chain in the interim.

## References

- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - Tool selection challenges
- [Agentic Document Processing](https://www.llamaindex.ai/blog/agentic-document-processing) - Tool orchestration patterns
- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - Tool description importance
