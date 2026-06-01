# Employment Timeline Conflicts

## Issue: AI System Fails to Detect Inconsistent Employment Dates Across Documents

**Frequency**: Common

**Symptoms**
- W-2 employer doesn't match current employer claim
- VOE start date differs from application
- Pay stub employer changed mid-processing
- Employment gaps not explained
- Overlapping employment dates impossible
- Tax return Schedule C conflicts with W-2 employment

**Root Cause**
Employment history appears across multiple documents: application, VOE, W-2s, pay stubs, tax returns, and credit report. Each source may show different dates or employers. AI systems must construct a coherent timeline and flag conflicts that indicate fraud or errors.

**Example**
```
Scenario 1: W-2 employer vs. current claim mismatch

Application claims (2025):
- Current employer: ABC Corporation
- Start date: January 2022
- Current position: 3+ years

W-2s provided:
- 2024: ABC Corporation ✓
- 2023: XYZ Industries ← DIFFERENT EMPLOYER
- 2022: XYZ Industries ← DIFFERENT EMPLOYER

Analysis:
- Applicant claims ABC Corp since Jan 2022
- W-2s show XYZ Industries in 2022-2023
- Switched to ABC Corp in 2024?

Possible explanations:
1. Application error
2. Job change not disclosed
3. Fraudulent employment history

← Timeline conflict requires explanation

---

Scenario 2: VOE contradicts application

Application:
- Employer: Tech Solutions Inc
- Start date: March 2020
- Position: Software Engineer

VOE from Tech Solutions:
- Employee name: ✓
- Start date: September 2022  ← 2.5 YEARS LATER
- Position: Junior Developer  ← DIFFERENT TITLE

Calculation impact:
- Application: 5 years employment (stability)
- VOE: 2.5 years (less stable)
- Position difference affects income projection

← VOE is authoritative source
← Application may be inflated

---

Scenario 3: Impossible overlapping employment

Document sources:

Employer 1 (W-2 2024):
- Company: Regional Bank
- Location: Chicago, IL
- Income: $75,000

Employer 2 (W-2 2024):
- Company: Financial Services Co
- Location: San Francisco, CA
- Income: $82,000

Pay stubs (current):
- Employer: Regional Bank
- Full-time: 40 hrs/week

Credit report employment:
- Financial Services Co: Current

Issue:
- Both appear as full-time
- Different cities
- Credit shows SF employer
- Pay stubs show Chicago

← One may be fabricated
← Cannot work full-time at both in different cities

---

Scenario 4: Self-employment timeline conflict

Application:
- Self-employed: January 2021 - Present
- Business: Consulting LLC
- No other employment

Tax returns show:
- 2024: Schedule C income (Consulting LLC) ✓
- 2023: W-2 income $45,000 from Corp X
         Schedule C income $30,000
- 2022: W-2 income $60,000 from Corp X

Analysis:
- Claims self-employed since 2021
- Tax returns show W-2 employment through 2023
- Transition was gradual, not as stated

Impact:
- Self-employment history shorter
- 2-year average SE income lower
- Qualifying income calculation changes

← Timeline affects income calculation

---

Employment timeline requirements:

  Document Source  | Date Type     | Authority
  -----------------|---------------|------------
  Application      | Self-reported | Lowest
  Pay Stub         | Current only  | Medium
  W-2              | Annual        | High
  VOE              | Verified      | Highest
  Tax Return       | Annual        | High
  Credit Report    | Historical    | Medium
  
  Timeline rules:
  - VOE dates override application
  - W-2 presence confirms employment that year
  - Gaps >30 days require explanation
  - Overlaps require verification (multiple jobs OK)
  - Self-employment + W-2 in same year is valid
```

**Key Statistics**
From Employment Verification (2025-2026):
- Employment date discrepancies: 10-15%
- Start date varies >6 months: 5-8%
- Employer name variations: 20-25%
- Undisclosed job changes: 3-5%
- Fraudulent employment history: 1-2%

**Contributing Factors**
- No timeline construction across documents
- Employer name normalization missing
- Date format variations mishandled
- VOE not used as authoritative source
- Multiple employers not aggregated
- Self-employment transitions not tracked

---

## Mitigation Strategies

### Prevention
1. **Timeline construction**: Build employment history from all sources
2. **Date reconciliation**: Normalize and compare all dates
3. **Employer matching**: Handle name variations
4. **Gap detection**: Flag unexplained gaps
5. **Overlap validation**: Verify concurrent employment possible
6. **Source weighting**: Prioritize VOE over application

### Implementation
```python
from datetime import date, timedelta
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Employment:
    employer: str
    start_date: date
    end_date: Optional[date]
    position: str
    source: str
    source_authority: float  # 0-1, higher = more authoritative
    location: Optional[str] = None
    full_time: bool = True

class EmploymentTimelineValidator:
    """Validate employment timeline across documents"""
    
    SOURCE_AUTHORITY = {
        "voe": 1.0,
        "w2": 0.9,
        "tax_return": 0.85,
        "pay_stub": 0.8,
        "credit_report": 0.6,
        "application": 0.5
    }
    
    def build_timeline(self, documents: list) -> dict:
        """Build employment timeline from all documents"""
        
        employments = []
        
        for doc in documents:
            doc_type = doc.get("type")
            authority = self.SOURCE_AUTHORITY.get(doc_type, 0.5)
            
            if doc_type == "application":
                for emp in doc.get("employment_history", []):
                    employments.append(Employment(
                        employer=self.normalize_employer(emp["employer"]),
                        start_date=emp["start_date"],
                        end_date=emp.get("end_date"),
                        position=emp.get("position", ""),
                        source="application",
                        source_authority=authority,
                        location=emp.get("location")
                    ))
            
            elif doc_type == "voe":
                employments.append(Employment(
                    employer=self.normalize_employer(doc["employer"]),
                    start_date=doc["hire_date"],
                    end_date=doc.get("termination_date"),
                    position=doc.get("position", ""),
                    source="voe",
                    source_authority=authority,
                    full_time=doc.get("full_time", True)
                ))
            
            elif doc_type == "w2":
                # W-2 confirms employment for that year
                tax_year = doc["tax_year"]
                employments.append(Employment(
                    employer=self.normalize_employer(doc["employer_name"]),
                    start_date=date(tax_year, 1, 1),
                    end_date=date(tax_year, 12, 31),
                    position="",  # W-2 doesn't have position
                    source="w2",
                    source_authority=authority
                ))
            
            elif doc_type == "pay_stub":
                employments.append(Employment(
                    employer=self.normalize_employer(doc["employer"]),
                    start_date=doc.get("hire_date", doc["pay_period_start"]),
                    end_date=None,  # Current
                    position=doc.get("position", ""),
                    source="pay_stub",
                    source_authority=authority
                ))
        
        # Sort by start date
        employments.sort(key=lambda e: e.start_date)
        
        return {
            "employments": employments,
            "timeline": self.merge_timeline(employments)
        }
    
    def validate_timeline(self, timeline: dict) -> dict:
        """Validate employment timeline for conflicts"""
        
        result = {
            "conflicts": [],
            "gaps": [],
            "risk_indicators": [],
            "risk_score": 0.0
        }
        
        employments = timeline["employments"]
        
        # Check for date conflicts
        for i, emp1 in enumerate(employments):
            for emp2 in employments[i+1:]:
                if self.same_employer(emp1.employer, emp2.employer):
                    conflict = self.check_date_conflict(emp1, emp2)
                    if conflict:
                        result["conflicts"].append(conflict)
        
        # Check for impossible overlaps
        overlaps = self.find_impossible_overlaps(employments)
        result["conflicts"].extend(overlaps)
        
        # Check for gaps
        gaps = self.find_gaps(employments)
        result["gaps"] = gaps
        
        # Check application vs VOE
        app_emp = [e for e in employments if e.source == "application"]
        voe_emp = [e for e in employments if e.source == "voe"]
        
        for app in app_emp:
            for voe in voe_emp:
                if self.same_employer(app.employer, voe.employer):
                    date_diff = abs((app.start_date - voe.start_date).days)
                    if date_diff > 180:  # 6 month variance
                        result["conflicts"].append({
                            "type": "start_date_conflict",
                            "employer": app.employer,
                            "application_date": str(app.start_date),
                            "voe_date": str(voe.start_date),
                            "difference_days": date_diff,
                            "severity": "high"
                        })
                        result["risk_score"] += 0.25
        
        # Calculate overall risk
        if result["conflicts"]:
            result["risk_indicators"].append("timeline_conflicts")
            result["risk_score"] += len(result["conflicts"]) * 0.15
        
        if len(gaps) > 0:
            total_gap_days = sum(g["days"] for g in gaps)
            if total_gap_days > 90:
                result["risk_indicators"].append("employment_gaps")
                result["risk_score"] += 0.2
        
        result["risk_score"] = min(result["risk_score"], 1.0)
        
        return result
    
    def find_impossible_overlaps(self, employments: list) -> list:
        """Find overlapping full-time employment in different locations"""
        
        overlaps = []
        
        full_time = [e for e in employments if e.full_time]
        
        for i, emp1 in enumerate(full_time):
            for emp2 in full_time[i+1:]:
                if self.same_employer(emp1.employer, emp2.employer):
                    continue
                
                # Check for date overlap
                if self.dates_overlap(emp1, emp2):
                    # Different locations?
                    if emp1.location and emp2.location:
                        if not self.same_location(emp1.location, emp2.location):
                            overlaps.append({
                                "type": "impossible_overlap",
                                "employer1": emp1.employer,
                                "employer2": emp2.employer,
                                "location1": emp1.location,
                                "location2": emp2.location,
                                "overlap_period": self.get_overlap_period(emp1, emp2),
                                "severity": "critical"
                            })
        
        return overlaps
    
    def find_gaps(self, employments: list) -> list:
        """Find gaps in employment history"""
        
        gaps = []
        
        # Sort by end date, filter to ended employments
        ended = [e for e in employments if e.end_date]
        ended.sort(key=lambda e: e.end_date)
        
        for i in range(len(ended) - 1):
            current_end = ended[i].end_date
            next_start = ended[i + 1].start_date
            
            gap_days = (next_start - current_end).days
            
            if gap_days > 30:  # Significant gap
                gaps.append({
                    "from_employer": ended[i].employer,
                    "to_employer": ended[i + 1].employer,
                    "gap_start": str(current_end),
                    "gap_end": str(next_start),
                    "days": gap_days
                })
        
        return gaps
    
    def normalize_employer(self, name: str) -> str:
        """Normalize employer name for matching"""
        
        name = name.lower().strip()
        
        # Remove common suffixes
        suffixes = [
            "inc", "inc.", "incorporated",
            "llc", "l.l.c.", "limited liability",
            "corp", "corp.", "corporation",
            "co", "co.", "company",
            "ltd", "ltd.", "limited"
        ]
        
        for suffix in suffixes:
            if name.endswith(f" {suffix}"):
                name = name[:-len(suffix)-1]
        
        return name.strip()
    
    def same_employer(self, name1: str, name2: str) -> bool:
        """Check if two employer names refer to same company"""
        
        n1 = self.normalize_employer(name1)
        n2 = self.normalize_employer(name2)
        
        if n1 == n2:
            return True
        
        # Check if one contains the other
        if n1 in n2 or n2 in n1:
            return True
        
        return False
    
    def dates_overlap(self, emp1: Employment, emp2: Employment) -> bool:
        """Check if two employments overlap in time"""
        
        end1 = emp1.end_date or date.today()
        end2 = emp2.end_date or date.today()
        
        return emp1.start_date <= end2 and emp2.start_date <= end1
```

### Risk Scoring for Employment Conflicts

| Conflict Type | Risk Score | Action |
|---------------|------------|--------|
| Start date differs >6 months | 0.25 | VOE authoritative |
| Impossible location overlap | 0.5 | Fraud investigation |
| Undisclosed employer | 0.3 | Request explanation |
| Employment gap >90 days | 0.2 | Document reason |
| W-2 missing for claimed employer | 0.35 | Verify employment |
| Position title conflict | 0.1 | Note discrepancy |

---

## References

- [Fannie Mae Employment Documentation](https://selling-guide.fanniemae.com/)
- [The Work Number](https://theworknumber.com/)
- [MISMO Employment Standards](https://www.mismo.org/)
