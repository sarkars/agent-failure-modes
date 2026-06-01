# Asset Source Tracing

## Issue: AI System Fails to Trace Assets to Legitimate Sources

**Frequency**: Common

**Symptoms**
- Large deposits not traced to source
- Gift funds without proper documentation
- Asset transfers between accounts not tracked
- Business funds commingled with personal
- Undisclosed liabilities hidden by transfers
- Seasoning requirements not validated

**Root Cause**
Mortgage underwriting requires tracing assets to their source to prevent money laundering and ensure legitimate down payment funds. AI systems must track money flow across bank statements, identify large deposits, correlate gift letters, and verify funds have been "seasoned" (in account for required period). Many systems only extract ending balances without analyzing transaction-level flows.

**Example**
```
Scenario 1: Large deposit without source

Bank statement (March 2025):
- Beginning balance: $12,500
- Deposits:
  - 03/05: Payroll $4,200
  - 03/15: Transfer $45,000  ← LARGE DEPOSIT
  - 03/19: Payroll $4,200
- Ending balance: $65,900

AI extraction:
- Ending balance: $65,900 ✓
- Sufficient for down payment ✓

Problem:
- $45,000 deposit = 360% of normal deposits
- Source unknown
- Not payroll, not regular transfer
- Requires documentation

Possible sources (require proof):
1. Gift from family (need gift letter)
2. Sale of asset (need bill of sale)
3. 401k withdrawal (need statement)
4. Loan (must be disclosed)

← Large deposit not flagged
← Source documentation not requested

---

Scenario 2: Gift letter doesn't match deposit

Gift letter:
- Donor: Mary Johnson (mother)
- Amount: $25,000
- Date: February 15, 2025
- Relationship: Mother

Bank statements:
- January: No large deposits
- February: $25,000 deposit on 02/20 ✓
- But: Deposit from "John Smith"  ← WRONG NAME

Analysis:
- Gift letter says Mary Johnson
- Deposit shows John Smith
- Could be father? Unrelated?

← Gift letter doesn't match actual deposit
← Additional documentation needed

---

Scenario 3: Circular transfer pattern

Account A (Borrower):
- 03/01: Balance $5,000
- 03/10: Transfer to Account B: -$20,000  ← Overdraft?
- 03/15: Transfer from Account B: +$25,000
- 03/31: Balance $10,000

Account B (Borrower):
- 03/01: Balance $30,000
- 03/10: Transfer from Account A: +$20,000
- 03/15: Transfer to Account A: -$25,000
- 03/31: Balance $25,000

Net effect:
- $5,000 moved from B to A
- But multiple large transfers
- Could be hiding the true source

← Circular transfers are red flag
← May indicate manufactured assets

---

Scenario 4: Business funds used for down payment

Application:
- Self-employed: Yes
- Business: Smith Consulting LLC

Personal bank statement:
- 03/20: Transfer from Smith Consulting: $50,000

Business bank statement (not provided):
- Source of $50,000 unknown

Issues:
1. Business funds ≠ Personal funds
2. Must prove business can afford distribution
3. Tax implications for withdrawal
4. May require business financials

← Business-to-personal transfer needs documentation
← Business cash flow must support withdrawal

---

Asset tracing requirements:

  Deposit Size    | Documentation Required
  ----------------|------------------------
  < 50% monthly   | None (normal income)
  50-100% monthly | Source explanation
  > 100% monthly  | Full documentation
  > $10,000       | Source documentation
  > $50,000       | Comprehensive paper trail
  
  Seasoning requirements:
  - Conventional: 60 days
  - FHA: 60 days
  - VA: 60 days
  - Gift funds: Must be deposited before closing
  
  Source types requiring documentation:
  - Gift funds: Letter, donor statement, relationship
  - Sale of asset: Bill of sale, prior ownership
  - 401k/IRA: Statement showing withdrawal
  - Insurance: Claim documentation
  - Legal settlement: Court documents
  - Business distribution: Business statements, tax returns
```

**Key Statistics**
From Asset Verification (2025-2026):
- Applications with large deposits: 25-35%
- Large deposits properly documented: 60-70%
- Gift funds: 15-20% of applications
- Undocumented asset sources: 8-12%
- Circular transfer patterns: 2-3%

**Contributing Factors**
- Transaction-level analysis not performed
- Large deposit detection threshold missing
- Gift letter correlation not automated
- Seasoning validation not checked
- Cross-account transfers not tracked
- Business/personal commingling ignored

---

## Mitigation Strategies

### Prevention
1. **Transaction analysis**: Review all deposits, not just balances
2. **Large deposit detection**: Flag deposits >50% of normal income
3. **Gift correlation**: Match gift letters to actual deposits
4. **Transfer tracking**: Follow money between accounts
5. **Seasoning validation**: Verify funds meet time requirements
6. **Source documentation**: Request proof for large deposits

### Implementation
```python
from datetime import date, timedelta
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Transaction:
    date: date
    amount: float
    description: str
    type: str  # deposit, withdrawal, transfer
    category: Optional[str] = None

@dataclass
class LargeDeposit:
    date: date
    amount: float
    description: str
    source_documented: bool
    source_type: Optional[str]
    documentation: Optional[str]

class AssetSourceTracer:
    """Trace assets to legitimate sources"""
    
    LARGE_DEPOSIT_THRESHOLD = 0.5  # 50% of monthly income
    ABSOLUTE_THRESHOLD = 10000     # $10,000 always flagged
    SEASONING_DAYS = 60            # Standard seasoning requirement
    
    def analyze_bank_statements(self, 
                                 statements: list,
                                 monthly_income: float,
                                 closing_date: date) -> dict:
        """Analyze bank statements for asset sourcing"""
        
        result = {
            "large_deposits": [],
            "undocumented_sources": [],
            "seasoning_issues": [],
            "circular_transfers": [],
            "gift_correlations": [],
            "risk_score": 0.0
        }
        
        # Extract all transactions
        all_transactions = []
        for statement in statements:
            transactions = self.extract_transactions(statement)
            all_transactions.extend(transactions)
        
        # Identify large deposits
        threshold = max(
            monthly_income * self.LARGE_DEPOSIT_THRESHOLD,
            self.ABSOLUTE_THRESHOLD
        )
        
        large_deposits = [
            t for t in all_transactions 
            if t.type == "deposit" and t.amount >= threshold
        ]
        
        for deposit in large_deposits:
            # Check if source is identifiable
            source = self.identify_source(deposit)
            
            large_dep = LargeDeposit(
                date=deposit.date,
                amount=deposit.amount,
                description=deposit.description,
                source_documented=source["documented"],
                source_type=source["type"],
                documentation=source.get("documentation")
            )
            
            result["large_deposits"].append(large_dep)
            
            if not source["documented"]:
                result["undocumented_sources"].append({
                    "deposit": large_dep,
                    "action": "Request source documentation"
                })
                result["risk_score"] += 0.2
        
        # Check seasoning
        for deposit in large_deposits:
            days_before_closing = (closing_date - deposit.date).days
            if days_before_closing < self.SEASONING_DAYS:
                result["seasoning_issues"].append({
                    "deposit_date": str(deposit.date),
                    "amount": deposit.amount,
                    "days_before_closing": days_before_closing,
                    "required_days": self.SEASONING_DAYS
                })
                result["risk_score"] += 0.15
        
        # Detect circular transfers
        transfers = [t for t in all_transactions if "transfer" in t.type.lower()]
        circular = self.detect_circular_transfers(transfers)
        result["circular_transfers"] = circular
        if circular:
            result["risk_score"] += 0.3
        
        result["risk_score"] = min(result["risk_score"], 1.0)
        
        return result
    
    def identify_source(self, transaction: Transaction) -> dict:
        """Identify the source of a deposit"""
        
        description = transaction.description.lower()
        
        # Payroll patterns
        payroll_keywords = ["payroll", "salary", "direct deposit", "wages", "adp", "paychex"]
        if any(kw in description for kw in payroll_keywords):
            return {
                "type": "payroll",
                "documented": True,
                "confidence": 0.95
            }
        
        # Transfer patterns
        if "transfer" in description:
            return {
                "type": "transfer",
                "documented": False,  # Need source account statement
                "action": "Provide source account statement",
                "confidence": 0.5
            }
        
        # Wire patterns
        if "wire" in description:
            return {
                "type": "wire",
                "documented": False,
                "action": "Provide wire documentation",
                "confidence": 0.3
            }
        
        # Cash/check deposits
        if "cash" in description or "check" in description:
            if transaction.amount > 10000:
                return {
                    "type": "cash_or_check",
                    "documented": False,
                    "action": "Provide source documentation",
                    "confidence": 0.2
                }
        
        # Unknown
        return {
            "type": "unknown",
            "documented": False,
            "action": "Identify and document source",
            "confidence": 0.1
        }
    
    def correlate_gift_funds(self, 
                             gift_letters: list,
                             transactions: list) -> dict:
        """Correlate gift letters with actual deposits"""
        
        correlations = {
            "matched": [],
            "unmatched_letters": [],
            "unmatched_deposits": []
        }
        
        gift_deposits = []
        
        for letter in gift_letters:
            donor = letter["donor_name"].lower()
            amount = letter["amount"]
            gift_date = letter["date"]
            
            # Look for matching deposit
            matched = False
            for txn in transactions:
                if txn.type != "deposit":
                    continue
                
                # Amount within 5%
                amount_match = abs(txn.amount - amount) / amount < 0.05
                
                # Date within 30 days
                date_diff = abs((txn.date - gift_date).days)
                date_match = date_diff <= 30
                
                # Donor name in description
                name_match = donor in txn.description.lower()
                
                if amount_match and date_match:
                    correlations["matched"].append({
                        "letter": letter,
                        "deposit": txn,
                        "name_match": name_match,
                        "verified": name_match
                    })
                    matched = True
                    break
            
            if not matched:
                correlations["unmatched_letters"].append(letter)
        
        return correlations
    
    def detect_circular_transfers(self, transfers: list) -> list:
        """Detect circular transfer patterns"""
        
        circular = []
        
        # Group by rough amount (within 10%)
        for i, t1 in enumerate(transfers):
            for t2 in transfers[i+1:]:
                # Opposite directions
                if t1.amount * t2.amount < 0:  # One positive, one negative
                    # Similar amounts
                    if abs(abs(t1.amount) - abs(t2.amount)) / max(abs(t1.amount), abs(t2.amount)) < 0.1:
                        # Within 30 days
                        if abs((t1.date - t2.date).days) <= 30:
                            circular.append({
                                "transfer1": t1,
                                "transfer2": t2,
                                "pattern": "offsetting_transfers",
                                "risk": "medium"
                            })
        
        return circular
    
    def check_business_distribution(self,
                                    personal_statements: list,
                                    business_statements: list,
                                    tax_returns: list) -> dict:
        """Validate business distributions for self-employed"""
        
        result = {
            "distributions_found": [],
            "issues": [],
            "risk_score": 0.0
        }
        
        # Find transfers from business to personal
        for p_stmt in personal_statements:
            for txn in p_stmt.get("transactions", []):
                if txn["type"] == "deposit":
                    desc = txn["description"].lower()
                    
                    # Business name patterns
                    if any(term in desc for term in ["llc", "corp", "inc", "consulting"]):
                        distribution = {
                            "date": txn["date"],
                            "amount": txn["amount"],
                            "from": txn["description"]
                        }
                        result["distributions_found"].append(distribution)
                        
                        # Verify against business statements
                        if not business_statements:
                            result["issues"].append({
                                "type": "missing_business_statements",
                                "distribution": distribution,
                                "action": "Request business bank statements"
                            })
                            result["risk_score"] += 0.25
        
        return result
    
    def extract_transactions(self, statement: dict) -> List[Transaction]:
        """Extract transactions from bank statement"""
        
        transactions = []
        
        for txn in statement.get("transactions", []):
            transactions.append(Transaction(
                date=txn["date"],
                amount=txn["amount"],
                description=txn.get("description", ""),
                type=self.categorize_transaction(txn)
            ))
        
        return transactions
    
    def categorize_transaction(self, txn: dict) -> str:
        """Categorize transaction type"""
        
        amount = txn["amount"]
        desc = txn.get("description", "").lower()
        
        if amount > 0:
            if "transfer" in desc:
                return "transfer_in"
            return "deposit"
        else:
            if "transfer" in desc:
                return "transfer_out"
            return "withdrawal"
```

### Risk Scoring for Asset Issues

| Issue | Risk Score | Action |
|-------|------------|--------|
| Large deposit undocumented | 0.25 | Request source docs |
| Seasoning not met | 0.15 | Verify before closing |
| Gift letter unmatched | 0.2 | Reconcile discrepancy |
| Circular transfers | 0.3 | Enhanced review |
| Business distribution undocumented | 0.25 | Business statements |
| Unknown large wire | 0.3 | Full paper trail |

---

## References

- [Fannie Mae Asset Documentation](https://selling-guide.fanniemae.com/)
- [HUD Gift Fund Requirements](https://www.hud.gov/)
- [Anti-Money Laundering](https://www.fincen.gov/)
