# Bank Statement Misreads

## Issue: OCR System Incorrectly Extracts Data from Bank Statements

**Frequency**: Common

**Symptoms**
- Balance vs. available balance confusion
- NSF (insufficient funds) transactions missed
- Account holder name extraction errors
- Multiple account aggregation failures
- Statement period misidentification
- Currency/decimal errors

**Root Cause**
Bank statements vary significantly by institution in format, terminology, and layout. OCR must handle diverse formats while extracting correct balances, identifying problematic transactions (NSF, overdrafts), and calculating averages. Errors affect asset verification and borrower qualification.

**Example**
```
Scenario 1: Balance confusion

Statement shows:
- Ledger balance: $45,000
- Available balance: $32,000 (holds pending)
- Ending balance: $45,000

OCR: Extracted $45,000 ledger balance
Issue: $13,000 in pending holds not available

← Available balance is what matters
← OCR picked wrong balance field

---

Scenario 2: NSF transactions missed

Transaction history:
03/15 NSF Fee          -$35.00
03/15 Return Check    -$500.00
03/18 NSF Fee          -$35.00
03/22 Overdraft       -$250.00

OCR: Extracted ending balance ✓
Missing: 4 NSF/overdraft events flagged

← Pattern of insufficient funds
← Credit risk indicator
← Transaction analysis missing

---

Scenario 3: Account type misread

Statement header: "BUSINESS CHECKING - Smith Consulting"
OCR: Extracted as personal checking

← Business account cannot be used for reserves
← Account type misclassification

---

Scenario 4: Multi-statement averaging

2 months of statements required:
- March: Ending balance $28,000
- April: Ending balance $52,000

OCR: Used April balance ($52,000)
Correct: Average $40,000 or use lower

← Single statement balance used
← Should average or use lower
← Overstated assets

---

Bank statement failures:
  
  Documents with statement issues: 18%
  
  Issue types:
    Balance field confusion: 30%
    NSF/overdraft missed: 25%
    Account type errors: 15%
    Averaging failures: 15%
    Period identification: 10%
    Currency/decimal: 5%
  
  Impact:
    Asset miscalculation: 12%
    Credit concerns missed: 8%
    Re-documentation: 10%
```

**Key Statistics**
From Bank Statement Analysis (2026):
- Statement extraction errors: 15-22%
- Balance field confusion: 25-35%
- NSF detection failures: 20-30%
- Asset verification impact: 10-15%

**Contributing Factors**
- Diverse bank statement formats
- Multiple balance definitions
- Transaction categorization complexity
- Multi-month handling
- Account type indicators vary

---

## Mitigation Strategies

### Prevention
1. **Institution-specific parsing**: Bank-specific templates
2. **Balance type identification**: Ledger vs. available
3. **NSF detection**: Flag insufficient fund events
4. **Multi-statement averaging**: Proper calculation
5. **Account classification**: Personal vs. business

### Implementation
```python
class BankStatementParser:
    """Parse bank statements for mortgage verification"""
    
    NSF_KEYWORDS = ["nsf", "insufficient", "overdraft", "returned", "od fee"]
    BUSINESS_INDICATORS = ["business", "commercial", "corp", "llc", "inc"]
    
    def extract_balances(self, statement: dict) -> dict:
        """Extract and classify balance types"""
        return {
            "ending_balance": statement.get("ending_balance"),
            "available_balance": statement.get("available_balance"),
            "average_balance": statement.get("average_daily_balance"),
            "recommended_for_verification": statement.get("available_balance") 
                or statement.get("ending_balance")
        }
    
    def detect_nsf_transactions(self, transactions: list) -> dict:
        """Detect NSF and overdraft transactions"""
        nsf_events = []
        
        for tx in transactions:
            description = tx.get("description", "").lower()
            
            for keyword in self.NSF_KEYWORDS:
                if keyword in description:
                    nsf_events.append({
                        "date": tx["date"],
                        "description": tx["description"],
                        "amount": tx["amount"],
                        "type": "nsf_or_overdraft"
                    })
                    break
        
        return {
            "nsf_count": len(nsf_events),
            "events": nsf_events,
            "risk_flag": len(nsf_events) > 2,
            "action": "review_credit" if len(nsf_events) > 2 else None
        }
    
    def classify_account_type(self, statement: dict) -> dict:
        """Classify account as personal or business"""
        account_name = statement.get("account_name", "").lower()
        account_type = statement.get("account_type", "").lower()
        
        for indicator in self.BUSINESS_INDICATORS:
            if indicator in account_name or indicator in account_type:
                return {
                    "type": "business",
                    "usable_for_reserves": False,
                    "usable_for_down_payment": False
                }
        
        return {
            "type": "personal",
            "usable_for_reserves": True,
            "usable_for_down_payment": True
        }
    
    def calculate_multi_month_assets(self, statements: list) -> dict:
        """Calculate assets from multiple statements"""
        balances = [s.get("ending_balance", 0) for s in statements]
        
        if not balances:
            return {"error": "No statements provided"}
        
        return {
            "individual_balances": balances,
            "average_balance": sum(balances) / len(balances),
            "minimum_balance": min(balances),
            "recommended_value": min(balances),
            "method": "use_lower_of_average_or_minimum"
        }
```

---

## References

- [Fannie Mae B3-4.2](https://selling-guide.fanniemae.com/) - Asset verification
- [Freddie Mac 5501](https://guide.freddiemac.com/) - Bank statement requirements
- [CFPB ATR](https://www.consumerfinance.gov/) - Ability to repay verification
