# Property Value Extraction Failures

## Issue: OCR System Incorrectly Extracts Property Values from Appraisals

**Frequency**: Common

**Symptoms**
- Appraised value vs. purchase price confusion
- As-is vs. subject-to value extraction errors
- Comparable sale prices incorrectly extracted
- Adjustment grid errors
- Land vs. improvement value confusion
- Multiple value opinions not distinguished

**Root Cause**
Appraisals contain multiple value figures—appraised value, contract price, comparable sales, land value, improvement value, and conditional values. OCR may extract the wrong value, confuse value types, or miss adjustments. Incorrect values affect LTV calculations and loan eligibility.

**Example**
```
Scenario 1: As-is vs. subject-to confusion

Appraisal shows:
- As-Is Value: $350,000
- Subject-To Completion: $425,000
- Property: Under construction

OCR: Extracted $425,000 as appraised value
Correct: $350,000 (as-is) until construction complete

← Wrong value for LTV calculation
← Over-lending risk
← Property not yet worth $425,000

---

Scenario 2: Comparable extraction error

Comparable sale grid:
- Comp 1: $380,000 sale, -$10,000 adjustment = $370,000
- Comp 2: $365,000 sale, +$15,000 adjustment = $380,000
- Comp 3: $390,000 sale, -$5,000 adjustment = $385,000

OCR: Extracted unadjusted prices
Should extract: Adjusted values for analysis

← Adjustments are critical for valuation
← Unadjusted values misleading

---

Scenario 3: Land/improvement split

Appraisal cost approach:
- Land value: $100,000
- Improvement value: $300,000
- Total: $400,000

OCR: Extracted $400,000 total only
Missing: Land/improvement breakdown

← Some loans require this split
← Cost approach analysis incomplete

---

Scenario 4: Multiple appraisals

File contains:
- Original appraisal: $380,000 (expired)
- Recertification: $385,000 (current)
- Prior appraisal (different property): $425,000

OCR: Extracted $425,000 (highest value)
Correct: $385,000 (current, subject property)

← Wrong appraisal selected
← Different property value extracted

---

Property value extraction failures:
  
  Documents with value issues: 10%
  
  Issue types:
    Value type confusion: 35%
    Comparable extraction errors: 25%
    Multiple appraisal confusion: 20%
    Land/improvement split missing: 12%
    Adjustment grid errors: 8%
  
  Impact:
    LTV miscalculation: 8%
    Over-lending risk: 3%
    Re-appraisal required: 5%
```

**Key Statistics**
From Appraisal Analysis Research (2026):
- Value extraction errors: 8-12%
- As-is/subject-to confusion: 5-8%
- Comparable adjustment errors: 10-15%
- LTV impact: 5-8%

**Contributing Factors**
- Multiple value fields on appraisal
- As-is vs. conditional values
- Comparable adjustment complexity
- Multiple appraisals in file
- Form version variations

---

## Mitigation Strategies

### Prevention
1. **Value type identification**: Distinguish as-is, subject-to, etc.
2. **Comparable extraction**: Include adjustments
3. **Document correlation**: Match appraisal to subject property
4. **Form parsing**: Handle different appraisal form types
5. **Current document selection**: Use most recent valid appraisal

### Implementation
```python
class AppraisalValueExtractor:
    """Extract property values from appraisals"""
    
    VALUE_TYPES = ["as_is", "subject_to_completion", "subject_to_repairs"]
    
    def extract_values(self, appraisal: dict) -> dict:
        """Extract all value types from appraisal"""
        values = {}
        
        # Primary value (as-is)
        values["as_is"] = appraisal.get("opinion_of_value")
        
        # Conditional values
        if appraisal.get("subject_to"):
            values["subject_to"] = {
                "value": appraisal["subject_to_value"],
                "condition": appraisal["subject_to_condition"]
            }
        
        # Cost approach breakdown
        values["cost_approach"] = {
            "land": appraisal.get("land_value"),
            "improvements": appraisal.get("improvement_value"),
            "total": appraisal.get("cost_approach_total")
        }
        
        # Sales comparison
        values["sales_comparison"] = appraisal.get("sales_comparison_value")
        
        return values
    
    def extract_comparables(self, appraisal: dict) -> list:
        """Extract comparable sales with adjustments"""
        comps = []
        
        for comp in appraisal.get("comparables", []):
            comps.append({
                "address": comp["address"],
                "sale_price": comp["sale_price"],
                "adjustments": comp.get("adjustments", {}),
                "adjusted_price": self.calculate_adjusted(comp),
                "sale_date": comp.get("sale_date"),
                "proximity": comp.get("distance_from_subject")
            })
        
        return comps
    
    def determine_applicable_value(self, 
                                   appraisal: dict,
                                   property_status: str) -> dict:
        """Determine which value applies for underwriting"""
        if property_status == "existing":
            return {
                "applicable_value": appraisal.get("as_is_value"),
                "value_type": "as_is"
            }
        
        if property_status == "under_construction":
            return {
                "applicable_value": appraisal.get("as_is_value"),
                "value_type": "as_is",
                "note": "Use as-is until construction complete"
            }
        
        if property_status == "proposed":
            return {
                "applicable_value": appraisal.get("subject_to_value"),
                "value_type": "subject_to_completion"
            }
        
        return {"error": "Unable to determine applicable value"}
```

---

## References

- [USPAP Standards](https://www.appraisalfoundation.org/) - Appraisal standards
- [Fannie Mae B4-1](https://selling-guide.fanniemae.com/) - Appraisal requirements
- [FHA Appraisal Guidelines](https://www.hud.gov/program_offices/housing/sfh) - FHA requirements
