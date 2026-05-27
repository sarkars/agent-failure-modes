# Debt Obligation Detection Failures

## Issue: OCR System Fails to Detect All Borrower Debt Obligations

**Frequency**: Common

**Symptoms**
- Credit report debts not fully extracted
- Co-signed debts missed
- Authorized user accounts counted incorrectly
- Alimony/child support obligations not identified
- Installment vs. revolving debt confusion
- Deferred debts (student loans) miscalculated

**Root Cause**
Debt-to-income (DTI) ratio requires accurate debt extraction from credit reports, applications, and supporting documents. OCR may miss debts, double-count obligations, misclassify debt types, or incorrectly handle special situations (co-signed, deferred, excluded). Errors lead to DTI miscalculation and improper qualification.

**Example**
```
Scenario 1: Student loan deferment

Credit report shows:
- Student loan balance: $45,000
- Payment status: "Deferred - In School"
- No monthly payment listed

OCR: Excluded from DTI (no payment)
Correct: Calculate 1% of balance = $450/month

← Deferred loans require imputed payment
← Fannie Mae rule: 1% of balance or IDR payment
← Understated monthly obligations

---

Scenario 2: Co-signed debt

Auto loan appears on borrower's credit:
- Balance: $28,000
- Payment: $550/month
- Account type: Joint

OCR: Included $550 in DTI
Reality: Borrower's child makes payments (12+ months proof)

← Could potentially be excluded
← OCR didn't flag for documentation
← May be overstating DTI

---

Scenario 3: Authorized user

Credit card on report:
- Account type: "Authorized User"
- Balance: $8,000
- Payment: $200/month

OCR: Included in DTI
Correct: Exclude - borrower not responsible

← Authorized users not liable
← Should be excluded from DTI
← Overstated debt obligations

---

Scenario 4: Alimony/child support

Application shows:
- Child support: $1,200/month (disclosed)
Credit report shows:
- No child support tradeline

OCR: No obligation detected from credit
Missing: $1,200/month from application

← Not all obligations on credit report
← Application data not correlated
← Understated DTI

---

Debt detection failures:
  
  Documents with debt issues: 22%
  
  Issue types:
    Deferred payment errors: 30%
    Co-signer handling: 20%
    Authorized user confusion: 15%
    Non-credit obligations: 15%
    Debt type misclassification: 12%
    Duplicate debt counting: 8%
  
  Impact:
    DTI miscalculation: 18%
    Qualification errors: 10%
    Re-underwriting required: 8%
```

**Key Statistics**
From DTI Analysis Research (2026):
- Debt extraction errors: 18-25%
- Student loan miscalculation: 25-35%
- Non-credit obligations missed: 15-20%
- DTI variance from errors: 2-5 points

**Contributing Factors**
- Deferred payment rules not implemented
- Co-signer exclusion criteria unknown
- Authorized user detection missing
- Application/credit correlation absent
- Installment debt categorization errors

---

## Mitigation Strategies

### Prevention
1. **Student loan calculation**: Apply 1% or IDR rule
2. **Account type detection**: AU, joint, individual
3. **Cross-document correlation**: Credit + application
4. **Payment status handling**: Deferred, forbearance, etc.
5. **Non-credit obligations**: Alimony, child support

### Implementation
```python
class DebtObligationExtractor:
    """Extract and calculate debt obligations"""
    
    STUDENT_LOAN_FACTOR = 0.01  # 1% of balance if no payment
    
    def extract_all_obligations(self, 
                               credit_report: dict,
                               application: dict) -> dict:
        """Extract all debt obligations"""
        obligations = []
        
        # Credit report debts
        for tradeline in credit_report.get("tradelines", []):
            obligation = self.process_tradeline(tradeline)
            if obligation:
                obligations.append(obligation)
        
        # Application-disclosed obligations
        for disclosed in application.get("other_obligations", []):
            obligations.append({
                "type": disclosed["type"],
                "payment": disclosed["monthly_payment"],
                "source": "application",
                "include_in_dti": True
            })
        
        return {
            "obligations": obligations,
            "total_monthly": sum(o["payment"] for o in obligations 
                               if o.get("include_in_dti")),
            "excluded_count": len([o for o in obligations 
                                  if not o.get("include_in_dti")])
        }
    
    def process_tradeline(self, tradeline: dict) -> dict:
        """Process individual tradeline for DTI"""
        account_type = tradeline.get("account_type", "")
        
        # Exclude authorized user accounts
        if "authorized user" in account_type.lower():
            return {
                "creditor": tradeline.get("creditor"),
                "balance": tradeline.get("balance"),
                "payment": 0,
                "include_in_dti": False,
                "exclusion_reason": "Authorized user - not liable"
            }
        
        # Handle student loans
        if self.is_student_loan(tradeline):
            return self.calculate_student_loan_payment(tradeline)
        
        # Standard debt
        return {
            "creditor": tradeline.get("creditor"),
            "balance": tradeline.get("balance"),
            "payment": tradeline.get("monthly_payment", 0),
            "type": tradeline.get("type"),
            "include_in_dti": True
        }
    
    def calculate_student_loan_payment(self, tradeline: dict) -> dict:
        """Calculate student loan payment for DTI"""
        balance = tradeline.get("balance", 0)
        reported_payment = tradeline.get("monthly_payment", 0)
        status = tradeline.get("status", "").lower()
        
        # If deferred or no payment, calculate 1%
        if status in ["deferred", "forbearance"] or reported_payment == 0:
            calculated_payment = balance * self.STUDENT_LOAN_FACTOR
            return {
                "creditor": tradeline.get("creditor"),
                "balance": balance,
                "payment": calculated_payment,
                "type": "student_loan",
                "include_in_dti": True,
                "calculation_method": "1% of balance (deferred)"
            }
        
        return {
            "creditor": tradeline.get("creditor"),
            "balance": balance,
            "payment": reported_payment,
            "type": "student_loan",
            "include_in_dti": True
        }
    
    def check_for_exclusion(self, 
                           tradeline: dict,
                           documentation: list) -> dict:
        """Check if debt can be excluded from DTI"""
        # Co-signed debt with payment history
        if tradeline.get("joint") and self.has_payment_proof(documentation):
            return {
                "exclude": True,
                "reason": "Co-signed - 12 months payment proof provided"
            }
        
        # Paid by business (self-employed)
        if tradeline.get("paid_by_business"):
            return {
                "exclude": True,
                "reason": "Paid by business - documented"
            }
        
        return {"exclude": False}
```

---

## References

- [Fannie Mae B3-6](https://selling-guide.fanniemae.com/) - Debt obligations
- [Freddie Mac 5306](https://guide.freddiemac.com/) - DTI calculation
- [CFPB DTI Rules](https://www.consumerfinance.gov/) - Ability to repay
