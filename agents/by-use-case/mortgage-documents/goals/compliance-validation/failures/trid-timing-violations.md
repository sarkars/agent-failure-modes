# TRID Timing Violations

## Issue: OCR System Fails to Detect or Flag TRID Disclosure Timing Violations

**Frequency**: Occasional but high regulatory risk

**Symptoms**
- Loan Estimate (LE) delivered after 3-day deadline missed
- Closing Disclosure (CD) 3-day waiting period not verified
- Changed circumstances not documented for LE revisions
- Fee tolerance violations undetected
- Consummation date validation failures
- Saturday/Sunday/holiday timing miscalculated

**Root Cause**
TILA-RESPA Integrated Disclosure (TRID) rules require specific timing for Loan Estimates and Closing Disclosures. OCR systems extracting dates from documents may not apply TRID business day calculations, miss tolerance violations, or fail to correlate disclosure timing with application and closing dates. Violations can result in significant regulatory penalties and loan repurchase demands.

**Example**
```
Scenario 1: Loan Estimate timing violation

Application received: Monday, March 3
LE delivered: Friday, March 7

OCR check: 4 days → PASS?

TRID rule: LE must be delivered within 3 BUSINESS days
- Monday (Day 0 - application)
- Tuesday (Day 1)
- Wednesday (Day 2)
- Thursday (Day 3 - deadline)
- Friday (Day 4) → VIOLATION

← OCR counted calendar days
← Should count business days
← Missed a timing violation

---

Scenario 2: Closing Disclosure waiting period

CD delivered: Monday, March 10
Closing scheduled: Wednesday, March 12

OCR check: 2 days → FAIL?

TRID rule: CD must be received 3 BUSINESS days before closing
- Monday: Day 0 (receipt)
- Tuesday: Day 1
- Wednesday: Day 2
- Thursday: Day 3 (earliest closing)

Actual: Wednesday closing with Monday receipt
← Only 2 business days
← VIOLATION - closing must move to Thursday

---

Scenario 3: Revised LE tolerance violation

Original LE (March 3):
- Origination fee: $1,500
- Title insurance: $1,200

Revised LE (March 15):
- Origination fee: $1,650 (+$150)
- Reason: "Rate lock"

CD (March 28):
- Origination fee: $1,650

OCR check: Revision matches CD → PASS?

TRID tolerance rules:
- Origination fee: ZERO tolerance (cannot increase)
- Rate lock is NOT a valid changed circumstance for fees
- $150 increase is a VIOLATION

← OCR didn't check tolerance categories
← Invalid changed circumstance not flagged

---

Scenario 4: Holiday timing calculation

CD mailed: Wednesday, December 23
Closing: Monday, December 28

Calendar count: 5 days → PASS?

Business day analysis:
- Dec 23 (Wed): Mailed
- Dec 24 (Thu): +3 mail days (deemed received Sat Dec 26)
- Dec 25 (Fri): Christmas - NOT a business day
- Dec 26 (Sat): NOT a business day (receipt assumed)
- Dec 27 (Sun): NOT a business day
- Dec 28 (Mon): Day 1
- Dec 29 (Tue): Day 2
- Dec 30 (Wed): Day 3 (earliest closing)

Actual: Closing Dec 28 → VIOLATION

← Holiday not factored
← Mail receipt rule not applied

---

Scenario 5: Changed circumstance validation

Revision issued for: "Borrower requested rate lock"

Required documentation:
- Rate lock request (written or recorded)
- Date/time of request
- Lock confirmation

OCR found: No rate lock request in file

← LE revised without valid changed circumstance
← Potential tolerance violation

---

TRID compliance analysis:
  
  Documents with timing data extracted: 95%
  
  Timing violations detected by OCR: 35%
  Timing violations missed by OCR: 65%
  
  Common missed violations:
    Business day miscalculation: 40%
    Holiday not excluded: 25%
    Mail receipt rule not applied: 20%
    Changed circumstance invalid: 15%
  
  Regulatory impact:
    Violations per 100 loans: 3-5
    Average penalty per violation: $5,000-$25,000
    Repurchase risk: Elevated
```

**Key Statistics**
From Mortgage Compliance Research (2026):
- TRID timing violations: 3-5% of loans
- OCR detection rate: 30-40%
- Business day errors: 40% of misses
- Holiday calculation errors: 25% of misses
- Average penalty: $5,000-$25,000 per violation

**TRID Timing Rules**
| Document | Timing Rule | Business Days |
|----------|------------|---------------|
| Initial LE | Within 3 BD of application | Mon-Sat, excl. holidays |
| Revised LE | Before CD, with valid CC | Mon-Sat, excl. holidays |
| Initial CD | 3 BD before consummation | Mon-Sat, excl. holidays |
| Revised CD | If changes, may reset 3 BD | Depends on change type |
| Mailed disclosure | +3 calendar days for receipt | For mailed docs |

**Contributing Factors**
- Calendar vs. business day confusion
- Holiday exclusion not implemented
- Mail receipt rule not applied
- Changed circumstance validation missing
- Tolerance categories not checked
- Date extraction without context

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Weekend app | Friday app, Monday LE | Day 1 | Day 3+ |
| Holiday | Holiday in period | Exclude | Count as day |
| Mailed CD | Mailed + 3 | Apply rule | Ignore mail |
| Zero tolerance | Fee increased | Flag | Accept |
| Changed circ | No documentation | Flag invalid | Accept |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Timing violation detection | > 90% | Known violations |
| Business day calculation | > 99% | Day count accuracy |
| Tolerance violation detection | > 95% | Fee comparisons |
| Changed circumstance validation | > 90% | Documentation check |

---

## Mitigation Strategies

### Prevention
1. **Business day calculator**: Proper TRID calendar
2. **Holiday database**: Federal + state holidays
3. **Mail receipt rule**: +3 days for mailed disclosures
4. **Tolerance engine**: Zero/10%/unlimited categories
5. **Changed circumstance validator**: Check documentation
6. **Cross-document dating**: Correlate all dates

### Implementation
```python
class TRIDComplianceChecker:
    """Check TRID timing and tolerance compliance"""
    
    FEDERAL_HOLIDAYS = [
        # List of federal holidays
        "2026-01-01",  # New Year's Day
        "2026-01-20",  # MLK Day
        # ... etc
    ]
    
    # Fee tolerance categories
    ZERO_TOLERANCE = [
        "origination_fee",
        "discount_points",
        "transfer_taxes"
    ]
    
    TEN_PERCENT_TOLERANCE = [
        "title_services",
        "required_services_borrower_cannot_shop"
    ]
    
    UNLIMITED_TOLERANCE = [
        "prepaid_interest",
        "property_insurance",
        "services_borrower_can_shop"
    ]
    
    def calculate_business_days(self, 
                                start_date: date, 
                                end_date: date) -> int:
        """Calculate business days between dates (TRID definition)"""
        business_days = 0
        current = start_date + timedelta(days=1)
        
        while current <= end_date:
            # TRID business day: Mon-Sat, excluding federal holidays
            if current.weekday() < 6:  # Not Sunday
                if current.isoformat() not in self.FEDERAL_HOLIDAYS:
                    business_days += 1
            current += timedelta(days=1)
        
        return business_days
    
    def check_le_timing(self, 
                        application_date: date,
                        le_delivery_date: date) -> dict:
        """Check Loan Estimate delivery timing"""
        business_days = self.calculate_business_days(
            application_date, 
            le_delivery_date
        )
        
        compliant = business_days <= 3
        
        return {
            "compliant": compliant,
            "application_date": application_date,
            "le_delivery_date": le_delivery_date,
            "business_days": business_days,
            "deadline": self.add_business_days(application_date, 3),
            "violation": None if compliant else "LE delivered late"
        }
    
    def check_cd_timing(self,
                        cd_delivery_date: date,
                        cd_delivery_method: str,
                        closing_date: date) -> dict:
        """Check Closing Disclosure timing"""
        # If mailed, add 3 calendar days for receipt
        if cd_delivery_method == "mail":
            receipt_date = cd_delivery_date + timedelta(days=3)
        else:
            receipt_date = cd_delivery_date
        
        business_days = self.calculate_business_days(
            receipt_date,
            closing_date
        )
        
        compliant = business_days >= 3
        
        return {
            "compliant": compliant,
            "cd_delivery": cd_delivery_date,
            "delivery_method": cd_delivery_method,
            "deemed_receipt": receipt_date,
            "closing_date": closing_date,
            "business_days_before_closing": business_days,
            "earliest_closing": self.add_business_days(receipt_date, 3),
            "violation": None if compliant else "CD waiting period not met"
        }
    
    def check_fee_tolerance(self,
                            le_fees: dict,
                            cd_fees: dict,
                            changed_circumstances: list) -> dict:
        """Check fee tolerance compliance"""
        violations = []
        
        for fee_name, cd_amount in cd_fees.items():
            le_amount = le_fees.get(fee_name, 0)
            difference = cd_amount - le_amount
            
            if difference <= 0:
                continue  # Decrease is always OK
            
            # Check tolerance category
            if fee_name in self.ZERO_TOLERANCE:
                # Zero tolerance - any increase is violation
                # Unless valid changed circumstance
                if not self.valid_changed_circumstance(
                    fee_name, changed_circumstances
                ):
                    violations.append({
                        "fee": fee_name,
                        "tolerance": "zero",
                        "le_amount": le_amount,
                        "cd_amount": cd_amount,
                        "increase": difference,
                        "violation": True
                    })
            
            elif fee_name in self.TEN_PERCENT_TOLERANCE:
                # 10% cumulative tolerance
                # Checked at category level, not individual fee
                pass  # Handled separately
        
        return {
            "compliant": len(violations) == 0,
            "violations": violations
        }
    
    def validate_changed_circumstance(self,
                                      cc_reason: str,
                                      documentation: list) -> dict:
        """Validate changed circumstance is documented"""
        valid_reasons = [
            "borrower_requested_change",
            "rate_lock",
            "new_information",
            "natural_disaster",
            "title_issue"
        ]
        
        required_docs = {
            "rate_lock": ["rate_lock_request", "lock_confirmation"],
            "borrower_requested_change": ["written_request"],
            "new_information": ["credit_supplement", "appraisal"]
        }
        
        if cc_reason not in valid_reasons:
            return {
                "valid": False,
                "reason": f"Invalid CC reason: {cc_reason}"
            }
        
        # Check documentation
        required = required_docs.get(cc_reason, [])
        found = [d for d in documentation if d in required]
        
        if len(found) < len(required):
            return {
                "valid": False,
                "reason": f"Missing documentation for {cc_reason}",
                "required": required,
                "found": found
            }
        
        return {"valid": True}
```

### Prompt Design
```yaml
instructions: |
  ## TRID COMPLIANCE CHECKING
  
  BUSINESS DAY DEFINITION (TRID):
  - Monday through Saturday
  - EXCLUDING federal holidays
  - Sunday is NEVER a business day
  
  LOAN ESTIMATE TIMING:
  - Must deliver within 3 BUSINESS days of application
  - Application date = Day 0
  - Count forward: Mon-Sat, skip Sun + holidays
  
  CLOSING DISCLOSURE TIMING:
  - Borrower must RECEIVE 3 business days before closing
  - If mailed: Add 3 CALENDAR days for receipt
  - Then count 3 business days from receipt
  
  FEE TOLERANCES:
  - ZERO tolerance (cannot increase without valid CC):
    * Origination charges
    * Points
    * Transfer taxes
  
  - 10% tolerance (cumulative):
    * Title services
    * Required services borrower cannot shop
  
  - Unlimited (can increase any amount):
    * Prepaid interest
    * Insurance premiums
    * Services borrower shopped for
  
  CHANGED CIRCUMSTANCES (must be documented):
  - Borrower requested change
  - New information affecting eligibility
  - Natural disaster
  - Rate lock (requires lock request + confirmation)
  
  FLAG violations, don't auto-correct. Include:
  - Specific rule violated
  - Dates involved
  - Business day calculation
  - Recommended cure
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `trid.violation_detection` | < 80% |
| `trid.business_day_accuracy` | < 99% |
| `trid.tolerance_violations` | > 3% |
| `trid.cc_undocumented` | > 5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Timing Violation Missed | Known violation not flagged | P1 |
| Business Day Error | Calculation wrong | P2 |
| Tolerance Violation | Fee increase undetected | P1 |
| Exam Finding | Regulatory exam issue | P1 |

---

## References

- [CFPB TRID Rule](https://www.consumerfinance.gov/rules-policy/regulations/1026/) - Regulation Z
- [TRID Small Entity Guide](https://files.consumerfinance.gov/f/201503_cfpb_tila-respa-integrated-disclosure-guide-to-forms.pdf) - CFPB guide
- [TRID FAQs](https://www.consumerfinance.gov/rules-policy/regulations/1026/interp-19/) - Interpretations
- [Fannie Mae TRID](https://singlefamily.fanniemae.com/originating-underwriting/compliance/trid) - Investor requirements
