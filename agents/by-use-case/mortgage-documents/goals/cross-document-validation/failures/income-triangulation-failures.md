# Income Triangulation Failures

## Issue: AI System Fails to Reconcile Income Across Multiple Document Sources

**Frequency**: Common

**Symptoms**
- W-2 Box 1 doesn't match tax return Line 1
- Pay stub YTD doesn't annualize to W-2
- VOE income differs from pay stubs
- Multiple income sources not aggregated correctly
- Overtime/bonus treated inconsistently
- Tax transcript doesn't match provided W-2
- Self-employment income not reconciled with Schedule C

**Root Cause**
Qualifying income must be verified across multiple sources. W-2 wages should match tax return wages, pay stub YTD should be proportional to W-2, and VOE should confirm all figures. AI systems that extract income from each document independently may miss discrepancies that indicate fraud or data entry errors.

**Example**
```
Scenario 1: W-2 vs. Tax Return mismatch

W-2 provided:
- Box 1 Wages: $85,000
- Employer: ABC Corp

Tax Return (1040):
- Line 1 Wages: $72,000

AI extraction:
- W-2 income: $85,000 ✓
- Tax return income: $72,000 ✓

Triangulation not performed:
- $13,000 discrepancy not flagged
- Which is correct?

Possible explanations:
1. W-2 altered (fraud)
2. Tax return missing second W-2
3. Tax return from prior year
4. Pre-tax deductions (shouldn't differ this much)

Risk: High - unexplained $13K variance

---

Scenario 2: Pay stub YTD extrapolation error

Pay stub (March 15):
- Current gross: $3,500
- YTD gross: $14,000

Expected annualized (using YTD):
- $14,000 ÷ 2.5 months × 12 = $67,200

W-2 from prior year:
- Box 1: $84,000

AI calculation:
- Used current pay × 24 = $84,000 ✓ (matches W-2)

Problem:
- YTD suggests lower income ($67,200)
- Recent pay cut or reduced hours?
- AI used wrong calculation method

Correct approach:
- Compare YTD annualized vs. prior W-2
- Flag 20%+ variance for review
- Consider trend direction

---

Scenario 3: Multiple employers not aggregated

Borrower has two jobs:

Job 1:
- W-2: $55,000
- Pay stub: $2,291/month

Job 2:
- W-2: $32,000
- Pay stub: $1,333/month

Tax return:
- Line 1: $87,000 (combined)

AI extraction:
- Job 1 income: $55,000
- Job 2 income: $32,000
- Tax return: $87,000

Triangulation:
- $55,000 + $32,000 = $87,000 ✓
- Tax return matches ✓

But AI reported:
- "Primary income: $55,000" (only counted one job)

← Multi-employer aggregation failure
← Understated qualifying income

---

Scenario 4: Self-employment income triangulation

Schedule C shows:
- Gross receipts: $180,000
- Expenses: $95,000
- Net profit: $85,000

Tax return:
- Schedule SE: $85,000 (matches)
- Line 12 (Schedule 1): $85,000 (matches)

Bank statements (business account):
- Average monthly deposits: $15,000
- Annual: $180,000 (matches gross)

AI triangulation needed:
- Net profit = Gross - Expenses ✓
- Bank deposits ≈ Gross receipts ✓
- Add-backs calculated (depreciation, etc.)

What AI missed:
- Depreciation: $12,000 (should add back)
- Qualifying income: $85,000 + $12,000 = $97,000

← Add-back calculation missed
← Income understated

---

Income triangulation matrix:

  Document relationships:
  
  W-2 Box 1 ←→ Tax Return Line 1
    Expected: Match within $500
    Red flag: >5% variance
    
  Pay Stub YTD ←→ W-2 (annualized)
    Expected: Proportional to time elapsed
    Red flag: >10% variance
    
  VOE Salary ←→ Pay Stub Rate
    Expected: Match exactly
    Red flag: Any variance
    
  Tax Transcript ←→ Provided W-2
    Expected: Exact match
    Red flag: Any variance (critical)
    
  Schedule C ←→ Business Bank Deposits
    Expected: Deposits ≈ Gross receipts
    Red flag: Deposits much higher (unreported income)
    Red flag: Deposits much lower (inflated gross)
```

**Key Statistics**
From Income Verification Research (2025-2026):
- Income discrepancies found: 8-12% of applications
- W-2 vs. tax return mismatches: 5-7%
- Pay stub extrapolation errors: 10-15%
- Self-employment calculation errors: 20-30%

**Contributing Factors**
- Independent document processing
- No cross-document correlation
- Calculation method variations
- Multiple income source handling
- Add-back rules not applied
- Tax transcript not used for verification

---

## Mitigation Strategies

### Prevention
1. **Triangulation matrix**: Define expected relationships
2. **Variance thresholds**: Flag discrepancies by type
3. **IRS transcript verification**: Ground truth for W-2s
4. **Calculation standardization**: Consistent methods
5. **Multi-source aggregation**: Combine all income sources
6. **Add-back automation**: Apply depreciation/depletion rules

### Implementation
```python
class IncomeTriangulator:
    """Triangulate income across multiple documents"""
    
    VARIANCE_THRESHOLDS = {
        "w2_vs_tax_return": 0.02,  # 2%
        "paystub_vs_w2": 0.10,     # 10%
        "voe_vs_paystub": 0.01,   # 1%
        "transcript_vs_w2": 0.0,  # Exact match
        "schedule_c_vs_bank": 0.15  # 15%
    }
    
    def triangulate_income(self, documents: dict) -> dict:
        """Perform full income triangulation"""
        
        results = {
            "triangulations": [],
            "discrepancies": [],
            "calculated_income": None,
            "risk_score": 0
        }
        
        # W-2 vs Tax Return
        if documents.get("w2") and documents.get("tax_return"):
            w2_result = self.triangulate_w2_tax(
                documents["w2"],
                documents["tax_return"]
            )
            results["triangulations"].append(w2_result)
            if w2_result["discrepancy"]:
                results["discrepancies"].append(w2_result)
                results["risk_score"] += 0.3
        
        # Pay Stub vs W-2
        if documents.get("pay_stub") and documents.get("w2"):
            ps_result = self.triangulate_paystub_w2(
                documents["pay_stub"],
                documents["w2"]
            )
            results["triangulations"].append(ps_result)
            if ps_result["discrepancy"]:
                results["discrepancies"].append(ps_result)
                results["risk_score"] += 0.2
        
        # Tax Transcript vs W-2 (critical)
        if documents.get("tax_transcript") and documents.get("w2"):
            transcript_result = self.triangulate_transcript_w2(
                documents["tax_transcript"],
                documents["w2"]
            )
            results["triangulations"].append(transcript_result)
            if transcript_result["discrepancy"]:
                results["discrepancies"].append(transcript_result)
                results["risk_score"] += 0.5  # High weight
        
        # Self-employment triangulation
        if documents.get("schedule_c"):
            se_result = self.triangulate_self_employment(
                documents["schedule_c"],
                documents.get("bank_statements"),
                documents.get("tax_return")
            )
            results["triangulations"].append(se_result)
            if se_result["discrepancy"]:
                results["discrepancies"].append(se_result)
                results["risk_score"] += 0.25
        
        # Calculate final qualifying income
        results["calculated_income"] = self.calculate_qualifying_income(
            documents
        )
        
        results["risk_score"] = min(results["risk_score"], 1.0)
        
        return results
    
    def triangulate_w2_tax(self, w2: dict, tax_return: dict) -> dict:
        """Compare W-2 wages to tax return Line 1"""
        
        w2_wages = w2.get("box1_wages", 0)
        tax_wages = tax_return.get("line1_wages", 0)
        
        # Handle multiple W-2s
        if isinstance(w2, list):
            w2_wages = sum(w.get("box1_wages", 0) for w in w2)
        
        variance = abs(w2_wages - tax_wages)
        variance_pct = variance / max(w2_wages, 1)
        
        threshold = self.VARIANCE_THRESHOLDS["w2_vs_tax_return"]
        discrepancy = variance_pct > threshold
        
        return {
            "comparison": "w2_vs_tax_return",
            "w2_amount": w2_wages,
            "tax_amount": tax_wages,
            "variance": variance,
            "variance_pct": variance_pct,
            "threshold": threshold,
            "discrepancy": discrepancy,
            "risk": "high" if variance > 5000 else "medium" if discrepancy else "low"
        }
    
    def triangulate_paystub_w2(self, pay_stub: dict, w2: dict) -> dict:
        """Compare pay stub YTD to W-2 (annualized)"""
        
        ytd_gross = pay_stub.get("ytd_gross", 0)
        pay_date = pay_stub.get("pay_date")
        w2_wages = w2.get("box1_wages", 0)
        w2_year = w2.get("tax_year")
        
        # Calculate expected YTD based on W-2
        if pay_date and w2_year:
            days_elapsed = (pay_date - date(pay_date.year, 1, 1)).days + 1
            expected_ytd = w2_wages * (days_elapsed / 365)
            
            variance = abs(ytd_gross - expected_ytd)
            variance_pct = variance / max(expected_ytd, 1)
            
            threshold = self.VARIANCE_THRESHOLDS["paystub_vs_w2"]
            discrepancy = variance_pct > threshold
            
            # Check direction of variance
            trend = "stable"
            if ytd_gross > expected_ytd * 1.15:
                trend = "increasing"
            elif ytd_gross < expected_ytd * 0.85:
                trend = "decreasing"
            
            return {
                "comparison": "paystub_vs_w2",
                "ytd_gross": ytd_gross,
                "expected_ytd": expected_ytd,
                "w2_wages": w2_wages,
                "variance_pct": variance_pct,
                "threshold": threshold,
                "discrepancy": discrepancy,
                "trend": trend,
                "risk": "high" if trend == "decreasing" and discrepancy else 
                        "medium" if discrepancy else "low"
            }
        
        return {"comparison": "paystub_vs_w2", "error": "Missing date information"}
    
    def triangulate_transcript_w2(self, 
                                  transcript: dict, 
                                  w2: dict) -> dict:
        """Compare IRS transcript to provided W-2 (critical check)"""
        
        transcript_wages = transcript.get("wages_tips", 0)
        w2_wages = w2.get("box1_wages", 0)
        
        # This should be exact match
        discrepancy = transcript_wages != w2_wages
        
        return {
            "comparison": "transcript_vs_w2",
            "transcript_amount": transcript_wages,
            "w2_amount": w2_wages,
            "discrepancy": discrepancy,
            "variance": abs(transcript_wages - w2_wages),
            "risk": "critical" if discrepancy else "low",
            "action": "W-2 may be altered - investigate" if discrepancy else None
        }
```

### Risk Scoring for Income Discrepancies

| Discrepancy Type | Risk Score | Action |
|-----------------|------------|--------|
| Transcript ≠ W-2 | 0.5 | Fraud investigation |
| W-2 vs Tax Return >5% | 0.3 | Request explanation |
| Pay stub YTD declining trend | 0.25 | Use lower income |
| Self-employment variance >15% | 0.2 | Additional documentation |
| VOE ≠ pay stub | 0.15 | Clarify with employer |

---

## References

- [Fannie Mae Income Calculator](https://singlefamily.fanniemae.com/applications-technology/income-calculator)
- [IRS Form 4506-C](https://www.irs.gov/forms-pubs/about-form-4506-c)
- [Freddie Mac Income Documentation](https://guide.freddiemac.com/)
