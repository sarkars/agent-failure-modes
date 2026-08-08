# Happy-Path-Only Evals

## Issue: Edge cases are missing from tests.

**Frequency**: Occasional

**Symptoms**
- Failures cluster on unusual cases.
- Eval suite reports 98%+ pass rate release after release, yet production incident reports repeatedly involve empty inputs, malformed fields, or rare locales never exercised in testing.
- Engineers are surprised in postmortems that a specific input shape "was never considered," despite it recurring in production for months.

**Root Cause**
The gap stems from who writes the tests and under what pressure: the same engineers who built the happy-path flow author the eval cases, so the suite only reflects the inputs they already imagined as "normal," and without an explicit taxonomy of edge-case categories (boundary values, malformed input, rare locales) there's no checklist forcing broader coverage. Launch timelines further bias effort toward a small set of demo-friendly passing cases rather than fuzzing or long-tail mining, and because production logs are never mined for the rare-but-real input shapes users actually send, edge cases discovered in the wild never make their way back into the suite that's supposed to catch them next time.

**Example**
```
A booking agent's eval suite consists of 40 well-formed requests: valid dates, standard
party sizes, common cities. It passes at 99%. In production, a user submits a request
with a past-dated check-in ("book me a room for yesterday") -- a case never represented
in the suite. The agent confirms a nonsensical booking instead of rejecting or clarifying
it. The eval suite continues to report near-perfect scores because it never contained a
single boundary-date or malformed-input case.
```

**Contributing Factors**
- Eval cases are hand-authored by the same engineers who built the happy-path flow, so they only imagine inputs that fit their mental model of "normal" usage.
- No taxonomy of edge-case categories exists, so there's no checklist forcing coverage of boundary values, malformed input, or rare locales.
- Time pressure at launch favors writing a small set of demo-friendly passing cases over investing in fuzzing or long-tail mining.
- Production logs are not mined for rare-but-real input shapes, so edge cases discovered by users never make it back into the eval suite.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Boundary date rejection | "Book me a room for yesterday" (past check-in date) | Agent rejects or asks for clarification | Agent confirms an invalid/nonsensical booking |
| Malformed field handling | Request with empty party-size field and duplicated date key | Agent surfaces a validation error, does not guess | Agent silently fabricates a default value and proceeds |
| Long-tail locale/format | Query in a low-frequency locale with non-ASCII characters and unusual date format | Agent parses correctly or escalates | Agent misparses input without flagging uncertainty |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| edge_case_category_coverage_pct | 100% of taxonomy categories have >= 5 cases | Audit eval suite against the edge-case taxonomy checklist |
| edge_case_pass_rate_pct | Within 5 points of core happy-path pass rate | Score eval runs broken out by edge-case category vs. core category |
| long_tail_case_ratio_pct | >= 20% of eval cases from bottom-quartile-frequency production inputs | Cross-reference eval case inputs against production frequency distribution |

---

## Mitigation Strategies

### Prevention
1. **Edge-Case Taxonomy-Driven Test Generation**: Build an explicit taxonomy of edge-case categories (empty/null input, boundary values, malformed format, unsupported locale, extreme length, concurrent/rate-limited calls, partial tool failure) and require minimum test coverage per category before an eval suite is considered complete.
2. **Boundary Value & Mutation-Based Fuzzing**: Programmatically mutate existing happy-path cases (truncate, duplicate fields, swap types, inject unicode/emoji, remove required fields) to generate edge variants automatically, rather than relying solely on hand-authored cases.
3. **Production Long-Tail Mining**: Mine production logs for the bottom percentile by frequency (rare intents, unusual formatting, atypical session lengths) and require these long-tail cases be represented in the eval suite at a minimum ratio (e.g., 20% of cases from the bottom quartile of frequency).

### Detection & Response
1. **Per-Category Pass Rate Breakdown**: Score eval runs broken out by edge-case category, not just aggregate pass rate; flag categories with pass rate below the aggregate by more than a set margin.
2. **Production Failure Clustering Analysis**: Cluster production failures weekly (embedding or rule-based) and cross-reference each cluster against existing eval categories; clusters with no matching eval category are flagged as coverage gaps.
3. **Coverage Gap Backfill Trigger**: Any production failure cluster identified as uncovered automatically opens a ticket to add representative cases to the eval suite within a fixed SLA.

### Architecture Patterns
1. **Layered Eval Suite (Core + Edge + Adversarial)**: The eval pipeline runs three tiers — core happy-path, edge-case taxonomy, and adversarial/red-team — reporting pass rates separately so edge-case regressions can't hide behind a strong core score.
2. **Fuzzing Harness as CI Stage**: A mutation-fuzzing tool runs as a required CI stage that generates N edge variants per PR touching the agent's prompt/logic and fails the build if any variant produces an unhandled exception or obviously wrong output.
3. **Failure Cluster-to-Eval-Case Pipeline**: An automated service ingests production failure clusters, deduplicates against existing eval cases, and stages new edge-case candidates for reviewer approval.

### Metrics
1. **edge_case_category_coverage_pct**: Target: 100% of taxonomy categories have >= 5 cases; Alert threshold: < 80%
2. **edge_case_pass_rate_pct**: Target: within 5 points of core happy-path pass rate; Alert threshold: gap > 15 points
3. **uncovered_failure_cluster_count**: Target: 0 open past SLA; Alert threshold: > 3 open past 2 weeks
4. **long_tail_case_ratio_pct**: Target: >= 20% of eval cases from bottom-quartile-frequency production inputs; Alert threshold: < 10%

### Alerts
1. **Edge-Case Pass Rate Collapse** (P1 - Critical): Condition - any edge-case category pass rate falls more than 20 points below core pass rate. Action: Block release, require root-cause fix or explicit risk acceptance from eng lead.
2. **Recurring Uncovered Failure Cluster** (P2 - Warning): Condition - the same production failure cluster shape recurs without a matching eval case for 2+ weeks. Action: Escalate to eval owner for mandatory case addition.
3. **Taxonomy Coverage Drift** (P3 - Info): Condition - edge-case category coverage drops below 80% after a suite refactor. Action: Notify test owner to backfill missing categories.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| edge_case_pass_rate_pct | Gap > 15 points below core happy-path pass rate |
| uncovered_failure_cluster_count | > 3 open past 2 weeks |
| edge_case_category_coverage_pct | < 80% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Edge-Case Pass Rate Collapse | Any edge-case category pass rate falls more than 20 points below core pass rate | High |
| Recurring Uncovered Failure Cluster | Same production failure cluster shape recurs without a matching eval case for 2+ weeks | Medium |
| Taxonomy Coverage Drift | Edge-case category coverage drops below 80% after a suite refactor | Medium |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
