# Inherited Errors

## Issue: Agent Propagates Errors from Sources or Tools

**Frequency**: Common

**Symptoms**
- Tool returns incorrect data, agent passes it through
- Source document contains error, agent repeats it
- Upstream agent makes mistake, downstream agent doesn't catch it

**Root Cause**
Agents trust their inputs. If a tool, document, or another agent provides incorrect information, the agent typically won't question it.

**Example**
```
Tool response: { "user_balance": 1000 }  // Database bug, actual: 10000

Agent: "Your current balance is $1,000"

User: "That's wrong, I deposited $9,000 yesterday"

Agent: "According to my records, your balance is $1,000"  // Confidently wrong

Result: Agent trusts tool over user, provides incorrect information
```

**Mitigation Strategies**
1. **Cross-validation**: Verify critical data from multiple sources
2. **Sanity checks**: Flag values outside expected ranges
3. **User feedback integration**: Allow corrections to tool outputs
4. **Source quality scoring**: Weight information by source reliability
5. **Uncertainty propagation**: Track confidence through pipeline
6. **Human-in-the-loop**: Verify high-stakes information before acting

**Detection**
- Track error rates by source/tool
- Monitor user corrections
- Compare tool outputs to ground truth
- Audit multi-step reasoning chains

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Research on error propagation in multi-agent systems
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Analysis of inherited error patterns in AI agent pipelines
