# Comprehensive Duplicate Audit Plan: 851 Agent Failure Patterns

> **Status update (2026-07-27)**: Part 1's 11 groups were re-verified against current disk state. 7 groups (infinite-loops, wrong-tool-selection, intent-misclassification, semantic-mismatch, distribution-shift, temporal-confusion, memory-poisoning) are already resolved — one copy was deleted in an earlier run (sometimes the opposite side of the pair from what this doc recommended, but only one copy remains either way, so there's no remaining duplicate). The other 4 groups (confidence-miscalibration ×3, attribute-hallucination ×2, object-hallucination ×2, privilege-escalation ×2) still have all copies on disk, but inspection shows they were **not** left as naive duplicates: each now carries an explicit `## Universal Pattern Reference` (pointing to a shared cross-cutting canonical) or `## Complementary Pattern` (explicit Prevention-vs-Detection&Response split) section, with genuinely distinct Root Cause/Example/Mitigations content per copy and correct cross-links between them. This is the legitimate domain-variant/complementary-split outcome `DUPLICATE_PREVENTION_PROTOCOL.md` allows, not leftover duplication — do **not** merge or delete these 4 groups. Part 1 of this plan is effectively closed; no further action needed on it.

## Executive Summary

### Audit Results

- **Total Patterns Analyzed**: 851 (across by-capability, by-use-case, cross-cutting)
- **Exact Name Duplicates Found**: 11 groups (22 patterns)
- **Cross-Category Duplicates**: 4 groups (8 patterns)
- **Total Duplicate Instances**: 23 patterns affected by 15 groups
- **Recommended Immediate Deletions**: 16 patterns (1.9% reduction)
- **Known Consolidation Candidates**: 6 major families with 100+ variants
- **Broader Consolidation Potential**: 150-200 additional patterns (18-24% total reduction)

### Critical Findings

**Immediate Action Required**:
- 11 groups of exactly-named duplicates across categories (easy to fix)
- 4 cross-category patterns that should consolidate to by-capability
- 6 known consolidation candidates with significant domain variants

**Broader Opportunities**:
- Hallucination patterns (40+ variants across domains) → 6 canonical
- Stale training knowledge variants (25+ patterns) → 1 canonical + references
- Context/memory loss (20+ patterns) → 1 canonical + variants
- Verification failures (30+ patterns) → 1 canonical + references

---

## Part 1: Exact Duplicate Groups (11 Groups, 23 Patterns)

### Group 1: confidence-miscalibration (3 instances)

**Pattern**: Agent generates high-confidence output despite lacking evidence

**Locations**:
- `agents/by-capability/document-processing/goals/multimodal-reliability/failures/confidence-miscalibration.md`
- `agents/by-capability/knowledge-retrieval/goals/answer-synthesis/failures/confidence-miscalibration.md`
- `agents/by-capability/vision-and-images/goals/visual-hallucination/failures/confidence-miscalibration.md`

**Recommendation**: 
- **Action**: CONSOLIDATE
- **Keep**: by-capability/knowledge-retrieval/answer-synthesis (broadest application)
- **Delete**: document-processing and vision-and-images copies
- **Impact**: -2 patterns

---

### Group 2: infinite-loops (2 instances)

**Pattern**: Agent enters repeating cycle without forward progress

**Locations**:
- `agents/by-capability/document-processing/goals/agentic-orchestration/failures/infinite-loops.md`
- `agents/cross-cutting/operations/goals/cost-efficiency/failures/infinite-loops.md`

**Recommendation**:
- **Action**: CONSOLIDATE to by-capability
- **Keep**: document-processing/agentic-orchestration (core mechanism)
- **Delete**: cross-cutting/operations copy
- **Impact**: -1 pattern

---

### Group 3: wrong-tool-selection (2 instances)

**Pattern**: Agent selects inappropriate tool or misapplies available tool

**Locations**:
- `agents/by-capability/document-processing/goals/agentic-orchestration/failures/wrong-tool-selection.md`
- `agents/cross-cutting/operations/goals/tool-reliability/failures/wrong-tool-selection.md`

**Recommendation**:
- **Action**: CONSOLIDATE to by-capability
- **Keep**: document-processing/agentic-orchestration
- **Delete**: cross-cutting/operations
- **Impact**: -1 pattern

---

### Group 4: attribute-hallucination (2 instances)

**Pattern**: Agent hallucinates object attributes not present in input

**Locations**:
- `agents/by-capability/document-processing/goals/multimodal-reliability/failures/attribute-hallucination.md`
- `agents/by-capability/vision-and-images/goals/visual-hallucination/failures/attribute-hallucination.md`

**Recommendation**:
- **Action**: CONSOLIDATE
- **Keep**: vision-and-images/visual-hallucination (more specific)
- **Delete**: document-processing copy
- **Impact**: -1 pattern

---

### Group 5: object-hallucination (2 instances)

**Pattern**: Agent hallucinates objects not present in input

**Locations**:
- `agents/by-capability/document-processing/goals/multimodal-reliability/failures/object-hallucination.md`
- `agents/by-capability/vision-and-images/goals/visual-hallucination/failures/object-hallucination.md`

**Recommendation**:
- **Action**: CONSOLIDATE
- **Keep**: vision-and-images/visual-hallucination
- **Delete**: document-processing copy
- **Impact**: -1 pattern

---

### Group 6: intent-misclassification (2 instances, cross-category)

**Pattern**: Agent misclassifies user intent/query type

**Locations**:
- `agents/by-capability/knowledge-retrieval/goals/query-understanding/failures/intent-misclassification.md`
- `agents/by-use-case/customer-service/goals/conversation-resolution/failures/intent-misclassification.md`

**Recommendation**:
- **Action**: CONSOLIDATE to by-capability
- **Keep**: knowledge-retrieval/query-understanding (generic capability)
- **Delete**: customer-service copy (domain variant)
- **Impact**: -1 pattern

---

### Group 7: semantic-mismatch (2 instances)

**Pattern**: Query and document are semantically related but surface keywords don't align

**Locations**:
- `agents/by-capability/knowledge-retrieval/goals/retrieval/failures/semantic-mismatch.md`
- `agents/by-capability/knowledge-retrieval/goals/retrieval-quality/failures/semantic-mismatch.md`

**Recommendation**:
- **Action**: CONSOLIDATE
- **Keep**: retrieval-quality (more specific goal)
- **Delete**: retrieval copy
- **Impact**: -1 pattern

---

### Group 8: distribution-shift (2 instances, cross-cutting)

**Pattern**: Model performance degrades due to distribution change in input data

**Locations**:
- `agents/by-capability/vision-and-images/goals/adversarial-robustness/failures/distribution-shift.md`
- `agents/cross-cutting/accuracy/goals/evaluation-reliability/failures/distribution-shift.md`

**Recommendation**:
- **Action**: CONSOLIDATE to by-capability
- **Keep**: vision-and-images/adversarial-robustness (specific capability)
- **Delete**: cross-cutting copy
- **Impact**: -1 pattern

---

### Group 9: temporal-confusion (2 instances)

**Pattern**: Agent confuses or mishandles temporal relationships/ordering

**Locations**:
- `agents/cross-cutting/accuracy/goals/output-accuracy/failures/temporal-confusion.md`
- `agents/cross-cutting/operations/goals/memory-management/failures/temporal-confusion.md`

**Recommendation**:
- **Action**: CONSOLIDATE
- **Keep**: accuracy/output-accuracy
- **Delete**: operations/memory-management
- **Impact**: -1 pattern

---

### Group 10: memory-poisoning (2 instances)

**Pattern**: Agent's memory/context contains false or corrupted data affecting outputs

**Locations**:
- `agents/cross-cutting/operations/goals/memory-safety/failures/memory-poisoning.md`
- `agents/cross-cutting/security/goals/safety-security/failures/memory-poisoning.md`

**Recommendation**:
- **Action**: CONSOLIDATE
- **Keep**: operations/memory-safety (operational concern)
- **Delete**: security copy
- **Impact**: -1 pattern

---

### Group 11: privilege-escalation (2 instances)

**Pattern**: Agent gains/requests unauthorized access levels

**Locations**:
- `agents/cross-cutting/security/goals/safety-security/failures/privilege-escalation.md`
- `agents/cross-cutting/security/goals/security-autonomy/failures/privilege-escalation.md`

**Recommendation**:
- **Action**: CONSOLIDATE
- **Keep**: safety-security (broader scope)
- **Delete**: security-autonomy copy
- **Impact**: -1 pattern

---

## Summary of Exact Duplicates

| Group | Primary Pattern | Instances | To Delete | Notes |
|-------|-----------------|-----------|-----------|-------|
| 1 | confidence-miscalibration | 3 | 2 | answer-synthesis is canonical |
| 2 | infinite-loops | 2 | 1 | by-capability canonical |
| 3 | wrong-tool-selection | 2 | 1 | by-capability canonical |
| 4 | attribute-hallucination | 2 | 1 | vision-and-images canonical |
| 5 | object-hallucination | 2 | 1 | vision-and-images canonical |
| 6 | intent-misclassification | 2 | 1 | by-capability canonical |
| 7 | semantic-mismatch | 2 | 1 | retrieval-quality canonical |
| 8 | distribution-shift | 2 | 1 | by-capability canonical |
| 9 | temporal-confusion | 2 | 1 | accuracy canonical |
| 10 | memory-poisoning | 2 | 1 | operations canonical |
| 11 | privilege-escalation | 2 | 1 | safety-security canonical |
| **TOTAL** | | **23** | **16** | **1.9% reduction** |

---

## Part 2: Cross-Category Consolidation Opportunities

### Known Consolidation Candidates with Semantic Variants

#### 1. Agent Defaults to Stale Training Knowledge Over Live-Lookup Tool

**Canonical Location**: `agents/cross-cutting/accuracy/goals/knowledge-staleness/failures/agent-defaults-to-stale-training-knowledge-over-live-lookup-tool.md`

**Root Cause**: Agent relies on parametric (training-time) knowledge instead of calling available live-lookup tools

**Estimated Variants Across Domains**: 25-30 patterns

**Sample Variants Found**:
- `stale-training-corpus-tone-rule-overrides-live-brand-voice-guideline-update.md` (content-marketing)
- `stale-training-corpus-disclosure-placement-rule-overrides-updated-regulatory-guidance.md` (content-marketing)
- `stale-training-corpus-quality-threshold-overrides-live-qc-policy-tool.md` (content-marketing)
- `stale-training-corpus-meta-tag-rule-overrides-live-seo-guidelines-tool.md` (content-marketing)
- `stale-training-corpus-comp-benchmarks-override-live-market-data.md` (hr-recruiting)
- `stale-training-corpus-visa-sponsorship-rule-overrides-live-immigration-policy-tool.md` (hr-recruiting)

**Consolidation Strategy**:
- Keep canonical in cross-cutting/accuracy/knowledge-staleness/
- Preserve 4-5 domain-specific variants (finance, healthcare, legal) with unique mitigations
- Create cross-references from other domains
- **Estimated Savings**: 20+ pattern deletions

---

#### 2. Self-Verification Cannot Catch Upstream Errors

**Canonical Location**: `agents/cross-cutting/accuracy/goals/output-verification/failures/self-verification-cannot-catch-upstream-errors.md`

**Root Cause**: Agent's own verification cannot detect errors in tools/data it depends on

**Estimated Variants**: 30-35 patterns across domains

**Consolidation Strategy**:
- Keep canonical as universal pattern
- Preserve 2-3 domain-specific variants (finance, healthcare - high stakes)
- Cross-reference from all other domains
- **Estimated Savings**: 28+ pattern deletions

---

#### 3. Long-Session Context Loss Violates Earlier Constraints

**Canonical Location**: `agents/cross-cutting/accuracy/goals/context-management/failures/long-session-context-loss-violates-earlier-constraints.md`

**Root Cause**: Agent forgets earlier constraints/instructions in multi-turn sessions

**Estimated Variants**: 25-30 patterns

**Consolidation Strategy**:
- Keep canonical
- Preserve conversation-flow variant (unique context for conversation agents)
- Create references from multi-turn agent use cases
- **Estimated Savings**: 24+ pattern deletions

---

#### 4. Hallucinated Completion When Upstream Dependency Fails

**Canonical Location**: `agents/cross-cutting/accuracy/goals/output-accuracy/failures/hallucinated-completion-when-upstream-dependency-fails.md`

**Root Cause**: Agent fabricates data when upstream tool/API fails instead of reporting failure

**Estimated Variants**: 35-40 patterns

**Consolidation Strategy**:
- Keep canonical
- Preserve 3-4 domain variants (finance error handling, compliance reporting)
- Create references from all other domains
- **Estimated Savings**: 33+ pattern deletions

---

#### 5. Semantic-Similarity Retrieval Misses Structural Attributes

**Canonical Location**: `agents/by-capability/knowledge-retrieval/goals/retrieval-relevance/failures/semantic-similarity-retrieval-misses-structural-attributes.md`

**Root Cause**: Embedding-based retrieval matches semantically but misses structural/attribute requirements

**Estimated Variants**: 4-6 patterns (mainly finance/legal)

**Consolidation Strategy**:
- Keep canonical in by-capability
- Preserve finance-specific variant (domain-unique mitigations)
- Create references from legal domain
- **Estimated Savings**: 3-4 pattern deletions

---

#### 6. Handoff Schema Loses Upstream Confidence Signal

**Canonical Location**: `agents/by-capability/multi-agent-systems/goals/handoff-reliability/failures/handoff-schema-loses-upstream-confidence-signal.md`

**Root Cause**: Multi-agent handoffs drop important metadata (confidence scores, version info, provenance)

**Estimated Variants**: 4-8 patterns (agent coordination scenarios)

**Consolidation Strategy**:
- Keep canonical
- Preserve high-value finance variant (trading agent handoffs)
- Create references from workflow automation
- **Estimated Savings**: 3-5 pattern deletions

---

## Part 3: Implementation Plan

### Phase 1: Immediate (Exact Duplicates) - 1-2 Days

**Files to Delete** (16 total):

1. `agents/by-capability/document-processing/goals/multimodal-reliability/failures/confidence-miscalibration.md`
2. `agents/by-capability/vision-and-images/goals/visual-hallucination/failures/confidence-miscalibration.md`
3. `agents/cross-cutting/operations/goals/cost-efficiency/failures/infinite-loops.md`
4. `agents/cross-cutting/operations/goals/tool-reliability/failures/wrong-tool-selection.md`
5. `agents/by-capability/document-processing/goals/multimodal-reliability/failures/attribute-hallucination.md`
6. `agents/by-capability/document-processing/goals/multimodal-reliability/failures/object-hallucination.md`
7. `agents/by-use-case/customer-service/goals/conversation-resolution/failures/intent-misclassification.md`
8. `agents/by-capability/knowledge-retrieval/goals/retrieval/failures/semantic-mismatch.md`
9. `agents/cross-cutting/accuracy/goals/evaluation-reliability/failures/distribution-shift.md`
10. `agents/cross-cutting/operations/goals/memory-management/failures/temporal-confusion.md`
11. `agents/cross-cutting/security/goals/safety-security/failures/memory-poisoning.md`
12. `agents/cross-cutting/security/goals/security-autonomy/failures/privilege-escalation.md`

**Commit Message**:
```
fix: consolidate 16 exact duplicate patterns

- confidence-miscalibration: keep answer-synthesis, delete duplicates
- infinite-loops: keep document-processing/agentic-orchestration
- wrong-tool-selection: keep document-processing/agentic-orchestration
- attribute-hallucination: keep vision-and-images
- object-hallucination: keep vision-and-images
- intent-misclassification: keep by-capability
- semantic-mismatch: keep retrieval-quality
- distribution-shift: keep vision-and-images
- temporal-confusion: keep output-accuracy
- memory-poisoning: keep operations
- privilege-escalation: keep safety-security

Updates README: 851 → 835 patterns (1.9% reduction)
```

**Verification**:
```bash
./check-duplicates.sh  # Should report 0 exact duplicates
find ./agents -name "*.md" | wc -l  # Should show 835
```

---

### Phase 2: Known Candidates (1-2 Weeks)

For each of the 6 known consolidation candidates:

1. Identify all related patterns in by-use-case
2. Review content for unique value (domain-specific examples, mitigations)
3. Decide: Delete (generic variant) vs Keep (domain-unique)
4. Create cross-reference patterns in domain folders
5. Update canonical pattern with domain examples

**Estimated Consolidation**:
- Stale training knowledge: 25 → 1 canonical + 4 domain = -20 patterns
- Self-verification upstream: 32 → 1 canonical + 2 domain = -29 patterns
- Context loss: 27 → 1 canonical + 1 domain = -25 patterns
- Hallucinated completion: 38 → 1 canonical + 3 domain = -34 patterns
- Semantic retrieval: 5 → 1 canonical + 1 domain = -3 patterns
- Handoff schema: 6 → 1 canonical + 1 domain = -4 patterns

**Total Phase 2 Reduction**: ~115 patterns

**Updated Count**: 835 → ~720 (15.4% total reduction)

---

### Phase 3: Category Review (Optional, 1 Week)

Sample 50 patterns from each category for recategorization:
- Do patterns in by-use-case belong in by-capability?
- Are cross-cutting patterns properly categorized?
- Any miscategorized patterns found?

Estimated: 10-20 additional patterns for recategorization

---

## Part 4: Detailed Merge/Recategorization Reference Table

### Exact Duplicates Reference Table

| Pattern Name | Locations (Count) | Canonical | Secondary | Action |
|--------------|-------------------|-----------|-----------|--------|
| confidence-miscalibration | document-processing, knowledge-retrieval, vision-and-images (3) | knowledge-retrieval | delete 2 | CONSOLIDATE |
| infinite-loops | document-processing, operations (2) | document-processing | delete ops | CONSOLIDATE |
| wrong-tool-selection | document-processing, operations (2) | document-processing | delete ops | CONSOLIDATE |
| attribute-hallucination | document-processing, vision-and-images (2) | vision-and-images | delete doc | CONSOLIDATE |
| object-hallucination | document-processing, vision-and-images (2) | vision-and-images | delete doc | CONSOLIDATE |
| intent-misclassification | by-capability, by-use-case (2) | by-capability | delete use-case | CONSOLIDATE |
| semantic-mismatch | retrieval, retrieval-quality (2) | retrieval-quality | delete retrieval | CONSOLIDATE |
| distribution-shift | vision-and-images, accuracy (2) | vision-and-images | delete acc | CONSOLIDATE |
| temporal-confusion | accuracy, operations (2) | accuracy | delete ops | CONSOLIDATE |
| memory-poisoning | operations, security (2) | operations | delete sec | CONSOLIDATE |
| privilege-escalation | safety-security, security-autonomy (2) | safety-security | delete auton | CONSOLIDATE |

---

## Part 5: Quality Impact

### Before Consolidation
- 851 total patterns
- 26+ duplicate groups (exact + cross-category)
- Inconsistent naming across domains
- Unclear which pattern to reference in each domain

### After Phase 1 (Exact Duplicates)
- 835 patterns (-1.9%)
- 0 exact duplicates
- Better category organization
- Clear canonical locations

### After Phase 2 (Known Candidates)
- ~720 patterns (-15.4% total)
- 80+ cross-references created
- Consolidated failure mechanisms
- Easier navigation for users

### After Phase 3 (Optional Recategorization)
- ~700 patterns (-17.8% total)
- Cleaner category boundaries
- Reduced miscategorization
- Improved by-capability vs by-use-case split

---

## Part 6: Success Criteria

- [x] Identified all exact name duplicates (11 groups)
- [x] Identified cross-category consolidation candidates (6 families)
- [x] Created actionable merge/deletion plan
- [x] Estimated net reduction (16-115+ patterns, 1.9-18% reduction)
- [x] Provided specific file operations needed
- [x] Documented consolidation strategy
- [ ] Execute Phase 1 (immediate)
- [ ] Execute Phase 2 (1-2 weeks)
- [ ] Verify no broken links post-consolidation
- [ ] Update README and documentation

---

## Appendix: Duplicate Detection Methodology

### Detection Strategies Used

1. **Exact Name Matching**: File names identical, different locations
2. **Normalized Name Matching**: Variations (hyphens, underscores, case)
3. **Root Cause Similarity**: Similar issue descriptions (>70% similarity)
4. **Cross-Category Analysis**: Same pattern across by-capability, by-use-case, cross-cutting
5. **Domain Variant Detection**: Named variations indicating domain specialization

### Threshold Settings

- Exact match: 100% filename match
- Cross-category: Same normalized name + different category branches
- Semantic similarity: >70% overlap in root cause description

### Known Limitations

- Semantic variants with completely different names may be missed
- Domain-specific variants may be legitimate and not duplicates
- Some "duplicates" may have subtle contextual differences worth preserving

---

**Report Generated**: July 13, 2026  
**Total Patterns Analyzed**: 851  
**Analysis Approach**: Comprehensive multi-strategy duplicate detection  
**Recommendation**: Implement Phase 1 immediately, Phase 2 within 2 weeks  
**Estimated Effort**: 1 week for full implementation + verification
