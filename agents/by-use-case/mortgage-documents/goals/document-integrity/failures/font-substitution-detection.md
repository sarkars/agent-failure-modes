# Font Substitution Detection

## Issue: AI System Fails to Detect Font Inconsistencies Indicating Document Tampering

**Frequency**: Occasional

**Symptoms**
- Different fonts used within same field
- Font family changes mid-document
- Edited text uses different font than original
- Font rendering differs from expected
- Character spacing anomalies
- Font embedding inconsistencies

**Root Cause**
Official documents use consistent fonts throughout. When fraudsters edit PDFs to change amounts or dates, the replacement text often uses a different font—even if visually similar. AI systems that don't analyze font metadata miss these tampering indicators.

**Example**
```
Scenario 1: W-2 wages edited with different font

Original W-2:
- Employer name: Courier New (IRS standard)
- Box 1 Wages: Courier New
- Box 2 Tax: Courier New

Altered W-2:
- Employer name: Courier New ✓
- Box 1 Wages: Arial ← DIFFERENT FONT
- Box 2 Tax: Courier New ✓

Visual appearance:
- Numbers look similar
- Spacing slightly different
- AI OCR reads correctly

Font analysis:
- Document uses 2 fonts
- Critical field (wages) different font
- Font substitution detected

← Wages field was edited
← Original amount replaced

---

Scenario 2: Bank statement balance manipulation

Expected bank statement fonts:
- Header: Proprietary bank font
- Body: Arial/Helvetica
- Numbers: Fixed-width (Consolas)

Submitted statement:
- Header: Expected ✓
- Body: Expected ✓
- Balance: Times New Roman ← MISMATCH

Analysis:
- Balance field uses different font family
- Fixed-width numbers expected for alignment
- Proportional font indicates editing

← Balance was changed
← Font doesn't match template

---

Scenario 3: Character-level font mixing

Pay stub gross pay field:

Analysis at character level:
- "$" - Arial, 11pt
- "6" - Arial, 11pt
- "5" - Arial Black, 11pt ← Different weight
- "," - Arial, 11pt
- "0" - Helvetica, 11pt ← Different family
- "0" - Arial, 11pt
- "0" - Arial, 11pt

Interpretation:
- Original: $35,000
- Changed to: $65,000
- "5" inserted (different weight)
- "6" edited (different family)

← Character-level editing detected
← Multiple font anomalies in one field

---

Scenario 4: Font embedding analysis

PDF font objects:

/Font <<
  /F1 (Courier) [embedded]
  /F2 (Arial) [embedded]
  /F3 (ArialMT) [subset embedded]  ← Suspicious
>>

Usage:
- F1: 95% of text
- F2: 4% of text (headers)
- F3: 1% of text ← Only in amount fields

Red flags:
- ArialMT subset only has digits 0-9
- Minimal character set = editing tool
- Used only in critical fields

← Editing tool embedded minimal font
← Only numbers were changed

---

Font consistency rules by document:

  Document Type  | Expected Fonts        | Red Flags
  ---------------|-----------------------|----------------
  W-2            | Courier, OCR-A        | Proportional fonts
  Tax Return     | Times, Courier        | Sans-serif in data
  Bank Statement | Institution-specific  | Mixed families
  Pay Stub       | Varies by provider    | Multiple families
  1099           | Courier, OCR-A        | Non-standard fonts
  
  Font tampering indicators:
  - More than 3 fonts in simple document
  - Different font in numeric fields only
  - Subset fonts with limited glyphs
  - Font weight changes within field
  - Character spacing anomalies
```

**Key Statistics**
From Font Analysis Studies (2025-2026):
- Documents with font inconsistencies: 2-4%
- Font anomalies in fraud cases: 35-45%
- AI systems checking fonts: 10-15%
- Font substitution detection accuracy: 85-90%

**Contributing Factors**
- Font metadata not extracted
- Character-level analysis not performed
- Font embedding not validated
- Visual similarity trusted over metadata
- PDF font objects not parsed
- Expected fonts not defined per document type

---

## Mitigation Strategies

### Prevention
1. **Font extraction**: Parse all PDF font objects
2. **Consistency checking**: Compare fonts across document
3. **Expected fonts**: Define valid fonts per document type
4. **Character analysis**: Check fonts at character level
5. **Subset detection**: Flag minimal character subsets
6. **Glyph comparison**: Compare character rendering

### Implementation
```python
from collections import defaultdict
from typing import List, Dict, Set

class FontAnalyzer:
    """Analyze document fonts for tampering indicators"""
    
    EXPECTED_FONTS = {
        "w2": {
            "required": ["Courier", "OCR-A", "OCR-B"],
            "allowed": ["Helvetica", "Arial"],
            "forbidden": ["Comic Sans", "Brush Script"]
        },
        "tax_return": {
            "required": [],
            "allowed": ["Times", "Courier", "Arial", "Helvetica"],
            "forbidden": []
        },
        "bank_statement": {
            "required": [],
            "allowed": [],  # Institution-specific
            "forbidden": []
        }
    }
    
    CRITICAL_FIELDS = [
        "wages", "income", "balance", "amount",
        "gross", "net", "total", "tax"
    ]
    
    def analyze_fonts(self, pdf_document: dict) -> dict:
        """Analyze fonts in PDF document"""
        
        result = {
            "fonts_found": [],
            "font_usage": {},
            "anomalies": [],
            "risk_indicators": [],
            "risk_score": 0.0
        }
        
        # Extract font objects
        fonts = self.extract_fonts(pdf_document)
        result["fonts_found"] = fonts
        
        # Analyze font usage by region
        usage = self.analyze_font_usage(pdf_document, fonts)
        result["font_usage"] = usage
        
        # Check for anomalies
        anomalies = self.detect_anomalies(
            fonts,
            usage,
            pdf_document.get("type", "unknown")
        )
        result["anomalies"] = anomalies
        
        # Check critical fields
        critical_field_issues = self.check_critical_fields(
            pdf_document,
            fonts
        )
        if critical_field_issues:
            result["anomalies"].extend(critical_field_issues)
            result["risk_score"] += 0.3
        
        # Calculate risk
        if len(fonts) > 3:
            result["risk_indicators"].append("excessive_fonts")
            result["risk_score"] += 0.1
        
        for anomaly in anomalies:
            if anomaly["severity"] == "high":
                result["risk_score"] += 0.25
            elif anomaly["severity"] == "medium":
                result["risk_score"] += 0.15
        
        result["risk_score"] = min(result["risk_score"], 1.0)
        
        return result
    
    def extract_fonts(self, document: dict) -> List[dict]:
        """Extract font objects from PDF"""
        
        fonts = []
        
        # Parse PDF font resources
        font_objects = document.get("font_objects", [])
        
        for font_obj in font_objects:
            font_info = {
                "name": font_obj.get("BaseFont", "Unknown"),
                "type": font_obj.get("Subtype", "Unknown"),
                "embedded": font_obj.get("FontDescriptor") is not None,
                "subset": self.is_subset_font(font_obj),
                "glyphs": self.count_glyphs(font_obj),
                "encoding": font_obj.get("Encoding", "Standard")
            }
            fonts.append(font_info)
        
        return fonts
    
    def is_subset_font(self, font_obj: dict) -> bool:
        """Check if font is subset embedded"""
        
        base_font = font_obj.get("BaseFont", "")
        
        # Subset fonts have random prefix like ABCDEF+FontName
        if "+" in base_font:
            prefix = base_font.split("+")[0]
            if len(prefix) == 6 and prefix.isupper():
                return True
        
        return False
    
    def count_glyphs(self, font_obj: dict) -> int:
        """Count number of glyphs in embedded font"""
        
        # Would parse actual font data
        # Return character set size
        widths = font_obj.get("Widths", [])
        return len(widths)
    
    def analyze_font_usage(self, 
                          document: dict,
                          fonts: list) -> dict:
        """Analyze where each font is used"""
        
        usage = defaultdict(lambda: {
            "count": 0,
            "regions": [],
            "fields": []
        })
        
        # Parse text content with font info
        text_objects = document.get("text_objects", [])
        
        for text_obj in text_objects:
            font_name = text_obj.get("font")
            text = text_obj.get("text", "")
            bbox = text_obj.get("bbox")  # Bounding box
            
            usage[font_name]["count"] += len(text)
            usage[font_name]["regions"].append(bbox)
            
            # Identify if in critical field
            for field in self.CRITICAL_FIELDS:
                if field in text.lower():
                    usage[font_name]["fields"].append(field)
        
        return dict(usage)
    
    def detect_anomalies(self,
                        fonts: list,
                        usage: dict,
                        doc_type: str) -> list:
        """Detect font-related anomalies"""
        
        anomalies = []
        
        # Check against expected fonts
        expected = self.EXPECTED_FONTS.get(doc_type, {})
        font_names = [f["name"].lower() for f in fonts]
        
        # Check forbidden fonts
        for forbidden in expected.get("forbidden", []):
            if any(forbidden.lower() in fn for fn in font_names):
                anomalies.append({
                    "type": "forbidden_font",
                    "font": forbidden,
                    "severity": "high"
                })
        
        # Check for subset fonts with minimal glyphs
        for font in fonts:
            if font["subset"] and font["glyphs"] < 15:
                anomalies.append({
                    "type": "minimal_subset",
                    "font": font["name"],
                    "glyphs": font["glyphs"],
                    "severity": "high",
                    "reason": "Editing tool signature"
                })
        
        # Check for font used only in numeric context
        for font_name, use in usage.items():
            text_sample = "".join(
                str(r) for r in use.get("regions", [])[:5]
            )
            if use["count"] < 20 and any(
                f in use.get("fields", []) 
                for f in self.CRITICAL_FIELDS
            ):
                anomalies.append({
                    "type": "isolated_font_in_critical_field",
                    "font": font_name,
                    "fields": use["fields"],
                    "severity": "high"
                })
        
        return anomalies
    
    def check_critical_fields(self,
                             document: dict,
                             fonts: list) -> list:
        """Check fonts in critical fields specifically"""
        
        issues = []
        
        # Get primary font (most used)
        usage = document.get("font_usage", {})
        if usage:
            primary_font = max(usage.keys(), key=lambda k: usage[k]["count"])
        else:
            return issues
        
        # Check fields that should match primary font
        field_extractions = document.get("extracted_fields", {})
        
        for field_name, field_data in field_extractions.items():
            if any(cf in field_name.lower() for cf in self.CRITICAL_FIELDS):
                field_font = field_data.get("font")
                
                if field_font and field_font != primary_font:
                    issues.append({
                        "type": "critical_field_font_mismatch",
                        "field": field_name,
                        "expected_font": primary_font,
                        "found_font": field_font,
                        "severity": "high"
                    })
        
        return issues
    
    def compare_character_rendering(self,
                                    char1: dict,
                                    char2: dict) -> dict:
        """Compare rendering of same character"""
        
        # Would analyze actual glyph shapes
        return {
            "match": True,
            "differences": []
        }
```

### Risk Scoring for Font Issues

| Issue | Risk Score | Action |
|-------|------------|--------|
| Different font in amount field | 0.35 | Fraud investigation |
| Minimal subset font | 0.3 | Enhanced review |
| Forbidden font for doc type | 0.25 | Verify authenticity |
| Multiple font families | 0.15 | Note anomaly |
| Font weight inconsistency | 0.2 | Character analysis |
| Isolated font in critical field | 0.35 | Investigation |

---

## References

- [PDF Font Specification](https://www.adobe.com/devnet/pdf/pdf_reference.html)
- [OpenType Specification](https://docs.microsoft.com/en-us/typography/opentype/spec/)
- [Document Forensics](https://www.nist.gov/)
