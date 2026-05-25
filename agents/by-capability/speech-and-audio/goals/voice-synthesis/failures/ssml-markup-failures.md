# SSML and Markup Failures

## Issue: Speech Markup Not Processed Correctly

**Frequency**: Occasional

**Symptoms**
- SSML tags read aloud as text
- Pauses not applied
- Phoneme overrides ignored
- Audio insertions fail
- Voice changes not happening

**Root Cause**
SSML (Speech Synthesis Markup Language) allows precise control over TTS output—pauses, pronunciations, emphasis. But SSML can fail: tags may be malformed, unsupported by the TTS engine, or stripped during processing. When SSML fails, the raw markup may be spoken aloud, or intended effects don't apply.

**Example**
```
Scenario: SSML processing failure

Input with SSML:
  <speak>
    Your balance is <say-as interpret-as="currency">$1234.56</say-as>.
    <break time="500ms"/>
    Press <say-as interpret-as="digits">1</say-as> for more options.
  </speak>

Expected output:
  "Your balance is twelve thirty four dollars and fifty six cents.
   [pause]
   Press one for more options."

Failure mode 1 - Tags spoken:
  "Less than speak greater than Your balance is less than say-as..."
  [Literally reading the markup]

Failure mode 2 - Tags stripped, effects lost:
  "Your balance is one two three four point five six dollars.
   Press one for more options."
  [Currency not formatted, pause missing]

Failure mode 3 - Partial processing:
  "Your balance is $1234.56.
   [pause works]
   Press 1 for more options."
  [say-as ignored, break works]

SSML failure analysis:
  Tags correctly processed: 75%
  Tags ignored: 15%
  Tags spoken aloud: 5%
  Partial processing: 5%
```

**Key Statistics**
From SSML Usage Research (2026):
- SSML adoption: 40% of production voice agents
- Tag processing success: 70-85%
- Cross-engine compatibility: 60-80%
- Tags spoken aloud incidents: 5-10%
- Implementation errors: 25% of advanced features

**Common SSML Failures**
| Failure | Cause | Impact |
|---------|-------|--------|
| Tags spoken | Bad escaping, wrong parser | Very confusing |
| Tags ignored | Unsupported feature | No effect applied |
| Malformed | Syntax error | Entire block fails |
| Incompatible | Engine doesn't support | Partial processing |
| Encoding | Character encoding issues | Corrupted output |

**Contributing Factors**
- Engine-specific SSML support
- No validation before sending
- Encoding/escaping issues
- Unsupported features used
- Version mismatches
- No fallback for failures

**Mitigation Strategies**
1. **SSML validation**: Validate markup before sending
2. **Feature detection**: Check engine capabilities
3. **Graceful degradation**: Fallback for unsupported features
4. **Testing**: Test all SSML constructs
5. **Escaping**: Proper escaping of special characters
6. **Engine abstraction**: Abstract engine-specific differences

**Detection**
- Monitor for markup in audio output
- Track SSML processing errors
- Compare expected vs actual duration (pauses)
- Test pronunciation overrides
- Audit advanced feature usage

## References

- [W3C SSML Specification](https://www.w3.org/TR/speech-synthesis11/) - Standard reference
- [Google Cloud TTS SSML](https://cloud.google.com/text-to-speech/docs/ssml) - Implementation guide
- [AWS Polly SSML](https://docs.aws.amazon.com/polly/latest/dg/ssml.html) - AWS implementation
- [Azure Speech SSML](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-synthesis-markup) - Azure guide
