# Vendor Promise Gap

## Issue: Marketed AI Accuracy vs. Production Reality Creates Unmet Expectations

**Frequency**: Common

**Symptoms**
- Vendor claims 99%+ accuracy, production shows 80-90%
- Demo performance doesn't match live deployment
- "Out of the box" solution requires extensive customization
- Accuracy degrades over time without maintenance
- Edge cases far more common than vendor anticipated
- ROI projections not achieved
- Hidden manual review requirements

**Root Cause**
IDP and AI vendors often market accuracy metrics achieved on clean test datasets. Production mortgage documents are messier—handwritten notes, faded scans, unusual formats. The gap between vendor demos (curated documents) and production reality (diverse, imperfect documents) creates unrealistic expectations and implementation failures.

**Example**
```
Scenario 1: Demo vs. production accuracy

Vendor claim:
- "98.5% extraction accuracy"
- "90% straight-through processing"
- "Minimal training required"

Production reality (after 6 months):
- Extraction accuracy: 82-87%
- Straight-through processing: 45-55%
- Custom training: 200+ hours invested

Gap analysis:
- Demo documents: Clean, standard formats
- Production documents: Mixed quality, variations
- Missing from demo: Handwritten notes, stamps, faded docs

← 11-16 point accuracy gap
← Half the straight-through rate promised
← Significant hidden implementation cost

---

Scenario 2: "Universal" document support

Vendor promise:
- "Supports all standard mortgage documents"
- "No template configuration needed"
- "Works on any document layout"

Reality:
- 40% of document types needed custom templates
- New form versions required retraining
- Unusual layouts (non-GSE) failed completely
- 6-month customization project to reach viability

← "Universal" excluded many real document types
← Ongoing maintenance not disclosed
← Template-free claim was misleading

---

Scenario 3: Accuracy decay

Implementation timeline:
- Month 1: 91% accuracy (matches vendor claim)
- Month 6: 85% accuracy
- Month 12: 78% accuracy

Causes:
- New form versions released by GSEs
- Document quality variation in production
- No retraining performed
- Model drift on distribution shift

Vendor response: "Requires annual retraining subscription"

← Accuracy was point-in-time
← Maintenance not included
← Ongoing cost not in original ROI

---

Scenario 4: Hidden manual review

Vendor STP claim: "90% straight-through processing"

Actual workflow:
- AI processes: 100% of documents
- Low confidence: 40% flagged for review
- Manual review completed: 35%
- Manual correction: 15%
- True STP: 50%

What vendor measured:
- "Processing" = AI touched the document
- Not: document completed without human intervention

← Definition of STP manipulated
← Manual review requirement hidden
← Labor cost savings not realized

---

Vendor promise gap analysis:

  Common gap areas:
    Accuracy claims: 10-20 point gaps
    STP rates: 30-50 point gaps
    Implementation time: 2-4x longer
    Training requirements: 3-5x more
    Ongoing maintenance: Not disclosed
  
  Why gaps occur:
    Demo on clean data: 95%+ achievable
    Production data: 75-85% realistic
    Edge cases: Far more common
    Maintenance: Not factored in
    
  Industry reality:
    "There's a misconception in the market that IDP 
    is a magic wand. Vendors often overpromise and 
    underdeliver, touting 100 percent accuracy."
    — Industry analysis, 2026
```

**Key Statistics**
From IDP Implementation Research (2025-2026):
- Average accuracy gap: 10-15 percentage points
- STP rate gaps: 20-40 percentage points
- Implementation overruns: 2-3x typical
- 40% of IDP implementations underperform ROI projections
- Ongoing maintenance costs: Often unbudgeted

**Contributing Factors**
- Demo data curation
- Accuracy measured differently
- Edge cases underestimated
- Maintenance requirements hidden
- STP definitions vary
- ROI models overly optimistic
- Competitive pressure to over-claim

---

## Mitigation Strategies

### Evaluation Best Practices
1. **Test on your documents**: Use actual production samples
2. **Define metrics clearly**: Agree on measurement methodology
3. **Include edge cases**: Test unusual document types
4. **Pilot before commitment**: 30-60 day production pilot
5. **Include maintenance costs**: Factor in ongoing retraining
6. **Check references**: Talk to similar-sized customers

### Implementation
```python
class VendorEvaluationFramework:
    """Framework for evaluating AI vendor claims"""
    
    def conduct_pilot_evaluation(self, 
                                 vendor: object,
                                 test_documents: list) -> dict:
        """Evaluate vendor on production documents"""
        
        results = {
            "documents_processed": len(test_documents),
            "by_document_type": {},
            "overall_metrics": {},
            "edge_case_performance": {}
        }
        
        # Test each document
        for doc in test_documents:
            doc_type = doc["type"]
            
            # Get vendor extraction
            extraction = vendor.process(doc)
            
            # Compare to ground truth
            ground_truth = doc["ground_truth"]
            accuracy = self.calculate_accuracy(extraction, ground_truth)
            
            # Track by document type
            if doc_type not in results["by_document_type"]:
                results["by_document_type"][doc_type] = {
                    "count": 0,
                    "total_accuracy": 0,
                    "failed": 0
                }
            
            results["by_document_type"][doc_type]["count"] += 1
            results["by_document_type"][doc_type]["total_accuracy"] += accuracy
            
            if accuracy < 0.80:
                results["by_document_type"][doc_type]["failed"] += 1
        
        # Calculate overall metrics
        total_accuracy = sum(
            r["total_accuracy"] / r["count"] 
            for r in results["by_document_type"].values()
        ) / len(results["by_document_type"])
        
        results["overall_metrics"] = {
            "field_accuracy": total_accuracy,
            "stp_rate": self.calculate_stp_rate(test_documents),
            "manual_review_rate": self.calculate_review_rate(test_documents)
        }
        
        # Separate edge case analysis
        edge_cases = [d for d in test_documents if d.get("edge_case")]
        if edge_cases:
            edge_accuracy = self.evaluate_edge_cases(vendor, edge_cases)
            results["edge_case_performance"] = edge_accuracy
        
        return results
    
    def compare_to_vendor_claims(self, 
                                 evaluation_results: dict,
                                 vendor_claims: dict) -> dict:
        """Compare actual results to vendor claims"""
        
        comparisons = []
        
        for metric, claimed_value in vendor_claims.items():
            actual_value = evaluation_results["overall_metrics"].get(metric)
            
            if actual_value is not None:
                gap = claimed_value - actual_value
                gap_pct = (gap / claimed_value) * 100
                
                comparisons.append({
                    "metric": metric,
                    "claimed": claimed_value,
                    "actual": actual_value,
                    "gap": gap,
                    "gap_percentage": gap_pct,
                    "acceptable": gap_pct < 10  # 10% variance acceptable
                })
        
        overall_acceptable = all(c["acceptable"] for c in comparisons)
        
        return {
            "comparisons": comparisons,
            "overall_acceptable": overall_acceptable,
            "recommendation": "proceed" if overall_acceptable else "negotiate_or_decline"
        }
    
    def calculate_tco(self, 
                      vendor_pricing: dict,
                      evaluation_results: dict,
                      volume: int) -> dict:
        """Calculate true total cost of ownership"""
        
        # Base licensing
        base_cost = vendor_pricing.get("annual_license", 0)
        
        # Per-document costs
        per_doc_cost = vendor_pricing.get("per_document", 0)
        volume_cost = per_doc_cost * volume
        
        # Implementation (often underestimated)
        implementation = vendor_pricing.get("implementation", 0)
        implementation_actual = implementation * 2.5  # Industry average overrun
        
        # Manual review labor
        review_rate = evaluation_results["overall_metrics"]["manual_review_rate"]
        review_cost_per_doc = 5.00  # $5 per manual review
        annual_review_cost = volume * review_rate * review_cost_per_doc
        
        # Ongoing maintenance (often not quoted)
        maintenance = base_cost * 0.20  # 20% of license for maintenance
        
        # Retraining
        retraining = 10000  # Annual retraining estimate
        
        return {
            "vendor_quoted_annual": base_cost + volume_cost,
            "actual_tco": {
                "licensing": base_cost,
                "volume": volume_cost,
                "implementation_adjusted": implementation_actual,
                "manual_review_labor": annual_review_cost,
                "maintenance": maintenance,
                "retraining": retraining
            },
            "total_year_1": (
                base_cost + volume_cost + implementation_actual + 
                annual_review_cost + maintenance + retraining
            ),
            "hidden_costs": annual_review_cost + maintenance + retraining
        }
```

---

## References

- [Indecomm: Why Document AI Breaks Mortgage Ops](https://indecomm.com/article/why-document-ai-breaks-mortgage-ops/)
- [Chrisman Commentary: IDP - New Engine of Mortgage Efficiency](https://www.chrismancommentary.com/post/intelligent-document-processing-mortgage-efficiency)
- [IDP Software: IDP Challenges 2026](https://idp-software.com/guides/idp-challenges-2026/)
- [DocVu.AI: 7 Mortgage Document Challenges](https://www.docvu.ai/7-mortgage-document-challenges-lenders-cant-ignore-in-2026-and-how-docvu-ai-solves-them/)
