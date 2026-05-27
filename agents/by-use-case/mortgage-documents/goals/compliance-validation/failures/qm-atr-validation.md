# QM/ATR Validation Failures

## Issue: OCR System Fails to Validate Qualified Mortgage and Ability-to-Repay Compliance

**Frequency**: Occasional but high liability risk

**Symptoms**
- DTI limit violations not detected
- Points and fees limit exceeded
- ARM adjustment caps not verified
- Negative amortization not flagged
- Balloon payment terms missed
- Income/asset verification gaps

**Root Cause**
Qualified Mortgage (QM) and Ability-to-Repay (ATR) rules under Regulation Z require specific underwriting standards. OCR extracts loan data but doesn't validate against QM criteria—43% DTI limit, points/fees caps, prohibited features. Non-QM loans without proper ATR documentation create significant legal liability.

**Example**
```
Scenario 1: DTI limit exceeded

Loan approved as QM:
- Monthly income: $8,000
- Total monthly debt: $3,800
- DTI: 47.5%

QM requirement: DTI ≤ 43% (general QM)
or: Meets GSE standards (GSE QM)

OCR: Extracted income and debt ✓
Missing: QM DTI validation

← 47.5% exceeds general QM limit
← Not documented as GSE QM or non-QM
← Safe harbor protection lost

---

Scenario 2: Points and fees violation

Loan amount: $150,000
Points and fees charged:
- Origination: $2,500
- Discount points: $1,500
- Broker fee: $2,000
- Title insurance (connected): $1,200
Total: $7,200 (4.8% of loan)

QM limit: 3% for loans ≥ $100,000

OCR: Fees extracted ✓
Missing: Points and fees test

← 4.8% exceeds 3% limit
← Cannot be QM
← Requires non-QM documentation

---

Scenario 3: Prohibited loan feature

Loan terms:
- Interest-only for 10 years
- Negative amortization possible
- 40-year term

QM prohibits:
- Negative amortization
- Interest-only (mostly)
- Terms > 30 years

OCR: Extracted loan terms ✓
Missing: Prohibited feature validation

← Multiple QM violations
← Must be documented as non-QM
← Full ATR analysis required

---

Scenario 4: ARM adjustment caps

5/1 ARM terms:
- Initial rate: 4.5%
- First adjustment cap: 3%
- Periodic cap: 2%
- Lifetime cap: 8%

After first adjustment: Could be 7.5%
After subsequent: Could be 9.5%
Maximum possible: 12.5%

QM requirement: Underwrite at max rate in first 5 years

OCR: Extracted ARM terms ✓
Missing: Maximum rate calculation and underwriting validation

← Was borrower qualified at 7.5%?
← ATR requires this analysis

---

QM/ATR validation failures:
  
  Loans with QM/ATR issues: 8%
  
  Issue types:
    DTI violations: 30%
    Points and fees: 25%
    Prohibited features: 20%
    ARM underwriting: 15%
    Documentation gaps: 10%
  
  Impact:
    Safe harbor loss: 8%
    ATR liability: 5%
    Investor repurchase: 3%
```

**Key Statistics**
From QM Compliance Research (2026):
- QM compliance failures: 5-10%
- Points/fees violations: 3-5%
- DTI limit issues: 4-6%
- Non-QM documentation gaps: 10-15%

**QM Requirements**
| Criteria | General QM | GSE QM |
|----------|-----------|--------|
| DTI | ≤ 43% | Per GSE guidelines |
| Points & Fees | ≤ 3% (for loans ≥$100k) | Same |
| Term | ≤ 30 years | ≤ 30 years |
| Neg-Am | Prohibited | Prohibited |
| Interest-Only | Prohibited (mostly) | Prohibited |
| Balloon | Prohibited (mostly) | Prohibited |

**Contributing Factors**
- DTI calculation errors
- Points/fees components missed
- Loan feature validation absent
- ARM max rate not calculated
- QM type determination missing

---

## Mitigation Strategies

### Prevention
1. **DTI calculation**: Accurate with QM limits
2. **Points and fees test**: Include all components
3. **Feature validation**: Check for prohibited terms
4. **ARM underwriting**: Calculate max rate
5. **QM type determination**: General vs. GSE vs. non-QM

### Implementation
```python
class QMATRValidator:
    """Validate QM and ATR compliance"""
    
    GENERAL_QM_DTI_LIMIT = 0.43
    
    POINTS_FEES_LIMITS = {
        100000: 0.03,  # 3% for loans >= $100k
        60000: 0.05,   # 5% for $60k-$100k
        20000: 0.08,   # 8% for $20k-$60k
        12500: 1000,   # $1,000 for $12.5k-$20k
        0: 0.08        # 8% for < $12.5k
    }
    
    PROHIBITED_FEATURES = [
        "negative_amortization",
        "interest_only",
        "balloon_payment",
        "term_over_30_years"
    ]
    
    def validate_qm_status(self, loan: dict) -> dict:
        """Determine if loan meets QM requirements"""
        issues = []
        
        # Check DTI
        dti = loan.get("dti", 0)
        if dti > self.GENERAL_QM_DTI_LIMIT:
            issues.append({
                "test": "dti",
                "value": dti,
                "limit": self.GENERAL_QM_DTI_LIMIT,
                "status": "exceeds_general_qm"
            })
        
        # Check points and fees
        pf_result = self.check_points_and_fees(loan)
        if not pf_result["compliant"]:
            issues.append(pf_result)
        
        # Check prohibited features
        for feature in self.PROHIBITED_FEATURES:
            if loan.get(feature):
                issues.append({
                    "test": "prohibited_feature",
                    "feature": feature,
                    "status": "qm_prohibited"
                })
        
        # Check term
        if loan.get("term_months", 0) > 360:
            issues.append({
                "test": "term",
                "value": loan["term_months"],
                "limit": 360,
                "status": "exceeds_30_years"
            })
        
        is_qm = len(issues) == 0
        
        return {
            "qm_eligible": is_qm,
            "qm_type": "general" if is_qm else "non_qm",
            "issues": issues,
            "safe_harbor": is_qm,
            "atr_documentation_required": not is_qm
        }
    
    def check_points_and_fees(self, loan: dict) -> dict:
        """Check points and fees against QM limits"""
        loan_amount = loan.get("loan_amount", 0)
        
        # Determine applicable limit
        limit_pct = 0.03  # Default
        for threshold, pct in sorted(self.POINTS_FEES_LIMITS.items(), reverse=True):
            if loan_amount >= threshold:
                limit_pct = pct
                break
        
        # Calculate points and fees
        points_fees = self.calculate_points_and_fees(loan)
        
        if isinstance(limit_pct, float):
            limit_amount = loan_amount * limit_pct
        else:
            limit_amount = limit_pct
        
        return {
            "test": "points_and_fees",
            "amount": points_fees,
            "limit": limit_amount,
            "limit_pct": limit_pct if isinstance(limit_pct, float) else None,
            "compliant": points_fees <= limit_amount
        }
    
    def calculate_points_and_fees(self, loan: dict) -> float:
        """Calculate total points and fees for QM test"""
        components = [
            loan.get("origination_fee", 0),
            loan.get("discount_points", 0),
            loan.get("broker_fees", 0),
            loan.get("lender_paid_compensation", 0)
        ]
        
        # Certain title insurance if creditor affiliated
        if loan.get("affiliated_title"):
            components.append(loan.get("title_insurance", 0))
        
        return sum(components)
    
    def validate_arm_underwriting(self, loan: dict) -> dict:
        """Validate ARM loan underwritten at max rate"""
        if not loan.get("is_arm"):
            return {"applicable": False}
        
        initial_rate = loan.get("initial_rate")
        first_cap = loan.get("first_adjustment_cap")
        periodic_cap = loan.get("periodic_cap")
        lifetime_cap = loan.get("lifetime_cap")
        
        # Calculate max rate in first 5 years
        max_first_adjustment = initial_rate + first_cap
        
        # For QM, must underwrite at this rate
        underwritten_rate = loan.get("qualifying_rate")
        
        if underwritten_rate < max_first_adjustment:
            return {
                "applicable": True,
                "compliant": False,
                "initial_rate": initial_rate,
                "max_first_5_years": max_first_adjustment,
                "underwritten_at": underwritten_rate,
                "issue": "Not underwritten at maximum rate"
            }
        
        return {
            "applicable": True,
            "compliant": True,
            "max_rate_considered": max_first_adjustment
        }
```

---

## References

- [CFPB QM Rule](https://www.consumerfinance.gov/rules-policy/regulations/1026/43/) - Regulation Z §1026.43
- [ATR/QM Guidance](https://www.consumerfinance.gov/rules-policy/final-rules/ability-to-repay-and-qualified-mortgage-standards-under-the-truth-in-lending-act-regulation-z/) - CFPB final rule
- [GSE QM Patch](https://www.fanniemae.com/) - GSE underwriting standards
