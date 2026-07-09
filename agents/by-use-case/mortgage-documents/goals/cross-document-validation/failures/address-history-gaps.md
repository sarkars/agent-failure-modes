# Address History Gaps

## Issue: AI System Fails to Trace Address Consistency Across Document Timeline

**Frequency**: Occasional

**Symptoms**
- Application address doesn't match current documents
- 2-year address history incomplete
- Address transitions not documented
- Mail forwarding patterns not detected
- Subject property address variations
- Prior addresses on credit report not explained

**Root Cause**
Mortgage applications require 2-year address history. Documents from different time periods should show consistent addresses for those periods. AI systems must correlate addresses across application, credit report, pay stubs, bank statements, and tax returns, flagging unexplained gaps or inconsistencies.

**Example**
```
Scenario 1: Current address mismatch

Application (submitted March 2025):
- Current address: 123 Oak Street, Chicago, IL
- Since: January 2023

Recent documents:
- Pay stub (Feb 2025): 456 Elm Ave, Chicago, IL ← DIFFERENT
- Bank statement (Feb 2025): 789 Pine Rd, Chicago, IL ← DIFFERENT
- W-2 (2024): 456 Elm Ave, Chicago, IL

Analysis:
- Three different addresses in recent documents
- Application says Oak Street since 2023
- Pay stub and W-2 show Elm Ave
- Bank statement shows Pine Rd

← Address history unclear
← Which is actually current?
← May indicate recent undisclosed move

---

Scenario 2: 2-year history gap

Application address history:
- Jan 2023 - Present: 123 Oak Street, Chicago
- Jul 2020 - Dec 2022: 456 Elm Ave, Chicago

Credit report addresses:
- 123 Oak Street, Chicago
- 456 Elm Ave, Chicago
- 100 Main St, Springfield (2022) ← NOT ON APPLICATION

Gap analysis:
- Application shows direct move Elm → Oak
- Credit report shows intermediate address
- Springfield address not disclosed
- Gap: Jan 2022 - Jun 2022?

← Undisclosed address
← 6-month gap in history

---

Scenario 3: Subject property address variations

Property being purchased: 555 Maple Lane, Unit 4B

Documents show:
- Purchase contract: 555 Maple Lane #4B
- Appraisal: 555 Maple Lane, Apt 4B
- Title: 555 Maple Ln, Unit 4-B
- Insurance: 555 Maple Lane 4B

AI processing:
- Flagged 4 different addresses
- Actually same property
- Unit number formatting varies

← False positive from formatting
← Should normalize address

---

Scenario 4: Mail forwarding pattern (fraud indicator)

Submitted documents:
- Application address: 123 Oak St, Chicago
- All documents mailed to: PO Box 999, Chicago

Investigation:
- Pay stubs show: PO Box 999
- Bank statements show: PO Box 999
- No documents at Oak Street

Red flags:
- Never received mail at "current" address?
- PO Box could be mail drop
- May not actually reside at Oak St

← Mail forwarding pattern
← May indicate address fraud

---

Address validation requirements:

  Period         | Documents to Check
  ---------------|---------------------
  Current        | Pay stubs, bank statements, utility bill
  Past 2 years   | Prior W-2s, tax returns, credit report
  Subject prop   | Contract, appraisal, title, insurance
  
  Common variations (normalize):
  - Street/St/St./Str
  - Avenue/Ave/Av
  - Apartment/Apt/Unit/#
  - Suite/Ste/Ste.
  - Direction (N/North, S/South)
  
  Red flags:
  - Current address with no recent mail
  - Undisclosed addresses on credit
  - Frequent moves (>3 in 2 years)
  - PO Box as primary address
```

**Key Statistics**
From Address Verification (2025-2026):
- Applications with address gaps: 8-12%
- Undisclosed prior addresses: 5-7%
- Address formatting variations: 30-40%
- Mail forwarding patterns: 2-3%
- Address fraud indicators: 1-2%

**Contributing Factors**
- Address normalization not applied
- Credit report addresses not compared
- Timeline not constructed
- Formatting variations cause false positives
- Mail pattern analysis missing
- Subject property variations flagged incorrectly

---

## Mitigation Strategies

### Prevention
1. **Deterministic Address Normalization Pipeline**: Apply a USPS Publication 28-based standardization pass (street-type and unit-type abbreviation tables, punctuation/whitespace normalization) to every extracted address before any comparison runs, eliminating the formatting-variation false positives seen in Scenario 3 (555 Maple Lane #4B vs. Apt 4B vs. Unit 4-B all normalize to the same canonical string).
2. **Multi-Source Timeline Construction Before Flagging**: Require the system to ingest application, credit report, and document-extracted addresses into a single unified chronological timeline first, then run gap/consistency checks against that timeline — rather than doing ad hoc pairwise document comparisons that miss intermediate addresses like the undisclosed Springfield entry in Scenario 2.
3. **Fuzzy Match with Confidence Threshold for Unit/Format Variants**: Use a component-overlap fuzzy matcher (e.g., 80%+ token overlap) specifically scoped to subject-property and unit-number variants, so legitimate formatting differences across contract/appraisal/title/insurance documents are reconciled instead of raised as four separate "different" addresses.

### Detection & Response
1. **Gap Threshold Scanner**: Automatically flag any unexplained period exceeding 30 days within the regulatory 2-year address-history window, and auto-generate a structured explanation request routed to the loan officer rather than silently accepting an incomplete timeline.
2. **Undisclosed Address Cross-Reference**: Diff the normalized, fuzzy-matched set of application addresses against credit-bureau-reported addresses; any credit report address with no matching application entry is flagged as undisclosed and routed for residence verification before underwriting proceeds.
3. **Mail Forwarding / PO Box Pattern Detector**: Correlate residence-tagged vs. mailing-tagged address fields across all document types; when mailing addresses are consistently disjoint from any claimed residence address and resolve to a PO Box, raise a fraud-review flag rather than treating it as a benign formatting mismatch.

### Architecture Patterns
1. **Address Normalization Microservice**: A shared service (USPS-standard abbreviation tables plus structured address parsing) that every downstream address comparison in the underwriting pipeline calls through a single API, so normalization logic and edge-case fixes live in one place instead of being reimplemented per document type.
2. **Timeline Reconciliation Engine**: Ingests tagged `AddressRecord` objects (source, date range, residence-vs-mailing flag) from application, documents, and credit report, and exposes a single underwriting API returning the unified timeline plus computed gap list — decoupling gap detection from any individual document parser.
3. **Fraud Signal Aggregator**: Combines the address risk score (gaps, undisclosed addresses, mail forwarding) with other document-validation risk scores (income consistency, identity verification) into a composite underwriting risk profile, so address anomalies are weighed alongside other fraud indicators rather than triggering isolated, uncontextualized flags.

### Metrics
1. **address_gap_detection_rate_percent**: Target: > 95% of true gaps caught in eval set; Alert threshold: < 90%
2. **false_positive_formatting_flag_rate_percent**: Target: < 5%; Alert threshold: > 15%
3. **undisclosed_address_catch_rate_percent**: Target: > 90% against known-fraud eval cases; Alert threshold: < 80%
4. **mail_forwarding_flag_precision_percent**: Target: > 85% (flags that survive manual fraud review); Alert threshold: < 60%

### Alerts
1. **Mail Forwarding / PO Box Fraud Pattern Detected** (P1 - Critical): Condition - all mailing addresses across submitted documents resolve to a PO Box disjoint from any claimed residence address. Action: Route to fraud investigation team, hold underwriting decision pending manual residence verification.
2. **Undisclosed Credit Report Address** (P2 - Warning): Condition - credit bureau reports an address not present (after fuzzy matching) on the application. Action: Request borrower explanation, verify residence, do not auto-approve until resolved.
3. **2-Year History Gap Unexplained** (P2 - Warning): Condition - gap > 30 days detected within the required 2-year window with no explanation on file. Action: Generate explanation request to loan officer, hold file in pending-documentation status.
4. **Formatting False-Positive Rate Spike** (P3 - Info): Condition - false_positive_formatting_flag_rate exceeds 15% over a rolling week of reviewed files. Action: Review and extend the normalization abbreviation tables and fuzzy-match threshold.

---

## References

- [USPS Address Standards](https://pe.usps.com/cpim/ftp/pubs/Pub28/pub28.pdf)
- [Fannie Mae Occupancy Requirements](https://selling-guide.fanniemae.com/)
- [FCRA Address Reporting](https://www.ftc.gov/legal-library/browse/statutes/fair-credit-reporting-act)
