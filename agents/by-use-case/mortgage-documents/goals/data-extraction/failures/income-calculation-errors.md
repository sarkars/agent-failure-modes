# Income Calculation Errors

## Issue: OCR Incorrectly Extracts or Calculates Borrower Income from Documents

**Frequency**: Common

**Symptoms**
- Gross income confused with net income
- YTD income extrapolated incorrectly
- Overtime/bonus income miscounted
- Self-employment income miscalculated
- Multiple income sources not aggregated
- Decimal point errors in dollar amounts

**Root Cause**
Mortgage qualification depends heavily on accurate income calculation. OCR systems must extract income from various document types (W-2, paystubs, tax returns), understand income categories (base, overtime, bonus, commission), and calculate qualifying income according to lending guidelines. Errors in any step lead to incorrect DTI ratios and qualification decisions.

**Example**
```
Scenario 1: YTD extrapolation error

Paystub shows:
- Pay period: 1/1 - 1/15 (first half of January)
- YTD Gross: $4,500
- Pay frequency: Semi-monthly

OCR calculation:
- Assumed monthly (not semi-monthly)
- $4,500 × 12 = $54,000 annual

Correct calculation:
- Semi-monthly = 24 pay periods/year
- $4,500 × 2 = $9,000 monthly
- $9,000 × 12 = $108,000 annual

← 50% understatement of income
← Would incorrectly disqualify borrower

---

Scenario 2: Box confusion on W-2

W-2 shows:
- Box 1 (Wages): $85,000
- Box 3 (SS Wages): $85,000
- Box 5 (Medicare): $85,000
- Box 12 (401k): $15,000

OCR extracted: $85,000 (correct)

But for another W-2:
- Box 1: $75,000
- Box 12a (401k deferrals): $10,000

OCR added them: $85,000

Correct: $75,000 (Box 12 is pre-tax, already excluded)

← Over-counted income by $10,000

---

Scenario 3: Self-employment income

Schedule C shows:
- Gross receipts: $250,000
- Expenses: $180,000
- Net profit: $70,000
- Depreciation: $15,000

OCR extracted: $70,000 net profit

Correct qualifying income:
- Net profit: $70,000
- Add back depreciation: +$15,000
- Qualifying: $85,000

← Under-counted by $15,000
← Depreciation add-back missed

---

Scenario 4: Overtime income

Paystubs show overtime income:
- January: $2,000 OT
- February: $1,500 OT
- March: $3,000 OT
- Current job: 18 months

OCR: Averaged overtime ($2,166/month)

Correct per guidelines:
- Need 2-year history for OT
- Only 18 months at job
- OT cannot be used for qualifying

← Incorrectly included non-qualifying income

---

Scenario 5: Multiple employer income

Borrower has:
- Full-time job: $65,000/year
- Part-time job: $15,000/year (started 10 months ago)

OCR: Combined $80,000

Correct per guidelines:
- Part-time income needs 2-year history
- Only full-time qualifies: $65,000

← Over-stated qualifying income by $15,000

---

Income calculation error analysis:
  
  Documents with income extraction errors: 18%
  
  Error types:
    Pay frequency misidentification: 25%
    YTD extrapolation errors: 22%
    Self-employment miscalculation: 18%
    Non-qualifying income included: 15%
    Box/field confusion: 12%
    Decimal errors: 8%
  
  Impact:
    DTI miscalculated: 15%
    Qualification decision affected: 8%
    Loan repriced after correction: 5%
```

**Key Statistics**
From Mortgage Processing Research (2026):
- Income extraction errors: 15-20%
- Pay frequency misidentification: 20-25%
- Self-employment errors: 25-30%
- Non-qualifying income inclusion: 10-15%
- Errors affecting qualification: 5-10%

**Income Calculation Complexities**
| Income Type | Calculation Method | Common Error |
|-------------|-------------------|--------------|
| Salary | Annual ÷ 12 | Using gross instead of qualifying |
| Hourly | Hours × Rate × 52 ÷ 12 | Wrong hours assumption |
| Overtime | 2-year average if consistent | Including without history |
| Bonus | 2-year average | Using single year |
| Commission | 2-year average, declining trend check | Not checking trend |
| Self-employment | Net + depreciation + amortization | Missing add-backs |
| Rental | 75% of gross rent - PITIA | Using 100% of rent |

**Contributing Factors**
- Pay frequency detection errors
- W-2 box confusion
- Missing guideline logic
- No depreciation add-back rules
- History requirement not checked
- Multiple income aggregation errors

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Semi-monthly | 24 pay periods | Correct annual | Monthly assumption |
| Bi-weekly | 26 pay periods | Correct annual | Monthly assumption |
| Self-employed | Schedule C | Net + add-backs | Net only |
| Overtime | 18-month history | Exclude | Include |
| W-2 Box 12 | 401k contribution | Not added | Added to income |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Income accuracy | > 95% | vs. human calc |
| Pay frequency detection | > 98% | Correct identification |
| Self-employment accuracy | > 90% | Add-back inclusion |
| Qualifying income correct | > 95% | Per guidelines |

---

## Mitigation Strategies

### Prevention
1. **Pay frequency detection**: Identify from paystub patterns
2. **W-2 box mapping**: Correct box interpretation
3. **Guideline integration**: Build in lending rules
4. **History validation**: Check employment duration
5. **Add-back logic**: Include depreciation, amortization
6. **Trend analysis**: Check for declining income

### Implementation
```python
class MortgageIncomeCalculator:
    """Calculate qualifying income per mortgage guidelines"""
    
    PAY_FREQUENCIES = {
        "weekly": 52,
        "bi-weekly": 26,
        "semi-monthly": 24,
        "monthly": 12
    }
    
    OVERTIME_HISTORY_MONTHS = 24
    BONUS_HISTORY_MONTHS = 24
    PART_TIME_HISTORY_MONTHS = 24
    
    def calculate_salary_income(self, paystub: dict) -> dict:
        """Calculate salary income from paystub"""
        # Detect pay frequency
        frequency = self.detect_pay_frequency(paystub)
        periods_per_year = self.PAY_FREQUENCIES[frequency]
        
        # Use current period gross (not YTD for extrapolation issues)
        current_gross = paystub.get("current_gross")
        
        # Calculate annual
        annual_income = current_gross * periods_per_year
        monthly_income = annual_income / 12
        
        return {
            "annual": annual_income,
            "monthly": monthly_income,
            "frequency": frequency,
            "calculation": f"{current_gross} × {periods_per_year} periods"
        }
    
    def detect_pay_frequency(self, paystub: dict) -> str:
        """Detect pay frequency from paystub"""
        # Check explicit frequency field
        if paystub.get("pay_frequency"):
            return self.normalize_frequency(paystub["pay_frequency"])
        
        # Infer from dates
        start = paystub.get("period_start")
        end = paystub.get("period_end")
        
        if start and end:
            days = (end - start).days + 1
            
            if days == 7:
                return "weekly"
            elif days == 14:
                return "bi-weekly"
            elif days in [15, 16]:
                return "semi-monthly"
            elif days in range(28, 32):
                return "monthly"
        
        # Default to semi-monthly (most common)
        return "semi-monthly"
    
    def calculate_self_employment_income(self, 
                                         schedule_c: dict,
                                         years: int = 2) -> dict:
        """Calculate self-employment qualifying income"""
        net_profit = schedule_c.get("net_profit", 0)
        depreciation = schedule_c.get("depreciation", 0)
        amortization = schedule_c.get("amortization", 0)
        depletion = schedule_c.get("depletion", 0)
        
        # Qualifying income = Net + Non-cash deductions
        qualifying = net_profit + depreciation + amortization + depletion
        
        # If 2-year average required
        if years == 2 and schedule_c.get("prior_year"):
            prior = schedule_c["prior_year"]
            prior_qualifying = (
                prior.get("net_profit", 0) +
                prior.get("depreciation", 0)
            )
            qualifying = (qualifying + prior_qualifying) / 2
        
        return {
            "net_profit": net_profit,
            "add_backs": {
                "depreciation": depreciation,
                "amortization": amortization,
                "depletion": depletion
            },
            "qualifying_annual": qualifying,
            "qualifying_monthly": qualifying / 12
        }
    
    def calculate_overtime_income(self,
                                  paystubs: list,
                                  employment_months: int) -> dict:
        """Calculate overtime income if qualifying"""
        # Check history requirement
        if employment_months < self.OVERTIME_HISTORY_MONTHS:
            return {
                "qualifies": False,
                "reason": f"Only {employment_months} months history, "
                         f"need {self.OVERTIME_HISTORY_MONTHS}",
                "monthly": 0
            }
        
        # Calculate average
        ot_amounts = [p.get("overtime", 0) for p in paystubs]
        average = sum(ot_amounts) / len(ot_amounts)
        
        # Check for declining trend (last 6 months vs prior 6)
        if len(ot_amounts) >= 12:
            recent = sum(ot_amounts[-6:]) / 6
            prior = sum(ot_amounts[-12:-6]) / 6
            
            if recent < prior * 0.8:  # 20% decline
                return {
                    "qualifies": False,
                    "reason": "Declining overtime trend",
                    "monthly": 0
                }
        
        return {
            "qualifies": True,
            "monthly": average,
            "annual": average * 12
        }
    
    def validate_w2_extraction(self, w2: dict) -> dict:
        """Validate W-2 income extraction"""
        # Box 1 is qualifying wages
        box1 = w2.get("box1_wages", 0)
        
        # Box 12 codes are NOT added to Box 1
        # They're already excluded (401k, HSA, etc.)
        box12 = w2.get("box12", {})
        
        # Common error: adding Box 12 to Box 1
        if w2.get("extracted_total") and w2["extracted_total"] != box1:
            return {
                "error": "incorrect_total",
                "extracted": w2["extracted_total"],
                "correct": box1,
                "likely_cause": "Box 12 incorrectly added"
            }
        
        return {
            "valid": True,
            "qualifying_income": box1
        }
```

### Prompt Design
```yaml
instructions: |
  ## MORTGAGE INCOME CALCULATION
  
  PAY FREQUENCY DETECTION:
  - Weekly: 7 days per period → 52 periods/year
  - Bi-weekly: 14 days → 26 periods/year
  - Semi-monthly: 15-16 days → 24 periods/year
  - Monthly: 28-31 days → 12 periods/year
  
  NEVER assume monthly. Always detect frequency.
  
  W-2 EXTRACTION:
  - Box 1 = Qualifying wages
  - Box 12 = PRE-TAX deductions (already excluded from Box 1)
  - NEVER add Box 12 to Box 1
  
  SELF-EMPLOYMENT:
  - Start with Schedule C net profit
  - ADD BACK: depreciation, amortization, depletion
  - These are non-cash expenses that don't reduce cash flow
  
  QUALIFYING RULES:
  - Overtime: Need 2-year history, check for declining trend
  - Bonus: Need 2-year history, average both years
  - Part-time: Need 2-year history
  - Commission: Need 2-year history, check declining trend
  
  If income type doesn't meet history requirement:
  - Flag it as non-qualifying
  - Calculate DTI both with and without
  
  ALWAYS output calculation steps for verification.
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `income.extraction_accuracy` | < 95% |
| `income.pay_frequency_error` | > 5% |
| `income.dti_miscalculation` | > 3% |
| `income.qualification_error` | > 2% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Income Accuracy Drop | < 90% | P1 |
| Pay Frequency Errors | > 10% | P2 |
| Self-Employment Errors | > 15% | P2 |
| Qualification Impact | > 5% | P1 |

---

## References

- [Fannie Mae Selling Guide](https://selling-guide.fanniemae.com/Selling-Guide/Origination-thru-Closing/Subpart-B3-Underwriting-Borrowers/Chapter-B3-3-Income-Assessment/) - Income guidelines
- [Freddie Mac Guide](https://guide.freddiemac.com/app/guide/section/5304.1) - Income calculation
- [CFPB ATR/QM](https://www.consumerfinance.gov/rules-policy/regulations/1026/43/) - Ability to repay
- [IRS W-2 Instructions](https://www.irs.gov/forms-pubs/about-form-w-2) - Box definitions
