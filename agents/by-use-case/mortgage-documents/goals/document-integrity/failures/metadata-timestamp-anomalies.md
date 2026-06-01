# Metadata Timestamp Anomalies

## Issue: AI System Fails to Detect Document Dates Inconsistent with File Metadata

**Frequency**: Occasional

**Symptoms**
- Document claims date before file creation
- Creation timestamp after modification timestamp
- Timezone inconsistencies suggest multiple origins
- File created in future relative to document date
- Metadata shows recent creation for "old" document
- Embedded timestamps contradict visible dates

**Root Cause**
Every digital document carries metadata timestamps indicating when it was created and modified. When someone creates a fake "2024 tax return" in 2025, the file metadata reveals the deception. AI systems that only extract visible dates miss this critical verification layer.

**Example**
```
Scenario 1: Tax return created after filing date

Document visible:
- Form 1040
- Tax Year: 2024
- E-Filed: April 15, 2025
- DCN: Present

PDF metadata:
- Created: June 3, 2025  ← AFTER FILING
- Modified: June 3, 2025
- Producer: Microsoft Word  ← NOT IRS

Analysis:
- Document claims filed April 15
- File created June 3 (49 days later)
- IRS doesn't use Word to generate returns

← Fabricated document
← Metadata proves forgery

---

Scenario 2: Bank statement backdating attempt

Document header:
- Statement Period: January 1-31, 2025
- Statement Date: February 1, 2025

PDF metadata:
- Created: March 15, 2025  ← 6 weeks after statement
- Modified: March 15, 2025
- Producer: Adobe Acrobat

Expected:
- Created: February 1-3, 2025
- Producer: Bank Statement System

← Statement generated well after period
← Likely modified version

---

Scenario 3: Timezone inconsistency

Employer VOE:
- Date: March 10, 2025
- Location: Chicago, IL

Metadata:
- Created: 2025-03-10T14:30:00+08:00  ← Hong Kong timezone
- Modified: 2025-03-10T09:00:00-06:00 ← Chicago timezone

Analysis:
- Document claims Chicago employer
- Created in +8 timezone (Asia)
- Modified in Chicago timezone

← Document created overseas
← Modified locally
← Offshore document fraud pattern

---

Scenario 4: Future timestamp (clock manipulation)

W-2 submitted: May 2025
W-2 visible year: 2024

Metadata:
- Created: January 15, 2026  ← FUTURE DATE
- Application date: May 10, 2025

Explanation:
- Fraudster's system clock wrong
- Set to future date during forgery
- Obvious manipulation indicator

← Impossible timestamp
← Clear fraud indicator

---

Timestamp analysis matrix:

  Check                    | Valid        | Suspicious
  -------------------------|--------------|------------
  Created ≤ Document date  | Yes          | Created after
  Created ≤ Submitted      | Yes          | Future creation
  Modified ≥ Created       | Yes          | Modified before created
  Timezone consistent      | One timezone | Multiple timezones
  Producer matches source  | Expected     | PDF editor
```

**Key Statistics**
From Document Forensics (2025-2026):
- Timestamp anomalies in fraud cases: 40-60%
- Documents with future timestamps: 2-3%
- Timezone inconsistencies: 5-8%
- Metadata checked by AI systems: 15-25%

**Contributing Factors**
- Metadata not extracted
- Timestamps not compared to document dates
- Timezone normalization not performed
- Producer string not validated
- No temporal logic validation
- File system timestamps ignored

---

## Mitigation Strategies

### Prevention
1. **Extract all timestamps**: PDF, file system, embedded
2. **Temporal validation**: Document date ≤ Creation date ≤ Submission
3. **Timezone analysis**: Flag inconsistencies
4. **Producer validation**: Match expected software
5. **Future date detection**: Impossible timestamps
6. **Clock drift tolerance**: Allow reasonable variance

### Implementation
```python
from datetime import datetime, timezone, timedelta
from typing import Optional
import pytz

class TimestampValidator:
    """Validate document timestamps for anomalies"""
    
    # Reasonable time for document generation after event
    GENERATION_WINDOWS = {
        "w2": timedelta(days=45),      # W-2s by Jan 31
        "tax_return": timedelta(days=0),  # Filed date = creation
        "bank_statement": timedelta(days=7),
        "pay_stub": timedelta(days=3),
        "voe": timedelta(days=14),
        "appraisal": timedelta(days=7)
    }
    
    EXPECTED_PRODUCERS = {
        "w2": ["ADP", "Paychex", "Gusto", "Paylocity", "QuickBooks"],
        "tax_return": ["IRS", "TurboTax", "H&R Block", "TaxAct"],
        "bank_statement": [],  # Institution-specific
        "pay_stub": ["ADP", "Paychex", "Gusto", "Paylocity"]
    }
    
    def validate_timestamps(self, 
                           document: dict,
                           submission_date: datetime) -> dict:
        """Validate document timestamps"""
        
        result = {
            "anomalies": [],
            "risk_indicators": [],
            "risk_score": 0.0
        }
        
        doc_type = document.get("type")
        visible_date = document.get("document_date")  # Parsed from content
        
        # PDF metadata
        created = document.get("metadata", {}).get("created")
        modified = document.get("metadata", {}).get("modified")
        producer = document.get("metadata", {}).get("producer", "")
        
        # Check 1: Future timestamp
        if created:
            if created > datetime.now(timezone.utc):
                result["anomalies"].append({
                    "type": "future_timestamp",
                    "severity": "critical",
                    "created": str(created),
                    "now": str(datetime.now(timezone.utc))
                })
                result["risk_indicators"].append("future_creation_date")
                result["risk_score"] += 0.5
        
        # Check 2: Created after submission
        if created and submission_date:
            if created > submission_date:
                result["anomalies"].append({
                    "type": "created_after_submission",
                    "severity": "critical",
                    "created": str(created),
                    "submitted": str(submission_date)
                })
                result["risk_indicators"].append("created_after_submitted")
                result["risk_score"] += 0.4
        
        # Check 3: Document date vs creation date
        if visible_date and created:
            # For tax returns, creation should be close to filing
            window = self.GENERATION_WINDOWS.get(doc_type, timedelta(days=30))
            expected_creation_end = visible_date + window
            
            if created > expected_creation_end:
                days_late = (created - expected_creation_end).days
                result["anomalies"].append({
                    "type": "created_after_document_date",
                    "severity": "high" if days_late > 30 else "medium",
                    "document_date": str(visible_date),
                    "created": str(created),
                    "days_late": days_late
                })
                result["risk_indicators"].append("late_creation")
                result["risk_score"] += 0.3 if days_late > 30 else 0.15
        
        # Check 4: Modified before created (impossible)
        if created and modified and modified < created:
            result["anomalies"].append({
                "type": "modified_before_created",
                "severity": "critical",
                "created": str(created),
                "modified": str(modified)
            })
            result["risk_indicators"].append("impossible_timestamps")
            result["risk_score"] += 0.4
        
        # Check 5: Timezone inconsistency
        if created and modified:
            tz_anomaly = self.check_timezone_consistency(created, modified)
            if tz_anomaly:
                result["anomalies"].append(tz_anomaly)
                result["risk_indicators"].append("timezone_inconsistency")
                result["risk_score"] += 0.25
        
        # Check 6: Producer validation
        expected = self.EXPECTED_PRODUCERS.get(doc_type, [])
        if expected and producer:
            if not any(exp.lower() in producer.lower() for exp in expected):
                if self.is_pdf_editor(producer):
                    result["anomalies"].append({
                        "type": "unexpected_producer",
                        "severity": "medium",
                        "producer": producer,
                        "expected": expected
                    })
                    result["risk_indicators"].append("pdf_editor_producer")
                    result["risk_score"] += 0.2
        
        result["risk_score"] = min(result["risk_score"], 1.0)
        
        return result
    
    def check_timezone_consistency(self,
                                   created: datetime,
                                   modified: datetime) -> Optional[dict]:
        """Check for timezone inconsistencies"""
        
        if created.tzinfo and modified.tzinfo:
            created_tz = str(created.tzinfo)
            modified_tz = str(modified.tzinfo)
            
            # Different timezones suggest different origins
            if created_tz != modified_tz:
                # Calculate offset difference
                created_offset = created.utcoffset().total_seconds() / 3600
                modified_offset = modified.utcoffset().total_seconds() / 3600
                
                offset_diff = abs(created_offset - modified_offset)
                
                if offset_diff > 3:  # More than 3 hours difference
                    return {
                        "type": "timezone_mismatch",
                        "severity": "medium",
                        "created_tz": created_tz,
                        "modified_tz": modified_tz,
                        "offset_difference_hours": offset_diff
                    }
        
        return None
    
    def is_pdf_editor(self, producer: str) -> bool:
        """Check if producer is a PDF editing tool"""
        
        editors = [
            "adobe acrobat",
            "pdf-xchange",
            "foxit",
            "nitro",
            "pdfelement",
            "sejda",
            "smallpdf"
        ]
        
        producer_lower = producer.lower()
        return any(editor in producer_lower for editor in editors)
    
    def extract_all_timestamps(self, document: dict) -> dict:
        """Extract all available timestamps from document"""
        
        timestamps = {
            "pdf_created": None,
            "pdf_modified": None,
            "file_created": None,
            "file_modified": None,
            "embedded_dates": [],
            "visible_date": None
        }
        
        # PDF metadata timestamps
        metadata = document.get("metadata", {})
        timestamps["pdf_created"] = metadata.get("created")
        timestamps["pdf_modified"] = metadata.get("modified")
        
        # File system timestamps
        timestamps["file_created"] = document.get("file_created")
        timestamps["file_modified"] = document.get("file_modified")
        
        # Embedded dates (XMP, custom metadata)
        timestamps["embedded_dates"] = metadata.get("xmp_dates", [])
        
        # Visible date from OCR
        timestamps["visible_date"] = document.get("document_date")
        
        return timestamps
```

### Risk Scoring for Timestamp Anomalies

| Anomaly | Risk Score | Action |
|---------|------------|--------|
| Future timestamp | 0.5 | Reject - impossible |
| Created after submission | 0.4 | Reject - fabricated |
| Created >30 days after doc date | 0.3 | Investigation |
| Modified before created | 0.4 | Reject - manipulated |
| Timezone inconsistency | 0.25 | Enhanced review |
| PDF editor as producer | 0.2 | Verify authenticity |

---

## References

- [PDF Metadata Standards](https://www.adobe.com/devnet/pdf/pdf_reference.html)
- [XMP Specification](https://www.adobe.com/devnet/xmp.html)
- [NIST Digital Forensics](https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt)
