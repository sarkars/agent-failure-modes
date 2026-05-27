# Employment History Gap Detection Failures

## Issue: OCR System Fails to Detect or Flag Gaps in Employment History

**Frequency**: Common

**Symptoms**
- Employment gaps not identified
- Overlapping employment dates missed
- Job tenure not calculated correctly
- Self-employment periods undetected
- Unemployment periods not flagged
- Seasonal employment not recognized

**Root Cause**
Mortgage guidelines require 2-year employment history with gaps explained. OCR extracts dates from various documents but doesn't correlate employment timeline, identify gaps, or verify continuity. Unexplained gaps can indicate undisclosed issues affecting qualification.

**Example**
```
Scenario 1: Undisclosed employment gap

W-2s provided:
- 2024: ABC Corp ($75,000)
- 2025: XYZ Inc ($82,000)

Employment dates extracted:
- ABC Corp: Jan 2023 - Aug 2024
- XYZ Inc: Feb 2025 - Present

OCR: Two employers, income extracted ✓
Gap: Sep 2024 - Jan 2025 (5 months unexplained)

← What happened during 5-month gap?
← Unemployment? Self-employment? Disability?
← No gap detection performed

---

Scenario 2: Overlapping employment

Resume shows:
- Company A: 2020-2024
- Company B: 2023-Present

Both show simultaneous full-time employment 2023-2024

OCR: Employment history extracted ✓
Issue: Overlapping dates not flagged

← Was one part-time?
← Resume exaggeration?
← Needs clarification

---

Scenario 3: Self-employment not identified

VOE shows:
- Current employer: Smith Consulting LLC
- Employee: John Smith
- Start date: 2020

OCR: Employed since 2020 ✓
Reality: John Smith OWNS Smith Consulting LLC

← Self-employed, not W-2 employee
← Requires different income documentation
← Schedule C, 2 years tax returns needed

---

Employment history failures:
  
  Documents with employment issues: 12%
  
  Issue types:
    Gap detection failures: 35%
    Tenure calculation errors: 25%
    Self-employment missed: 20%
    Overlap not flagged: 12%
    Seasonal employment issues: 8%
  
  Impact:
    Additional documentation: 10%
    Qualification impact: 5%
    Undisclosed issues: 3%
```

**Key Statistics**
From Employment Verification Research (2026):
- Unexplained employment gaps: 8-12%
- Self-employment misclassification: 5-8%
- Tenure calculation errors: 10-15%
- Gap-related qualification issues: 3-5%

**Contributing Factors**
- No timeline construction
- Gap threshold not defined
- Self-employment indicators missed
- Overlap detection absent
- Multiple job handling errors

---

## Mitigation Strategies

### Prevention
1. **Timeline construction**: Build complete employment timeline
2. **Gap detection**: Flag unexplained periods
3. **Self-employment detection**: Owner/employee indicators
4. **Tenure calculation**: Accurate duration computation
5. **Overlap validation**: Flag concurrent employment

### Implementation
```python
class EmploymentHistoryAnalyzer:
    """Analyze employment history for gaps and issues"""
    
    REQUIRED_HISTORY_MONTHS = 24
    GAP_THRESHOLD_DAYS = 31  # Gaps > 1 month need explanation
    
    SELF_EMPLOYMENT_INDICATORS = [
        "owner", "president", "founder", "member",
        "sole proprietor", "partner", "principal"
    ]
    
    def build_timeline(self, employments: list) -> dict:
        """Build employment timeline and detect gaps"""
        sorted_emp = sorted(employments, key=lambda x: x["start_date"])
        
        gaps = []
        prev_end = None
        
        for emp in sorted_emp:
            if prev_end:
                gap_days = (emp["start_date"] - prev_end).days
                
                if gap_days > self.GAP_THRESHOLD_DAYS:
                    gaps.append({
                        "start": prev_end,
                        "end": emp["start_date"],
                        "days": gap_days,
                        "explanation_required": True
                    })
            
            prev_end = emp.get("end_date") or date.today()
        
        return {
            "timeline": sorted_emp,
            "gaps": gaps,
            "total_history_months": self.calculate_history_months(sorted_emp),
            "meets_requirement": len(gaps) == 0 or all(
                g.get("explained") for g in gaps
            )
        }
    
    def detect_self_employment(self, employment: dict) -> dict:
        """Detect if employment is actually self-employment"""
        title = employment.get("title", "").lower()
        company = employment.get("company", "").lower()
        employee_name = employment.get("employee_name", "").lower()
        
        # Check title indicators
        for indicator in self.SELF_EMPLOYMENT_INDICATORS:
            if indicator in title:
                return {
                    "self_employed": True,
                    "indicator": f"title contains '{indicator}'",
                    "documentation_required": ["schedule_c", "tax_returns_2yr"]
                }
        
        # Check if employee name is in company name
        name_parts = employee_name.split()
        for part in name_parts:
            if len(part) > 2 and part in company:
                return {
                    "self_employed": True,
                    "indicator": "employee name matches company name",
                    "documentation_required": ["schedule_c", "tax_returns_2yr"]
                }
        
        return {"self_employed": False}
    
    def detect_overlaps(self, employments: list) -> list:
        """Detect overlapping employment periods"""
        overlaps = []
        
        for i, emp1 in enumerate(employments):
            for emp2 in employments[i+1:]:
                if self.dates_overlap(emp1, emp2):
                    overlaps.append({
                        "employer1": emp1["company"],
                        "employer2": emp2["company"],
                        "overlap_period": self.get_overlap_period(emp1, emp2),
                        "clarification_needed": True
                    })
        
        return overlaps
```

---

## References

- [Fannie Mae B3-3.1](https://selling-guide.fanniemae.com/) - Employment requirements
- [Freddie Mac 5302](https://guide.freddiemac.com/) - Employment history
- [CFPB ATR](https://www.consumerfinance.gov/) - Income verification
