# Stale Training-Corpus Tone Rule Overrides Live Brand-Voice-Guideline Update

## Issue: A Content-Generation Agent Answers Questions About the Brand's Permitted Tone, Person, or Phrasing Conventions (e.g., Whether Second-Person "You" Address Is Allowed, Whether Exclamation Points Are Permitted, Whether the Brand Name Should Be Used as a Verb) from General Stylistic Patterns Absorbed During Pretraining or from an Early, Now-Superseded Memory of the Brand Voice, Instead of Calling the Live Brand-Voice-Guideline Tool It Has Available, Producing Content That Violates a Recently Updated Rule

**Frequency**: Occasional

**Symptoms**
- Generated copy violates a brand-voice rule that was updated within the last few weeks, while complying with the prior version of that same rule
- The agent had a live brand-voice-guideline lookup tool available for the session but the trace shows no call to it before the violating copy was drafted
- When asked directly to consult the guideline tool, the agent retrieves the current rule correctly and flags its own earlier draft as non-compliant
- The violated rule is disproportionately one that recently changed direction (e.g., a previously discouraged convention was newly permitted, or vice versa) rather than a long-stable rule
- Editors note the agent "used to get this right" before a recent brand-voice update, suggesting the agent is anchored to an earlier guideline state rather than the current one

**Example**
```
Brand-voice guideline is updated this quarter to newly permit casual contractions and a single exclamation point per
paragraph for social captions, reversing a year-old "no exclamation points, no contractions" rule
Agent is asked to draft a product-launch caption and has a live brand-voice-guideline lookup tool available
Agent drafts the caption in the old, more formal register -- no contractions, no exclamation points -- without calling
the guideline tool first
Editor flags the caption as "stiff" relative to recent approved captions; on review, the agent's draft matches the
guideline as it stood roughly a year ago, before the update, not the current permitted style
When the editor explicitly instructs the agent to "check the current brand-voice guideline before redrafting," the agent
calls the tool, retrieves the updated rule, and produces a compliant caption on the second attempt
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey research on LLM agent hallucination identifies reliance on memorized, static training-time knowledge in place of an available live tool result as a distinct and recurring failure mechanism, separate from outright fabrication | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds agents often default to internally generated answers in situations where a tool call would resolve ambiguity, particularly when the agent already has a plausible-sounding answer available from prior training or context | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Execution-provenance research for LLM agents argues that without traceable evidence linking a stylistic or factual claim to an actual tool call, there is no way to distinguish a grounded current answer from one based on outdated memorized context | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- The agent treats brand-voice tone rules as stable background knowledge rather than as a live, versioned policy that can change between sessions
- No standing instruction requiring a guideline-tool call specifically when drafting copy in a category (captions, taglines) where the guideline was recently revised
- The agent's own prior turns or session memory of the brand voice, formed before the update, are weighted similarly to a fresh tool call would be, with no explicit recency signal distinguishing them
- No automated diff alert notifies the content pipeline when the brand-voice guideline changes, so there is no trigger forcing a guideline-tool call on the next draft

---

## Mitigation Strategies

1. **Mandatory Guideline Call Before Tone-Sensitive Drafts**: Require an explicit live brand-voice-guideline tool call before drafting any copy in a category covered by a tone, person, or punctuation rule, regardless of whether the agent believes it already knows the rule
2. **Guideline-Change Trigger**: When the brand-voice guideline is updated, automatically flag the next N drafts in affected content categories for mandatory guideline-tool verification rather than relying on the agent to notice unprompted
3. **Recency-Tagged Guideline Snapshot**: Pass the guideline's last-updated timestamp alongside its content in tool results so the agent can recognize when its own background assumption might predate the current rule
4. **Diff Against Current Guideline Before Publish**: Run an automated check comparing generated copy's tone markers (contraction use, punctuation, person) against the current guideline tool's output before publication, independent of whether the agent called the tool during drafting

### Metrics
- Rate of published copy violating a brand-voice rule that was updated within the prior 90 days
- Number of drafts produced without a corresponding brand-voice-guideline tool call in the session trace
- Time lag between a guideline update and the first agent-drafted piece that correctly reflects it

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Draft violates recently updated rule | Generated copy fails a tone/style rule changed within the last 90 days | P2 | Block publication; require guideline-tool-verified redraft |
| No guideline call before tone-sensitive draft | Draft in a tone-governed category produced with no guideline-tool call in trace | P3 | Flag for manual review; reinforce mandatory-call instruction |
| Post-update violation spike | Rate of guideline violations rises in the two weeks following a guideline update | P2 | Trigger mandatory verification mode for affected categories |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
