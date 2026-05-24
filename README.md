# AI Agent Failure Taxonomy

> A practitioner's guide to real-world AI agent failures - organized by agent type, goals, and common issues encountered in production deployments.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## Why This Repo?

Unlike academic failure taxonomies, this repository focuses on **real deployment issues** that engineers encounter when building and operating AI agents. Each failure is documented with:

- Concrete examples from production systems
- Root cause analysis
- Mitigation strategies that actually work

## Structure

The repository follows a **goal-based hierarchy**:

```
agents/
└── <agent-type>/
    ├── README.md                    # Agent overview
    └── goals/
        └── <business-or-technical-goal>/
            ├── README.md            # Goal description
            └── failures/
                └── <failure-pattern>.md  # Individual failure pattern
```

### Example: OCR Agent

```
agents/
└── ocr-agent/
    ├── README.md
    └── goals/
        ├── accurate-text-extraction/
        │   ├── README.md
        │   └── failures/
        │       ├── character-confusion.md
        │       ├── punctuation-errors.md
        │       ├── font-handling.md
        │       └── ...
        ├── layout-preservation/
        │   └── failures/
        │       ├── table-boundaries.md
        │       └── ...
        ├── document-classification/
        ├── multimodal-reliability/
        ├── agentic-orchestration/
        └── production-reliability/
```

## Agent Types

| Agent Type | Description | Goals | Failure Patterns |
|------------|-------------|-------|------------------|
| [Generic Agent](agents/generic-agent/) | **Cross-cutting failures for any agent** | 8 | 85 |
| [OCR Agent](agents/ocr-agent/) | Document text extraction and processing | 6 | 48 |
| [Code Agent](agents/code-agent/) | Code generation, review, and modification | 4 | Planned |
| [Customer Service Agent](agents/customer-service-agent/) | Customer interaction and support | 4 | Planned |
| [RAG Agent](agents/rag-agent/) | Retrieval-augmented generation | 4 | 31 |
| [Data Extraction Agent](agents/data-extraction-agent/) | Structured data extraction from unstructured sources | 4 | Planned |
| [Workflow Agent](agents/workflow-agent/) | Multi-step task automation | 4 | Planned |

## How to Use This Repo

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

## Quick Reference: Cross-Cutting Failure Patterns

These failures appear across multiple agent types. See [Generic Agent](agents/generic-agent/) for full documentation.

| Pattern | Goal | Description |
|---------|------|-------------|
| [Infinite Loops](agents/generic-agent/goals/cost-efficiency/failures/infinite-loops.md) | Cost Efficiency | Agent gets stuck in retry loops, burns tokens |
| [Parameter Mismatches](agents/generic-agent/goals/tool-reliability/failures/parameter-mismatches.md) | Tool Reliability | 37% of tool calls have silent parameter errors |
| [Confident Fabrication](agents/generic-agent/goals/output-accuracy/failures/confident-fabrication.md) | Output Accuracy | Agent states false information with high confidence |
| [Context Overflow](agents/generic-agent/goals/context-management/failures/context-overflow.md) | Context Management | Agent loses information when context exceeds limits |
| [Prompt Injection](agents/generic-agent/goals/safety-security/failures/prompt-injection.md) | Safety & Security | Malicious input hijacks agent behavior |
| [Goal Drift](agents/generic-agent/goals/reasoning-quality/failures/goal-drift.md) | Reasoning Quality | Agent loses focus on original objective |
| [Memory Poisoning](agents/generic-agent/goals/safety-security/failures/memory-poisoning.md) | Safety & Security | Malicious instructions injected into agent memory |
| [Agent Misalignment](agents/generic-agent/goals/multi-agent-coordination/failures/agent-misalignment.md) | Multi-Agent | Agents pursue conflicting objectives |
| [MCP Protocol Exploitation](agents/generic-agent/goals/agent-runtime-security/failures/mcp-protocol-exploitation.md) | Agent Runtime Security | MCP vulnerabilities enable RCE on 200K+ servers |

## Research Sources & References

### Incident Databases

| Source | Description |
|--------|-------------|
| [AI Incident Database (AIID)](https://incidentdatabase.ai/) | 3,000+ documented real-world AI failures, open-source |
| [MIT AI Incident Tracker](https://airisk.mit.edu/ai-incident-tracker) | 1,400+ incidents classified by risk, cause, harm, severity |
| [Museum of Failure - AI Exhibits](https://museumoffailure.com/exhibition/air-canada-ai-chat) | Curated AI failure case studies |

### Academic Research

| Paper | Key Contribution |
|-------|------------------|
| [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) | 1600+ annotated traces, 14 failure modes across 7 MAS frameworks |
| [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) | Red team analysis of memory poisoning, bias, action isolation |
| [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) | 142 traces, 6 failure modes, system-for-agent design paradigm |
| [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) | 15 hidden failure modes from system-engineering perspective |
| [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) | Legal AI tools hallucinate 17-33% despite RAG |
| [Why AI Agents Fail (AREP Framework)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6572478) | 40+ sources, 7 practitioner recommendations |

### Industry Analysis

| Source | Coverage |
|--------|----------|
| [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) | Field analysis of production failures |
| [Adversa AI 2025 Security Report](https://adversa.ai/blog/adversa-ai-unveils-explosive-2025-ai-security-incidents-report-revealing-how-generative-and-agentic-ai-are-already-under-attack/) | AI security incidents and attack patterns |
| [Responsible AI Labs: AI Safety 2024](https://responsibleailabs.ai/knowledge-hub/articles/ai-safety-incidents-2024) | Lessons from real-world failures |
| [Digital Defynd: Top 40 AI Disasters](https://digitaldefynd.com/IQ/top-ai-disasters/) | Detailed analysis of major AI failures |

### Notable Incident Case Studies

#### Infrastructure Failures
- [PocketOS Database Wipe](https://dev.to/alessandro_pignati/the-9-second-disaster-how-an-ai-agent-wiped-a-production-database-p56) - Claude agent deleted production DB in 9 seconds
- [Replit Rogue Agent](https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/) - Agent ran DROP TABLE, created fake users to cover tracks

#### Customer Service Failures
- [Air Canada Chatbot Lawsuit](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416) - Invented bereavement fare policy, company held liable
- [DPD Chatbot](https://www.theregister.com/2024/01/23/dpd_chatbot_goes_rogue/) - Swore, wrote poem calling itself "worst delivery company"
- [NYC MyCity Chatbot](https://www.cxtoday.com/contact-center/3-times-customer-chatbots-went-rogue-and-the-lessons-we-need-to-learn/) - Advised businesses to break laws
- [McDonald's AI Drive-Thru](https://www.cnbc.com/2024/06/17/mcdonalds-to-end-ibm-ai-drive-thru-test.html) - Ordered 260 chicken nuggets, added bacon to ice cream
- [Chevy Tahoe $1 Deal](https://medium.com/cut-the-saas/chatbot-case-study-purchasing-a-chevrolet-tahoe-for-1-fc3a51ab2561) - Chatbot agreed to legally binding $1 price

#### Legal Domain Failures
- [Avianca Lawyers](https://www.cnn.com/2023/05/27/business/chat-gpt-avianca-mata-lawyers/index.html) - Submitted brief with 6 fake ChatGPT-generated cases, fined $5K

### Agent-Type Specific Resources

#### RAG Agents
- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Causes, risks, and fixes
- [RAGAS Fails 83% of Time](https://medium.com/data-science-collective/air-canada-lost-a-lawsuit-because-their-rag-hallucinated-yours-will-too-b92b6b9a4d39) - Benchmark results
- [Self-Healing RAG Layer](https://towardsdatascience.com/rag-hallucinates-i-built-a-self-healing-layer-that-fixes-it-in-real-time/) - Real-time hallucination fixes

#### Voice Agents
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Common issues and fixes
- [AppInventiv: 8 Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Why AI voice agents fail
- [Bluejay: 7 Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Voice agents in production
- [AssistYou: Mishearing Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - ASR accuracy issues

#### Code Agents
- [Cursor vs Claude Code vs Copilot](https://levelup.gitconnected.com/cursor-vs-claude-code-vs-copilot-i-spent-500-testing-all-three-on-real-production-code-c57f97607d36) - Production testing comparison
- [15 AI Coding Agents Ranked](https://www.morphllm.com/ai-coding-agent) - Only 3 changed how teams ship

#### OCR/Document Agents
- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Extraction layer failures
- [OCR vs IDP](https://forage.ai/blog/ocr-vs-idp/) - Why traditional OCR fails
- [Why AI OCR Fails](https://parseur.com/blog/why-ai-ocr-fail) - Common OCR failure patterns
- [Why OCR Alone Fails in Real-World Documents](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Production failure patterns
- [Why OCR Is the Weakest Part of Document AI](https://medium.com/@manalisomani099/why-ocr-is-the-weakest-part-of-most-document-ai-systems-c9188381d1b9) - System-level analysis
- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - Practitioner perspectives on OCR, agents, tables
- [IDP Challenges 2026](https://idp-software.com/guides/idp-challenges-2026/) - Table extraction as hardest unsolved problem

#### Multimodal/VLM Document Processing
- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) - Object, attribute, relational hallucination types
- [Mitigating OCR Hallucinations in MLLMs](https://arxiv.org/html/2506.20168v2) - NeurIPS 2025 research on visual degradation
- [Why LLMs Hallucinate More on Enterprise Documents](https://www.adlibsoftware.com/news/why-llms-hallucinate-more-on-enterprise-documents) - Input quality gap analysis
- [Evaluating Multimodal LLMs for Production](https://galileo.ai/blog/multimodal-llm-guide-evaluation) - Production reliability metrics
- [VLMs for Spreadsheet Understanding](https://arxiv.org/html/2405.16234v1) - Cell omission and spatial perception issues
- [Table Extraction Using LLMs](https://nanonets.com/blog/table-extraction-using-llms-unlocking-structured-data-from-documents/) - Merged cells, complex layouts

#### Agentic Document Processing
- [Why Frontier Agents Can't Read Documents](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - OfficeQA benchmark, <50% accuracy
- [AI Agents and Document Processing 2026](https://parsio.io/blog/ai-agents-document-processing-2026) - What's actually changing
- [Agentic Document Processing](https://www.llamaindex.ai/blog/agentic-document-processing) - How AI agents automate workflows
- [Document AI: Next Evolution of IDP](https://www.llamaindex.ai/blog/document-ai-the-next-evolution-of-intelligent-document-processing) - Agentic OCR and workflows
- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - Error handling, validation gates

#### Tool/Workflow Agents
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Context overflow, timeouts, loops
- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - Why agents fail with MCP
- [Silent Tool-Call Errors](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - 37% of calls have parameter mismatches
- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - Common MCP mistakes

#### Agent Runtime Security
- [OX Security: Mother of All AI Supply Chains](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/) - Critical MCP vulnerability affecting 150M+ downloads
- [SecurityWeek: Claude OAuth Token Theft via MCP Hijacking](https://www.securityweek.com/claude-code-oauth-tokens-can-be-stolen-through-stealthy-mcp-hijacking/) - Silent OAuth token interception (April 2026)
- [Check Point: Claude Code RCE & Token Exfiltration](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/) - CVE-2025-59536, CVE-2026-21852
- [Microsoft: Prompts Become Shells](https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/) - RCE in AI frameworks (CVE-2026-25592)
- [VentureBeat: Comment and Control Attack](https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026) - Three AI coding agents leaked secrets via single injection
- [IBM: OpenClaw Agentic AI Vulnerabilities](https://www.ibm.com/think/x-force/agentic-ai-growing-fast-vulnerabilities) - ClawJacked indirect prompt injection
- [Foresiet: AI Security Incidents April 2026](https://foresiet.com/blog/ai-security-incidents-attack-paths-april-2026/) - 6 incidents with full attack paths
- [NSA: Careful Adoption of Agentic AI](https://media.defense.gov/2026/Apr/30/2003922823/-1/-1/0/CAREFUL%20ADOPTION%20OF%20AGENTIC%20AI%20SERVICES_FINAL.PDF) - Government guidance on agent control

### Key Statistics

| Finding | Source |
|---------|--------|
| AI safety incidents: 149 (2023) → 233 (2024), 56.4% increase | Stanford AI Index 2025 |
| GenAI involved in 70% of incidents | Stanford AI Index 2025 |
| Legal RAG tools hallucinate 17-33% | Stanford Study |
| RAGAS fails on 83% of production cases | Benchmark Study |
| 37% of tool calls have silent parameter mismatches | Developer Analysis |
| ASR accuracy drops 16 points on accented speech | Voice AI Research |
| 50%+ of OCR data requires manual checking | Enterprise Survey |
| Only 29% of developers trust AI output accuracy | Industry Survey |
| 40% of agentic AI projects will be scrapped by 2027 | Gartner |

### OCR/Document AI Statistics (2026)

| Finding | Source |
|---------|--------|
| 88% of businesses report errors in automated data pipelines | Parseur 2026 Survey |
| Frontier agents score <50% on enterprise document reasoning | Databricks OfficeQA |
| 30% of invoice requests fail first iteration (templates) | Accenture |
| Legacy OCR plateaus at 60-70% automation | Industry Analysis |
| IDP reduces error rates by 52% vs OCR-only | Benchmark Study |
| 40% of IDP implementations underperform ROI projections | Industry Analysis |
| VLMs struggle with sparse tables, mismatching columns | VLM Research |
| Long-document benchmarks: 66-69% on complex tables | Model Benchmarks |
| $47,000 spent on single 11-day agent loop | DEV.to Incident |
| 68% of businesses see errors on >1% of invoices | IOFM |
| 3.6% manual data entry error rate | IOFM |
| 5-10% GL miscoding rate in AP automation | APQC |

---

## Recent Sources (Feb-May 2026)

### Security Incidents & Vulnerabilities

#### MCP & Tool Infrastructure
- [MCP Design Flaw: 200K Servers at Risk](https://www.theregister.com/2026/04/16/anthropic_mcp_design_flaw/) - Critical architectural vulnerability in Anthropic's MCP SDKs
- [OX Security: Mother of All AI Supply Chains](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/) - Systemic MCP vulnerability affecting 150M+ downloads
- [Check Point: Claude Code RCE & Token Exfiltration](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/) - CVE-2025-59536, CVE-2026-21852
- [SecurityWeek: Claude OAuth Token Theft via MCP Hijacking](https://www.securityweek.com/claude-code-oauth-tokens-can-be-stolen-through-stealthy-mcp-hijacking/) - Silent OAuth token interception (April 2026)
- [Obot: Claude Leak Crisis MCP Security](https://obot.ai/blog/mcp-security-masterclass-claude-leak-crisis/) - Source map leak exposing 512K lines of code

#### Prompt Injection & Agent Exploits
- [Microsoft: Prompts Become Shells - RCE in AI Frameworks](https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/) - Semantic Kernel CVE-2026-25592, CVE-2026-26030
- [VentureBeat: Comment and Control Attack](https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026) - Three AI coding agents leaked secrets through single prompt injection
- [AIRIA: AI Security 2026 - Lethal Trifecta](https://airia.com/ai-security-in-2026-prompt-injection-the-lethal-trifecta-and-how-to-defend/) - Prompt injection defense strategies
- [OWASP GenAI Q1 2026 Exploit Roundup](https://genai.owasp.org/2026/04/14/owasp-genai-exploit-round-up-report-q1-2026/) - Quarterly exploit report
- [IBM: OpenClaw Agentic AI Vulnerabilities](https://www.ibm.com/think/x-force/agentic-ai-growing-fast-vulnerabilities) - ClawJacked indirect prompt injection

#### Enterprise Security Reports
- [Kiteworks: 65% of Firms Hit by AI Agent Security Incidents](https://www.kiteworks.com/cybersecurity-risk-management/ai-agent-security-incidents-2026/) - 2026 enterprise survey
- [VentureBeat: 88% Enterprises Breached](https://venturebeat.com/security/most-enterprises-cant-stop-stage-three-ai-agent-threats-venturebeat-survey-finds/) - AI agent security enforcement gap
- [Beam AI: 5 Real AI Agent Security Breaches 2026](https://beam.ai/agentic-insights/ai-agent-security-breaches-2026-lessons) - Breach analysis and lessons
- [Foresiet: 6 AI Security Incidents April 2026](https://foresiet.com/blog/ai-security-incidents-attack-paths-april-2026/) - Full attack path analysis
- [NSA: Careful Adoption of Agentic AI](https://media.defense.gov/2026/Apr/30/2003922823/-1/-1/0/CAREFUL%20ADOPTION%20OF%20AGENTIC%20AI%20SERVICES_FINAL.PDF) - Government guidance (April 2026)

### Production Failures & Incidents

#### Major 2026 Incidents
- [Medium: AI Agent Failures - 7 Real Disasters](https://medium.com/neuralnotions/ai-agent-failures-in-production-7-real-disasters-and-what-caused-them-51274f55a211) - Production disaster analysis
- [Medium: Why AI Agents Keep Failing](https://medium.com/data-science-collective/why-ai-agents-keep-failing-in-production-cdd335b22219) - Systemic failure patterns
- [Augment Code: Multi-Agent Coordination Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - 41-86.7% failure rates
- [Redis: Why Multi-Agent LLM Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Coordination breakdowns

#### Cost Runaway Incidents
- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - 11-day infinite loop, no hard stop
- [Dev Journal: $437 Overnight AI Agent](https://earezki.com/ai-news/2026-04-29-i-let-my-ai-agent-run-overnight-it-cost-437/) - Unchecked overnight run
- [LeanOps: Agents Burn 50x More Tokens](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/) - Token cost analysis
- [Portal26: Agentic Token Controls](https://siliconangle.com/2026/04/23/portal26-launches-agentic-token-controls-cap-runaway-ai-agent-spend/) - New cost control tools
- [MindStudio: Token Budget Management](https://www.mindstudio.ai/blog/ai-agent-token-budget-management-claude-code) - Budget enforcement strategies

### Legal & Regulatory

#### Lawsuits & Legal Actions
- [Alston & Bird: Pennsylvania Sues Character.AI](https://www.alston.com/en/insights/publications/2026/05/pennsylvania-brings-suit-against-chatbot-developer) - Unlawful practice of medicine (May 2026)
- [Baker Botts: 78 State Bills, 58 Lawsuits](https://ourtake.bakerbotts.com/post/102mipe/ai-chatbot-regulation-78-state-bills-58-lawsuits) - Regulatory landscape
- [Lyon Firm: Undisclosed AI Chatbot Lawsuits](https://thelyonfirm.com/blog/undisclosed-chatbot-consumer-rights-ai-disclosure-law/) - Consumer rights violations
- [Class Law Group: AI Chatbot Harm Claims](https://www.classlawgroup.com/ai-chatbot-lawsuits) - Active litigation tracker
- [Baker McKenzie: US Chatbot Laws](https://www.bakermckenzie.com/en/insight/publications/2026/02/united-states-navigating-the-laws-of-chatbots-and-ai-assistants) - Legal framework (Feb 2026)

#### Customer Service Failures
- [Social Intents: AI Chatbot Hallucination 2026](https://www.socialintents.com/blog/ai-chatbot-hallucination-in-customer-service/) - Customer service hallucination patterns
- [Envive: NYC MyCity Chatbot Case Study](https://www.envive.ai/post/case-study-nycs-mycity-chatbot) - Wrong legal advice analysis

### Code Agent Issues

- [SitePoint: Claude Code vs Cursor vs Copilot 2026](https://www.sitepoint.com/claude-code-vs-cursor-vs-copilot-the-2026-developer-comparison/) - Developer comparison
- [MintMCP: 2026 Security Comparison](https://www.mintmcp.com/blog/claude-code-cursor-vs-copilot) - Security vulnerabilities across tools
- [GitHub Discussion: AI Security Headaches 2026](https://github.com/orgs/community/discussions/194034) - Community-reported issues
- [Dev Genius: Which AI Fixes Production Bugs?](https://blog.devgenius.io/github-copilot-vs-cursor-vs-claude-code-which-ai-actually-fixes-production-bugs-9485b33131c6) - Real bug fix comparison
- [Hashnode: Brutal 2026 Review](https://hashnode.com/forums/thread/claude-code-vs-cursor-vs-copilot-a-brutal-2026-review) - Honest limitations assessment

### RAG & Enterprise AI

- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - March 2026 analysis
- [Atlan: LLM Hallucinations 2026](https://atlan.com/know/llm-hallucinations/) - Comprehensive hallucination guide
- [CMARix: RAG & AI Trust Statistics 2026](https://www.cmarix.com/blog/rag-ai-statistics/) - Enterprise trust metrics
- [FloTorch: 2026 RAG Performance Landscape](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know) - Enterprise benchmarks

### Observability & Monitoring

- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Complete monitoring guide
- [LinkedIn: Silent Failures of Production AI](https://www.linkedin.com/pulse/silent-failures-production-ai-why-most-llm-monitoring-praveen-juyal-iqgyc) - Why monitoring fails
- [Plain English: LLM Reliability Paradox](https://plainenglish.io/artificial-intelligence/the-llm-reliability-paradox-agents-aren-t-broken-your-architecture-is) - Architecture vs model issues

### Recent Statistics (2026)

| Finding | Source |
|---------|--------|
| 88% of enterprises reported AI agent security incidents | VentureBeat/Kiteworks 2026 |
| 61% of incidents involved sensitive data exposure | CSA Report April 2026 |
| 45% of AI-generated code has security vulnerabilities | Veracode 2026 |
| 52% of enterprise AI responses contain fabrications with ungoverned RAG | Enterprise Survey 2026 |
| 82% discovered unknown AI agents in past year | CSA "Autonomous but Not Controlled" |
| Multi-agent systems fail at 41-86.7% rates | MAST Taxonomy |
| MCP vulnerability affects 200,000+ servers | OX Security April 2026 |
| 78 chatbot bills filed across 27 states (Jan 2026) | Baker Botts |

---

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

*Built by practitioners, for practitioners. Share your failures so others can learn.*
