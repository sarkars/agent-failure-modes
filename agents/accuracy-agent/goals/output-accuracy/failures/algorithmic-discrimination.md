# Algorithmic Discrimination

## Issue: AI System Systematically Discriminates Against Protected Groups

**Frequency**: Common

**Symptoms**
- Protected groups disproportionately rejected/scored lower
- Historical bias patterns replicated at scale
- "Black box" decisions without explainability
- High reversal rates on appeals
- Disparate impact statistics in outcomes

**Root Cause**
AI systems trained on historical data inherit and amplify societal biases, making discriminatory decisions at massive scale. Unlike individual bias, algorithmic discrimination affects thousands or millions of decisions automatically, with no human review catching the pattern.

**Example**
```
Case: SafeRent Tenant Screening (2024)

System: AI-powered "tenant score" for landlord decisions

What happened:
- Algorithm systematically discriminated against Black and 
  Hispanic renters
- Low-income housing voucher holders disproportionately rejected
- Mary Louis: steady rent history + government voucher guarantee
  → Still received failing score → automatic rejection

Investigation findings:
- Opaque algorithm unfairly weighted credit history
- Ignored voucher income guarantees
- Disparately impacted protected classes

Outcome:
- $2.2 million class-action settlement
- Must stop offering "accept/decline" scores for voucher holders
- Future scoring models require independent fairness audits

Result: First-of-its-kind enforcement showing AI bias
        violates anti-discrimination laws
```

**Key Statistics**
From Digital Defynd AI Disasters Analysis (2026):
- SafeRent: $2.2M settlement for housing discrimination
- Workday: Nationwide class action for age discrimination in hiring
- Amazon: Scrapped recruiting tool that penalized "women's" terms
- Cigna PxDx: 300,000 claims denied with 1.2-second "reviews"
- UHC nH Predict: 90%+ appeal reversal rate suggesting systematic errors

**Discrimination Patterns**
| Domain | AI System | Bias Pattern |
|--------|-----------|--------------|
| Housing | Tenant screening | Racial, income-based discrimination |
| Hiring | Resume screening | Gender, age, disability bias |
| Insurance | Claims processing | Systematic denial of legitimate claims |
| Lending | Credit scoring | Redlining patterns replicated |
| Criminal Justice | Risk assessment | Racial disparities in scoring |

**Contributing Factors**
- Training data reflects historical discrimination
- Proxy variables correlate with protected characteristics
- No fairness testing before deployment
- "Black box" models without explainability
- Scale amplifies individual biases to systematic patterns

**Mitigation Strategies**
1. **Bias audits**: Regular independent testing for disparate impact
2. **Fairness constraints**: Build fairness metrics into model training
3. **Explainability requirements**: Understand why decisions are made
4. **Human review**: Maintain human oversight for high-stakes decisions
5. **Appeal processes**: Track reversal rates as bias indicators

**Detection**
- Statistical analysis of outcomes by protected group
- High appeal/reversal rates
- Disparate impact testing
- User complaints and lawsuits
- Regulatory investigations

## References

- [Digital Defynd: Top 40 AI Disasters](https://digitaldefynd.com/IQ/top-ai-disasters/) - SafeRent (#10), Workday (#11), Amazon (#22), Cigna (#38), UHC (#39)
- [AI Incident Database](https://incidentdatabase.ai/) - Algorithmic discrimination incidents
- [EEOC AI Guidance](https://www.eeoc.gov/laws/guidance/americans-disabilities-act-and-use-software-algorithms-and-artificial-intelligence) - AI and employment discrimination
