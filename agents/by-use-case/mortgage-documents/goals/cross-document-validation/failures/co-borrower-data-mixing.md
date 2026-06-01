# Co-Borrower Data Mixing

## Issue: AI System Incorrectly Attributes Data Between Borrower and Co-Borrower

**Frequency**: Occasional

**Symptoms**
- Co-borrower income counted for primary borrower
- Primary borrower debt assigned to co-borrower
- Employment mixed between parties
- Assets attributed to wrong person
- Credit scores swapped
- Tax return income combined incorrectly

**Root Cause**
Joint mortgage applications involve two or more borrowers with separate income, assets, and credit histories. Documents may list both parties, use joint accounts, or file combined tax returns. AI systems must carefully attribute data to the correct borrower while properly combining joint assets and handling married-filing-jointly scenarios.

**Example**
```
Scenario 1: Income attribution error

Application:
- Primary: John Smith, SSN: 111-22-3333
- Co-borrower: Jane Smith, SSN: 444-55-6666

Documents:
- W-2 #1: John Smith, $85,000
- W-2 #2: Jane Smith, $62,000
- Joint tax return (MFJ): AGI $147,000

AI extraction:
- John income: $147,000 ← ERROR (used joint AGI)
- Jane income: $62,000

Problem:
- John's income overstated by $62,000
- Used total AGI instead of individual W-2
- DTI calculation incorrect

← Income from co-borrower attributed to primary

---

Scenario 2: Debt attribution error

Credit reports:
- John: 3 credit cards, $12,000 balance
- Jane: 2 credit cards, $8,000 balance
- Joint mortgage: $250,000

AI processing:
- John debts: $270,000 (included joint mortgage)
- Jane debts: $258,000 (also included joint mortgage)

Problem:
- Joint mortgage counted TWICE
- Total debt overstated by $250,000
- DTI ratio incorrect for both

← Joint liability double-counted

---

Scenario 3: Employment confusion

Both borrowers work at large employers:

John:
- Employer: ABC Corporation
- Position: Senior Engineer
- W-2: $95,000

Jane:
- Employer: ABC Corporation (same company!)
- Position: Marketing Manager
- W-2: $78,000

AI extraction:
- Found 2 W-2s from "ABC Corporation"
- Assumed duplicate, kept one
- Total income: $95,000 (should be $173,000)

← Same employer doesn't mean same person
← Both incomes should count

---

Scenario 4: Credit score mix-up

Credit pulls:
- Equifax John: 745
- Equifax Jane: 680
- Experian John: 752
- Experian Jane: 675

AI reported:
- Primary borrower score: 680 ← Wrong (Jane's score)
- Co-borrower score: 745 ← Wrong (John's score)

Impact:
- Pricing based on lower score
- But attributed to wrong person
- May affect eligibility determination

← Scores swapped between borrowers

---

Scenario 5: Asset account ownership

Bank statements:
- Account A (John): $25,000
- Account B (Jane): $18,000  
- Account C (Joint): $45,000

Application requires $50,000 for closing

AI asset allocation:
- John's assets: $25,000 (only individual)
- Jane's assets: $18,000 (only individual)
- "Insufficient for closing"

Problem:
- Joint account not attributed
- $45,000 available for either borrower
- Total available: $88,000

← Joint assets not properly handled

---

Co-borrower data rules:

  Data Type     | Primary    | Co-Borrower | Joint
  --------------|------------|-------------|--------
  W-2 income    | By SSN     | By SSN      | N/A
  Tax return    | Allocated  | Allocated   | Split by W-2
  Credit score  | Their own  | Their own   | N/A
  Bank account  | Individual | Individual  | Either/both
  Mortgage debt | Both if joint | Both if joint | Counted once
  Car loan      | By name    | By name     | Both if joint
```

**Key Statistics**
From Co-Borrower Processing (2025-2026):
- Applications with co-borrowers: 40-50%
- Data attribution errors: 8-12%
- Income misattribution: 5-7%
- Debt double-counting: 3-5%
- Asset ownership confusion: 6-8%

**Contributing Factors**
- SSN-to-borrower mapping inconsistent
- Joint account handling undefined
- Same employer confusion
- Married-filing-jointly not parsed correctly
- Debt ownership not tracked
- Credit report person matching weak

---

## Mitigation Strategies

### Prevention
1. **SSN-based attribution**: Always use SSN as primary key
2. **Joint account rules**: Define how to handle shared assets
3. **Debt deduplication**: Track joint liabilities once
4. **MFJ parsing**: Allocate income from joint returns
5. **Name disambiguation**: Handle same employer scenarios
6. **Credit report matching**: Verify person on each report

### Implementation
```python
from dataclasses import dataclass
from typing import List, Dict, Optional, Set
from enum import Enum

class Ownership(Enum):
    PRIMARY = "primary"
    CO_BORROWER = "co_borrower"
    JOINT = "joint"
    UNKNOWN = "unknown"

@dataclass
class Borrower:
    name: str
    ssn: str
    role: str  # primary or co_borrower

@dataclass
class DataItem:
    type: str
    amount: float
    ownership: Ownership
    source_document: str
    confidence: float

class CoBorrowerDataManager:
    """Manage data attribution for multiple borrowers"""
    
    def __init__(self, borrowers: List[Borrower]):
        self.borrowers = borrowers
        self.primary = next(b for b in borrowers if b.role == "primary")
        self.co_borrowers = [b for b in borrowers if b.role != "primary"]
        
        # SSN lookup
        self.ssn_map = {b.ssn: b for b in borrowers}
        
        # Track joint liabilities to avoid double-counting
        self.joint_liabilities: Set[str] = set()
    
    def process_income_documents(self, documents: list) -> dict:
        """Process income documents with proper attribution"""
        
        income = {
            "primary": [],
            "co_borrower": [],
            "total_primary": 0,
            "total_co_borrower": 0,
            "total_household": 0
        }
        
        for doc in documents:
            doc_type = doc.get("type")
            
            if doc_type == "w2":
                # Attribute by SSN on W-2
                doc_ssn = doc.get("employee_ssn")
                borrower = self.identify_by_ssn(doc_ssn)
                
                amount = doc.get("box1_wages", 0)
                
                if borrower:
                    item = DataItem(
                        type="w2_income",
                        amount=amount,
                        ownership=Ownership.PRIMARY if borrower == self.primary 
                                  else Ownership.CO_BORROWER,
                        source_document=doc.get("id"),
                        confidence=1.0 if doc_ssn else 0.5
                    )
                    
                    if borrower == self.primary:
                        income["primary"].append(item)
                        income["total_primary"] += amount
                    else:
                        income["co_borrower"].append(item)
                        income["total_co_borrower"] += amount
            
            elif doc_type == "tax_return":
                # Handle MFJ returns
                if doc.get("filing_status") == "married_filing_jointly":
                    income = self.allocate_mfj_income(doc, income)
                else:
                    # Single/separate - attribute by SSN
                    self.attribute_tax_return(doc, income)
        
        income["total_household"] = (
            income["total_primary"] + income["total_co_borrower"]
        )
        
        return income
    
    def allocate_mfj_income(self, 
                           tax_return: dict,
                           income: dict) -> dict:
        """Allocate income from married-filing-jointly return"""
        
        # Get individual W-2 amounts already extracted
        primary_w2_total = income["total_primary"]
        co_w2_total = income["total_co_borrower"]
        
        # Tax return Line 1 should roughly equal W-2 totals
        tax_wages = tax_return.get("line1_wages", 0)
        
        # Verify alignment
        w2_total = primary_w2_total + co_w2_total
        variance = abs(tax_wages - w2_total)
        
        if variance / max(tax_wages, 1) > 0.05:
            # Significant variance - investigate
            income["mfj_warning"] = {
                "tax_wages": tax_wages,
                "w2_total": w2_total,
                "variance": variance
            }
        
        # Schedule C income - need to identify whose business
        if tax_return.get("schedule_c"):
            for schedule_c in tax_return["schedule_c"]:
                owner_ssn = schedule_c.get("owner_ssn")
                if owner_ssn:
                    borrower = self.identify_by_ssn(owner_ssn)
                    se_income = schedule_c.get("net_profit", 0)
                    
                    if borrower == self.primary:
                        income["total_primary"] += se_income
                    else:
                        income["total_co_borrower"] += se_income
        
        return income
    
    def process_debts(self, credit_reports: list) -> dict:
        """Process debts avoiding double-counting joint accounts"""
        
        debts = {
            "primary": [],
            "co_borrower": [],
            "joint": [],
            "total_monthly_primary": 0,
            "total_monthly_co_borrower": 0,
            "total_monthly_payment": 0
        }
        
        for report in credit_reports:
            # Identify whose report
            report_ssn = report.get("subject_ssn")
            borrower = self.identify_by_ssn(report_ssn)
            
            if not borrower:
                continue
            
            for account in report.get("accounts", []):
                account_id = self.generate_account_id(account)
                
                # Check if joint and already processed
                if account.get("account_type") == "joint":
                    if account_id in self.joint_liabilities:
                        # Already counted
                        continue
                    self.joint_liabilities.add(account_id)
                    
                    debts["joint"].append({
                        "account": account,
                        "payment": account.get("monthly_payment", 0)
                    })
                    debts["total_monthly_payment"] += account.get(
                        "monthly_payment", 0
                    )
                
                else:
                    # Individual account
                    payment = account.get("monthly_payment", 0)
                    
                    if borrower == self.primary:
                        debts["primary"].append(account)
                        debts["total_monthly_primary"] += payment
                    else:
                        debts["co_borrower"].append(account)
                        debts["total_monthly_co_borrower"] += payment
        
        # Total is primary + co-borrower + joint (counted once)
        debts["total_monthly_payment"] += (
            debts["total_monthly_primary"] + 
            debts["total_monthly_co_borrower"]
        )
        
        return debts
    
    def process_assets(self, bank_statements: list) -> dict:
        """Process assets with joint account handling"""
        
        assets = {
            "primary_individual": [],
            "co_borrower_individual": [],
            "joint": [],
            "total_primary": 0,
            "total_co_borrower": 0,
            "total_available": 0
        }
        
        for statement in bank_statements:
            account_type = self.determine_ownership(statement)
            balance = statement.get("ending_balance", 0)
            
            asset = {
                "account": statement.get("account_number_masked"),
                "institution": statement.get("institution"),
                "balance": balance,
                "ownership": account_type
            }
            
            if account_type == Ownership.PRIMARY:
                assets["primary_individual"].append(asset)
                assets["total_primary"] += balance
            elif account_type == Ownership.CO_BORROWER:
                assets["co_borrower_individual"].append(asset)
                assets["total_co_borrower"] += balance
            elif account_type == Ownership.JOINT:
                assets["joint"].append(asset)
                # Joint available to either borrower
                assets["total_primary"] += balance
                assets["total_co_borrower"] += balance
        
        # Total available is sum of all (joint counted once)
        assets["total_available"] = (
            sum(a["balance"] for a in assets["primary_individual"]) +
            sum(a["balance"] for a in assets["co_borrower_individual"]) +
            sum(a["balance"] for a in assets["joint"])
        )
        
        return assets
    
    def identify_by_ssn(self, ssn: str) -> Optional[Borrower]:
        """Identify borrower by SSN"""
        
        if not ssn:
            return None
        
        # Normalize SSN
        normalized = ssn.replace("-", "").replace(" ", "")
        
        for stored_ssn, borrower in self.ssn_map.items():
            stored_normalized = stored_ssn.replace("-", "")
            if normalized == stored_normalized:
                return borrower
            # Match on last 4 if partial
            if len(normalized) == 4 and stored_normalized.endswith(normalized):
                return borrower
        
        return None
    
    def determine_ownership(self, statement: dict) -> Ownership:
        """Determine account ownership from statement"""
        
        account_holders = statement.get("account_holders", [])
        
        if len(account_holders) == 0:
            return Ownership.UNKNOWN
        
        if len(account_holders) >= 2:
            return Ownership.JOINT
        
        # Single holder - identify
        holder = account_holders[0]
        holder_ssn = holder.get("ssn")
        
        if holder_ssn:
            borrower = self.identify_by_ssn(holder_ssn)
            if borrower == self.primary:
                return Ownership.PRIMARY
            elif borrower in self.co_borrowers:
                return Ownership.CO_BORROWER
        
        # Try name matching
        holder_name = holder.get("name", "").lower()
        if self.primary.name.lower() in holder_name:
            return Ownership.PRIMARY
        for co in self.co_borrowers:
            if co.name.lower() in holder_name:
                return Ownership.CO_BORROWER
        
        return Ownership.UNKNOWN
    
    def generate_account_id(self, account: dict) -> str:
        """Generate unique ID for deduplication"""
        
        return f"{account.get('creditor', '')}_{account.get('account_number', '')}".lower()
```

### Risk Scoring for Co-Borrower Issues

| Issue | Risk Score | Action |
|-------|------------|--------|
| Income misattributed | 0.3 | Recalculate DTI |
| Debt double-counted | 0.25 | Deduplicate liabilities |
| Joint asset unattributed | 0.15 | Verify ownership |
| Credit scores swapped | 0.2 | Re-pull reports |
| MFJ income not allocated | 0.25 | Match to W-2s |
| Unknown ownership | 0.1 | Request documentation |

---

## References

- [Fannie Mae Co-Borrower Requirements](https://selling-guide.fanniemae.com/)
- [MISMO Borrower Data Standards](https://www.mismo.org/)
- [IRS MFJ Guidelines](https://www.irs.gov/publications/p17)
