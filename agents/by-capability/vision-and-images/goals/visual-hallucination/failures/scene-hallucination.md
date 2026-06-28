# Scene Hallucination

## Issue: Vision Model Detects Entire Scenes or Complex Contexts Not Present in Image

**Frequency**: Rare but High-Impact

**Symptoms**
- Model outputs detailed description of scene elements that don't exist
- Hallucinated scene elements are contextually plausible (e.g., "people in meeting room" when only furniture visible)
- Agent makes decisions based on hallucinated scene context
- Severe impact when safety/compliance decisions depend on scene understanding

**Root Cause**
Vision models learn strong statistical associations about typical scene compositions. When presented with ambiguous or partial visual evidence, the model's prior about "what scenes typically contain" overrides visual grounding. This is especially pronounced when the model is prompted to describe scenes (caption generation), which amplifies hallucination compared to simple object detection.

**Example**
```
Scenario: Safety compliance agent checking office occupancy for evacuation

Image: Office with desks, computers, chairs, but no people (after-hours)

Model caption: "Meeting in progress with 5 people discussing documents at table"

Agent action: Marks office as occupied, delays evacuation alarm

Reality: Office is empty (desks empty, just furniture visible)

Impact: Evacuation delay, potential safety risk
```

**Key Statistics**
- Scene hallucination rate: 5-10% on images with minimal human figures or activity
- Occurs in 15-20% of cases when model is asked to describe rather than detect
- Hallucination confidence: avg 72% despite 40% actual incorrectness rate

**Contributing Factors**
- Scene captioning task (description) vs. detection (class labels)
- Partial visual evidence enabling multiple valid interpretations
- Model temperature/diversity settings
- Training on curated datasets with common scene compositions

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Empty scenes | Image of empty room | "Empty room" or low-confidence description | Model describes activity/people not present |
| Sparse scenes | Few objects in frame | Accurate minimal description | Hallucinated context or additional elements |
| Ambiguous scenes | Shadows, reflections, occlusions | Careful hedging or uncertainty | Confident description with unwarranted detail |
| Temporal hallucination | Static image | No past/future events | Model describes actions (running, talking) not visible |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Scene Accuracy | >90% | % of scene descriptions matching human annotation |
| Hallucination Rate | <5% | % of sentences in output not grounded in visual evidence |
| Temporal Grounding | 100% | % of described actions actually visible in image |

---

## Mitigation Strategies

### Prevention
1. **Visual Grounding**: Require model to cite visual evidence for each claim (e.g., "people detected at [coordinates]")
2. **Captioning Caution**: Use detection-based summaries instead of free-form captions for safety-critical decisions
3. **Conservative Language**: Train model to use hedging language ("appears to", "possibly") for low-confidence claims
4. **Negative Examples**: Train on deliberately empty/sparse scenes to teach model to recognize and describe emptiness

### Detection & Response
1. **Textual Grounding Check**: For each hallucinated element, verify it appears in bounding boxes or spatial coordinates
2. **Cross-Modal Validation**: Audio (mic) or occupancy sensors (PIR) cross-check claimed presence of people
3. **Caption Confidence**: Separate confidence score for overall scene description vs. individual elements

### Architecture Patterns
1. **Hybrid Approach**: Use object detection for high-stakes decisions (people, hazards); use captions for low-stakes context
2. **Evidence-Based Summaries**: Generate summary only from detected objects, not hallucinated context
3. **Human Review**: Route scene descriptions for safety decisions to human review

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `vision.hallucination_rate` | >5% |
| `vision.ungrounded_claims` | >2 per caption |
| `sensor.audio_people_mismatch` | Model detects people, audio disagrees |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Safety-Critical Hallucination | Hallucinated people/activity in safety zone | P1 |
| Ungrounded Scene Description | Described elements not in bounding boxes | P2 |
| Temporal Hallucination | Described action not visible in static image | P2 |

---

## References

- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2)
- [Vision and Language Grounding](https://arxiv.org/abs/2212.14843)
- [Mitigating Hallucinations in Vision-Language Models](https://arxiv.org/abs/2402.05655)
