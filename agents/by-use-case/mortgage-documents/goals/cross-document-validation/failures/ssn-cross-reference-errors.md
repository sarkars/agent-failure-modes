# SSN Cross-Reference Errors

## Issue: AI System Fails to Properly Verify SSN Consistency Across Documents

**Frequency**: Common

**Symptoms**
- SSN extracted differently from different documents
- Partial SSN (XXX-XX-1234) not matched to full SSN
- SSN on tax documents doesn't match application
- Co-borrower SSN attributed to primary borrower
- OCR errors in SSN digits not detected
- SSN format variations cause false mismatches

**Root Cause**
Social Security Numbers appear on nearly every mortgage document but in different formats: full (123-45-6789), partial (XXX-XX-6789), or masked (***-**-6789). AI systems must normalize formats, handle partial matches, and cross-reference across all documents. OCR errors on a single digit can create false mismatches or, worse, miss actual identity fraud.

**Example**
```
Scenario 1: OCR error creates false mismatch

Application SSN: 123-45-6789

Document extractions:
- W-2: 123-45-6789 ✓
- Tax Return: 123-45-6789 ✓
- Bank Statement: 123-45-6789 ✓
- Pay Stub: 128-45-6789 ← OCR error (3→8)

AI result: SSN MISMATCH DETECTED
Manual review triggered

Investigation:
- Pay stub scan quality: Poor
- Digit "3" misread as "8"
- All other documents consistent

← False positive from OCR error
← Should validate against majority
← Quality-based confidence scoring needed

---

Scenario 2: Partial SSN not correlated

Application (full): 456-78-9012

Document formats:
- W-2: 456-78-9012 (full)
- Bank statement: ***-**-9012 (masked)
- Credit report: XXX-XX-9012 (partial)
- Pay stub: Last 4: 9012

AI extraction:
- W-2 SSN: 456-78-9012
- Bank SSN: "masked"
- Credit SSN: "partial"
- Pay stub SSN: "9012"

Correlation result:
- Only W-2 matched to application
- Other documents "no SSN found"

← Partial SSN matching not implemented
← Should verify last 4 digits match

---

Scenario 3: True SSN mismatch (fraud indicator)

Application: 789-01-2345

Document extractions:
- W-2: 789-01-2345 ✓
- Tax Return: 789-01-2345 ✓
- Credit Report: 789-01-2345 ✓
- Prior Employer W-2: 789-01-2346 ← ONE DIGIT OFF

Investigation:
- Typo on old W-2? 
- Different person's W-2?
- Synthetic identity?

Risk: Moderate to High
- Single digit could be typo
- But could be different person's income

← True mismatch requiring investigation
← Not OCR error (different document)

---

Scenario 4: Co-borrower SSN confusion

Joint application:
- Primary: John Smith, SSN: 111-22-3333
- Co-borrower: Jane Smith, SSN: 444-55-6666

Document assignment:
- John's W-2: 111-22-3333 ✓
- Jane's W-2: 444-55-6666 ✓
- Joint bank account: Both listed
- Tax return (MFJ): Both SSNs present

AI error:
- Extracted all SSNs
- Assigned Jane's W-2 income to John
- Doubled John's income incorrectly

← SSN-to-borrower mapping failed
← Income from wrong SSN counted

---

SSN validation matrix:

  Document         | SSN Format    | Verification
  -----------------|---------------|------------------
  Application      | Full          | Source of truth
  W-2              | Full          | Must match exactly
  Tax Return       | Full          | Must match exactly
  Credit Report    | Full or Last4 | Match available digits
  Bank Statement   | Masked/Last4  | Match last 4
  Pay Stub         | Varies        | Match available
  1099             | Full          | Must match exactly
  SSA-89           | Full          | IRS verification
```

**Key Statistics**
From SSN Verification Studies (2025-2026):
- SSN extraction errors: 2-4% of documents
- OCR errors on SSN digits: 1-2%
- Partial SSN not correlated: 15-20%
- True SSN mismatches (fraud): 0.5-1%
- Co-borrower SSN confusion: 3-5%

**Contributing Factors**
- Format normalization not applied
- Partial matching not implemented
- OCR confidence not considered
- Document-to-borrower mapping weak
- No majority validation
- Single error triggers full mismatch

---

## Mitigation Strategies

### Prevention
1. **Format normalization**: Strip dashes, convert to 9 digits
2. **Partial matching**: Match available digits
3. **Confidence scoring**: Weight by OCR quality
4. **Majority validation**: Compare across all documents
5. **Borrower assignment**: Map SSN to specific borrower
6. **IRS verification**: Use 4506-C transcript

### Implementation
```python
class SSNValidator:
    """Validate SSN consistency across documents"""
    
    def __init__(self):
        self.ssn_pattern = re.compile(r'\d{3}[-\s]?\d{2}[-\s]?\d{4}')
        self.partial_pattern = re.compile(r'[X*]{3}[-\s]?[X*]{2}[-\s]?\d{4}')
        self.last4_pattern = re.compile(r'(?:last\s*4|xxxx)[-:\s]*(\d{4})', re.I)
    
    def normalize_ssn(self, ssn_string: str) -> dict:
        """Normalize SSN to standard format"""
        
        if not ssn_string:
            return {"type": "missing", "value": None, "last4": None}
        
        # Remove formatting
        cleaned = re.sub(r'[-\s]', '', ssn_string)
        
        # Full SSN
        if re.match(r'^\d{9}$', cleaned):
            return {
                "type": "full",
                "value": cleaned,
                "last4": cleaned[-4:],
                "formatted": f"{cleaned[:3]}-{cleaned[3:5]}-{cleaned[5:]}"
            }
        
        # Masked/partial (XXX-XX-1234)
        partial_match = self.partial_pattern.search(ssn_string)
        if partial_match:
            last4 = re.search(r'\d{4}', ssn_string)
            return {
                "type": "partial",
                "value": None,
                "last4": last4.group() if last4 else None,
                "formatted": ssn_string
            }
        
        # Last 4 only
        last4_match = self.last4_pattern.search(ssn_string)
        if last4_match:
            return {
                "type": "last4",
                "value": None,
                "last4": last4_match.group(1),
                "formatted": f"XXX-XX-{last4_match.group(1)}"
            }
        
        return {"type": "invalid", "value": None, "last4": None}
    
    def validate_across_documents(self, 
                                   application_ssn: str,
                                   documents: list) -> dict:
        """Validate SSN across all documents"""
        
        result = {
            "application_ssn": self.normalize_ssn(application_ssn),
            "document_results": [],
            "mismatches": [],
            "ocr_quality_issues": [],
            "risk_score": 0.0
        }
        
        app_normalized = result["application_ssn"]
        
        for doc in documents:
            doc_ssn = doc.get("ssn")
            doc_type = doc.get("type")
            ocr_confidence = doc.get("ocr_confidence", 1.0)
            
            normalized = self.normalize_ssn(doc_ssn)
            
            match_result = self.compare_ssn(
                app_normalized,
                normalized,
                ocr_confidence
            )
            
            doc_result = {
                "document_type": doc_type,
                "ssn_found": normalized,
                "match_status": match_result["status"],
                "confidence": match_result["confidence"]
            }
            
            result["document_results"].append(doc_result)
            
            if match_result["status"] == "mismatch":
                result["mismatches"].append({
                    "document": doc_type,
                    "expected": app_normalized["formatted"],
                    "found": normalized["formatted"],
                    "ocr_confidence": ocr_confidence
                })
            
            if ocr_confidence < 0.9:
                result["ocr_quality_issues"].append(doc_type)
        
        # Calculate risk
        result["risk_score"] = self.calculate_risk(result)
        
        return result
    
    def compare_ssn(self, 
                    ssn1: dict, 
                    ssn2: dict,
                    ocr_confidence: float) -> dict:
        """Compare two SSNs with appropriate matching"""
        
        # Both full - exact match required
        if ssn1["type"] == "full" and ssn2["type"] == "full":
            if ssn1["value"] == ssn2["value"]:
                return {"status": "match", "confidence": 1.0}
            
            # Check for single digit OCR error
            diff_count = sum(
                1 for a, b in zip(ssn1["value"], ssn2["value"]) 
                if a != b
            )
            
            if diff_count == 1 and ocr_confidence < 0.95:
                return {
                    "status": "possible_ocr_error",
                    "confidence": 0.7,
                    "diff_count": diff_count
                }
            
            return {"status": "mismatch", "confidence": 1.0}
        
        # Partial match - compare last 4
        if ssn1.get("last4") and ssn2.get("last4"):
            if ssn1["last4"] == ssn2["last4"]:
                return {"status": "partial_match", "confidence": 0.9}
            else:
                return {"status": "mismatch", "confidence": 0.9}
        
        # Missing SSN in document
        if ssn2["type"] == "missing":
            return {"status": "not_found", "confidence": 0.0}
        
        return {"status": "unable_to_compare", "confidence": 0.0}
    
    def calculate_risk(self, validation_result: dict) -> float:
        """Calculate risk score based on validation"""
        
        risk = 0.0
        
        # Full mismatches are high risk
        full_mismatches = [
            m for m in validation_result["mismatches"]
            if m.get("ocr_confidence", 1.0) > 0.95
        ]
        risk += len(full_mismatches) * 0.4
        
        # OCR errors are lower risk
        ocr_errors = [
            m for m in validation_result["mismatches"]
            if m.get("ocr_confidence", 1.0) <= 0.95
        ]
        risk += len(ocr_errors) * 0.1
        
        # Critical documents matter more
        critical_docs = ["w2", "tax_return", "tax_transcript"]
        for mismatch in validation_result["mismatches"]:
            if mismatch["document"] in critical_docs:
                risk += 0.2
        
        return min(risk, 1.0)
    
    def assign_ssn_to_borrower(self, 
                               borrowers: list,
                               documents: list) -> dict:
        """Assign documents to correct borrower by SSN"""
        
        assignments = {b["name"]: [] for b in borrowers}
        unassigned = []
        
        borrower_ssns = {
            b["ssn"]: b["name"] for b in borrowers
        }
        
        for doc in documents:
            doc_ssn = self.normalize_ssn(doc.get("ssn"))
            
            if doc_ssn["type"] == "full":
                if doc_ssn["value"] in borrower_ssns:
                    borrower = borrower_ssns[doc_ssn["value"]]
                    assignments[borrower].append(doc)
                    continue
            
            # Try last 4 match
            if doc_ssn.get("last4"):
                for ssn, name in borrower_ssns.items():
                    if ssn.endswith(doc_ssn["last4"]):
                        assignments[name].append(doc)
                        break
                else:
                    unassigned.append(doc)
            else:
                unassigned.append(doc)
        
        return {
            "assignments": assignments,
            "unassigned": unassigned
        }
```

### Risk Scoring for SSN Issues

| Issue | Risk Score | Action |
|-------|------------|--------|
| Full SSN mismatch (high confidence) | 0.5 | Fraud investigation |
| Full SSN mismatch (low OCR quality) | 0.15 | Re-scan document |
| Last 4 mismatch | 0.3 | Verify with additional docs |
| Missing SSN in critical doc | 0.2 | Request clearer copy |
| Co-borrower SSN confusion | 0.25 | Manual review |
| Multiple single-digit errors | 0.35 | Quality review |

---

## References

- [SSA: Social Security Number Verification](https://www.ssa.gov/employer/ssnv.htm)
- [IRS Form 4506-C](https://www.irs.gov/forms-pubs/about-form-4506-c)
- [FCRA: Identity Verification](https://www.ftc.gov/legal-library/browse/statutes/fair-credit-reporting-act)
