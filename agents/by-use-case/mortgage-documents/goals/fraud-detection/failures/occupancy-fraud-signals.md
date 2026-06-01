# Occupancy Fraud Signal Detection Failures

## Issue: AI System Fails to Detect False Owner-Occupancy Claims

**Frequency**: Common

**Symptoms**
- Borrower claims primary residence but indicators suggest investment
- Address history shows pattern of property flipping
- Existing primary residence not being sold
- Property location inconsistent with employment
- Borrower already owns multiple properties
- Rental listings appearing shortly after closing
- Insurance type doesn't match occupancy claim

**Root Cause**
Owner-occupied loans receive better rates and terms than investment properties. Fraudsters claim primary residence intent when planning to rent or flip. AI systems verify occupancy claims on paper but miss behavioral and contextual signals that indicate investment intent. Post-closing, properties are often listed for rent within months.

**Example**
```
Scenario 1: Existing primary not being sold

Application claims:
- Property: Primary residence
- Current residence: "Will be sold"

AI verification:
- Occupancy field: "Primary" ✓
- Property type: Single family ✓
- Intent to occupy letter: Signed ✓

Reality check (not performed):
- Current primary residence: No listing found
- Current mortgage: No payoff planned
- Two primary residences not possible

← Will rent new property as investment
← Current home kept as actual residence
← AI didn't verify sale plan

---

Scenario 2: Geographic impossibility

Application data:
- Employer: Downtown Chicago
- Work type: Full-time, on-site
- Subject property: Miami, FL (1,300 miles)
- Occupancy: Primary residence

AI verification:
- Employment: Verified ✓
- Property: Appraised ✓
- Occupancy claim: Documented ✓

Occupancy signals missed:
- 1,300-mile commute impossible
- No job transfer documentation
- No remote work arrangement
- No logical occupancy path

← Investment property at primary rates
← Geographic analysis not performed

---

Scenario 3: Property flipping pattern

Borrower history:
- Property 1 (2023): Purchased as "primary," sold 8 months later
- Property 2 (2024): Purchased as "primary," sold 6 months later
- Property 3 (2025): Current application, "primary residence"

AI verification:
- Current application: Verified ✓
- Credit report: Reviewed ✓
- Property: Appraised ✓

Pattern missed:
- Serial "primary residence" claims
- Short hold periods indicate flipping
- No actual occupancy

← Third fraudulent occupancy claim
← Pattern visible in credit history
← No historical occupancy analysis

---

Scenario 4: Post-closing rental listing

Application:
- Occupancy: Primary residence
- Closed: March 2026

Post-closing discovery (AI not monitoring):
- Zillow rental listing: April 2026
- Listed rent: $2,400/month
- Property photos match closing docs

← Never intended to occupy
← AI only verified at application
← No post-closing monitoring

---

Occupancy fraud indicators:

  Pre-closing signals:
    Multiple owned properties: 30%
    Geographic mismatch: 25%
    Existing primary not sold: 20%
    Property type mismatch: 15%
    Income/property ratio: 10%
  
  Post-closing signals:
    Rental listing within 12 months: 40%
    Insurance change: 30%
    Address change: 20%
    Utility transfer: 10%
  
  Detection rates:
    Application-only review: 15-25%
    With behavioral analysis: 40-55%
    With post-closing monitoring: 70-85%
```

**Key Statistics**
From Occupancy Fraud Research (2025-2026):
- Occupancy misrepresentation: 10-15% of loans
- Rate difference (primary vs. investment): 0.5-0.75%
- Average fraud savings to borrower: $50-$150/month
- Investor losses when discovered: Varies (rep & warrant claims)

**Contributing Factors**
- Self-certification of occupancy
- No post-closing verification
- Geographic analysis not standard
- Historical pattern review limited
- Rental listings not monitored
- Rate incentive for fraud

---

## Mitigation Strategies

### Prevention
1. **Geographic plausibility**: Check property/employment distance
2. **Historical pattern review**: Analyze prior occupancy claims
3. **Existing property analysis**: Verify sale/disposition plans
4. **Post-closing monitoring**: Check rental listings, address changes
5. **Insurance verification**: Confirm owner-occupied coverage
6. **Utility monitoring**: Verify borrower-named utilities

### Implementation
```python
class OccupancyFraudDetector:
    """Detect occupancy fraud indicators"""
    
    MAX_COMMUTE_MILES = 75
    MIN_HOLD_PERIOD_MONTHS = 12
    
    def analyze_occupancy(self, application: dict) -> dict:
        """Analyze application for occupancy fraud indicators"""
        
        indicators = []
        risk_score = 0
        
        # Geographic plausibility
        geo_result = self.check_geographic_plausibility(application)
        if geo_result["implausible"]:
            indicators.append(geo_result)
            risk_score += 0.35
        
        # Existing property disposition
        existing_result = self.check_existing_properties(application)
        if existing_result["suspicious"]:
            indicators.append(existing_result)
            risk_score += 0.30
        
        # Historical pattern
        history_result = self.check_occupancy_history(application)
        if history_result["pattern_detected"]:
            indicators.append(history_result)
            risk_score += 0.40
        
        # Property/income fit
        fit_result = self.check_property_income_fit(application)
        if fit_result["mismatch"]:
            indicators.append(fit_result)
            risk_score += 0.20
        
        return {
            "occupancy_fraud_risk": min(risk_score, 1.0),
            "claimed_occupancy": application.get("occupancy_type"),
            "indicators": indicators,
            "recommendation": self.get_recommendation(risk_score)
        }
    
    def check_geographic_plausibility(self, application: dict) -> dict:
        """Check if occupancy is geographically plausible"""
        
        if application.get("occupancy_type") != "primary_residence":
            return {"implausible": False}
        
        property_loc = application.get("property_address")
        employer_loc = application.get("employer_address")
        work_type = application.get("work_type", "on_site")
        
        if not property_loc or not employer_loc:
            return {"implausible": False, "note": "Missing location data"}
        
        distance = self.calculate_distance(property_loc, employer_loc)
        
        if distance > self.MAX_COMMUTE_MILES and work_type == "on_site":
            return {
                "indicator": "geographic_implausibility",
                "implausible": True,
                "distance_miles": distance,
                "work_type": work_type,
                "issue": f"Property {distance} miles from on-site job",
                "risk": "high"
            }
        
        return {"implausible": False}
    
    def check_existing_properties(self, application: dict) -> dict:
        """Check disposition plan for existing primary residence"""
        
        # Get borrower's existing properties
        credit_report = application.get("credit_report", {})
        existing_mortgages = credit_report.get("mortgages", [])
        
        current_primary = None
        for mortgage in existing_mortgages:
            if mortgage.get("property_type") == "primary_residence":
                current_primary = mortgage
                break
        
        if not current_primary:
            return {"suspicious": False}
        
        # Check if there's a disposition plan
        disposition = application.get("existing_property_disposition")
        
        if not disposition or disposition == "retain":
            return {
                "indicator": "existing_primary_retention",
                "suspicious": True,
                "current_property": current_primary.get("address"),
                "issue": "Retaining existing primary while claiming new primary",
                "risk": "high"
            }
        
        if disposition == "sell":
            # Verify listing exists
            listing = self.check_for_listing(current_primary.get("address"))
            if not listing:
                return {
                    "indicator": "no_sale_listing",
                    "suspicious": True,
                    "issue": "Claims to sell but no listing found",
                    "risk": "medium"
                }
        
        return {"suspicious": False}
    
    def check_occupancy_history(self, application: dict) -> dict:
        """Check for pattern of short-term primary residence claims"""
        
        credit_report = application.get("credit_report", {})
        mortgage_history = credit_report.get("mortgage_history", [])
        
        short_holds = []
        
        for mortgage in mortgage_history:
            if mortgage.get("original_occupancy") == "primary_residence":
                hold_months = mortgage.get("months_held", 0)
                
                if hold_months < self.MIN_HOLD_PERIOD_MONTHS:
                    short_holds.append({
                        "property": mortgage.get("address"),
                        "months_held": hold_months,
                        "disposition": mortgage.get("disposition")
                    })
        
        if len(short_holds) >= 2:
            return {
                "indicator": "occupancy_pattern",
                "pattern_detected": True,
                "short_hold_count": len(short_holds),
                "properties": short_holds,
                "issue": "Pattern of short-term primary residence claims",
                "risk": "high"
            }
        
        return {"pattern_detected": False}
    
    def schedule_post_closing_monitoring(self, loan: dict) -> dict:
        """Schedule post-closing occupancy monitoring"""
        
        monitoring_schedule = {
            "loan_id": loan["id"],
            "property_address": loan["property_address"],
            "checks": [
                {
                    "type": "rental_listing_scan",
                    "frequency": "monthly",
                    "duration_months": 12,
                    "sources": ["zillow", "apartments.com", "craigslist"]
                },
                {
                    "type": "address_change_monitor",
                    "frequency": "quarterly",
                    "duration_months": 24
                },
                {
                    "type": "insurance_verification",
                    "frequency": "annually",
                    "check": "owner_occupied_coverage"
                }
            ]
        }
        
        return monitoring_schedule
```

---

## References

- [Fannie Mae: Occupancy Requirements](https://selling-guide.fanniemae.com/Selling-Guide/Origination-thru-Closing/Subpart-B2-Eligibility/Chapter-B2-1-Mortgage-Eligibility/1032992061/B2-1-01-Occupancy-Types-10-07-2020.htm)
- [FBI: Mortgage Fraud Schemes](https://www.fbi.gov/investigate/white-collar-crime/mortgage-fraud)
- [FHFA: Occupancy Fraud](https://www.fhfa.gov/)
