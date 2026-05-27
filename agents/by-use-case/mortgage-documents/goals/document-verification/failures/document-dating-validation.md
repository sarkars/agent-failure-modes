# Document Dating Validation Failures

## Issue: OCR System Fails to Validate Document Dates and Date Relationships

**Frequency**: Common

**Symptoms**
- Future-dated documents not flagged
- Pre-dated documents accepted
- Date inconsistencies across documents
- Effective date vs. signature date confusion
- Expiration date violations missed
- Business day calculations incorrect

**Root Cause**
Mortgage documents have complex date relationships—application dates, lock dates, disclosure dates, signing dates, and closing dates must align. OCR extracts dates individually without validating relationships, leading to compliance issues, invalid documents, and timeline violations.

**Example**
```
Scenario 1: Future-dated application

Application date extracted: April 15, 2026
Document received date: April 10, 2026
Processing date: April 10, 2026

← Application dated 5 days in the future
← Possible backdating attempt
← OCR didn't flag temporal impossibility

---

Scenario 2: Expired documents

Appraisal effective date: January 15, 2026
Closing date: July 20, 2026

FNMA rule: Appraisal valid for 180 days
Days elapsed: 186 days

OCR: Appraisal extracted ✓
Reality: Appraisal expired, needs recertification

---

Scenario 3: Rate lock expiration

Rate lock date: March 1, 2026
Lock period: 45 days
Lock expiration: April 15, 2026
Closing date: April 20, 2026

OCR: Dates extracted ✓
Reality: Closing 5 days after lock expiration

← Extension required
← Pricing impact
← OCR didn't calculate expiration

---

Scenario 4: Inconsistent closing dates

Closing Disclosure: March 15, 2026
HUD-1 Settlement: March 16, 2026
Note: March 15, 2026
Deed of Trust: March 15, 2026

← Which date is accurate?
← HUD-1 shows different date
← OCR didn't correlate dates

---

Document dating failures:
  
  Documents with date issues: 18%
  
  Issue types:
    Date inconsistencies: 35%
    Expired documents: 25%
    Future/impossible dates: 15%
    Effective vs signature confusion: 15%
    Business day errors: 10%
  
  Impact:
    Invalid documents: 5%
    Re-documentation: 10%
    Compliance findings: 8%
```

**Key Statistics**
From Mortgage Quality Control (2026):
- Date-related defects: 15-20%
- Expired document issues: 5-8%
- Date inconsistencies: 10-12%
- Compliance findings (dating): 5-10%

**Contributing Factors**
- No cross-document date validation
- Expiration rules not implemented
- Business day calculation missing
- Future date detection absent
- Document type date requirements unknown

---

## Mitigation Strategies

### Prevention
1. **Date relationship rules**: Define valid relationships
2. **Expiration tracking**: Document validity periods
3. **Cross-document validation**: Correlate all dates
4. **Temporal validation**: Flag impossible dates
5. **Business day awareness**: Apply correct calculations

### Implementation
```python
class DocumentDateValidator:
    """Validate document dates and relationships"""
    
    VALIDITY_PERIODS = {
        "appraisal": 180,  # days
        "credit_report": 120,
        "income_documentation": 120,
        "asset_documentation": 90,
        "title_commitment": 90
    }
    
    def validate_expiration(self, 
                           doc_type: str, 
                           doc_date: date,
                           closing_date: date) -> dict:
        """Check document not expired at closing"""
        validity = self.VALIDITY_PERIODS.get(doc_type)
        
        if validity:
            days_elapsed = (closing_date - doc_date).days
            
            if days_elapsed > validity:
                return {
                    "valid": False,
                    "error": "document_expired",
                    "doc_date": doc_date,
                    "closing_date": closing_date,
                    "days_elapsed": days_elapsed,
                    "max_validity": validity,
                    "action": "recertification_required"
                }
        
        return {"valid": True}
    
    def validate_date_relationships(self, documents: dict) -> list:
        """Validate date relationships across documents"""
        issues = []
        
        closing_date = documents.get("closing_date")
        application_date = documents.get("application_date")
        
        # Application must precede closing
        if application_date and closing_date:
            if application_date > closing_date:
                issues.append({
                    "error": "application_after_closing",
                    "application": application_date,
                    "closing": closing_date
                })
        
        # LE must precede CD
        le_date = documents.get("loan_estimate_date")
        cd_date = documents.get("closing_disclosure_date")
        
        if le_date and cd_date and le_date > cd_date:
            issues.append({
                "error": "le_after_cd",
                "le_date": le_date,
                "cd_date": cd_date
            })
        
        return issues
    
    def flag_impossible_dates(self, 
                              doc_date: date, 
                              processing_date: date) -> dict:
        """Flag dates that are temporally impossible"""
        if doc_date > processing_date:
            return {
                "valid": False,
                "error": "future_dated_document",
                "doc_date": doc_date,
                "received": processing_date,
                "risk": "high"
            }
        
        return {"valid": True}
```

---

## References

- [Fannie Mae Selling Guide B4-1.2-01](https://selling-guide.fanniemae.com/) - Document age requirements
- [CFPB TRID Timing](https://www.consumerfinance.gov/rules-policy/regulations/1026/) - Disclosure timing
- [Freddie Mac Guide 5601.2](https://guide.freddiemac.com/) - Document validity
