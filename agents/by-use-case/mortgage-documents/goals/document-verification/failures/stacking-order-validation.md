# Stacking Order Validation Failures

## Issue: OCR System Fails to Validate Document Stacking Order and Sequence

**Frequency**: Common

**Symptoms**
- Documents in wrong sequence not flagged
- Disclosure sequence violations missed
- Missing required documents in stack
- Duplicate documents not identified
- Version conflicts (outdated forms present)
- Investor stacking requirements not met

**Root Cause**
Mortgage document packages must follow specific stacking orders for compliance, investor requirements, and regulatory examinations. OCR systems typically process documents individually without validating sequence, leading to audit failures, investor rejections, and compliance issues.

**Example**
```
Scenario 1: Disclosure sequence violation

Required TRID sequence:
1. Loan Estimate (must precede CD)
2. Intent to Proceed (after LE)
3. Closing Disclosure (3 days before closing)

Actual document order in package:
1. Closing Disclosure
2. Loan Estimate (dated after CD!)
3. Intent to Proceed

OCR: All documents present ✓
Reality: Disclosure sequence violated

← LE dated after CD is impossible
← Intent to Proceed timing invalid
← Major compliance violation

---

Scenario 2: Investor stacking requirements

Fannie Mae requires:
1. Note (original)
2. Deed of Trust
3. Uniform Residential Appraisal
4. Title Policy
5. Closing Disclosure
... [specific order of 30+ documents]

Submitted package: Random order

OCR: Documents extracted
Issue: Won't pass investor quality control

---

Scenario 3: Duplicate versions

Package contains:
- Loan Estimate v1 (March 1)
- Loan Estimate v2 (March 5) 
- Loan Estimate v1 (March 1) - duplicate

OCR: Extracted all three as separate documents
Issue: Duplicate detected but not flagged

← Confusion about which version applies
← Storage bloat
← Audit trail unclear

---

Stacking order failures:
  
  Documents with stacking issues: 20%
  
  Issue types:
    Wrong sequence: 35%
    Missing documents: 25%
    Duplicates present: 20%
    Version conflicts: 15%
    Investor requirements not met: 5%
  
  Impact:
    Investor rejection: 8%
    Audit findings: 12%
    Re-sorting required: 15%
```

**Key Statistics**
From Mortgage Operations Research (2026):
- Stacking order issues: 15-25%
- Investor rejections (stacking): 5-10%
- Audit findings (sequence): 10-15%
- Re-work time: 15-30 min per file

**Contributing Factors**
- No sequence validation logic
- Document-by-document processing
- Missing document manifest
- Version control absent
- Investor rules not encoded

---

## Mitigation Strategies

### Prevention
1. **Stacking order rules**: Encode investor/compliance requirements
2. **Manifest validation**: Check against required document list
3. **Duplicate detection**: Hash-based comparison
4. **Version control**: Track document versions
5. **Sequence validation**: Date and order checks

### Implementation
```python
class StackingOrderValidator:
    """Validate document stacking order"""
    
    FANNIE_MAE_ORDER = [
        "promissory_note",
        "deed_of_trust",
        "uniform_residential_appraisal",
        "title_policy",
        "closing_disclosure",
        # ... full stacking order
    ]
    
    TRID_SEQUENCE = {
        "loan_estimate": {"before": ["closing_disclosure", "intent_to_proceed"]},
        "intent_to_proceed": {"after": ["loan_estimate"], "before": ["closing_disclosure"]},
        "closing_disclosure": {"after": ["loan_estimate", "intent_to_proceed"]}
    }
    
    def validate_trid_sequence(self, documents: list) -> dict:
        """Validate TRID disclosure sequence"""
        violations = []
        doc_dates = {d["type"]: d["date"] for d in documents}
        
        for doc_type, rules in self.TRID_SEQUENCE.items():
            if doc_type not in doc_dates:
                continue
                
            doc_date = doc_dates[doc_type]
            
            # Check "after" requirements
            for req in rules.get("after", []):
                if req in doc_dates and doc_dates[req] > doc_date:
                    violations.append({
                        "violation": f"{doc_type} dated before {req}",
                        "doc_date": doc_date,
                        "required_after": doc_dates[req]
                    })
        
        return {
            "valid": len(violations) == 0,
            "violations": violations
        }
    
    def detect_duplicates(self, documents: list) -> list:
        """Detect duplicate documents"""
        hashes = {}
        duplicates = []
        
        for doc in documents:
            doc_hash = self.compute_hash(doc["content"])
            if doc_hash in hashes:
                duplicates.append({
                    "document": doc["type"],
                    "duplicate_of": hashes[doc_hash]
                })
            else:
                hashes[doc_hash] = doc["type"]
        
        return duplicates
```

---

## References

- [Fannie Mae Selling Guide](https://selling-guide.fanniemae.com/) - Document requirements
- [Freddie Mac Guide](https://guide.freddiemac.com/) - Stacking requirements
- [CFPB TRID](https://www.consumerfinance.gov/rules-policy/regulations/1026/) - Disclosure sequence
