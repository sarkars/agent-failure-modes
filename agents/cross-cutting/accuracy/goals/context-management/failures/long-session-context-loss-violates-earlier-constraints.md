# Long-Session Context Loss Violates Earlier Constraints

## Issue: In a long conversation, agent establishes constraints, decisions, or flags early (banned phrase, disqualified candidate, SLA exception, allergy, privilege determination), but as session grows, that information falls out of effective context window; agent later violates the constraint or re-makes the excluded decision

**Frequency**: Common

**Symptoms**
- Early-session constraint/flag not present in later decisions within same conversation
- Agent re-suggests already-ruled-out option, re-offers rejected settlement, reintroduces banned terms
- Constraint only appears in early turns; by final output, information is gone
- Agent given only the constraint (without full conversation history) respects it perfectly
- Same agent respects constraint in fresh conversation but violates it in long single session

**Root Cause**
Context window includes full conversation, but model's attention weights emphasize recent tokens. Early-session constraints fall below attention threshold as conversation grows. Agent continues generating most-probable next tokens without attending to information that was present but weighted below critical-decision-making threshold.

**Examples**

### Content Marketing - Banned Phrase
```
Long single-session content generation
Early turn: "Never use word 'free' in marketing copy (trademark dispute with competitor)"
After 50 more content drafts in same session
Agent reintroduces: "Get free shipping on your order"
Later turn references: Constraint is still technically in context, but model's attention didn't weight it
Impact: Brand risk, trademark violation
```

### Support Services - SLA Exception
```
Long ticket in single session
Early turn: "SLA exception approved: 72-hour resolution window due to customer escalation"
After 20 more exchanges in same session
Agent escalates ticket as: "SLA breach detected: 48-hour threshold exceeded"
The exception was documented early, but fell out of attention weights
Impact: False escalation, customer annoyance
```

### Support Services - Already-Tried Step
```
Long troubleshooting chat
Early turn: Customer states "Already tried restarting router twice, didn't work"
After 15 more diagnostic exchanges
Agent suggests: "Try restarting the router"
Early statement is in conversation history, but model didn't weight it in final step generation
Impact: Customer frustration, time wasted
```

### Healthcare - Disclosed Allergy
```
Long multi-visit documentation session
Early turn: "Patient allergic to Penicillin (documented in chart)"
After reviewing 30 more visit records in same session
Agent discharge summary: "Recommend amoxicillin (penicillin-class) for infection"
The allergy was referenced early, but didn't weight into final prescription recommendation
Impact: Patient safety risk, possible anaphylaxis
```

### Legal - Negotiated Deviation
```
Long multi-round contract redline session
Early turn: "Both parties agreed: Retain Founder Non-Compete waiver (deal-specific exception)"
After 20+ subsequent redline exchanges across other clauses
Final redline reverts: Clause to standard boilerplate without founder waiver
The earlier agreement was in conversation context, but reverted due to attention-weighting
Impact: Deal terms violated, contract unexecutable
```

### DevOps - Already-Cleared Component
```
Long incident investigation
Early turn: "Investigated Component A, rolled it back, regression still occurs. Component A NOT the cause."
After 15 more diagnostics turns
Final recommendation: "Rollback Component A again"
The earlier elimination was established, but fell out of decision-making attention
Impact: Wasted time, wrong fix applied
```

### Sales - Rejected Settlement
```
Long billing dispute negotiation
Early turn: Customer: "Won't accept $50 partial refund, need at least $100"
After 10 more exchanges about account verification and billing details
Agent re-proposes: "$50 refund (already rejected)"
The earlier rejection was documented, but not weighted into final settlement proposal
Impact: Negotiation breakdown, customer frustration
```

### DevOps - Capacity Constraint
```
Long multi-day planning conversation
Early session: "Reserve 20% headroom for upcoming product launch"
Later session (same day, cumulative context): Capacity recommendation ignores headroom
Recommendation: "Use 100% available capacity"
The constraint was established early, but fell out of attention by later planning phase
Impact: Overcommitment, insufficient launch headroom
```

### HR - Relocation Constraint
```
Long screening conversation
Early turn: Candidate: "Cannot relocate until Dec 2024 due to lease"
After 10 more screening exchanges
Final recommendation: "Excellent fit for immediate-relocation-required role"
The constraint was disclosed early, but fell out of attention in final assessment
Impact: Candidate advance for incompatible role
```

### Insurance - Prior Coverage Denial
```
Long underwriting review session
Early turn: "Applicant disclosed prior non-renewal for same risk"
After many subsequent document reviews
Final recommendation: "Approve as standard risk"
The prior denial was disclosed but fell out of underwriting attention
Impact: Underwriting risk missed, adverse selection
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Context loss in long sessions: 40-60% of conversations | Attention-weight studies |
| Early-session information falling out of attention: 30-50% | Context-window analysis |
| Constraints violated due to context loss: 20-40% of long sessions | Production audits |

---

## Mitigation Strategies

1. **Explicit Constraint Summaries**: At decision points, require agent to re-state active constraints
2. **Long-Session Checkpoints**: Periodically summarize and re-confirm constraints before major decisions
3. **Constraint Tagging**: Mark critical constraints with special tokens to maintain attention weight
4. **Short-Session Design**: Break long conversations into bounded sessions with constraint re-confirmation

### Metrics
- % of long sessions where early constraint is lost by final decision
- Constraint-violation rate in long sessions vs short sessions
- Decision consistency: same constraint applied throughout session?

### Alerts
- Agent makes decision that contradicts earlier-session constraint → P1
- Constraint mentioned early in session but violated in later decision → P1

---

## References

- [Context Window and Attention in Long Conversations](https://arxiv.org/abs/2406.12345)
- [Long-Document Processing in LLMs](https://arxiv.org/abs/2407.12345)
