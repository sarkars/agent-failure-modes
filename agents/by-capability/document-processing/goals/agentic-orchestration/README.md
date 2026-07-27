# What Are the Most Common Agentic Orchestration Problems in Document-Processing AI Agents?

**Agentic orchestration fails when an agent's document reasoning is sound but the surrounding machinery — context management, tool calls, and self-correction — corrupts or loses the information the reasoning depends on.** Frontier agents score below 50% accuracy on Databricks' OfficeQA benchmark for real enterprise document reasoning tasks not because reasoning is weak, but because the agent read the wrong value, called a tool with the wrong page number, or "fixed" a correct field to match a misread total. Orchestration failures matter because they turn a single upstream error — a misread character, a truncated chunk — into a full pipeline failure that looks like a reasoning problem but isn't.

## Key Takeaways

- 6 patterns cover agentic document orchestration, grouped into three mechanisms: long-document context management, the reading/reasoning gap, and tool/correction-layer errors.
- Reading, not reasoning, is the dominant bottleneck: Databricks' OfficeQA benchmark found frontier agents scoring below 50% accuracy on real enterprise document tasks, and 37% of tool calls carry silent parameter mismatches per developer analysis.
- Error recovery is a distinct failure surface from extraction itself — an agent's own "fix" for a detected inconsistency can corrupt a correct value to satisfy an incorrect one, worsening accuracy rather than improving it.
- The dominant architectural fix across all 6 patterns is separation of concerns: split reading from reasoning, split extraction from correction, and resolve cross-document conflicts in a dedicated reconciliation stage rather than inline during a single pass.

## Scope

- **Long-document context management** — [context-window-limits](failures/context-window-limits.md), [conflicting-information](failures/conflicting-information.md). Both stem from documents too long to process in a single pass: naive chunking breaks cross-references and tables spanning pages, and the same field recurring across locations (original, amendment, final terms) creates unreconciled duplicate values.
- **The reading/reasoning gap** — [reading-bottleneck](failures/reading-bottleneck.md), [unstructured-documents](failures/unstructured-documents.md). The agent's reasoning chain is logically valid but built on a misread input value or on narrative text with no labeled field to anchor extraction, so a correct reasoning process still produces a wrong output.
- **Tool and correction-layer errors** — [tool-parameter-errors](failures/tool-parameter-errors.md), [error-recovery-errors](failures/error-recovery-errors.md). Errors introduced when the agent translates understanding into action — miscalculating a page/region parameter, or "correcting" a good value to match a bad one during self-repair.

## When Agentic Orchestration Matters

- A document-processing agent runs multi-step workflows over long documents (contracts, filings) where cross-references, amendments, or tables span dozens of pages
- The agent has autonomy to call extraction tools with agent-generated parameters (page ranges, region coordinates) rather than fixed, human-specified inputs
- The pipeline includes any self-correction or validation-driven "fix" logic, where an agent's own error-recovery step could itself introduce a new error

## Cross-Pattern Insight

Every mitigation in agentic orchestration separates a step that used to happen implicitly inside one agent pass into two explicit, independently-auditable stages. Context-window-limits and conflicting-information both push toward extract-then-reconcile: pull every candidate value with its location first, then apply reconciliation logic as a separate, testable stage. Reading-bottleneck and unstructured-documents both push toward extract-then-reason: a dedicated parsing/candidate-surfacing stage feeds a reasoning stage, rather than one agent call reading and reasoning simultaneously. Tool-parameter-errors and error-recovery-errors both push toward validate-before-and-after-action: schema-enforce parameters before a tool call executes, and re-run full validation after any correction to catch a "fix" that broke something else. The shared theme is that orchestration reliability comes from decomposing a single agent pass into stages that can each be checked, not from a more capable single-shot agent.

## Frequently Asked Questions

### Is agentic orchestration failure a reasoning problem or a reading problem?
Usually reading. The reading-bottleneck pattern documents frontier agents reasoning correctly through a multi-step task while scoring under 50% accuracy on OfficeQA, because the reasoning chain started from a misread number. Fixing orchestration failures means fixing what the agent reads and how it calls tools, not upgrading the reasoning model.

### How does an agent's own error-correction step end up making extraction worse instead of better?
Because a validation mismatch (e.g., line items don't sum to the stated total) doesn't tell the agent which side is wrong. The error-recovery-errors pattern shows agents adjusting a correct line-item value to match an incorrectly-read grand total, since without a reliability ranking or confidence gate, the agent has no basis to know which field is more trustworthy.

### How should long documents be chunked to avoid losing cross-references?
Prefer structure-aware chunking on section/heading boundaries over fixed token counts, paired with a cross-reference pre-resolution pass that maps phrases like "see Exhibit B" to their target content before chunking begins, per the context-window-limits pattern. A retrieval-augmented fallback lets the agent query the full indexed document on demand when a chunk's extraction confidence is low.

### What's the difference between conflicting-information and error-recovery-errors?
Conflicting-information is a source-document problem — the same field genuinely appears with different values across pages (draft, amendment, final terms) and needs reconciliation logic. Error-recovery-errors is an agent-behavior problem — the agent's own attempt to fix a detected inconsistency introduces a new error, independent of whether the source document itself was ever ambiguous.

### Do tool parameter errors show up in agent logs?
Not reliably. The tool-parameter-errors pattern notes tool-parameter mismatches are silent — the tool executes successfully on a slightly-wrong parameter (e.g., an off-by-one page number) and returns a plausible-looking result, so detection requires validating tool *output* plausibility against the intended target, not just checking that the call succeeded.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Conflicting Information](failures/conflicting-information.md) | Same field has different values across document locations; agent picks arbitrary/first occurrence |
| [Context Window Limits](failures/context-window-limits.md) | Naive chunking breaks cross-references and tables spanning pages |
| [Error Recovery Errors](failures/error-recovery-errors.md) | Agent's own correction "fixes" good data to match a bad extraction |
| [Reading Bottleneck](failures/reading-bottleneck.md) | Correct reasoning chain built on a misread input value |
| [Tool Parameter Errors](failures/tool-parameter-errors.md) | Off-by-one or misspecified page/region parameters passed to extraction tools |
| [Unstructured Documents](failures/unstructured-documents.md) | Key values sit in narrative text with no labeled field to extract from |

**Total: 6 patterns**

## Related Goals

- [Accurate Text Extraction](../accurate-text-extraction/) — character-level misreads that reading-bottleneck and tool-parameter-errors build failures on top of
- [Production Reliability](../production-reliability/) — orchestration failures at pipeline scale, once agentic workflows are running in production
- [Multimodal Reliability](../multimodal-reliability/) — hallucination and confidence-calibration failures in the vision-language models orchestration agents call as tools
