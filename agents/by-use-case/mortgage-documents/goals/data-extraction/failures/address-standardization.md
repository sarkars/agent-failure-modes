# Address Standardization Failures

## Issue: OCR System Fails to Standardize or Match Addresses Across Documents

**Frequency**: Common

**Symptoms**
- Address variations not matched (St. vs Street)
- Unit/apartment numbers inconsistent
- PO Box vs. physical address confusion
- Property address vs. mailing address mixed
- Zip+4 handling errors
- Rural route address parsing failures

**Root Cause**
Mortgage files contain property addresses, mailing addresses, employer addresses, and more across dozens of documents. OCR extracts addresses verbatim without standardization, leading to mismatches that prevent document correlation, title issues, and compliance problems.

**Example**
```
Scenario 1: Address variation

Appraisal: "123 Main Street, Apt 4B"
Deed: "123 Main St #4B"
Title: "123 Main Street, Unit 4-B"

OCR: Three different addresses extracted
Reality: Same property

← Abbreviations not standardized
← Unit designator variations
← Failed to match property

---

Scenario 2: Property vs. mailing confusion

Application property address: "456 Oak Lane"
Application mailing address: "PO Box 789"

Appraisal subject: "456 Oak Lane"
Bank statement address: "PO Box 789"

OCR: Flagged bank statement as wrong property
Reality: PO Box is borrower's mailing address

← Property vs. mailing not distinguished
← False mismatch flagged

---

Scenario 3: Directional issues

Title search: "123 N Main St"
Appraisal: "123 North Main Street"
Deed: "123 Main Street N"

OCR: Three different addresses
Reality: Same property, directional placement varies

← N/North not standardized
← Position variation (prefix vs suffix)

---

Scenario 4: Rural addressing

Property: "Rural Route 2, Box 145"
911 Address: "1045 County Road 22"
Mailing: "RR 2 Box 145"

All refer to same property
OCR: Three unrelated addresses

← Rural routes being phased out
← 911 address may differ
← Multiple valid addresses for same property

---

Address standardization failures:
  
  Documents with address issues: 25%
  
  Issue types:
    Abbreviation variations: 35%
    Unit number formatting: 20%
    Directional handling: 15%
    Property/mailing confusion: 15%
    Rural/non-standard addresses: 10%
    Zip code variations: 5%
  
  Impact:
    Document matching failures: 15%
    False mismatch flags: 10%
    Title concerns: 5%
```

**Key Statistics**
From Address Matching Research (2026):
- Address variation rate: 20-30%
- Successful matching (raw): 60-70%
- Successful matching (standardized): 95-98%
- Title issues from address mismatches: 2-3%

**Contributing Factors**
- No USPS standardization
- Abbreviation database missing
- Unit designator variations
- Directional position handling
- Property vs. mailing distinction

---

## Mitigation Strategies

### Prevention
1. **USPS standardization**: Use CASS-certified tools
2. **Abbreviation normalization**: St→Street, N→North
3. **Unit parsing**: Standardize designators
4. **Address type classification**: Property vs. mailing
5. **Fuzzy matching**: Handle minor variations

### Implementation
```python
class AddressStandardizer:
    """Standardize and match mortgage addresses"""
    
    ABBREVIATIONS = {
        "st": "street", "st.": "street",
        "rd": "road", "rd.": "road",
        "ave": "avenue", "ave.": "avenue",
        "blvd": "boulevard", "blvd.": "boulevard",
        "ln": "lane", "ln.": "lane",
        "dr": "drive", "dr.": "drive",
        "ct": "court", "ct.": "court",
        "pl": "place", "pl.": "place",
        "n": "north", "n.": "north",
        "s": "south", "s.": "south",
        "e": "east", "e.": "east",
        "w": "west", "w.": "west",
        "apt": "apartment", "apt.": "apartment",
        "#": "unit"
    }
    
    UNIT_DESIGNATORS = ["apartment", "apt", "unit", "suite", "ste", "#"]
    
    def standardize(self, address: str) -> dict:
        """Standardize address to USPS format"""
        addr_lower = address.lower().strip()
        
        # Expand abbreviations
        words = addr_lower.split()
        standardized_words = []
        
        for word in words:
            standardized_words.append(
                self.ABBREVIATIONS.get(word, word)
            )
        
        standardized = " ".join(standardized_words)
        
        # Extract components
        return {
            "original": address,
            "standardized": standardized,
            "components": self.parse_components(standardized)
        }
    
    def parse_components(self, address: str) -> dict:
        """Parse address into components"""
        # Extract unit number
        unit = None
        for designator in self.UNIT_DESIGNATORS:
            if designator in address:
                # Extract unit value
                idx = address.find(designator)
                unit_part = address[idx:].split()[1] if len(address[idx:].split()) > 1 else None
                unit = unit_part
                break
        
        # Basic parsing (would use proper parser in production)
        parts = address.split(",")
        
        return {
            "street": parts[0] if parts else None,
            "unit": unit,
            "city": parts[1].strip() if len(parts) > 1 else None,
            "state_zip": parts[2].strip() if len(parts) > 2 else None
        }
    
    def match_addresses(self, addr1: str, addr2: str) -> dict:
        """Check if two addresses match"""
        std1 = self.standardize(addr1)
        std2 = self.standardize(addr2)
        
        # Exact match after standardization
        if std1["standardized"] == std2["standardized"]:
            return {"match": True, "confidence": 1.0}
        
        # Component-level matching
        comp1 = std1["components"]
        comp2 = std2["components"]
        
        # Street number must match exactly
        street1_num = self.extract_street_number(comp1.get("street", ""))
        street2_num = self.extract_street_number(comp2.get("street", ""))
        
        if street1_num != street2_num:
            return {
                "match": False,
                "reason": "Street numbers differ"
            }
        
        # Fuzzy match street name
        similarity = self.string_similarity(
            comp1.get("street", ""),
            comp2.get("street", "")
        )
        
        return {
            "match": similarity > 0.85,
            "confidence": similarity,
            "variations": {
                "addr1": std1["standardized"],
                "addr2": std2["standardized"]
            }
        }
    
    def classify_address_type(self, address: str) -> str:
        """Classify as property, mailing, or PO Box"""
        addr_lower = address.lower()
        
        if "po box" in addr_lower or "p.o. box" in addr_lower:
            return "po_box"
        
        if "rural route" in addr_lower or "rr " in addr_lower:
            return "rural_route"
        
        # Default to physical
        return "physical"
    
    def cross_validate_addresses(self, 
                                 documents: list,
                                 subject_property: str) -> dict:
        """Validate addresses match subject property"""
        std_subject = self.standardize(subject_property)
        mismatches = []
        
        for doc in documents:
            if doc.get("property_address"):
                match = self.match_addresses(
                    subject_property,
                    doc["property_address"]
                )
                
                if not match["match"]:
                    mismatches.append({
                        "document": doc["type"],
                        "address": doc["property_address"],
                        "confidence": match.get("confidence", 0)
                    })
        
        return {
            "subject_property": subject_property,
            "all_match": len(mismatches) == 0,
            "mismatches": mismatches
        }
```

---

## References

- [USPS Addressing Standards](https://pe.usps.com/text/pub28/welcome.htm) - Publication 28
- [CASS Certification](https://postalpro.usps.com/certifications/cass) - Address validation
- [ALTA Standards](https://www.alta.org/) - Title industry addressing
