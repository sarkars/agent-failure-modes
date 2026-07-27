# What Are the Most Common Output Filtering and Moderation Failures in AI Agents?

**Output filtering fails when agents designed to prevent harmful, illegal, or policy-violating content in their outputs instead produce content that violates guardrails, bypasses moderation checks, or leaks unfiltered data.** An agent trained to refuse hate-speech requests outputs responses that skirt policy by using coded language or dog-whistles, an agent's output filtering checks miss adversarially-crafted content that technically passes filters but violates policy intent, and an agent designed to redact sensitive data in outputs fails to redact because the sensitive patterns were not anticipated. Output filtering failures matter precisely because they represent failures of the final safety layer: even if upstream systems are secure, harmful output directly harms users and erodes trust.

## Key Takeaways

- Output filtering and moderation cover detecting and preventing harmful, illegal, or policy-violating content in agent output.
- Output filtering gaps are often discovered via user escalation or public exposure rather than automated detection, indicating that moderation systems are incomplete.
- Adversarial inputs and outputs that technically pass filters but violate policy intent are common: filters based on exact-match or keyword detection can be evaded by paraphrase or coded language.
- Effective output filtering requires both technical checks (pattern matching, format validation) and semantic checks (does output violate policy intent), plus continuous red-teaming to identify filter bypasses.

## Scope

Output filtering covers multiple moderation concerns, including:
- **Harmful Content Detection** — Detect and block hate speech, violence, harassment, sexual content, illegal activity guidance.
- **Policy Violation Detection** — Detect and block content that violates organizational policy (data exfiltration guidance, competitor information, proprietary code leakage).
- **Sensitive Data Redaction** — Redact PII, credentials, trade secrets, and other sensitive information from agent output.
- **Format and Structure Validation** — Validate output format and structure to prevent injection attacks or policy violations in output structure.

## When Output Filtering Matters

- Agents operate in high-risk domains (child safety, financial fraud, terrorism) where harmful output directly endangers users.
- Agents produce output that reaches external audiences (user-facing interfaces, published documents) and moderation failures are visible to users and regulators.
- Agents output structured data (JSON, SQL, code) where format or structure violations can enable downstream attacks or policy violations.

## Cross-Pattern Insight

Effective output filtering requires defense in depth: no single filter (keyword detection, pattern matching, LLM-based moderation) is sufficient alone. Keyword filters miss paraphrases and coded language. LLM-based moderation can be adversarially manipulated. Format validation prevents injection but not content violations. The shared lesson is that output filtering requires layered defenses, continuous testing against adversarial evasion attempts, and human review of filter failures to close gaps.

## Failure Patterns

The output-filtering-moderation goal currently has no documented failure patterns. Patterns in output-filtering-moderation will focus on filter-bypass techniques, adversarial evasion of moderation systems, false-negative and false-positive rates in moderation detection, and failures in sensitive-data redaction.

## Related Goals

- [Safety & Security](../safety-security/) — core safety constraints; output-filtering focuses on preventing harmful content in outputs after agent reasoning.
- [Data Loss Prevention](../data-loss-prevention/) — prevents data exfiltration; output-filtering includes sensitive-data redaction to prevent data leakage via output.
