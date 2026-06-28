# Pattern Currency Review

A pass over all 544 failure-pattern files (by filename, then by content for
plausible candidates) to find patterns that newer model/agent capabilities
have significantly mitigated. Goal: avoid presenting solved problems as open
frontier risks.

## Method
1. Listed every file under `agents/**/failures/*.md` (544 total).
2. Scanned filenames for likely candidates: anything implying a pre-structured-output,
   pre-large-context-window, or pre-voice-native-model failure mode.
3. Read the full content of each candidate before acting — filename alone is not
   sufficient evidence of staleness (several "looked old" but the content's root
   cause turned out to be architectural, not a model-capability gap).

## Confirmed deprecated (marked in-file)

| File | Reason |
|------|--------|
| [`tool-reliability/failures/parameter-mismatches.md`](agents/cross-cutting/operations/goals/tool-reliability/failures/parameter-mismatches.md) | Model emitting wrong parameter *types* (string vs int, etc.) is largely closed by strict JSON-schema / structured-output tool-calling, now standard across major model APIs. |
| [`conversation-flow/failures/text-prompt-voice-failure.md`](agents/by-capability/speech-and-audio/goals/conversation-flow/failures/text-prompt-voice-failure.md) | Assumes a cascaded text-LLM-then-TTS pipeline. Native speech-to-speech models generate audio directly and don't carry markdown/list formatting into speech, so this mainly applies to legacy cascaded architectures. |

## Candidates examined and rejected (kept as-is, with reasoning)

These looked like plausible "solved by bigger context windows / better tooling"
candidates by name, but reading the content showed the failure is architectural,
not capability-bound — larger windows or better tokenizers don't fix them:

| File | Why it's still current |
|------|------------------------|
| `agentic-orchestration/failures/context-window-limits.md` | About chunking breaking cross-references in long documents — a chunking-strategy problem, independent of window size. |
| `context-management/failures/context-overflow.md` | Same root cause — information loss from truncation/summarization, not eliminated by bigger windows, only deferred. |
| `answer-synthesis/failures/context-window-saturation.md` | Explicitly about "lost in the middle" attention degradation — research (e.g. arXiv 2307.03172) shows *more* context can hurt quality even with 100k+ token windows. Larger windows make this worse, not better. |
| `cost-tracking/failures/token-counting-inaccuracy.md` | Multimodal/image token estimation and tokenizer-version mismatches are still common; not resolved by model upgrades. |
| `agentic-orchestration/failures/tool-parameter-errors.md` | Looks like a duplicate of `parameter-mismatches.md`, but the example is a semantic error (off-by-one page number), not a type/schema error — structured-output enforcement doesn't catch this class of mistake. |
| `tool-reliability/failures/silent-type-coercion.md`, `schema-drift.md`, `tool-invocation/failures/wrong-argument-format.md`, `missing-required-parameter.md` | All about tool-side leniency or tool versioning, not model-generation capability — unaffected by model upgrades. |

## Full-repo sweep (completed)

All 544 files have now been read in full (via parallel/sequential read-only
audits, one pass per category, same strict bar: only flag if a *specific,
named* capability closes the *specific* root cause — not "models are better
now"). Result: **no additional deprecation candidates found.**

| Category | Files reviewed | New candidates |
|---|---|---|
| `by-capability/document-processing` | 48 | 0 |
| `by-capability/speech-and-audio` | 65 (+1 already deprecated) | 0 |
| `by-capability/knowledge-retrieval` + `multi-agent-systems` + `task-planning` + `external-actions` + `domain-expertise` | 109 | 0 |
| `cross-cutting/operations` + `governance` + `learning` | 143 | 0 |
| `cross-cutting/security` + `accuracy` | 109 | 0 (security/hallucination patterns are explicitly open problems, not closed by model upgrades) |
| `by-use-case/mortgage-documents` | 53 | 0 (compliance/regulatory/fraud patterns are legal/process problems immune to model upgrades) |
| `by-use-case/customer-service` | 11 | 0 — all 11 files are unfilled stubs with no described failure mechanism, so staleness can't even be judged until they're fleshed out (a content-completeness issue, separate from staleness) |

**Final tally: 2 of 544 files (0.4%) marked deprecated.** The corpus is, on
the whole, well-curated against staleness — most "looked old" candidates
(context-window-limits, token-counting, response-latency) turned out on
close reading to be architectural/persistent rather than capability-bound.
The dominant quality issue in this repo remains the ~32% unfilled
placeholder stubs identified in the earlier quality review, not staleness.
