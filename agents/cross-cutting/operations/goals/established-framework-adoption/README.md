# Established Framework Adoption

The recurring mechanism across every pattern here: a well-solved problem (PII detection, prompt-injection defense, cost observability, RAG pipelines, agent evaluation, secrets scanning) already has a mature, publicly available framework, but the team builds ad-hoc or custom tooling instead — missing the edge-case coverage, tested defaults, and maintenance the framework would have provided. Distinct from the many existing *symptom*-level patterns elsewhere in this repo (e.g., PII leakage, credential leakage) — those describe what goes wrong; these describe the upstream root cause of not adopting the tool that would have caught it.

## Failure Patterns

| Pattern |
|---------|
| [Missing PII Detection Framework](failures/missing-pii-detection-framework.md) |
| [Missing Prompt Injection Guardrails Framework](failures/missing-prompt-injection-guardrails-framework.md) |
| [Missing Cost Observability Framework](failures/missing-cost-observability-framework.md) |
| [Missing RAG Framework Adoption](failures/missing-rag-framework-adoption.md) |
| [Missing Agent Eval Framework](failures/missing-agent-eval-framework.md) |
| [Missing Secrets Detection Framework](failures/missing-secrets-detection-framework.md) |

**Total: 6 patterns**
