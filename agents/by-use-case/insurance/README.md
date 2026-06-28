# Insurance

Agents processing claims, detecting fraud, underwriting policies, and managing renewals face risks around bias, fraud-legitimacy tradeoff, and actuarial fairness.

## Goals

| Goal | Description | Patterns |
|------|-------------|----------|
| [Claim Processing](goals/claim-processing/) | Adjudication bias, exclusion blindness, coverage validation | 2 |
| [Fraud Detection](goals/fraud-detection/) | False positive impact, fraud-conversion tradeoff, evolving fraud patterns | 1 |
| [Underwriting](goals/underwriting/) | Risk miscalculation, missing features, model decay | 1 |
| [Policy Management](goals/policy-management/) | Renewal rate errors, limit violations, history lag | 1 |

**Status**: 5 of ~30 patterns planned

## Key Challenges

1. **Historical Bias**: Training data reflects past discrimination
2. **Fraud-Conversion Tradeoff**: Aggressive detection blocks legitimate claims
3. **Risk Underestimation**: Model missing key risk factors
4. **Actuarial Fairness**: Renewal rates don't reflect actual risk
5. **Claims History Lag**: Prior claims not visible during adjudication
