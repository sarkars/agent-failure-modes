# IP Assignment Gap in Contractor Agreements

## Issue: Agent Reviewing a Contractor or Consultant Agreement Confirms "IP Assignment Clause Present" Without Verifying It Actually Covers the Work Product Category at Issue

**Frequency**: Common

**Symptoms**
- Agent flags an agreement as having IP assignment language but does not check whether the assignment language covers pre-existing IP, jointly developed IP, and IP created using the contractor's own tools/background IP separately
- "Work made for hire" language is present but the agreement is with an independent contractor in a jurisdiction/context where work-for-hire doctrine does not automatically apply to the relevant category of work, leaving title with the contractor absent an explicit assignment
- Moral rights waiver (relevant in jurisdictions where moral rights are non-waivable by work-for-hire alone) is omitted, leaving residual rights with the creator
- Open-source or third-party component usage by the contractor is not addressed, so IP assignment may not actually transfer clean title if third-party-licensed code is embedded

**Root Cause**
IP assignment adequacy depends on matching the specific assignment mechanism (work-for-hire doctrine, present assignment of future rights, or both) to the specific category of work product and the specific jurisdiction's treatment of contractor-created IP — work-for-hire doctrine, where it exists, typically applies automatically only to a narrow statutory list of work categories and does not reliably apply to independent contractors by default the way it does to employees. A presence check for assignment-sounding language does not verify this mechanism-to-work-category-to-jurisdiction match, so a contract can read as IP-protective while leaving a real title gap.

**Example**
```
Scenario: Software development agreement with an independent contractor (not an employee)
Agreement language: "All work product shall be deemed work made for hire"
Jurisdiction: Work-for-hire doctrine for contractors applies only to a specific statutory list of commissioned work categories; custom software is not reliably on that list
Missing: No present-assignment clause as a fallback for work outside the work-for-hire categories
Impact: Title to the custom software work product may remain with the contractor, not the hiring company, despite the work-for-hire language
```

**Key Statistics**
- Work-for-hire doctrine misapplication to independent contractors (as opposed to employees) is a frequently cited drafting error in IP and technology transaction practice
- A meaningful share of contractor agreements rely on work-for-hire language alone without a present-assignment fallback clause, which is the recommended best practice specifically because work-for-hire doctrine has narrow statutory scope for contractors
- Legal-AI clause review research notes that compound IP assignment adequacy (mechanism + work category + jurisdiction) is a multi-factor determination that single-clause presence detection systematically under-evaluates

---

## Mitigation Strategies

1. **Mechanism-Category-Jurisdiction Matching**: Require the agent to explicitly check whether the work-for-hire categories applicable in the relevant jurisdiction cover the actual type of work being performed, not just whether work-for-hire language exists
2. **Present-Assignment Fallback Check**: Flag any contractor agreement relying on work-for-hire language alone, without a present-assignment-of-rights fallback clause, as incomplete
3. **Background IP and Third-Party Component Disclosure**: Require explicit disclosure and carve-out language for contractor background IP and any third-party/open-source components incorporated into deliverables
4. **Moral Rights Waiver Check**: In jurisdictions with non-waivable-by-assignment-alone moral rights, verify an explicit moral rights waiver is present where legally permissible

### Metrics
- % of contractor agreements with both work-for-hire and present-assignment fallback language verified
- Rate of work-category-to-doctrine mismatches caught in QA sampling
- Background IP / third-party component disclosure completeness rate

### Alerts
- Contractor agreement relies on work-for-hire language alone with no present-assignment fallback → P1
- Work product category falls outside the jurisdiction's work-for-hire statutory list with no fallback assignment → P1

---

## References

- [Large Language Models Meet Legal Artificial Intelligence: A Survey](https://arxiv.org/pdf/2509.09969)
- [Exploring the Nexus of Large Language Models and Legal Systems: A Short Survey](https://arxiv.org/pdf/2404.00990)
