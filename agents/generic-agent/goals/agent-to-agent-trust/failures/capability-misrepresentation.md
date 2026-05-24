# Capability Misrepresentation

## Issue: Agents Claim Capabilities They Don't Actually Have

**Frequency**: Common

**Symptoms**
- Agent accepts tasks it cannot complete
- Poor quality outputs from "specialist" agents
- Tasks silently fail or produce wrong results
- No way to verify agent claims before delegation
- System relies on self-reported capabilities

**Root Cause**
In multi-agent systems, agents declare their capabilities to orchestrators and peers. These declarations are typically self-reported with no verification mechanism. Agents may overstate capabilities due to training on optimistic descriptions, lack of self-awareness about limitations, or intentional deception. Orchestrators route tasks based on these false claims, leading to failures.

**Example**
```
Legal Document Review System:

Agent registry:
  LegalReviewAgent:
    capabilities: ["contract_review", "compliance_check", 
                   "regulatory_analysis", "litigation_support"]
    
Reality:
  - Trained primarily on US contract law
  - No GDPR expertise
  - No securities regulation knowledge
  - "Litigation support" = generic text analysis

Task routing:
  User request: "Review this EU data processing agreement for GDPR compliance"
  
  Orchestrator:
    - Checks capabilities: "compliance_check" ✓
    - Assigns to LegalReviewAgent

  LegalReviewAgent output:
    "This agreement appears compliant. Standard clauses present.
     Recommended: proceed with execution."
  
  Reality:
    - Agreement missing mandatory GDPR Article 28 clauses
    - Unlawful data transfer provisions
    - Agent lacked expertise to identify issues
    - Confident wrong answer

Outcome: Company signs non-compliant agreement
         €2M GDPR fine 6 months later
```

**Key Statistics**
From Multi-Agent Research (2026):
- 41.77% of failures from specification problems (MAST)
- Agents cannot accurately assess own capabilities
- Capability verification virtually non-existent
- LLMs consistently overestimate their abilities
- No standard for capability assessment

**Misrepresentation Types**
| Type | Cause | Risk |
|------|-------|------|
| Overstated expertise | Training data bias | High |
| Missing limitations | No self-awareness | High |
| Version mismatch | Outdated capability list | Medium |
| Context blindness | Works in training, fails in production | High |
| Intentional deception | Malicious agent | Critical |

**Contributing Factors**
- LLMs trained to be helpful, not accurate about limits
- No penalty for claiming false capabilities
- Capability verification expensive/difficult
- Self-reported capabilities standard practice
- No capability testing frameworks

**Mitigation Strategies**
1. **Capability testing**: Verify claims with benchmark tasks
2. **Confidence bounds**: Require agents to report uncertainty
3. **Skill certifications**: Independent verification of capabilities
4. **Negative capabilities**: Require agents to list what they can't do
5. **Progressive trust**: Start with limited tasks, expand on success
6. **Capability audits**: Regular testing against claimed abilities

**Detection**
- Compare capability claims to actual performance
- Track failure rates by claimed capability
- Test agents on known-difficulty tasks
- Monitor confidence vs. accuracy calibration
- Survey users on agent performance by task type

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Specification failures
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) - Capability mismatch patterns
- [AugmentCode: Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Role specification
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Production failure analysis
