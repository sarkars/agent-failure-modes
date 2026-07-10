# Unverified Clearance Opinion Filed Without Checking Cited Clause Against Source Agreement

## Issue: An IP-Clearance Agent Asked to Confirm a Company Holds Sufficient Rights to Use a Third-Party Asset (a Licensed Image, a Vendor-Supplied Code Library, a Co-Developed Patent Disclosure) Generates a Clearance Opinion That Quotes a Specific License Clause as Granting the Needed Right, Then Autonomously Files or Releases That Opinion to the Requesting Team Without Re-Reading the Actual Source License Text It Just Cited to Confirm the Quoted Clause Says What the Opinion Claims It Says

**Frequency**: Occasional

**Symptoms**
- Clearance opinion confidently states "Section 4.2 of the License Agreement grants worldwide, perpetual sublicensing rights" but Section 4.2 of the actual source document grants a narrower, non-sublicensable, field-of-use-restricted right
- The opinion's quoted clause language is close to but not an exact match for the source document's actual text -- a paraphrase that drifted toward the broader right the requesting team was hoping for
- Downstream teams (product, marketing, engineering) proceed to use the asset in a manner consistent with the opinion's claimed scope, not the source license's actual scope, before anyone re-reads the underlying agreement
- The discrepancy surfaces only when the licensor's counsy or an external audit re-reads the actual clause and flags that the company's use exceeds the granted rights
- Re-running the same clearance request with an explicit instruction to quote the source clause verbatim and diff it against the opinion's paraphrase reliably surfaces the mismatch, showing the agent had access to the correct text and simply did not check its own output against it before releasing the opinion

**Root Cause**
The agent treats opinion drafting and verification as a single pass: it generates the clearance opinion's characterization of a clause from its working understanding of the license, and the same generation step that produces the paraphrase also produces the opinion's confidence and the act of releasing it, with no independent verification step that re-reads the actual source clause text and checks the opinion's claim against it before the opinion is treated as actionable. Because the model's paraphrase of a clause is fluent and internally consistent with the rest of its own opinion, there is no internal signal that distinguishes a verified quote from a confident misremembering of the clause's actual scope.

**Example**
```
Engineering team asks the IP-clearance agent to confirm rights to sublicense a third-party code library bundled into a customer-facing product
Agent retrieves the vendor license agreement and produces an opinion: "Section 4.2 grants the Company a worldwide, perpetual, sublicensable license to incorporate the Library into Company products and distribute to end customers"
Opinion is filed directly to engineering's rights-clearance tracker as "Cleared -- sublicensing confirmed," unblocking the release
Six weeks later, the vendor's legal team flags that Section 4.2 actually grants a non-sublicensable, internal-use-only license; sublicensing requires a separate addendum that was never executed
Re-reading Section 4.2 against the opinion's quoted text shows the opinion's "sublicensable" characterization does not appear anywhere in the actual clause -- the agent generated it as a plausible extension of the surrounding license language rather than a verified reading of that specific term
Product is already shipped to customers with the unlicensed sublicense scope; remediation requires emergency relicensing negotiation under disadvantageous terms
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM agents asserting task completion (here, "clearance confirmed") frequently do so without verifying the actual state of the artifact they are claiming about, relying on surface-level confidence cues rather than a check against ground truth | [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/html/2606.09863) |
| LLM-based agents are documented to produce fabricated or drifted characterizations of source content that read as plausible and internally consistent, making self-generated paraphrases unreliable as a substitute for re-checking the original text | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Execution-provenance research for LLM agents argues that traceable evidence linking a generated claim to the exact source span it is based on is necessary because models do not reliably self-report when a claim has drifted from its cited source | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- No structural separation between the generation step that drafts the opinion's characterization of a clause and a distinct verification step that re-reads the actual clause text before the opinion is releasable
- The opinion's prose quotes the clause in a way that looks like a direct citation, giving downstream readers false confidence that the text was checked verbatim
- Autonomous filing/release of the opinion to a tracker that downstream teams treat as authoritative removes the natural human checkpoint where someone might otherwise re-read the source agreement before acting
- Time pressure from the requesting team to get a fast "cleared" answer discourages a slower, independent verification pass

---

## Mitigation Strategies

### Prevention

1. **Mandatory two-phase verification: generation + independent re-check**: Restructure clearance workflow: (a) Phase 1 (Generation): Agent drafts opinion with clause characterizations and paraphrases, (b) Phase 2 (Verification): Before filing, separate verification pass (human or independent model prompt) re-reads source document WITHOUT seeing Phase 1 opinion, (c) Verification pass extracts verbatim clause text and generates independent characterization, (d) Auto-diff: compare Phase 1 characterization against verbatim source text, flag any drift, (e) If drift detected, block filing and escalate to human legal review. Root cause: Separates draft from verification so mischaracterizations are caught before release.

2. **Verbatim-quote extraction and inline-diff enforcement**: Within opinion text, enforce structure: for any claim about a license right, require inline citation format: "{Claim} [Source: {Section}, Clause: {quoted verbatim text from source}]". On filing, automated extraction: (a) parse all claims and their quoted source texts, (b) cross-check each quoted text against actual source document, (c) if any quote does not appear verbatim in source (e.g., quote is paraphrase or inaccurate), highlight as "UNVERIFIED CLAIM" and flag for correction, (d) only allow filing if all claims are verified or explicitly labeled "Unverified - requires manual review." Root cause: Prevents paraphrases from masquerading as direct quotes.

3. **Confidence-scoring and claim-grading with evidence tracing**: Opinion structured with three claim categories: (a) Verified-Direct-Quote: clause text matches source verbatim, confidence 100%, (b) Characterized-From-Source: characterization of clause but not verbatim, requires verification before use, confidence 50-90%, (c) Inferred-or-Extrapolated: claim not directly stated in source, requires manual review, confidence <50%. Opinion output shows: "{Claim} [Grade: Verified-Direct-Quote / Characterized / Inferred] [Confidence: X%]". High-stakes clearances require all claims be Verified-Direct-Quote grade; Characterized/Inferred claims require human sign-off before filing.

### Detection & Response

1. **Verification gate with verbatim-diff audit logging**: For each clearance opinion about to be filed, log: {opinion_id, source_doc_id, claims_count, verified_direct_quote_count, characterized_count, inferred_count, verification_gate_pass (Y/N), verification_timestamp, verified_by (human/model)}. Run daily audit: sample 20% of filed opinions from past 24h, re-read source documents, verify all Verified-Direct-Quote claims actually appear verbatim in source. Alert if: >5% have quote mismatches, or >10% filed without verification gate.

2. **Post-filing source-verification audit with downstream usage tracking**: On discovery of a characterization-mismatch post-filing, trigger: (a) audit trail: when did teams rely on this opinion? What actions taken in reliance? (b) downstream impact assessment: is product already shipped, distributed, licensed? (c) remediation: if impact minimal, correct opinion + notify teams; if impact material, escalate to legal for licensor notification + remedial licensing. Log all instances in trend-analysis dashboard.

### Architecture Patterns

1. **Two-Phase Verification Engine**: Phase 1 (Generation) → Opinion draft with characterizations. Phase 2 (Verification) → Independent prompt re-reads source with instruction "extract verbatim clause text, provide independent characterization without seeing prior opinion". Diff engine auto-compares Phase 1 vs. Phase 2, flags discrepancies. Verification gate: no filing unless diff passes or human approves override.

2. **Verbatim-Quote Extraction & Enforcement**: Opinion generation enforces inline citation format. On extraction, verify every quoted text against source document via string matching. Build quote index: {source_section, quote_text, claim_number}. Diff report: shows which quotes verified verbatim vs. unverified.

3. **Claim-Grading & Evidence Tracing**: Opinion structured with claim-grade metadata {claim_grade: verified-direct-quote|characterized|inferred, confidence_score, source_section, evidence_span (text range from source)}. High-stakes clearances require evidence_span for all claims, enabling human auditor to immediately locate and re-read source evidence.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Verbatim-Quote Verification Rate | 100% | <99% | # of quoted clauses matching source document verbatim on re-read / total quoted clauses in filed opinions |
| Verified-Direct-Quote Percentage | >95% | <90% | # of claims graded Verified-Direct-Quote / total claims in high-stakes clearance opinions |
| Characterization-Mismatch Detection Rate | >99% | <95% | # of characterization mismatches caught by verification gate before filing / total characterizations in opinions |
| Opinion-File Verification-Gate Pass Rate | 100% | <99% | # of opinions passing verification gate on first attempt / total opinions filed |
| Post-Filing Discrepancy Rate | 0% | >0.5% | # of filed opinions later found to have verbatim-quote or characterization mismatches / total filed opinions |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Verbatim-Quote Mismatch | Quoted clause text does not appear verbatim in source document on re-read | CRITICAL | Block filing; route to independent legal review; correct quote or revise characterization; re-file only after verification |
| Characterization Drift Detected | Verification gate finds opinion's characterization of clause differs materially from independent re-read | CRITICAL | Block filing; escalate to IP counsel for source clause interpretation; re-file with verified characterization |
| Unverified Claim Detected | Opinion filed with claim graded Inferred or Characterized without underlying direct quote | HIGH | Retroactively verify; if mismatch found, notify downstream teams of potential reliance error; may require usage remediation |
| High Post-Filing Discrepancy Rate | >1% of filed opinions later found to have quote/characterization mismatches in monthly audit | HIGH | Audit clearance prompts/templates; investigate verification gate effectiveness; may require human sign-off on all opinions until remediation confirmed |

---

## References

- [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/html/2606.09863)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
