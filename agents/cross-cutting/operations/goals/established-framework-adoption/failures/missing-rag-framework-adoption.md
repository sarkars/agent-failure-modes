# Missing RAG Framework Adoption

## Issue: Team builds a bespoke retrieval pipeline (custom chunking, custom vector store glue, custom prompt assembly) from scratch instead of adopting an established RAG framework, missing built-in chunking strategies, retrieval orchestration, and evaluation tooling that ship by default.

**Frequency**: Occasional

**Symptoms**
- Chunking, embedding orchestration, and retrieval-to-prompt assembly are all hand-rolled, with no framework providing tested defaults for any pipeline stage
- [Add more specific symptoms]

**Root Cause**
Team builds a bespoke retrieval pipeline from scratch instead of adopting an established RAG framework, missing built-in chunking strategies, retrieval orchestration, and evaluation tooling that ship by default.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- No evaluation of established RAG frameworks (document processing, embedding orchestration, retrieval, evaluation) was done before building each pipeline stage independently in-house
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **[Add Name]**: [Add description]

### Detection & Response
1. **[Add Name]**: [Add description]

### Architecture Patterns
1. **[Add Name]**: [Add description]

### Metrics
1. **[metric_name]**: Target: [Add]; Alert threshold: [Add]

### Alerts
1. **[Add Alert Name]** (P3 - Info): Condition - [Add]. Action: [Add].

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## Related Patterns

- [Chunk Boundary Failure](../../../../../by-capability/knowledge-retrieval/goals/retrieval/failures/chunk-boundary-failure.md) - a downstream symptom this pattern's missing framework (with tested chunking strategies) would help prevent
- [Low Recall Retrieval](../../../../../by-capability/knowledge-retrieval/goals/retrieval/failures/low-recall-retrieval.md) - a related downstream symptom; hybrid search and re-ranking (missing here) are exactly the kind of tested defaults an established framework provides out of the box

## References

- [15 Best Open-Source RAG Frameworks in 2026](https://www.firecrawl.dev/blog/best-open-source-rag-frameworks) - survey of mature RAG frameworks and their pipeline coverage
- [Best RAG Framework 2026: LangChain vs LlamaIndex vs DSPy](https://iternal.ai/blockify-rag-frameworks) - LangChain for rapid prototyping, LlamaIndex for document-centric RAG, Haystack for enterprise-grade production pipelines with built-in evaluation tooling
- [RAGAS evaluation](https://www.olostep.com/blog/open-source-rag-frameworks) - RAGAS provides objective context precision/recall/faithfulness/relevancy metrics and automatic test-dataset generation, usable across any RAG framework
