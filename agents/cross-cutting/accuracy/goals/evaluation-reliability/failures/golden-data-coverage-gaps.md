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

---

## Test Scenario & Reproduction

### Scenario Setup
- A medical triage chatbot golden dataset composed predominantly of common-symptom cases (80%), with emergency scenarios (1%), non-English speakers (0%), and elderly-with-multiple-conditions cases (0.5%) heavily underrepresented or absent
- No production-distribution-mapped sampling or mandatory minimum coverage gate applied when the golden set was built
- Production traffic containing a materially different segment mix (5% emergency, 12% non-English, 15% elderly-multi-condition)

### Trigger Mechanism
1. Run the standard golden-set evaluation and record the aggregate accuracy
2. Segment production traffic by the same categories used in the golden set
3. Draw a labeled sample of production queries from the underrepresented segments (emergency, non-English, elderly-multi-condition)
4. Run the agent against that labeled underrepresented-segment sample and score accuracy per segment

**Example Reproduction Steps:**
```
1. Run golden-set eval (1000 cases: 80% common, 15% moderate, 4% rare, 1% emergency, 0% non-English, 0.5% elderly-multi) and record aggregate accuracy (96%)
2. Pull a labeled production sample stratified by segment: common 60%, moderate 20%, rare 8%, emergency 5%, non-English 12%, elderly-multi 15%
3. Score agent accuracy specifically on the emergency-scenario subsample
4. Score agent accuracy specifically on the non-English-speaker subsample
5. Score agent accuracy specifically on the elderly-with-multiple-conditions subsample
6. Compare each segment's accuracy against the golden-set aggregate accuracy (96%)
```

### Expected Failure State
- Emergency-scenario accuracy in production is dramatically lower than the golden aggregate (e.g., ~58% vs. 96%), despite the golden set reporting high overall accuracy
- Non-English-speaker accuracy is very low (e.g., ~41%) because that segment had zero golden-set representation to catch it beforehand
- Elderly-with-multiple-conditions accuracy is similarly degraded (e.g., ~52%), a segment that was 30x underrepresented in golden data relative to production volume
- A correctly-behaving evaluation process would have surfaced these segment-level accuracy cliffs before deployment, since the golden set's composition would have been checked against production distribution rather than left as a convenience sample

---

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
