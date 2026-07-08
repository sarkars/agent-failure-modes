# False Premise Acceptance

## Issue: System Accepts User's Incorrect Assumptions

**Frequency**: Common

**Symptoms**
- System builds response on user's mistaken premise
- No correction of factually wrong query assumptions
- Answer is logically consistent but based on false foundation
- Compounds misinformation instead of correcting it
- User's misunderstanding is reinforced

**Root Cause**
RAG systems are designed to be helpful and answer questions, not to challenge user premises. When a query contains factual errors or incorrect assumptions, the system often accepts these as given and provides responses that build on the false foundation rather than correcting it.

**Example**
```
Query: "Why did Justice Ginsburg dissent in Obergefell v. Hodges?"

User's false premise: Ginsburg dissented

Actual fact: Justice Ginsburg JOINED the majority opinion 
             legalizing same-sex marriage

RAG Response (Ask Practical Law AI):
"Justice Ginsburg's dissent in Obergefell focused on concerns
about judicial overreach and federalism. She argued that the
Court should have allowed states more time to address the
marriage equality question through democratic processes."

Problem:
- System accepted false premise without verification
- Generated plausible-sounding but entirely fabricated dissent
- Retrieved content about actual dissents and applied to Ginsburg
- User's misunderstanding reinforced with false details

Result: User walks away with completely wrong understanding
        of a landmark Supreme Court decision
```

**Key Statistics**
From Stanford Legal RAG Hallucinations Study (2025):
- False premise acceptance documented as distinct failure mode
- Example from Thomson Reuters's Ask Practical Law AI
- System "fails to correct the user's mistaken premise"
- Adds additional false information compounding the error

**Acceptance Patterns**
- **Entity confusion**: User names wrong person, system plays along
- **Temporal errors**: User cites wrong date, system accepts it
- **Outcome reversal**: User states opposite outcome, system elaborates
- **Procedural mistakes**: User misunderstands process, system builds on it
- **Definitional errors**: User uses term incorrectly, system follows

**Contributing Factors**
- Systems trained to be helpful, not confrontational
- Retrieval finds documents matching query keywords
- Generation model interpolates between query and retrieved content
- No fact-checking of query premises
- Easier to answer than to challenge

**Mitigation Strategies**
1. **Premise verification**: Check factual claims in query before answering
2. **Confidence thresholds**: Express uncertainty about unlikely premises
3. **Fact-check integration**: Verify key entities and claims
4. **Gentle correction**: "I think you may mean..." approach
5. **Source grounding**: Require retrieved sources to support query premise
6. **Contradiction detection**: Flag when query contradicts retrieved facts

**Detection**
- Expert review of query-answer pairs
- Automated fact-checking of query premises
- User feedback "that's not what I was asking about"
- Contradiction analysis between query and knowledge base


## Mitigation Strategies

### Prevention

1. **Implement query-answer consistency validation**: Decompose complex queries into atomic components and verify each component is addressed in the answer before returning. Use RAGAS Answer Relevancy metric (target: >0.75) with automatic re-generation for scores below threshold. Root cause mitigation: Prevents context-anchoring by explicitly binding answer generation to parsed query intent.

2. **Apply multi-source consensus verification**: Require answers synthesized from multiple sources to explicitly cite which sources support each claim and flag unresolved contradictions. Implementation: Use semantic similarity checks across source fragments to detect cherry-picked evidence patterns. Root cause: Ensures balanced representation of evidence when sources conflict.

3. **Enforce comprehensive coverage checks**: Implement structured extraction requiring explicit treatment of caveats, limitations, exceptions, and counterevidence for each claim type. Use template responses with mandatory caveat sections. Root cause: Prevents omission of qualifying information that would change user decision-making.

### Detection & Response

1. **Answer completeness monitoring**: Measure coverage of query intents in generated answers. Track query decomposition rate (% of query components explicitly addressed) and flag responses with coverage <85%. Instrument RAG pipeline to log query-answer similarity scores per component. Alert on sustained scores <0.70.

2. **Evidence balance scoring**: For each answer, compute evidence distribution across sources and flag one-sided responses (>70% from single source on multi-source queries). Implement automated extraction of caveat/limitation mentions and track inclusion rates by query type. Target: >80% of medical/financial answers include relevant caveats.

### Architecture Patterns

1. Query Intent Decomposition Graph: Parse complex queries into a DAG of atomic intents before retrieval. Each retrieved document is mapped to specific intent nodes. Answer generation must satisfy all leaf nodes. Validation layer computes coverage before response generation.

2. Evidence Consensus Engine: Maintain a fact graph where each claim is attributed to specific sources with confidence scores. Multi-source claims require consensus computation (intersection of sources supporting claim). Flagging layer surfaces contradictions to generation model.

3. Structured Response Templates: Use task-specific response schemas that enforce inclusion of: primary answer, supporting evidence, relevant caveats/exceptions, alternative interpretations, confidence bounds. Auto-flag template violations before user delivery.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Answer Relevancy Score | >0.75 | <0.70 | RAGAS metric on generated answers vs. original query |
| Query Coverage Rate | >90% | <85% | Percentage of query components explicitly addressed in answer |
| Evidence Balance Index | >0.6 | <0.4 | Distribution of citations across sources (Gini coefficient, 0=balanced, 1=single-source) |
| Caveat Inclusion Rate | >80% | <70% | Percentage of medical/financial answers including relevant limitations |
| User Clarification Rate | <5% | >10% | Percentage of answered queries requiring follow-up clarification |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Low Answer Relevancy | Answer Relevancy Score < 0.70 for >5% of queries in 1-hour window | HIGH | Page on-call; trigger re-generation with query reinforcement prompt |
| Single-Source Dominance | Evidence Balance Index < 0.4 on multi-source queries for >3 consecutive queries | MEDIUM | Log event; audit cherry-picking patterns in retrieval/synthesis |
| Rising Clarification Demand | User Clarification Rate exceeds 10% (vs. 5% baseline) over 24-hour window | HIGH | Investigate query decomposition or answer template effectiveness |


## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - False premise acceptance example (Figure 2)
- [Air Canada Chatbot Lawsuit](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416) - Accepting and elaborating false policy premises
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Pre-training bias issues
