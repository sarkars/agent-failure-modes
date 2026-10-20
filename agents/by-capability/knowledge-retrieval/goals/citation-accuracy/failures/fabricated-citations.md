# AI Agent Cites Sources That Don't Exist: Causes and Fixes

## Issue: AI agent invents plausible-sounding citations — studies, articles, or case law — that don't actually exist.

**Frequency**: Occasional

**Symptoms**
- Citation references non-existent document
- Made-up document titles or authors
- URLs that lead nowhere
- Plausible-sounding but fake references
- Commonly reported in RAG and legal-research agents (LangChain, LlamaIndex) when the model generates content beyond what was actually retrieved

**Root Cause**
When model generates content beyond retrieved context, it may also generate citations for that content, creating entirely fabricated references.

**Example**
```
Query: "What research supports this treatment?"

Agent response: "According to the Johnson et al. (2023) study 
published in the Journal of Medical Research, the treatment 
showed 89% efficacy [1]."

Reality: 
- No such study exists
- No "Journal of Medical Research"
- Citation is completely fabricated

Result: User can't verify, may cite fake study themselves
```

**Real Incidents**
- Lawyers cited 6 fake ChatGPT-generated cases (Avianca lawsuit)
- Legal RAG tools generate plausible-looking fake citations

**Mitigation Strategies**
1. **Citation validation**: Verify all references exist
2. **Closed-book prevention**: Only cite from retrieved content
3. **URL verification**: Check URLs are valid before including
4. **Source registry**: Only allow citations to known sources
5. **Citation generation from extraction**: Build citations from metadata
6. **Warning labels**: Flag citations that couldn't be verified

**Detection**
- Validate all citations against source index
- Check URLs for accessibility
- Cross-reference author/title combinations
- Flag citations not in retrieved documents

**How to fix it**: restrict citations to sources actually present in retrieved context and validate every reference before output — see Mitigation Strategies below.

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


## Chat assistant examples

### Claims to have read inaccessible sources
Illustrative transcript (a research assistant in a chat app; the link is a subscriber-only Wall Street Journal article the tool cannot open):

Before:
```
User: Summarize this for my memo: https://www.wsj.com/articles/example-subscriber-story
Bot:  The article reports that the company cut its guidance and plans layoffs.
      As the article notes, "management expects a difficult second half."
      (the fetch returned a login page; the bot never saw the text)
User: Can I quote that line in my memo?
Bot:  Yes, it is from the article.
```
After:
```
User: Summarize this for my memo: https://www.wsj.com/articles/example-subscriber-story
Bot:  I could not read that article. The link opened a subscriber login page.
      I can only see the headline in the URL, so I will not summarize it or quote it.
      If you paste the text, I will summarize that. I can also look for
      public coverage, and I will label it as secondhand.
```
**What the user experiences:** a confident summary and a quotation that look read, so the user puts words in a memo that nobody checked, and learns this only when a colleague opens the link.
**Fix:** record per source whether the page body was opened; if the fetch returned a login page, paywall, or robots block, say so in the reply and do not summarize or quote it. Offer to work from pasted text or label any secondhand coverage as such. Reported case: when Press Gazette asked ChatGPT to chart Telegraph profits, its answer included figures and links, then it said its own citations were "hallucinated — but plausible" ([Press Gazette, Nov 2025](https://pressgazette.co.uk/platforms/chatgpt-took-press-gazette-content-then-said-that-could-not-have-happened/), opened). Metric: claims about sources the agent could not open, target 0. See the [confident wrong answer with no way to check](../../../../human-machine-interface/goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) pattern.

### Fabricated indicators or vulnerability details
Illustrative transcript (a security assistant in a SOC chat tool; the CVE number and IP address are fictional, from a reserved documentation range):

Before:
```
Analyst: What does CVE-2099-0000 affect, and is it being exploited?
Bot:     It affects Acme VPN Gateway 4.1 through 4.6 and is fixed in 4.7. Attackers
         are using 203.0.113.47 for command and control.
         (no lookup ran; the versions and the IP came from the model alone)
```
After:
```
Analyst: What does CVE-2099-0000 affect, and is it being exploited?
Bot:     I could not find CVE-2099-0000 in the NVD or CISA's Known Exploited
         Vulnerabilities catalog, so I cannot give versions, a fix, or indicators.
         Check the ID for a typo, or send the vendor advisory and I will summarize it.
```
**What the user experiences:** precise versions and an IP address that look looked up, so the analyst patches the wrong build and blocks an address with no link to the threat, and learns it only when the vendor advisory disagrees.
**Fix:** before presenting any CVE number, affected or fixed version, hash, IP, or domain, look it up in an authoritative feed (NVD, the CISA KEV catalog, the vendor advisory) and show the source next to each item; if the lookup finds nothing, say so instead of filling in details. In a controlled test, ChatGPT wrote plausible advisories for 97% of fake CVE IDs ([arXiv 2506.13161](https://arxiv.org/html/2506.13161v1), abstract opened). Metric: unsupported indicators in reports, target 0. See the [confident wrong answer with no way to check](../../../../human-machine-interface/goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) pattern.

## References
- [Avianca Lawyers](https://www.cnn.com/2023/05/27/business/chat-gpt-avianca-mata-lawyers/index.html) - 6 fake cases cited
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Fabricated legal citations
