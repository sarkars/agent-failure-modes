# What Are the Most Common Supplier Onboarding Failures in AI Agents?

**Supplier-onboarding agents extract certification fields from uploaded documents and treat extraction success as equivalent to verification against the issuing authority's own records, apply the wrong certification checklist to a new supplier because embedding similarity matches boilerplate language instead of category-specific distinguishing clauses, fail to trace sub-tier sourcing and detect counterfeit components because onboarding stops at business-legitimacy verification, and drop beneficial-ownership discrepancies (owner mismatch across documents) that exist in free-text cross-document-review notes but not in structured checklist fields.** These patterns cluster around three categories: certification verification gaps (extraction treated as verification, wrong templates), handoff schema brittleness (beneficial-ownership findings lost), and scope gaps (authenticity and sub-tier sourcing not included in business-legitimacy checks). Onboarding failures introduce counterfeit, fraudulent, or high-risk suppliers into the sourcing network, with potential product liability, compliance, or supply-continuity impact.

## Key Takeaways

- 4 distinct failure patterns affect supplier onboarding, grouped into three mechanisms: certification verification gaps (extraction vs. verification, template mismatch), beneficial-ownership handoff loss, and scope gaps (authenticity verification separate from legitimacy).
- Certification-extraction-as-verification failures occur at "occasional" frequency, with periodic registrar audits finding 5-15% of approved certifications not actually issued or already revoked.
- Template-category mismatches affect 5-10% of onboarded suppliers when policies are template-derived with distinguishing clauses representing a small fraction of embedding space, concentrating on suppliers in adjacent categories.
- Beneficial-ownership discrepancies that are flagged in free-text cross-document-review notes but not captured in structured handoff fields allow suppliers with unresolved ownership anomalies to be approved, discovered only during later compliance audits or sanctions re-screening.

## Scope

- **Certification Verification Gaps** — [certification-extraction-treated-as-verification-in-supplier-onboarding](failures/certification-extraction-treated-as-verification-in-supplier-onboarding.md), [embedding-retrieval-matches-new-supplier-to-wrong-certification-template](failures/embedding-retrieval-matches-new-supplier-to-wrong-certification-template.md). Extracting a well-formed certificate number from an uploaded document is not equivalent to verifying the certificate against the issuing authority; category-specific certification templates are mismatched when selected via description-text similarity instead of registered product-category code.
- **Authenticity & Counterfeit Verification Gaps** — [counterfeit-supplier-verification-gap](failures/counterfeit-supplier-verification-gap.md). Onboarding agents verify business legitimacy (registration, tax ID, references) but do not separately verify component authenticity or sub-tier sourcing, leaving counterfeit-component and gray-market risks undetected.
- **Beneficial-Ownership Handoff Loss** — [multi-agent-handoff-drops-beneficial-ownership-discrepancy-before-onboarding-approval](failures/multi-agent-handoff-drops-beneficial-ownership-discrepancy-before-onboarding-approval.md). Document-review agent flags beneficial-owner mismatch across submitted documents in free-text notes; structured handoff checklist has no field for cross-document discrepancies, so approval stage sees no flag.

## When Supplier Onboarding Matters

- Onboarding is the gate to sourcing: a supplier approved here enters the purchasing network with access to production capacity, often with advance commitments and partial payment terms.
- Counterfeit, gray-market, or fraudulently-registered suppliers introduce product liability (component failures), legal risk (sanctions violations for beneficial-owner mismatch), and supply-continuity risk (supplier later discovered ineligible and relationship terminated mid-fulfillment).
- Certification verification and beneficial-ownership verification are compliance-critical for regulated industries (aerospace, defense, medical devices, food) and sanctioned-entity screening.

## Cross-Pattern Insight

All four supplier-onboarding patterns share a vulnerability to conflation of necessary but different tasks: extracting information from a document is not the same as verifying the information against a source-of-truth system; checking that a supplier is a registered business is not the same as checking that the supplier is authorized to sell the specific components being sourced; matching a supplier to a certification template via topical similarity is not the same as confirming they meet the category-specific requirements. When onboarding agents optimize for efficiency (accepting extracted data, using templates to streamline compliance), they implicitly delegate verification to downstream audits or incident response. Mitigation is architectural: every certification must be independently verified against issuing-authority records before approval; category-specific verification requirements must be enforced via deterministic-lookup rules, not template matching; authenticity and sub-tier sourcing must be explicit verification steps separate from business-legitimacy checks; cross-document findings must be represented in mandatory structured fields that block approval until resolved.

## Frequently Asked Questions

### What's the difference between certification extraction and certification verification?

Extraction is document-understanding: reading a certificate number and expiry date from a PDF or image and confirming it is well-formed. Verification is querying the issuing authority's own database to confirm the certificate exists, is current, and has not been revoked. A well-formatted fabricated certificate passes extraction; it fails verification. Require issuing-authority verification before approval is granted.

### How do onboarding agents confuse business legitimacy with component authenticity?

Business-legitimacy verification (registration, tax ID, references, financial health) establishes that a supplier is a real, legal business capable of fulfilling a contract. Component-authenticity verification (sub-tier sourcing disclosure, certificate-of-authenticity validation against issuing authority, pricing alignment with supply-chain norms) establishes that the specific goods being sourced are genuine and traceable. A legitimate business can be the source of counterfeit goods; a fraudulent business would fail legitimacy checks. Onboarding agents must run both verification streams independently.

### How do template-category mismatches occur?

Certification checklists across adjacent categories (food-contact packaging vs. general industrial packaging) share extensive common boilerplate with only category-determining clauses differing. When template selection is done via embedding similarity over supplier self-description (a supplier describes themselves as a "packaging manufacturer"), the similar boilerplate dominates the embedding space and the category-determining clauses (migration testing, food-contact certification) become a small, low-weight fraction of the match signal. Result: wrong template is selected. Fix: require category selection to be deterministic, based on registered product-category code, not description similarity.

### How do you prevent beneficial-ownership mismatches from slipping through?

Add a mandatory cross-document-discrepancy field to the onboarding checklist. Require the document-review agent to populate it whenever reviewing multiple identity or ownership documents (corporate registration, bank verification, beneficial-ownership registry). Require onboarding-approval logic to check for any populated discrepancy field and place the supplier in a hold state until resolved, rather than allowing approval to proceed.

### What signals indicate that below-market pricing is a counterfeit indicator rather than a procurement win?

Pricing 30%+ below market for a component category is a red flag for either counterfeit sourcing or unsustainable business practices. It should trigger enhanced authenticity verification, not be treated as a win. Combine pricing-threshold alerts with sub-tier sourcing disclosure requirements and independent authenticity verification before approval.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Certification Extraction Treated as Verification in Supplier Onboarding](failures/certification-extraction-treated-as-verification-in-supplier-onboarding.md) | Document extraction confirms certificate number is well-formed; issuing-authority verification not called; fabricated or expired certificates approved |
| [Embedding Retrieval Matches New Supplier to Wrong Certification Template](failures/embedding-retrieval-matches-new-supplier-to-wrong-certification-template.md) | Template selection by description-text similarity matches boilerplate language; category-determining clauses missed; wrong checklist applied |
| [Counterfeit Supplier Verification Gap](failures/counterfeit-supplier-verification-gap.md) | Onboarding verifies business legitimacy (registration, tax ID) but not component authenticity or sub-tier sourcing; counterfeit or gray-market components not detected |
| [Multi-Agent Handoff Drops Beneficial-Ownership Discrepancy Before Onboarding Approval](failures/multi-agent-handoff-drops-beneficial-ownership-discrepancy-before-onboarding-approval.md) | Document-review agent flags beneficial-owner mismatch in free text; structured handoff has no cross-document-discrepancy field; approval ignores the flag |

**Total: 4 patterns**

## Related Goals

- [Supplier Risk](../supplier-risk/) — downstream from onboarding; suppliers approved with onboarding gaps (authentic-component verification, beneficial-ownership verification) introduce ongoing risk that risk-monitoring may not detect until materialized.
