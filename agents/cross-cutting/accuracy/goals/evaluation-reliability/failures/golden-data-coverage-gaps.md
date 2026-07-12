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

## Mitigation Strategies

### Prevention
1. **Production-distribution-mapped stratified sampling**: Build the golden set by sampling proportional to (or oversampling relative to risk for) the actual production query distribution across segments, rather than convenience sampling, since the example's golden set had 0% non-English speakers against 12% of actual production volume. Trade-off: requires ongoing production distribution analysis and may require translating/localizing test cases.
2. **Deliberate edge-case and adversarial-case mining**: Allocate dedicated effort to constructing edge-case, adversarial, and rare-condition test cases rather than relying on convenience samples, since edge cases are only 2-5% of golden data but drive 15-25% of production failures per Key Statistics. Trade-off: edge-case creation is expensive and requires domain expertise to construct realistic scenarios.
3. **Mandatory minimum coverage gate for new features**: Require every new feature to ship with golden-set coverage meeting a minimum threshold before launch, rather than launching with under 50% coverage as is typical per Key Statistics. Trade-off: adds eval-authoring time to the feature timeline, creating pressure to skip this step under deadline pressure.

### Detection & Response
1. **Golden-vs-production distribution comparison**: Continuously compare golden-set composition against actual production query distribution across the same segment categories, surfacing gaps like the example's "Emergency scenarios: 1% golden vs 5% production" before they cause missed escalations.
2. **Segment-level accuracy monitoring with risk-weighted alerting**: Track production accuracy broken out by segment and weight alerting by the safety/business criticality of that segment, since the example's emergency-scenario accuracy (58%) and elderly-multi-condition accuracy (52%) were the most dangerous gaps despite low golden-set volume.
3. **Underrepresented-category failure clustering**: When analyzing production failures, specifically tag and count how many trace back to categories below a coverage threshold in the golden set, directly measuring the "40% of critical failures from untested scenarios" finding.

### Architecture Patterns
1. **Continuous production-sampling pipeline feeding golden set**: Architect an ongoing pipeline that samples real production queries (with privacy review) into the golden set on a schedule, weighted toward underrepresented and high-risk segments, rather than treating golden-set creation as a one-time convenience-sample exercise.
2. **Coverage-metrics dashboard gating releases**: Build a coverage-tracking system that computes golden-set representation against defined production segments and blocks deployment when any critical segment (e.g., emergency scenarios in a medical triage bot) falls below its required minimum.
3. **Adversarial/red-team test-case generation harness**: Maintain a dedicated adversarial test generation process as a permanent part of the eval architecture, separate from the "happy path" golden set, so adversarial coverage doesn't compete with or get diluted by common-case cases.

### Metrics
1. **golden_production_segment_coverage_ratio**: Target: each defined segment represented at >=80% of its production proportion; Alert when any segment falls below 30% of its production proportion
2. **edge_case_representation_rate**: Target: edge/rare cases >=10% of golden set; Alert when below 5%
3. **new_feature_launch_coverage_percent**: Target: >=80% golden coverage at feature launch; Alert if a feature launches below 50%
4. **critical_segment_accuracy_floor**: Target: no safety-critical segment (e.g., emergency scenarios) below 90% accuracy; Alert on any critical segment below floor

### Alerts
1. **Safety-Critical Segment Coverage Gap** (P1): Condition - a safety/business-critical segment (e.g., emergency scenarios, non-English speakers) falls below minimum golden-set representation. Action: block release, prioritize immediate test-case creation for that segment, escalate to eval owner.
2. **Segment Accuracy Cliff in Production** (P1): Condition - production accuracy for any tracked segment drops significantly below the golden-set-measured accuracy for that segment. Action: page on-call, investigate whether coverage gap or genuine regression, add representative cases to golden set.
3. **New Feature Launched Below Coverage Threshold** (P2): Condition - a feature reaches production with golden-set coverage below the required minimum. Action: flag to engineering leadership, schedule urgent backfill of test cases, increase production monitoring for that feature until coverage closes.

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Coverage limitations
- [Databricks: OfficeQA Benchmark](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - Enterprise coverage gaps
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Test coverage
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Edge case failures
- [CMARix: RAG & AI Trust Statistics](https://www.cmarix.com/blog/rag-ai-statistics/) - Coverage metrics
