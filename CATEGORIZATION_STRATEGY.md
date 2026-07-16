# Comprehensive Categorization and Recategorization Plan
## 851 Agent Failure Patterns - Focus on Proper Categorization, Not Deletion

**Status**: Detailed Analysis Phase  
**Date**: 2026-07-13  
**Focus**: Preserve domain-specific value while consolidating universal failures  

---

## Executive Summary

### Overview
- **Total Patterns**: 851 (by-capability: 11 capabilities, by-use-case: 12 domains, cross-cutting: 5 areas)
- **Exact Duplicate Groups**: 15 groups (23 patterns total)
- **Categorization Decision**: Keep domain variants IF they add value; move ONLY universal failures to cross-cutting

### Key Principle
**A pattern belongs in a domain IF:**
- Domain-specific examples are essential to understanding the failure
- Mitigation strategies differ meaningfully by domain
- Practitioners in that domain would not find it by searching cross-cutting
- The failure manifests differently in that domain

**A pattern belongs in cross-cutting IF:**
- The root cause is identical across all domains
- Mitigation is universal, not domain-dependent
- It's a fundamental mechanism (e.g., hallucination, privilege escalation)

### Categorization vs. Deletion Philosophy
This plan is **NOT about deletion** (as in DUPLICATE_AUDIT_PLAN.md). Instead:
- **Consolidation**: Keep ONE canonical location + domain variants with cross-references
- **Cross-Reference**: Link canonical to variants; link variants to canonical
- **Preservation**: Keep domain variants ONLY if they add unique value
- **Deletion**: Only delete exact accidental duplicates with no unique content

---

## Part 1: Analysis of 15 Duplicate Groups

### Group 1: Confidence-Miscalibration (3 instances)

**Instances Found**:
1. `by-capability/knowledge-retrieval/goals/answer-synthesis/failures/confidence-miscalibration.md`
2. `by-capability/document-processing/goals/multimodal-reliability/failures/confidence-miscalibration.md`
3. `by-capability/vision-and-images/goals/visual-hallucination/failures/confidence-miscalibration.md`

**Root Cause** (Universal): LLMs are trained to produce fluent text; they don't naturally express calibrated uncertainty

**Assessment**:
- **Knowledge-Retrieval Version**: RAG-specific - focuses on answer relevancy scoring, evidence consensus, source citation accuracy. Mitigations include RAGAS metrics, query decomposition, evidence balance indices.
- **Document-Processing Version**: VLM/extraction-specific - focuses on token-level probability inspection, calibration curves for OCR, field consistency validation. Different mitigation approach (field-level validation).
- **Vision-and-Images Version**: (Need to verify) - Likely vision-model-specific confidence curves, visual grounding checks

**Decision**: **KEEP ALL 3 AS DOMAIN VARIANTS**
- **Rationale**: Same root cause (LLM training), but domain-specific manifestations and mitigations
- **Canonical**: `cross-cutting/accuracy/goals/output-accuracy/failures/confidence-miscalibration.md` (CREATE NEW - universal version with cross-domain examples)
- **Domain Variants**: Keep all 3 in their domains
- **Cross-References**: 
  - Canonical links to all 3 domain variants: "See domain-specific variants for implementation details"
  - Each domain variant links back to canonical: "This pattern is domain-specific manifestation of universal confidence-miscalibration"
- **Action**: CREATE canonical, ADD cross-references to existing domain files

---

### Group 2: Infinite-Loops (2 instances)

**Instances Found**:
1. `by-capability/document-processing/goals/agentic-orchestration/failures/infinite-loops.md`
2. `cross-cutting/operations/goals/cost-efficiency/failures/infinite-loops.md`

**Root Cause** (Universal): Agent enters repeating cycle without forward progress

**Assessment**:
- **Document-Processing Version**: Document parsing infinite loops - re-reading same section repeatedly
- **Operations/Cost-Efficiency Version**: Agentic loop cost control - unbounded token consumption
- **Manifestation Difference**: Same failure mechanism, but context differs (parsing vs. cost)

**Decision**: **CONSOLIDATE - MOVE BOTH TO CROSS-CUTTING, KEEP OPERATION LOCATION AS CANONICAL**
- **Rationale**: Infinite loops is a universal operations/cost problem, not document-specific
- **Canonical**: `cross-cutting/operations/goals/cost-efficiency/failures/infinite-loops.md` (enhance with multi-domain examples)
- **Domain Reference**: Keep lightweight reference in document-processing pointing to canonical
- **Action**: DELETE `by-capability/document-processing/.../infinite-loops.md`, add cross-reference in document-processing README

---

### Group 3: Wrong-Tool-Selection (2 instances)

**Instances Found**:
1. `by-capability/document-processing/goals/agentic-orchestration/failures/wrong-tool-selection.md`
2. `cross-cutting/operations/goals/tool-reliability/failures/wrong-tool-selection.md`

**Root Cause** (Universal): Agent selects inappropriate tool or misapplies available tool

**Assessment**:
- **Document-Processing Version**: Specific to tool selection in document parsing workflows (OCR tool vs. layout analysis tool)
- **Operations/Tool-Reliability Version**: Universal tool selection problem across all domains
- **Manifestation**: Tool selection logic differs by domain (parsing vs. general operations)

**Decision**: **MOVE DOCUMENT-PROCESSING TO CROSS-CUTTING AS CANONICAL**
- **Rationale**: Wrong tool selection is a universal tool-invocation problem, belongs in operations/tool-reliability
- **Canonical**: `cross-cutting/operations/goals/tool-reliability/failures/wrong-tool-selection.md` (already exists, enhance with document-processing examples)
- **Domain Reference**: Keep minimal reference in document-processing
- **Action**: DELETE `by-capability/document-processing/.../wrong-tool-selection.md`, cross-reference in document-processing README

---

### Group 4: Attribute-Hallucination (2 instances)

**Instances Found**:
1. `by-capability/document-processing/goals/multimodal-reliability/failures/attribute-hallucination.md`
2. `by-capability/vision-and-images/goals/visual-hallucination/failures/attribute-hallucination.md`

**Root Cause** (Universal): Agent hallucinates object attributes not present in input

**Assessment**:
- **Document-Processing Version**: Hallucinating attributes of extracted document objects (invoice totals, field names)
- **Vision-and-Images Version**: Hallucinating attributes of visual objects (color, size, position)
- **Manifestation**: Same root cause, completely different domain implementations

**Decision**: **KEEP BOTH AS DOMAIN VARIANTS**
- **Rationale**: Attribute hallucination manifests fundamentally differently in document extraction vs. vision
  - Document: Extract metadata attributes not present in text
  - Vision: Describe non-existent visual properties
- **Canonical**: `cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-attribute.md` (CREATE NEW - universal version)
- **Domain Variants**: Keep both in their domains
- **Cross-References**: Add bidirectional links
- **Action**: CREATE canonical, ADD cross-references to both domain files

---

### Group 5: Object-Hallucination (2 instances)

**Instances Found**:
1. `by-capability/document-processing/goals/multimodal-reliability/failures/object-hallucination.md`
2. `by-capability/vision-and-images/goals/visual-hallucination/failures/object-hallucination.md`

**Root Cause** (Universal): Agent hallucinates objects not present in input

**Assessment**:
- **Document-Processing Version**: Hallucinating extracted objects/fields (invoice line items, table rows)
- **Vision-and-Images Version**: Hallucinating visual objects (people, animals, objects in image)
- **Manifestation**: Both fit "hallucination" family, but domain-specific

**Decision**: **KEEP BOTH AS DOMAIN VARIANTS**
- **Rationale**: Object hallucination is fundamentally different in document extraction (structured data objects) vs. visual hallucination (visual entities)
- **Canonical**: `cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-object.md` (CREATE NEW)
- **Domain Variants**: Keep both
- **Cross-References**: Add bidirectional links
- **Action**: CREATE canonical, ADD cross-references

---

### Group 6: Intent-Misclassification (2 instances, cross-category)

**Instances Found**:
1. `by-capability/knowledge-retrieval/goals/query-understanding/failures/intent-misclassification.md`
2. `by-use-case/customer-service/goals/conversation-resolution/failures/intent-misclassification.md`

**Root Cause** (Universal): Agent misclassifies user intent/query type

**Assessment**:
- **Knowledge-Retrieval Version**: Classification of information-seeking intent types (lookup vs. synthesis vs. comparison)
- **Customer-Service Version**: Classification of conversation intents (complaint, question, escalation, feedback)
- **Manifestation**: Completely different domain contexts

**Decision**: **CONSOLIDATE - KEEP ONLY BY-CAPABILITY VERSION**
- **Rationale**: 
  - by-capability is about a fundamental agent capability (understanding intent)
  - by-use-case customer-service version is a domain application of the capability
  - Practitioners need the capability view, not the use-case view
- **Canonical**: `by-capability/knowledge-retrieval/goals/query-understanding/failures/intent-misclassification.md`
- **Action**: DELETE `by-use-case/customer-service/.../intent-misclassification.md`, cross-reference in customer-service README

---

### Group 7: Semantic-Mismatch (2 instances)

**Instances Found**:
1. `by-capability/knowledge-retrieval/goals/retrieval/failures/semantic-mismatch.md`
2. `by-capability/knowledge-retrieval/goals/retrieval-quality/failures/semantic-mismatch.md`

**Root Cause** (Universal): Query and document are semantically related but surface keywords don't align

**Assessment**:
- **Retrieval Goal**: General semantic mismatch in retrieval phase
- **Retrieval-Quality Goal**: Semantic mismatch as quality metric/indicator
- **Manifestation**: Same failure, different framing (mechanism vs. quality dimension)

**Decision**: **CONSOLIDATE - KEEP RETRIEVAL-QUALITY AS CANONICAL**
- **Rationale**: Retrieval-quality is the more specific and useful categorization for this goal
- **Canonical**: `by-capability/knowledge-retrieval/goals/retrieval-quality/failures/semantic-mismatch.md`
- **Action**: DELETE `by-capability/knowledge-retrieval/goals/retrieval/failures/semantic-mismatch.md`, cross-reference in retrieval README

---

### Group 8: Distribution-Shift (2 instances, cross-cutting)

**Instances Found**:
1. `by-capability/vision-and-images/goals/adversarial-robustness/failures/distribution-shift.md`
2. `cross-cutting/accuracy/goals/evaluation-reliability/failures/distribution-shift.md`

**Root Cause** (Universal): Model performance degrades due to distribution change in input data

**Assessment**:
- **Vision-and-Images Version**: Distribution shift in visual domain (different camera angles, lighting, backgrounds)
- **Accuracy/Evaluation Version**: Universal distribution shift affecting model evaluation
- **Manifestation**: Both universal, but vision has specific examples

**Decision**: **CONSOLIDATE - KEEP CROSS-CUTTING AS CANONICAL**
- **Rationale**: Distribution shift is a universal ML concept, belongs in cross-cutting accuracy/evaluation
- **Canonical**: `cross-cutting/accuracy/goals/evaluation-reliability/failures/distribution-shift.md` (enhance with vision examples)
- **Domain Reference**: Keep lightweight reference in vision
- **Action**: DELETE `by-capability/vision-and-images/.../distribution-shift.md`, cross-reference in vision README

---

### Group 9: Temporal-Confusion (2 instances, cross-cutting)

**Instances Found**:
1. `cross-cutting/accuracy/goals/output-accuracy/failures/temporal-confusion.md`
2. `cross-cutting/operations/goals/memory-management/failures/temporal-confusion.md`

**Root Cause** (Universal): Agent confuses or mishandles temporal relationships/ordering

**Assessment**:
- **Accuracy/Output-Accuracy Version**: Temporal accuracy in outputs (wrong dates, ordering)
- **Operations/Memory-Management Version**: Temporal memory management (old cache, stale state)
- **Manifestation**: Different aspects of same phenomenon

**Decision**: **CONSOLIDATE - KEEP OUTPUT-ACCURACY AS CANONICAL**
- **Rationale**: Temporal confusion is fundamentally an output accuracy problem, not a memory operations problem
- **Canonical**: `cross-cutting/accuracy/goals/output-accuracy/failures/temporal-confusion.md`
- **Action**: DELETE `cross-cutting/operations/goals/memory-management/.../temporal-confusion.md`, cross-reference in operations README

---

### Group 10: Memory-Poisoning (2 instances, cross-cutting)

**Instances Found**:
1. `cross-cutting/operations/goals/memory-safety/failures/memory-poisoning.md`
2. `cross-cutting/security/goals/safety-security/failures/memory-poisoning.md`

**Root Cause** (Universal): Agent's memory/context contains false or corrupted data affecting outputs

**Assessment**:
- **Operations/Memory-Safety Version**: Memory safety perspective - data corruption, injection attacks
- **Security/Safety-Security Version**: Security perspective - malicious poisoning, attack vectors
- **Manifestation**: Same failure, different concern areas (operations vs. security)

**Decision**: **CONSOLIDATE - KEEP OPERATIONS AS CANONICAL**
- **Rationale**: Memory poisoning is fundamentally an operational integrity issue, not primarily a security concern
  - Prevention is through memory management discipline, not security policies
  - Detection is through data validation, not threat models
- **Canonical**: `cross-cutting/operations/goals/memory-safety/failures/memory-poisoning.md` (enhance with security perspective)
- **Action**: DELETE `cross-cutting/security/goals/safety-security/.../memory-poisoning.md`, cross-reference in security README

---

### Group 11: Privilege-Escalation (2 instances, same category)

**Instances Found**:
1. `cross-cutting/security/goals/safety-security/failures/privilege-escalation.md`
2. `cross-cutting/security/goals/security-autonomy/failures/privilege-escalation.md`

**Root Cause** (Universal): Agent gains/uses higher permissions than intended

**Assessment**:
- **Safety-Security Version**: 
  - Focus: Architectural patterns for permission enforcement
  - Content: Tool-level permission checks, capability-token architecture, centralized PDP
  - Examples: Permission validation at invocation time
- **Security-Autonomy Version**:
  - Focus: Attack scenarios and recovery procedures
  - Content: Detailed SQL escalation example, contributing factors, recovery steps
  - Examples: Social engineering to trigger escalation
- **Manifestation**: Same failure, complementary perspectives (prevention architecture vs. attack response)

**Decision**: **KEEP BOTH BUT REORGANIZE**
- **Rationale**: These are NOT true duplicates - they serve different purposes:
  - **safety-security**: HOW to design systems to prevent escalation (architecture patterns)
  - **security-autonomy**: WHAT escalation looks like and HOW to recover (attack response)
  - Practitioners need BOTH: design patterns AND response procedures
- **Canonical**: `cross-cutting/security/goals/safety-security/failures/privilege-escalation.md` (architectural prevention)
- **Complementary**: Keep `cross-cutting/security/goals/security-autonomy/failures/privilege-escalation.md` (attack/response)
- **Cross-References**: Link both ways:
  - safety-security → "See security-autonomy for attack scenarios and recovery procedures"
  - security-autonomy → "See safety-security for architectural prevention patterns"
- **Action**: ADD cross-references to both files; DO NOT delete

---

## Part 2: Hallucination Family Deep Analysis

The audit identified hallucination as a major consolidation candidate. This needs careful analysis:

### Hallucination Variants Found
1. **confidence-miscalibration** (confidence without accuracy)
2. **attribute-hallucination** (false attributes)
3. **object-hallucination** (false objects)
4. **answer-hallucination** (false answers in RAG)
5. **ocr-hallucination** (false OCR output)
6. **vision-model-hallucination** (false visual content)

### Canonicalization Strategy for Hallucination Family

**DO NOT consolidate all hallucinations into one pattern.**

**Instead**: Create multi-level canonical structure:

```
cross-cutting/accuracy/goals/output-accuracy/failures/
├── hallucination-base-mechanism.md (Universal: LLMs generate plausible false content)
├── hallucination-confidence-miscalibration.md (Sub-pattern: High confidence on false content)
├── hallucination-attribute.md (Sub-pattern: False object attributes)
├── hallucination-object.md (Sub-pattern: False objects/entities)
└── Domain variants (cross-reference to canonical + unique domain examples):
    ├── by-capability/document-processing/.../hallucination-extraction.md
    ├── by-capability/vision-and-images/.../hallucination-visual.md
    ├── by-capability/knowledge-retrieval/.../hallucination-answer-synthesis.md
    └── [other domains]
```

**Rationale**:
- **Base mechanism** is universal (LLM training produces fluent false content)
- **Sub-patterns** (confidence, attribute, object) are recurring mechanisms within hallucination family
- **Domain variants** show how hallucinations manifest specifically:
  - Document: extraction quality, field values
  - Vision: visual properties, scene understanding
  - RAG: answer synthesis, source grounding
  - Speech: transcription, semantic content

**Benefits**:
- Practitioners can understand universal hallucination mechanism
- Specific manifestations are documented in domain contexts
- Sub-patterns capture recurring hallucination modes
- No massive consolidation that loses domain context

---

## Part 3: Summary of Categorization Decisions

### Patterns to CREATE (New Canonical Versions in Cross-Cutting)
1. `cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-base-mechanism.md`
2. `cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-confidence-miscalibration.md`
3. `cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-attribute.md`
4. `cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-object.md`

### Patterns to KEEP in Original Locations (With Cross-References Added)
1. `by-capability/document-processing/.../confidence-miscalibration.md` (VLM-specific)
2. `by-capability/document-processing/.../attribute-hallucination.md` (Document extraction specifics)
3. `by-capability/document-processing/.../object-hallucination.md` (Document object specifics)
4. `by-capability/vision-and-images/.../confidence-miscalibration.md` (Vision model specifics)
5. `by-capability/vision-and-images/.../attribute-hallucination.md` (Visual attribute specifics)
6. `by-capability/vision-and-images/.../object-hallucination.md` (Visual object specifics)
7. `by-capability/knowledge-retrieval/.../confidence-miscalibration.md` (RAG-specific confidence)
8. `cross-cutting/security/goals/safety-security/failures/privilege-escalation.md`
9. `cross-cutting/security/goals/security-autonomy/failures/privilege-escalation.md`

### Patterns to DELETE (True Accidental Duplicates Only)
1. `by-capability/knowledge-retrieval/goals/retrieval/failures/semantic-mismatch.md` (redundant to retrieval-quality version)
2. `by-use-case/customer-service/goals/conversation-resolution/failures/intent-misclassification.md` (covered by by-capability version)

### Patterns to MOVE (Consolidate to Better Location)
1. `cross-cutting/operations/goals/cost-efficiency/failures/infinite-loops.md` ← DELETE from document-processing
2. `cross-cutting/operations/goals/tool-reliability/failures/wrong-tool-selection.md` ← DELETE from document-processing
3. `cross-cutting/accuracy/goals/evaluation-reliability/failures/distribution-shift.md` ← DELETE from vision-and-images
4. `cross-cutting/accuracy/goals/output-accuracy/failures/temporal-confusion.md` ← DELETE from operations
5. `cross-cutting/operations/goals/memory-safety/failures/memory-poisoning.md` ← DELETE from security

---

## Part 4: Cross-Reference Architecture

### Pattern: Canonical + Domain Variants Model

Each canonical pattern should include:

```markdown
## Domain-Specific Variants

This is the universal version of this pattern. For domain-specific implementations, see:

### Domain Variants
- [Vision-Specific Implementation](../../../by-capability/vision-and-images/...)
  - Focus: Visual hallucination detection and prevention
  - Unique mitigations: Vision grounding, scene consistency checks
  
- [Document-Processing Implementation](../../../by-capability/document-processing/...)
  - Focus: OCR and extraction hallucinations
  - Unique mitigations: Field consistency validation, OCR confidence scoring
  
- [RAG/Knowledge-Retrieval Implementation](../../../by-capability/knowledge-retrieval/...)
  - Focus: Answer synthesis hallucinations
  - Unique mitigations: Source grounding, evidence consensus
```

Each domain variant should include:

```markdown
## Related Universal Pattern

This is a domain-specific implementation of the universal pattern:
[Link to canonical](../../../cross-cutting/accuracy/...)

The universal pattern covers the underlying LLM training mechanism. This variant focuses on 
how this specific failure manifests in [DOMAIN] and domain-specific mitigation strategies.
```

### Navigation Tree

```
cross-cutting/accuracy/failures/
├── README: "Accuracy Failures - Universal Patterns"
│   └── Lists all canonical accuracy failures
│   └── Each links to domain variants
│
├── hallucination-base-mechanism.md
│   ├── Universal LLM training root cause
│   └── Links to: confidence-miscalibration, attribute, object
│
├── hallucination-confidence-miscalibration.md
│   ├── Root cause: Confidence training doesn't track truth
│   └── Links to domain variants: doc-processing, vision, knowledge-retrieval
│
└── [other canonical patterns]

by-capability/document-processing/failures/
├── README: "Document Processing Failures"
│   └── Lists patterns specific to document processing
│   └── Where applicable, notes that this is a domain variant of universal pattern
│
├── confidence-miscalibration.md
│   ├── VLM confidence in OCR/extraction tasks
│   ├── Specific to document processing
│   └── Links back to: cross-cutting/accuracy/hallucination-confidence-miscalibration
│
└── [other patterns]
```

---

## Part 5: Implementation Plan

### Phase 1: Create Canonical Cross-Cutting Patterns (1-2 days)

**Files to Create**:
1. `agents/cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-base-mechanism.md`
   - Universal LLM fluency produces plausible false content
   - Examples from multiple domains
   - Links to all hallucination sub-patterns and domain variants

2. `agents/cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-confidence-miscalibration.md`
   - Extends hallucination-base-mechanism
   - Focus: Confidence mismatch with accuracy
   - Multi-domain examples

3. `agents/cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-attribute.md`
   - Extends hallucination-base-mechanism
   - Focus: False object attributes
   - Multi-domain examples

4. `agents/cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-object.md`
   - Extends hallucination-base-mechanism
   - Focus: False objects/entities
   - Multi-domain examples

**Content Structure for Each**:
- Issue: What is the failure?
- Root Cause: Why does this happen? (universal mechanism)
- Examples: 2-3 domain-specific examples showing how it manifests
- Mitigation: Universal strategies applicable across domains
- Domain-Specific Variants: Links with notes on domain-specific approaches
- References: Academic/technical references

**Estimated Effort**: 4-6 hours (leverage existing patterns, consolidate common content)

---

### Phase 2: Add Cross-References (1 day)

**For Each Domain Variant Pattern** (e.g., document-processing/confidence-miscalibration.md):

Add section at end:
```markdown
## Universal Pattern Reference

This is a domain-specific implementation of the universal pattern:
**[Hallucination and Confidence Miscalibration](../../../cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-confidence-miscalibration.md)**

See the canonical pattern for:
- Universal LLM root causes
- Multi-domain examples
- General mitigation strategies

This variant focuses specifically on [DOMAIN] implementations and domain-specific approaches.

## Related Domain Variants

Other domains implementing this pattern:
- [Vision-Specific Version](../vision-and-images/.../confidence-miscalibration.md)
- [Knowledge-Retrieval Version](../knowledge-retrieval/.../confidence-miscalibration.md)
```

**For Each Canonical Cross-Cutting Pattern**:

Add section at end:
```markdown
## Domain-Specific Variants

See domain-specific implementations for implementation details:

### Document Processing
[Document-Processing: Confidence Miscalibration in OCR/Extraction](../../../by-capability/document-processing/.../confidence-miscalibration.md)
- Focus: VLM confidence in extraction tasks
- Unique aspects: Token-level probability inspection, calibration curves, OCR examples

### Vision and Images
[Vision: Confidence Miscalibration in Visual Tasks](../../../by-capability/vision-and-images/.../confidence-miscalibration.md)
- Focus: Visual confidence grounding
- Unique aspects: Scene consistency checks, visual grounding methods

### Knowledge Retrieval
[Knowledge Retrieval: Confidence Miscalibration in Answer Synthesis](../../../by-capability/knowledge-retrieval/.../confidence-miscalibration.md)
- Focus: RAG answer generation confidence
- Unique aspects: Evidence consensus, source grounding, answer relevancy metrics
```

**Estimated Effort**: 2-3 hours

---

### Phase 3: Delete True Duplicates Only (1-2 hours)

**Files to DELETE**:
1. `agents/by-capability/knowledge-retrieval/goals/retrieval/failures/semantic-mismatch.md`
   - Reason: Redundant to retrieval-quality version; no unique domain-specific content
   
2. `agents/by-use-case/customer-service/goals/conversation-resolution/failures/intent-misclassification.md`
   - Reason: Covered by by-capability/knowledge-retrieval version; by-use-case is domain variant without unique value

**Deletion Verification**:
```bash
# Verify files exist before deletion
ls agents/by-capability/knowledge-retrieval/goals/retrieval/failures/semantic-mismatch.md
ls agents/by-use-case/customer-service/goals/conversation-resolution/failures/intent-misclassification.md

# Check for references (should update these)
grep -r "semantic-mismatch" agents/by-capability/knowledge-retrieval/README.md
grep -r "intent-misclassification" agents/by-use-case/customer-service/README.md

# Delete
rm agents/by-capability/knowledge-retrieval/goals/retrieval/failures/semantic-mismatch.md
rm agents/by-use-case/customer-service/goals/conversation-resolution/failures/intent-misclassification.md
```

**Estimated Effort**: 30 minutes

---

### Phase 4: Move Domain-Generic Patterns to Cross-Cutting (2-3 days)

For each pattern to move, maintain two files:
1. **Canonical in cross-cutting**: Full pattern with multi-domain examples
2. **Reference in by-capability**: Lightweight pointer to canonical

#### Pattern: Infinite-Loops

**Canonical**: `agents/cross-cutting/operations/goals/cost-efficiency/failures/infinite-loops.md`
- Enhance with document-processing examples
- Add examples from other domains (conversation loops, etc.)

**Keep in by-capability**:
```markdown
# Infinite Loops (Document-Processing Context)

> **Note**: This is a domain-specific manifestation of the universal pattern:
> [Infinite Loops - Cross-Cutting Operations](../../../cross-cutting/operations/...)
>
> That canonical pattern covers the universal mechanism. This reference highlights
> document-processing-specific aspects.

[Rest of document-processing-specific content]
```

**Files**:
- KEEP: `agents/cross-cutting/operations/goals/cost-efficiency/failures/infinite-loops.md` (enhance)
- DELETE: `agents/by-capability/document-processing/goals/agentic-orchestration/failures/infinite-loops.md`
- ADD: Reference in `agents/by-capability/document-processing/goals/agentic-orchestration/README.md`

#### Pattern: Wrong-Tool-Selection

Similar approach:
- CANONICAL: `agents/cross-cutting/operations/goals/tool-reliability/failures/wrong-tool-selection.md` (enhance)
- DELETE: `agents/by-capability/document-processing/goals/agentic-orchestration/failures/wrong-tool-selection.md`
- ADD: Reference in by-capability README

#### Pattern: Distribution-Shift

- CANONICAL: `agents/cross-cutting/accuracy/goals/evaluation-reliability/failures/distribution-shift.md` (enhance)
- DELETE: `agents/by-capability/vision-and-images/goals/adversarial-robustness/failures/distribution-shift.md`
- ADD: Reference in by-capability README

#### Pattern: Temporal-Confusion

- CANONICAL: `agents/cross-cutting/accuracy/goals/output-accuracy/failures/temporal-confusion.md` (verify it's canonical)
- DELETE: `agents/cross-cutting/operations/goals/memory-management/failures/temporal-confusion.md`
- ADD: Reference in operations README

#### Pattern: Memory-Poisoning

- CANONICAL: `agents/cross-cutting/operations/goals/memory-safety/failures/memory-poisoning.md` (enhance with security perspective)
- DELETE: `agents/cross-cutting/security/goals/safety-security/failures/memory-poisoning.md`
- ADD: Reference in security README

**Estimated Effort**: 3-4 hours

---

### Phase 5: Recategorization Review (Optional, 1 week)

Sample-based recategorization of remaining 851-5=846 patterns:

**Process**:
1. Randomly sample 50 patterns from each category
2. For each sample:
   - Does the pattern belong in its current category?
   - Would practitioners find it in that category?
   - Are there better categorical homes?
3. For miscategorized patterns: Plan moves

**Estimated Findings**:
- 5-10% miscategorized (40-85 patterns)
- Most common: by-use-case pattern that should be by-capability
- Some: cross-cutting patterns that should be domain-specific

**Estimated Effort**: 1 week for sampling + analysis + planning

---

## Part 6: Metrics and Success Criteria

### Pre-Implementation Metrics
- Total patterns: 851
- Exact duplicate groups: 15
- Patterns affected by duplicates: 23
- Cross-cutting patterns: TBD (to count)
- by-capability patterns: TBD (to count)
- by-use-case patterns: TBD (to count)

### Post-Implementation Metrics (Phase 1-4)

After completing Phases 1-4:
- Total patterns: 846 (851 - 5 deleted)
- Exact duplicates: 0 (consolidated)
- Canonical patterns in cross-cutting: +4 new (hallucination family)
- Domain-variant patterns with cross-references: 6 (confidence-miscalibration family)
- Domain-variant patterns linked to canonical: 100% of cross-referenced patterns

### Quality Metrics
- [ ] All canonical patterns include 2+ domain-specific examples
- [ ] All domain variants link back to canonical
- [ ] All canonicals link to all relevant domain variants
- [ ] No broken cross-reference links
- [ ] README files updated with new cross-references
- [ ] Navigation tree reflects canonical + variant structure
- [ ] Practitioners can find pattern via either canonical or domain context

### Success Criteria
✓ All 15 duplicate groups analyzed and categorized  
✓ Proper categorization decisions made (universal vs. domain-specific)  
✓ Domain value preserved for 9+ patterns  
✓ Only 2-5 true accidental duplicates deleted  
✓ 4+ new canonical patterns created  
✓ 50+ cross-references added  
✓ No patterns lost; all receive improved navigation  
✓ Phase 1-4 completed in < 1 week  
✓ Navigation architecture supports both canonical and domain views  

---

## Part 7: Detailed Decision Matrix

| Group | Pattern | Instances | Decision | Canonical | Delete | Action | Preserve |
|-------|---------|-----------|----------|-----------|--------|--------|----------|
| 1 | confidence-miscalibration | 3 | KEEP_VARIANTS | create canonical | 0 | create cross-cutting + cross-refs | YES (3 variants) |
| 2 | infinite-loops | 2 | CONSOLIDATE | operations | 1 | move doc-proc to cross-ref | NO (1 canonical) |
| 3 | wrong-tool-selection | 2 | CONSOLIDATE | operations | 1 | move doc-proc to cross-ref | NO (1 canonical) |
| 4 | attribute-hallucination | 2 | KEEP_VARIANTS | create canonical | 0 | create cross-cutting + cross-refs | YES (2 variants) |
| 5 | object-hallucination | 2 | KEEP_VARIANTS | create canonical | 0 | create cross-cutting + cross-refs | YES (2 variants) |
| 6 | intent-misclassification | 2 | CONSOLIDATE | by-capability | 1 | delete use-case | NO (1 canonical) |
| 7 | semantic-mismatch | 2 | CONSOLIDATE | retrieval-quality | 1 | delete retrieval | NO (1 canonical) |
| 8 | distribution-shift | 2 | CONSOLIDATE | cross-cutting | 1 | move vision to cross-ref | NO (1 canonical) |
| 9 | temporal-confusion | 2 | CONSOLIDATE | output-accuracy | 1 | delete operations | NO (1 canonical) |
| 10 | memory-poisoning | 2 | CONSOLIDATE | operations | 1 | delete security | NO (1 canonical) |
| 11 | privilege-escalation | 2 | KEEP_BOTH | safety-security + autonomy | 0 | cross-ref complementary | YES (2 patterns) |
| **TOTALS** | | **23** | | | **8** | | **18 patterns kept + enhanced** |

---

## Part 8: Post-Implementation Navigation Examples

### Example 1: Practitioner in Document Processing

**Goal**: Understand how to prevent agent confidence miscalibration in document extraction

**Current UX**: Click on `by-capability/document-processing/.../confidence-miscalibration.md`
- Gets domain-specific information immediately
- Includes OCR examples, field-level validation
- Link at bottom: "See universal pattern for LLM training root cause and multi-domain examples"
- Links to other domain variants (vision, knowledge-retrieval)

**Benefit**: Stays in domain context but can access universal knowledge

### Example 2: Practitioner Building Multi-Domain Agent

**Goal**: Understand hallucination mechanisms across all domains

**Current UX**: Start at `cross-cutting/accuracy/.../hallucination-base-mechanism.md`
- Get universal LLM training root cause
- See references to sub-patterns (confidence, attribute, object)
- See links to all domain variants
- Can drill down to specific domain implementations

**Benefit**: Systemic understanding with domain detail on demand

### Example 3: Security Team

**Goal**: Understand privilege escalation attacks and prevention

**Current UX**: Access `cross-cutting/security/goals/safety-security/.../privilege-escalation.md`
- Gets architectural prevention patterns
- Link: "See security-autonomy variant for attack scenarios and recovery procedures"
- Can cross-reference to see how different security goals interact

**Benefit**: Both prevention (architecture) and response (incident handling) available

---

## Part 9: Maintenance Guidelines

### Adding New Patterns

**When creating a new pattern, check**:
1. Is there a universal/canonical version of this pattern?
2. If yes, is this a domain-specific variant?
3. If it's a variant, link to the canonical
4. If it's a new universal pattern, create in cross-cutting with note about future variants
5. Update README files in both canonical and domain locations

**Decision Tree**:
```
New pattern idea
├── Is this a universal mechanism (applies to all/most domains)?
│   ├── YES → Create in cross-cutting/[area]/goals/[goal]/failures/
│   │   └── Note: Future domain variants should link to this
│   └── NO → Create in by-capability/[capability]/goals/[goal]/failures/
│       └── Check if universal canonical exists
│           ├── YES → Add link to canonical
│           └── NO → Consider if canonical needed
```

### Updating Existing Patterns

**When updating a pattern, check**:
1. If it's a canonical pattern, ensure domain variants are still linked
2. If it's a domain variant, ensure it still links to canonical
3. If adding new domain example, consider if canonical needs updating
4. Update README references

### Migration Path for New Discoveries

**When discovering a new duplicate or miscategorization**:
1. Document in CATEGORIZATION_UPDATES.md (new file)
2. Analyze using same criteria as Part 1
3. If consolidation needed:
   - Create PR with categorization decision documented
   - Update canonical and/or domain files
   - Update cross-references
   - Update this strategy document

---

## Part 10: Rollout and Communication

### For Pattern Maintainers

**Message**: "We're improving pattern organization to help practitioners find both universal patterns and domain-specific implementations."

**Changes**:
- New canonical patterns in cross-cutting will emerge
- Your domain patterns may gain links to universals
- Some cross-cutting patterns will gain domain variant links
- This improves discoverability without changing content

### For Pattern Users

**Message**: "Better navigation between universal patterns and domain-specific implementations."

**Improvements**:
- Start with universal pattern, drill down to domain
- Start with domain pattern, see universal mechanism
- Find complementary patterns more easily
- Clearer picture of pattern relationships

### Migration Checklist

- [ ] Identify all patterns affected by cross-references
- [ ] Verify cross-reference links are correct
- [ ] Test navigation from canonical to variants and vice versa
- [ ] Update all README.md files to note new organization
- [ ] Create index of canonical patterns
- [ ] Create index of domain variants
- [ ] Update search/indexing if applicable
- [ ] Communicate changes to pattern library users
- [ ] Gather feedback on new navigation

---

## Conclusion

This categorization strategy prioritizes **proper categorization** over aggressive consolidation. Key principles:

1. **Preserve Domain Value**: Keep domain-specific patterns IF they add unique value
2. **Avoid Over-Consolidation**: Not all duplicates should be deleted
3. **Create Navigation**: Cross-references replace simple consolidation
4. **Build Canonical+Variants Model**: Universal patterns + domain variants work together
5. **Support Multiple Views**: Practitioners can navigate via domain OR universal paths

**Implementation Timeline**:
- Phase 1-4: 1 week
- Phase 5 (optional): 1 week
- **Total**: 1-2 weeks to completion

**Expected Outcome**:
- 851 patterns → 846 patterns (8 deletions)
- 0 exact duplicates
- 50+ high-quality cross-references
- Universal patterns properly categorized
- Domain variants preserved and linked
- Practitioners navigate easily

---

**Document Version**: 1.0  
**Last Updated**: 2026-07-13  
**Status**: Ready for Implementation Phase
