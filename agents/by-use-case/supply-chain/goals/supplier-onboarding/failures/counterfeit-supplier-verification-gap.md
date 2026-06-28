# Counterfeit Supplier Verification Gap

## Issue: Agent Onboarding a New Supplier Verifies Business Registration and Pricing Competitiveness but Does Not Verify Component Authenticity or Sub-Tier Sourcing Chain

**Frequency**: Occasional (Low frequency, high severity)

**Symptoms**
- New supplier passes business legitimacy checks (registration documents, tax ID, business address verification) and is onboarded, but the agent does not separately verify that components it sells are sourced from authorized/authentic supply chains
- Pricing significantly below market average is treated as a positive procurement signal rather than a counterfeit-risk indicator requiring additional scrutiny
- Sub-tier sourcing (where the new supplier itself sources from) is not traced; the agent's diligence stops at the immediate counterparty
- Certificates of authenticity or compliance documents submitted by the supplier are accepted without independent verification against the issuing authority

**Root Cause**
Supplier onboarding agents are commonly optimized to verify that a counterparty is a legitimate, registered business entity capable of fulfilling a contract — a necessary but separate question from whether the specific components that entity sells are authentic and traceable to an authorized source. Counterfeit and gray-market component risk lives specifically in the sub-tier sourcing chain and in document authenticity, neither of which is captured by standard business-legitimacy verification, so an onboarding process that stops at "is this a real company" systematically misses this risk category.

**Example**
```
Scenario: New electronics component supplier offers pricing 35% below market average
Onboarding checks: Business registration verified, tax ID valid, references checked — supplier approved
Missing check: Component authenticity verification, sub-tier sourcing trace, certificate-of-authenticity validation against issuing authority
Components received: Counterfeit parts with falsified authenticity certificates
Impact: Counterfeit components enter production; potential product failure, recall, and liability exposure
```

**Key Statistics**
- Counterfeit component infiltration into legitimate supply chains is a persistent and costly risk in electronics and industrial supply chains, with below-market pricing repeatedly identified as a leading indicator in counterfeit-detection research and industry guidance
- Sub-tier sourcing chain opacity (visibility limited to the immediate counterparty) is consistently cited as the primary structural gap enabling counterfeit components to enter legitimate procurement channels
- Independent certificate-of-authenticity verification against the issuing authority, rather than accepting submitted documents at face value, is a standard recommended control in anti-counterfeiting procurement guidance

---

## Mitigation Strategies

1. **Component Authenticity Verification Track, Separate from Business Legitimacy**: Run a distinct authenticity/provenance verification process for the actual goods being sourced, independent of and in addition to standard business-legitimacy checks
2. **Below-Market Pricing as a Risk Flag**: Treat pricing significantly below market average as a trigger for additional scrutiny, not a purely positive procurement signal
3. **Sub-Tier Sourcing Chain Disclosure**: Require new suppliers to disclose their own upstream sourcing for critical components, and verify at least one tier beyond the immediate counterparty for high-risk categories
4. **Independent Document Verification**: Verify certificates of authenticity and compliance documents directly against the issuing authority rather than accepting supplier-submitted copies at face value

### Metrics
- % of new suppliers for high-risk component categories with completed authenticity/provenance verification
- Rate of below-market-pricing suppliers receiving enhanced scrutiny vs. standard onboarding
- Counterfeit component incident rate, tracked from supplier onboarding cohort

### Alerts
- New supplier onboarded for a high-risk component category without authenticity/provenance verification completed → P1
- Submitted certificate of authenticity not independently verified against issuing authority before approval → P1

---

## References

- [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184)
- [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597)
