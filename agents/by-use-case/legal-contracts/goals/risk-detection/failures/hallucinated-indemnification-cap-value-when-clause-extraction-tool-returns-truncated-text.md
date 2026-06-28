# Hallucinated Indemnification-Cap Value When Clause-Extraction Tool Returns Truncated Text

## Issue: A Risk-Detection Agent Extracting the Numeric Indemnification Cap From a Contract Clause Via a Document-Parsing Tool That Returns Truncated or Malformed Text for That Specific Clause -- Due to a Page-Break Artifact or OCR Error in the Source Document -- Completes the Extraction With a Plausible Numeric Value Rather Than Flagging the Extraction as Incomplete

**Frequency**: Occasional

**Symptoms**
- The risk-detection summary reports a specific dollar figure as the contract's indemnification cap, but the underlying clause-extraction tool's logged output for that clause is truncated mid-sentence or contains OCR-garbled characters where the cap figure should appear
- The reported cap value is plausible -- a round number consistent with typical caps for similar contract types -- but does not match the actual figure printed in the source document when manually reviewed
- Re-running the document-parsing tool with corrected page-break handling or against a cleaner source scan returns a different cap figure than what the agent originally reported
- The mismatch concentrates on clauses spanning a page break or appearing in scanned (rather than native-text) contract documents, where extraction artifacts are most common
- The risk-detection summary presents the cap figure with full confidence and no indication that the source extraction was incomplete or degraded

**Root Cause**
When the document-parsing tool returns truncated or garbled text for the specific span containing the cap figure, the risk-detection task still requires a numeric value to complete its summary, and the agent has no instruction distinguishing "extraction incomplete for this clause" from "extraction succeeded and the cap is unusually structured." Lacking that distinction, the model completes the missing or garbled portion with a plausible numeric value consistent with the surrounding clause language and typical industry caps, rather than escalating the incomplete extraction to a human reviewer.

**Example**
```
Indemnification clause spans a page break in a scanned contract document; the clause-extraction tool's OCR output for the page-break region reads "...liability under this Section shall not exceed $[illegible]00,000 in the aggregate..."
Risk-detection agent's extraction step completes the garbled figure as "$2,000,000," a plausible round number consistent with the clause's surrounding language
Manual review of the original scanned document shows the actual printed figure is "$500,000," a materially different and lower cap than what the agent reported
Risk summary delivered to the deal team materially overstates the counterparty's actual indemnification exposure cap, affecting the negotiation position taken based on the summary
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to complete plausible-sounding values when an expected tool or extraction output is missing or incomplete, rather than treating the gap as a blocking error | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Frameworks for detecting and correcting tool-use errors in agentic systems identify failure to recognize truncated or malformed tool output as a distinct, recurring tool-use error category | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Evaluations of large language models in legal applications identify numeric-value extraction from degraded or page-break-spanning source text as a distinct reliability gap from general clause-interpretation accuracy | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |

**Contributing Factors**
- The document-parsing tool's output for a truncated or garbled clause span is structurally valid text, with no explicit flag distinguishing it from a fully clean extraction
- The risk-detection task treats producing a numeric cap value as a harder constraint than verifying that value came from clean, complete extracted text
- No automated check compares the reported cap figure's character-level confidence or completeness score against a defined threshold before the figure is used in a risk summary

---

## Mitigation Strategies

1. **Hard Stop on Low-Confidence or Truncated Numeric Extractions**: Prohibit the risk-detection agent from reporting a numeric cap value extracted from text flagged as truncated, garbled, or below a defined OCR-confidence threshold, requiring human verification instead
2. **Explicit Extraction-Quality Flag in Parsing Tool Output**: Require the document-parsing tool to return an explicit completeness or confidence flag for each extracted clause span, and block downstream use of any numeric value extracted from a flagged span
3. **Page-Break and Scan-Quality Triage**: Flag any clause known to span a page break, or any source document identified as a scan rather than native text, for mandatory secondary verification of extracted numeric figures before they are used in risk summaries
4. **Source-Image Cross-Check for High-Materiality Figures**: For numeric figures that materially affect a risk assessment (such as indemnification or liability caps), require a side-by-side check of the extracted value against the original source image or text, regardless of the parsing tool's reported confidence

### Metrics
- Rate of risk-detection summaries reporting a numeric value extracted from a clause span flagged as truncated or low-confidence
- Rate of cap-value discrepancies found when cross-checking extracted figures against original source documents in audit samples
- Rate of clauses spanning page breaks or appearing in scanned documents relative to total clauses processed

### Alerts
- A finalized risk-detection summary reports a numeric cap value extracted from a flagged truncated or low-confidence text span → P1
- A cross-check finds a material discrepancy between a reported cap figure and the original source document → P1
- Truncated or low-confidence extraction rate for numeric clause values exceeds the defined threshold for a rolling window → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
