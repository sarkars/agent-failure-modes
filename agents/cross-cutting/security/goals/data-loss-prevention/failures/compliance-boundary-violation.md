# Compliance Boundary Violation

## Issue: Agent Outputs Violate Regulatory Data Handling Requirements

**Frequency**: Common

**Symptoms**
- PHI shared outside HIPAA-covered systems
- EU citizen data transferred outside EU (GDPR)
- Payment card data mishandled (PCI-DSS)
- Data retained beyond legal limits
- Minor's data processed without consent

**Root Cause**
Regulatory compliance requires data to stay within specific boundaries - geographic, systemic, and temporal. Agents often cross these boundaries unknowingly: sending HIPAA data to non-BAA vendors, transferring EU data to US-hosted LLMs, or retaining data beyond deletion requirements. The agent doesn't understand compliance constraints unless explicitly programmed.

**Example**
```
HIPAA violation:

Healthcare agent with US-hosted LLM:
User: "Summarize this patient's condition"
Context: [Patient records with PHI]

Agent: [Sends PHI to OpenAI API - no BAA in place]
Agent: "The patient presents with Stage 2 hypertension..."

Problem: PHI sent to vendor without Business Associate 
         Agreement - HIPAA violation
         Potential fine: $50,000+ per violation

---

GDPR violation:

EU customer support agent:
User (EU citizen): "Look up my account history"

Agent: [Retrieves data from EU database]
Agent: [Sends to US-based LLM for processing]
Agent: [LLM provider logs the data]

Problem: EU personal data transferred to US without 
         adequate safeguards (Schrems II)
         Potential fine: Up to 4% of global revenue

---

PCI-DSS violation:

Agent: "Your card ending in 7890 was charged $500"
Log: {"prompt": "...", "card": "4532-1234-5678-7890"}

Problem: Full card number logged
         PCI-DSS requires no storage of full PAN
```

**Key Statistics**
From Compliance Research (2026):
- GDPR fines for AI: $50M+ in 2025
- HIPAA AI violations: Rising 40% year-over-year
- PCI non-compliance: 80% of orgs fail first audit
- Cross-border data issues: Top concern for global deployments
- Compliance in AI: Only 35% have formal programs

**Compliance Frameworks**
| Regulation | Scope | Key Requirements |
|------------|-------|------------------|
| GDPR | EU personal data | Data minimization, consent, transfer rules |
| HIPAA | US health data | BAA required, access controls, audit |
| PCI-DSS | Payment cards | No PAN storage, encryption, access |
| CCPA/CPRA | California consumers | Disclosure, deletion rights |
| SOC 2 | Service organizations | Security controls, monitoring |

**Contributing Factors**
- LLM providers without compliance certifications
- No data residency controls
- Unaware of cross-border transfer
- Logging capturing regulated data
- Third-party tools without compliance
- No compliance layer in agent architecture

**Mitigation Strategies**
1. **Data classification**: Tag data with compliance requirements
2. **Residency controls**: Keep data in required geography
3. **Vendor compliance**: Only use compliant LLM providers
4. **Consent management**: Track and enforce consent
5. **Retention enforcement**: Auto-delete per requirements
6. **Audit logging**: Compliance-ready audit trails

**Detection**
- Map data flows against compliance boundaries
- Monitor cross-border transfers
- Audit LLM provider compliance
- Track data retention vs. requirements
- Alert on regulated data in non-compliant systems

## References

- [GDPR Official Text](https://gdpr-info.eu/) - EU regulation
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
- [PCI-DSS v4.0](https://www.pcisecuritystandards.org/) - Payment card security
- [IAPP: AI and Privacy](https://iapp.org/resources/article/ai-governance/) - Compliance guidance
