# Employment Fabrication Detection Failures

## Issue: AI System Fails to Detect Fake Employers or Fabricated Employment

**Frequency**: Common

**Symptoms**
- Employer doesn't exist or is shell company
- VOE returns from fraudulent source
- Employer phone routes to fraud ring
- Business registration recent but claims long employment
- No online presence for claimed employer
- Employer address is residential or virtual office
- Industry/role mismatch with stated income

**Root Cause**
Employment verification traditionally relies on contacting the employer. Fraudsters create fake companies, establish phone numbers that route to accomplices, and generate authentic-looking VOE responses. AI systems that verify employment through traditional channels (phone, fax, document verification) can be defeated by sophisticated fraud operations.

**Example**
```
Scenario 1: Shell company employment

Application claims:
- Employer: "Global Tech Solutions LLC"
- Position: "Senior Consultant"
- Annual income: $145,000
- Employment: 3 years

AI verification:
- VOE sent: Returned completed ✓
- Phone verification: "Confirmed" ✓
- Paystubs: Match application ✓
- W-2: Provided ✓

Reality:
- LLC registered 6 months ago
- Address: UPS Store mailbox
- Phone: VoIP routing to fraud ring
- Website: Template site, no clients
- W-2: Fabricated

← All traditional verification passed
← Shell company created for fraud
← No business legitimacy check

---

Scenario 2: Employer impersonation

Application claims:
- Employer: "Microsoft Corporation"
- Position: "Software Engineer"
- Income: $180,000

Verification process:
- VOE faxed to: Number provided by applicant
- Response received: Employment confirmed
- Phone callback: "HR confirmed"

Fraud method:
- Applicant provided fake HR number
- Number routes to accomplice
- Fake VOE returned
- Never contacted real Microsoft

← Verification went to fraudulent number
← Real employer never contacted
← Independent lookup not performed

---

Scenario 3: Income inflation with real employer

Actual employment:
- Employer: Real company
- Position: Warehouse associate
- Actual income: $42,000

Fraudulent claim:
- Same employer
- Position: "Operations Manager"
- Claimed income: $95,000

Verification:
- Phone VOE to real HR: "Yes, employed"
- But: HR didn't confirm title/salary
- Paystubs: Altered documents

← Real employer, fake details
← HR confirmed employment only
← Title/salary not verified

---

Scenario 4: Employment verification service fraud

Fraud ring operation:
1. Create verification service company
2. List multiple "employers" in database
3. When lenders verify, service confirms
4. Multiple loans originated using fake employers

AI verification:
- Third-party service: Confirmed employment ✓
- Service appears legitimate
- Multiple verifications through same service

← Verification service itself is fraudulent
← AI trusted third-party confirmation
← No independent validation

---

Employment fraud indicators:

  Common fraud patterns:
    Shell company: 35%
    Phone number manipulation: 25%
    Document alteration: 20%
    Real employer inflation: 15%
    Verification service fraud: 5%
  
  Detection rates:
    Traditional VOE: 20-35%
    With business registry check: 50-65%
    With independent lookup: 70-85%
    With IRS verification: 90%+
```

**Key Statistics**
From Employment Fraud Research (2025-2026):
- Employment fraud in mortgage apps: 10-15%
- Shell company detection rate: 30-50%
- Income inflation cases: 20-30% of fraud
- VOE manipulation success rate: 60-80%

**Contributing Factors**
- VOE relies on applicant-provided info
- Phone numbers easily spoofed
- LLC registration fast and cheap
- No standard employer verification database
- HR confirms employment, not details
- Third-party services not validated

---

## Mitigation Strategies

### Prevention
1. **Independent employer lookup**: Don't use applicant-provided numbers
2. **Business registry check**: Verify incorporation date, status
3. **Online presence analysis**: Website, LinkedIn, reviews
4. **IRS verification**: 4506-C transcript confirms employer
5. **Payroll provider verification**: Direct to ADP, Paychex, etc.
6. **Industry/income validation**: Role vs. salary plausibility

### Implementation
```python
class EmploymentFraudDetector:
    """Detect fabricated employment"""
    
    INCOME_RANGES = {
        "warehouse_associate": (30000, 55000),
        "software_engineer": (80000, 200000),
        "senior_consultant": (90000, 180000),
        "administrative_assistant": (35000, 60000),
        "manager": (50000, 120000)
    }
    
    def verify_employment(self, application: dict) -> dict:
        """Comprehensive employment verification"""
        
        employer_name = application.get("employer_name")
        employer_ein = application.get("employer_ein")
        
        verification_results = []
        risk_score = 0
        
        # 1. Business registry check
        registry_result = self.check_business_registry(
            employer_name, 
            employer_ein,
            application.get("employer_state")
        )
        verification_results.append(registry_result)
        if registry_result["risk"]:
            risk_score += registry_result["risk_weight"]
        
        # 2. Independent contact lookup
        contact_result = self.lookup_independent_contact(employer_name)
        verification_results.append(contact_result)
        
        # 3. Online presence analysis
        presence_result = self.analyze_online_presence(employer_name)
        verification_results.append(presence_result)
        if presence_result["suspicious"]:
            risk_score += 0.25
        
        # 4. Income plausibility
        income_result = self.check_income_plausibility(
            application.get("job_title"),
            application.get("annual_income")
        )
        verification_results.append(income_result)
        if income_result["implausible"]:
            risk_score += 0.30
        
        # 5. IRS verification recommendation
        if risk_score > 0.3:
            verification_results.append({
                "type": "recommendation",
                "action": "Request 4506-C IRS transcript",
                "reason": "High employment fraud risk"
            })
        
        return {
            "employment_fraud_risk": min(risk_score, 1.0),
            "verification_results": verification_results,
            "recommendation": self.get_recommendation(risk_score)
        }
    
    def check_business_registry(self, 
                                name: str, 
                                ein: str,
                                state: str) -> dict:
        """Check business registration status"""
        
        # Query state business registry
        registration = self.state_registry.lookup(name, state)
        
        if not registration:
            return {
                "type": "business_registry",
                "found": False,
                "risk": True,
                "risk_weight": 0.40,
                "issue": "Business not found in state registry"
            }
        
        # Check registration date
        reg_date = registration.get("registration_date")
        today = date.today()
        age_months = (today - reg_date).days / 30
        
        if age_months < 12:
            return {
                "type": "business_registry",
                "found": True,
                "risk": True,
                "risk_weight": 0.30,
                "issue": f"Business registered only {age_months:.0f} months ago",
                "registration": registration
            }
        
        return {
            "type": "business_registry",
            "found": True,
            "risk": False,
            "age_months": age_months,
            "status": registration.get("status")
        }
    
    def analyze_online_presence(self, employer_name: str) -> dict:
        """Analyze employer's online presence"""
        
        signals = {
            "website_exists": False,
            "linkedin_company": False,
            "reviews_exist": False,
            "news_mentions": False
        }
        
        # Check website
        website = self.find_company_website(employer_name)
        if website:
            signals["website_exists"] = True
            
            # Analyze website quality
            website_analysis = self.analyze_website(website)
            signals["website_quality"] = website_analysis
        
        # Check LinkedIn
        linkedin = self.linkedin_api.search_company(employer_name)
        if linkedin:
            signals["linkedin_company"] = True
            signals["linkedin_employees"] = linkedin.get("employee_count", 0)
        
        # Check reviews (Glassdoor, Indeed)
        reviews = self.check_employer_reviews(employer_name)
        signals["reviews_exist"] = len(reviews) > 0
        signals["review_count"] = len(reviews)
        
        # Calculate suspicion score
        presence_score = sum([
            signals["website_exists"],
            signals["linkedin_company"],
            signals["reviews_exist"],
            signals["news_mentions"]
        ])
        
        suspicious = presence_score < 2
        
        return {
            "type": "online_presence",
            "signals": signals,
            "presence_score": presence_score,
            "suspicious": suspicious,
            "issue": "Limited online presence for claimed employer" if suspicious else None
        }
    
    def check_income_plausibility(self, 
                                  job_title: str,
                                  annual_income: float) -> dict:
        """Check if income is plausible for role"""
        
        # Normalize job title
        normalized_title = self.normalize_title(job_title)
        
        if normalized_title in self.INCOME_RANGES:
            min_income, max_income = self.INCOME_RANGES[normalized_title]
            
            if annual_income > max_income * 1.5:
                return {
                    "type": "income_plausibility",
                    "implausible": True,
                    "stated_income": annual_income,
                    "expected_range": (min_income, max_income),
                    "issue": f"Income ${annual_income:,.0f} exceeds typical range for {job_title}"
                }
            
            if annual_income < min_income * 0.5:
                return {
                    "type": "income_plausibility",
                    "implausible": True,
                    "stated_income": annual_income,
                    "expected_range": (min_income, max_income),
                    "issue": f"Income ${annual_income:,.0f} below typical range for {job_title}"
                }
        
        return {
            "type": "income_plausibility",
            "implausible": False,
            "stated_income": annual_income,
            "title": job_title
        }
```

---

## References

- [FBI: Employment Fraud Schemes](https://www.fbi.gov/investigate/white-collar-crime/mortgage-fraud)
- [Fannie Mae: Employment Verification](https://selling-guide.fanniemae.com/)
- [IRS Form 4506-C](https://www.irs.gov/forms-pubs/about-form-4506-c)
- [CrossCheck: Employment Verification](https://crosscheckcompliance.com/)
