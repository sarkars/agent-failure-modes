# PII Exposure

## Issue: Agent Outputs Contain Personally Identifiable Information

**Frequency**: Very Common

**Symptoms**
- Names, SSNs, addresses in agent responses
- Email addresses, phone numbers exposed
- Health information (PHI) in outputs
- Financial data (account numbers, card numbers) leaked
- "Example" data that's actually real customer data

**Root Cause**
Agents with access to databases, documents, or context containing PII may include this data in responses without recognizing it as sensitive. The model doesn't inherently understand data classification - it treats all text equally. Without explicit output filtering, PII flows through to users, logs, and downstream systems.

**Example**
```
User: "Show me how customer records are formatted"

Agent response:
"Here's a typical customer record format:

Customer ID: 10847293
Name: Sarah Johnson
SSN: 287-65-4921
DOB: 03/15/1985
Address: 4521 Oak Lane, Austin, TX 78701
Phone: (512) 555-0147
Email: sarah.johnson@email.com

As you can see, we store demographic and contact info..."

Problem: Agent used REAL customer data as an "example"
         exposing PII to unauthorized user

Expected: Use synthetic/fake data or describe format abstractly
```

**Key Statistics**
From PII Exposure Research (2026):
- 61% of AI agent incidents involve sensitive data exposure
- PII in LLM outputs: 15-25% of enterprise deployments affected
- Average cost of PII breach: $4.5M (IBM)
- Regulatory fines: GDPR up to 4% of global revenue
- Detection without DLP: <40% of exposures caught

**PII Categories at Risk**
| Category | Examples | Regulation |
|----------|----------|------------|
| Identity | SSN, passport, driver's license | Various |
| Contact | Address, phone, email | GDPR, CCPA |
| Financial | Card numbers, bank accounts | PCI-DSS |
| Health | Medical records, diagnoses | HIPAA |
| Biometric | Fingerprints, face data | BIPA, GDPR |

**Contributing Factors**
- No PII detection on agent outputs
- Training or fine-tuning on real customer data
- RAG retrieving documents with PII
- "Helpful" agent using real examples
- No data classification in context
- Overly broad database access

**Mitigation Strategies**
1. **Output scanning**: Real-time PII detection on all outputs
2. **Synthetic data**: Train agents to use fake examples
3. **Data masking**: Mask PII before it reaches agent context
4. **Access controls**: Limit agent's data access scope
5. **Classification tags**: Mark sensitive data, instruct agent to avoid
6. **Redaction layer**: Automatic redaction before final output

**Detection**
- Regex patterns for SSN, email, phone, card numbers
- Named entity recognition for names, addresses
- ML-based PII classifiers
- Monitor for data that matches customer records
- Alert on output length anomalies (large data dumps)

## References

- [CSA: AI Agent Security Incidents](https://cloudsecurityalliance.org/) - 61% data exposure
- [IBM: Cost of Data Breach 2025](https://www.ibm.com/security/data-breach) - Breach costs
- [Microsoft Presidio](https://github.com/microsoft/presidio) - PII detection tool
- [GDPR Article 83](https://gdpr-info.eu/art-83-gdpr/) - Penalty provisions
