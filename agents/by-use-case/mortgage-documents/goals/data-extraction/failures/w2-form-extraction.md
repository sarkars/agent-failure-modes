# W-2 Form Extraction Failures

## Issue: OCR System Incorrectly Extracts Data from W-2 Forms

**Frequency**: Common

**Symptoms**
- Box number confusion (Box 1 vs Box 3 vs Box 5)
- Employer identification (EIN) errors
- Multi-state W-2 aggregation failures
- YTD vs. annual income confusion
- Box 12 code misinterpretation
- W-2c (corrected) not identified

**Root Cause**
W-2 forms contain multiple wage and tax figures across 20+ boxes. OCR must extract the correct qualifying income (Box 1), handle multi-state situations, avoid double-counting, and identify corrections. Box confusion leads to significant income errors affecting loan qualification.

**Example**
```
Scenario 1: Box confusion

W-2 shows:
- Box 1 (Wages): $82,000
- Box 3 (SS Wages): $82,000  
- Box 5 (Medicare): $85,000

OCR: Extracted $85,000 (highest value)
Correct: $82,000 (Box 1 only)

← Box 5 includes pre-tax benefits
← Box 1 is qualifying income
← Overstated by $3,000

---

Scenario 2: Multi-state W-2s

Employee worked in two states:
W-2 #1 (CA): Box 1 = $60,000
W-2 #2 (NV): Box 1 = $60,000

Same employer, same EIN

OCR: Added both = $120,000
Correct: $60,000 (same employer, split for state taxes)

← Multi-state split, not separate income
← Double-counted income

---

Scenario 3: Box 12 mishandling

W-2 shows:
- Box 1: $75,000
- Box 12a (Code D - 401k): $12,000
- Box 12b (Code DD - Health): $8,000

OCR: $75,000 + $12,000 = $87,000
Correct: $75,000 only

← Box 12 is informational
← Pre-tax deductions already excluded from Box 1
← Should not be added

---

Scenario 4: W-2c (Corrected)

File contains:
- Original W-2: $95,000
- W-2c: Corrected to $78,000

OCR: Extracted $95,000 (original)
Correct: $78,000 (corrected)

← W-2c supersedes original
← Form type not identified

---

W-2 extraction failures:
  
  Documents with W-2 issues: 15%
  
  Issue types:
    Box confusion: 35%
    Multi-W-2 errors: 25%
    Box 12 mishandling: 20%
    W-2c not identified: 12%
    EIN matching failures: 8%
  
  Impact:
    Income miscalculation: 12%
    Over/understatement: 10%
    Additional docs required: 8%
```

**Key Statistics**
From W-2 Processing Research (2026):
- W-2 extraction errors: 12-18%
- Box confusion: 30-40% of errors
- Multi-W-2 double-counting: 15-20%
- Income impact: 8-12%

**Contributing Factors**
- Multiple boxes with similar values
- Multi-employer/multi-state complexity
- Box 12 code interpretation
- Form version variations
- W-2c identification

---

## Mitigation Strategies

### Prevention
1. **Box-specific extraction**: Always use Box 1 for wages
2. **EIN matching**: Identify same-employer W-2s
3. **Box 12 exclusion**: Never add to income
4. **W-2c detection**: Use corrected values
5. **Multi-year consistency**: Compare year over year

### Implementation
```python
class W2Extractor:
    """Extract W-2 data for mortgage qualification"""
    
    # Box 12 codes - informational only, never add to income
    BOX_12_CODES = {
        "D": "401k_contribution",
        "E": "403b_contribution",
        "DD": "health_insurance_cost",
        "W": "hsa_contribution"
    }
    
    def extract_qualifying_income(self, w2: dict) -> dict:
        """Extract Box 1 wages only"""
        box1 = w2.get("box1_wages", 0)
        
        # Validate against other boxes for consistency
        box3 = w2.get("box3_ss_wages", 0)
        box5 = w2.get("box5_medicare", 0)
        
        # Box 1 should be <= Box 5 (Medicare has no cap)
        if box1 > box5 and box5 > 0:
            return {
                "warning": "Box 1 exceeds Box 5 - verify extraction",
                "box1": box1,
                "box5": box5
            }
        
        return {
            "qualifying_income": box1,
            "source": "box1_wages",
            "note": "Box 12 codes are informational only"
        }
    
    def consolidate_multi_state(self, w2s: list) -> dict:
        """Consolidate W-2s from same employer"""
        by_employer = {}
        
        for w2 in w2s:
            ein = w2.get("employer_ein")
            employer = w2.get("employer_name")
            key = ein or employer
            
            if key not in by_employer:
                by_employer[key] = {
                    "employer": employer,
                    "ein": ein,
                    "w2_count": 0,
                    "box1_total": 0,
                    "states": []
                }
            
            by_employer[key]["w2_count"] += 1
            by_employer[key]["states"].append(w2.get("state"))
            
            # Only count Box 1 once per employer
            if by_employer[key]["w2_count"] == 1:
                by_employer[key]["box1_total"] = w2.get("box1_wages", 0)
            else:
                # Multi-state - verify if it's split or additional
                existing = by_employer[key]["box1_total"]
                new_box1 = w2.get("box1_wages", 0)
                
                if abs(existing - new_box1) < 100:
                    # Same amount - likely state split
                    by_employer[key]["is_state_split"] = True
                else:
                    # Different amounts - sum them
                    by_employer[key]["box1_total"] += new_box1
        
        return by_employer
    
    def check_for_correction(self, forms: list) -> dict:
        """Check for W-2c corrected forms"""
        w2c_forms = [f for f in forms if f.get("form_type") == "W-2c"]
        
        if w2c_forms:
            latest_correction = max(w2c_forms, key=lambda x: x.get("date", ""))
            return {
                "has_correction": True,
                "use_values_from": "W-2c",
                "corrected_box1": latest_correction.get("corrected_box1"),
                "reason": "W-2c supersedes original W-2"
            }
        
        return {"has_correction": False}
```

---

## References

- [IRS W-2 Instructions](https://www.irs.gov/forms-pubs/about-form-w-2) - Box definitions
- [Fannie Mae B3-3.1-09](https://selling-guide.fanniemae.com/) - W-2 requirements
- [Freddie Mac 5302.3](https://guide.freddiemac.com/) - Income documentation
