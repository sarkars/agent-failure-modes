# What Are the Most Common Citation Accuracy Failures in AI Agents?

**Citation accuracy fails when a citation exists and looks legitimate but doesn't actually do the job a citation is supposed to do — either the source doesn't exist at all, the source exists but doesn't support the specific claim attached to it, or the citation points at the wrong document, the wrong granularity, or a broken link.** The mechanism that makes citation-accuracy failures dangerous is that most of the 7 patterns pass a naive verification check: a user who clicks a citation and confirms the source is real has not confirmed the source actually supports what was claimed, and legal RAG tools measured at 17-33% hallucination rates show the gap is common even in citation-heavy, high-stakes domains.

## Key Takeaways

- 7 patterns are documented here, splitting cleanly into citations that shouldn't exist (fabrication) and citations that exist but fail the job a citation is supposed to do (misgrounding, wrong source, missing coverage, wrong granularity, dead links).
- Misgrounded citations are the most insidious of the seven: a real, correctly-formatted citation to a real document that has been overruled, superseded, or simply doesn't say what the claim asserts passes basic source-existence verification while still being wrong.
- The real-world cost is documented, not hypothetical: lawyers in the Avianca lawsuit cited 6 fake ChatGPT-generated cases, and Westlaw's AI-Assisted Research tool showed roughly 2x the hallucination rate of other legal RAG tools in the Stanford study.
- Every one of the 7 patterns shares the same class of fix — verify the citation-claim relationship itself (via NLI/entailment checking, extractive quoting, or citing-from-metadata) rather than verifying only that the cited document exists.

## Scope

- **Fabrication** — [Fabricated Citations](failures/fabricated-citations.md). The model generates content beyond what was retrieved and invents a citation to match it — a nonexistent study, a fake case, a URL that leads nowhere.
- **Misgrounding** — [Misgrounded Citation](failures/misgrounded-citation.md), [Unsupported Claim](failures/unsupported-claim.md), [Wrong Source](failures/wrong-source.md). The cited document is real, but the claim-source relationship is broken: the source doesn't say what's claimed, has been superseded or overruled, or is simply the wrong one of several retrieved documents.
- **Coverage and Precision Gaps** — [Missing Citations](failures/missing-citations.md), [Granularity Mismatch](failures/granularity-mismatch.md). The citation practice itself is inconsistent — some claims go uncited entirely, or a citation points at an entire 500-page document instead of the specific section that actually supports the claim.
- **Link Integrity** — [Broken References](failures/broken-references.md). The citation was valid when generated but the underlying document has since moved, been deleted, or had its permissions changed.

## When Citation Accuracy Matters

- An agent operates in a domain (legal, medical, financial) where a citation is the mechanism a user relies on to independently verify a claim before acting on it
- Users are known to treat "the citation exists and I can click it" as sufficient verification, without checking whether the source's content actually supports the specific claim attached to it
- A knowledge base mixes documents from different time periods or jurisdictions, creating conditions for a citation to be technically real but no longer controlling (an overruled precedent, a repealed statute, a superseded policy)

## Cross-Pattern Insight

The through-line across all 7 citation-accuracy patterns is that citation verification has two independent layers, and most naive verification only checks one layer: does the cited source exist, and does the cited source actually support the specific claim attached to it. Fabricated Citations fails the first layer; Misgrounded Citation, Unsupported Claim, and Wrong Source all fail the second layer while passing the first, which is exactly why the second layer is harder to catch — a user or an automated link-checker confirming a document exists provides false reassurance about a claim the document doesn't actually support. The fix documented across citation accuracy is consistently to add claim-level verification — NLI/entailment scoring between the claim and the cited passage, requiring an extractive quote alongside every citation, or building citations directly from extraction metadata rather than letting the generation step attach citations after the fact — rather than treating citation existence as a proxy for citation correctness.

## Frequently Asked Questions

### What is the difference between a fabricated citation and a misgrounded citation?
A [Fabricated Citation](failures/fabricated-citations.md) points to a document that doesn't exist at all — a made-up study, case, or URL. A [Misgrounded Citation](failures/misgrounded-citation.md) points to a real, correctly-formatted, verifiable document that simply doesn't support the claim attached to it — the Stanford study's example is citing the real case Planned Parenthood v. Casey for a legal standard that was overruled by Dobbs. The second is harder to catch because the source passes existence verification.

### How do you catch a citation that supports the wrong claim?
Per [Unsupported Claim](failures/unsupported-claim.md) and [Wrong Source](failures/wrong-source.md), use an NLI (natural language inference) entailment check between the generated claim and the cited passage's actual text, and require an extractive quote alongside any generated citation so a mismatch between claim and source text is visible rather than implicit.

### Does citing the correct document guarantee the citation is accurate?
No. [Granularity Mismatch](failures/granularity-mismatch.md) shows a citation can point at a technically correct but practically useless level of specificity — an entire 500-page document when the claim is supported by one paragraph — forcing the user to search for the actual support. Correct-document citation and correctly-scoped citation are separate accuracy dimensions.

### Can citation problems be fixed by only citing from retrieved content?
It substantially reduces fabrication (per [Fabricated Citations](failures/fabricated-citations.md)) but does not fix misgrounding, wrong-source attribution, or granularity mismatch, since those three patterns involve citations to genuinely retrieved documents that are still wrong in their relationship to the claim. Closed-book citation generation is a necessary but not sufficient mitigation.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Broken References](failures/broken-references.md) | Cited URL or document has moved, been deleted, or had permissions changed since the citation was generated |
| [Fabricated Citations](failures/fabricated-citations.md) | Model generates content beyond retrieved context and invents a matching but nonexistent citation |
| [Granularity Mismatch](failures/granularity-mismatch.md) | Citation points at an entire document instead of the specific section/paragraph that supports the claim |
| [Misgrounded Citation](failures/misgrounded-citation.md) | A real, correctly-cited source doesn't actually support the claim — often because it's overruled, superseded, or off-topic |
| [Missing Citations](failures/missing-citations.md) | Citation practice is applied inconsistently, leaving some factual claims with no attribution at all |
| [Unsupported Claim](failures/unsupported-claim.md) | Cited source exists and is topically related but doesn't state the specific claim attached to it |
| [Wrong Source](failures/wrong-source.md) | Model confuses which of several retrieved documents actually contained the cited information |

**Total: 7 patterns**

## Related Goals

- [Answer Synthesis](../answer-synthesis/) — synthesis-stage failures (source contradiction, cherry-picking) that often co-occur with and compound citation-accuracy failures
- [Retrieval](../retrieval/) — retrieval-stage citation-mismatch failures that happen before generation even attaches a citation to a claim
- [Knowledge Freshness](../knowledge-freshness/) — the temporal-supersession mechanism behind misgrounded citations to overruled or repealed sources
