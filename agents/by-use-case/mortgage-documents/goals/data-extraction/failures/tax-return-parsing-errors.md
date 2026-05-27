# Tax Return Parsing Errors

## Issue: OCR System Incorrectly Extracts Data from Tax Returns

**Frequency**: Common

**Symptoms**
- Schedule income types confused
- Multi-year averaging errors
- Loss carryforward miscalculated
- K-1 income attribution wrong
- Amended return not identified
- Tax transcript vs. return mismatch

**Root Cause**
Tax returns contain complex, multi-schedule income information. OCR must navigate 1040s with multiple schedules (C, E, K-1, etc.), understand income categories, calculate multi-year averages, and handle losses. Errors directly impact income qualification and loan eligibility.

**Example**
```
Scenario 1: Schedule E loss handling

Schedule E shows:
- Rental property 1: +$12,000 income
- Rental property 2: -$8,000 loss
- Net Schedule E: +$4,000

OCR: Extracted $12,000 (first property only)
Reality: Net $4,000 qualifies

← Losses must be netted
← Overstated rental income by $8,000

---

Scenario 2: K-1 income attribution

K-1 from S-Corp shows:
- Ordinary business income: $85,000
- Distributions: $120,000
- Borrower ownership: 50%

OCR: Extracted $120,000 distributions
Reality: Only $42,500 qualifies (50% of ordinary income)

← Distributions ≠ income
← Ownership percentage not applied

---

Scenario 3: Declining self-employment

Schedule C (2024): $95,000
Schedule C (2025): $65,000
Decline: 32%

Guideline: If declining > 20%, use lower year
OCR: Averaged ($80,000)
Correct: Use $65,000 (declining trend)

---

Scenario 4: Amended return

1040 shows: AGI $120,000
1040-X (amended): AGI $85,000
Filing date: 1040-X filed after 1040

OCR: Extracted $120,000 from original
Correct: $85,000 from amended return

← Amended return supersedes original
← OCR didn't identify amendment

---

Tax return parsing failures:
  
  Documents with tax issues: 20%
  
  Issue types:
    Schedule netting errors: 30%
    K-1 misattribution: 20%
    Declining income handling: 18%
    Multi-year averaging: 15%
    Amended returns missed: 10%
    Loss carryforward: 7%
  
  Impact:
    Income miscalculation: 15%
    Qualification impact: 8%
    Re-documentation: 12%
```

**Key Statistics**
From Tax Document Analysis (2026):
- Tax return extraction errors: 15-25%
- Schedule-related errors: 30-40% of tax issues
- K-1 errors: 15-20%
- Impact on qualification: 8-12%

**Contributing Factors**
- Multi-schedule complexity
- Loss netting rules
- Ownership percentage application
- Amended return identification
- Year-over-year trend analysis missing

---

## Mitigation Strategies

### Prevention
1. **Schedule aggregation**: Net all related schedules
2. **K-1 ownership**: Apply ownership percentage
3. **Trend analysis**: Detect declining income
4. **Amendment detection**: Identify and use 1040-X
5. **Multi-year averaging**: Proper calculation

### Implementation
```python
class TaxReturnParser:
    """Parse tax returns for mortgage qualification"""
    
    DECLINE_THRESHOLD = 0.20  # 20% decline triggers lower year
    
    def calculate_schedule_e_income(self, schedule_e: dict) -> dict:
        """Calculate net Schedule E rental income"""
        properties = schedule_e.get("properties", [])
        
        total_income = 0
        total_expenses = 0
        total_depreciation = 0
        
        for prop in properties:
            total_income += prop.get("gross_rent", 0)
            total_expenses += prop.get("total_expenses", 0)
            total_depreciation += prop.get("depreciation", 0)
        
        net_income = total_income - total_expenses
        
        # Add back depreciation for cash flow
        qualifying_income = net_income + total_depreciation
        
        return {
            "gross_rents": total_income,
            "total_expenses": total_expenses,
            "net_income": net_income,
            "depreciation_addback": total_depreciation,
            "qualifying_income": qualifying_income
        }
    
    def calculate_k1_income(self, k1: dict, ownership_pct: float) -> dict:
        """Calculate K-1 qualifying income"""
        # Only ordinary business income qualifies
        ordinary_income = k1.get("ordinary_business_income", 0)
        
        # Apply ownership percentage
        borrower_share = ordinary_income * ownership_pct
        
        return {
            "total_k1_income": ordinary_income,
            "ownership_percentage": ownership_pct,
            "borrower_qualifying_income": borrower_share,
            "note": "Distributions are NOT income"
        }
    
    def analyze_income_trend(self, 
                            year1_income: float,
                            year2_income: float) -> dict:
        """Analyze income trend for declining self-employment"""
        if year1_income <= 0:
            return {"trend": "unable_to_calculate"}
        
        change = (year2_income - year1_income) / year1_income
        
        if change < -self.DECLINE_THRESHOLD:
            return {
                "trend": "declining",
                "change_percentage": change * 100,
                "qualifying_income": year2_income,
                "method": "use_lower_year"
            }
        
        # Average if stable or increasing
        average = (year1_income + year2_income) / 2
        return {
            "trend": "stable_or_increasing",
            "change_percentage": change * 100,
            "qualifying_income": average,
            "method": "two_year_average"
        }
    
    def check_for_amendment(self, returns: list) -> dict:
        """Check for amended returns"""
        amendments = [r for r in returns if r.get("form") == "1040-X"]
        
        if amendments:
            latest_amendment = max(amendments, key=lambda x: x["filing_date"])
            return {
                "amended": True,
                "use_return": latest_amendment,
                "reason": "Amended return supersedes original"
            }
        
        return {"amended": False}
```

---

## References

- [IRS Form Instructions](https://www.irs.gov/forms-instructions) - Tax form guidance
- [Fannie Mae B3-3.2](https://selling-guide.fanniemae.com/) - Self-employment income
- [Freddie Mac 5304](https://guide.freddiemac.com/) - Tax return analysis
