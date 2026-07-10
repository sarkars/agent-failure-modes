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

## Mitigation Strategies

### Prevention
1. **Pre-Send SSML Validation**: Validate all SSML against the target engine's supported schema (well-formedness plus feature support) before sending to synthesis, rejecting or auto-correcting malformed markup rather than discovering failures only when tags are spoken aloud in production. Trade-off: strict validation can reject valid-but-unusual markup if the schema definition is incomplete or outdated relative to the engine's actual support.
2. **Engine Capability Feature Detection**: Maintain an explicit capability matrix per TTS engine/version (which SSML tags and attributes are supported) and generate markup only using features known-supported for the target engine, rather than assuming a single SSML dialect works everywhere. Trade-off: requires maintaining and updating the matrix as engines add/drop features across versions.
3. **Proper Escaping of Special Characters**: Systematically escape XML special characters (`&`, `<`, `>`, quotes) in any dynamically inserted content (names, addresses, user-provided text) before embedding into SSML templates, preventing malformed markup from user-controlled input.

### Detection & Response
1. **Spoken-Markup Detection**: Run automated detection on synthesized audio/transcript output for literal markup fragments ("less than speak greater than," raw tag names) which indicates a parsing failure; treat any occurrence as a P1-class defect given how jarring and unprofessional it sounds to end users.
2. **Duration-Based Pause Verification**: For SSML `<break>` and pause-related tags, programmatically verify the actual synthesized audio duration reflects the expected pause length, catching silent pause-tag failures that don't produce spoken markup but simply drop the intended effect.
3. **Cross-Engine Regression Testing on Feature Add/Change**: Whenever a new SSML construct is added to templates or an engine version changes, run the full SSML construct test suite against that specific engine/version combination before deployment, rather than assuming prior validation still holds.

### Architecture Patterns
1. **Engine Abstraction Layer with Per-Engine Templates**: Generate an internal, engine-agnostic markup representation and compile it to each specific TTS provider's actual SSML dialect at synthesis time, isolating template authors from engine-specific quirks and enabling safe multi-engine or failover support.
2. **Graceful Degradation for Unsupported Features**: When a requested SSML feature isn't supported by the current engine/version (per the capability matrix), degrade gracefully to the closest supported equivalent (e.g., use punctuation-based pause instead of `<break>`) rather than silently dropping the feature or failing the whole request.
3. **CI-Gated SSML Test Suite**: Maintain an automated test suite covering every SSML construct in active use, run against every engine/version in the supported matrix as a deployment gate, catching cross-engine incompatibilities before they reach production traffic.

### Metrics
1. **ssml_validation_pass_rate_percent**: Target: 100% of sent markup passes pre-send validation; Alert threshold: < 99%
2. **spoken_markup_incident_rate_percent**: Target: 0%; Alert threshold: > 0% (any occurrence triggers investigation)
3. **tag_processing_success_rate_percent**: Target: > 95%; Alert threshold: < 85%
4. **pause_duration_accuracy_percent**: Target: > 95% of breaks within 10% of expected duration; Alert threshold: < 80%

### Alerts
1. **Markup Spoken Aloud** (P1): Condition - any instance of literal SSML tags detected in synthesized output. Action: Immediate rollback of the responsible template/engine change, hotfix escaping/validation gap.
2. **SSML Feature Regression After Engine Upgrade** (P1): Condition - tag-processing success rate drops after a TTS engine/version upgrade. Action: Check capability matrix against new engine version, roll back upgrade if unresolved.
3. **Validation Bypass** (P2): Condition - markup reaches synthesis without passing the pre-send validator (pipeline bug). Action: Audit synthesis call sites for validator bypass, patch pipeline.

## References

- [W3C SSML Specification](https://www.w3.org/TR/speech-synthesis11/) - Standard reference
- [Google Cloud TTS SSML](https://cloud.google.com/text-to-speech/docs/ssml) - Implementation guide
- [AWS Polly SSML](https://docs.aws.amazon.com/polly/latest/dg/ssml.html) - AWS implementation
- [Azure Speech SSML](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-synthesis-markup) - Azure guide
