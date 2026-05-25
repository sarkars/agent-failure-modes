# Name Recognition Failures

## Issue: ASR Fails to Correctly Transcribe Personal and Business Names

**Frequency**: Very Common

**Symptoms**
- Customer names consistently misspelled
- Business names transcribed as common words
- Ethnic names particularly error-prone
- Account lookups fail due to name mismatch
- Address names (streets, cities) wrong

**Root Cause**
Names are open-vocabulary—they can be any sequence of sounds, including rare combinations not in ASR training data. Ethnic names, unusual spellings, and names that sound like common words are especially problematic. Since names are often critical for identity and account lookup, errors directly impact transaction success.

**Example**
```
Scenario: Bank account lookup

User: "My name is Siobhan O'Brien"
ASR attempts:
  - "My name is Sha von O'Brien"
  - "My name is See oh bon O'Brien"  
  - "My name is Chevon O'Brien"
Correct: "Siobhan O'Brien"
Account found: No

User: "The account is under Nguyen"
ASR: "The account is under Win" / "New Yen" / "Gwen"
Correct: "Nguyen"
Account found: No

User: "I'm calling about my son, Aditya Krishnamurthy"
ASR: "I'm calling about my son, a duty a Krishna Murphy"
Correct: "Aditya Krishnamurthy"

Name error analysis:
  Name lookups attempted: 10,000
  Exact match success: 6,200 (62%)
  Fuzzy match recovered: 2,100 (21%)
  Failed lookups: 1,700 (17%)
  
Error distribution:
  Anglo names: 8% error rate
  Hispanic names: 15% error rate
  Asian names: 25% error rate
  African names: 28% error rate
  Gaelic/Celtic names: 22% error rate
```

**Key Statistics**
From Name Recognition Research (2026):
- Name WER: 20-40% (vs. 5-10% for common words)
- Ethnic name error rate: 2-4x higher
- Failed account lookups from name errors: 15-20%
- Customer callbacks due to name issues: 12%
- Name-based discrimination complaints increasing

**Common Name Errors**
| Name Type | Error Pattern | Error Rate |
|-----------|---------------|------------|
| Gaelic (Siobhan) | Phonetic mismatch | 30-40% |
| Vietnamese (Nguyen) | Unfamiliar phonemes | 35-45% |
| Indian (Krishnamurthy) | Length/complexity | 25-35% |
| Arabic (Abdulrahman) | Compound handling | 20-30% |
| Chinese (Xiaoping) | Tone/romanization | 25-35% |

**Contributing Factors**
- Names not in ASR vocabulary
- Ethnic phonemes missing
- No name-specific model
- Spelling vs. pronunciation mismatch
- No fuzzy matching in lookup
- Training data bias toward Western names

**Mitigation Strategies**
1. **Name vocabulary**: Add common names to ASR lexicon
2. **Phonetic matching**: Use soundex/metaphone for lookup
3. **Spelling mode**: Allow letter-by-letter spelling
4. **Name confirmation**: Display/repeat name for verification
5. **Fuzzy lookup**: Account lookup tolerates variations
6. **Multi-attempt**: Try multiple transcription hypotheses

**Detection**
- Track name-specific WER
- Monitor account lookup failure rates
- Analyze failures by name ethnicity
- Compare ASR confidence on names vs. common words
- Survey customer name recognition experience

## References

- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Name issues
- [Stanford: Racial Disparities in ASR](https://www.pnas.org/doi/10.1073/pnas.1915768117) - Name bias
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Identity handling
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
