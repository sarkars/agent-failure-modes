# PDF Modification Detection

## Issue: AI System Fails to Detect Post-Creation Edits to PDF Documents

**Frequency**: Common

**Symptoms**
- Edited PDFs accepted as authentic
- Modification timestamps not checked
- Incremental saves not analyzed
- Text layer edits undetected
- Image replacements missed
- Font changes overlooked

**Root Cause**
PDF files maintain internal structure that reveals modifications. Incremental saves, object stream changes, and metadata updates indicate post-creation editing. AI systems that only extract visible content miss these forensic indicators. Fraudsters use PDF editors to alter amounts, dates, and names while maintaining visual appearance.

**Example**
```
Scenario 1: Incremental save reveals editing

Original bank statement PDF:
- Created: 2025-03-15 09:30:00
- Modified: 2025-03-15 09:30:00
- Producer: Bank Statement Generator v3.2
- PDF version: 1.7

Submitted PDF:
- Created: 2025-03-15 09:30:00  ← Original date preserved
- Modified: 2025-04-02 14:22:00  ← EDITED 18 days later
- Producer: Adobe Acrobat Pro 2024
- PDF version: 1.7

Internal structure:
- 2 incremental saves detected
- Object 45 (text stream) modified
- Font substitution in object 12
- XRef table shows additions

AI extraction:
- Balance: $48,500 ✓ (extracted)
- Document valid ✓

← Modification not flagged
← Should trigger investigation

---

Scenario 2: Text layer manipulation

Pay stub PDF analysis:

Layer 1 (Image):
- Scanned document image
- Gross pay shows: $3,200

Layer 2 (Text):
- OCR/Text layer
- Gross pay text: $6,200  ← MISMATCH

Detection method:
- Extract image, OCR independently
- Compare to embedded text layer
- $3,000 discrepancy

← Text layer edited without changing image
← Common in scanned document fraud

---

Scenario 3: Object-level forensics

W-2 PDF internal objects:

Object 1: Document catalog
Object 5: Page content
Object 12: Font (Helvetica)
Object 15: Font (ArialMT)  ← SUSPICIOUS
Object 23: Text stream (wages)
  - "85000" inserted at position 234
  - Font reference: Object 15
Object 24: Text stream (employer)
  - Font reference: Object 12

Analysis:
- Two different fonts in same document
- Wages field uses different font than employer
- ArialMT not typical for official W-2

← Font inconsistency indicates editing
← Official forms use consistent fonts

---

Scenario 4: Creation metadata analysis

Tax return PDF metadata:

Stated: "E-filed 04/15/2025"

PDF metadata:
- Creator: Microsoft Word  ← RED FLAG
- Producer: PDF-XChange
- Created: 2025-04-20  ← After claimed filing date
- Custom metadata: Empty

Expected for IRS e-file:
- Creator: IRS e-file System
- Producer: IRS PDF Generator
- Created: On or before filing date
- Custom metadata: DCN, timestamps

← Document likely fabricated
← Not actual IRS-generated return

---

PDF forensic indicators:

  Indicator          | Clean Doc | Tampered Doc
  -------------------|-----------|-------------
  Incremental saves  | 0-1       | 2+
  Modification date  | = Created | > Created
  Font count         | Consistent| Multiple added
  Object additions   | None      | New objects
  Producer string    | Expected  | PDF editor
  XRef integrity     | Valid     | Modified
  Linearized         | Often yes | Often no
```

**Key Statistics**
From PDF Forensics Studies (2025-2026):
- PDFs with detectable modifications: 3-5% of submissions
- Fraudulent modifications caught: 40-60% (when checked)
- AI systems checking PDF structure: 10-15%
- Average time between creation and modification (fraud): 5-15 days

**Contributing Factors**
- PDF treated as static image
- Metadata not extracted or analyzed
- Internal structure not parsed
- Text layer not compared to image
- Incremental saves not detected
- Producer string not validated

---

## Mitigation Strategies

### Prevention
1. **Parse PDF structure**: Analyze objects, XRefs, streams
2. **Check metadata**: Compare creation/modification dates
3. **Validate producer**: Match expected software
4. **Count incremental saves**: Flag multiple saves
5. **Font analysis**: Detect substitutions
6. **Text-image comparison**: OCR image, compare to text layer

### Implementation
```python
import hashlib
from datetime import datetime
from typing import Optional

class PDFForensicAnalyzer:
    """Analyze PDF for signs of modification"""
    
    EXPECTED_PRODUCERS = {
        "w2": ["IRS", "ADP", "Paychex", "QuickBooks"],
        "tax_return": ["IRS", "TurboTax", "H&R Block", "TaxAct"],
        "bank_statement": ["Bank", "Statement", "Financial"],
        "pay_stub": ["ADP", "Paychex", "Gusto", "Paylocity"]
    }
    
    def analyze_pdf(self, pdf_path: str, doc_type: str) -> dict:
        """Perform forensic analysis on PDF"""
        
        result = {
            "metadata": {},
            "structure": {},
            "modifications": [],
            "risk_indicators": [],
            "risk_score": 0.0
        }
        
        # Extract metadata
        metadata = self.extract_metadata(pdf_path)
        result["metadata"] = metadata
        
        # Check creation vs modification
        if metadata.get("modified") and metadata.get("created"):
            created = metadata["created"]
            modified = metadata["modified"]
            
            if modified > created:
                time_diff = (modified - created).days
                result["modifications"].append({
                    "type": "date_mismatch",
                    "created": str(created),
                    "modified": str(modified),
                    "days_between": time_diff
                })
                
                if time_diff > 1:
                    result["risk_indicators"].append("modified_after_creation")
                    result["risk_score"] += 0.3
        
        # Check producer
        producer = metadata.get("producer", "")
        expected = self.EXPECTED_PRODUCERS.get(doc_type, [])
        
        if not any(exp.lower() in producer.lower() for exp in expected):
            if "adobe" in producer.lower() or "pdf-" in producer.lower():
                result["risk_indicators"].append("pdf_editor_used")
                result["risk_score"] += 0.35
        
        # Analyze structure
        structure = self.analyze_structure(pdf_path)
        result["structure"] = structure
        
        # Check incremental saves
        if structure.get("incremental_saves", 0) > 1:
            result["risk_indicators"].append("multiple_saves")
            result["risk_score"] += 0.25
        
        # Check fonts
        fonts = structure.get("fonts", [])
        if len(set(fonts)) > 3:  # Too many different fonts
            result["risk_indicators"].append("font_inconsistency")
            result["risk_score"] += 0.2
        
        # Text layer vs image comparison
        text_image_match = self.compare_text_to_image(pdf_path)
        if not text_image_match["matches"]:
            result["risk_indicators"].append("text_image_mismatch")
            result["risk_score"] += 0.4
            result["modifications"].append({
                "type": "text_layer_edited",
                "discrepancies": text_image_match["discrepancies"]
            })
        
        result["risk_score"] = min(result["risk_score"], 1.0)
        
        return result
    
    def extract_metadata(self, pdf_path: str) -> dict:
        """Extract PDF metadata"""
        
        # Using PyPDF2 or similar
        metadata = {
            "created": None,
            "modified": None,
            "producer": "",
            "creator": "",
            "title": "",
            "author": ""
        }
        
        # Parse PDF and extract /Info dictionary
        # ...implementation with PDF library...
        
        return metadata
    
    def analyze_structure(self, pdf_path: str) -> dict:
        """Analyze PDF internal structure"""
        
        structure = {
            "incremental_saves": 0,
            "object_count": 0,
            "fonts": [],
            "xref_valid": True,
            "linearized": False,
            "encrypted": False
        }
        
        # Count %%EOF markers (indicates incremental saves)
        with open(pdf_path, 'rb') as f:
            content = f.read()
            structure["incremental_saves"] = content.count(b'%%EOF')
        
        # Parse object structure
        # Extract font references
        # Validate XRef table
        # ...implementation...
        
        return structure
    
    def compare_text_to_image(self, pdf_path: str) -> dict:
        """Compare embedded text layer to OCR of image"""
        
        result = {
            "matches": True,
            "discrepancies": []
        }
        
        # Extract text layer
        text_layer = self.extract_text_layer(pdf_path)
        
        # Render to image and OCR
        image = self.render_to_image(pdf_path)
        ocr_text = self.ocr_image(image)
        
        # Compare key fields
        # Amount fields are most critical
        text_amounts = self.extract_amounts(text_layer)
        ocr_amounts = self.extract_amounts(ocr_text)
        
        for field, text_val in text_amounts.items():
            ocr_val = ocr_amounts.get(field)
            if ocr_val and text_val != ocr_val:
                result["matches"] = False
                result["discrepancies"].append({
                    "field": field,
                    "text_layer": text_val,
                    "ocr_value": ocr_val
                })
        
        return result
    
    def calculate_file_hash(self, pdf_path: str) -> dict:
        """Calculate multiple hashes for verification"""
        
        with open(pdf_path, 'rb') as f:
            content = f.read()
        
        return {
            "md5": hashlib.md5(content).hexdigest(),
            "sha256": hashlib.sha256(content).hexdigest(),
            "size": len(content)
        }
```

### Risk Scoring for PDF Modifications

| Indicator | Risk Score | Reason |
|-----------|------------|--------|
| Modified after creation (>1 day) | 0.3 | Likely edited |
| PDF editor in producer | 0.35 | Tool for tampering |
| Multiple incremental saves | 0.25 | Multiple edit sessions |
| Text-image mismatch | 0.4 | Text layer edited |
| Font inconsistency | 0.2 | Possible text replacement |
| Missing expected metadata | 0.15 | May be fabricated |

---

## References

- [PDF Specification ISO 32000-2](https://www.iso.org/standard/75839.html)
- [PDF Forensics Techniques](https://www.nist.gov/)
- [Adobe PDF Security](https://www.adobe.com/security.html)
