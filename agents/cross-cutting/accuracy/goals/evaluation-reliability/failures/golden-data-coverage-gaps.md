# Golden Data Coverage Gaps

## Issue: Golden Dataset Missing Critical Scenarios or Edge Cases

**Frequency**: Very Common

**Symptoms**
- Agent passes all tests but fails on common real queries
- Edge cases discovered only in production
- Golden set skewed toward easy cases
- Important user segments not represented
- New features untested in golden set

**Root Cause**
Golden datasets are created from available examples, often biased toward common, clean, easy cases. Edge cases, adversarial inputs, minority user segments, and unusual scenarios are underrepresented or missing entirely. The agent appears accurate on evaluation but fails when encountering the long tail of real-world queries.

**Example**
```
Scenario: Medical triage chatbot evaluation

Golden dataset composition (1000 cases):
  - Common symptoms: 800 (80%)
  - Moderate complexity: 150 (15%)
  - Rare conditions: 40 (4%)
  - Emergency scenarios: 10 (1%)
  - Non-English speakers: 0 (0%)
  - Elderly with multiple conditions: 5 (0.5%)

Evaluation result: 96% accuracy

Production query distribution:
  - Common symptoms: 60%
  - Moderate complexity: 20%
  - Rare conditions: 8%
  - Emergency scenarios: 5%  ← 5x underrepresented
  - Non-English speakers: 12%  ← Not tested at all
  - Elderly with multiple: 15%  ← 30x underrepresented

Production accuracy by segment:
  - Common symptoms: 97%
  - Moderate complexity: 89%
  - Rare conditions: 72%
  - Emergency scenarios: 58%  ← Critical failures
  - Non-English speakers: 41%  ← Never evaluated
  - Elderly with multiple: 52%  ← Dangerous gaps

Impact:
  - 3 missed emergency escalations
  - Patient safety incidents
  - 12% of users completely unserved by evaluation
```

**Key Statistics**
From Coverage Research (2026):
- Average golden set covers <60% of production query types
- Edge cases: 2-5% of golden data, 15-25% of production failures
- 40% of critical failures from untested scenarios
- Minority segments missing in 70% of golden datasets
- New features have <50% golden data coverage at launch

**Coverage Gap Types**
| Gap Type | Example | Risk |
|----------|---------|------|
| Edge cases | Unusual inputs | Silent failures |
| Demographics | Age, language, region | Bias, exclusion |
| Complexity | Multi-step, ambiguous | Quality drop |
| Adversarial | Malformed, tricky inputs | Security, errors |
| Temporal | Seasonal, time-sensitive | Wrong answers |
| New features | Recently added capabilities | Untested paths |

**Contributing Factors**
- Golden data from convenience samples
- Bias toward "clean" examples
- Expensive to create edge case data
- Unknown unknowns (can't test what you don't know)
- Production distribution not analyzed
- New features added without test data

**Mitigation Strategies**
1. **Coverage analysis**: Map golden data to production distribution
2. **Stratified sampling**: Ensure representation across segments
3. **Edge case mining**: Deliberately create challenging cases
4. **Production sampling**: Add real queries to golden set
5. **Adversarial testing**: Include deliberately difficult inputs
6. **Coverage metrics**: Track and require minimum coverage

**Detection**
- Compare golden vs. production query distributions
- Track accuracy by query segment
- Monitor failures from underrepresented categories
- Audit golden set demographics
- Alert on coverage threshold violations

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Coverage limitations
- [Databricks: OfficeQA Benchmark](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - Enterprise coverage gaps
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Test coverage
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Edge case failures
- [CMARix: RAG & AI Trust Statistics](https://www.cmarix.com/blog/rag-ai-statistics/) - Coverage metrics
