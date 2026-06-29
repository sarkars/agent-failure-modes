# Earlier-Established Negative-Keyword Constraint Lost from Context in Long Keyword-Research Session

## Issue: During an Extended Single-Session SEO Content-Planning Conversation Covering Dozens of Target Pages, an Editor's Early Instruction That a Specific Keyword Cluster Must Be Excluded (Because It Cannibalizes an Existing High-Ranking Page or Conflicts With a Paid-Search Exclusion List) Falls Out of the Agent's Effective Context as the Session Grows, and the Agent Later Recommends or Drafts Content Targeting the Excluded Cluster as if the Constraint Had Never Been Stated

**Frequency**: Occasional

**Symptoms**
- A keyword cluster explicitly excluded near the start of a long planning session reappears as a recommended target 40-60 turns later in the same session
- The agent's later recommendation shows no awareness that the cluster was previously discussed and rejected, treating it as a fresh, unconstrained suggestion
- Re-stating the exclusion mid-session corrects the next few recommendations, but the constraint fades again as the session continues to grow
- The dropped constraint is reliably present near the beginning or just past the middle of the transcript, not at the very end, when the transcript is inspected after the fact
- Editors report having to repeat the same exclusion rule multiple times across a single working session as the apparent cause

**Example**
```
Turn 3 of a content-planning session: editor tells the agent "Do not target anything in the 'apartment moving checklist' cluster --
that traffic is already owned by /guides/moving-checklist and we don't want to cannibalize it"
Turns 4-45: agent and editor work through unrelated keyword clusters for 40+ turns, building out a content calendar
Turn 52: editor asks the agent to suggest five more content ideas to fill out the quarter's calendar
Agent recommends "Ultimate Apartment Moving Checklist for Renters" targeting the exact excluded cluster, with no
acknowledgment that this was ruled out 49 turns earlier
Editor catches the conflict only because they happen to recognize the title; a less familiar reviewer approves it,
and the new page is later found splitting search traffic and rankings with the existing guide
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Transformer-based language models exhibit a measurable drop in recall and use of information placed in the early-to-middle portion of a long context window relative to information near the start or end, even when the relevant information is fully present in context | [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) |
| Surveyed agent failure taxonomies identify loss of earlier-established constraints across an extended interaction as a distinct agent-environment failure mode rather than a model-capability gap that shorter prompts would avoid | [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) |
| Broader failure-mode analysis of LLM systems documents context-retention degradation as a recurring root cause behind agents silently violating instructions given earlier in the same session | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |

**Contributing Factors**
- The exclusion was stated once, in free text, early in the session, with no mechanism re-injecting it into the agent's active context as the conversation grows
- No structured, persistent "session constraints" list separate from the raw transcript that the agent is required to re-check before each new recommendation
- The agent's recommendation-generation step treats each new request as largely independent, re-deriving suggestions from the topic and general SEO heuristics rather than consulting a running constraint list
- Long planning sessions are treated as a single continuous conversation rather than being periodically summarized and restarted with a compact, explicit constraint set carried forward

---

## Mitigation Strategies

1. **Persistent Constraint Ledger**: Maintain a structured, separately-tracked list of session-level exclusions and constraints that is re-injected into the prompt or system context before every new recommendation, rather than relying on the raw transcript history
2. **Periodic Session Compaction**: For long planning sessions, periodically summarize established constraints into a compact carryover block and restart the working context from that summary rather than letting the full transcript grow unbounded
3. **Pre-Recommendation Constraint Check**: Require the agent to explicitly check each new keyword recommendation against the current constraint ledger and state the check result before presenting the recommendation
4. **Cross-Reference Against Existing Site Map**: Independently validate any new content recommendation against the current sitemap and known cannibalization-risk list via a tool call, rather than relying solely on the conversation's memory of prior exclusions

### Metrics
- Rate of recommended keywords/clusters that match a previously stated exclusion when checked against the constraint ledger
- Average transcript length (turns or tokens) at which previously stated constraints stop being honored in testing
- Number of mid-session constraint restatements required per planning session

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Excluded cluster re-recommended | New recommendation matches an entry in the session's constraint ledger | P2 | Block recommendation; surface ledger entry to editor for confirmation |
| Constraint ledger empty in long session | Session exceeds turn-length threshold with no constraint ledger populated despite exclusions stated in transcript | P3 | Flag session for ledger backfill; audit constraint-capture step |
| Repeated manual restatement | Same constraint restated by a human user more than once in a single session | P3 | Investigate context-retention gap; consider session compaction |

---

## References

- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
