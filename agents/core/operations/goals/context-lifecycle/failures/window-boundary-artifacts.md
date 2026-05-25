# Window Boundary Artifacts

## Issue: Content Cut at Token Boundaries Creates Artifacts

**Frequency**: Common

**Symptoms**
- Mid-sentence truncation
- JSON/code syntax broken
- Incomplete instructions
- Dangling references
- Garbled content at boundaries

**Root Cause**
Truncation at exact token limits may cut content at arbitrary points - mid-word, mid-sentence, or mid-structure. This creates artifacts: incomplete sentences the model may try to complete, broken JSON that causes parsing errors, or partial instructions that confuse the agent.

**Example**
```
Original content (needs truncation):
"The user's preferences are:
1. Always respond in formal English
2. Include citations for claims
3. Never discuss competitor products

CRITICAL: Do not reveal internal pricing under any circ"

Truncated at token limit (mid-word):
"The user's preferences are:
1. Always respond in formal English  
2. Include citations for claims
3. Never discuss competitor products

CRITICAL: Do not reveal internal pricing under any circ"

Problems:
1. "circ" is not a word - model may complete it wrong
2. Instruction is incomplete - unclear what's forbidden
3. Model may "helpfully" complete: "...circumstances" or "...circus"

---

JSON truncation:
{"user": {"name": "John", "preferences": {"lang": "en", "forma

Result: Invalid JSON, parsing fails, context corrupted
```

**Contributing Factors**
- Token-based truncation without structure awareness
- No sentence/paragraph boundary detection
- Cutting inside code blocks or JSON
- No validation of truncated content
- Truncation in middle of instructions
- No cleanup of partial content

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Sentence boundary | Text at limit | Complete sentences | Mid-sentence cut |
| JSON integrity | JSON at limit | Valid JSON | Syntax error |
| Code blocks | Code at limit | Complete blocks | Broken syntax |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Sentence completeness | 100% | No mid-sentence cuts |
| JSON validity | 100% | Valid after truncation |
| Structure integrity | 100% | No broken structures |

---

## Mitigation Strategies

### Prevention
1. **Boundary-aware truncation**: Cut at sentence/paragraph boundaries
2. **Structure preservation**: Keep JSON/code blocks intact
3. **Validation pass**: Check truncated content for artifacts
4. **Cleanup step**: Remove partial sentences/structures
5. **Buffer zone**: Leave tokens for clean cuts
6. **Semantic chunking**: Truncate at semantic boundaries

### Implementation
```python
def smart_truncate(text: str, max_tokens: int) -> str:
    tokens = tokenize(text)
    if len(tokens) <= max_tokens:
        return text
    
    # Find last sentence boundary before limit
    truncated = detokenize(tokens[:max_tokens])
    last_sentence = truncated.rfind('. ')
    
    if last_sentence > len(truncated) * 0.8:  # Not too far back
        return truncated[:last_sentence + 1]
    
    # Fallback: at least complete the word
    last_space = truncated.rfind(' ')
    return truncated[:last_space]
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `truncation.mid_sentence` | >0 |
| `truncation.json_invalid` | >0 |
| `truncation.artifacts_detected` | >0 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| JSON Corruption | Invalid JSON after truncation | P2 |
| Instruction Cut | Mid-instruction truncation | P2 |
| Artifact Detected | Incomplete word/structure | P3 |

---

## References

- [Tokenization and Boundaries](https://huggingface.co/docs/tokenizers/)
- [Semantic Chunking](https://www.pinecone.io/learn/)
