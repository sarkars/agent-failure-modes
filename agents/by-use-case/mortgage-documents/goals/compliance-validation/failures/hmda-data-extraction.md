# HMDA Data Extraction Errors

## Issue: OCR System Incorrectly Extracts Data Required for HMDA Reporting

**Frequency**: Common

**Symptoms**
- Census tract geocoding errors
- Loan purpose misclassification
- Ethnicity/race data extraction failures
- Action taken codes incorrect
- Rate spread calculation errors
- Property type misidentification

**Root Cause**
Home Mortgage Disclosure Act (HMDA) requires lenders to report detailed loan data including demographics, loan terms, and geographic information. OCR extracts data from applications but may misinterpret fields, fail to standardize responses, or miss required data points. HMDA errors result in regulatory penalties and fair lending exposure.

**Example**
```
Scenario 1: Census tract error

Property address: "123 Main St, Springfield, IL 62701"

OCR geocoded: Census tract 17167010100
Actual tract: Census tract 17167010200

← Single digit error
← Wrong tract demographics
← HMDA data integrity issue

---

Scenario 2: Ethnicity extraction

Application shows:
Borrower marked: "Hispanic or Latino"
And marked: "White"

OCR extracted: "White" only

← Ethnicity collected separately from race
← Both must be reported
← Missed Hispanic ethnicity

---

Scenario 3: Loan purpose

Refinance transaction:
- Existing loan: $250,000
- New loan: $300,000
- Cash out: $50,000

OCR: Coded as "Refinancing"
Correct: "Cash-out refinancing"

← Different HMDA purpose codes
← Cash-out vs. rate/term refinance
← Affects HMDA analysis

---

Scenario 4: Action taken timing

Application timeline:
- Received: January 15
- Withdrawn: January 20
- Denied: January 22 (after withdrawal)

OCR: Coded as "Denied"
Correct: "Withdrawn" (occurred first)

← Application was withdrawn before denial
← Action taken code wrong
← Affects denial rate reporting

---

Scenario 5: Rate spread

Loan details:
- Rate: 6.25%
- APOR on lock date: 5.15%
- Spread: 1.10%

Threshold: 1.5% (first lien)

OCR: Rate spread reported as 1.35%
Correct: 1.10%

← Calculation error
← Misreporting above/below threshold

---

HMDA extraction failures:
  
  Records with HMDA errors: 12%
  
  Issue types:
    Census tract/geocoding: 25%
    Ethnicity/race: 20%
    Loan purpose: 18%
    Action taken: 15%
    Rate spread: 12%
    Property type: 10%
  
  Impact:
    HMDA resubmission: 8%
    Regulatory findings: 5%
    Fair lending exposure: Variable
```

**Key Statistics**
From HMDA Compliance Research (2026):
- HMDA data errors: 10-15%
- Geocoding errors: 5-8%
- Demographic data errors: 8-12%
- Resubmission rate: 5-10%

**Key HMDA Fields**
| Category | Fields |
|----------|--------|
| Application | Date, loan type, purpose, preapproval |
| Borrower | Ethnicity, race, sex, income |
| Property | Type, census tract, address |
| Loan | Amount, rate spread, term, points |
| Action | Action taken, date, reason codes |

**Contributing Factors**
- Geocoding complexity
- Ethnicity vs. race distinction
- Multiple action taken scenarios
- Rate spread calculations
- Loan purpose nuances

---

## Mitigation Strategies

### Prevention
1. **Geocoding validation**: Use FFIEC geocoder
2. **Ethnicity/race separation**: Distinct field extraction
3. **Action sequencing**: First reportable action
4. **Rate spread calculation**: Use official APOR
5. **Purpose classification**: Detailed rules

### Implementation
```python
class HMDAExtractor:
    """Extract and validate HMDA reportable data"""
    
    LOAN_PURPOSE_CODES = {
        "purchase": 1,
        "refinance": 31,
        "cash_out_refinance": 32,
        "home_improvement": 2,
        "other": 4
    }
    
    ACTION_TAKEN_PRIORITY = [
        "application_withdrawn",
        "file_closed_incomplete",
        "loan_originated",
        "loan_denied"
    ]
    
    def extract_demographics(self, application: dict) -> dict:
        """Extract ethnicity and race (separately)"""
        ethnicity = application.get("ethnicity", [])
        race = application.get("race", [])
        
        # Ethnicity must be extracted separately
        if isinstance(ethnicity, str):
            ethnicity = [ethnicity]
        
        if isinstance(race, str):
            race = [race]
        
        return {
            "ethnicity": {
                "values": ethnicity,
                "hispanic_latino": "hispanic_or_latino" in [e.lower().replace(" ", "_") for e in ethnicity]
            },
            "race": {
                "values": race,
                "multi_racial": len(race) > 1
            },
            "collection_method": application.get("demographic_collection_method", "face_to_face")
        }
    
    def determine_loan_purpose(self, loan: dict) -> dict:
        """Determine HMDA loan purpose code"""
        if loan.get("transaction_type") == "purchase":
            return {"code": 1, "description": "Home purchase"}
        
        if loan.get("transaction_type") == "refinance":
            # Distinguish cash-out from rate/term
            existing_balance = loan.get("existing_loan_balance", 0)
            new_amount = loan.get("loan_amount", 0)
            
            if new_amount > existing_balance * 1.05:  # 5% buffer for costs
                return {"code": 32, "description": "Cash-out refinancing"}
            else:
                return {"code": 31, "description": "Refinancing"}
        
        return {"code": 4, "description": "Other purpose"}
    
    def determine_action_taken(self, application: dict) -> dict:
        """Determine correct action taken code"""
        events = application.get("action_events", [])
        
        # Sort by date
        sorted_events = sorted(events, key=lambda x: x["date"])
        
        # Find first reportable action
        for event in sorted_events:
            if event["action"] in self.ACTION_TAKEN_PRIORITY:
                return {
                    "action_taken": event["action"],
                    "date": event["date"],
                    "code": self.get_action_code(event["action"])
                }
        
        return {"error": "No reportable action found"}
    
    def calculate_rate_spread(self, 
                             loan_rate: float,
                             lock_date: str,
                             lien_type: str) -> dict:
        """Calculate rate spread for HMDA"""
        # Get APOR for lock date
        apor = self.get_apor(lock_date, loan["term"], loan["amortization_type"])
        
        spread = loan_rate - apor
        
        # Threshold varies by lien type
        threshold = 1.5 if lien_type == "first" else 3.5
        
        return {
            "loan_rate": loan_rate,
            "apor": apor,
            "rate_spread": round(spread, 2),
            "above_threshold": spread >= threshold,
            "reportable": spread >= threshold
        }
    
    def geocode_property(self, address: dict) -> dict:
        """Geocode property to census tract"""
        # Use FFIEC geocoder API
        result = self.ffiec_geocode(
            street=address["street"],
            city=address["city"],
            state=address["state"],
            zip=address["zip"]
        )
        
        return {
            "census_tract": result["tract"],
            "state_code": result["state_fips"],
            "county_code": result["county_fips"],
            "msa": result.get("msa"),
            "geocode_source": "FFIEC"
        }
    
    def validate_hmda_record(self, record: dict) -> dict:
        """Validate HMDA record completeness and accuracy"""
        issues = []
        
        required_fields = [
            "census_tract", "loan_amount", "action_taken",
            "ethnicity", "race", "sex", "income"
        ]
        
        for field in required_fields:
            if not record.get(field):
                issues.append({
                    "field": field,
                    "issue": "missing_required_field"
                })
        
        # Validate census tract format
        if record.get("census_tract"):
            if not self.valid_tract_format(record["census_tract"]):
                issues.append({
                    "field": "census_tract",
                    "value": record["census_tract"],
                    "issue": "invalid_format"
                })
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
```

---

## References

- [CFPB HMDA](https://www.consumerfinance.gov/data-research/hmda/) - HMDA data and reporting
- [FFIEC HMDA](https://www.ffiec.gov/hmda/) - Reporting requirements
- [HMDA Filing Instructions](https://www.consumerfinance.gov/data-research/hmda/for-filers/) - Technical specifications
- [FFIEC Geocoder](https://geomap.ffiec.gov/FFIECGeocMap/GeocodeMap1.aspx) - Census tract lookup
