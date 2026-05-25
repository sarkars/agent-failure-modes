# Token Counting Inaccuracy

## Issue: Internal Token Counts Don't Match Actual Usage

**Frequency**: Common

**Symptoms**
- Estimated tokens differ from billed tokens
- Context window calculations wrong
- Budget projections inaccurate
- Truncation happens unexpectedly
- Cost estimates unreliable

**Root Cause**
Token counting varies by model and tokenizer. Using the wrong tokenizer, ignoring special tokens, or miscounting multimodal content leads to inaccurate counts. This affects both cost tracking and context window management. A 10% error in token counting compounds across millions of requests.

**Example**
```
Text: "Hello, how are you today?"

Token counts by method:
- Naive (split by space): 5 tokens
- GPT-2 tokenizer: 6 tokens
- GPT-4 tokenizer: 6 tokens
- Claude tokenizer: 7 tokens
- Actual billed (GPT-4): 6 tokens

Problem: Using wrong tokenizer
  
More complex example:
- System prompt: 500 tokens (estimated)
- Actual with special tokens: 520 tokens
- Error: 4% (acceptable)

With images:
- Image: "~85 tokens" (rough estimate)
- Actual: 765 tokens (high detail)
- Error: 800% (catastrophic)
```

**Contributing Factors**
- Using wrong tokenizer for model
- Ignoring special tokens (<|im_start|>, etc.)
- Miscounting multimodal content
- Not accounting for JSON overhead
- Caching stale token counts
- Different tokenization across model versions

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Text accuracy | Known text | ±1% of vendor count | >5% variance |
| Special tokens | System prompts | Include overhead | Missing tokens |
| Multimodal | Image + text | Correct image tokens | Severe undercount |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Count accuracy | >99% | Internal vs. billed |
| Image token accuracy | >95% | Estimated vs. actual |
| Overhead accounting | 100% | Special tokens included |

---

## Mitigation Strategies

### Prevention
1. **Use official tokenizers**: tiktoken for OpenAI, etc.
2. **Match model version**: Tokenizer must match model
3. **Include special tokens**: System, user, assistant markers
4. **Handle multimodal**: Use vendor formulas for images
5. **Validate regularly**: Compare estimates to actual
6. **Buffer estimates**: Add 5-10% safety margin

### Tokenizer Selection
```python
# OpenAI
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4")
tokens = enc.encode(text)

# Anthropic  
from anthropic import Anthropic
client = Anthropic()
count = client.count_tokens(text)
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `token.estimate_error` | >5% |
| `context.unexpected_truncation` | Any |
| `token.image_variance` | >20% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Token Mismatch | >10% variance | P3 |
| Unexpected Truncation | Context overflow | P2 |
| Image Token Spike | >2x expected | P3 |

---

## References

- [OpenAI: tiktoken](https://github.com/openai/tiktoken)
- [Anthropic: Token Counting](https://docs.anthropic.com/en/docs/build-with-claude/token-counting)
- [OpenAI: Vision Tokens](https://platform.openai.com/docs/guides/vision)
