# Failure to Ask for Clarification

## Issue: Agent Proceeds Despite Ambiguity

**Frequency**: Common (6.8% of MAS failures)

**Symptoms**
- Agent makes assumptions instead of asking
- Ambiguous requirements interpreted arbitrarily
- Different agents have different interpretations
- Task fails due to misunderstood requirements

**Root Cause**
Agent fails to ask for clarification when facing ambiguous or incomplete information. Instead of seeking clarity, the agent proceeds with assumptions that may be incorrect, leading to task failures that could have been avoided.

**Example**
```
Task: "Update the customer's address"

Ambiguity: Which customer? Which address field? What's the new value?

Agent behavior:
Agent: "I'll update the address now."
       [Searches for most recent customer]
       [Updates shipping address with billing address]
       "Done! Address has been updated."

Expected behavior:
Agent: "I need clarification:
       1. Which customer should I update?
       2. Which address (shipping or billing)?
       3. What is the new address?"

Result: Wrong customer's address changed incorrectly
```

**Key Statistics**
From MAST study of 1642 MAS traces:
- Failure to ask for clarification accounts for 6.8% of failures
- Part of "Inter-Agent Misalignment" category (32.3% total)
- Often cascades into larger task failures

**Clarification Failure Types**
- **Assumption making**: Guessing instead of asking
- **Partial understanding**: Proceeding with incomplete info
- **Overconfidence**: Believing interpretation is correct
- **Efficiency bias**: Avoiding "unnecessary" questions

**Contributing Factors**
- Training bias toward being "helpful" immediately
- No clear protocol for when to seek clarification
- Pressure to complete tasks quickly
- Unclear escalation paths for ambiguity
- Lack of uncertainty awareness

**Mitigation Strategies**
1. **Ambiguity detection**: Identify unclear requirements
2. **Clarification prompts**: Encourage asking questions
3. **Required fields**: Define mandatory information
4. **Confidence thresholds**: Ask when uncertain
5. **Clarification templates**: Structured question formats

**Detection**
- Actions taken with incomplete information
- Assumptions stated without verification
- Different agents interpreting same request differently
- User corrections after agent's interpretation

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Failure mode 2.2: Fail to Ask for Clarification (6.8%)
- [Air Canada Chatbot Lawsuit](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416) - Assumptions leading to liability
- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Misinterpretation of instructions
