# Building Custom Instead of Using Established AI Frameworks: PII, Guardrails, RAG, Evals, and Secrets

**Established framework adoption failures happen when a team builds ad-hoc tooling for a problem that a mature, public framework already solves, and so misses the edge cases, tested defaults, and maintenance the framework would have provided.** Six patterns cover PII detection, prompt-injection guardrails, cost observability, RAG, evaluation, and secrets detection.

## Key Takeaways

- These describe an upstream cause, not a symptom: not adopting the tool that would have caught the problem.
- Symptom-level patterns such as PII leakage and credential leakage live elsewhere in the library.
- Most of these start as quick work handed to one engineer, with no build-versus-buy review.

## Patterns

| Pattern | What goes wrong |
|---|---|
| [Missing Agent Eval Framework](failures/missing-agent-eval-framework.md) | Team builds a custom eval harness (a handful of manually-written test prompts checked by eyeballing the output) instead of adopting an established agent/RAG evaluation… |
| [Missing Cost Observability Framework](failures/missing-cost-observability-framework.md) | Team tracks LLM spend via manual log scraping or spreadsheet exports instead of adopting an established gateway/observability framework, losing real-time budget… |
| [Missing PII Detection Framework](failures/missing-pii-detection-framework.md) | Team relies on ad-hoc regex or manual review for PII detection/redaction instead of adopting an established, maintained framework, missing entity types and edge cases… |
| [Missing Prompt Injection Guardrails Framework](failures/missing-prompt-injection-guardrails-framework.md) | System prompt instructions are the only defense against prompt injection and unsafe output, with no established guardrails/scanning framework wired in front of or behind… |
| [Missing RAG Framework Adoption](failures/missing-rag-framework-adoption.md) | Team builds a bespoke retrieval pipeline (custom chunking, custom vector store glue, custom prompt assembly) from scratch instead of adopting an established RAG… |
| [Missing Secrets Detection Framework](failures/missing-secrets-detection-framework.md) | Agent outputs, logs, and tool-call payloads are never scanned by an automated secrets/credential-detection framework, relying on manual review (or nothing) to catch API… |

**Total: 6 patterns**

## How These Patterns Group

- **Safety and security:** Missing PII Detection Framework, Missing Prompt Injection Guardrails Framework, Missing Secrets Detection Framework
- **Quality and operations:** Missing Agent Eval Framework, Missing RAG Framework Adoption, Missing Cost Observability Framework

## When This Matters

- A custom regex, eval script, or retrieval pipeline is carrying production risk
- A build-versus-buy decision has not been made explicit
- Compliance or security needs a maintained control

## Frequently Asked Questions

### Should I build my own PII detection?

Ad-hoc regex tends to miss entity types a maintained framework covers. See missing PII detection framework.

### Are system prompt instructions enough to stop prompt injection?

The pattern argues no: they hold up in casual testing but not under adversarial testing. See missing prompt injection guardrails framework.

### Where should I scan for leaked secrets?

Not only in source code: logs, transcripts, and tool-call payloads too. See missing secrets detection framework.

## Related

- [All operations goals](../)
- [Operations overview](../../)
