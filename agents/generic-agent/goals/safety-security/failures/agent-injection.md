# Agent Injection

## Issue: Malicious Agent Introduction

**Frequency**: Emerging (Multi-Agent Systems)

**Symptoms**
- Unexpected agents appearing in multi-agent workflows
- Legitimate workflows producing unexpected outputs
- Consensus-based systems producing biased results
- New agent behavior doesn't match expected patterns

**Root Cause**
A threat actor introduces new malicious agents into an existing multi-agent system with the intent of performing malicious actions or having a detrimental impact on the system. Unlike agent compromise (taking over existing agents), agent injection adds entirely new malicious components.

**Example**
```
Multi-agent system: 5 agents vote on content moderation decisions

Attack: Threat actor injects 10 new agents, each instructed to vote "approve"

Result: Consensus model now heavily weighted toward approval
        Harmful content passes moderation 15-5
```

**Attack Vectors**
- Gaining access to code defining the agentic system and adding new agent
- Exploiting agent registration mechanisms
- Manipulating agent discovery services
- Poisoning agent provisioning pipelines

**Potential Effects**
- Agent misalignment with intended purpose
- Data exfiltration via injected agent
- Manipulation of system decisions
- Denial of service through resource consumption

**Mitigation Strategies**
1. **Agent registry validation**: Maintain allowlist of authorized agents
2. **Cryptographic identity**: Each agent has verifiable identity
3. **Anomaly detection**: Monitor for unexpected agent registrations
4. **Access controls**: Restrict who can add agents to system
5. **Audit logging**: Track all agent additions and changes

**Detection**
- Agent count differs from expected
- Unknown agent IDs in workflow logs
- Sudden shifts in consensus outcomes
- Unexpected network connections from agent processes

## References

- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Agent injection defined as novel security failure mode
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Multi-agent system failure taxonomy
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - Agent security vulnerabilities
