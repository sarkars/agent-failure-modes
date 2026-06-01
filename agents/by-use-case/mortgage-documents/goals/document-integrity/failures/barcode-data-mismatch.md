# Barcode Data Mismatch

## Issue: AI System Fails to Detect When Visible Text Doesn't Match Encoded Barcode Data

**Frequency**: Common

**Symptoms**
- W-2 visible wages don't match barcode-encoded wages
- Tax return DCN barcode doesn't match form data
- Bank statement QR code contains different account info
- Pay stub barcode differs from printed amounts
- Document passed visual validation but barcode reveals tampering

**Root Cause**
Many mortgage documents contain barcodes or QR codes that encode key data for machine reading. When fraudsters alter visible text (changing $50,000 to $80,000), they often don't know about or can't modify the embedded barcode. AI systems that only OCR visible text miss this critical verification layer.

**Example**
```
Scenario 1: W-2 barcode vs. visible text

Visible W-2 fields:
- Box 1 Wages: $95,000
- Box 2 Federal Tax: $18,500
- Box 3 SS Wages: $95,000

Barcode data (Code 128):
- Wages: $65,000  ← MISMATCH
- Federal Tax: $12,800  ← MISMATCH
- SS Wages: $65,000  ← MISMATCH

AI extraction (OCR only):
- Income: $95,000 ✓

Problem:
- Fraudster altered visible amounts
- Original barcode unchanged
- AI didn't decode barcode
- $30,000 income inflation undetected

← Critical fraud indicator missed
← Barcode is ground truth

---

Scenario 2: Tax return DCN verification

IRS e-filed return:
- Visible DCN: 12345-67890-12345
- Visible AGI: $125,000
- 2D Barcode present

Barcode decoding:
- DCN: 12345-67890-12345 ✓ (matches)
- AGI: $125,000 ✓ (matches)
- SSN last 4: 5678 ✓
- Filing date: 04/15/2025 ✓

Result: Document authentic
← Barcode confirms data integrity

---

Scenario 3: Altered bank statement with QR

Bank statement header:
- Account: ****1234
- Statement period: March 2025
- Ending balance: $45,250

QR code (institution-specific):
- Account hash: ABC123XYZ
- Period: 2025-03
- Balance: $12,250  ← MISMATCH

Analysis:
- $33,000 balance inflation
- QR code encoded at generation
- Text layer modified after
- AI only read visible text

← Significant fraud detected via QR
← Balance inflated to meet reserves

---

Scenario 4: Pay stub with check verification barcode

Pay stub visible:
- Gross pay: $6,500
- Net pay: $4,850
- Check #: 10542

MICR/Barcode data:
- Amount: $3,200  ← MISMATCH
- Check #: 10542 ✓

Explanation:
- Pay stub gross inflated
- Check amount is actual deposit
- MICR encoding matches bank processing

← Pay stub altered
← Check data reveals true amount

---

Barcode types in mortgage documents:

  Document Type → Barcode Format:
  
  W-2 Forms → Code 128, 2D PDF417
    Contains: EIN, wages, withholdings
    
  Tax Returns (e-filed) → 2D barcode, DCN
    Contains: DCN, AGI, SSN hash
    
  Bank Statements → QR Code (institution-specific)
    Contains: Account hash, balance, period
    
  Pay Stubs → Code 39, QR (varies)
    Contains: Employee ID, amounts
    
  Checks → MICR (magnetic), Code 128
    Contains: Routing, account, check #, amount
    
  1099 Forms → 2D PDF417
    Contains: Payer TIN, amounts, recipient SSN
```

**Key Statistics**
From Document Fraud Detection (2025-2026):
- Documents with barcodes: 60-70% of standard forms
- Barcode tampering attempted: 5-8% of fraudulent documents
- Barcode mismatch detection rate: 15-25% (when checked)
- Documents with barcode not decoded: 70-80%

**Contributing Factors**
- Barcode decoding not implemented
- Multiple barcode formats not supported
- Low-quality scans make barcodes unreadable
- Barcode-to-field mapping undefined
- Only visual OCR performed
- No cross-reference between barcode and text

---

## Mitigation Strategies

### Prevention
1. **Decode all barcodes**: Support Code 128, PDF417, QR, DataMatrix
2. **Cross-reference**: Compare barcode data to visible text
3. **Flag mismatches**: Any variance is high-risk indicator
4. **Institution patterns**: Know which docs have barcodes
5. **Quality requirements**: Reject scans with unreadable barcodes
6. **Checksum validation**: Verify barcode internal checksums

### Implementation
```python
class BarcodeValidator:
    """Validate document barcodes against visible text"""
    
    DOCUMENT_BARCODE_FIELDS = {
        "w2": {
            "barcode_type": ["code128", "pdf417"],
            "fields": ["box1_wages", "box2_federal_tax", "ein"]
        },
        "tax_return": {
            "barcode_type": ["pdf417", "2d"],
            "fields": ["dcn", "agi", "ssn_last4"]
        },
        "bank_statement": {
            "barcode_type": ["qr"],
            "fields": ["account_hash", "ending_balance", "period"]
        },
        "pay_stub": {
            "barcode_type": ["code39", "qr"],
            "fields": ["net_pay", "employee_id"]
        }
    }
    
    def validate_document(self, document: dict) -> dict:
        """Validate barcode against OCR data"""
        
        doc_type = document.get("type")
        ocr_data = document.get("ocr_extracted")
        image = document.get("image")
        
        result = {
            "barcode_found": False,
            "barcode_decoded": False,
            "mismatches": [],
            "risk_score": 0.0
        }
        
        # Detect barcodes in document
        barcodes = self.detect_barcodes(image)
        
        if not barcodes:
            result["barcode_found"] = False
            # Some documents should have barcodes
            if doc_type in ["w2", "tax_return"]:
                result["risk_score"] = 0.15  # Missing expected barcode
            return result
        
        result["barcode_found"] = True
        
        # Decode each barcode
        for barcode in barcodes:
            decoded = self.decode_barcode(barcode)
            if decoded:
                result["barcode_decoded"] = True
                
                # Compare to OCR data
                mismatches = self.compare_to_ocr(
                    decoded, 
                    ocr_data,
                    doc_type
                )
                
                result["mismatches"].extend(mismatches)
        
        # Calculate risk
        if result["mismatches"]:
            # Any mismatch is critical
            result["risk_score"] = 0.5
            for mismatch in result["mismatches"]:
                if mismatch["type"] == "amount":
                    result["risk_score"] = min(
                        result["risk_score"] + 0.2, 
                        1.0
                    )
        
        return result
    
    def detect_barcodes(self, image) -> list:
        """Detect all barcodes in document image"""
        
        barcodes = []
        
        # Use pyzbar or similar library
        # decoded_objects = decode(image)
        
        # Detect different formats
        formats = ["code128", "code39", "pdf417", "qr", "datamatrix"]
        
        for fmt in formats:
            detected = self.detect_format(image, fmt)
            barcodes.extend(detected)
        
        return barcodes
    
    def decode_barcode(self, barcode: dict) -> dict:
        """Decode barcode data into structured format"""
        
        raw_data = barcode.get("data")
        barcode_type = barcode.get("type")
        
        # Parse based on format
        if barcode_type == "pdf417":
            return self.parse_pdf417(raw_data)
        elif barcode_type == "qr":
            return self.parse_qr(raw_data)
        elif barcode_type in ["code128", "code39"]:
            return self.parse_linear(raw_data)
        
        return {"raw": raw_data}
    
    def compare_to_ocr(self, 
                       barcode_data: dict,
                       ocr_data: dict,
                       doc_type: str) -> list:
        """Compare decoded barcode to OCR extracted data"""
        
        mismatches = []
        
        field_mapping = self.DOCUMENT_BARCODE_FIELDS.get(doc_type, {})
        fields_to_check = field_mapping.get("fields", [])
        
        for field in fields_to_check:
            barcode_value = barcode_data.get(field)
            ocr_value = ocr_data.get(field)
            
            if barcode_value is None or ocr_value is None:
                continue
            
            # Normalize for comparison
            bc_normalized = self.normalize_value(barcode_value)
            ocr_normalized = self.normalize_value(ocr_value)
            
            if bc_normalized != ocr_normalized:
                mismatch_type = "amount" if self.is_amount(field) else "text"
                
                mismatches.append({
                    "field": field,
                    "barcode_value": barcode_value,
                    "ocr_value": ocr_value,
                    "type": mismatch_type,
                    "variance": self.calculate_variance(
                        barcode_value, 
                        ocr_value
                    ) if mismatch_type == "amount" else None
                })
        
        return mismatches
    
    def normalize_value(self, value) -> str:
        """Normalize value for comparison"""
        if isinstance(value, (int, float)):
            return str(round(float(value), 2))
        return str(value).strip().lower()
    
    def is_amount(self, field: str) -> bool:
        """Check if field represents a monetary amount"""
        amount_fields = [
            "wages", "tax", "balance", "pay", "amount",
            "agi", "gross", "net", "withholding"
        ]
        return any(af in field.lower() for af in amount_fields)
```

### Risk Scoring for Barcode Mismatches

| Scenario | Risk Score | Action |
|----------|------------|--------|
| Barcode matches OCR | 0.0 | High confidence |
| Missing expected barcode | 0.15 | Note, proceed |
| Amount mismatch | 0.5+ | Fraud investigation |
| Multiple mismatches | 0.8 | Reject document |
| Barcode checksum invalid | 0.4 | Document corrupted/altered |

---

## References

- [ISO/IEC 15438](https://www.iso.org/standard/65502.html) - PDF417 barcode specification
- [IRS Form Standards](https://www.irs.gov/forms-pubs/about-form-w-2)
- [ABA Check Standards](https://www.aba.com/)
