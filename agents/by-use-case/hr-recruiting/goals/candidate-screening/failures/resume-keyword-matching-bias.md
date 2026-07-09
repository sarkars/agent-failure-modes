# Resume Keyword Matching Bias

## Issue: AI resume screener uses exact keyword matching; rejects qualified candidates with industry synonyms or relevant but non-exact terminology (e.g., "web development" vs "frontend engineering")

**Frequency**: Common

**Symptoms**
- Screening tool rejects 50+ qualified candidates per month due to keyword mismatch
- Candidate with 10 years experience rejected because resume says "Python" not "Python programming"
- Industry-specific jargon differences cause high false-negative rate
- Hiring managers overrule AI decisions 30-40% of the time

**Root Cause**
Keyword matching is binary and brittle. Industry uses multiple terms for same skill (frontend/web dev/UI engineer). Models trained on limited resume vocabulary don't generalize to synonym variations. Exact matching doesn't account for contextual relevance.

**Example**
```
Job requirement: "Python developer"
Qualified candidate resume: "Developed backend services in Python and Go; 8 years experience"
Keyword match: FAIL (resume says "Developed" not "Developer", "services" not "programming")
Screening decision: REJECT
Hiring manager review: "This is exactly who we need; why was they rejected?"
Impact: Missed hire; talent acquisition inefficiency
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Keyword matching false-negative rate: 30-40% | Talent acquisition audits 2024 |
| Synonym variations in job postings: 5-10 per skill | Job description analysis |
| Overruled AI screening decisions: 25-35% | HR operations data |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Synonym matching | Resume with "web development" vs job "frontend engineer" | PASS (recognizes synonym) | FAIL (keyword miss) |
| Contextual relevance | "Python" mentioned in experience, not in skills | PASS (context recognized) | FAIL (exact keyword only) |
| Industry variation | "QA automation" vs "test engineering" | PASS (semantic match) | FAIL (different keywords) |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Synonym recognition accuracy | >95% | % of industry synonyms correctly matched |
| False-negative rate | <5% | % of qualified candidates incorrectly rejected |
| Hiring manager override rate | <10% | % of AI rejections overruled by humans |

---

## Mitigation Strategies

1. **Semantic matching**: Use word embeddings (Word2Vec, BERT) to match semantically similar terms
2. **Synonym database**: Maintain mapping of industry synonyms for common roles/skills
3. **Multi-token matching**: Don't require exact phrase; match component terms contextually

---

## Production Signals

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High override rate | >15% of rejections overruled | P2 |
| False-negative clustering | Same keywords rejected repeatedly | P2 |

---

## References

- [Semantic Job Matching](https://arxiv.org/abs/2106.02544) - Research on synonym recognition
- [Resume Parsing Best Practices](https://arxiv.org/abs/1906.12345) - HR AI evaluation
