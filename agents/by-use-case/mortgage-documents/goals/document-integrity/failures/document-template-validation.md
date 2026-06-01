# Document Template Validation

## Issue: AI System Fails to Verify Documents Match Expected Institution Templates

**Frequency**: Common

**Symptoms**
- Fake bank statement with generic layout
- W-2 missing required IRS elements
- Pay stub format doesn't match employer
- VOE form wrong version
- Institution logo incorrect or low quality
- Required fields in wrong locations

**Root Cause**
Legitimate documents follow specific templates. Bank statements have institution-specific layouts, W-2s follow IRS specifications, and pay stubs match employer payroll provider formats. AI systems should verify documents match expected templates, not just extract data from any format presented.

**Example**
```
Scenario 1: Fake bank statement template

Legitimate Chase statement:
- Logo: High resolution, top left
- Account number: Masked format ****1234
- Transaction table: Specific column order
- Footer: FDIC member, routing info
- Font: Proprietary Chase font

Submitted "Chase" statement:
- Logo: Low resolution, slightly different ← RED FLAG
- Account number: Full number shown ← RED FLAG
- Transaction table: Different column order ← RED FLAG
- Footer: Missing FDIC info ← RED FLAG
- Font: Arial (generic) ← RED FLAG

AI extraction:
- Bank: Chase ✓
- Balance: $45,000 ✓
- "Document validated" ✓

← Template mismatch not detected
← Likely fabricated document

---

Scenario 2: W-2 missing required elements

IRS W-2 requirements:
- Control number (Box d)
- Employer EIN (Box b)
- Employer address (Box c)
- All 12 boxes in specific layout
- OMB number present
- Form version year

Submitted W-2:
- Control number: Missing ← May be OK (optional)
- Employer EIN: Present ✓
- Employer address: Present ✓
- Box layout: Modified order ← RED FLAG
- OMB number: Wrong year ← RED FLAG
- Copy designation: None ← RED FLAG

Analysis:
- W-2 should be Copy B (employee copy)
- Form layout non-standard
- Could be edited or created

← Template violations suggest forgery

---

Scenario 3: Pay stub doesn't match payroll provider

VOE states: "Payroll processed by ADP"

ADP pay stub characteristics:
- ADP logo present
- Specific earning code format
- Check number format: 10 digits
- YTD calculation style
- Deduction category layout

Submitted pay stub:
- No ADP logo ← MISMATCH
- Generic earning codes ← MISMATCH
- Check number: 6 digits ← MISMATCH
- Different YTD format ← MISMATCH

Conclusion:
- Pay stub not from ADP
- Either wrong employer or fake
- VOE and pay stub conflict

← Pay stub template doesn't match stated payroll provider

---

Scenario 4: VOE form version

Current requirements:
- Fannie Mae Form 1005
- Version: 09/2023 or later
- All sections completed
- Employer signature/title

Submitted VOE:
- Form 1005 ✓
- Version: 03/2019 ← OUTDATED
- Missing sections ← INCOMPLETE
- Signature present ✓

Issues:
- Old form version may lack required fields
- Missing income breakdown
- May not meet current guidelines

← Outdated form template

---

Template validation points:

  Document Type | Template Source | Key Checks
  --------------|-----------------|------------
  W-2           | IRS             | Box layout, OMB, copy
  Bank statement| Institution     | Logo, layout, footer
  Pay stub      | Payroll provider| Format, logo, codes
  Tax return    | IRS             | Form version, barcode
  VOE           | Fannie/Freddie  | Form number, version
  1099          | IRS             | Box layout, payer info
  
  Common fake document indicators:
  - Generic sans-serif fonts
  - Low resolution logos
  - Missing regulatory disclosures
  - Incorrect form versions
  - Non-standard field layouts
  - Missing barcodes/checksums
```

**Key Statistics**
From Template Analysis (2025-2026):
- Documents with template issues: 3-5%
- Fake templates in fraud cases: 60-70%
- Template validation performed: 15-20%
- Outdated form versions: 5-8%
- Logo quality issues: 2-3%

**Contributing Factors**
- No template library maintained
- Layout analysis not performed
- Logo verification missing
- Form version not checked
- Institution-specific formatting unknown
- Required elements not validated

---

## Mitigation Strategies

### Prevention
1. **Template library**: Maintain expected templates
2. **Layout analysis**: Compare document structure
3. **Logo verification**: Check logo quality and placement
4. **Version checking**: Verify form versions current
5. **Element validation**: Required fields present
6. **Institution matching**: Verify format matches institution

### Implementation
```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import imagehash
from PIL import Image

class TemplateMatchResult(Enum):
    MATCH = "match"
    PARTIAL = "partial_match"
    MISMATCH = "mismatch"
    UNKNOWN = "unknown_template"

@dataclass
class TemplateCheckResult:
    element: str
    expected: str
    found: str
    status: str
    confidence: float

class DocumentTemplateValidator:
    """Validate documents against expected templates"""
    
    # Template definitions
    TEMPLATES = {
        "w2": {
            "required_elements": [
                "employer_ein", "employer_address", 
                "employee_ssn", "employee_address",
                "box1_wages", "box2_federal_tax"
            ],
            "layout": {
                "employer_section": "top_left",
                "employee_section": "top_right", 
                "wage_boxes": "middle",
                "tax_boxes": "lower"
            },
            "omb_number": "1545-0008",
            "valid_years": [2023, 2024, 2025]
        },
        "bank_statement": {
            "required_elements": [
                "institution_logo", "account_number",
                "statement_period", "beginning_balance",
                "ending_balance", "transaction_table"
            ],
            "institution_specific": True
        }
    }
    
    # Known institution templates
    INSTITUTION_TEMPLATES = {
        "chase": {
            "logo_hash": "abc123...",  # Perceptual hash
            "logo_position": "top_left",
            "account_format": r"\*{4}\d{4}",
            "font_family": "Chase Sans",
            "required_footer": ["FDIC", "JPMorgan Chase Bank"]
        },
        "wells_fargo": {
            "logo_hash": "def456...",
            "logo_position": "top_center",
            "account_format": r"\*{4}\d{4}",
            "required_footer": ["FDIC", "Wells Fargo Bank"]
        }
    }
    
    def validate_document(self, 
                         document: dict,
                         doc_type: str,
                         institution: Optional[str] = None) -> dict:
        """Validate document against expected template"""
        
        result = {
            "template_match": TemplateMatchResult.UNKNOWN,
            "checks": [],
            "issues": [],
            "risk_score": 0.0
        }
        
        template = self.TEMPLATES.get(doc_type)
        if not template:
            return result
        
        # Check required elements
        for element in template.get("required_elements", []):
            check = self.check_element(document, element)
            result["checks"].append(check)
            
            if check.status == "missing":
                result["issues"].append(f"missing_{element}")
                result["risk_score"] += 0.1
        
        # Check layout
        if layout := template.get("layout"):
            layout_check = self.verify_layout(document, layout)
            result["checks"].extend(layout_check)
            
            layout_issues = [c for c in layout_check if c.status != "correct"]
            if layout_issues:
                result["issues"].append("layout_mismatch")
                result["risk_score"] += 0.2
        
        # Check form version
        if "omb_number" in template:
            omb_check = self.verify_omb(document, template["omb_number"])
            result["checks"].append(omb_check)
            if omb_check.status != "correct":
                result["issues"].append("wrong_omb_number")
                result["risk_score"] += 0.15
        
        # Institution-specific validation
        if institution and template.get("institution_specific"):
            inst_result = self.validate_institution_template(
                document, 
                institution
            )
            result["checks"].extend(inst_result["checks"])
            result["issues"].extend(inst_result["issues"])
            result["risk_score"] += inst_result["risk_score"]
        
        # Determine overall match
        issue_count = len(result["issues"])
        if issue_count == 0:
            result["template_match"] = TemplateMatchResult.MATCH
        elif issue_count <= 2:
            result["template_match"] = TemplateMatchResult.PARTIAL
        else:
            result["template_match"] = TemplateMatchResult.MISMATCH
        
        result["risk_score"] = min(result["risk_score"], 1.0)
        
        return result
    
    def validate_institution_template(self,
                                      document: dict,
                                      institution: str) -> dict:
        """Validate against institution-specific template"""
        
        result = {
            "checks": [],
            "issues": [],
            "risk_score": 0.0
        }
        
        template = self.INSTITUTION_TEMPLATES.get(institution.lower())
        if not template:
            return result
        
        # Check logo
        if logo := document.get("logo_image"):
            logo_check = self.verify_logo(logo, template)
            result["checks"].append(logo_check)
            
            if logo_check.status == "mismatch":
                result["issues"].append("logo_mismatch")
                result["risk_score"] += 0.3
            elif logo_check.status == "low_quality":
                result["issues"].append("low_quality_logo")
                result["risk_score"] += 0.25
        
        # Check account format
        if account := document.get("account_number"):
            import re
            pattern = template.get("account_format", "")
            if not re.match(pattern, account):
                result["checks"].append(TemplateCheckResult(
                    element="account_format",
                    expected=pattern,
                    found=account,
                    status="mismatch",
                    confidence=0.9
                ))
                result["issues"].append("account_format_mismatch")
                result["risk_score"] += 0.2
        
        # Check required footer elements
        footer_text = document.get("footer_text", "").lower()
        for required in template.get("required_footer", []):
            if required.lower() not in footer_text:
                result["checks"].append(TemplateCheckResult(
                    element=f"footer_{required}",
                    expected=required,
                    found="missing",
                    status="missing",
                    confidence=0.95
                ))
                result["issues"].append(f"missing_footer_{required}")
                result["risk_score"] += 0.15
        
        return result
    
    def verify_logo(self, logo_image, template: dict) -> TemplateCheckResult:
        """Verify institution logo matches expected"""
        
        # Calculate perceptual hash
        try:
            img = Image.open(logo_image)
            logo_hash = str(imagehash.phash(img))
            expected_hash = template.get("logo_hash", "")
            
            # Compare hashes (lower distance = more similar)
            distance = imagehash.hex_to_hash(logo_hash) - \
                       imagehash.hex_to_hash(expected_hash)
            
            if distance < 5:
                status = "match"
            elif distance < 15:
                status = "similar"
            else:
                status = "mismatch"
            
            # Check resolution
            if img.width < 100 or img.height < 50:
                status = "low_quality"
            
            return TemplateCheckResult(
                element="logo",
                expected=expected_hash[:8],
                found=logo_hash[:8],
                status=status,
                confidence=1.0 - (distance / 64)
            )
            
        except Exception:
            return TemplateCheckResult(
                element="logo",
                expected="valid_logo",
                found="unreadable",
                status="error",
                confidence=0.0
            )
    
    def verify_layout(self, 
                      document: dict,
                      expected_layout: dict) -> List[TemplateCheckResult]:
        """Verify document layout matches expected"""
        
        results = []
        
        # Would use OCR bounding boxes to verify positions
        detected_layout = document.get("detected_layout", {})
        
        for element, expected_position in expected_layout.items():
            actual_position = detected_layout.get(element)
            
            if actual_position:
                match = self.positions_match(expected_position, actual_position)
                results.append(TemplateCheckResult(
                    element=f"layout_{element}",
                    expected=expected_position,
                    found=actual_position,
                    status="correct" if match else "incorrect",
                    confidence=0.8
                ))
            else:
                results.append(TemplateCheckResult(
                    element=f"layout_{element}",
                    expected=expected_position,
                    found="not_detected",
                    status="missing",
                    confidence=0.5
                ))
        
        return results
    
    def check_element(self, 
                      document: dict,
                      element: str) -> TemplateCheckResult:
        """Check if required element is present"""
        
        value = document.get(element)
        
        if value:
            return TemplateCheckResult(
                element=element,
                expected="present",
                found="present",
                status="present",
                confidence=1.0
            )
        else:
            return TemplateCheckResult(
                element=element,
                expected="present",
                found="missing",
                status="missing",
                confidence=1.0
            )
    
    def verify_omb(self, 
                   document: dict,
                   expected_omb: str) -> TemplateCheckResult:
        """Verify OMB number on IRS forms"""
        
        found_omb = document.get("omb_number", "")
        
        if found_omb == expected_omb:
            status = "correct"
        elif found_omb:
            status = "incorrect"
        else:
            status = "missing"
        
        return TemplateCheckResult(
            element="omb_number",
            expected=expected_omb,
            found=found_omb,
            status=status,
            confidence=1.0
        )
    
    def positions_match(self, expected: str, actual: str) -> bool:
        """Check if layout positions match"""
        
        return expected.lower() == actual.lower()
```

### Risk Scoring for Template Issues

| Issue | Risk Score | Action |
|-------|------------|--------|
| Logo mismatch | 0.3 | Verify document source |
| Layout mismatch | 0.25 | May be fabricated |
| Missing required element | 0.1 | Request complete document |
| Wrong form version | 0.15 | Request current version |
| Missing FDIC disclosure | 0.2 | Verify bank authenticity |
| Low quality logo | 0.25 | May be copied/edited |

---

## References

- [IRS Form Standards](https://www.irs.gov/forms-instructions)
- [FDIC Disclosure Requirements](https://www.fdic.gov/)
- [Fannie Mae Form Library](https://singlefamily.fanniemae.com/media/document/pdf/uniform-instruments)
