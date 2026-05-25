# Feedback Not Incorporated

## Issue: Human Corrections Ignored in Subsequent Agent Decisions

**Frequency**: Common

**Symptoms**
- Agent repeats corrected mistakes
- Human feedback acknowledged but not applied
- Corrections effective for one turn, forgotten next
- Feedback stored but not retrieved
- Same errors require repeated correction

**Root Cause**
Humans provide corrections, clarifications, or guidance, but the agent fails to incorporate this feedback into future decisions. Feedback may be acknowledged in the moment but not persisted, stored but not retrieved, or retrieved but not weighted appropriately. This is particularly problematic in multi-turn or multi-session interactions where context about prior corrections is lost.

**Example**
```
Session 1:
  User: "Summarize Q3 revenue"
  Agent: "Q3 revenue was $10.2M"
  User: "That's wrong - it's $12.2M. The report you're using is outdated."
  Agent: "I apologize. Q3 revenue was $12.2M."
  Feedback logged: "User corrected revenue figure"

Session 2 (next day):
  User: "What was Q3 revenue again?"
  Agent: "Q3 revenue was $10.2M"  ← Same wrong answer
  User: "I told you yesterday it was $12.2M!"
  
Investigation:
  - Feedback was logged but not indexed
  - No retrieval mechanism for prior corrections
  - Agent re-used same outdated source
  - No update to underlying knowledge
  
Impact:
  - User frustration
  - Repeated correction effort
  - Trust erosion
  - Wrong data in subsequent analysis
```

**Key Statistics**
From LLM Behavior Research (2026):
- Only 12% of corrections persist across sessions
- 67% of users repeat same feedback 3+ times
- Feedback incorporation drops 80% after context window
- 45% of feedback is logged but never retrieved
- Users abandon correction after 4 failed attempts

**Feedback Loss Points**
| Point | Description | Mitigation |
|-------|-------------|------------|
| Not logged | Feedback never recorded | Automatic logging |
| Not indexed | Logged but not searchable | Semantic indexing |
| Not retrieved | Indexed but not queried | Retrieval triggers |
| Not weighted | Retrieved but ignored | Priority weighting |
| Not persisted | Applied once, lost | Long-term memory |

**Contributing Factors**
- No persistent memory across sessions
- Feedback stored separately from knowledge
- Context window limits
- No retrieval-augmented correction
- Implicit feedback not detected

**Mitigation Strategies**
1. **Feedback persistence**: Store corrections in retrievable memory
2. **Semantic indexing**: Index feedback by topic for retrieval
3. **Proactive retrieval**: Query prior feedback before answering
4. **Source updating**: Update underlying data when corrected
5. **Feedback weighting**: Prioritize human corrections over base knowledge
6. **Correction confirmation**: Verify feedback was incorporated

**Detection**
- Track repeated corrections for same error
- Monitor feedback-to-behavior change rate
- Compare agent responses pre/post feedback
- Survey user satisfaction with correction handling
- Audit feedback retrieval rates

## References

- [Anthropic: Constitutional AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) - Learning from feedback
- [OpenAI: InstructGPT](https://openai.com/research/instruction-following) - Human feedback incorporation
- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Feedback loops
- [LangChain: Memory](https://python.langchain.com/docs/modules/memory/) - Conversation memory patterns
