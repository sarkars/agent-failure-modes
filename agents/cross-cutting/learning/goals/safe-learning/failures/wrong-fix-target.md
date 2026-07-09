# Wrong Fix Target

## Issue: System changes prompt when schema/retrieval/tool/data was root cause.

**Frequency**: Common

**Symptoms**
- Fix has no effect on reproduced failure.
- [Add more specific symptoms]

**Root Cause**
System changes prompt when schema/retrieval/tool/data was root cause.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
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
1. **Root-Cause-to-Fix-Layer Mapping Requirement**: The RCA must identify a specific layer (prompt, retrieval, schema, tool, data) as the confirmed root cause before a fix PR touching that layer can be authored; a fix proposing a prompt edit when the RCA points to a schema issue is blocked at review.
2. **Component-Level Fault Isolation Testing**: Before writing a fix, run the failing case through isolated component tests — substitute a known-good retrieval result, a corrected schema, a mocked tool response — to empirically confirm which layer actually produces the wrong output, rather than assuming based on where the symptom surfaced.
3. **Fix Proposal Review Against Evidence**: Reviewers check that the fix's target layer matches the documented root-cause evidence in the RCA, not just that the fix "sounds plausible" or that the reported symptom text superficially resembles a prompt-wording issue.

### Detection & Response
1. **Fix Verification Against Original Repro**: After a fix ships, immediately re-run the exact originally failing case; if it still fails, the fix targeted the wrong layer and is rejected rather than marked complete because a diff was merged.
2. **Fix-Type vs Root-Cause-Layer Mismatch Detection**: An automated linter compares the RCA's declared root-cause layer against the file paths actually touched in the fix diff, flagging mismatches (e.g., RCA says "retrieval" but diff only touches prompt template files) before merge.
3. **Recurrence Tracking by Layer**: Track whether incidents recur after fixes, segmented by which layer the fix targeted; layers with chronically low fix-efficacy indicate systematic misdiagnosis for that failure category (e.g., prompt fixes for what are actually schema issues).

### Architecture Patterns
1. **Layered Fault Isolation Harness**: Mockable boundaries between prompt, retrieval, schema, tool-call, and data layers that allow binary-search-style fault localization — swap one layer at a time for a known-good version until the failure disappears.
2. **Root-Cause-to-Diff Linter**: A CI check that parses RCA metadata and the PR's changed file paths, flagging any mismatch between the declared root-cause layer and the layer actually modified, blocking merge until resolved or explicitly overridden with justification.
3. **Fix Efficacy Dashboard**: Tracks post-fix repro pass/fail rate segmented by fix-target layer over time, surfacing which layers have chronically low fix-efficacy and thus warrant deeper isolation tooling or team retraining.

### Metrics
1. **fix_verification_pass_rate_percent**: Target: 100% (original repro passes after fix); Alert threshold: < 90%
2. **root_cause_fix_layer_match_rate_percent**: Target: 100%; Alert threshold: < 85%
3. **wrong_target_recurrence_count**: Target: 0 per month; Alert threshold: >= 2 in a rolling 30 days
4. **mean_fixes_per_incident**: Target: 1.0-1.2; Alert threshold: > 2 (proxy for repeated wrong-target attempts on the same incident)

### Alerts
1. **Fix Verification Failed** (P1 - Critical): Condition - post-fix re-run of the original failing case still fails. Action: Reject the fix, reopen RCA, mandate isolation testing before a new fix attempt is authored.
2. **Root-Cause-to-Diff Mismatch** (P2 - Warning): Condition - linter detects the fix diff doesn't touch the layer the RCA declared as root cause. Action: Block merge pending reviewer justification or corrected RCA.
3. **Repeated Wrong-Target Attempts** (P3 - Info): Condition - an incident accumulates 2+ fix attempts without resolution. Action: Escalate to senior engineer for deeper isolation testing, review whether the failure taxonomy needs a new category.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
