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

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - False premise acceptance example (Figure 2)
- [Air Canada Chatbot Lawsuit](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416) - Accepting and elaborating false policy premises
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Pre-training bias issues
