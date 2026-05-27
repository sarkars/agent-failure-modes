# APR Calculation Errors

## Issue: OCR System Incorrectly Extracts or Validates APR Calculations

**Frequency**: Occasional but high regulatory risk

**Symptoms**
- Disclosed APR doesn't match calculated APR
- Finance charge components missed
- Prepaid interest calculation errors
- Points and fees not included
- Tolerance violations undetected
- Irregular payment handling failures

**Root Cause**
The Annual Percentage Rate (APR) must be calculated per Regulation Z and disclosed within tolerance (0.125% for regular, 0.25% for irregular transactions). OCR extracts the disclosed APR but doesn't validate the calculation against loan terms. Tolerance violations result in compliance findings and potential liability.

**Example**
```
Scenario 1: Missing finance charge

Disclosed on CD:
- APR: 5.875%
- Interest rate: 5.5%
- Loan amount: $300,000
- Points: $3,000 (1 point)

OCR: Extracted APR 5.875% ✓

Missing from APR calc:
- Mortgage insurance premium: $2,400/year
- Required escrow at closing: $1,200

Correct APR with all charges: 6.125%
Disclosed APR: 5.875%
Variance: 0.25%

← Exceeds 0.125% tolerance
← TILA violation

---

Scenario 2: Prepaid interest error

Loan details:
- Closing: March 15
- First payment: May 1
- Days of prepaid interest: 17

Disclosed: 15 days prepaid
Actual: 17 days

← 2 days prepaid interest missing from finance charge
← Affects APR calculation

---

Scenario 3: Irregular payment handling

Loan structure:
- Interest-only for 5 years
- Then fully amortizing for 25 years
- ARM with rate caps

Disclosed APR: 6.25%
Calculation requires: Composite rate methodology

OCR: Verified APR against simple calculation
Reality: Complex APR requires specialized calc

← Wrong APR methodology applied
← Tolerance 0.25% for irregular
← Still potentially out of tolerance

---

APR calculation failures:
  
  Documents with APR issues: 8%
  
  Issue types:
    Finance charge omissions: 35%
    Prepaid interest errors: 25%
    Tolerance violations: 20%
    Irregular payment handling: 12%
    Rounding errors: 8%
  
  Impact:
    TILA violations: 5%
    Rescission risk: 3%
    Regulatory penalties: Variable
```

**Key Statistics**
From Compliance Audit Research (2026):
- APR tolerance violations: 5-10%
- Finance charge omissions: 8-12%
- Irregular transaction errors: 15-20%
- Rescission claims (APR): 1-2%

**APR Tolerance Rules**
| Transaction Type | Tolerance |
|-----------------|-----------|
| Regular (fixed, monthly) | 0.125% |
| Irregular (ARM, I/O, balloon) | 0.25% |

**Contributing Factors**
- Finance charge components complex
- Prepaid interest calculation
- ARM composite rate methodology
- MI premium inclusion rules
- Rounding methodology differences

---

## Mitigation Strategies

### Prevention
1. **Finance charge extraction**: All Reg Z components
2. **APR recalculation**: Independent verification
3. **Tolerance checking**: Automated comparison
4. **Irregular transaction detection**: Flag for review
5. **Prepaid interest validation**: Day count verification

### Implementation
```python
class APRValidator:
    """Validate APR calculations"""
    
    REGULAR_TOLERANCE = 0.00125  # 0.125%
    IRREGULAR_TOLERANCE = 0.0025  # 0.25%
    
    FINANCE_CHARGE_COMPONENTS = [
        "interest",
        "points",
        "origination_fee",
        "mortgage_insurance",
        "prepaid_interest",
        "private_mortgage_insurance"
    ]
    
    def calculate_finance_charge(self, loan: dict) -> dict:
        """Calculate total finance charge per Reg Z"""
        components = {}
        
        # Interest over life of loan
        components["total_interest"] = self.calculate_total_interest(loan)
        
        # Points and fees
        components["points"] = loan.get("discount_points", 0)
        components["origination"] = loan.get("origination_fee", 0)
        
        # Mortgage insurance (if required for life of loan)
        if loan.get("pmi_required"):
            components["mortgage_insurance"] = self.calculate_mi_charge(loan)
        
        # Prepaid interest
        components["prepaid_interest"] = self.calculate_prepaid_interest(loan)
        
        total = sum(components.values())
        
        return {
            "components": components,
            "total_finance_charge": total
        }
    
    def calculate_apr(self, loan: dict) -> float:
        """Calculate APR per Reg Z methodology"""
        amount_financed = loan["loan_amount"] - loan.get("prepaid_finance_charges", 0)
        finance_charge = self.calculate_finance_charge(loan)["total_finance_charge"]
        
        # Use actuarial method for APR calculation
        # (Simplified - actual implementation uses iterative solving)
        
        return self.solve_for_apr(
            amount_financed=amount_financed,
            finance_charge=finance_charge,
            payment=loan["monthly_payment"],
            term=loan["term_months"]
        )
    
    def validate_disclosed_apr(self, 
                               disclosed_apr: float,
                               loan: dict) -> dict:
        """Validate disclosed APR is within tolerance"""
        calculated_apr = self.calculate_apr(loan)
        
        # Determine tolerance
        is_irregular = self.is_irregular_transaction(loan)
        tolerance = self.IRREGULAR_TOLERANCE if is_irregular else self.REGULAR_TOLERANCE
        
        variance = abs(disclosed_apr - calculated_apr)
        within_tolerance = variance <= tolerance
        
        return {
            "disclosed_apr": disclosed_apr,
            "calculated_apr": calculated_apr,
            "variance": variance,
            "tolerance": tolerance,
            "transaction_type": "irregular" if is_irregular else "regular",
            "within_tolerance": within_tolerance,
            "violation": not within_tolerance
        }
    
    def is_irregular_transaction(self, loan: dict) -> bool:
        """Determine if loan is irregular transaction"""
        # ARM loans
        if loan.get("is_arm"):
            return True
        
        # Interest-only
        if loan.get("interest_only_period"):
            return True
        
        # Balloon
        if loan.get("balloon_payment"):
            return True
        
        # Irregular payments
        if loan.get("payment_schedule") != "monthly":
            return True
        
        return False
```

---

## References

- [Regulation Z](https://www.consumerfinance.gov/rules-policy/regulations/1026/) - Truth in Lending
- [CFPB APR Calculation](https://www.consumerfinance.gov/rules-policy/regulations/1026/22/) - APR rules
- [Appendix J to Reg Z](https://www.consumerfinance.gov/rules-policy/regulations/1026/J/) - APR computation
