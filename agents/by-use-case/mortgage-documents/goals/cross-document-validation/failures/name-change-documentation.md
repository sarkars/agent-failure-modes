# Name Change Documentation Failures

## Issue: AI System Incorrectly Handles Legal Name Changes Across Document Timeline

**Frequency**: Occasional

**Symptoms**
- Maiden name flagged as identity mismatch
- Marriage certificate not linked to name change
- Divorce name reversion not tracked
- Court-ordered name change missed
- Gender transition name change not handled
- Prior deed in former name flagged as different person
- Credit report AKA names not correlated

**Root Cause**
Borrowers legally change names for marriage, divorce, court order, or other reasons. Documents from before the change show the prior name; documents after show the new name. AI systems must recognize that "Jane Smith" (prior deed) and "Jane Johnson" (current application) are the same person when marriage documentation connects them.

**Example**
```
Scenario 1: Marriage name change

Prior documents (2020-2023):
- Prior deed: "Jane Elizabeth Smith"
- Prior mortgage: "Jane E. Smith"
- Tax returns 2020-2022: "Jane Smith"

Current documents (2024+):
- Application: "Jane Elizabeth Johnson"
- Current W-2: "Jane E. Johnson"
- Current bank statements: "Jane Johnson"

Supporting documentation:
- Marriage certificate: Jane Smith → Jane Johnson (2023)

AI result without name change handling:
- "Jane Smith" ≠ "Jane Johnson" → MISMATCH
- Prior deed: Different owner?
- Flag for manual review

AI result with name change handling:
- Marriage certificate links names
- Prior documents: Verified as same person
- Proceed normally

← Name change documentation must be correlated
← Prior name documents still valid

---

Scenario 2: Divorce name reversion

Document timeline:
- 2018: Purchased property as "Sarah Miller"
- 2020: Married, became "Sarah Thompson"
- 2024: Divorced, reverted to "Sarah Miller"

Current application:
- Name: "Sarah Miller"
- Property: Purchased as "Sarah Miller" (2018) ← Matches!
- Credit report shows: "Sarah Thompson" AKA "Sarah Miller"

AI confusion:
- Which name is current?
- Is "Sarah Thompson" on credit report an error?
- Does applicant match original deed?

Resolution requires:
- Divorce decree showing name reversion
- Timeline correlation
- AKA name handling from credit report

---

Scenario 3: Court-ordered name change

Situation:
- Original name: "Robert James Wilson"
- Court order (2022): Changed to "Alex Jordan Wilson"
- Reason: Gender transition

Document state:
- Prior tax returns: "Robert J. Wilson"
- Prior W-2s: "Robert Wilson"
- Current documents: "Alex J. Wilson"
- SSA name change: Completed

AI challenges:
- First name completely different
- Not marriage/divorce related
- Requires court order correlation
- SSN unchanged

← Court order must link names
← No fuzzy matching will connect Robert → Alex
← Explicit documentation required

---

Scenario 4: Name change not properly marked

Credit report shows:
- Current name: "Jennifer Davis"
- AKA: "Jennifer Williams"

Application claims:
- Married in 2020
- Prior name: Williams

Issue:
- No marriage certificate provided
- AI flags AKA as unexplained
- Manual request for documentation

But applicant says:
- "I uploaded marriage certificate"

Investigation:
- Marriage certificate present in file
- AI didn't connect it to name change
- Document not indexed as "name change proof"

← Documentation existed but wasn't correlated
← AI needs to identify name change documents

---

Name change patterns:

  Change types:
    Marriage: 70%
    Divorce reversion: 15%
    Court order: 10%
    Other (adoption, etc.): 5%
  
  Required documentation:
    Marriage: Certificate
    Divorce: Decree with name provision
    Court order: Order document
    SSA change: SS-5 or confirmation
  
  Common failures:
    Documentation not linked: 40%
    Prior name docs flagged: 30%
    AKA not correlated: 20%
    Timeline not considered: 10%
```

**Key Statistics**
From Name Change Processing (2025-2026):
- Applications with name changes: 15-20%
- Name changes not properly documented: 5-8%
- Prior name documents flagged incorrectly: 25-30%
- Manual review for name change: 10-15%

**Contributing Factors**
- Name change documents not identified
- Timeline not considered in matching
- AKA names not utilized
- No name change event detection
- Prior documents not back-correlated
- Marriage/divorce not flagged as name change

---

## Mitigation Strategies

### Prevention
1. **Document classification**: Identify name change documents
2. **Timeline building**: Construct name history
3. **AKA correlation**: Use credit report AKAs
4. **Prior document linking**: Connect prior name docs
5. **Event detection**: Flag marriage/divorce as name changes
6. **Name history tracking**: Maintain borrower name timeline

### Implementation
```python
class NameChangeTracker:
    """Track and validate name changes across documents"""
    
    NAME_CHANGE_DOCUMENTS = [
        "marriage_certificate",
        "divorce_decree",
        "court_order_name_change",
        "ssa_name_change",
        "passport_with_prior_name",
        "drivers_license_with_prior_name"
    ]
    
    def build_name_timeline(self, documents: list) -> dict:
        """Build borrower's name timeline from documents"""
        
        timeline = {
            "names": [],
            "change_events": [],
            "current_name": None,
            "prior_names": []
        }
        
        # Extract names with dates from all documents
        name_occurrences = []
        
        for doc in documents:
            name = doc.get("borrower_name")
            date = doc.get("document_date")
            doc_type = doc.get("type")
            
            if name and date:
                name_occurrences.append({
                    "name": self.normalize_name(name),
                    "date": date,
                    "document": doc_type
                })
        
        # Sort by date
        name_occurrences.sort(key=lambda x: x["date"])
        
        # Identify name changes
        current_name = None
        for occurrence in name_occurrences:
            if current_name is None:
                current_name = occurrence["name"]
            elif occurrence["name"] != current_name:
                # Name changed
                timeline["change_events"].append({
                    "from": current_name,
                    "to": occurrence["name"],
                    "approximate_date": occurrence["date"],
                    "detected_in": occurrence["document"]
                })
                timeline["prior_names"].append(current_name)
                current_name = occurrence["name"]
        
        timeline["current_name"] = current_name
        timeline["names"] = list(set(
            [n["name"] for n in name_occurrences]
        ))
        
        return timeline
    
    def validate_name_changes(self, 
                              timeline: dict,
                              documents: list) -> dict:
        """Validate name changes have supporting documentation"""
        
        validation_results = []
        
        for change in timeline["change_events"]:
            # Look for supporting documentation
            support_doc = self.find_name_change_document(
                documents,
                change["from"],
                change["to"],
                change["approximate_date"]
            )
            
            if support_doc:
                validation_results.append({
                    "change": change,
                    "documented": True,
                    "document": support_doc["type"],
                    "status": "verified"
                })
            else:
                validation_results.append({
                    "change": change,
                    "documented": False,
                    "document": None,
                    "status": "requires_documentation",
                    "action": "Request name change documentation"
                })
        
        all_documented = all(r["documented"] for r in validation_results)
        
        return {
            "all_changes_documented": all_documented,
            "results": validation_results,
            "risk_score": 0.0 if all_documented else 0.3
        }
    
    def find_name_change_document(self,
                                  documents: list,
                                  name_from: str,
                                  name_to: str,
                                  change_date: date) -> dict:
        """Find document supporting name change"""
        
        for doc in documents:
            doc_type = doc.get("type", "").lower()
            
            # Check if it's a name change document type
            if not any(nc in doc_type for nc in self.NAME_CHANGE_DOCUMENTS):
                continue
            
            # Check date proximity
            doc_date = doc.get("document_date")
            if doc_date:
                days_diff = abs((doc_date - change_date).days)
                if days_diff > 365:  # Within 1 year
                    continue
            
            # Check names mentioned
            doc_names = doc.get("names_mentioned", [])
            from_found = any(
                self.names_match(name_from, n) for n in doc_names
            )
            to_found = any(
                self.names_match(name_to, n) for n in doc_names
            )
            
            if from_found and to_found:
                return doc
        
        return None
    
    def correlate_credit_akas(self, 
                              timeline: dict,
                              credit_report: dict) -> dict:
        """Correlate timeline with credit report AKAs"""
        
        akas = credit_report.get("aka_names", [])
        
        correlations = []
        unmatched_akas = []
        
        for aka in akas:
            normalized_aka = self.normalize_name(aka)
            
            # Check if AKA is in timeline
            found = False
            for name in timeline["names"]:
                if self.names_match(normalized_aka, name):
                    correlations.append({
                        "aka": aka,
                        "matched_to": name,
                        "status": "correlated"
                    })
                    found = True
                    break
            
            if not found:
                unmatched_akas.append(aka)
        
        return {
            "correlations": correlations,
            "unmatched_akas": unmatched_akas,
            "risk_score": len(unmatched_akas) * 0.15,
            "action": "Investigate unmatched AKAs" if unmatched_akas else None
        }
```

### Risk Scoring for Name Changes

| Scenario | Risk Score | Action |
|----------|------------|--------|
| Name change with documentation | 0.0 | Proceed |
| Name change without documentation | 0.3 | Request documents |
| Unexplained AKA on credit | 0.2 | Investigate |
| Multiple unexplained name changes | 0.4 | Enhanced review |
| Name change timeline inconsistent | 0.35 | Manual review |

---

## References

- [SSA Name Changes](https://www.ssa.gov/myaccount/name-change.html)
- [State Court Name Changes](https://www.nolo.com/legal-encyclopedia/name-change)
- [CFPB Identity Verification](https://www.consumerfinance.gov/)
