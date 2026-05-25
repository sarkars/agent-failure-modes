# Lost Decision Context

## Issue: Cannot Understand Why Agent Made Specific Decisions

**Frequency**: Common

**Symptoms**
- Agent output correct but reasoning unknown
- Cannot explain decision to stakeholders
- Policy compliance unverifiable
- Cannot distinguish bug from feature
- Improvement impossible without understanding

**Root Cause**
Agents make decisions through complex reasoning processes that aren't captured in outputs. The final action is logged, but the chain of reasoning—what information was considered, what alternatives were evaluated, what trade-offs were made—is lost. This makes it impossible to understand, explain, or improve agent decision-making.

**Example**
```
Loan Application Decision:

Output logged:
  {
    "decision": "DENIED",
    "application_id": "APP-12345",
    "timestamp": "2026-04-15T10:30:00Z"
  }

What's missing:
  - Which factors contributed to denial?
  - What was the confidence level?
  - Were there borderline considerations?
  - What would have changed the decision?
  - Did the agent consider all required factors?
  - Was this consistent with similar applications?

Customer complaint:
  "Why was I denied? I have good credit."

Investigation:
  - Can't explain the specific denial
  - Can't verify discrimination didn't occur
  - Can't check if policy was followed
  - Can't improve decision quality

Regulatory inquiry:
  "Provide the factors that led to this adverse action"
  
Response: "We don't have that information"
          → Compliance violation
```

**Key Statistics**
From AI Governance Research (2026):
- Explainability requirements in EU AI Act, CCPA, ECOA
- Most agent frameworks don't capture reasoning
- "Right to explanation" increasingly enforced
- Unexplainable decisions create legal liability
- Trust requires understanding, not just accuracy

**Lost Context Types**
| Context | Importance | Typical Capture |
|---------|------------|-----------------|
| Input factors considered | Critical | Rarely |
| Weights/importance | High | Almost never |
| Alternatives evaluated | High | Rarely |
| Uncertainty/confidence | Medium | Sometimes |
| Policy rules applied | Critical | Sometimes |
| Similar case comparisons | Medium | Rarely |

**Contributing Factors**
- LLM reasoning is implicit in weights
- Chain-of-thought not always captured
- Structured logging not implemented
- Focus on outcomes, not process
- Explainability seen as optional

**Mitigation Strategies**
1. **Reasoning capture**: Log chain-of-thought explicitly
2. **Factor attribution**: Record which inputs influenced output
3. **Confidence logging**: Capture uncertainty in decisions
4. **Alternative tracking**: Log options considered
5. **Policy checkpoint logging**: Record rule evaluations
6. **Explanation generation**: Produce human-readable rationale

**Detection**
- "Why did it do that?" question frequency
- Explanation request fulfillment rate
- Compliance audit findings
- Stakeholder satisfaction with explanations
- Decision appeal resolution time

## References

- [EU AI Act](https://artificialintelligenceact.eu/) - Explainability requirements
- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Transparency requirements
- [Responsible AI Labs: AI Safety 2024](https://responsibleailabs.ai/knowledge-hub/articles/ai-safety-incidents-2024) - Explainability failures
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - Accountability gaps
