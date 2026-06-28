# Pediatric Dosing Extrapolation Error

## Issue: Agent Extrapolates Adult Weight-Based or Fixed Dosing Formulas to Pediatric Patients, Producing Unsafe Doses

**Frequency**: Common

**Symptoms**
- Pediatric dose calculated by naively scaling adult dose by body weight ratio, ignoring nonlinear pediatric pharmacokinetics
- Neonatal and infant dosing (which often requires different mg/kg/day schedules than older children) treated identically to general "pediatric" dosing
- Maximum single-dose or daily-dose caps from adult labeling applied incorrectly to children, or pediatric-specific caps missed entirely
- Liquid formulation concentration errors not caught when converting a weight-based dose to a volume to administer

**Root Cause**
Pediatric pharmacokinetics differ nonlinearly from adults due to differences in body composition, organ maturation (renal/hepatic clearance), and developmental stage — a simple linear weight-based scaling of adult dosing is frequently incorrect and can be dangerously high or low depending on the drug. Many models default to generic "mg/kg" scaling learned from training data without applying drug-specific, age-band-specific pediatric dosing references (e.g., neonatal vs. infant vs. adolescent bands), and without flagging the formulation/concentration conversion step where calculation errors are common.

**Example**
```
Scenario: Pediatric agent dosing a renally-cleared antibiotic for a 6-month-old infant
Naive approach: Scale adult dose by weight ratio (e.g., 10kg/70kg * adult dose)
Correct approach: Use infant-specific mg/kg/dose and dosing-interval schedule from a pediatric reference (interval often differs from adult, not just dose magnitude)
Discrepancy: Linear adult-scaling under- or over-doses by a clinically significant margin depending on drug-specific pediatric PK
Impact: Subtherapeutic dosing risks treatment failure; supratherapeutic dosing risks toxicity in an immature renal/hepatic system
```

**Key Statistics**
- Pediatric medication dosing errors, particularly in neonates and infants, are reported at substantially higher rates than adult dosing errors in hospital medication-safety studies
- Weight-based linear extrapolation from adult dosing is a recognized root cause category in pediatric adverse drug event reviews
- Formulation/concentration conversion errors (mg-to-mL calculations) account for a notable share of pediatric dosing incidents independent of the dose-calculation itself

---

## Mitigation Strategies

1. **Pediatric-Specific Dosing References**: Always query a dedicated pediatric dosing reference (age-band-specific mg/kg/dose and interval), never linearly extrapolate from adult dosing
2. **Age-Band Stratification**: Explicitly branch dosing logic by neonate/infant/child/adolescent age bands rather than a single "pediatric" bucket
3. **Independent Concentration-Conversion Check**: Add a separate verification step for mg-to-mL/volume conversion, flagged for pharmacist double-check
4. **Maximum Dose Cap Enforcement**: Encode pediatric-specific (not adult) maximum single and daily dose caps per drug

### Metrics
- % of pediatric dose calculations using age-band-specific reference vs. linear adult extrapolation
- Dosing error rate stratified by age band (neonate/infant/child/adolescent)
- Concentration-conversion error rate

### Alerts
- Pediatric dose calculated via linear adult-weight scaling without age-band reference → P1
- Calculated dose exceeds pediatric-specific maximum for age band → P1

---

## References

- [Large Language Models for Disease Diagnosis: A Scoping Review](https://arxiv.org/abs/2409.00097)
- [Multi-model assurance analysis showing large language models are highly vulnerable to adversarial hallucination attacks during clinical decision support](https://www.nature.com/articles/s43856-025-01021-3)
