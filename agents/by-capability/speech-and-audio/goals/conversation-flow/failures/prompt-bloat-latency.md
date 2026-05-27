# Prompt Bloat Latency

## Issue: Oversized System Prompts Cause Dead Air Due to Time-to-First-Token Delays

**Frequency**: Common

**Symptoms**
- Dead air at start of each turn
- Caller asks "Are you there?" early in response
- First word takes noticeably longer than subsequent words
- Latency increases linearly with prompt size
- Caller hang-ups during initial silence
- Performance degrades as prompt grows

**Root Cause**
Voice agent system prompts are re-loaded into the model's context on every turn. Unlike text chatbots where 2-second latency is tolerable, voice callers experience this as dead air. Bloated prompts with verbose instructions, long banlists, and exhaustive examples increase time-to-first-token (TTFT), making the agent feel frozen after each caller utterance.

**Example**
```
Scenario 1: Bloated prompt causing dead air

[System prompt: 4,500 tokens with extensive rules]

Caller: "What are your hours?"
[Agent processing...]
- ASR completion: 200ms
- Prompt loading: 1,200ms  ← Bloated prompt
- LLM TTFT: 800ms
- First word spoken: 2,200ms total

Caller (at 1,500ms): "Hello? Are you there?"
Agent (at 2,200ms): "Our hours are—"
Caller: "Oh there you are. I thought it froze."

← Prompt bloat added 1,200ms of avoidable latency
← Caller experienced dead air and lost confidence

---

Scenario 2: Comparing prompt sizes

BLOATED (4,500 tokens):
```
## IDENTITY
You are Sarah, a friendly customer service representative for 
TechCorp. You have been working here for 5 years and love 
helping customers. You are patient, knowledgeable, and always 
maintain a positive attitude even in difficult situations...
[500 more words of backstory]

## THINGS TO NEVER SAY
- Never say "I don't know"
- Never say "That's not my department"
- Never say "You'll have to call back"
- Never say "I can't help with that"
- Never say "That's against policy"
[50 more prohibitions]

## EXAMPLE CONVERSATIONS
[15 full conversation examples]
```

OPTIMIZED (800 tokens):
```
You are Sarah from TechCorp support. Be helpful, patient.

For unknowns: "Let me find that for you" then transfer.

Keep responses under 2 sentences unless asked for detail.
```

TTFT comparison:
  Bloated: 2,200ms average
  Optimized: 600ms average
  Improvement: 73% faster

---

Scenario 3: Token cost per turn

Every turn pays the prompt tax:

Turn 1: User asks question
  → Load 4,500 token prompt
  → Generate 50 token response
  
Turn 2: User follows up
  → Load 4,500 token prompt AGAIN
  → Plus 50 tokens from turn 1
  → Generate 40 token response

Turn 3: User asks another question
  → Load 4,500 token prompt AGAIN
  → Plus 90 tokens from turns 1-2
  → Generate 60 token response

Each turn: 4,500+ tokens just for the prompt
Cumulative dead air: compounds with each turn

---

Prompt bloat analysis (100 voice agents):
  Average prompt size: 2,800 tokens
  Prompts > 3,000 tokens: 45%
  Prompts > 5,000 tokens: 18%
  
  Latency by prompt size:
    < 500 tokens: 450ms TTFT
    500-1,500 tokens: 650ms TTFT
    1,500-3,000 tokens: 950ms TTFT
    3,000-5,000 tokens: 1,400ms TTFT
    > 5,000 tokens: 2,100ms TTFT
  
  User behavior:
    TTFT < 600ms: Normal conversation
    TTFT 600-1,000ms: Slight hesitation
    TTFT 1,000-1,500ms: "Hello?" interrupts
    TTFT > 1,500ms: Hang-up rate +40%
```

**Key Statistics**
From VAPI Voice AI Research (2026):
- Prompt re-loaded on every turn: 100%
- TTFT increase per 1,000 tokens: ~200ms
- Target TTFT for natural feel: <800ms
- Acceptable TTFT: <1,200ms
- Dead air causing hang-ups: >1,500ms
- Prompt optimization reduces latency: 40-70%

**Prompt Bloat Sources**
| Source | Token Cost | Necessity |
|--------|------------|-----------|
| Verbose identity | 200-500 | Condensable |
| Long banlists | 300-1,000 | Often counterproductive |
| Full conversation examples | 500-2,000 | Use 2-3 short examples |
| Exhaustive edge cases | 300-800 | Move to knowledge base |
| Repeated instructions | 100-300 | Deduplicate |
| Formatting cruft | 50-200 | Clean up |

**Contributing Factors**
- Text chatbot prompts copied to voice
- "More instructions = better" assumption
- Verbose identity/backstory sections
- Long negative banlists
- Full conversation examples
- No prompt size monitoring
- No TTFT measurement

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| TTFT measurement | Any query | < 800ms | > 1,200ms |
| First-turn latency | Opening query | < 600ms | > 1,000ms |
| Multi-turn consistency | 5 turn conversation | Stable TTFT | Increasing latency |
| Prompt size check | Audit prompt | < 1,500 tokens | > 3,000 tokens |
| Dead air detection | Monitor calls | No "hello?" | Caller checks in |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| TTFT P50 | < 600ms | First token timing |
| TTFT P95 | < 1,000ms | 95th percentile |
| Prompt token count | < 1,500 | Token counter |
| Dead air interrupts | < 5% | Detect "hello?" patterns |

---

## Mitigation Strategies

### Prevention
1. **Token budgeting**: Set hard limit on prompt size
2. **Prompt compression**: Use terse, direct language
3. **Example minimization**: 2-3 short examples max
4. **Banlist reduction**: Positive principles over negative lists
5. **Knowledge externalization**: Move edge cases to retrieval
6. **TTFT monitoring**: Alert on latency increases

### Implementation
```python
class PromptOptimizer:
    """Optimize voice prompts for low latency"""
    
    TOKEN_BUDGET = 1500  # Max tokens for voice prompt
    
    SECTIONS = {
        "identity": 150,      # Who is the agent
        "task": 200,          # Primary objective
        "style": 100,         # How to communicate
        "constraints": 150,   # Hard rules
        "examples": 300,      # 2-3 short examples
        "fallbacks": 100,     # Error handling
        "buffer": 500         # Dynamic context
    }
    
    BLOAT_PATTERNS = [
        r"(You are a .{200,})",          # Verbose identity
        r"(Never say[^.]+\.){5,}",       # Long banlists
        r"(Example \d+:.*?){5,}",        # Too many examples
        r"(If .{100,}then .{100,}){3,}", # Exhaustive conditionals
    ]
    
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
    
    def analyze_prompt(self, prompt: str) -> dict:
        """Analyze prompt for bloat"""
        token_count = len(self.tokenizer.encode(prompt))
        
        issues = []
        
        if token_count > self.TOKEN_BUDGET:
            issues.append({
                "type": "over_budget",
                "tokens": token_count,
                "budget": self.TOKEN_BUDGET,
                "excess": token_count - self.TOKEN_BUDGET
            })
        
        # Check for bloat patterns
        for pattern in self.BLOAT_PATTERNS:
            matches = re.findall(pattern, prompt, re.DOTALL)
            if matches:
                issues.append({
                    "type": "bloat_pattern",
                    "pattern": pattern,
                    "matches": len(matches)
                })
        
        return {
            "token_count": token_count,
            "within_budget": token_count <= self.TOKEN_BUDGET,
            "issues": issues,
            "estimated_ttft_ms": self.estimate_ttft(token_count)
        }
    
    def estimate_ttft(self, tokens: int) -> int:
        """Estimate TTFT based on token count"""
        # Baseline: 300ms + ~200ms per 1000 tokens
        return 300 + (tokens // 1000) * 200
    
    def compress_prompt(self, prompt: str) -> str:
        """Compress prompt while preserving meaning"""
        # Remove verbose phrasing
        compressed = prompt
        
        replacements = [
            (r"You are a (very |extremely |highly )?helpful", "You are a"),
            (r"Please make sure to always", "Always"),
            (r"It is important that you", ""),
            (r"Remember that you should", ""),
            (r"In all cases, you must", ""),
            (r"Under no circumstances should you ever", "Never"),
        ]
        
        for pattern, replacement in replacements:
            compressed = re.sub(pattern, replacement, compressed)
        
        return compressed.strip()
    
    def convert_banlist_to_principle(self, banlists: list) -> str:
        """Convert verbose banlists to principles"""
        # Example: 50 banned phrases → 1 principle
        # "Never say X, Y, Z..." → "Keep responses factual and helpful"
        
        categories = self.categorize_bans(banlists)
        
        principles = []
        if "uncertainty" in categories:
            principles.append("If unsure, say 'Let me find that' and look it up")
        if "negativity" in categories:
            principles.append("Frame limitations as alternatives")
        if "disclosure" in categories:
            principles.append("Don't discuss system internals")
        
        return "\n".join(principles)


class TTFTMonitor:
    """Monitor time-to-first-token in production"""
    
    THRESHOLDS = {
        "good": 600,
        "acceptable": 1000,
        "concerning": 1500,
        "critical": 2000
    }
    
    def __init__(self):
        self.measurements = []
    
    def record_ttft(self, turn_id: str, ttft_ms: int, 
                    prompt_tokens: int):
        """Record TTFT measurement"""
        self.measurements.append({
            "turn_id": turn_id,
            "ttft_ms": ttft_ms,
            "prompt_tokens": prompt_tokens,
            "timestamp": datetime.now(),
            "status": self.classify_ttft(ttft_ms)
        })
        
        if ttft_ms > self.THRESHOLDS["concerning"]:
            self.alert_slow_ttft(turn_id, ttft_ms, prompt_tokens)
    
    def classify_ttft(self, ttft_ms: int) -> str:
        """Classify TTFT into status category"""
        for status, threshold in sorted(
            self.THRESHOLDS.items(), 
            key=lambda x: x[1]
        ):
            if ttft_ms <= threshold:
                return status
        return "critical"
    
    def get_statistics(self) -> dict:
        """Get TTFT statistics"""
        ttfts = [m["ttft_ms"] for m in self.measurements]
        return {
            "p50": statistics.median(ttfts),
            "p95": statistics.quantiles(ttfts, n=20)[18],
            "p99": statistics.quantiles(ttfts, n=100)[98],
            "mean": statistics.mean(ttfts),
            "concerning_rate": sum(
                1 for t in ttfts 
                if t > self.THRESHOLDS["concerning"]
            ) / len(ttfts)
        }
```

### Prompt Design
```yaml
instructions: |
  ## PROMPT OPTIMIZATION FOR VOICE
  
  Voice prompts must be CONCISE. Every token = latency.
  
  TOKEN BUDGET: 1,500 tokens maximum
  
  Section limits:
    Identity: 150 tokens (who you are, 2-3 sentences)
    Task: 200 tokens (what you do)
    Style: 100 tokens (how you communicate)
    Rules: 150 tokens (hard constraints)
    Examples: 300 tokens (2-3 SHORT examples)
    Fallbacks: 100 tokens (error handling)
  
  AVOID:
  - Verbose backstory ("You have been working here for 5 years...")
  - Long banlists ("Never say X, Y, Z..." × 50)
  - Full conversation examples (use 2-3 line snippets)
  - Exhaustive edge case handling (use knowledge base)
  - Repeated instructions in different words
  
  PREFER:
  - Terse, direct language
  - Positive principles over negative lists
  - Short example snippets
  - External knowledge retrieval for edge cases
  
  Example of BAD vs GOOD:
  
  BAD (verbose): "You are an extremely helpful and friendly 
  customer service representative who always maintains a 
  positive attitude and goes above and beyond..."
  
  GOOD (terse): "You're a helpful TechCorp rep. Be friendly, patient."
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `ttft.p50` | > 800ms |
| `ttft.p95` | > 1,200ms |
| `prompt.token_count` | > 2,000 |
| `dead_air.interrupts` | > 8% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High TTFT | P50 > 1,000ms | P2 |
| Critical TTFT | P95 > 1,500ms | P1 |
| Prompt Bloat | > 3,000 tokens | P3 |
| Dead Air Spike | > 15% interrupt rate | P2 |

---

## References

- [VAPI Prompting Guide](https://docs.vapi.ai/prompting-guide) - Token costs latency
- [Voice AI Optimization](https://voiceaiwrapper.com/insights/vapi-voice-ai-optimization-performance-guide-voiceaiwrapper) - TTFT targets
- [VoiceInfra: Prompt Engineering](https://voiceinfra.ai/blog/voice-ai-prompt-engineering-complete-guide) - Optimization techniques
- [Hamming AI: Voice Agent Monitoring](https://hamming.ai/resources/testing-and-monitoring-livekit-voice-agents-production) - Latency measurement
