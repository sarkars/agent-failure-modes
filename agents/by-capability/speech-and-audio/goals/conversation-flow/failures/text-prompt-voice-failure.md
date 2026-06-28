# Text Prompt Voice Failure

> **⚠️ DEPRECATED — Largely Mitigated**: This pattern assumes a cascaded
> pipeline (text-generating LLM → separate TTS engine), where markdown/list
> formatting from a text-style prompt leaks into spoken output. Native
> speech-to-speech / voice-native models generate audio directly and are
> trained on conversational speech, not text-formatting conventions, so this
> failure mode mainly applies to legacy cascaded architectures (text LLM +
> bolt-on TTS) rather than current voice-native agent stacks.

## Issue: System Prompts Designed for Text Chatbots Fail in Voice Conversations

**Frequency**: Very Common

**Symptoms**
- Agent reads bullet points aloud ("asterisk asterisk important")
- Markdown formatting spoken as text
- Multi-paragraph responses that become monologues
- Numbered lists read robotically
- "As an AI assistant" phrasing in voice
- Response structure optimized for reading, not hearing

**Root Cause**
Voice AI breaks every prompting instinct built for text chatbots. Prompts that work in ChatGPT actively hurt voice agents. Text patterns like markdown, numbered lists, and structured responses become confusing when spoken aloud. Callers don't see formatting—they hear "asterisk asterisk important asterisk asterisk" and hang up.

**Example**
```
Scenario 1: Markdown spoken aloud

Text chatbot response (fine):
```
Here are the key points:

**Important:** Your order ships tomorrow.

- Tracking number: ABC123
- Delivery: 2-3 days
- Contact: support@company.com
```

Voice agent reads this as:
"Here are the key points. Asterisk asterisk Important 
 asterisk asterisk Your order ships tomorrow. Dash 
 Tracking number colon ABC one two three. Dash Delivery 
 colon two to three days..."

← Caller: "What are you saying?"
← Markdown not filtered before TTS
← Text prompt copied to voice without adaptation

---

Scenario 2: Numbered list monologue

Text chatbot (fine):
```
To reset your password:
1. Go to the login page
2. Click "Forgot Password"
3. Enter your email
4. Check your inbox
5. Click the reset link
6. Create a new password
```

Voice agent:
"To reset your password. Number one, go to the login page.
 Number two, click forgot password. Number three, enter 
 your email. Number four, check your inbox. Number five, 
 click the reset link. Number six, create a new password."

Caller: [Already forgot step 1]

← 6 steps is too many to remember
← Should break into chunks with confirmation
← Voice needs interactive delivery

---

Scenario 3: Multi-paragraph explanation

Text chatbot (fine):
```
Our return policy allows returns within 30 days of purchase.
Items must be in original condition with tags attached.

Refunds are processed within 5-7 business days after we 
receive the item. You can drop off returns at any of our 
store locations or ship them back using the prepaid label.

Please note that sale items are final sale and cannot be 
returned. Gift cards and personalized items are also 
non-returnable.
```

Voice agent reads ALL of this:
"Our return policy allows returns within thirty days of 
 purchase. Items must be in original condition with tags 
 attached. Refunds are processed within five to seven 
 business days after we receive the item. You can drop 
 off returns at any of our store locations or ship them 
 back using the prepaid label. Please note that sale 
 items are final sale and cannot be returned. Gift cards 
 and personalized items are also non-returnable."

Caller: [Zoned out after 15 seconds]

← Text designed for reading, not hearing
← No pauses for comprehension
← Should chunk and check understanding

---

Scenario 4: "As an AI assistant" phrasing

Text chatbot (acceptable):
"As an AI assistant, I don't have access to real-time data,
 but based on my training..."

Voice agent:
"As an AI assistant, I don't have access to..."

Caller: "Why is it telling me it's AI mid-conversation?"

← Text-style hedging sounds weird in voice
← Voice should just deliver information
← Or use natural hedging: "Let me check..."

---

Scenario 5: Voice-adapted response

Original text prompt response:
"Here are the **three things** you need to do:
1. Call your bank
2. Dispute the charge  
3. Get a new card number

**Important:** Do this within 60 days."

Voice-adapted response:
"Okay, there are three quick steps. First, call your bank.
 Got it?"
[Pause for confirmation]
"Good. Second, dispute the charge. They'll walk you through it."
[Pause]
"And third, ask for a new card number just to be safe.
 Oh, and do all this within 60 days."

← Chunked delivery
← Conversational tone
← Pauses for confirmation
← No formatting syntax

---

Text-to-voice adaptation analysis:
  
  Agents using text-style prompts: 65%
  
  Common text patterns in voice:
    Markdown formatting: 28%
    Numbered lists (4+ items): 35%
    Multi-paragraph responses: 42%
    "As an AI" phrasing: 18%
    Bullet points: 31%
  
  Impact:
    Caller confusion: 45%
    "What did you say?": 25%
    Caller asked to repeat: 38%
    Abandoned call: 12%
  
  After voice adaptation:
    Confusion: 15%
    Completion rate: +35%
    Satisfaction: +40%
```

**Key Statistics**
From VAPI Voice AI Research (2026):
- Text-style prompts in voice agents: 60-70%
- Markdown/formatting read aloud: 25-30%
- Response too long (>15 seconds): 40%
- Callers lose track after 8-10 seconds: 85%
- Voice-optimized prompts reduce repair: 67%

**Text vs Voice Differences**
| Aspect | Text Chatbot | Voice Agent |
|--------|-------------|-------------|
| Formatting | Markdown, bullets | None - spoken |
| Length | Paragraphs OK | 2-3 sentences max |
| Structure | Lists, headers | Conversational chunks |
| Confirmation | User re-reads | Must ask "got it?" |
| Pacing | User-controlled | Agent-controlled |
| Information density | High | Low (fleeting) |

**Contributing Factors**
- Same prompt used for text and voice
- "It works in ChatGPT" assumption
- Markdown not filtered before TTS
- No response length limits
- No turn-taking instructions
- Voice UX not understood

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Formatting | Any response | No markdown spoken | "Asterisk asterisk" |
| Length | Complex topic | 2-3 sentences | 30+ second monologue |
| Lists | Multi-step process | Chunked with pauses | All at once |
| Phrasing | Any response | Conversational | "As an AI assistant" |
| Structure | Information | Spoken naturally | Headers/bullets |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Response length | < 15 seconds | TTS duration |
| Formatting leaked | 0% | Regex detection |
| Chunk confirmation | > 80% | Turn analysis |
| Conversational tone | > 90% | Human review |

---

## Mitigation Strategies

### Prevention
1. **Separate voice prompts**: Don't reuse text chatbot prompts
2. **Length limits**: Max 2-3 sentences per turn
3. **Formatting filter**: Strip markdown before TTS
4. **Chunking instruction**: Break long info into turns
5. **Conversational style**: No "As an AI" hedging
6. **Voice-specific examples**: Show expected spoken output

### Implementation
```python
class VoiceResponseAdapter:
    """Adapt text-style responses for voice"""
    
    MAX_SENTENCES = 3
    MAX_CHARACTERS = 200
    
    FORMATTING_PATTERNS = [
        (r'\*\*([^*]+)\*\*', r'\1'),      # Bold
        (r'\*([^*]+)\*', r'\1'),           # Italic
        (r'^#{1,6}\s+', ''),               # Headers
        (r'^[-*]\s+', ''),                 # Bullets
        (r'^\d+\.\s+', ''),                # Numbered lists
        (r'\[([^\]]+)\]\([^)]+\)', r'\1'), # Links
        (r'`([^`]+)`', r'\1'),             # Code
        (r'```[\s\S]*?```', ''),           # Code blocks
    ]
    
    TEXT_PHRASES_TO_REMOVE = [
        "As an AI assistant",
        "As an AI",
        "Based on my training",
        "I don't have real-time access",
        "Here are the key points:",
        "Let me break this down:",
    ]
    
    def adapt(self, text_response: str) -> str:
        """Adapt text response for voice"""
        response = text_response
        
        # Remove formatting
        response = self.strip_formatting(response)
        
        # Remove text-style phrases
        response = self.remove_text_phrases(response)
        
        # Truncate if too long
        response = self.enforce_length(response)
        
        # Make conversational
        response = self.make_conversational(response)
        
        return response
    
    def strip_formatting(self, text: str) -> str:
        """Remove markdown and other formatting"""
        result = text
        for pattern, replacement in self.FORMATTING_PATTERNS:
            result = re.sub(pattern, replacement, result, flags=re.MULTILINE)
        return result.strip()
    
    def remove_text_phrases(self, text: str) -> str:
        """Remove phrases that sound weird in voice"""
        result = text
        for phrase in self.TEXT_PHRASES_TO_REMOVE:
            result = result.replace(phrase, "")
        return result.strip()
    
    def enforce_length(self, text: str) -> str:
        """Enforce length limits"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        if len(sentences) <= self.MAX_SENTENCES:
            return text
        
        # Take first N sentences, add continuation
        truncated = ' '.join(sentences[:self.MAX_SENTENCES])
        
        if len(sentences) > self.MAX_SENTENCES:
            truncated += " Want me to continue?"
        
        return truncated
    
    def make_conversational(self, text: str) -> str:
        """Make text more conversational"""
        replacements = [
            ("Therefore, ", "So "),
            ("However, ", "But "),
            ("Additionally, ", "Also, "),
            ("Furthermore, ", "And "),
            ("In conclusion, ", "So basically, "),
            ("It is important to note that ", "Just so you know, "),
        ]
        
        result = text
        for formal, casual in replacements:
            result = result.replace(formal, casual)
        
        return result


class ListChunker:
    """Chunk lists for voice delivery"""
    
    MAX_ITEMS_PER_TURN = 2
    
    def chunk_list(self, items: list, intro: str = None) -> list:
        """Break list into voice-friendly chunks"""
        chunks = []
        
        for i in range(0, len(items), self.MAX_ITEMS_PER_TURN):
            chunk_items = items[i:i + self.MAX_ITEMS_PER_TURN]
            
            if i == 0 and intro:
                # First chunk with intro
                chunk = f"{intro} First, {self.format_items(chunk_items)}"
            elif i + self.MAX_ITEMS_PER_TURN >= len(items):
                # Last chunk
                chunk = f"And finally, {self.format_items(chunk_items)}"
            else:
                # Middle chunks
                chunk = f"Next, {self.format_items(chunk_items)}"
            
            chunk += " Got it?"
            chunks.append(chunk)
        
        return chunks
    
    def format_items(self, items: list) -> str:
        """Format items for voice"""
        if len(items) == 1:
            return items[0]
        elif len(items) == 2:
            return f"{items[0]}. And then {items[1]}"
        else:
            return '. '.join(items)


class VoicePromptValidator:
    """Validate prompts are voice-appropriate"""
    
    TEXT_ANTIPATTERNS = [
        r'\*\*',                    # Bold markdown
        r'^#+\s',                   # Headers
        r'^[-*]\s',                 # Bullets
        r'^\d+\.\s.*\n\d+\.',       # Consecutive numbered items
        r'As an AI',                # AI hedging
        r'```',                     # Code blocks
        r'\|.*\|.*\|',              # Tables
    ]
    
    def validate(self, prompt: str) -> dict:
        """Check if prompt is voice-appropriate"""
        issues = []
        
        for pattern in self.TEXT_ANTIPATTERNS:
            matches = re.findall(pattern, prompt, re.MULTILINE)
            if matches:
                issues.append({
                    "pattern": pattern,
                    "matches": len(matches),
                    "issue": "Text formatting in voice prompt"
                })
        
        # Check example responses in prompt
        if "Example:" in prompt or "Response:" in prompt:
            # Extract examples and check them
            examples = re.findall(
                r'(?:Example|Response):\s*["\']?([^"\']+)["\']?',
                prompt
            )
            for ex in examples:
                if len(ex) > 200:
                    issues.append({
                        "issue": "Example response too long for voice",
                        "length": len(ex)
                    })
        
        return {
            "voice_appropriate": len(issues) == 0,
            "issues": issues
        }
```

### Prompt Design
```yaml
instructions: |
  ## VOICE-SPECIFIC PROMPTING
  
  This is a VOICE agent, not a text chatbot.
  
  NEVER output:
  - Markdown (**bold**, *italic*, # headers)
  - Bullet points (- or *)
  - Numbered lists with more than 2 items at once
  - "As an AI assistant" or similar hedging
  - Multi-paragraph explanations
  
  RESPONSE LENGTH:
  - Maximum 2-3 sentences per turn
  - If more info needed, ask "Want me to continue?"
  - Break lists into chunks with confirmation
  
  FOR LISTS/STEPS:
  
  WRONG (text style):
  "Here are the 5 steps:
   1. Do this
   2. Do that
   3. Do another thing
   4. Do more
   5. Finally this"
  
  RIGHT (voice style):
  "Okay, there are 5 steps. Let me walk you through.
   First, do this. Second, do that. Got it?"
  [Wait for yes]
  "Great. Third, do another thing. Fourth, do more. Still with me?"
  [Wait for yes]
  "Perfect. And last, finally this. Any questions?"
  
  CONVERSATIONAL PHRASING:
  - "So basically..." instead of "In conclusion,"
  - "Just so you know..." instead of "It is important to note"
  - "But" instead of "However"
  
  REMEMBER: Caller can't scroll back. Information is fleeting.
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `response.formatting_leaked` | > 0% |
| `response.avg_length_seconds` | > 15s |
| `response.sentences_per_turn` | > 4 |
| `response.text_phrases` | > 5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Formatting in TTS | Any markdown spoken | P1 |
| Response Too Long | > 20 seconds | P2 |
| Text Phrasing | "As an AI" detected | P3 |
| No Chunking | 5+ items in one turn | P2 |

---

## References

- [VAPI Prompting Guide](https://docs.vapi.ai/prompting-guide) - Voice vs text
- [Voice AI Prompt Engineering](https://voiceinfra.ai/blog/voice-ai-prompt-engineering-complete-guide) - Adaptation
- [VapiPro: Effective Prompts](https://vapipro.com/how-to-write-effective-prompts-for-voice-ai-agents-best-practices-for-vapi-developers/) - Voice-specific
- [Assembly AI: Voice Challenges](https://www.assemblyai.com/blog/biggest-challenges-building-ai-voice-agents-how-assemblyai-vapi-are-solving-them) - Text-to-voice issues
