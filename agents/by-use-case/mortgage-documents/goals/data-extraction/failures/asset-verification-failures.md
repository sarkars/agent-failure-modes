# Asset Verification Failures

## Issue: OCR System Incorrectly Extracts or Validates Borrower Assets

**Frequency**: Common

**Symptoms**
- Large deposits not flagged for sourcing
- Account balance averaging errors
- Gift funds misidentified
- Business vs. personal account confusion
- Retirement account liquidity miscalculated
- Earnest money deposit not traced

**Root Cause**
Mortgage underwriting requires verified assets for down payment, closing costs, and reserves. OCR must extract balances, identify account types, flag large deposits, and calculate available funds. Errors lead to incorrect qualification, undisclosed borrowing, and investor repurchase demands.

**Example**
```
Scenario 1: Large deposit not flagged

Bank statement shows:
- Beginning balance: $15,000
- Deposit March 3: $25,000
- Ending balance: $42,000 (includes other activity)

OCR: Extracted ending balance $42,000 ✓
Issue: $25,000 deposit exceeds 50% of income - requires sourcing

← Large deposit detection missing
← Potential undisclosed debt
← Compliance violation

---

Scenario 2: Business account as personal

Account extracted:
- Account holder: "John Smith DBA Smith Consulting"
- Balance: $85,000

OCR: Extracted as personal asset
Reality: Business operating account

← Business assets typically not usable for down payment
← Account type misclassified
← Inflated available assets

---

Scenario 3: Retirement account vesting

401(k) statement shows:
- Total balance: $150,000
- Vested: $95,000
- Employer match (unvested): $55,000

OCR: Extracted $150,000 total
Qualifying: Only $95,000 vested amount

← Unvested funds cannot be used
← Overstated assets by $55,000

---

Scenario 4: Gift fund documentation

Deposit sourced as gift:
- Gift letter: $30,000 from parent
- Bank statement: $30,000 deposit
- Donor bank statement: Not provided

OCR: Gift documented ✓
Missing: Donor's ability to give (bank statement showing withdrawal)

---

Asset verification failures:
  
  Documents with asset issues: 15%
  
  Issue types:
    Large deposit flagging: 30%
    Account type misclassification: 25%
    Vesting/liquidity errors: 20%
    Gift documentation gaps: 15%
    Balance calculation errors: 10%
  
  Impact:
    Qualification errors: 8%
    Additional docs required: 12%
    Investor findings: 5%
```

**Key Statistics**
From Mortgage Underwriting Research (2026):
- Asset-related defects: 12-18%
- Large deposit issues: 8-12%
- Gift fund documentation gaps: 10-15%
- Account type errors: 5-8%

**Contributing Factors**
- Large deposit threshold not applied
- Account type indicators missed
- Vesting status not extracted
- Gift fund trail not verified
- Business vs. personal not distinguished

---

## Mitigation Strategies

### Prevention
1. **Large deposit detection**: Flag deposits > 50% monthly income
2. **Account type classification**: Business vs. personal
3. **Vesting extraction**: Vested vs. unvested amounts
4. **Gift fund tracing**: Require donor documentation
5. **Balance averaging**: 60-day average calculation

### Implementation
```python
class AssetVerifier:
    """Verify and validate mortgage assets"""
    
    LARGE_DEPOSIT_THRESHOLD = 0.50  # 50% of monthly income
    
    def flag_large_deposits(self, 
                           transactions: list,
                           monthly_income: float) -> list:
        """Flag deposits requiring sourcing"""
        threshold = monthly_income * self.LARGE_DEPOSIT_THRESHOLD
        flags = []
        
        for tx in transactions:
            if tx["type"] == "deposit" and tx["amount"] > threshold:
                flags.append({
                    "date": tx["date"],
                    "amount": tx["amount"],
                    "threshold": threshold,
                    "action": "source_of_funds_required"
                })
        
        return flags
    
    def classify_account(self, account_info: dict) -> dict:
        """Classify account as personal or business"""
        name = account_info.get("account_holder", "").upper()
        
        business_indicators = ["LLC", "INC", "CORP", "DBA", "TRUST"]
        
        for indicator in business_indicators:
            if indicator in name:
                return {
                    "type": "business",
                    "usable_for_mortgage": False,
                    "indicator": indicator
                }
        
        return {"type": "personal", "usable_for_mortgage": True}
    
    def calculate_available_retirement(self, statement: dict) -> dict:
        """Calculate available retirement assets"""
        total = statement.get("total_balance", 0)
        vested = statement.get("vested_balance", total)
        
        # Apply withdrawal penalty factor (typically 60%)
        available = vested * 0.60
        
        return {
            "total_balance": total,
            "vested_balance": vested,
            "available_for_mortgage": available,
            "penalty_factor": 0.40
        }
```

---

## References

- [Fannie Mae B3-4.2](https://selling-guide.fanniemae.com/) - Asset requirements
- [CFPB ATR/QM](https://www.consumerfinance.gov/) - Asset verification
- [Gift Fund Guidelines](https://singlefamily.fanniemae.com/) - Gift documentation
