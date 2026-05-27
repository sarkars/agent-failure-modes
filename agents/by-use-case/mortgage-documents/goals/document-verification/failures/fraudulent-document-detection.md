# Fraudulent Document Detection Failures

## Issue: OCR System Fails to Detect Altered, Forged, or Fabricated Mortgage Documents

**Frequency**: Occasional but high-impact

**Symptoms**
- Altered income figures not flagged
- Photoshopped bank statements accepted
- Forged employer letters pass validation
- Manipulated tax returns undetected
- Synthetic identity documents approved
- Digitally edited signatures missed

**Root Cause**
Mortgage fraud often involves document manipulation—altering income on W-2s, inflating bank balances, forging employment letters, or creating synthetic identities. Standard OCR focuses on text extraction, not authenticity. Without fraud detection layers, altered documents pass through the pipeline undetected, leading to bad loans, regulatory violations, and financial losses.

**Example**
```
Scenario 1: Altered W-2 income

Original W-2 (from IRS records): $65,000
Submitted W-2 (applicant's copy): $95,000

← Applicant digitally altered Box 1 wages
← OCR extracted $95,000 (the altered value)
← No cross-reference to IRS transcript
← Loan approved based on falsified income

Detection points missed:
- Font inconsistency in altered digits
- JPEG artifacts around modified area
- Mismatch with 4506-T transcript
- DTI would have been too high with real income

---

Scenario 2: Fabricated bank statement

Submitted: Chase Bank statement showing $45,000 balance
Reality: Account doesn't exist at Chase

Red flags missed:
- Statement layout slightly off (wrong margins)
- Account number format invalid for Chase
- No micro-deposits for verification
- Logo resolution lower than authentic

---

Scenario 3: Forged employment letter

Letter states: "John Smith, Senior Engineer, $120,000/year"
Reality: John Smith never worked at this company

What OCR extracted:
- Employer name: TechCorp Inc.
- Title: Senior Engineer
- Salary: $120,000
- Status: Current employee

What wasn't checked:
- Company phone number goes to applicant's cell
- Email domain registered 2 weeks ago
- No LinkedIn presence for this company
- Letterhead downloaded from template site

---

Scenario 4: Synthetic identity

Documents show consistent identity across:
- Driver's license
- SSN card
- W-2s
- Bank statements

All documents fabricated for synthetic identity:
- SSN belongs to deceased person
- Address is a mail drop
- Employer is shell company
- Bank account opened with synthetic ID

← All documents "match" because all are fake
← No cross-reference to external databases

---

Fraud detection failure analysis:
  
  Fraudulent applications processed: 2-5%
  Fraud detected by OCR system: 15%
  Fraud detected by human review: 45%
  Fraud detected post-closing: 40%
  
  Common fraud types:
    Income inflation: 45%
    Asset misrepresentation: 25%
    Employment fraud: 15%
    Identity fraud: 10%
    Property fraud: 5%
  
  Detection failure cost:
    Average loss per fraudulent loan: $75,000
    Regulatory penalties: Variable
    Reputation damage: Significant
```

**Key Statistics**
From Mortgage Fraud Research (2026):
- Mortgage fraud rate: 0.5-2% of applications
- Fraud detected pre-closing: 40-60%
- Post-closing fraud discovery: 30-50%
- OCR-only detection rate: 10-20%
- Multi-layer detection rate: 70-85%

**Fraud Indicators**
| Indicator | Detection Method | OCR Limitation |
|-----------|-----------------|----------------|
| Altered digits | Font analysis | Text-only extraction |
| Fake letterhead | Template matching | No image verification |
| Invalid formats | Format validation | May not know formats |
| Synthetic identity | Cross-database check | No external queries |
| Photoshop artifacts | Image forensics | Not performed |

**Contributing Factors**
- OCR focuses on extraction, not verification
- No image forensics layer
- Missing cross-document validation
- No external database verification
- Human review bottlenecks
- Time pressure to close loans

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Altered W-2 | Modified income | Flag anomaly | Accept as-is |
| Fake statement | Template-based | Detect template | Extract data |
| Forged letter | Invalid employer | Flag for verification | Accept |
| Font mismatch | Edited document | Detect inconsistency | Miss |
| Cross-doc mismatch | Inconsistent income | Flag discrepancy | Not correlated |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Fraud detection rate | > 70% | Known fraud samples |
| False positive rate | < 5% | Legitimate flagged |
| Cross-doc correlation | > 95% | Mismatch detection |
| Altered doc detection | > 60% | Forensic test set |

---

## Mitigation Strategies

### Prevention
1. **Image forensics**: Detect manipulation artifacts
2. **Font consistency**: Analyze font uniformity
3. **Cross-document correlation**: Match income across sources
4. **External verification**: 4506-T, VOE, VOD
5. **Format validation**: Check document format standards
6. **Metadata analysis**: Check document creation metadata

### Implementation
```python
class FraudDetector:
    """Detect fraudulent mortgage documents"""
    
    INCOME_VARIANCE_THRESHOLD = 0.05  # 5% variance allowed
    
    def __init__(self):
        self.image_forensics = ImageForensicsEngine()
        self.font_analyzer = FontConsistencyAnalyzer()
        self.format_validator = DocumentFormatValidator()
    
    def analyze_document(self, document: dict) -> dict:
        """Comprehensive fraud analysis"""
        flags = []
        
        # Image-level analysis
        if document.get("image"):
            image_flags = self.image_forensics.analyze(document["image"])
            flags.extend(image_flags)
        
        # Font consistency
        font_flags = self.font_analyzer.check_consistency(document)
        flags.extend(font_flags)
        
        # Format validation
        format_flags = self.format_validator.validate(
            document["type"], 
            document["content"]
        )
        flags.extend(format_flags)
        
        # Cross-reference if available
        if document.get("verification_source"):
            xref_flags = self.cross_reference(
                document["content"],
                document["verification_source"]
            )
            flags.extend(xref_flags)
        
        return {
            "fraud_flags": flags,
            "risk_score": self.calculate_risk(flags),
            "recommendation": self.get_recommendation(flags)
        }
    
    def cross_reference_income(self, 
                               w2_income: float,
                               tax_transcript_income: float) -> dict:
        """Cross-reference W-2 with IRS transcript"""
        variance = abs(w2_income - tax_transcript_income) / tax_transcript_income
        
        if variance > self.INCOME_VARIANCE_THRESHOLD:
            return {
                "flag": "income_mismatch",
                "severity": "high",
                "w2_income": w2_income,
                "transcript_income": tax_transcript_income,
                "variance": variance,
                "action": "manual_review_required"
            }
        
        return {"flag": None, "verified": True}
    
    def detect_altered_digits(self, document_image) -> list:
        """Detect digitally altered numbers"""
        flags = []
        
        # Analyze numeric regions for:
        # - Font inconsistency
        # - JPEG artifacts
        # - Color depth variations
        # - Alignment anomalies
        
        numeric_regions = self.extract_numeric_regions(document_image)
        
        for region in numeric_regions:
            analysis = self.image_forensics.analyze_region(region)
            
            if analysis["manipulation_probability"] > 0.7:
                flags.append({
                    "flag": "potential_alteration",
                    "region": region["location"],
                    "confidence": analysis["manipulation_probability"],
                    "indicators": analysis["indicators"]
                })
        
        return flags


class CrossDocumentValidator:
    """Validate consistency across mortgage documents"""
    
    def validate_income_consistency(self, documents: dict) -> dict:
        """Check income matches across all sources"""
        income_sources = {
            "w2": documents.get("w2", {}).get("wages"),
            "paystub": documents.get("paystub", {}).get("ytd_gross"),
            "tax_return": documents.get("tax_return", {}).get("agi"),
            "employment_letter": documents.get("voe", {}).get("annual_salary"),
            "transcript": documents.get("4506t", {}).get("wages")
        }
        
        # Remove None values
        available = {k: v for k, v in income_sources.items() if v}
        
        if len(available) < 2:
            return {"status": "insufficient_sources"}
        
        # Check consistency
        values = list(available.values())
        max_val = max(values)
        min_val = min(values)
        variance = (max_val - min_val) / max_val
        
        if variance > 0.10:  # More than 10% variance
            return {
                "status": "mismatch",
                "severity": "high" if variance > 0.25 else "medium",
                "sources": available,
                "variance": variance,
                "action": "investigate_discrepancy"
            }
        
        return {"status": "consistent", "sources": available}
```

### Prompt Design
```yaml
instructions: |
  ## FRAUD DETECTION FOR MORTGAGE DOCUMENTS
  
  When processing mortgage documents, flag these red flags:
  
  DOCUMENT AUTHENTICITY:
  - Font inconsistencies within same document
  - Poor image quality on specific sections
  - Misaligned text or numbers
  - Unusual formatting for document type
  - Metadata showing recent creation/editing
  
  INCOME VERIFICATION:
  - W-2 income doesn't match 4506-T transcript
  - Paystub YTD doesn't align with W-2
  - Employment letter salary differs from W-2
  - Self-employment income lacks Schedule C support
  
  ASSET VERIFICATION:
  - Large deposits without documentation
  - Account numbers in wrong format for institution
  - Statement layout doesn't match bank's format
  - Balance inconsistent across statement pages
  
  IDENTITY:
  - SSN format invalid or recycled
  - Address is known mail drop
  - Employment unverifiable
  - Multiple applications with similar info
  
  FLAG for human review, don't auto-reject:
  High confidence fraud indicators require escalation.
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `fraud.detection_rate` | < 50% |
| `fraud.false_positive_rate` | > 10% |
| `fraud.post_closing_discovery` | > 1% |
| `fraud.cross_doc_mismatch` | > 5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Low Detection Rate | < 40% | P1 |
| High Post-Closing Fraud | > 2% | P1 |
| Income Mismatch Spike | > 10% | P2 |
| Verification Bypass | Any | P1 |

---

## References

- [FBI Mortgage Fraud Report](https://www.fbi.gov/investigate/white-collar-crime/mortgage-fraud) - Fraud patterns
- [CFPB Mortgage Origination](https://www.consumerfinance.gov/compliance/compliance-resources/mortgage-resources/) - Compliance
- [Fannie Mae Fraud Detection](https://singlefamily.fanniemae.com/originating-underwriting/fraud-prevention) - Industry practices
- [Document Forensics Research](https://arxiv.org/abs/2305.14902) - Image manipulation detection
