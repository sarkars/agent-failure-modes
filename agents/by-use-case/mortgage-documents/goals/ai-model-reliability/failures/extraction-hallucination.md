# Extraction Hallucination

## Issue: LLMs Fabricating or Misreading Values from Mortgage Documents

**Frequency**: Common

**Symptoms**
- Extracted income doesn't match document
- Dates pulled that don't appear in source
- Employer names partially correct but modified
- Asset balances confidently wrong
- Field values swapped between documents
- Data extracted from wrong document entirely
- High confidence scores on fabricated data

**Root Cause**
Large Language Models used for document extraction can hallucinate—generating plausible but incorrect data. Unlike OCR errors (character misreads), LLM hallucinations create coherent but fabricated values. The model may "fill in" expected values, transpose data from prior context, or generate syntactically correct but factually wrong extractions.

**Example**
```
Scenario 1: Income fabrication

W-2 Document (actual):
- Box 1 Wages: $72,450.00
- Box 12a (401k): $8,500.00

LLM Extraction:
- Box 1 Wages: $80,950.00  ← HALLUCINATED
- Box 12a (401k): $8,500.00 ✓

What happened:
- Model added Box 1 + Box 12a = $80,950
- Created "plausible" total income figure
- High confidence: 0.94

← LLM performed incorrect arithmetic
← Created coherent but wrong value
← Confidence score misleading

---

Scenario 2: Date hallucination

Pay stub shows:
- Pay period: 03/01/2026 - 03/15/2026
- Pay date: 03/20/2026

LLM Extraction:
- Pay period end: 03/15/2026 ✓
- Pay date: 03/15/2026 ← HALLUCINATED

What happened:
- Model confused period end with pay date
- Generated plausible but incorrect date
- Timing validation would fail

← Common date field confusion
← Creates downstream calculation errors

---

Scenario 3: Cross-document contamination

Context window contains:
- Document 1: John Smith's W-2, $95,000
- Document 2: Jane Smith's W-2, $62,000

Extracting Document 2:

LLM Output:
- Employee: Jane Smith ✓
- Employer: Same as Document 1 ← HALLUCINATED
- Wages: $95,000 ← CONTAMINATED from Doc 1

What happened:
- Prior document "leaked" into extraction
- Model retrieved wrong employer
- Income attributed to wrong borrower

← Context window contamination
← Critical for co-borrower loans

---

Scenario 4: Plausible fabrication

Bank statement shows:
- Account ending: ...4521
- Ending balance: [illegible/damaged area]

LLM Extraction:
- Account: ...4521 ✓
- Ending balance: $45,210.00 ← HALLUCINATED

What happened:
- Model couldn't read damaged area
- Generated "plausible" balance using account digits
- No indication of low confidence or uncertainty

← Fabricated coherent value from partial data
← No uncertainty flag raised

---

Hallucination patterns in mortgage extraction:

  Hallucination frequency by document type:
    W-2s: 5-8% of extractions
    Pay stubs: 8-12% of extractions
    Bank statements: 10-15% of extractions
    Tax returns: 12-18% of extractions
  
  Hallucination types:
    Arithmetic combinations: 30%
    Cross-document contamination: 25%
    Field transposition: 20%
    Plausible fabrication: 15%
    Date confusion: 10%
  
  Detection difficulty:
    OCR errors: Detectable (obviously wrong)
    LLM hallucinations: Hard (plausible values)
```

**Key Statistics**
From LLM Document Extraction Research (2025-2026):
- LLM extraction hallucination rate: 5-18% depending on document complexity
- Hallucinations with high confidence: 60-70% of hallucinated values
- Detection rate without verification: 10-20%
- Financial impact per undetected hallucination: $500-$50,000

**Contributing Factors**
- LLMs trained to generate coherent output
- No "I don't know" training for extraction
- Context window mixing multiple documents
- Poor document quality triggers fabrication
- Confidence calibration not designed for extraction
- Pressure to extract values even from damaged documents

---

## Mitigation Strategies

### Prevention
1. **Multi-pass extraction**: Multiple models, compare outputs
2. **Source highlighting**: Require model to cite exact location
3. **Confidence calibration**: Train for extraction uncertainty
4. **Cross-validation**: Verify against independent sources
5. **Arithmetic validation**: Check internal consistency
6. **Human review thresholds**: Force review on key fields

### Implementation
```python
class HallucinationDetector:
    """Detect LLM hallucination in document extraction"""
    
    ARITHMETIC_FIELDS = {
        "w2": [("box1", "box3", "box1 >= box3")],
        "paystub": [
            ("gross_pay", "net_pay", "gross_pay > net_pay"),
            ("ytd_gross", "current_gross", "ytd_gross >= current_gross")
        ]
    }
    
    def verify_extraction(self, 
                         document: dict,
                         extraction: dict,
                         doc_type: str) -> dict:
        """Verify extraction for potential hallucination"""
        
        issues = []
        
        # Check arithmetic consistency
        arith_result = self.check_arithmetic(doc_type, extraction)
        if arith_result["violations"]:
            issues.extend(arith_result["violations"])
        
        # Check for cross-document contamination
        if document.get("context_docs"):
            contam_result = self.check_contamination(
                extraction, 
                document["context_docs"]
            )
            if contam_result["contaminated"]:
                issues.append({
                    "type": "cross_document_contamination",
                    "fields": contam_result["fields"],
                    "severity": "high"
                })
        
        # Check source citation
        for field, value in extraction.items():
            citation = extraction.get(f"{field}_source_location")
            if not citation:
                issues.append({
                    "type": "missing_source_citation",
                    "field": field,
                    "severity": "medium"
                })
        
        # Check plausibility
        plausibility = self.check_plausibility(doc_type, extraction)
        if plausibility["suspicious"]:
            issues.extend(plausibility["issues"])
        
        return {
            "likely_hallucination": len(issues) > 0,
            "issues": issues,
            "confidence_adjustment": self.calculate_confidence_adjustment(issues),
            "recommendation": "human_review" if len(issues) > 0 else "proceed"
        }
    
    def check_arithmetic(self, doc_type: str, extraction: dict) -> dict:
        """Check internal arithmetic consistency"""
        violations = []
        
        rules = self.ARITHMETIC_FIELDS.get(doc_type, [])
        
        for field1, field2, rule in rules:
            val1 = extraction.get(field1)
            val2 = extraction.get(field2)
            
            if val1 is not None and val2 is not None:
                # Evaluate rule
                if not eval(rule.replace(field1, str(val1)).replace(field2, str(val2))):
                    violations.append({
                        "type": "arithmetic_violation",
                        "rule": rule,
                        "values": {field1: val1, field2: val2},
                        "severity": "high"
                    })
        
        return {"violations": violations}
    
    def check_contamination(self, 
                           extraction: dict,
                           context_docs: list) -> dict:
        """Check if values leaked from other documents"""
        
        contaminated_fields = []
        
        for field, value in extraction.items():
            for ctx_doc in context_docs:
                ctx_extraction = ctx_doc.get("extraction", {})
                
                # Check if value appears in wrong document
                for ctx_field, ctx_value in ctx_extraction.items():
                    if ctx_value == value and ctx_field != field:
                        # Value from different document, different field
                        contaminated_fields.append({
                            "field": field,
                            "value": value,
                            "source_doc": ctx_doc["id"],
                            "source_field": ctx_field
                        })
        
        return {
            "contaminated": len(contaminated_fields) > 0,
            "fields": contaminated_fields
        }
    
    def multi_pass_extraction(self, 
                             document: dict,
                             models: list) -> dict:
        """Extract using multiple models, compare for hallucination"""
        
        extractions = []
        for model in models:
            result = model.extract(document)
            extractions.append(result)
        
        # Compare extractions
        consensus = {}
        disagreements = []
        
        all_fields = set()
        for ext in extractions:
            all_fields.update(ext.keys())
        
        for field in all_fields:
            values = [ext.get(field) for ext in extractions if field in ext]
            
            if len(set(values)) == 1:
                # All models agree
                consensus[field] = values[0]
            else:
                # Disagreement - potential hallucination
                disagreements.append({
                    "field": field,
                    "values": values,
                    "action": "human_review"
                })
        
        return {
            "consensus": consensus,
            "disagreements": disagreements,
            "hallucination_risk": len(disagreements) / len(all_fields) if all_fields else 0
        }
```

---

## References

- [SCN Soft: LLMs for Mortgage](https://www.scnsoft.com/lending/large-language-models)
- [BizTech: LLM Hallucinations in Financial Institutions](https://biztechmagazine.com/article/2025/08/llm-hallucinations-what-are-implications-financial-institutions)
- [PerformLine: How LLMs Represent Financial Products](https://performline.com/blog-post/how-llms-represent-financial-products/)
- [Nature: Hallucination Detection and Mitigation](https://www.nature.com/articles/s41598-025-31075-1)
