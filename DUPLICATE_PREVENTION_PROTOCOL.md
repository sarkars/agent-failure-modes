# Duplicate Prevention Protocol for New Pattern Authorship

**Version**: 1.0  
**Date**: July 2026  
**Baseline**: 837 existing patterns across cross-cutting, by-capability, by-use-case  
**Consolidation History**: 141+ duplicates merged in prior audit  

---

## OVERVIEW

This protocol prevents duplicate pattern creation during new authorship. It uses a **4-layer validation system**:

1. **Semantic Deduplication** — Check if failure mechanism already exists
2. **Pattern Registry** — Indexed lookup by failure type
3. **Consolidation Rules** — When to merge vs. create new
4. **Validation Checklist** — Pre-authorship screening

---

## LAYER 1: SEMANTIC DEDUPLICATION RULES

### Rule 1A: Same Mechanism, Different Domain = CONSOLIDATE

**Pattern**: Hallucinated tool invocation  
**Examples**:
- Legal: "Called non-existent statute"
- Healthcare: "Prescribed non-existent drug interaction"
- Code: "Invoked undefined function"

**Action**: Single cross-cutting pattern with domain-specific examples

**Existing Pattern**: [agents/cross-cutting/operations/goals/tool-reliability/failures/parameter-mismatches.md](../agents/cross-cutting/operations/goals/tool-reliability/failures/parameter-mismatches.md)

---

### Rule 1B: Different Mechanism, Same Domain = CREATE NEW

**Pattern A**: Hallucinated legal case citations (mechanism: fabrication)  
**Pattern B**: Legal statute misquotation (mechanism: misremembering specific text)

**Action**: Separate patterns with clear mechanism distinction

**Reasoning**: Mitigations differ:
- Fabrication: Verify against case database
- Misquotation: Verify exact statute text character-by-character

---

### Rule 1C: Different Mechanism & Domain = CREATE NEW

**Always create new** unless the mechanism is already documented in a cross-cutting category.

**Example**: 
- Vision model counting failures (mechanism: patch tokenization)
- Code generation logic bugs (mechanism: insufficient reasoning)
→ **Two separate patterns** (different roots)

---

### Rule 1D: Subspecialization = LINK, Don't Duplicate

**Parent Pattern**: "Hallucinated completion when upstream dependency fails"  
**Subspecializations**: 
- API timeout variant
- Database query timeout variant
- Network failure variant

**Action**: One parent pattern + examples cover subspecializations; don't create separate patterns

**Existing**: [agents/cross-cutting/accuracy/goals/output-accuracy/failures/hallucinated-completion-when-upstream-dependency-fails.md](../agents/cross-cutting/accuracy/goals/output-accuracy/failures/hallucinated-completion-when-upstream-dependency-fails.md)

---

## LAYER 2: PATTERN REGISTRY LOOKUP

### Before Authoring Any New Pattern, Query These Indices:

#### 2A. Failure Mechanism Index (by root cause)

**Command to search**:
```bash
grep -r "Root Cause" agents/*/goals/*/failures/*.md | grep -i "YOUR_MECHANISM"
```

**Example**: Before authoring "tool selection confidence miscalibration":
```bash
grep -r "Root Cause" agents/ | grep -i "confidence\|calibration"
```

Result:
- agents/cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md
- agents/by-capability/knowledge-retrieval/goals/answer-synthesis/failures/uncertainty-not-surfaced.md

**Action**: Link to these instead of creating new pattern with same root cause.

---

#### 2B. Symptom Index (by observable behavior)

**Patterns with overlapping symptoms are likely duplicates**:

| Symptom | Existing Patterns | Action |
|---|---|---|
| "Agent outputs with high confidence but is wrong" | confident-fabrication, output-verification (self-verification-cannot-catch-upstream) | CHECK: Same root cause? |
| "Agent suggests already-ruled-out option" | long-session-context-loss-violates-earlier-constraints | Link to parent |
| "Tool selection increases errors with tool count" | parameter-mismatches, tool-reliability patterns | Consolidate mechanisms |
| "Multi-agent system shows 80%+ failure" | multi-agent error propagation patterns | Check: Count effects or structural issues? |

---

#### 2C. Domain Index (by use-case)

**Search existing patterns in target domain FIRST**:

Before creating mortgage patterns:
```bash
ls agents/by-use-case/mortgage-documents/goals/*/failures/*.md | wc -l
# Returns: 47 existing patterns

grep -r "## Issue" agents/by-use-case/mortgage-documents/goals/*/failures/*.md | head -20
# Shows: existing failure issues
```

**For each new source**, check if that failure mode is already documented in domain directory.

---

## LAYER 3: CONSOLIDATION DECISION TREE

Use this flowchart **before authoring**:

```
NEW FAILURE PATTERN IDENTIFIED
│
├─ Does it exist in cross-cutting? 
│  ├─ YES (same mechanism) → LINK TO EXISTING + ADD EXAMPLE
│  └─ NO → Continue
│
├─ Does it exist in by-capability?
│  ├─ YES (same mechanism) → LINK TO EXISTING + ADD EXAMPLE
│  └─ NO → Continue
│
├─ Does it exist in by-use-case for this domain?
│  ├─ YES (same mechanism) → CONSOLIDATE (move to parent category)
│  └─ NO → Continue
│
├─ Is mechanism GENUINELY DIFFERENT from all similar patterns?
│  ├─ NO (similar root cause) → CONSOLIDATE to existing pattern
│  ├─ YES → Continue to author NEW PATTERN
│
└─ Author new pattern with:
   ├─ Issue (clear failure mechanism)
   ├─ Root Cause (why this specific thing fails)
   ├─ Distinguishing Example (how it differs from related patterns)
   ├─ Cross-references (links to related patterns)
   └─ Template compliance check
```

---

## LAYER 4: PRE-AUTHORSHIP VALIDATION CHECKLIST

**BEFORE writing any new pattern file**, complete this checklist**:

### A. Semantic Uniqueness
- [ ] Pattern has **distinct root cause** from existing patterns (not subspecialization)
- [ ] Searched for similar patterns using: name, mechanism, symptom
- [ ] Searched cross-cutting categories first (most likely consolidation point)
- [ ] Found 0 patterns with identical "Issue" statement
- [ ] Found 0 patterns with identical "Root Cause"

### B. Domain Placement
- [ ] Pattern categorized in correct hierarchy:
  - [ ] Cross-cutting (applies to ALL agent types)? → agents/cross-cutting/[category]/
  - [ ] By-capability (specific to agent design pattern)? → agents/by-capability/[capability]/
  - [ ] By-use-case (industry/domain specific)? → agents/by-use-case/[domain]/
- [ ] Searched existing category before placement
- [ ] No duplication across categories with same mechanism

### C. Source Grounding
- [ ] Source is academic paper (arXiv, conference) OR production incident
- [ ] Source explicitly documents this failure OR arXiv paper cites it
- [ ] Source is from 2023-2026 (recency check)
- [ ] Source is NOT theoretical; has concrete examples or data

### D. Mechanism Clarity
- [ ] Root Cause explains WHY (not WHAT agent does)
- [ ] Root Cause differs clearly from [list 3-5 similar patterns]
- [ ] Mitigation targets the root cause, not symptoms
- [ ] Can distinguish this pattern from similar ones in 1 sentence

### E. Consolidation Check
- [ ] If pattern is subspecialization of existing pattern → LINK instead
- [ ] If pattern exists in domain but belongs in cross-cutting → NOTE for consolidation
- [ ] If pattern exists with different name but same mechanism → DEDUPLICATE now

### F. Template Compliance
- [ ] Issue: Present and specific
- [ ] Frequency: Documented or data-driven
- [ ] Symptoms: Concrete, verifiable
- [ ] Root Cause: Mechanistic, not behavioral
- [ ] Examples: Realistic, from source
- [ ] Key Statistics: Cited from source
- [ ] Mitigation Strategies: Actionable
- [ ] Production Signals: Specific (metrics, alerts)
- [ ] References: Linked to sources

### G. Cross-Reference Check
- [ ] Pattern links to 2-5 related patterns
- [ ] Related patterns link back (bidirectional)
- [ ] Links use [pattern-title](../path/to/pattern.md) format
- [ ] No orphaned patterns (every pattern has ≥1 inbound link)

### H. Duplicate Final Check
- [ ] Filename unique (no existing file with same name)
- [ ] Filename follows: kebab-case-failure-mode.md
- [ ] Search codebase for similar phrase in 5-word window
  ```bash
  grep -r "hallucinated tool\|tool hallucination" agents/
  # Should return only THIS new pattern
  ```

---

## PRACTICAL DEDUPLICATION WORKFLOW

### Pre-Authorship (5 minutes per pattern)

**STEP 1: Identify failure mechanism**
```
Source: arXiv:2509.15435 (ORCA)
Failure: Vision models fail at grid cell counting for specific cell sizes
Mechanism: Patch tokenization hides visual boundaries
```

**STEP 2: Search for existing patterns with this mechanism**
```bash
grep -r "patch tokenization\|tokenization boundary\|visual boundary" agents/
grep -r "grid.*count\|counting task" agents/
```

Result: No existing patterns → Proceed

**STEP 3: Check category placement**
```bash
ls agents/by-capability/vision-and-images/goals/*/failures/ | wc -l
# 18 existing vision patterns

grep -r "hallucination" agents/by-capability/vision-and-images/goals/*/failures/ | wc -l
# 8 hallucination patterns (but none about patch tokenization)

# Placement: agents/by-capability/vision-and-images/goals/visual-hallucination/failures/
```

**STEP 4: Complete validation checklist** (8 subsections above)

**STEP 5: Write pattern file**

**STEP 6: Add cross-references**
```markdown
## Related Patterns
- [Confident Fabrication](../../../cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md) — Hallucination mechanism (different domain)
- [Vision Model Confidence Miscalibration](./vision-hallucination-confidence-miscalibration.md) — Related VLM failure
```

---

## AUTOMATED DEDUPLICATION CHECKS

### Pre-Commit Hook (Optional)

Save as `.claude/settings.json` or add to hooks:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "command",
        "command": "grep -r \"$(grep '## Issue' $FILE | head -1 | sed 's/## Issue: //')\" agents/ --include='*.md' | grep -v \"$FILE\" | wc -l",
        "statusMessage": "Checking for duplicate Issue statements..."
      }]
    }]
  }
}
```

**If output > 0**: Pattern likely duplicates existing. Review similar patterns.

---

## CONSOLIDATION TRIGGERS

### Auto-Consolidate If:
- [ ] Two patterns share identical "Root Cause" explanation
- [ ] Two patterns have identical "Issue" statement in different domains
- [ ] Two patterns document same mechanism with <10% variation in examples
- [ ] One pattern is clearly a subspecialization (same mechanism, narrower scope)

### How to Consolidate:
1. Keep parent pattern in highest-priority category (cross-cutting > by-capability > by-use-case)
2. Delete domain-specific duplicate file
3. Add example to parent pattern's Examples section
4. Link from domain README to parent pattern
5. Commit message: "Consolidate [pattern-name]: Move [domain] variant to [category]"

---

## DEDUPLICATION AUDIT (POST-AUTHORSHIP)

After completing a batch of new patterns:

```bash
# Find patterns with identical root causes
for file in agents/*/goals/*/failures/*.md; do
  root_cause=$(grep "Root Cause" "$file" | head -1)
  echo "$root_cause" >> /tmp/rc_check.txt
done

sort /tmp/rc_check.txt | uniq -d
# Shows duplicate root causes

# Find patterns with overlapping symptoms
grep -h "## Symptoms" agents/*/goals/*/failures/*.md | sort | uniq -c | awk '$1 > 1'
```

**Quarterly audit**: Run deduplication checks after each 50+ pattern batch.

---

## SPECIAL CASE: DOMAIN VARIANTS

### When IS it OK to Have Domain-Specific Variants?

**YES, create separate patterns if**:
- Mechanism is IDENTICAL, but mitigation is domain-specific
- Example: "Hallucinated legal case" vs "Hallucinated medical treatment"
  - Root cause: Same (confidence > accuracy)
  - Mitigation: Different (legal database verification vs medical literature search)
  - Pattern placement: Keep separate in respective domain directories
  - Link: Both link to parent "Confident Fabrication" in cross-cutting

**NO, don't create separate patterns if**:
- Mechanism is identical AND mitigation is identical (just different nouns)
- Example: "Hallucinated mortgage deadline" vs "Hallucinated employment deadline"
  - Root cause: Same
  - Mitigation: Same (verify against authoritative source)
  - Pattern placement: CONSOLIDATE to single cross-cutting pattern
  - Reason: No unique value; same mitigation applies everywhere

---

## EXAMPLE: AUDIT THIS SCENARIO

**New Source**: arXiv:2605.29442 (How Coding Agents Fail Their Users)

**Proposed Pattern**: "Code verification bottleneck: time saved writing code re-spent auditing it"

**Deduplication Check**:

1. **Search existing for "verification"**:
   ```bash
   grep -r "verification\|verify" agents/by-use-case/code-generation/goals/*/failures/ | head
   # Result: No patterns about verification bottleneck
   ```

2. **Search cross-cutting for similar**:
   ```bash
   grep -r "bottleneck\|tradeoff" agents/cross-cutting/
   # Result: No similar cross-cutting patterns
   ```

3. **Check if it's subspecialization**:
   - Could this be "time-accuracy tradeoff"? 
   - No—it's specific to verification becoming the bottleneck, not general tradeoff
   - Proceed with new pattern

4. **Validate placement**:
   - Domain-specific to code generation
   - Mitigation unique to code (automated testing, type checking, linting)
   - Placement: agents/by-use-case/code-generation/goals/code-quality/failures/

5. **Complete checklist** → Write pattern

---

## TRACKING & MONITORING

### Pattern Inventory (Run Monthly)

```bash
# Total patterns by category
find agents/cross-cutting -name "*.md" -path "*/failures/*" | wc -l  # Cross-cutting count
find agents/by-capability -name "*.md" -path "*/failures/*" | wc -l  # By-capability count
find agents/by-use-case -name "*.md" -path "*/failures/*" | wc -l    # By-use-case count
```

### Consolidation Opportunities (Run Quarterly)

```bash
# Find patterns with IDENTICAL root causes (consolidation candidates)
awk '/^# [A-Za-z]/ { pattern=$0 } /Root Cause/ { print pattern ": " $0 }' agents/*/goals/*/failures/*.md | sort | uniq -d
```

### Duplicate Patterns (Alert on)

```bash
# Find files with near-identical content (>90% similarity)
# Use: diff -u pattern1.md pattern2.md | wc -l
# If < 20 lines diff: likely duplicate
```

---

## APPROVAL CHECKLIST FOR NEW BATCHES

Before committing a batch of new patterns (50+):

- [ ] All patterns pass pre-authorship validation checklist
- [ ] No patterns share identical root causes
- [ ] Cross-references are bidirectional (no orphaned patterns)
- [ ] Domain placement follows hierarchy (cross-cutting first rule applied)
- [ ] All sources are cited (arXiv ID or URL)
- [ ] No patterns have template placeholders ([Add ...])
- [ ] README files updated with new pattern counts
- [ ] Quarterly deduplication audit passed

---

## VERSION HISTORY

| Version | Date | Changes |
|---|---|---|
| 1.0 | Jul 2026 | Initial protocol; 4-layer validation; audit templates |

