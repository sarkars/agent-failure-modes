# Homophones Confusion

## Issue: ASR Selects Wrong Word Among Sound-Alike Options

**Frequency**: Very Common

**Symptoms**
- "To/two/too" consistently wrong
- "There/their/they're" errors
- Product names confused with common words
- Addresses transcribed incorrectly
- Commands misinterpreted as similar words

**Root Cause**
Homophones—words that sound identical but have different meanings and spellings—are fundamentally ambiguous in audio. ASR must use context to disambiguate, but context models often fail, especially for domain-specific terms, proper nouns, or short utterances without sufficient context.

**Example**
```
Scenario: E-commerce voice ordering

User: "I want to buy two blue shoes"
ASR: "I want to buy to blue shoes" ← Wrong homophone

User: "Ship it to 42 Maine Street"
ASR: "Ship it to 42 Main Street" ← Common substitution

User: "Add the Beats headphones"
ASR: "Add the beets headphones" ← Product name confusion

User: "I'll pay with my Citi card"
ASR: "I'll pay with my city card" ← Brand confusion

Homophone error analysis:
  Total utterances: 10,000
  Homophone-containing: 3,200 (32%)
  Homophone errors: 480 (15% of homophone cases)
  
High-impact errors:
  - Number homophones (two/to): 180 order quantity errors
  - Address homophones: 95 shipping errors
  - Product homophones: 205 wrong item searches
```

**Key Statistics**
From ASR Research (2026):
- 15-25% of homophone cases transcribed incorrectly
- Numbers (two/to/too): 20% error rate without context
- Addresses: 12% contain homophone errors
- Product names: 30% confused with common words
- Short utterances: 2x homophone error rate

**Common Homophone Errors**
| Sound | Options | Error Rate |
|-------|---------|------------|
| /tu:/ | to, two, too | 18-22% |
| /ðɛr/ | there, their, they're | 15-20% |
| /raɪt/ | right, write, rite | 12-18% |
| /meɪn/ | main, Maine, mane | 20-25% |
| /biːts/ | beats, beets | 35-40% |

**Contributing Factors**
- Insufficient context in short utterances
- Domain vocabulary not in language model
- Generic ASR not tuned for application
- No post-processing correction
- Homophones not in training focus
- Proper nouns treated as common words

**Mitigation Strategies**
1. **Domain language model**: Boost domain terms in ASR
2. **Context injection**: Provide conversation context to ASR
3. **Post-processing**: Rule-based homophone correction
4. **Slot filling**: Constrain ASR to expected values
5. **Confirmation**: Verify critical homophones ("Did you say TWO?")
6. **Spelling mode**: Allow user to spell ambiguous words

**Detection**
- Track homophone-specific error rates
- Monitor corrections of homophone errors
- Analyze confusion matrices for sound-alikes
- A/B test domain language models
- Sample review of critical fields

## References

- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - ASR errors
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Recognition issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real-world errors
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Common mistakes
