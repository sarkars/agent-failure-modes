# Pronunciation Errors

## Issue: TTS Mispronounces Words, Names, or Domain Terms

**Frequency**: Common

**Symptoms**
- Names pronounced incorrectly
- Acronyms spelled out or wrong
- Technical terms mangled
- Foreign words anglicized incorrectly
- Heteronyms (read/read) wrong

**Root Cause**
Text-to-speech must convert text to phonemes, but many words have ambiguous or unusual pronunciations. Names, acronyms, foreign words, and domain terms often aren't in the TTS lexicon. Heteronyms (same spelling, different pronunciation based on meaning) require context understanding. Without custom pronunciation rules, TTS guesses incorrectly.

**Example**
```
Scenario: Customer service voice agent

Text: "Your representative is Siobhan McLeod"
TTS output: "See-oh-ban Mc-Lee-odd"
Correct: "Shiv-awn Mc-Cloud"

Text: "Please check your AWS S3 bucket"
TTS output: "Please check your A-W-S S-three bucket"
Should be: "Please check your AWS S-three bucket"

Text: "The résumé will be reviewed"
TTS output: "The re-zoom will be reviewed"
Context: Written document, not "continue"

Text: "Navigate to San José"
TTS output: "San Josey" (should be "San Ho-zay")

Pronunciation error analysis:
  Names: 25% error rate
  Acronyms: 30% error rate  
  Foreign words: 35% error rate
  Heteronyms: 20% error rate
  Technical terms: 15% error rate

Business impact:
  - Customer name wrong: Trust damage
  - Product name wrong: Confusion
  - Command wrong: Failed action
```

**Key Statistics**
From TTS Research (2026):
- Name pronunciation errors: 20-30%
- Acronym errors: 25-35%
- Heteronym errors: 15-25%
- Foreign word errors: 30-40%
- Custom lexicon reduces errors by 80%

**Pronunciation Error Types**
| Type | Example | Cause |
|------|---------|-------|
| Name | "Ng" → "Nug" | Unknown phonetics |
| Acronym | "SQL" → "S-Q-L" vs "Sequel" | Ambiguous |
| Heteronym | "read" (present vs past) | Context needed |
| Foreign | "José" → "Jo-see" | Wrong language rules |
| Technical | "OAuth" → "Oh-auth" | Domain term |

**Contributing Factors**
- Limited TTS lexicon
- No custom pronunciation dictionary
- No context for heteronyms
- Missing SSML phoneme tags
- No language detection
- No domain-specific training

**Mitigation Strategies**
1. **Custom lexicon**: Add domain terms and names
2. **SSML phonemes**: Specify exact pronunciation
3. **Context modeling**: Use context for heteronyms
4. **Language tags**: Mark foreign words with language
5. **Acronym handling**: Define pronunciation per acronym
6. **Regular auditing**: Review common mispronunciations

**Detection**
- Sample and review TTS output
- Track user corrections ("It's pronounced...")
- Monitor complaint keywords
- Compare against pronunciation dictionary
- Survey name pronunciation satisfaction

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - TTS issues
- [SSML Specification](https://www.w3.org/TR/speech-synthesis11/) - Pronunciation markup
- [Google Cloud TTS: Custom Voice](https://cloud.google.com/text-to-speech/docs/ssml) - Customization
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Speech issues
