# Categorization Strategy - Quick Reference

**For**: Practitioners implementing CATEGORIZATION_STRATEGY.md  
**Status**: Ready to use  
**Last Updated**: 2026-07-13

---

## The Core Principle

✓ **KEEP** domain-specific variants if they add unique value  
✗ **DELETE** only true accidental duplicates (exact copies)  
↔ **CROSS-REFERENCE** canonical patterns to domain variants  

---

## 15 Duplicate Groups - Decision Summary

### Group 1: Confidence-Miscalibration (3 instances)
- **Decision**: KEEP ALL 3 as domain variants
- **Create**: Canonical in cross-cutting/accuracy
- **Add cross-references**: Between canonical and all 3 domain versions
- **Result**: 3 variants + 1 canonical = enhanced navigation

### Group 2: Infinite-Loops (2 instances)
- **Decision**: CONSOLIDATE to cross-cutting/operations
- **Delete**: by-capability/document-processing version
- **Action**: Enhance canonical with multi-domain examples

### Group 3: Wrong-Tool-Selection (2 instances)
- **Decision**: CONSOLIDATE to cross-cutting/operations
- **Delete**: by-capability/document-processing version
- **Action**: Enhance canonical

### Group 4: Attribute-Hallucination (2 instances)
- **Decision**: KEEP BOTH as domain variants
- **Create**: Canonical in cross-cutting/accuracy
- **Add cross-references**: Bidirectional links
- **Result**: 2 variants + 1 canonical

### Group 5: Object-Hallucination (2 instances)
- **Decision**: KEEP BOTH as domain variants
- **Create**: Canonical in cross-cutting/accuracy
- **Add cross-references**: Bidirectional links
- **Result**: 2 variants + 1 canonical

### Group 6: Intent-Misclassification (2 instances)
- **Decision**: CONSOLIDATE to by-capability (keep capability view)
- **Delete**: by-use-case/customer-service version
- **Action**: Add reference in use-case README

### Group 7: Semantic-Mismatch (2 instances)
- **Decision**: CONSOLIDATE within by-capability
- **Delete**: retrieval version
- **Keep**: retrieval-quality version (more specific)

### Group 8: Distribution-Shift (2 instances)
- **Decision**: CONSOLIDATE to cross-cutting/accuracy
- **Delete**: by-capability/vision-and-images version
- **Action**: Enhance canonical with vision examples

### Group 9: Temporal-Confusion (2 instances)
- **Decision**: CONSOLIDATE to cross-cutting/accuracy
- **Delete**: cross-cutting/operations version
- **Keep**: output-accuracy location (better categorized)

### Group 10: Memory-Poisoning (2 instances)
- **Decision**: CONSOLIDATE to cross-cutting/operations
- **Delete**: cross-cutting/security version
- **Action**: Enhance canonical with security perspective

### Group 11: Privilege-Escalation (2 instances)
- **Decision**: KEEP BOTH (complementary perspectives)
- **safety-security version**: Architectural prevention patterns
- **security-autonomy version**: Attack scenarios and recovery
- **Add**: Cross-references between them (not deletion!)

---

## Summary of File Operations

### CREATE (4 files)
```
✓ cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-base-mechanism.md
✓ cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-confidence-miscalibration.md
✓ cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-attribute.md
✓ cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-object.md
```

### DELETE (7 files - consolidations and duplicates)
```
✗ by-capability/knowledge-retrieval/goals/retrieval/failures/semantic-mismatch.md
✗ by-use-case/customer-service/goals/conversation-resolution/failures/intent-misclassification.md
✗ by-capability/document-processing/goals/agentic-orchestration/failures/infinite-loops.md
✗ by-capability/document-processing/goals/agentic-orchestration/failures/wrong-tool-selection.md
✗ by-capability/vision-and-images/goals/adversarial-robustness/failures/distribution-shift.md
✗ cross-cutting/operations/goals/memory-management/failures/temporal-confusion.md
✗ cross-cutting/security/goals/safety-security/failures/memory-poisoning.md
```

### ENHANCE (5 canonicals - add multi-domain examples)
```
~ cross-cutting/operations/goals/cost-efficiency/failures/infinite-loops.md
~ cross-cutting/operations/goals/tool-reliability/failures/wrong-tool-selection.md
~ cross-cutting/accuracy/goals/evaluation-reliability/failures/distribution-shift.md
~ cross-cutting/accuracy/goals/output-accuracy/failures/temporal-confusion.md
~ cross-cutting/operations/goals/memory-safety/failures/memory-poisoning.md
```

### LINK (9 files - add cross-references)
```
↔ by-capability/knowledge-retrieval/goals/answer-synthesis/failures/confidence-miscalibration.md
↔ by-capability/document-processing/goals/multimodal-reliability/failures/confidence-miscalibration.md
↔ by-capability/vision-and-images/goals/visual-hallucination/failures/confidence-miscalibration.md
↔ by-capability/document-processing/goals/multimodal-reliability/failures/attribute-hallucination.md
↔ by-capability/vision-and-images/goals/visual-hallucination/failures/attribute-hallucination.md
↔ by-capability/document-processing/goals/multimodal-reliability/failures/object-hallucination.md
↔ by-capability/vision-and-images/goals/visual-hallucination/failures/object-hallucination.md
↔ cross-cutting/security/goals/safety-security/failures/privilege-escalation.md
↔ cross-cutting/security/goals/security-autonomy/failures/privilege-escalation.md
```

---

## What This Achieves

### Before
- 851 patterns with 15 duplicate groups (23 instances)
- No clear relationship between universal and domain-specific patterns
- Practitioners don't know which variant to use
- Some patterns exist in multiple places identically

### After
- 846 patterns (851 - 5 deleted = 846)
- 4 new canonical patterns with clear domain variants
- 9 patterns with bidirectional cross-references
- Clear navigation: canonical → domain variants → back to canonical
- No redundant exact duplicates

---

## How Practitioners Use This

### Scenario 1: "I work in Document Processing - show me confidence-miscalibration"
**Old**: One pattern at `by-capability/document-processing/.../confidence-miscalibration.md`  
**New**: Same location, PLUS link to canonical + links to other domain variants  
**Benefit**: Understand domain-specific approach AND universal mechanism

### Scenario 2: "I'm building a multi-domain agent - I need to understand hallucinations universally"
**Old**: Search multiple domains, find different implementations  
**New**: Start at `cross-cutting/accuracy/.../hallucination-base-mechanism.md`  
**Benefit**: Get universal understanding, then drill into any domain needed

### Scenario 3: "Privilege escalation - I need both prevention AND incident response"
**Old**: Two patterns in security goals, no indication they're related  
**New**: Both patterns exist, with cross-references showing relationship  
**Benefit**: See both architectural prevention and attack response in context

---

## Navigation Model

### Canonical Pattern Structure
```markdown
# [Pattern Name]

## Issue/Root Cause/Mitigation (UNIVERSAL)

## Domain-Specific Variants
- [Link to variant 1]
- [Link to variant 2]
- [Link to variant 3]
```

### Domain Variant Structure
```markdown
# [Pattern Name] - [Domain Specific]

## Issue/Root Cause/Mitigation (DOMAIN-SPECIFIC)

## Universal Pattern Reference
- [Link to canonical]

## Related Domain Variants
- [Link to variant in other domain]
```

### README Structure
```markdown
# [Category] Failures

## Navigation
- **Universal patterns**: See cross-cutting/
- **Domain-specific variants**: See below

## Pattern List
- [Pattern 1] (has universal canonical at...)
- [Pattern 2] (unique to this domain)
- [Pattern 3] (cross-reference to universal at...)
```

---

## Implementation Timeline

| Phase | What | Time | Effort |
|-------|------|------|--------|
| 1 | Create 4 canonical patterns | 1 day | 5-6 hrs |
| 2 | Add cross-references | 1 day | 2-3 hrs |
| 3 | Delete accidental duplicates | 0.5 day | 1-2 hrs |
| 4 | Consolidate to cross-cutting | 1 day | 3-4 hrs |
| 5 | Update READMEs | 1 day | 2-3 hrs |
| 6 | Verify + test | 1 day | 5-7 hrs |
| 7 | Documentation | 1 day | 3-4 hrs |
| **TOTAL** | | **1 week** | **22-29 hrs** |

---

## Success Checklist

- [ ] 4 new canonical patterns created
- [ ] 7 redundant/consolidatable patterns deleted
- [ ] 50+ cross-references added and verified
- [ ] 9+ files enhanced with multi-domain examples
- [ ] 8+ README files updated
- [ ] All navigation links tested and working
- [ ] No dead links in repository
- [ ] Domain value preserved for hallucination family
- [ ] Privilege escalation both prevention and response viewpoints kept
- [ ] Practitioners can navigate both directions (canonical↔variant)

---

## Red Flags During Implementation

🚨 **If you see these, something's wrong:**

1. **Deleting a domain variant without unique content** ✓ Correct
2. **Deleting a pattern just because name matches** ✗ Wrong - check for unique domain value first
3. **Creating cross-references without checking links work** ✗ Wrong - test all links
4. **Not updating README when deleting/moving pattern** ✗ Wrong - always update README
5. **Canonical pattern with no domain examples** ✗ Wrong - canonical should include multi-domain examples
6. **Domain variant not linking back to canonical** ✗ Wrong - make bidirectional
7. **Keeping privilege escalation as single pattern** ✗ Wrong - keep both (complementary perspectives)
8. **Deleting hallucination variants** ✗ Wrong - keep domain-specific versions, create canonical

---

## Common Questions

**Q: Do we really need to keep 3 confidence-miscalibration patterns?**
A: Yes! Each domain has unique manifestations:
- Document: VLM token-level probability inspection
- Vision: Visual grounding and scene consistency
- RAG: Answer relevancy scoring and evidence consensus

Users searching in their domain won't find papers/examples they understand if we delete their domain version.

**Q: Why keep both privilege-escalation patterns?**
A: They serve different purposes:
- safety-security: "How do I build systems that prevent this?"
- security-autonomy: "This happened to us. Now what?"

Both are needed. Don't consolidate.

**Q: Should I create references instead of deleting patterns?**
A: Decision matrix in CATEGORIZATION_STRATEGY.md Part 1 explains each group. For intent-misclassification, the use-case version adds no unique value → delete. For confidence-miscalibration, domain versions add significant value → keep + link.

**Q: How do I know if a domain variant adds value?**
A: Ask these questions:
- Would examples/case studies in this domain help practitioners? → KEEP
- Would mitigation strategies differ meaningfully? → KEEP
- Is this just copied content from another domain? → DELETE
- Would practitioners searching in this domain NOT find this content elsewhere? → KEEP

**Q: What if I find patterns not in the 15 groups that might be duplicates?**
A: Document in CATEGORIZATION_UPDATES.md and follow same categorization analysis. Don't make decisions alone - create issue for review.

---

## Key Contacts

**Questions about strategy**:
- See CATEGORIZATION_STRATEGY.md Part 1-3

**Questions about implementation**:
- See CATEGORIZATION_IMPLEMENTATION_CHECKLIST.md

**Questions about navigation**:
- See NAVIGATION_GUIDE.md (will be created)

**Questions about specific patterns**:
- See CATEGORIZATION_STRATEGY.md Part 7 (Decision Matrix)

---

## Metrics to Track

**Before Implementation**:
```
Total patterns: 851
Duplicate groups: 15
Affected patterns: 23
Cross-references: 0
Canonical patterns: 0
```

**After Implementation (Target)**:
```
Total patterns: 846 (851 - 5 deleted)
Duplicate groups: 0 (consolidated)
Affected patterns: 0 (consolidated)
Cross-references: 50+
Canonical patterns: 4+ (new in cross-cutting)
Domain variants linked: 9+ 
```

---

**Print this page and keep at desk during implementation!**  
**Updated**: 2026-07-13  
**Version**: 1.0
