# AI Agent Reliability Playbook

> Failure patterns, eval recipes, mitigation strategies, and production signals for real-world AI agents.

⭐ Star this repo if you are building production AI agents.
🤝 PRs welcome: contribute failures from your domain.
📚 Use this as a checklist before shipping an AI agent.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

<p align="center">
  <strong>An open-source project by <a href="https://saralabs.ai">SaraLabs.ai</a></strong><br>
  We help teams build AI agents that work reliably in production.<br><br>
  <a href="https://saralabs.ai">Website</a> · <a href="mailto:team@saralabs.ai">Contact Us</a> · <a href="#about-saralabsai">About</a>
</p>

---

## Index

| Section | Description |
|---------|-------------|
| [Why This Repo?](#why-this-repo) | What makes this playbook different |
| [Structure](#structure) | How the repository is organized |
| [Agent Types](#agent-types) | Base agents and domain-specific agents |
| [How to Use](#how-to-use-this-repo) | Practical use cases and pattern structure |
| [Quick Reference](#quick-reference-cross-cutting-failure-patterns) | Most common failure patterns at a glance |
| [References](REFERENCES.md) | Research sources, incident databases, statistics |
| [Contributing](#contributing) | How to add failure patterns |
| [About SaraLabs.ai](#about-saralabsai) | Who we are and how to work with us |

---

## Why This Repo?

Unlike academic failure taxonomies, this repository focuses on **real deployment issues** that engineers encounter when building and operating AI agents. Each failure pattern is a complete playbook:

- **Eval Recipes**: Test cases and metrics to catch failures before production
- **Mitigation Strategies**: Architecture patterns and code to prevent failures
- **Production Signals**: Metrics, alerts, and dashboards to detect failures in real-time

Plus concrete examples from production systems and root cause analysis.

## Structure

The repository follows a **goal-based hierarchy**:

```
agents/
├── cross-cutting/                 # Apply to ALL AI systems
│   ├── security/                  # 57 patterns
│   ├── accuracy/                  # 53 patterns
│   ├── operations/                # 112 patterns
│   ├── governance/                # 12 patterns
│   └── learning/                  # 12 patterns
│
├── by-capability/                 # Design-driven failure modes
│   ├── task-planning/             # Planning, goal understanding
│   ├── external-actions/          # External system execution
│   ├── speech-and-audio/          # Speech/audio handling
│   ├── domain-expertise/          # Domain judgment
│   ├── document-processing/       # OCR patterns
│   ├── knowledge-retrieval/       # RAG patterns
│   └── multi-agent-systems/       # Coordination
│
└── by-use-case/                   # Domain-specific
    ├── customer-service/          # Support conversations
    └── mortgage-documents/        # Mortgage OCR and compliance
```

## Pattern Categories

### Cross-Cutting (Apply to ALL AI Systems)

| Category | Description | Goals | Patterns |
|----------|-------------|-------|----------|
| [Cross-Cutting](agents/cross-cutting/) | **All universal patterns** | 24 | 246 |
| ├─ [Security](agents/cross-cutting/security/) | Security, trust, runtime protection, DLP | 5 | 57 |
| ├─ [Accuracy](agents/cross-cutting/accuracy/) | Output correctness, evaluation, verification | 5 | 53 |
| ├─ [Operations](agents/cross-cutting/operations/) | Tools, cost, coordination, memory, state | 12 | 112 |
| ├─ [Governance](agents/cross-cutting/governance/) | Compliance, audit, accountability | 1 | 12 |
| └─ [Learning](agents/cross-cutting/learning/) | Self-improvement, feedback loops | 1 | 12 |

### By Capability (Design-Driven Failure Modes)

| Capability | Description | Goals | Patterns |
|------------|-------------|-------|----------|
| [Task Planning](agents/by-capability/task-planning/) | Goal understanding, task planning | 2 | 20 |
| [External Actions](agents/by-capability/external-actions/) | Action execution in external systems | 1 | 11 |
| [Speech and Audio](agents/by-capability/speech-and-audio/) | Speech recognition and synthesis | 4 | 66 |
| [Domain Expertise](agents/by-capability/domain-expertise/) | Domain-specific judgment | 1 | 10 |
| [Document Processing](agents/by-capability/document-processing/) | OCR and document text extraction | 6 | 48 |
| [Knowledge Retrieval](agents/by-capability/knowledge-retrieval/) | RAG and retrieval-augmented generation | 5 | 52 |
| [Multi-Agent Systems](agents/by-capability/multi-agent-systems/) | Coordination and orchestration | 1 | 15 |

### By Use Case (Domain-Specific)

| Use Case | Description | Goals | Patterns |
|----------|-------------|-------|----------|
| [Customer Service](agents/by-use-case/customer-service/) | Customer conversation resolution | 1 | 11 |
| [Mortgage Documents](agents/by-use-case/mortgage-documents/) | Mortgage document OCR and compliance | 3 | 24 |
| [Code](agents/by-use-case/code/) | Code generation and review | - | Planned |
| [Data Extraction](agents/by-use-case/data-extraction/) | Structured data extraction | - | Planned |

**Total: 503 patterns across 48 goals**

## How to Use This Repo

### Quick Start

1. **Identify your agent type** - Find the category that matches your use case (e.g., `agents/ocr-agent/`)
2. **Browse by goal** - Each agent has business/technical goals (e.g., `goals/accurate-text-extraction/`)
3. **Review failure patterns** - Each goal contains documented failures (e.g., `failures/character-confusion.md`)
4. **Apply mitigations** - Each failure includes root cause analysis and mitigation strategies

### Navigation Path

```
Agent Type → Business/Technical Goal → Failure Pattern
    ↓              ↓                        ↓
OCR Agent → Accurate Text Extraction → Character Confusion
```

### Practical Use Cases

#### During Development
- **Pre-build planning**: Review failure patterns for your agent type before writing code. Understanding common pitfalls helps you design defensive architectures from the start.
- **Code reviews**: Reference specific failure patterns when reviewing agent implementations. Ask "Have we mitigated [failure-pattern]?"
- **Test case generation**: Use failure examples to create targeted test cases that probe known weak points.

#### During Testing & QA
- **Red teaming**: Use failure patterns as a checklist for adversarial testing. Each pattern suggests specific attack vectors or edge cases to test.
- **Evaluation design**: Build evaluation datasets that specifically target documented failure modes.
- **Acceptance criteria**: Define pass/fail criteria based on whether known failure patterns are adequately mitigated.

#### In Production
- **Incident response**: When failures occur, use the taxonomy to quickly categorize and diagnose issues. Match symptoms to documented patterns for faster resolution.
- **Monitoring & alerting**: Set up observability based on failure detection strategies in each pattern.
- **Post-mortems**: Reference failure patterns in incident reports to connect specific failures to systemic issues.

#### For Teams & Organizations
- **Onboarding**: New team members can study failure patterns to quickly understand what can go wrong with AI agents.
- **Knowledge sharing**: Use patterns as a shared vocabulary across teams ("We're seeing a classic context-overflow failure").
- **Risk assessment**: Before deploying agents, audit against relevant failure patterns to identify gaps.

### Each Failure Pattern Includes

| Section | What It Tells You |
|---------|-------------------|
| **Issue** | One-line description of the failure |
| **Frequency** | How often this occurs (Common, Occasional, Rare) |
| **Symptoms** | Observable signs that this failure is happening |
| **Root Cause** | Why this failure occurs at a technical level |
| **Example** | Concrete scenario with code/logs showing the failure |
| **Key Statistics** | Data from research and production systems |
| **Contributing Factors** | Conditions that increase likelihood |

#### Actionable Sections

| Section | Purpose | Contents |
|---------|---------|----------|
| **Eval Recipes** | Test before production | Test cases, evaluation datasets, metrics, automated checks |
| **Mitigation Strategies** | Prevent the failure | Prevention techniques, detection & response, architecture patterns |
| **Production Signals** | Monitor in production | Key metrics, logs & traces, alerts, dashboard panels, health checks |

See [PATTERN_TEMPLATE.md](PATTERN_TEMPLATE.md) for the full pattern structure.

## Quick Reference: Cross-Cutting Failure Patterns

These failures appear across multiple AI systems. See [Cross-Cutting Patterns](agents/cross-cutting/) for full documentation.

| Pattern | Category | Goal | Description |
|---------|----------|------|-------------|
| [Prompt Injection](agents/cross-cutting/security/goals/safety-security/failures/prompt-injection.md) | Security | Safety & Security | Malicious input hijacks system behavior |
| [Memory Poisoning](agents/cross-cutting/security/goals/safety-security/failures/memory-poisoning.md) | Security | Safety & Security | Malicious instructions injected into memory |
| [MCP Protocol Exploitation](agents/cross-cutting/security/goals/runtime-security/failures/mcp-protocol-exploitation.md) | Security | Runtime Security | MCP vulnerabilities enable RCE on 200K+ servers |
| [Unverified Output](agents/cross-cutting/security/goals/agent-trust/failures/unverified-agent-output.md) | Security | Agent Trust | Accepting outputs without verification |
| [Confident Fabrication](agents/cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md) | Accuracy | Output Accuracy | False information stated with high confidence |
| [Goal Drift](agents/cross-cutting/accuracy/goals/reasoning-quality/failures/goal-drift.md) | Accuracy | Reasoning Quality | Losing focus on original objective |
| [Context Overflow](agents/cross-cutting/accuracy/goals/context-management/failures/context-overflow.md) | Accuracy | Context Management | Information loss when context exceeds limits |
| [Infinite Loops](agents/cross-cutting/operations/goals/cost-efficiency/failures/infinite-loops.md) | Operations | Cost Efficiency | Stuck in retry loops, burns tokens |
| [Parameter Mismatches](agents/cross-cutting/operations/goals/tool-reliability/failures/parameter-mismatches.md) | Operations | Tool Reliability | 37% of tool calls have silent parameter errors |
| [Agent Misalignment](agents/cross-cutting/operations/goals/multi-agent-coordination/failures/agent-misalignment.md) | Operations | Multi-Agent | Pursuing conflicting objectives |
| [PII Exposure](agents/cross-cutting/security/goals/data-loss-prevention/failures/pii-exposure.md) | Security | Data Loss Prevention | Outputs contain personal data |
| [Cross-Session Bleed](agents/cross-cutting/security/goals/data-loss-prevention/failures/cross-session-bleed.md) | Security | Data Loss Prevention | User A's data appears in User B's session |

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

To add a new failure pattern:
1. Navigate to the appropriate agent type (e.g., `agents/ocr-agent/`)
2. Find or create the relevant goal folder (e.g., `goals/accurate-text-extraction/`)
3. Add a new failure file in `failures/` (e.g., `failures/my-failure.md`)
4. Update the goal's README.md to include your failure in the table
5. Submit a PR

## Related Resources

- [Awesome Agent Failures (Vectara)](https://github.com/vectara/awesome-agent-failures) - Academic/research-focused failure documentation
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - Security vulnerabilities in LLM applications

---

## About SaraLabs.ai

<p align="center">
  <a href="https://saralabs.ai"><strong>saralabs.ai</strong></a> — Building reliable AI agents for production
</p>

This repository is maintained by **[SaraLabs.ai](https://saralabs.ai)**, a company dedicated to making AI agents work reliably in production environments.

### Our Mission

We believe AI agents will transform how businesses operate—but only if they work reliably. Today, **40% of agentic AI projects are projected to be scrapped by 2027** (Gartner), and **88% of enterprises report AI agent security incidents**. We're here to change that.

SaraLabs.ai builds the knowledge, tools, and expertise needed to deploy AI agents with confidence.

### What We Do

| Area | Description |
|------|-------------|
| **Domain-Specific Reliability** | Deep expertise in vertical-specific agent failures (legal, healthcare, finance, enterprise) |
| **Production AI Agents** | Build and deploy agents that handle real-world edge cases |
| **Reliability Engineering** | Eval frameworks, monitoring systems, and failure detection |
| **Consulting & Advisory** | Help teams ship agents faster with fewer production incidents |

### Why This Repository?

This playbook represents our core belief: **reliability knowledge should be open**.

- Every failure pattern comes from real production incidents
- We continuously update with new failure modes as the field evolves
- Domain-specific agents (OCR, RAG, Voice, Code) get dedicated coverage
- Community contributions make this resource stronger

By sharing this knowledge openly, we help the entire ecosystem build better AI agents—and demonstrate the depth of expertise we bring to our work.

### Work With Us

| Need | How We Help |
|------|-------------|
| **Shipping an AI agent?** | We audit for reliability gaps before launch |
| **Agent failing in production?** | We diagnose and fix systematic issues |
| **Building an eval framework?** | We design domain-specific evaluation systems |
| **Training your team?** | We run workshops on agent reliability |

### Get In Touch

| | |
|---|---|
| **General inquiries** | [team@saralabs.ai](mailto:team@saralabs.ai) |
| **Consulting & projects** | [team@saralabs.ai](mailto:team@saralabs.ai) |
| **Contribute a pattern** | Submit a PR or email us |
| **Report an issue** | Open a GitHub issue |

We respond to every inquiry. If you've encountered a failure pattern not documented here, we'd love to hear about it.

<p align="center">
  <a href="https://saralabs.ai"><strong>Visit saralabs.ai →</strong></a>
</p>

---

*Built by [SaraLabs.ai](https://saralabs.ai) — Reliable AI agents for production.*
