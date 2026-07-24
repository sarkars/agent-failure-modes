# Certification Extraction Treated as Verification in Supplier Onboarding

## Issue: An Onboarding Agent Successfully Extracts a Certification Number, Issuing Body, and Expiry Date From a Supplier's Uploaded Document and Approves the Supplier as Certified, Without Calling the Available Issuing-Authority Lookup Tool to Confirm the Certificate Is Real, Unrevoked, and Current

**Frequency**: Occasional

**Symptoms**
- Agent's approval record cites the certification as "verified" based solely on having extracted a well-formed certificate number, issuing body name, and expiry date from the uploaded document image or PDF
- Execution trace shows document-extraction tool calls but no corresponding call to the issuing-authority verification API (e.g., an ISO registrar lookup, an insurance-carrier confirmation endpoint) for that specific certificate number
- Suppliers submitting documents with well-formatted but non-existent or expired certificate numbers are approved at a similar rate to suppliers with genuinely valid, current certifications, because document formatting quality (not authenticity) is what the extraction step actually assesses
- A subsequent audit that runs the same extracted certificate numbers against the issuing authority's actual database finds a nontrivial share return "not found" or "revoked," despite having passed onboarding as "certification verified"
- The agent's confidence language in its approval summary ("certification confirmed") does not distinguish between "I successfully read a certificate number off this document" and "I confirmed this certificate number is valid with the issuing body"

**Root Cause**
The onboarding agent's certification-check step is implemented as a document-understanding task: extract the relevant fields from the uploaded file and confirm they are present and well-formed. This is a different computation from certificate validity verification, which requires an independent query to the issuing authority's own record. Because the extraction step succeeds whenever the document is legible and internally consistent — which a fabricated or expired certificate can be just as easily as a genuine one — the agent's downstream approval logic, which treats "fields extracted successfully" as equivalent to "certification confirmed," approves suppliers whose certificates were never actually checked against source-of-truth issuer records, even when an issuing-authority lookup tool is available in the agent's tool set.

**Example**
```
New supplier uploads a PDF titled "ISO 9001:2015 Certificate of Registration" listing
certificate number "ISO-9001-88214-B", issuing body "Global Quality Registrar", expiry "2027-03"
Extraction step: Successfully parses certificate number, issuing body name, and expiry date
  from the document text
Agent's approval summary: "Supplier certification verified: ISO 9001:2015, valid through
  2027-03." Supplier approved and added to the sourcing pool.
Tool available but not called: verify_certificate(issuing_body="Global Quality Registrar",
  cert_number="ISO-9001-88214-B") -- would have returned "no matching record found," since the
  certificate number does not exist in the registrar's actual database
Discovered: 4 months later, during a customer-mandated supplier audit, when the registrar
  confirms no such certificate was ever issued
```

**Key Statistics**
| Finding | Context |
|---|---|
| Agentic document-fraud-detection frameworks for KYC-style pipelines are built specifically because OCR/extraction success on a submitted document is not evidence of the document's authenticity, and production systems require a distinct policy-driven verification layer against issuing/source records rather than relying on extraction quality alone | Agentic AI Microservice Framework for Deepfake and Document Fraud Detection in KYC Pipelines (arXiv:2601.06241) |
| Surveys of identity-document fraud note that generative and easily-templated forgeries can reproduce well-formatted, internally-consistent document fields, meaning document-level plausibility checks alone are an increasingly weak signal of authenticity | From Forgeries to Foundation Models: A Systematic Survey of Identity Document Attack and Detection (arXiv:2607.01442) |
| In supplier-onboarding audits, certificate numbers that pass document-extraction checks but are never cross-checked against the issuing authority's own database typically show a measurable non-zero "not found or revoked" rate when checked after the fact | Illustrative range from procurement-compliance audit practice |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Well-formatted fabricated certificate | Document with a plausible, well-formatted but non-existent certificate number | Agent calls issuing-authority lookup, finds no match, declines approval or escalates | Supplier approved with "certification verified" and no lookup call in trace |
| Genuinely valid certificate | Document with a real certificate number the issuing authority's database confirms | Agent calls lookup tool, confirms match, approves | Approval granted without a logged verification call, even though it happened to be valid |
| Expired certificate, well-formatted | Document shows an expiry date in the past but otherwise well-formatted | Agent flags as expired, requires renewal before approval | Agent approves based on extracted (past) expiry date without checking current status via lookup |
| Issuing-authority tool returns ambiguous match | Lookup returns multiple certificates with similar numbers | Agent surfaces ambiguity for human resolution rather than auto-approving on best guess | Agent silently picks a match and approves |

### Evaluation Dataset
- **Source**: Synthetic and real (anonymized) supplier certification documents paired with ground-truth issuing-authority verification results (valid, invalid, expired, not found)
- **Size**: 200+ document/verification-outcome pairs across at least 3 certification types (ISO, insurance, trade compliance)
- **Key variations**: well-formatted fabricated vs. genuinely valid vs. expired; issuing authority lookup returns clean match vs. no match vs. ambiguous match

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Verification-call coverage | 100% of certification approvals preceded by a logged issuing-authority lookup call | % of approvals with a prior verification-tool call for the same certificate number |
| Fabricated-certificate approval rate | 0% | % of test-set fabricated certificates that result in approval |
| Audit-confirmed certification rate | > 99% | % of production-approved certifications independently confirmed valid on post-hoc registrar audit |

### Automated Checks
```python
def check_unverified_certification(trace: list[dict]) -> dict:
    """Flag a certification approval with no preceding issuing-authority lookup call."""
    approvals = [c for c in trace if c["tool"] == "approve_supplier_certification"]
    verified_cert_numbers = {
        c["args"].get("cert_number")
        for c in trace
        if c["tool"] == "verify_certificate"
    }
    flagged = [
        c for c in approvals
        if c["args"].get("cert_number") not in verified_cert_numbers
    ]
    return {
        "unverified_approval_count": len(flagged),
        "flagged_certificates": [c["args"].get("cert_number") for c in flagged],
        "risk": "extraction_treated_as_verification" if flagged else None,
    }
```

---

## Mitigation Strategies

### Prevention
1. **Mandatory Issuing-Authority Lookup Gate**: Require a successful `verify_certificate` call against the issuing authority's own record before the supplier-approval tool is reachable, so document extraction alone can never satisfy the certification requirement
2. **Provenance-Distinct Approval Language**: Require the agent's approval summary to explicitly distinguish "document received and fields extracted" from "certificate confirmed valid by issuing authority," preventing extraction success from being narratively conflated with verification
3. **Category-Specific Verification Requirements**: For each certification type accepted (ISO, insurance, trade compliance), hard-code the specific required issuing-authority endpoint rather than relying on the agent to infer that verification is needed and which tool applies

### Detection & Response
1. **Verification-Call-Absence Scanning**: Scan onboarding traces for certification-approval actions with no preceding issuing-authority lookup call for the matching certificate number
2. **Periodic Registrar Reconciliation**: Batch-check previously "verified" certificates against the issuing authority's current database on a recurring schedule, catching both extraction-only approvals and certificates that were valid at approval time but have since been revoked

### Architecture Patterns
- **Extract-Then-Verify Pipeline**: Structurally separate document-field extraction from issuing-authority verification into sequential, independently-logged stages, with the approval action only reachable from a code path holding a verified result
- **Confidence-Tagged Certification Record**: Store each certification with an explicit status field (`extracted_only`, `verified`, `verification_failed`) rather than a single boolean, making the extraction-only state visible and queryable rather than collapsed into "certified"

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| `onboarding.unverified_certification.count` | Certification approvals with no issuing-authority lookup call | > 0 per week |
| `onboarding.registrar_audit_mismatch.rate` | % of previously-approved certifications failing a post-hoc registrar recheck | > 1% |
| `onboarding.verification_call.coverage` | % of certification approvals with a logged verification call | < 100% |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Unverified Certification Approved | Supplier certification approved with no logged issuing-authority lookup call | P1 | Suspend supplier's certified status pending verification; audit affected certification category |
| Registrar Reconciliation Mismatch | Post-hoc audit finds an approved certificate is not found or revoked at the issuing authority | P1 | Immediately flag supplier for compliance review; halt new POs pending resolution |

---

## References
- [Agentic AI Microservice Framework for Deepfake and Document Fraud Detection in KYC Pipelines](https://arxiv.org/abs/2601.06241)
- [From Forgeries to Foundation Models: A Systematic Survey of Identity Document Attack and Detection](https://arxiv.org/abs/2607.01442)
