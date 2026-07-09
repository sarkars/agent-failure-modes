# Catastrophe Correlation Blindness

## Issue: Catastrophe risk model assumes independent claims; hurricane hits coast, model hadn't provisioned for 10k simultaneous claims; reserve exhausted within days

**Frequency**: Occasional

**Symptoms**
- Model predicts $100M reserve needed based on average annual claims
- Single catastrophic event (hurricane, earthquake, fire) generates $500M in claims
- Reserve depleted; company forced to hold up payments or borrow
- Historical disaster scenarios not captured in model

**Root Cause**
Reserve models assume claims are independent random events. Catastrophes create correlated massive claims (hurricane hits region = 1000s of simultaneous claims). Models trained on normal claim distribution miss tail correlations. CAT models exist but rarely integrated into core reserve calculations.

**Example**
```
Insurer: Coastal homeowners, 1M active policies
Model: Average annual claims = $50M, reserve = $100M
Historical data: 10 years of data, no major hurricanes
Model assumption: Claims are independent Poisson process
2024 reality: Cat 5 hurricane hits coast
Actual claims in September 2024: $450M (900+ simultaneous claims)
Reserve remaining: $100M - $450M = DEFICIT
Company response: Emergency reinsurance, credit line drawdown
Impact: Regulatory capital requirements breached; company facing insolvency
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Catastrophe events vs frequency assumption: 10-100x tail risk | Insurance industry reports |
| Reserves inadequate during disasters: 15-20% of carriers | Post-disaster audits |
| Correlation during catastrophes: Near 1.0 (all claims spike together) | Reinsurance data |

---

## Mitigation Strategies

1. **CAT modeling integration**: Use separate CAT model for reserve calculations
2. **Stress testing**: Model 100-year and 500-year disaster scenarios
3. **Reinsurance layers**: Transfer tail risk above reserve capacity

---

## References

- [Catastrophe Risk Modeling](https://arxiv.org/abs/1512.04567) - Insurance risk research
- [Reserve Adequacy During Disasters](https://www.naic.org/documents/prod_ins_catastro.pdf) - Regulatory guidance
