# Appraisal Data Discrepancy Detection Failures

## Issue: AI QC System Fails to Detect Appraisal Inconsistencies That Trigger GSE Findings

**Frequency**: Common - Top defect category per Fannie Mae

**Symptoms**
- Property details don't match MLS data
- Comparable sales adjustments inconsistent
- GLA (gross living area) mismatches between sources
- Photos don't match property description
- Market conditions analysis contradicts data
- Prior sale information incorrect
- Subject property address variations

**Root Cause**
Five of the top ten loan quality findings from Fannie Mae relate to appraisal data. AI QC systems must cross-reference appraisal data against multiple sources (MLS, county records, prior appraisals, collateral data), but often fail to detect subtle discrepancies. These mismatches trigger GSE findings and potential repurchase demands.

**Example**
```
Scenario 1: GLA mismatch

Appraisal shows:
- Subject GLA: 2,450 sq ft
- Source: "Measured by appraiser"

County records show:
- Finished area: 2,150 sq ft
- Last update: 2024

Fannie Mae Collateral Underwriter (CU):
- Flags 300 sq ft discrepancy
- Requires explanation or re-measure

AI QC result: No flag raised

← 300 sq ft = significant discrepancy
← 14% variance affects value
← AI didn't cross-reference county data

---

Scenario 2: Comparable adjustment inconsistency

Appraisal grid:
  Comp 1: +$10,000 for inferior location
  Comp 2: +$5,000 for inferior location (same neighborhood)
  Comp 3: -$8,000 for superior location

Issue: Comps 1 and 2 are in same neighborhood but have
       different location adjustments (+$10K vs +$5K)

AI QC result: Adjustments within guidelines ✓

CU finding: "Inconsistent location adjustments for 
           similar properties"

← AI validated each adjustment individually
← Failed to compare adjustments across comps
← Common GSE finding pattern

---

Scenario 3: Market conditions vs. data

Appraisal states:
- Market conditions: "Stable"
- Days on market: "30-60 days typical"

MLS data shows:
- Median DOM last 6 months: 15 days
- Price appreciation: +8% YoY
- Multiple offer situations: 65% of sales

Discrepancy: Market is actually "increasing," not "stable"
Impact: May affect value conclusion and risk assessment

AI QC result: Market conditions field populated ✓

← AI validated field presence, not accuracy
← Failed to verify against actual market data
← Appraisal understates market strength

---

Scenario 4: Photo inconsistency

Appraisal describes:
- "Well-maintained property"
- "Recently renovated kitchen"
- "No deferred maintenance observed"

Photos show:
- Peeling paint on exterior
- Original 1990s kitchen cabinets
- Cracked driveway

AI QC result: Photos present ✓

Human review finding: "Description inconsistent with photos"

← AI verified photo presence
← No image analysis performed
← Description/photo mismatch missed

---

Appraisal discrepancy patterns:

  Top GSE appraisal findings (Q1 2025):
    GLA discrepancies: 25%
    Adjustment inconsistencies: 20%
    Comp selection issues: 18%
    Market conditions errors: 15%
    Photo/description mismatches: 12%
    Other: 10%
  
  AI detection rates:
    GLA discrepancies: 40-60% (requires data cross-reference)
    Adjustment inconsistencies: 20-30% (complex logic)
    Market conditions: 10-20% (requires market data)
    Photo analysis: 5-10% (limited capability)
```

**Key Statistics**
From Fannie Mae Quality Insider (Q1 2025):
- Appraisal-related findings: 5 of top 10 defects
- GLA discrepancy threshold: 100 sq ft or 5%
- Adjustment inconsistencies: Leading cause of CU flags
- Photo-description mismatches: Growing concern

**Contributing Factors**
- Limited cross-reference data integration
- Adjustment comparison logic missing
- No image analysis capability
- Market data not integrated
- Individual field validation vs. holistic review
- CU findings not predicted by AI QC

---

## Mitigation Strategies

### Prevention
1. **County data integration**: Cross-reference GLA, lot size, rooms
2. **Adjustment comparison**: Flag inconsistencies across comps
3. **Market data feeds**: Validate conditions against MLS/market data
4. **Image analysis**: Compare photos to written descriptions
5. **CU prediction**: Model likely CU findings before submission
6. **Historical comparison**: Check against prior appraisals

### Implementation
```python
class AppraisalQCValidator:
    """Validate appraisals against GSE requirements"""
    
    GLA_THRESHOLD_PCT = 0.05  # 5%
    GLA_THRESHOLD_ABS = 100   # sq ft
    
    def validate_appraisal(self, appraisal: dict) -> dict:
        """Comprehensive appraisal validation"""
        findings = []
        
        # Check GLA against county records
        gla_result = self.validate_gla(appraisal)
        if gla_result["discrepancy"]:
            findings.append(gla_result)
        
        # Check adjustment consistency
        adj_result = self.validate_adjustments(appraisal)
        findings.extend(adj_result["inconsistencies"])
        
        # Check market conditions
        market_result = self.validate_market_conditions(appraisal)
        if market_result["mismatch"]:
            findings.append(market_result)
        
        # Predict CU findings
        cu_prediction = self.predict_cu_findings(appraisal)
        
        return {
            "findings": findings,
            "finding_count": len(findings),
            "cu_risk_score": cu_prediction["risk_score"],
            "predicted_cu_flags": cu_prediction["flags"],
            "recommendation": "address_before_delivery" if findings else "proceed"
        }
    
    def validate_gla(self, appraisal: dict) -> dict:
        """Validate GLA against county records"""
        appraisal_gla = appraisal.get("subject_gla")
        
        # Fetch county data
        county_data = self.county_api.get_property(
            appraisal["subject_address"]
        )
        county_gla = county_data.get("finished_area")
        
        if not county_gla:
            return {"discrepancy": False, "note": "No county data available"}
        
        # Calculate discrepancy
        diff = abs(appraisal_gla - county_gla)
        diff_pct = diff / county_gla
        
        if diff > self.GLA_THRESHOLD_ABS or diff_pct > self.GLA_THRESHOLD_PCT:
            return {
                "discrepancy": True,
                "type": "gla_mismatch",
                "appraisal_value": appraisal_gla,
                "county_value": county_gla,
                "difference": diff,
                "difference_pct": diff_pct,
                "severity": "high" if diff_pct > 0.10 else "medium",
                "action": "Require explanation or re-measure"
            }
        
        return {"discrepancy": False}
    
    def validate_adjustments(self, appraisal: dict) -> dict:
        """Check adjustment consistency across comparables"""
        comps = appraisal.get("comparables", [])
        inconsistencies = []
        
        # Group comps by similar characteristics
        adjustment_types = ["location", "gla", "condition", "view"]
        
        for adj_type in adjustment_types:
            adjustments = []
            
            for i, comp in enumerate(comps):
                adj_value = comp.get(f"{adj_type}_adjustment", 0)
                characteristic = comp.get(adj_type)
                adjustments.append({
                    "comp": i + 1,
                    "adjustment": adj_value,
                    "characteristic": characteristic
                })
            
            # Check for inconsistencies
            # Same characteristic should have similar adjustments
            grouped = {}
            for adj in adjustments:
                key = adj["characteristic"]
                if key not in grouped:
                    grouped[key] = []
                grouped[key].append(adj)
            
            for characteristic, adj_list in grouped.items():
                if len(adj_list) > 1:
                    values = [a["adjustment"] for a in adj_list]
                    if max(values) - min(values) > 5000:  # $5K threshold
                        inconsistencies.append({
                            "type": f"{adj_type}_adjustment_inconsistency",
                            "characteristic": characteristic,
                            "adjustments": adj_list,
                            "variance": max(values) - min(values),
                            "severity": "medium"
                        })
        
        return {"inconsistencies": inconsistencies}
    
    def validate_market_conditions(self, appraisal: dict) -> dict:
        """Validate market conditions against actual data"""
        stated_conditions = appraisal.get("market_conditions", "").lower()
        
        # Get market data
        market_data = self.market_api.get_conditions(
            appraisal["subject_address"],
            months=6
        )
        
        # Determine actual conditions
        appreciation = market_data.get("price_appreciation_yoy", 0)
        median_dom = market_data.get("median_days_on_market", 0)
        
        if appreciation > 5 and median_dom < 30:
            actual_conditions = "increasing"
        elif appreciation < -3 or median_dom > 90:
            actual_conditions = "declining"
        else:
            actual_conditions = "stable"
        
        if actual_conditions != stated_conditions:
            return {
                "mismatch": True,
                "type": "market_conditions_mismatch",
                "stated": stated_conditions,
                "actual": actual_conditions,
                "data": {
                    "appreciation_yoy": appreciation,
                    "median_dom": median_dom
                },
                "severity": "medium"
            }
        
        return {"mismatch": False}
```

---

## References

- [Fannie Mae Quality Insider Q1 2025](https://singlefamily.fanniemae.com/originating-underwriting/loan-quality/quality-insider/september-2025)
- [Fannie Mae Loan Quality](https://singlefamily.fanniemae.com/originating-underwriting/loan-quality)
- [Collateral Underwriter (CU)](https://singlefamily.fanniemae.com/applications-technology/collateral-underwriter)
