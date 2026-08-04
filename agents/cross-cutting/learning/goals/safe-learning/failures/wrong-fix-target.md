# Wrong Fix Target

## Issue: System changes prompt when schema/retrieval/tool/data was root cause.

**Frequency**: Common

**Symptoms**
- Fix has no effect on reproduced failure.
- The RCA correctly identifies the root-cause layer (e.g., "retrieval index returns stale documents") but the merged fix diff only touches an unrelated layer (e.g., a prompt wording tweak), because it was easier or faster to change than the actual identified cause.
- The same incident accumulates multiple fix attempts across different PRs, each addressing a plausible-sounding but unconfirmed layer, before someone finally targets the layer the original RCA had already pinpointed.

**Root Cause**
System changes prompt when schema/retrieval/tool/data was root cause.

**Example**
```
An RCA for a booking agent conclusively determines, via isolation testing, that a tool integration is
returning cached availability data 20 minutes stale, causing the agent to confirm bookings for slots
that are already taken. The RCA document explicitly states "root cause: tool layer, stale cache TTL."
Under deadline pressure, the assigned engineer instead ships a prompt change telling the model to
"double-check availability before confirming," reasoning that it's a faster change to deploy than
touching the tool's caching config. The original failing case still reproduces identically after the
fix ships, because the prompt was never the problem -- the stale cache is still being read.
```

**Contributing Factors**
- Fixing the RCA-identified layer (e.g., a tool config, schema migration) requires more time, coordination, or risk than a prompt edit, creating pressure to take the easier path regardless of what the RCA found.
- No automated check compares the RCA's declared root-cause layer against the file paths actually touched in the fix diff, so a mismatch isn't caught at review.
- The engineer authoring the fix is not the same person who ran the RCA/isolation testing, and the root-cause finding doesn't fully transfer.
- No post-fix verification re-runs the original failing case, so a fix that doesn't address the real cause can still be merged and marked "resolved."

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| RCA-to-diff layer match | RCA declares "tool layer" as root cause; fix PR only modifies prompt template files | Root-cause-to-diff linter blocks merge, flagging the mismatch | Fix merges despite touching a different layer than the RCA declared |
| Post-fix repro re-run | Original failing case (stale-cache booking confirmation) replayed against the merged fix | Case now passes because the actual tool/cache issue was addressed | Case still fails identically, confirming the fix targeted the wrong layer |
| Repeated-attempt tracking | Incident with 3 sequential fix PRs, none touching the RCA-declared layer | Fix-efficacy dashboard flags the incident for escalation after the 2nd unresolved attempt | Incident accumulates further wrong-target attempts with no escalation trigger |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| root_cause_fix_layer_match_rate_percent (eval) | 100% | Compare RCA-declared root-cause layer against fix-diff file paths across a sample of closed incidents |
| fix_verification_pass_rate_percent (eval) | 100% | Re-run each incident's original failing case against its merged fix and measure pass rate |
| mean_fixes_per_incident (eval) | 1.0-1.2 | Count fix PRs per incident until the original repro case passes |

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
| fix_verification_pass_rate_percent | < 90% |
| root_cause_fix_layer_match_rate_percent | < 85% |
| wrong_target_recurrence_count | >= 2 in a rolling 30 days |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Fix Verification Failed | post-fix re-run of the original failing case still fails | High |
| Root-Cause-to-Diff Mismatch | linter detects the fix diff doesn't touch the layer the RCA declared as root cause | Medium |
| Repeated Wrong-Target Attempts | an incident accumulates 2+ fix attempts without resolution | Low |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
