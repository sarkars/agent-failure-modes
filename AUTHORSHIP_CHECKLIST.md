# Pattern Authorship Quick Checklist

**Print this and check off as you author each pattern**

---

## BEFORE YOU START WRITING

### ✅ Deduplication Check (5 min)
- [ ] Run: `./check-duplicates.sh "your-pattern-name"`
- [ ] Result is GREEN (low risk) or YELLOW (review only)
- [ ] If RED: Stop, consolidate to existing pattern instead
- [ ] Searched for similar patterns manually in:
  - [ ] agents/cross-cutting/ (most likely place)
  - [ ] agents/by-capability/[relevant-capability]/
  - [ ] agents/by-use-case/[domain]/

### ✅ Source Validation (2 min)
- [ ] Source is from 2023-2026 (recency)
- [ ] Source is academic (arXiv/conference) OR production incident
- [ ] Source explicitly documents this failure
- [ ] Have arXiv ID or URL ready to cite

### ✅ Mechanism Clarity (3 min)
- [ ] Can describe root cause in ONE sentence
- [ ] Root cause is mechanistic (not behavioral description)
- [ ] Root cause differs from ≥3 related existing patterns
- [ ] Mitigation would be different from related patterns

### ✅ Category Placement (2 min)
- [ ] Applies to ALL agents? → **cross-cutting**
- [ ] Specific to agent capability (RAG, vision, etc.)? → **by-capability**
- [ ] Specific to domain/industry? → **by-use-case**
- [ ] Category directory exists (checked via `ls agents/[category]/goals/`)

---

## WHILE WRITING THE PATTERN FILE

### Issue Section
```markdown
## Issue: [Clear, specific failure description]
```
- [ ] Written as observable agent behavior (not root cause)
- [ ] Specific enough that someone could recognize it
- [ ] <50 words

**Example**: ✅ "Agent suggests option already ruled out earlier in conversation"  
**NOT**: ❌ "Agent forgets constraints"

---

### Frequency Section
```markdown
**Frequency**: [Common|Uncommon|Rare]
```
- [ ] Based on data/research (not guess)
- [ ] Source cites this pattern

---

### Symptoms Section
```markdown
## Symptoms
- Concrete, observable behaviors only
- No "the agent thinks..." (internal states)
- Verifiable by monitoring/logging
```
- [ ] ≥3 specific symptoms
- [ ] Each is verifiable in production
- [ ] No placeholder text

---

### Root Cause Section
```markdown
## Root Cause
[One paragraph explaining WHY, grounded in mechanism]
```
- [ ] Explains mechanism (not just "model limitation")
- [ ] Grounded in research/source
- [ ] One sentence summary at end
- [ ] Different from related patterns' root causes

---

### Examples Section
```markdown
## Examples

### [Domain 1]
```
- [ ] ≥3 concrete examples (real or realistic)
- [ ] From different domains if applicable
- [ ] Each shows: input → agent action → wrong output
- [ ] Each has expected outcome
- [ ] Each has business impact

---

### Key Statistics Section
```markdown
## Key Statistics
| Finding | Source |
|---|---|
```
- [ ] ≥2 statistics from source
- [ ] Cites arXiv ID or report
- [ ] Numbers grounded in research (not speculation)

---

### Mitigation Strategies Section
```markdown
## Mitigation Strategies

1. [Specific, actionable strategy]
```
- [ ] ≥3 mitigation strategies
- [ ] Each is specific (not "improve LLM")
- [ ] Each addresses root cause, not symptom
- [ ] Prioritized by feasibility/impact

---

### Metrics Section
```markdown
### Metrics
- % of X where Y occurs
```
- [ ] Measurable, not vague
- [ ] Connected to root cause
- [ ] Trackable via logs/monitoring

---

### Alerts Section
```markdown
### Alerts
- [Specific condition] → [Severity]
```
- [ ] ≥2 alert rules
- [ ] Trigger on observable conditions
- [ ] Severity (P1/P2/P3) justified

---

### References Section
```markdown
## References

- [Full Citation](URL or arXiv)
```
- [ ] ≥1 reference (source of pattern)
- [ ] Additional references for related work
- [ ] All URLs valid & accessible
- [ ] arXiv links in format: arxiv.org/abs/XXXX.XXXXX

---

## AFTER WRITING THE PATTERN FILE

### ✅ Template Compliance (3 min)
- [ ] File structure matches PATTERN_TEMPLATE.md
- [ ] All required sections present
- [ ] No placeholder text ([Add ...], [EXAMPLE], etc.)
- [ ] Markdown syntax valid (check with Markdown linter)

### ✅ Cross-References (5 min)
- [ ] Added section: "## Related Patterns"
- [ ] ≥2 links to related patterns
- [ ] Links use format: [title](../../path/to/pattern.md)
- [ ] All links tested (run `ls` to verify file exists)
- [ ] Update those related patterns to link back (bidirectional)

### ✅ File Naming (1 min)
- [ ] Filename is kebab-case
- [ ] Filename matches pattern title (roughly)
- [ ] No spaces or special chars except hyphens
- [ ] Length <60 chars
- [ ] Not already used (check: `ls agents/*/goals/*/failures/ | grep filename`)

**Examples**:
- ✅ `tool-selection-hallucination.md`
- ✅ `memory-poisoning-attack-success.md`
- ❌ `Tool Selection Hallucination.md` (spaces)
- ❌ `hallucination-in-tool-selection.md` (redundant vs directory context)

### ✅ Placement Verification (2 min)
- [ ] File location follows category/goal/failures pattern
- [ ] Directory path is: `agents/[cross-cutting|by-capability|by-use-case]/[category]/goals/[goal]/failures/[pattern].md`
- [ ] Directory structure exists (created if needed)
- [ ] Goal's README.md mentions new pattern

### ✅ Goal README Update (3 min)
- [ ] Goal README exists at `goals/[goal]/README.md`
- [ ] Added entry to pattern table:
  ```markdown
  | [Pattern Title](failures/pattern-filename.md) | Brief description | Issue number |
  ```
- [ ] Table is sorted (alphabetically or by severity)

### ✅ Source Citation (2 min)
- [ ] Pattern cites source clearly
- [ ] Source appears in References section
- [ ] Source is specific (arXiv:XXXX.XXXXX, not just "arXiv")
- [ ] If from blog/report: full URL, not shortened

### ✅ Category README Update (3 min)
- [ ] Category README exists at `agents/[category]/README.md`
- [ ] Category-level pattern count updated
- [ ] New pattern added to table (if category uses table)

---

## DEDUPLICATION FINAL GATE (5 min)

Run this check before committing:

```bash
# 1. Check filename uniqueness
ls agents/*/goals/*/failures/ | sort | uniq -d | grep "your-pattern-name"
# Should return: EMPTY (no duplicates)

# 2. Check for identical Issues (catch exact duplicates)
grep -r "^## Issue: " agents/ --include="*.md" | grep -i "your pattern keywords" | wc -l
# Should return: 1 (only yours)

# 3. Check for identical Root Causes (catch mechanism duplicates)
grep -r "Root Cause" agents/ -A 2 --include="*.md" | grep -i "your root cause keywords" | wc -l
# Should return: < 3 (if >3, likely consolidation needed)
```

If any check fails → **STOP, review consolidation rules**

---

## BATCH CHECKLIST (Before Committing 50+ Patterns)

Run AFTER completing a batch:

- [ ] All patterns pass individual checklists above
- [ ] No duplicate filenames (run: `ls agents/*/goals/*/failures/ | sort | uniq -d`)
- [ ] Cross-references complete (every pattern has ≥2 outbound, ≥1 inbound)
- [ ] Pattern counts updated in all README files
- [ ] README tables sorted consistently
- [ ] No [Placeholder] text anywhere (run: `grep -r "\[Add\|TODO\|FIXME" agents/`)
- [ ] All links valid (run script: `verify-links.sh`)
- [ ] Commit message follows format: "Add [count] new patterns: [categories]"

**Example commit message**:
```
Add 42 new patterns: vision hallucination (12), multi-agent coordination (15), code generation (15)

- Vision: patch tokenization, counting failures (arXiv:2509.15435)
- Multi-agent: error propagation, consensus collapse (arXiv:2503.13657)
- Code: security regression, verification bottleneck (arXiv:2605.29442)
```

---

## CONSOLIDATION DECISION (If You Hit Duplicate)

**If dedup check shows existing pattern:**

### Option A: Consolidate (Pattern is subspecialization)
```bash
# Example: Your "mortgage FHA hallucination" is subspecialization of "confident fabrication"

# Step 1: Add example to existing pattern
# Edit: agents/cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md
# Add under Examples section:
# ### Mortgage Lending - FHA Limit Hallucination
# [Your example]

# Step 2: Link from domain to parent
# Add to: agents/by-use-case/mortgage/goals/compliance/README.md
# "See [Confident Fabrication](../../../cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md) for hallucination patterns"

# Step 3: Commit
git commit -m "Consolidate mortgage FHA hallucination: add example to confident-fabrication pattern"
```

### Option B: Create Specialized Variant (Different mitigation)
```bash
# Example: "Legal case hallucination" vs "Medical treatment hallucination"
# Same root cause (confidence > accuracy), but DIFFERENT mitigation (legal DB vs medical literature)

# Step 1: Create domain-specific pattern in use-case directory
# File: agents/by-use-case/legal/goals/research-accuracy/failures/hallucinated-case-citation.md

# Step 2: Link to parent
# Add to References: [Confident Fabrication](../../../cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md)

# Step 3: Add parent cross-reference back
# Edit parent pattern, add: "Domain-specific variants: [Legal](path), [Healthcare](path)"

# Step 4: Commit
git commit -m "Add legal-specific case hallucination pattern (consolidates to confident-fabrication for mechanism)"
```

---

## QUALITY ASSURANCE SIGN-OFF

Before marking pattern complete, verify:

- [ ] **Semantic**: Pattern mechanism is unique or clearly specialized
- [ ] **Sourced**: Grounded in research/production incident, not speculation
- [ ] **Structured**: Follows PATTERN_TEMPLATE.md exactly
- [ ] **Discoverable**: Cross-referenced, linked, indexed
- [ ] **Production-Ready**: Mitigation is actionable, metrics are measurable
- [ ] **Not Duplicate**: Passed all dedup checks

---

## EXAMPLE: COMPLETE AUTHORSHIP FLOW

**Source**: arXiv:2605.29442 (Coding Agents Fail Users)  
**Topic**: Code verification bottleneck

### 1. Deduplication Check
```bash
./check-duplicates.sh "code verification bottleneck" "verification time tradeoff"
# Result: GREEN (no duplicates)
```

### 2. Write Pattern File
- File: `agents/by-use-case/code-generation/goals/code-quality/failures/code-verification-bottleneck.md`
- Issue: "Verification phase consumes time saved during generation; net productivity loss"
- Root Cause: "Manual code audit required to catch logic bugs; testing insufficient"

### 3. Add Examples
- Example 1: Security finding in generated code
- Example 2: Logic bug in generated function
- Example 3: Dependency conflict not caught by linter

### 4. Cross-Reference
- Links to: [Code Security Regression](./code-generation-security-regression.md)
- Links to: [Confident Fabrication](../../../cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md)
- Update those patterns to link back

### 5. Category Update
- Update: `agents/by-use-case/code-generation/goals/code-quality/README.md` (add to table)
- Update: `agents/by-use-case/code-generation/README.md` (increment pattern count)

### 6. Validation Checklist
- ✅ Dedup green
- ✅ Template complete
- ✅ Cross-references bidirectional
- ✅ Sources cited
- ✅ Production signals defined

### 7. Commit
```bash
git add agents/by-use-case/code-generation/
git commit -m "Add code-verification-bottleneck pattern (arXiv:2605.29442)"
```

Done! ✅

---

## QUICK REFERENCE TABLE

| Task | Time | Command/Tool |
|---|---|---|
| Check duplicates | 5 min | `./check-duplicates.sh "name" "keywords"` |
| Validate pattern | 15 min | Check template against PATTERN_TEMPLATE.md |
| Find related patterns | 5 min | `grep -r "Root Cause" agents/` |
| Update counts | 3 min | `find agents -name "failures/*.md" \| wc -l` |
| Test links | 2 min | `verify-links.sh` (create if needed) |
| Batch check | 10 min | Run all validation checks on 50+ patterns |

---

## WHEN IN DOUBT

❓ **"Should I consolidate or create new?"**  
→ Different mitigation = create new; same mitigation = consolidate

❓ **"Which category?"**  
→ Cross-cutting first (applies to all?), then by-capability (design pattern?), then by-use-case (domain-specific?)

❓ **"Is my pattern too specific?"**  
→ If subspecialization of existing (same mechanism, narrower scope) = add as example to parent

❓ **"Found an existing pattern; what now?"**  
→ If same mechanism: link or consolidate. If different mechanism: both can coexist (with bidirectional links)

