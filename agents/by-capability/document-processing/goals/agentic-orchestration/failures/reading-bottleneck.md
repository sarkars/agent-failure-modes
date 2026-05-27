# Document Reading Bottleneck

## Issue: Document Reading Bottleneck

**Frequency**: Very Common

**Symptoms**
- Agent reasons correctly but extracts wrong data
- Logical conclusions based on misread inputs
- Multi-step workflows fail despite correct reasoning chain

**Root Cause**
Agents reason well over clean text but fall apart when faced with real enterprise documents. The bottleneck isn't reasoning - it's reading.

**Example**
```
Task: "Extract the contract value and calculate 10% retention"

Agent reasoning: "I'll extract the contract value, then calculate 10%"
Extracted value: $100,000 (actual: $1,000,000 - misread due to poor scan)
Calculated retention: $10,000 (should be $100,000)

Result: Financially material error from reading failure, not reasoning failure
```

**Key Statistic**
Databricks' OfficeQA benchmark found frontier agents scored below 50% accuracy on real enterprise document reasoning tasks.

**Mitigation Strategies**
1. **Document preprocessing**: ai_parse_document delivered 16% average performance gain across agent frameworks
2. **Extraction verification**: Agent checks extractions before reasoning
3. **Confidence-aware reasoning**: Agent explicitly reasons about extraction uncertainty
4. **Human validation gates**: Critical values require human confirmation before agent proceeds

## References

- [Why Frontier Agents Can't Read Documents](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - OfficeQA benchmark, <50% accuracy
- [Agentic Document Processing](https://www.llamaindex.ai/blog/agentic-document-processing) - Reading as primary bottleneck
- [AI Agents and Document Processing 2026](https://parsio.io/blog/ai-agents-document-processing-2026) - Preprocessing importance
