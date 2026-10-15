# Mortgage Document Verification Agent: Business Goals, Failure Definitions, and Test List

An agent that reads a loan file, extracts the data, checks documents against each other, flags problems, and routes exceptions to an underwriter. It does not approve loans.

> **Read this first.** These are design starting points to adapt with your own business owners, not benchmarks or advice. No target numbers are given because none can be set without your baseline. Parts of this agent touch law or regulated practice (flags: L, E); get legal or expert review before use.

## Scope (a starting point)

**The agent does:**
- Extract income, assets, identity, and property data
- Compare data across documents
- Flag missing, inconsistent, or suspect documents for a human

**The agent does not:**
- Approve or deny a loan
- Make fair-lending or compliance determinations alone
- Alter source documents

## Business goals

| # | Goal | Success means | Owner |
|---|---|---|---|
| G1 | Extract the data accurately | Extracted values match the documents, and uncertain values are marked. | Head of loan operations |
| G2 | Find inconsistencies across documents | Conflicts in income, employment, names, and dates across documents are found and shown. | Underwriting manager |
| G3 | Detect altered or fraudulent documents and route them to people | Suspect documents and identities are flagged for human review, with the evidence. | Head of fraud and underwriting |
| G4 | Meet compliance requirements and keep an audit trail | Required disclosures, timing, and fair-lending checks are tracked, and every decision step is recorded. | Compliance officer |

## Goal definitions

For every goal: how to measure it, how to find your baseline, what counts as a failure and how severe it is, and when the agent hands over to a person. Baseline method for all goals: Take a sample of conversations or cases the way a person handled them over a period you choose (one vendor's guidance uses 90 days as an example) and compute the same measure. A statement like "it takes too long" is not a baseline.

### G1. Extract the data accurately

| Field | Definition |
|---|---|
| How to measure | Field-level accuracy on a labelled sample by document type, and the share of low-confidence values routed for review. |
| A failure is | Income miscalculated, bank-statement lines misread, names and SSNs mismatched. |
| Severity | Critical: a wrong income or liability figure that changes the decision. High: wrong identity data. Medium: formatting errors. |
| Hand over to a person when | Confidence below the set bar; conflicting values. |

**Failures to test for this goal (from the library):**
- [Income Calculation Errors](../../by-use-case/mortgage-documents/goals/data-extraction/failures/income-calculation-errors.md): OCR Incorrectly Extracts or Calculates Borrower Income from Documents
- [Bank Statement Misreads](../../by-use-case/mortgage-documents/goals/data-extraction/failures/bank-statement-misreads.md): OCR System Incorrectly Extracts Data from Bank Statements
- [Name and SSN Mismatch Detection Failures](../../by-use-case/mortgage-documents/goals/data-extraction/failures/name-ssn-mismatches.md): OCR System Fails to Detect Inconsistent Names or SSNs Across Documents
- [W-2 Form Extraction Failures](../../by-use-case/mortgage-documents/goals/data-extraction/failures/w2-form-extraction.md): OCR System Incorrectly Extracts Data from W-2 Forms

### G2. Find inconsistencies across documents

| Field | Definition |
|---|---|
| How to measure | Seeded-error detection rate on test files; conflicts found by underwriters that the agent missed. |
| A failure is | Co-borrower data mixed, timelines that conflict, income that does not triangulate. |
| Severity | High: a material conflict missed. Medium: a minor mismatch missed. |
| Hand over to a person when | Any unresolved conflict. |

**Failures to test for this goal (from the library):**
- [Income Triangulation Failures](../../by-use-case/mortgage-documents/goals/cross-document-validation/failures/income-triangulation-failures.md): AI System Fails to Reconcile Income Across Multiple Document Sources
- [Employment Timeline Conflicts](../../by-use-case/mortgage-documents/goals/cross-document-validation/failures/employment-timeline-conflicts.md): AI System Fails to Detect Inconsistent Employment Dates Across Documents
- [Co-Borrower Data Mixing](../../by-use-case/mortgage-documents/goals/cross-document-validation/failures/co-borrower-data-mixing.md): AI System Incorrectly Attributes Data Between Borrower and Co-Borrower
- [Name Variation Mishandling](../../by-use-case/mortgage-documents/goals/cross-document-validation/failures/name-variation-mishandling.md): AI System Incorrectly Flags or Misses Legitimate Name Variations Across Documents

### G3. Detect altered or fraudulent documents and route them to people

| Field | Definition |
|---|---|
| How to measure | Detection rate on seeded forgeries; false-flag rate; time to human review. |
| A failure is | AI-generated forgeries, synthetic identities, or deepfaked callers pass. |
| Severity | Critical: a forged document accepted. High: a false flag that delays an honest borrower. |
| Hand over to a person when | Any suspected forgery or identity concern. |

**Failures to test for this goal (from the library):**
- [Fraudulent Document Detection Failures](../../by-use-case/mortgage-documents/goals/document-verification/failures/fraudulent-document-detection.md): OCR System Fails to Detect Altered, Forged, or Fabricated Mortgage Documents
- [Document Authenticity Marker Failures](../../by-use-case/mortgage-documents/goals/document-verification/failures/document-authenticity-markers.md): OCR System Fails to Validate Document Authenticity Markers
- [AI-Generated Document Forgery Detection Failures](../../by-use-case/mortgage-documents/goals/fraud-detection/failures/ai-generated-forgery.md): AI Fraud Detection Fails to Identify Documents Created with Generative AI Tools
- [Synthetic Identity Detection Failures](../../by-use-case/mortgage-documents/goals/fraud-detection/failures/synthetic-identity-detection.md): AI System Fails to Detect Synthetic Identities Combining Real and Fabricated Data
- [Deepfake Impersonation Detection Failures](../../by-use-case/mortgage-documents/goals/fraud-detection/failures/deepfake-impersonation.md): AI System Fails to Detect Video/Voice Deepfakes in Remote Closings

### G4. Meet compliance requirements and keep an audit trail

| Field | Definition |
|---|---|
| How to measure | Compliance exceptions found in audit; steps with no record. |
| A failure is | Missing disclosures, timing violations, and fair-lending red flags not surfaced. |
| Severity | Critical: a compliance breach. High: a missing disclosure. |
| Hand over to a person when | Any compliance flag goes to compliance staff. |

**Failures to test for this goal (from the library):**
- [Fair Lending Red Flag Detection Failures](../../by-use-case/mortgage-documents/goals/compliance-validation/failures/fair-lending-red-flags.md): OCR System Fails to Detect Fair Lending Compliance Concerns
- [TRID Timing Violations](../../by-use-case/mortgage-documents/goals/compliance-validation/failures/trid-timing-violations.md): OCR System Fails to Detect or Flag TRID Disclosure Timing Violations
- [Disclosure Document Gaps](../../by-use-case/mortgage-documents/goals/compliance-validation/failures/disclosure-document-gaps.md): OCR System Fails to Detect Missing or Incomplete Required Disclosures
- [QM/ATR Validation Failures](../../by-use-case/mortgage-documents/goals/compliance-validation/failures/qm-atr-validation.md): OCR System Fails to Validate Qualified Mortgage and Ability-to-Repay Compliance

## Operations concerns for this agent

| Area | Why it matters here | Patterns |
|---|---|---|
| [Input Output Handling](../../cross-cutting/operations/goals/input-output-handling/) | Scans, photos, and mixed formats are the input | 22 |
| [Tool Reliability](../../cross-cutting/operations/goals/tool-reliability/) | Extraction and lookup tools must report failure | 19 |
| [State Consistency](../../cross-cutting/operations/goals/state-consistency/) | Values must stay consistent as files change | 8 |
| [Traceability](../../cross-cutting/operations/goals/traceability/) | Every step is auditable | 8 |
| [Human Oversight Reliability](../../cross-cutting/operations/goals/human-oversight-reliability/) | Exceptions go to underwriters | 8 |
| [Fault Tolerance](../../cross-cutting/operations/goals/fault-tolerance/) | Batch files fail partway | 20 |
| [Version Management](../../cross-cutting/operations/goals/version-management/) | Document and form versions change | 22 |

## Security and governance to check

- [Data Loss Prevention](../../cross-cutting/security/goals/data-loss-prevention/) (security)
- [Tool Authorization Limits](../../cross-cutting/security/goals/tool-authorization-limits/) (security)
- [Governance](../../cross-cutting/governance/goals/governance/) (governance)
- [Verification](../../cross-cutting/accuracy/goals/verification/) (accuracy)

## Decisions your business owner must make

- The confidence bar below which a human reviews
- Which findings must always go to compliance
- How long source documents and extracted data are retained
- Which loan types and states are in scope

## Related

- [All agents by business goal](../)
