# Address History Gaps

## Issue: AI System Fails to Trace Address Consistency Across Document Timeline

**Frequency**: Occasional

**Symptoms**
- Application address doesn't match current documents
- 2-year address history incomplete
- Address transitions not documented
- Mail forwarding patterns not detected
- Subject property address variations
- Prior addresses on credit report not explained

**Root Cause**
Mortgage applications require 2-year address history. Documents from different time periods should show consistent addresses for those periods. AI systems must correlate addresses across application, credit report, pay stubs, bank statements, and tax returns, flagging unexplained gaps or inconsistencies.

**Example**
```
Scenario 1: Current address mismatch

Application (submitted March 2025):
- Current address: 123 Oak Street, Chicago, IL
- Since: January 2023

Recent documents:
- Pay stub (Feb 2025): 456 Elm Ave, Chicago, IL ← DIFFERENT
- Bank statement (Feb 2025): 789 Pine Rd, Chicago, IL ← DIFFERENT
- W-2 (2024): 456 Elm Ave, Chicago, IL

Analysis:
- Three different addresses in recent documents
- Application says Oak Street since 2023
- Pay stub and W-2 show Elm Ave
- Bank statement shows Pine Rd

← Address history unclear
← Which is actually current?
← May indicate recent undisclosed move

---

Scenario 2: 2-year history gap

Application address history:
- Jan 2023 - Present: 123 Oak Street, Chicago
- Jul 2020 - Dec 2022: 456 Elm Ave, Chicago

Credit report addresses:
- 123 Oak Street, Chicago
- 456 Elm Ave, Chicago
- 100 Main St, Springfield (2022) ← NOT ON APPLICATION

Gap analysis:
- Application shows direct move Elm → Oak
- Credit report shows intermediate address
- Springfield address not disclosed
- Gap: Jan 2022 - Jun 2022?

← Undisclosed address
← 6-month gap in history

---

Scenario 3: Subject property address variations

Property being purchased: 555 Maple Lane, Unit 4B

Documents show:
- Purchase contract: 555 Maple Lane #4B
- Appraisal: 555 Maple Lane, Apt 4B
- Title: 555 Maple Ln, Unit 4-B
- Insurance: 555 Maple Lane 4B

AI processing:
- Flagged 4 different addresses
- Actually same property
- Unit number formatting varies

← False positive from formatting
← Should normalize address

---

Scenario 4: Mail forwarding pattern (fraud indicator)

Submitted documents:
- Application address: 123 Oak St, Chicago
- All documents mailed to: PO Box 999, Chicago

Investigation:
- Pay stubs show: PO Box 999
- Bank statements show: PO Box 999
- No documents at Oak Street

Red flags:
- Never received mail at "current" address?
- PO Box could be mail drop
- May not actually reside at Oak St

← Mail forwarding pattern
← May indicate address fraud

---

Address validation requirements:

  Period         | Documents to Check
  ---------------|---------------------
  Current        | Pay stubs, bank statements, utility bill
  Past 2 years   | Prior W-2s, tax returns, credit report
  Subject prop   | Contract, appraisal, title, insurance
  
  Common variations (normalize):
  - Street/St/St./Str
  - Avenue/Ave/Av
  - Apartment/Apt/Unit/#
  - Suite/Ste/Ste.
  - Direction (N/North, S/South)
  
  Red flags:
  - Current address with no recent mail
  - Undisclosed addresses on credit
  - Frequent moves (>3 in 2 years)
  - PO Box as primary address
```

**Key Statistics**
From Address Verification (2025-2026):
- Applications with address gaps: 8-12%
- Undisclosed prior addresses: 5-7%
- Address formatting variations: 30-40%
- Mail forwarding patterns: 2-3%
- Address fraud indicators: 1-2%

**Contributing Factors**
- Address normalization not applied
- Credit report addresses not compared
- Timeline not constructed
- Formatting variations cause false positives
- Mail pattern analysis missing
- Subject property variations flagged incorrectly

---

## Mitigation Strategies

### Prevention
1. **Address normalization**: Standardize all addresses
2. **Timeline construction**: Build address history
3. **Credit report correlation**: Compare all addresses
4. **Gap detection**: Flag unexplained periods
5. **Pattern analysis**: Detect mail forwarding
6. **Subject property matching**: Normalize property address

### Implementation
```python
from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Tuple
import usaddress

@dataclass
class AddressRecord:
    address: str
    normalized: str
    city: str
    state: str
    zip_code: str
    start_date: Optional[date]
    end_date: Optional[date]
    source: str
    is_mailing: bool = False
    is_residence: bool = True

class AddressHistoryValidator:
    """Validate address history across documents"""
    
    STREET_ABBREVIATIONS = {
        "street": "st", "avenue": "ave", "road": "rd",
        "drive": "dr", "lane": "ln", "boulevard": "blvd",
        "court": "ct", "place": "pl", "circle": "cir"
    }
    
    UNIT_ABBREVIATIONS = {
        "apartment": "apt", "unit": "unit", "suite": "ste",
        "#": "apt", "number": "apt"
    }
    
    def validate_address_history(self,
                                  application: dict,
                                  documents: list,
                                  credit_report: dict) -> dict:
        """Validate complete address history"""
        
        result = {
            "address_timeline": [],
            "gaps": [],
            "undisclosed_addresses": [],
            "formatting_issues": [],
            "risk_indicators": [],
            "risk_score": 0.0
        }
        
        # Build timeline from application
        app_addresses = self.extract_application_addresses(application)
        
        # Extract addresses from all documents
        doc_addresses = []
        for doc in documents:
            addrs = self.extract_document_addresses(doc)
            doc_addresses.extend(addrs)
        
        # Extract credit report addresses
        cr_addresses = self.extract_credit_addresses(credit_report)
        
        # Normalize all addresses
        all_addresses = app_addresses + doc_addresses + cr_addresses
        for addr in all_addresses:
            addr.normalized = self.normalize_address(addr.address)
        
        # Build unified timeline
        timeline = self.build_timeline(app_addresses)
        result["address_timeline"] = timeline
        
        # Find gaps
        gaps = self.find_gaps(timeline, years=2)
        result["gaps"] = gaps
        if gaps:
            result["risk_indicators"].append("address_history_gaps")
            result["risk_score"] += 0.15 * len(gaps)
        
        # Find undisclosed addresses
        undisclosed = self.find_undisclosed(
            app_addresses, 
            cr_addresses
        )
        result["undisclosed_addresses"] = undisclosed
        if undisclosed:
            result["risk_indicators"].append("undisclosed_addresses")
            result["risk_score"] += 0.2 * len(undisclosed)
        
        # Check current address consistency
        current_issues = self.verify_current_address(
            app_addresses,
            doc_addresses
        )
        if current_issues:
            result["risk_indicators"].append("current_address_inconsistent")
            result["risk_score"] += 0.25
        
        # Check for mail forwarding pattern
        if self.detect_mail_forwarding(doc_addresses):
            result["risk_indicators"].append("mail_forwarding_pattern")
            result["risk_score"] += 0.3
        
        result["risk_score"] = min(result["risk_score"], 1.0)
        
        return result
    
    def normalize_address(self, address: str) -> str:
        """Normalize address for comparison"""
        
        if not address:
            return ""
        
        # Lowercase
        addr = address.lower().strip()
        
        # Remove punctuation
        addr = addr.replace(".", "").replace(",", "").replace("#", " apt ")
        
        # Standardize street types
        for full, abbrev in self.STREET_ABBREVIATIONS.items():
            addr = addr.replace(f" {full} ", f" {abbrev} ")
            addr = addr.replace(f" {full}", f" {abbrev}")
        
        # Standardize unit types
        for full, abbrev in self.UNIT_ABBREVIATIONS.items():
            addr = addr.replace(f" {full} ", f" {abbrev} ")
        
        # Normalize whitespace
        addr = " ".join(addr.split())
        
        return addr
    
    def addresses_match(self, addr1: str, addr2: str) -> bool:
        """Check if two addresses match after normalization"""
        
        norm1 = self.normalize_address(addr1)
        norm2 = self.normalize_address(addr2)
        
        return norm1 == norm2
    
    def build_timeline(self, 
                       addresses: List[AddressRecord]) -> List[dict]:
        """Build chronological address timeline"""
        
        # Filter to residence addresses with dates
        dated = [a for a in addresses if a.start_date and a.is_residence]
        
        # Sort by start date
        dated.sort(key=lambda a: a.start_date)
        
        timeline = []
        for addr in dated:
            timeline.append({
                "address": addr.normalized,
                "start": str(addr.start_date),
                "end": str(addr.end_date) if addr.end_date else "present",
                "source": addr.source
            })
        
        return timeline
    
    def find_gaps(self, 
                  timeline: list,
                  years: int = 2) -> List[dict]:
        """Find gaps in address timeline"""
        
        gaps = []
        cutoff = date.today().replace(year=date.today().year - years)
        
        for i in range(len(timeline) - 1):
            current_end = timeline[i].get("end")
            next_start = timeline[i + 1].get("start")
            
            if current_end == "present":
                continue
            
            end_date = date.fromisoformat(current_end)
            start_date = date.fromisoformat(next_start)
            
            gap_days = (start_date - end_date).days
            
            if gap_days > 30:  # More than 30 days
                if end_date >= cutoff:  # Within required history
                    gaps.append({
                        "from_address": timeline[i]["address"],
                        "to_address": timeline[i + 1]["address"],
                        "gap_start": str(end_date),
                        "gap_end": str(start_date),
                        "days": gap_days
                    })
        
        return gaps
    
    def find_undisclosed(self,
                         application_addrs: List[AddressRecord],
                         credit_addrs: List[AddressRecord]) -> List[dict]:
        """Find credit report addresses not on application"""
        
        undisclosed = []
        
        app_normalized = {
            self.normalize_address(a.address) 
            for a in application_addrs
        }
        
        for cr_addr in credit_addrs:
            cr_normalized = self.normalize_address(cr_addr.address)
            
            # Check if on application
            matched = any(
                self.fuzzy_match(cr_normalized, app_norm)
                for app_norm in app_normalized
            )
            
            if not matched:
                undisclosed.append({
                    "address": cr_addr.address,
                    "source": "credit_report",
                    "reported_date": str(cr_addr.start_date) if cr_addr.start_date else "unknown"
                })
        
        return undisclosed
    
    def verify_current_address(self,
                               application_addrs: List[AddressRecord],
                               doc_addrs: List[AddressRecord]) -> List[dict]:
        """Verify current address matches recent documents"""
        
        issues = []
        
        # Get current address from application
        current = next(
            (a for a in application_addrs 
             if a.end_date is None and a.is_residence),
            None
        )
        
        if not current:
            return issues
        
        current_norm = self.normalize_address(current.address)
        
        # Check recent documents
        recent_cutoff = date.today().replace(
            month=date.today().month - 3 if date.today().month > 3 else 12
        )
        
        for doc_addr in doc_addrs:
            if doc_addr.start_date and doc_addr.start_date >= recent_cutoff:
                doc_norm = self.normalize_address(doc_addr.address)
                
                if not self.fuzzy_match(current_norm, doc_norm):
                    if doc_addr.is_residence:  # Skip mailing addresses
                        issues.append({
                            "expected": current.address,
                            "found": doc_addr.address,
                            "source": doc_addr.source
                        })
        
        return issues
    
    def detect_mail_forwarding(self, 
                               doc_addrs: List[AddressRecord]) -> bool:
        """Detect mail forwarding pattern (fraud indicator)"""
        
        mailing_addrs = [a for a in doc_addrs if a.is_mailing]
        residence_addrs = [a for a in doc_addrs if a.is_residence]
        
        if not mailing_addrs or not residence_addrs:
            return False
        
        # Check if all mail goes to different address
        mail_normalized = {self.normalize_address(a.address) for a in mailing_addrs}
        res_normalized = {self.normalize_address(a.address) for a in residence_addrs}
        
        # If mailing addresses are all different from residence
        if mail_normalized.isdisjoint(res_normalized):
            # Check if mailing is PO Box
            for mail in mailing_addrs:
                if "po box" in mail.address.lower():
                    return True
        
        return False
    
    def fuzzy_match(self, addr1: str, addr2: str) -> bool:
        """Fuzzy match addresses allowing minor variations"""
        
        if addr1 == addr2:
            return True
        
        # Check if one contains the other (for unit variations)
        if addr1 in addr2 or addr2 in addr1:
            return True
        
        # Split and compare components
        parts1 = set(addr1.split())
        parts2 = set(addr2.split())
        
        # If 80%+ overlap, consider match
        intersection = parts1.intersection(parts2)
        union = parts1.union(parts2)
        
        if len(intersection) / len(union) >= 0.8:
            return True
        
        return False
    
    def extract_application_addresses(self, 
                                      application: dict) -> List[AddressRecord]:
        """Extract addresses from loan application"""
        
        addresses = []
        
        for addr in application.get("address_history", []):
            addresses.append(AddressRecord(
                address=addr["address"],
                normalized="",
                city=addr.get("city", ""),
                state=addr.get("state", ""),
                zip_code=addr.get("zip", ""),
                start_date=addr.get("from_date"),
                end_date=addr.get("to_date"),
                source="application",
                is_residence=True
            ))
        
        return addresses
    
    def extract_document_addresses(self, 
                                   document: dict) -> List[AddressRecord]:
        """Extract addresses from various documents"""
        
        addresses = []
        doc_type = document.get("type")
        doc_date = document.get("date")
        
        if doc_type in ["pay_stub", "w2", "bank_statement"]:
            if addr := document.get("employee_address"):
                addresses.append(AddressRecord(
                    address=addr,
                    normalized="",
                    city="", state="", zip_code="",
                    start_date=doc_date,
                    end_date=None,
                    source=doc_type,
                    is_residence=True
                ))
        
        return addresses
    
    def extract_credit_addresses(self, 
                                 credit_report: dict) -> List[AddressRecord]:
        """Extract addresses from credit report"""
        
        addresses = []
        
        for addr in credit_report.get("addresses", []):
            addresses.append(AddressRecord(
                address=addr.get("address", ""),
                normalized="",
                city=addr.get("city", ""),
                state=addr.get("state", ""),
                zip_code=addr.get("zip", ""),
                start_date=addr.get("reported_date"),
                end_date=None,
                source="credit_report",
                is_residence=True
            ))
        
        return addresses
```

### Risk Scoring for Address Issues

| Issue | Risk Score | Action |
|-------|------------|--------|
| Gap in 2-year history | 0.15 | Request explanation |
| Undisclosed credit address | 0.2 | Verify residence |
| Current address mismatch | 0.25 | Recent docs differ |
| Mail forwarding pattern | 0.3 | Fraud investigation |
| Multiple recent moves | 0.15 | Stability concern |
| PO Box as residence | 0.35 | Verify actual address |

---

## References

- [USPS Address Standards](https://pe.usps.com/cpim/ftp/pubs/Pub28/pub28.pdf)
- [Fannie Mae Occupancy Requirements](https://selling-guide.fanniemae.com/)
- [FCRA Address Reporting](https://www.ftc.gov/legal-library/browse/statutes/fair-credit-reporting-act)
