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

**Mitigation Strategies**
1. **Document classification first**: Classify before tool selection
2. **Region-level routing**: Different tools for different page regions
3. **Tool capability descriptions**: Clear tool descriptions help agent selection
4. **Fallback chains**: If primary tool fails, try alternatives

## References

- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - Tool selection challenges
- [Agentic Document Processing](https://www.llamaindex.ai/blog/agentic-document-processing) - Tool orchestration patterns
- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - Tool description importance
