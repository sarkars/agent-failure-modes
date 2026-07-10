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

## Mitigation Strategies

### Prevention
1. **Custom Pronunciation Lexicon**: Maintain a domain-specific lexicon (names, acronyms, product terms, technical jargon) with explicit phonetic overrides, checked and applied before falling back to the TTS engine's default grapheme-to-phoneme guessing — directly targeting the ~80% error reduction custom lexicons provide. Trade-off: lexicon maintenance is an ongoing content-ops burden as new names/terms enter the domain.
2. **SSML Phoneme Tags for High-Stakes Terms**: For terms where mispronunciation causes real harm (customer names, safety-critical instructions), explicitly wrap them in SSML `<phoneme>` tags with IPA or engine-specific phonetic strings rather than relying on lexicon lookup alone, since lexicons can miss inflected or compound forms.
3. **Context-Aware Heteronym Disambiguation**: Use surrounding context (part-of-speech, semantic role) to select the correct pronunciation for heteronyms ("read" past vs. present, "résumé" vs. "resume") rather than defaulting to the most frequent reading regardless of context.

### Detection & Response
1. **User-Correction Signal Capture**: Detect and log explicit user corrections ("It's pronounced...", "no, that's...") during conversations, feeding them directly into the pronunciation lexicon review queue rather than letting them go unrecorded.
2. **Automated Output Sampling Against Known Terms**: Regularly synthesize a test set of known-tricky terms (enrolled customer names, product names, acronyms) and compare output phonetically against expected pronunciation, catching regressions from TTS engine/version upgrades before they reach users.
3. **Complaint Keyword Monitoring**: Track feedback mentioning mispronunciation specifically, segmenting by term category (name vs. acronym vs. foreign word vs. technical term) to prioritize lexicon additions where they'll have the most impact.

### Architecture Patterns
1. **Lexicon-First Synthesis Pipeline**: Insert a lexicon lookup/override stage between text normalization and the TTS engine's default G2P (grapheme-to-phoneme) conversion, so any term with a known override always bypasses the engine's guess.
2. **Per-Customer Name Pronunciation Storage**: For contexts with enrolled/known users (support agents, personalized assistants), store a per-customer phonetic override for their name (potentially self-provided at signup) rather than relying on a generic lexicon to guess every possible name.
3. **Engine Abstraction for Cross-Provider Lexicon Portability**: Maintain the custom lexicon in an engine-agnostic format (e.g., IPA) with a translation layer to each TTS provider's specific SSML/phoneme dialect, so lexicon investment isn't lost when switching or multi-sourcing TTS engines.

### Metrics
1. **name_pronunciation_error_rate_percent**: Target: < 5% (down from ~25% baseline); Alert threshold: > 15%
2. **lexicon_coverage_percent**: Target: > 95% of known high-frequency terms/names in lexicon; Alert threshold: < 80%
3. **user_correction_rate_percent**: Target: < 3%; Alert threshold: > 10%
4. **heteronym_disambiguation_accuracy_percent**: Target: > 90%; Alert threshold: < 70%

### Alerts
1. **Pronunciation Regression After Engine Upgrade** (P1): Condition - automated known-term test set shows increased mispronunciation rate after a TTS engine/version change. Action: Verify lexicon compatibility with new engine version, roll back if unresolved before next release.
2. **High-Frequency Term Missing from Lexicon** (P3): Condition - a term/name appears in user-correction logs 3+ times without a lexicon entry. Action: Add to lexicon review queue, prioritize by frequency.
3. **Heteronym Accuracy Drop** (P2): Condition - heteronym disambiguation accuracy on eval set falls below 70%. Action: Review context-model changes, retrain/tune disambiguation logic.

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - TTS issues
- [SSML Specification](https://www.w3.org/TR/speech-synthesis11/) - Pronunciation markup
- [Google Cloud TTS: Custom Voice](https://cloud.google.com/text-to-speech/docs/ssml) - Customization
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Speech issues
