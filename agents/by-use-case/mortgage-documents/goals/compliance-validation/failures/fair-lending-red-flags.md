# Fair Lending Red Flag Detection Failures

## Issue: OCR System Fails to Detect Fair Lending Compliance Concerns

**Frequency**: Occasional but high regulatory/reputational risk

**Symptoms**
- Pricing disparities by demographic not flagged
- Steering indicators undetected
- Redlining patterns missed
- Underwriting inconsistencies by protected class
- Disparate impact unidentified
- Documentation of exceptions inconsistent

**Root Cause**
Fair lending laws (ECOA, Fair Housing Act) prohibit discrimination in mortgage lending. OCR extracts loan data but doesn't analyze patterns across applications or compare treatment by protected class characteristics. Without fair lending analysis, disparate treatment and disparate impact go undetected, creating regulatory and legal exposure.

**Example**
```
Scenario 1: Pricing disparity

Loans in same census tract, same risk profile:
Borrower A (majority tract): Rate 5.5%, Points 0.5
Borrower B (minority tract): Rate 5.875%, Points 1.0

Risk factors identical:
- Same credit score range
- Same LTV
- Same DTI
- Same loan amount

OCR: Both loans documented correctly ✓
Missing: Pricing comparison analysis

← 0.375% rate difference unexplained
← Potential ECOA/FHA violation
← No pattern analysis performed

---

Scenario 2: Underwriting inconsistency

Loan 1 approved:
- DTI: 48%
- Credit score: 680
- Exception granted for DTI

Loan 2 denied:
- DTI: 46%
- Credit score: 690
- No exception offered

Difference: Applicant demographics

OCR: Both files documented
Missing: Exception consistency analysis

← Better-qualified applicant denied
← No exception offered
← Potential disparate treatment

---

Scenario 3: Steering indicators

Refinance transaction:
- Borrower qualified for conventional
- Placed in FHA (higher costs)
- No documentation of borrower preference

Conventional would have provided:
- Lower MI costs
- No upfront MIP
- Better long-term terms

OCR: FHA documentation complete ✓
Missing: Product suitability analysis

← Steering to less favorable product
← Protected class concentration in FHA
← Fair lending concern

---

Scenario 4: Documentation disparity

Conventional loan:
- Income: 2 years paystubs required
- Assets: 60 days statements

Same conventional loan (different applicant):
- Income: 3 years tax returns + CPA letter
- Assets: 6 months statements + source letters

OCR: Both documented per requirements
Issue: Different documentation burden

← Excessive documentation for some borrowers
← Pattern correlates with demographics

---

Fair lending detection failures:
  
  Files with fair lending concerns: 5%
  
  Issue types:
    Pricing disparities: 30%
    Underwriting inconsistencies: 25%
    Steering indicators: 20%
    Documentation disparities: 15%
    Exception inconsistencies: 10%
  
  Impact:
    Regulatory examination findings: 8%
    DOJ/CFPB enforcement risk: Variable
    Fair lending settlements: $Millions
```

**Key Statistics**
From Fair Lending Research (2026):
- Pricing variance (unexplained): 15-25 bps average
- Exception inconsistencies: 10-15%
- Steering findings: 3-5%
- Enforcement actions: Increasing

**Protected Classes**
- Race, Color, National Origin
- Religion
- Sex (including pregnancy, sexual orientation, gender identity)
- Familial Status
- Disability
- Age
- Receipt of public assistance

**Contributing Factors**
- Single-file processing (no pattern analysis)
- No demographic correlation
- Exception tracking absent
- Pricing analysis not performed
- Underwriting consistency not measured

---

## Mitigation Strategies

### Prevention
1. **Pricing analysis**: Compare rates across demographics
2. **Exception tracking**: Consistent criteria and documentation
3. **Product placement review**: Analyze steering patterns
4. **Documentation standards**: Uniform requirements
5. **Pattern analysis**: Cross-file comparison

### Implementation
```python
class FairLendingAnalyzer:
    """Analyze fair lending compliance"""
    
    PRICING_VARIANCE_THRESHOLD = 0.25  # 25 bps
    
    def analyze_pricing_disparity(self, loans: list) -> dict:
        """Analyze pricing across demographic groups"""
        # Group loans by similar risk profile
        risk_groups = self.group_by_risk_profile(loans)
        
        disparities = []
        
        for group_key, group_loans in risk_groups.items():
            # Compare pricing across census tract characteristics
            by_tract_type = self.group_by_tract_type(group_loans)
            
            if "majority" in by_tract_type and "minority" in by_tract_type:
                majority_avg = self.average_rate(by_tract_type["majority"])
                minority_avg = self.average_rate(by_tract_type["minority"])
                
                variance = minority_avg - majority_avg
                
                if variance > self.PRICING_VARIANCE_THRESHOLD:
                    disparities.append({
                        "risk_group": group_key,
                        "majority_avg_rate": majority_avg,
                        "minority_avg_rate": minority_avg,
                        "variance_bps": variance * 100,
                        "flag": "pricing_disparity"
                    })
        
        return {
            "disparities_found": len(disparities) > 0,
            "disparities": disparities,
            "action": "fair_lending_review" if disparities else None
        }
    
    def analyze_exception_consistency(self, loans: list) -> dict:
        """Analyze underwriting exception consistency"""
        exceptions = [l for l in loans if l.get("has_exception")]
        denials = [l for l in loans if l.get("decision") == "denied"]
        
        inconsistencies = []
        
        # Find denials that could have received exception
        for denial in denials:
            for exception in exceptions:
                if self.similar_profile(denial, exception):
                    if denial["risk_score"] <= exception["risk_score"]:
                        inconsistencies.append({
                            "denied_loan": denial["loan_id"],
                            "exception_loan": exception["loan_id"],
                            "denied_score": denial["risk_score"],
                            "exception_score": exception["risk_score"],
                            "flag": "exception_inconsistency"
                        })
        
        return {
            "inconsistencies": inconsistencies,
            "review_required": len(inconsistencies) > 0
        }
    
    def detect_steering_indicators(self, loan: dict) -> dict:
        """Detect potential steering indicators"""
        indicators = []
        
        # Check if conventional eligible but placed in FHA/VA
        if loan.get("product") in ["FHA", "VA"]:
            if self.conventional_eligible(loan):
                if not loan.get("borrower_product_preference"):
                    indicators.append({
                        "type": "potential_steering",
                        "actual_product": loan["product"],
                        "eligible_for": "Conventional",
                        "documentation": "No preference documented"
                    })
        
        # Check if higher-cost loan when lower available
        if loan.get("rate") > self.best_available_rate(loan):
            variance = loan["rate"] - self.best_available_rate(loan)
            if variance > 0.25 and not loan.get("rate_justification"):
                indicators.append({
                    "type": "pricing_steering",
                    "actual_rate": loan["rate"],
                    "best_available": self.best_available_rate(loan),
                    "variance": variance
                })
        
        return {
            "steering_indicators": indicators,
            "risk_level": "high" if indicators else "none"
        }
    
    def compare_documentation_burden(self, loans: list) -> dict:
        """Compare documentation requirements"""
        doc_counts = []
        
        for loan in loans:
            doc_counts.append({
                "loan_id": loan["loan_id"],
                "census_tract": loan["census_tract"],
                "documents_required": len(loan.get("documents", [])),
                "conditions_required": len(loan.get("conditions", []))
            })
        
        # Compare across tract types
        by_tract = self.group_by_tract_type(doc_counts)
        
        if "majority" in by_tract and "minority" in by_tract:
            maj_avg = sum(d["documents_required"] for d in by_tract["majority"]) / len(by_tract["majority"])
            min_avg = sum(d["documents_required"] for d in by_tract["minority"]) / len(by_tract["minority"])
            
            if min_avg > maj_avg * 1.2:  # 20% more docs
                return {
                    "disparity": True,
                    "majority_avg_docs": maj_avg,
                    "minority_avg_docs": min_avg,
                    "flag": "documentation_disparity"
                }
        
        return {"disparity": False}
```

---

## References

- [ECOA](https://www.consumerfinance.gov/rules-policy/regulations/1002/) - Equal Credit Opportunity Act
- [Fair Housing Act](https://www.hud.gov/program_offices/fair_housing_equal_opp/fair_housing_act_overview) - HUD
- [CFPB Fair Lending](https://www.consumerfinance.gov/fair-lending/) - Compliance resources
- [OCC Fair Lending](https://www.occ.gov/topics/consumers-and-communities/consumer-protection/fair-lending/index-fair-lending.html) - Examination procedures
