# Document Date Correlation

## Issue: AI System Fails to Verify Document Dates Align with Stated Timeline

**Frequency**: Occasional

**Symptoms**
- Pay stub from future date
- W-2 year doesn't match tax return year
- Bank statement period doesn't cover required timeframe
- VOE dated after stated employment end
- Appraisal dated before contract
- Documents from impossible timeline

**Root Cause**
Mortgage document packages have internal timeline requirements. Pay stubs must be recent, W-2s must match tax return years, and bank statements must cover specific periods. AI systems that extract dates without correlating them across the package miss impossible timelines that indicate fraud or errors.

**Example**
```
Scenario 1: Future-dated pay stub

Application submitted: March 15, 2025

Pay stub provided:
- Pay period: March 16-31, 2025 ← FUTURE
- Pay date: March 31, 2025 ← FUTURE

AI extraction:
- Gross pay: $4,500 ✓
- YTD: $13,500 ✓
- "Valid pay stub" ✓

Problem:
- Pay stub is for future pay period
- Cannot exist at submission time
- Fabricated document

← Future date not flagged
← Impossible timeline

---

Scenario 2: W-2 vs Tax Return year mismatch

Tax return provided:
- Form 1040
- Tax year: 2024
- Line 1 wages: $95,000

W-2 provided:
- Tax year: 2023 ← WRONG YEAR
- Box 1 wages: $92,000

AI correlation:
- Tax return income: $95,000
- W-2 income: $92,000
- "Slight variance within tolerance" ✓

Problem:
- W-2 is from wrong year
- Cannot match 2024 return with 2023 W-2
- Should request 2024 W-2

← Year mismatch not detected
← Documents from different tax years

---

Scenario 3: Bank statement coverage gap

Requirement: 60-day asset seasoning

Application date: April 15, 2025
Required coverage: February 15 - April 15, 2025

Bank statements provided:
- January 1-31, 2025 ← TOO OLD
- February 1-28, 2025 ✓
- (March missing) ← GAP
- April 1-15, 2025 ✓

Coverage analysis:
- January: Not needed
- February: Covered ✓
- March: MISSING ←
- April: Partially covered ✓

← March statement missing
← Cannot verify 60-day seasoning

---

Scenario 4: Appraisal before contract

Timeline:
- Purchase contract: March 10, 2025
- Appraisal: February 28, 2025 ← BEFORE CONTRACT

Issue:
- How can property be appraised before contract?
- Appraisal should be ordered after contract
- Suggests recycled appraisal

Possible explanations:
1. Appraisal from failed transaction
2. Contract date error
3. Fraudulent timeline

← Appraisal cannot predate contract

---

Scenario 5: VOE dated after employment ended

Application states:
- Current employer: ABC Corp
- Position: Active employee

VOE shows:
- Employer: ABC Corp
- Hire date: January 2020
- Termination date: February 2025 ← TERMINATED
- VOE signed: March 10, 2025 ← AFTER TERMINATION

Problem:
- Applicant claims current employment
- VOE shows terminated in February
- Documents contradict employment status

← Employment ended before application
← Possible misrepresentation

---

Document timeline requirements:

  Document      | Timing Rule
  --------------|------------------------------------------
  Pay stub      | Within 30 days of application
  W-2           | Most recent tax year (or current)
  Tax return    | Most recent 2 years
  Bank statement| Cover 60 days before application
  VOE           | Within 120 days, employment current
  Appraisal     | After contract, within 120 days
  Credit report | Within 120 days of closing
  Title         | After appraisal, before closing
  
  Impossible timelines:
  - Future dates (beyond submission)
  - Appraisal before contract
  - VOE before hire date
  - Statement after account closed
  - Tax return before year end
```

**Key Statistics**
From Document Timeline Analysis (2025-2026):
- Documents with date issues: 8-12%
- Future-dated documents: 1-2%
- Missing coverage periods: 5-7%
- Year mismatches: 3-5%
- Impossible timelines (fraud): 0.5-1%

**Contributing Factors**
- Dates extracted but not correlated
- Timeline rules not enforced
- Coverage gaps not calculated
- Future dates not flagged
- Year mismatches overlooked
- Document relationships not understood

---

## Mitigation Strategies

### Prevention
1. **Timeline construction**: Build document chronology
2. **Coverage validation**: Verify required periods covered
3. **Future date detection**: Flag impossible dates
4. **Year matching**: Ensure tax years align
5. **Relationship rules**: Enforce document order
6. **Gap detection**: Identify missing periods

### Implementation
```python
from datetime import date, timedelta
from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple
from enum import Enum

class DateIssueType(Enum):
    FUTURE_DATE = "future_date"
    YEAR_MISMATCH = "year_mismatch"
    COVERAGE_GAP = "coverage_gap"
    SEQUENCE_ERROR = "sequence_error"
    IMPOSSIBLE_TIMELINE = "impossible_timeline"
    STALE_DOCUMENT = "stale_document"

@dataclass
class DateIssue:
    type: DateIssueType
    document: str
    expected: str
    found: str
    severity: str

class DocumentDateValidator:
    """Validate document dates and timeline correlation"""
    
    FRESHNESS_REQUIREMENTS = {
        "pay_stub": 30,      # days
        "bank_statement": 60,
        "voe": 120,
        "appraisal": 120,
        "credit_report": 120,
        "title": 30
    }
    
    DOCUMENT_SEQUENCE = [
        ("contract", "appraisal"),      # appraisal after contract
        ("appraisal", "title"),         # title after appraisal
        ("voe", "closing"),             # VOE before closing
        ("credit_report", "closing")    # credit before closing
    ]
    
    def validate_timeline(self, 
                         documents: list,
                         application_date: date,
                         contract_date: Optional[date] = None,
                         closing_date: Optional[date] = None) -> dict:
        """Validate complete document timeline"""
        
        result = {
            "issues": [],
            "coverage_analysis": {},
            "sequence_analysis": [],
            "risk_score": 0.0
        }
        
        # Extract all dates
        doc_dates = self.extract_dates(documents)
        
        # Check for future dates
        future = self.check_future_dates(doc_dates, application_date)
        result["issues"].extend(future)
        
        # Check freshness
        stale = self.check_freshness(doc_dates, application_date)
        result["issues"].extend(stale)
        
        # Check year alignment
        year_issues = self.check_year_alignment(documents)
        result["issues"].extend(year_issues)
        
        # Check coverage periods
        coverage = self.check_coverage(documents, application_date)
        result["coverage_analysis"] = coverage
        if coverage.get("gaps"):
            for gap in coverage["gaps"]:
                result["issues"].append(DateIssue(
                    type=DateIssueType.COVERAGE_GAP,
                    document="bank_statement",
                    expected=f"Coverage from {gap['start']} to {gap['end']}",
                    found="Missing",
                    severity="medium"
                ))
        
        # Check document sequence
        if contract_date:
            sequence = self.check_sequence(
                doc_dates, 
                contract_date,
                closing_date
            )
            result["sequence_analysis"] = sequence
            result["issues"].extend(sequence)
        
        # Calculate risk
        for issue in result["issues"]:
            if issue.severity == "critical":
                result["risk_score"] += 0.4
            elif issue.severity == "high":
                result["risk_score"] += 0.25
            elif issue.severity == "medium":
                result["risk_score"] += 0.15
        
        result["risk_score"] = min(result["risk_score"], 1.0)
        
        return result
    
    def check_future_dates(self, 
                          doc_dates: dict,
                          reference_date: date) -> List[DateIssue]:
        """Check for impossible future dates"""
        
        issues = []
        
        for doc_type, dates in doc_dates.items():
            doc_date = dates.get("date")
            
            if doc_date and doc_date > reference_date:
                issues.append(DateIssue(
                    type=DateIssueType.FUTURE_DATE,
                    document=doc_type,
                    expected=f"On or before {reference_date}",
                    found=str(doc_date),
                    severity="critical"
                ))
            
            # Check period dates
            period_end = dates.get("period_end")
            if period_end and period_end > reference_date:
                issues.append(DateIssue(
                    type=DateIssueType.FUTURE_DATE,
                    document=f"{doc_type} period",
                    expected=f"Period ending on or before {reference_date}",
                    found=str(period_end),
                    severity="critical"
                ))
        
        return issues
    
    def check_freshness(self,
                       doc_dates: dict,
                       reference_date: date) -> List[DateIssue]:
        """Check documents meet freshness requirements"""
        
        issues = []
        
        for doc_type, max_age in self.FRESHNESS_REQUIREMENTS.items():
            if doc_type in doc_dates:
                doc_date = doc_dates[doc_type].get("date")
                
                if doc_date:
                    age = (reference_date - doc_date).days
                    
                    if age > max_age:
                        issues.append(DateIssue(
                            type=DateIssueType.STALE_DOCUMENT,
                            document=doc_type,
                            expected=f"Within {max_age} days",
                            found=f"{age} days old",
                            severity="medium"
                        ))
        
        return issues
    
    def check_year_alignment(self, documents: list) -> List[DateIssue]:
        """Check tax year alignment across documents"""
        
        issues = []
        
        # Group by tax year
        w2_years = set()
        tax_return_years = set()
        
        for doc in documents:
            doc_type = doc.get("type")
            
            if doc_type == "w2":
                year = doc.get("tax_year")
                if year:
                    w2_years.add(year)
            
            elif doc_type == "tax_return":
                year = doc.get("tax_year")
                if year:
                    tax_return_years.add(year)
        
        # Each tax return year should have matching W-2
        for return_year in tax_return_years:
            if return_year not in w2_years:
                issues.append(DateIssue(
                    type=DateIssueType.YEAR_MISMATCH,
                    document=f"W-2 for {return_year}",
                    expected=f"W-2 for tax year {return_year}",
                    found=f"W-2s only for years: {w2_years}",
                    severity="high"
                ))
        
        return issues
    
    def check_coverage(self,
                       documents: list,
                       application_date: date) -> dict:
        """Check bank statement coverage"""
        
        result = {
            "required_start": None,
            "required_end": None,
            "covered_periods": [],
            "gaps": []
        }
        
        # Calculate required period
        required_days = self.FRESHNESS_REQUIREMENTS.get("bank_statement", 60)
        result["required_start"] = application_date - timedelta(days=required_days)
        result["required_end"] = application_date
        
        # Collect bank statement periods
        periods = []
        for doc in documents:
            if doc.get("type") == "bank_statement":
                period_start = doc.get("period_start")
                period_end = doc.get("period_end")
                
                if period_start and period_end:
                    periods.append((period_start, period_end))
        
        # Sort by start date
        periods.sort(key=lambda p: p[0])
        result["covered_periods"] = periods
        
        # Find gaps
        if periods:
            # Check start coverage
            if periods[0][0] > result["required_start"]:
                result["gaps"].append({
                    "start": str(result["required_start"]),
                    "end": str(periods[0][0])
                })
            
            # Check internal gaps
            for i in range(len(periods) - 1):
                if periods[i][1] < periods[i + 1][0] - timedelta(days=1):
                    result["gaps"].append({
                        "start": str(periods[i][1]),
                        "end": str(periods[i + 1][0])
                    })
            
            # Check end coverage
            if periods[-1][1] < result["required_end"]:
                result["gaps"].append({
                    "start": str(periods[-1][1]),
                    "end": str(result["required_end"])
                })
        
        return result
    
    def check_sequence(self,
                       doc_dates: dict,
                       contract_date: date,
                       closing_date: Optional[date]) -> List[DateIssue]:
        """Check document sequence requirements"""
        
        issues = []
        
        # Add reference dates
        dates = dict(doc_dates)
        dates["contract"] = {"date": contract_date}
        if closing_date:
            dates["closing"] = {"date": closing_date}
        
        for before, after in self.DOCUMENT_SEQUENCE:
            if before in dates and after in dates:
                before_date = dates[before].get("date")
                after_date = dates[after].get("date")
                
                if before_date and after_date:
                    if before_date > after_date:
                        issues.append(DateIssue(
                            type=DateIssueType.SEQUENCE_ERROR,
                            document=after,
                            expected=f"After {before} ({before_date})",
                            found=str(after_date),
                            severity="high"
                        ))
        
        # Specific check: appraisal before contract
        if "appraisal" in doc_dates:
            appraisal_date = doc_dates["appraisal"].get("date")
            if appraisal_date and appraisal_date < contract_date:
                issues.append(DateIssue(
                    type=DateIssueType.IMPOSSIBLE_TIMELINE,
                    document="appraisal",
                    expected=f"After contract date ({contract_date})",
                    found=f"Dated {appraisal_date}",
                    severity="critical"
                ))
        
        return issues
    
    def extract_dates(self, documents: list) -> Dict[str, dict]:
        """Extract all dates from documents"""
        
        dates = {}
        
        for doc in documents:
            doc_type = doc.get("type")
            
            dates[doc_type] = {
                "date": doc.get("document_date"),
                "period_start": doc.get("period_start"),
                "period_end": doc.get("period_end"),
                "tax_year": doc.get("tax_year")
            }
        
        return dates
```

### Risk Scoring for Date Issues

| Issue | Risk Score | Action |
|-------|------------|--------|
| Future date | 0.5 | Reject - impossible |
| Appraisal before contract | 0.4 | Investigation |
| Tax year mismatch | 0.3 | Request correct year |
| Coverage gap | 0.2 | Request missing period |
| Stale document | 0.15 | Request fresh copy |
| Sequence error | 0.25 | Verify timeline |

---

## References

- [Fannie Mae Document Age Requirements](https://selling-guide.fanniemae.com/)
- [Freddie Mac Documentation](https://guide.freddiemac.com/)
- [TRID Timing Requirements](https://www.consumerfinance.gov/rules-policy/regulations/1026/)
