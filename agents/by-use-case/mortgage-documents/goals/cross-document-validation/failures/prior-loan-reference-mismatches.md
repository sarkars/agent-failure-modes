# Prior Loan Reference Mismatches

## Issue: AI System Fails to Verify Prior Loan Details Against Credit Report and Public Records

**Frequency**: Occasional

**Symptoms**
- Prior mortgage balance doesn't match credit report
- Refinance payoff amount inconsistent
- Prior lender name differs across documents
- Loan number discrepancies
- Property address variations
- Undisclosed mortgages not detected

**Root Cause**
Borrowers with existing mortgages must have prior loan details verified. The credit report shows current balances, statements show payment history, and title searches reveal liens. AI systems must correlate these sources to detect discrepancies that may indicate fraud, errors, or undisclosed obligations.

**Example**
```
Scenario 1: Balance mismatch between credit and statement

Credit report (pulled March 2025):
- Lender: FirstBank Mortgage
- Original: $320,000
- Current balance: $285,000
- Payment: $1,850/month

Mortgage statement (February 2025):
- Lender: FirstBank Mortgage ✓
- Current balance: $248,000 ← $37,000 DIFFERENCE

Analysis:
- Credit shows $285K
- Statement shows $248K
- 13% variance

Possible explanations:
1. Credit report outdated
2. Large principal payment not reflected
3. Different account
4. Statement altered

← Significant balance discrepancy
← May affect DTI calculation

---

Scenario 2: Undisclosed second mortgage

Application declares:
- First mortgage: $300,000 with MegaBank
- No other liens

Credit report shows:
- MegaBank: $298,500 ✓
- HomeEquity LLC: $45,000 ← NOT DISCLOSED

Title search confirms:
- First lien: MegaBank
- Second lien: HomeEquity LLC

Issue:
- Second mortgage not on application
- Affects total debt
- May affect LTV on refinance
- Intentional omission?

← Undisclosed lien discovered
← Application misrepresentation

---

Scenario 3: Refinance payoff discrepancy

Refinancing existing loan:
- Stated current balance: $225,000
- Stated lender: Regional Bank

Payoff statement received:
- Lender: Regional Bank ✓
- Payoff amount: $228,450
- Includes: Principal + interest + fees

Credit report shows:
- Regional Bank balance: $226,800

Discrepancy analysis:
- Application: $225,000
- Credit: $226,800 (+$1,800)
- Payoff: $228,450 (+$3,450)

Explanations:
- Payoff includes per diem interest ✓
- Credit may lag 30 days ✓
- Application was estimate ✓

← Minor variance acceptable
← Within expected tolerance

---

Scenario 4: Prior loan number inconsistency

VOE from prior mortgage:
- Loan #: 12345678

Credit report:
- Account #: 1234-5678-XX

Payoff statement:
- Loan #: 8765-4321 ← DIFFERENT

Application:
- Account #: 12345678

Analysis:
- Three different formats
- Payoff number completely different
- Could be:
  1. Different accounts
  2. Account number changes
  3. Wrong payoff requested

← Loan number discrepancy
← Verify correct account

---

Scenario 5: Property address variations across liens

Subject property: 123 Main Street, Unit 4B

Credit report lien:
- Property: 123 Main St #4B

Title search:
- Property: 123 Main Street, Apt 4-B

Prior loan statement:
- Property: 125 Main Street ← DIFFERENT ADDRESS

Issue:
- Prior statement shows different address
- Could be:
  1. Wrong statement provided
  2. Address typo on original loan
  3. Different property

← Property address doesn't match subject

---

Prior loan verification matrix:

  Data Point       | Sources to Compare
  -----------------|------------------------------------
  Current balance  | Credit report, statement, payoff
  Monthly payment  | Credit report, statement, application
  Lender name      | Credit, statement, title
  Loan number      | Credit, statement, payoff
  Property address | Credit, title, statement
  Loan type        | Credit, application
  
  Acceptable variances:
  - Balance: ±$2,000 or 1% (whichever greater)
  - Payment: ±$50
  - Payoff: Higher due to per diem
  
  Red flags:
  - Undisclosed liens
  - Balance >5% different
  - Wrong property address
  - Lender name mismatch
```

**Key Statistics**
From Prior Loan Verification (2025-2026):
- Balance discrepancies: 10-15%
- Discrepancies >$5,000: 3-5%
- Undisclosed liens: 2-3%
- Property address issues: 1-2%
- Lender name mismatches: 5-8%

**Contributing Factors**
- Single-source balance used
- Credit report timing not considered
- Multiple liens not aggregated
- Loan number formats not normalized
- Address matching not performed
- Payoff quotes not validated

---

## Mitigation Strategies

### Prevention
1. **Multi-source verification**: Compare all balance sources
2. **Timing consideration**: Account for credit report lag
3. **Lien aggregation**: Count all liens on property
4. **Number normalization**: Handle format variations
5. **Address matching**: Normalize and compare
6. **Payoff validation**: Request official payoff quote

### Implementation
```python
from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import date, timedelta
import re

@dataclass
class PriorLoan:
    lender: str
    account_number: str
    original_amount: float
    current_balance: float
    monthly_payment: float
    property_address: str
    source: str
    as_of_date: date

@dataclass
class LoanDiscrepancy:
    field: str
    source1: str
    value1: str
    source2: str
    value2: str
    variance: float
    severity: str

class PriorLoanValidator:
    """Validate prior loan references across documents"""
    
    BALANCE_TOLERANCE_PCT = 0.02  # 2%
    BALANCE_TOLERANCE_ABS = 2000  # $2,000
    PAYMENT_TOLERANCE = 50       # $50
    
    def validate_prior_loans(self,
                             application: dict,
                             credit_report: dict,
                             statements: list,
                             title_search: dict,
                             payoff_quotes: list) -> dict:
        """Validate all prior loan references"""
        
        result = {
            "loans_identified": [],
            "discrepancies": [],
            "undisclosed_liens": [],
            "risk_score": 0.0
        }
        
        # Extract loans from each source
        app_loans = self.extract_application_loans(application)
        credit_loans = self.extract_credit_loans(credit_report)
        statement_loans = self.extract_statement_loans(statements)
        title_liens = self.extract_title_liens(title_search)
        
        # Correlate loans across sources
        correlated = self.correlate_loans(
            app_loans, credit_loans, statement_loans, title_liens
        )
        result["loans_identified"] = correlated
        
        # Check for discrepancies
        for loan_group in correlated:
            discrepancies = self.check_discrepancies(loan_group)
            result["discrepancies"].extend(discrepancies)
        
        # Check for undisclosed liens
        undisclosed = self.find_undisclosed_liens(
            app_loans, credit_loans, title_liens
        )
        result["undisclosed_liens"] = undisclosed
        
        # Calculate risk
        for disc in result["discrepancies"]:
            if disc.severity == "critical":
                result["risk_score"] += 0.35
            elif disc.severity == "high":
                result["risk_score"] += 0.2
            elif disc.severity == "medium":
                result["risk_score"] += 0.1
        
        for lien in result["undisclosed_liens"]:
            result["risk_score"] += 0.4  # Undisclosed is serious
        
        result["risk_score"] = min(result["risk_score"], 1.0)
        
        return result
    
    def correlate_loans(self,
                        app_loans: List[PriorLoan],
                        credit_loans: List[PriorLoan],
                        statement_loans: List[PriorLoan],
                        title_liens: List[PriorLoan]) -> List[List[PriorLoan]]:
        """Correlate same loan across sources"""
        
        all_loans = (
            [(l, "application") for l in app_loans] +
            [(l, "credit") for l in credit_loans] +
            [(l, "statement") for l in statement_loans] +
            [(l, "title") for l in title_liens]
        )
        
        groups = []
        used = set()
        
        for i, (loan1, source1) in enumerate(all_loans):
            if i in used:
                continue
            
            group = [loan1]
            used.add(i)
            
            for j, (loan2, source2) in enumerate(all_loans[i+1:], i+1):
                if j in used:
                    continue
                
                if self.loans_match(loan1, loan2):
                    group.append(loan2)
                    used.add(j)
            
            groups.append(group)
        
        return groups
    
    def loans_match(self, loan1: PriorLoan, loan2: PriorLoan) -> bool:
        """Determine if two loan records refer to same loan"""
        
        # Check account number
        norm1 = self.normalize_account(loan1.account_number)
        norm2 = self.normalize_account(loan2.account_number)
        
        if norm1 and norm2:
            # If account numbers match, same loan
            if norm1 == norm2:
                return True
            # If very different, probably different loans
            if len(set(norm1) & set(norm2)) < len(norm1) * 0.5:
                return False
        
        # Check lender name
        if self.lenders_match(loan1.lender, loan2.lender):
            # Same lender - check balance proximity
            if loan1.current_balance and loan2.current_balance:
                variance = abs(loan1.current_balance - loan2.current_balance)
                avg = (loan1.current_balance + loan2.current_balance) / 2
                
                if variance / avg < 0.1:  # Within 10%
                    return True
        
        # Check property address
        if self.addresses_match(loan1.property_address, loan2.property_address):
            return True
        
        return False
    
    def check_discrepancies(self, 
                            loan_group: List[PriorLoan]) -> List[LoanDiscrepancy]:
        """Check for discrepancies within a loan group"""
        
        discrepancies = []
        
        if len(loan_group) < 2:
            return discrepancies
        
        # Compare balances
        balances = [
            (l.source, l.current_balance, l.as_of_date) 
            for l in loan_group if l.current_balance
        ]
        
        if len(balances) >= 2:
            # Sort by date to compare most recent
            balances.sort(key=lambda x: x[2] if x[2] else date.min)
            
            for i in range(len(balances) - 1):
                source1, bal1, date1 = balances[i]
                source2, bal2, date2 = balances[i + 1]
                
                variance = abs(bal1 - bal2)
                tolerance = max(
                    self.BALANCE_TOLERANCE_ABS,
                    max(bal1, bal2) * self.BALANCE_TOLERANCE_PCT
                )
                
                if variance > tolerance:
                    # Account for time between reports
                    days_diff = (date2 - date1).days if date1 and date2 else 0
                    expected_reduction = days_diff * (bal1 / 360 / 30) * 0.8  # Rough amortization
                    
                    adjusted_variance = abs(variance - expected_reduction)
                    
                    if adjusted_variance > tolerance:
                        severity = "high" if variance > 10000 else "medium"
                        
                        discrepancies.append(LoanDiscrepancy(
                            field="current_balance",
                            source1=source1,
                            value1=f"${bal1:,.0f}",
                            source2=source2,
                            value2=f"${bal2:,.0f}",
                            variance=variance,
                            severity=severity
                        ))
        
        # Compare monthly payments
        payments = [
            (l.source, l.monthly_payment) 
            for l in loan_group if l.monthly_payment
        ]
        
        if len(payments) >= 2:
            for i in range(len(payments) - 1):
                source1, pay1 = payments[i]
                source2, pay2 = payments[i + 1]
                
                variance = abs(pay1 - pay2)
                
                if variance > self.PAYMENT_TOLERANCE:
                    discrepancies.append(LoanDiscrepancy(
                        field="monthly_payment",
                        source1=source1,
                        value1=f"${pay1:,.0f}",
                        source2=source2,
                        value2=f"${pay2:,.0f}",
                        variance=variance,
                        severity="medium"
                    ))
        
        # Compare lender names
        lenders = [(l.source, l.lender) for l in loan_group if l.lender]
        
        if len(lenders) >= 2:
            for i in range(len(lenders) - 1):
                source1, lender1 = lenders[i]
                source2, lender2 = lenders[i + 1]
                
                if not self.lenders_match(lender1, lender2):
                    discrepancies.append(LoanDiscrepancy(
                        field="lender",
                        source1=source1,
                        value1=lender1,
                        source2=source2,
                        value2=lender2,
                        variance=0,
                        severity="medium"
                    ))
        
        return discrepancies
    
    def find_undisclosed_liens(self,
                               app_loans: List[PriorLoan],
                               credit_loans: List[PriorLoan],
                               title_liens: List[PriorLoan]) -> List[dict]:
        """Find liens not disclosed on application"""
        
        undisclosed = []
        
        # Combine credit and title for full picture
        discovered_loans = credit_loans + title_liens
        
        for discovered in discovered_loans:
            # Check if disclosed
            disclosed = False
            for app_loan in app_loans:
                if self.loans_match(discovered, app_loan):
                    disclosed = True
                    break
            
            if not disclosed:
                undisclosed.append({
                    "lender": discovered.lender,
                    "balance": discovered.current_balance,
                    "payment": discovered.monthly_payment,
                    "source": discovered.source,
                    "property": discovered.property_address
                })
        
        return undisclosed
    
    def normalize_account(self, account: str) -> str:
        """Normalize account number for comparison"""
        
        if not account:
            return ""
        
        # Remove non-alphanumeric
        return re.sub(r'[^a-zA-Z0-9]', '', account.upper())
    
    def lenders_match(self, lender1: str, lender2: str) -> bool:
        """Check if lender names refer to same institution"""
        
        if not lender1 or not lender2:
            return False
        
        # Normalize
        l1 = lender1.lower()
        l2 = lender2.lower()
        
        # Remove common suffixes
        suffixes = ["bank", "mortgage", "lending", "financial", "na", "n.a."]
        for suffix in suffixes:
            l1 = l1.replace(suffix, "").strip()
            l2 = l2.replace(suffix, "").strip()
        
        # Check exact match
        if l1 == l2:
            return True
        
        # Check if one contains the other
        if l1 in l2 or l2 in l1:
            return True
        
        return False
    
    def addresses_match(self, addr1: str, addr2: str) -> bool:
        """Check if property addresses match"""
        
        if not addr1 or not addr2:
            return False
        
        # Normalize
        a1 = addr1.lower().replace(",", "").replace(".", "")
        a2 = addr2.lower().replace(",", "").replace(".", "")
        
        # Standardize common abbreviations
        replacements = [
            ("street", "st"), ("avenue", "ave"), ("road", "rd"),
            ("drive", "dr"), ("apartment", "apt"), ("unit", "apt")
        ]
        
        for full, abbrev in replacements:
            a1 = a1.replace(full, abbrev)
            a2 = a2.replace(full, abbrev)
        
        # Remove extra spaces
        a1 = " ".join(a1.split())
        a2 = " ".join(a2.split())
        
        return a1 == a2
    
    def extract_application_loans(self, application: dict) -> List[PriorLoan]:
        """Extract loans from application"""
        
        loans = []
        for loan in application.get("existing_mortgages", []):
            loans.append(PriorLoan(
                lender=loan.get("lender", ""),
                account_number=loan.get("account_number", ""),
                original_amount=loan.get("original_amount", 0),
                current_balance=loan.get("current_balance", 0),
                monthly_payment=loan.get("monthly_payment", 0),
                property_address=loan.get("property_address", ""),
                source="application",
                as_of_date=date.today()
            ))
        return loans
    
    def extract_credit_loans(self, credit_report: dict) -> List[PriorLoan]:
        """Extract mortgage loans from credit report"""
        
        loans = []
        for account in credit_report.get("accounts", []):
            if account.get("account_type") == "mortgage":
                loans.append(PriorLoan(
                    lender=account.get("creditor", ""),
                    account_number=account.get("account_number", ""),
                    original_amount=account.get("original_amount", 0),
                    current_balance=account.get("balance", 0),
                    monthly_payment=account.get("monthly_payment", 0),
                    property_address=account.get("property_address", ""),
                    source="credit_report",
                    as_of_date=credit_report.get("pulled_date", date.today())
                ))
        return loans
    
    def extract_statement_loans(self, statements: list) -> List[PriorLoan]:
        """Extract loan info from mortgage statements"""
        
        loans = []
        for stmt in statements:
            if stmt.get("type") == "mortgage_statement":
                loans.append(PriorLoan(
                    lender=stmt.get("servicer", ""),
                    account_number=stmt.get("loan_number", ""),
                    original_amount=stmt.get("original_principal", 0),
                    current_balance=stmt.get("principal_balance", 0),
                    monthly_payment=stmt.get("payment_amount", 0),
                    property_address=stmt.get("property_address", ""),
                    source="statement",
                    as_of_date=stmt.get("statement_date", date.today())
                ))
        return loans
    
    def extract_title_liens(self, title_search: dict) -> List[PriorLoan]:
        """Extract liens from title search"""
        
        loans = []
        for lien in title_search.get("liens", []):
            loans.append(PriorLoan(
                lender=lien.get("lender", ""),
                account_number=lien.get("document_number", ""),
                original_amount=lien.get("amount", 0),
                current_balance=0,  # Title doesn't show current balance
                monthly_payment=0,
                property_address=title_search.get("property_address", ""),
                source="title",
                as_of_date=lien.get("recorded_date", date.today())
            ))
        return loans
```

### Risk Scoring for Prior Loan Issues

| Issue | Risk Score | Action |
|-------|------------|--------|
| Undisclosed lien | 0.4 | Application misrepresentation |
| Balance >$10K difference | 0.25 | Verify correct balance |
| Lender name mismatch | 0.15 | Verify same loan |
| Property address mismatch | 0.2 | Verify correct property |
| Payment amount differs | 0.1 | Update DTI calculation |
| Account number mismatch | 0.15 | Verify loan identity |

---

## References

- [Fannie Mae Prior Mortgage Documentation](https://selling-guide.fanniemae.com/)
- [Credit Report Standards](https://www.consumerfinance.gov/)
- [Title Insurance Requirements](https://www.alta.org/)
