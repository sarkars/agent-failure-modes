# Brand and Term Mispronunciation

## Issue: TTS Mispronounces Brand Names, Domain Terms, or Key Phrases

**Frequency**: Very Common

**Symptoms**
- Brand names sound wrong ("Zapp Chess" → "Zap Chest")
- Domain terms mangled ("HIPAA" → "hip-ah")
- Acronyms expanded incorrectly
- Foreign words anglicized inappropriately
- Numbers/codes read incorrectly (version "2.0" → "two point oh")

**Root Cause**
Text-to-speech systems use grapheme-to-phoneme models trained on general text. Brand names, technical terms, and domain-specific vocabulary often have non-standard pronunciations. Without explicit pronunciation guidance (SSML, lexicons, or phonetic hints), TTS applies default rules that produce incorrect or awkward pronunciations.

**Example**
```
Scenario 1: Brand name confusion

Brand: "Zapp Chess"
Expected: "Zap Chess" (short 'a', chess as board game)
TTS produced: "Zap Chest" (misheard 'chess' as 'chest')

Other attempts:
- "Zapp" → "Zap-pee" (doubled consonant confusion)
- "Chess" → "Chase" (vowel substitution)

---

Scenario 2: Domain terms

Medical: "HIPAA compliance"
Expected: "hip-ah"
TTS: "hi-pah-ah" (treated as word, not acronym)

Legal: "GDPR"
Expected: "G-D-P-R" (spelled out)
TTS: "gid-per" (attempted pronunciation)

Tech: "OAuth"
Expected: "oh-auth"
TTS: "oh-ath" (wrong vowel)

---

Scenario 3: Product versions

"Version 2.5"
Expected: "version two point five"
TTS: "version twenty-five" (misread decimal)

"iOS 17.4.1"
Expected: "iOS seventeen point four point one"
TTS: "iOS one seven four one" (digit by digit)

---

Scenario 4: Names and places

"Jamia Millia Islamia" (Indian university)
Expected: Local pronunciation
TTS: Anglicized pronunciation, unrecognizable

"Vellore Institute of Technology"
Expected: "Vell-ore"
TTS: "Veh-lore" or "Vel-lore"

---

Mispronunciation analysis (1,000 calls):
  Total brand mentions: 2,340
  Correct pronunciation: 1,872 (80%)
  
  Error types:
    Vowel substitution: 45%
    Consonant confusion: 25%
    Stress misplacement: 15%
    Acronym expansion: 10%
    Number format: 5%
```

**Key Statistics**
From TTS Pronunciation Research (2026):
- Brand name accuracy without hints: 60-75%
- Domain term accuracy: 50-70%
- Acronym handling errors: 20-35%
- User confusion from mispronunciation: 25-40%
- Brand perception impact: 15-20% negative

**Common Mispronunciation Types**
| Type | Example | Error |
|------|---------|-------|
| Similar sounds | Chess → Chest | Phoneme confusion |
| Doubled letters | Zapp → Zap-pee | Phonotactic error |
| Acronyms | GDPR → "gidper" | Not spelled out |
| Foreign words | Jamia → anglicized | Cultural mismatch |
| Numbers | 2.5 → twenty-five | Format confusion |

**Contributing Factors**
- No custom lexicon for brand terms
- Missing SSML pronunciation hints
- TTS trained on general corpus
- Regional pronunciation variants ignored
- Acronym vs. word ambiguity
- Version/number format detection failure

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Brand name | "Zapp Chess" | "Zap Chess" | "Zap Chest/Chase" |
| Acronym | "GDPR" | Spelled out | Pronounced as word |
| Version | "v2.5" | "version two point five" | "v twenty-five" |
| Domain term | "OAuth" | "oh-auth" | "oh-ath" |
| Local name | University name | Correct local pronunciation | Anglicized |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Brand pronunciation | > 98% | Human eval on recordings |
| Acronym handling | > 95% | Spelled vs. pronounced |
| Number format | > 95% | Correct reading |
| Domain terms | > 90% | Phonetic accuracy |

---

## Mitigation Strategies

### Prevention
1. **Custom lexicons**: Define pronunciation for brand terms
2. **SSML markup**: Use phoneme tags for critical words
3. **STT key terms**: Ensure ASR also recognizes terms correctly
4. **Phonetic spelling**: Write terms as they should sound
5. **TTS model selection**: Choose models with relevant language support
6. **Pronunciation testing**: Audio QA for key terms before launch

### Implementation
```python
class PronunciationManager:
    """Manage pronunciation for brand and domain terms"""
    
    # Custom lexicon with IPA and alternative spellings
    LEXICON = {
        "Zapp Chess": {
            "phonetic": "Zap Chess",  # How to write for TTS
            "ipa": "zæp tʃɛs",
            "ssml": '<phoneme alphabet="ipa" ph="zæp tʃɛs">Zapp Chess</phoneme>'
        },
        "GDPR": {
            "phonetic": "G D P R",
            "ssml": '<say-as interpret-as="characters">GDPR</say-as>'
        },
        "OAuth": {
            "phonetic": "oh auth",
            "ipa": "oʊ ɔːθ",
            "ssml": '<phoneme alphabet="ipa" ph="oʊ ɔːθ">OAuth</phoneme>'
        },
        "v2.5": {
            "phonetic": "version two point five",
            "ssml": '<say-as interpret-as="characters">v</say-as> 2.5'
        }
    }
    
    def __init__(self, use_ssml=True):
        self.use_ssml = use_ssml
    
    def process_text(self, text: str) -> str:
        """Replace terms with pronunciation-safe versions"""
        processed = text
        
        for term, pronunciation in self.LEXICON.items():
            if term.lower() in processed.lower():
                if self.use_ssml:
                    replacement = pronunciation.get("ssml", 
                                    pronunciation["phonetic"])
                else:
                    replacement = pronunciation["phonetic"]
                
                # Case-insensitive replacement
                import re
                processed = re.sub(
                    re.escape(term), 
                    replacement, 
                    processed, 
                    flags=re.IGNORECASE
                )
        
        return processed
    
    def add_term(self, term: str, phonetic: str, 
                 ipa: str = None) -> None:
        """Add new term to lexicon"""
        self.LEXICON[term] = {
            "phonetic": phonetic,
            "ipa": ipa,
            "ssml": f'<phoneme alphabet="ipa" ph="{ipa}">{term}</phoneme>' 
                    if ipa else phonetic
        }


# ElevenLabs specific pronunciation
class ElevenLabsPronunciation:
    """Handle ElevenLabs-specific pronunciation hints"""
    
    def __init__(self):
        # ElevenLabs pronunciation dictionary format
        self.pronunciation_dict = []
    
    def add_pronunciation(self, original: str, 
                          replacement: str) -> None:
        """Add to ElevenLabs pronunciation dictionary"""
        self.pronunciation_dict.append({
            "original": original,
            "replacement": replacement
        })
    
    def get_api_format(self) -> list:
        """Return in ElevenLabs API format"""
        return self.pronunciation_dict


# Example configuration
pronunciation_config = {
    "text_to_speech": {
        "provider": "elevenlabs",
        "pronunciation": [
            {"original": "Zapp Chess", "replacement": "Zap Chess"},
            {"original": "chess", "replacement": "chess"},  # Reinforce
            {"original": "GDPR", "replacement": "G D P R"},
        ]
    }
}
```

### SSML Examples
```xml
<!-- Brand name with phoneme -->
<speak>
  Hi, this is Riya from 
  <phoneme alphabet="ipa" ph="zæp tʃɛs">Zapp Chess</phoneme>.
</speak>

<!-- Acronym spelled out -->
<speak>
  We're <say-as interpret-as="characters">GDPR</say-as> compliant.
</speak>

<!-- Version number -->
<speak>
  You're using version 
  <say-as interpret-as="cardinal">2</say-as> point 
  <say-as interpret-as="cardinal">5</say-as>.
</speak>

<!-- Indian university name with emphasis -->
<speak>
  Are you at 
  <lang xml:lang="hi-IN">Jamia Millia Islamia</lang>?
</speak>
```

### STT Key Terms
```json
{
  "speech_to_text": {
    "keyterms": [
      "Zapp Chess",
      "Zap Chess",
      "chess",
      "Campus Ambassador",
      "WhatsApp",
      "playbook"
    ]
  }
}
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `pronunciation.brand.accuracy` | < 95% |
| `pronunciation.acronym.correct` | < 90% |
| `pronunciation.user_confusion` | > 10% |
| `pronunciation.repeat_requests` | > 8% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Brand Mispronounced | accuracy < 90% | P2 |
| High User Confusion | confusion > 15% | P2 |
| Acronym Errors | errors > 20% | P3 |

---

## References

- [W3C SSML Specification](https://www.w3.org/TR/speech-synthesis11/) - Pronunciation markup
- [ElevenLabs Pronunciation](https://elevenlabs.io/docs/speech-synthesis/pronunciation) - Custom dictionaries
- [Google Cloud TTS SSML](https://cloud.google.com/text-to-speech/docs/ssml) - SSML support
- [Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Pronunciation issues
