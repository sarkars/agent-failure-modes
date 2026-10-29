# AI Image Wrong Shadows and Reflections: Check the Light and Physics Before You Publish

<!-- SEO
title: AI Image Wrong Shadows, Reflections and Physics: How to Catch Them
description: AI images show shadows pointing different ways, mirrors reflecting wrong things and impossible physics. Check with lines, not a glance, before you publish.
search phrases:
- ai image wrong shadows
- ai generated image shadows inconsistent
- ai image reflection wrong in mirror
- how to tell if an image is ai shadows
- ai image impossible physics
- dall-e shadows and reflections
- ai virtual staging mirror reflection wrong
- ai generated photo lighting looks off
-->

**Frequency**: Common

## Issue: AI image tools draw shadows that point in different directions, mirrors that reflect something that is not in the room and scenes that break simple physics (a seesaw balanced under an elephant), and people rarely notice at a glance. Flag every photo-style image with hard shadows, mirrors or shiny surfaces, or weight and support, check it with lines drawn on the image, fix or simplify the scene and have a named person sign off.

> **One line:** A Scottsdale patio furniture brand posts an AI shot of its new dining set where the umbrella's shadow falls one way, the chairs' shadows another and the pool reflects a table that is not there; the fix is to draw shadow and reflection lines on every image like it before it ships, fix the broken region or change the light, and record a person's check.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. All opened studies and the incident are still images. The goal also covers video; video physics is not part of this page. |
| **Channel** | Text-to-image tools, AI editing and virtual staging features, and assistants that call them, used for ads, social posts, product shots and property listings |
| **Stakes** | Medium. A wrong shadow or reflection marks an image as fake to anyone who looks closely, and in a property listing it can show a room that does not exist (our judgment, supported by the incident in section 4). |
| **Who is affected** | People who see the ad or listing, buyers and renters who rely on it, and the brand or agent whose name is on it |
| **Frequency** | Common in tests on one model: in 2022, every sunny-day DALL-E 2 image Farid analyzed had shadows that did not fit one sun, and 22 of 25 mirror images had reflections obviously disconnected from the scene (section 4). No opened source gives a rate for current models or for published business images. |
| **Pattern ID** | ai-image-generator-broken-shadows-reflections-and-impossible-physics |
| **Family** | [AI Image Artifacts: Hands, Anatomy and Physics](../README.md) |
| **Goal** | AI images and video show bodies, objects and motion that could exist: correct hands and anatomy, shadows and reflections that match, and physics that holds. |
| **Primary metric** | Unchecked-or-defective light-and-physics publish rate: published photo-style AI-made or AI-edited images that contain cast shadows, mirrors or reflective surfaces, or objects resting on or balanced against each other, where no light-and-physics check was recorded or a later review finds a shadow, reflection or physics error, divided by all such published images. Proposed starting target: 0. |
| **Maturity** | Researched; tests written, not yet run. Evidence is one arXiv preprint and one blog post by the same forensics researcher, one arXiv benchmark preprint and one news report of a suspected AI listing photo. |
| **Will a better model fix this?** | Partly. Farid expected larger models might learn consistent geometry, but the newest model in these sources (DALL-E 3, 2024) still drew a balanced seesaw, and no opened source tests current models, so keep the check (our judgment). |
| **Also searched as** | AI photo shadows going two directions · AI mirror reflection wrong · virtual staging fake reflection · how to spot AI image lighting |

Tests: [AI image generator broken shadows, reflections and impossible physics test file](../../../tests/ai-image-generator-broken-shadows-reflections-and-impossible-physics.md).

## 1. In plain words
A patio brand wants a sunny shot of its new dining set by a pool. The AI picture looks bright and real. But the umbrella's shadow goes left, the chairs' shadows go right, and the pool reflects a table that is not on the deck. Nobody sees it on a phone. A customer does, and posts it. The tool never built a 3D scene with one sun, so nothing forced the light to agree. Eyes are bad at catching this. Lines drawn on the image are not.

## 2. What it looks like
The brand, people and files below are invented.

**Without the fix**
```
Marketer:  Make a photo of our Mesa dining set on a pool deck, bright sun, for Instagram.
Assistant: Here is your image. (Umbrella shadow falls left, chair shadows fall right,
           and the pool reflects a second table.)
Marketer:  Looks great. Scheduling it for 10 a.m.
           (That afternoon)
Commenter: Two suns? And where's the table in the pool coming from? Is this set even real?
Marketer:  Pulling it. Can we get a real photo by Friday?
```
**With the fix**
```
Marketer:  Make a photo of our Mesa dining set on a pool deck, bright sun, for Instagram.
Assistant: Done. It has hard sun shadows and a pool reflection, so I ran the light check.
           Shadows: umbrella and chair lines do not meet at one sun. Reflection: the pool
           shows a table that is not on the deck. I fixed the shadow and pool regions and
           checked again: all shadow lines meet; the pool shows only the real set.
           Options: use the fixed version; switch to a shaded, overcast look with soft
           shadows; use the studio photo of the set; something else.
Marketer:  Use the fixed version.
Assistant: Sent to Luis Ortega (brand) to re-check the lines and approve before 10 a.m.
```
The fixed version names what it checked, shows the defect, repairs only those regions, checks again, offers other ways out and ends with a named person.

## 3. Why it happens
- **No 3D scene and no single light.** Farid notes that "paint by text is not based on explicit geometric modeling," so nothing forces every shadow to come from one sun or every reflection to obey the mirror. His result: shadows and structures are "locally consistent, but globally inconsistent."
- **Reflections are rarer in training images.** Farid says DALL-E 2 "struggles to synthesize plausible reflections, presumably because such reflections are less common in its training image data set."
- **The tool follows words, not physics.** PhyBench's authors conclude current models are "primarily focused on text-to-image translation," lacking reasoning about physical commonsense; when the prompt spelled the physics out, scores rose. The human eye does not save you: Farid's abstract points to its "often obliviousness to even glaring geometric inconsistencies."

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Of 25 DALL-E 2 images of "three cubes on a sidewalk photographed on a sunny day," "in all cases, the cast shadows are not physically consistent with a scene illuminated by a single light source," though they looked plausible. The cloudy-day prompt gave no shadows. | [Farid, "Perspective (In)consistency of Paint by Text," arXiv 2206.14617](https://arxiv.org/abs/2206.14617) (June 2022), full text on [ar5iv](https://ar5iv.labs.arxiv.org/html/2206.14617), opened Oct 29, 2026 | Preprint; one model (DALL-E 2), one prompt, 25 images, analysis by the author. Image counts read from the ar5iv rendering. |
| Of 25 images for "a photo of a toy dinosaur and its reflection in a vanity mirror," "in all but three cases, the reflection was obviously disconnected from the scene"; two plausible-looking ones still failed the geometric test. Kitchen floors were consistent but counters did not share their vanishing line. | Farid, as above | Same limits. Newer models are not tested. |
| A point on an object, its shadow and the light lie on one line, so lines from shadows to objects should meet at the light; lines from objects to their mirror reflections should meet at one point. Correct lens distortion first. "Today's AI-generated images seem to struggle to produce perspectively correct shadows and reflections." Farid expects larger models may fix this. | [Hany Farid, "Photo forensics from lighting, shadows and reflections," Content Authenticity Initiative blog, Sept 14, 2023](https://contentauthenticity.org/blog/photo-forensics-from-lighting-shadows-and-reflections), opened Oct 29, 2026 | Explainer by the same researcher; single-source for the method on this page. Examples are DALL-E 2. |
| PhyBench: 700 prompts in 31 physical scenarios (mechanics, optics, thermodynamics, materials) on six models (DALL-E 2, DALL-E 3, Midjourney, Gemini, SD XL, SD 3). Models usually drew the scene but "performance on physical correctness is generally poor," except optics. DALL-E 3 drew "a balanced seesaw with an elephant and a mouse on either side." Rewriting prompts to state the physics "can significantly improve" accuracy. | [Meng et al., "PhyBench," arXiv 2406.11802v3](https://arxiv.org/html/2406.11802v3) (revised Sept 21, 2024), HTML opened Oct 29, 2026 | Preprint. Scored by GPT-4o with human checks. Several numbers are garbled in the HTML, so only counts confirmed in the page source are used. |
| PhyBench found models did well on simple optics (light in straight lines, scattering), while Farid found broken shadows and reflections. | PhyBench and Farid, as above | Our reading: PhyBench scores whether the effect appears; Farid tests whether its geometry agrees. Do not read "optics passed" as "reflections are safe." |

**Incident (US, AI use suspected, not confirmed):** On Feb 18, 2026, Futurism reported a rental listing in Fort Totten, Washington, DC, whose bathroom photo showed a disfigured figure in the mirror and an ottoman in the middle of the floor; Reddit users suggested AI image editing, the photo carried an MLS watermark with no sign of AI editing, and the listing was taken down from Apartments.com. Source: [Victor Tangermann, Futurism, Feb 18, 2026](https://futurism.com/artificial-intelligence/realtor-ai-photo-mirror), opened Oct 29, 2026. A search summary said J.Crew's August 2025 AI campaign had "a misplaced reflection"; the opened [Futurism report, Aug 31, 2025](https://futurism.com/j-crew-ad-faked-ai) and [Aperture, Jan 23, 2026](https://aperture.org/editorial/fashion-photographys-ai-reckoning/) do not mention reflections or shadows, so that detail is unverified and not used. No public incident was found of a brand ad pulled specifically for wrong shadows.

## 5. The fix
**The principle:** One scene has one sun and one mirror rule. Check them with lines, because eyes miss it.

**Do this: teams and assistants that make or edit photo-style images**
1. **Flag images that need a light-and-physics check.** Any photo-style AI-made or AI-edited image with hard cast shadows, a mirror, window, water or other shiny surface, or objects that rest on, hang from or balance against each other is marked "light check" before anyone shows it as final.
2. **Check shadows with lines.** For a scene lit by sun or one strong lamp, draw lines from at least three shadow points to the matching object points (after correcting lens distortion). They must meet at one point, and every object touching the ground in sun has a shadow. Record pass or fail per image.
3. **Check reflections with lines.** Every object in front of a mirror or calm water appears in it, nothing appears that is not in the scene, and lines from at least three object points to their reflections meet at one point. Record pass or fail.
4. **Check the physics the scene implies.** Write down what must be true (the heavier end is down, the glass is supported, the liquid is level) and check it. When regenerating, state the physics in the prompt, as PhyBench's rewrites did.
5. **A person signs the check.** A vision model may pre-screen (proposed), but no opened source shows one can draw these lines reliably, and Farid notes people miss errors at a glance, so the record is a person's line check.
6. **Fix only the broken region, then change the light if needed.** Repaint the shadow or reflection area, then check again; stop at a limit the team sets (3 tries is our proposed starting point). After that, offer an overcast or shaded scene (Farid's cloudy prompt gave no hard shadows), remove the mirror or shiny surface, or use a real photo.
7. **Re-check every new version.** Each AI edit, virtual staging pass, crop or resize gets its own check. For property listings, mirrors and windows are always checked.
8. **Log it.** Per image: version, checks run (shadow, reflection, physics), result, fix method and tries, checker, approver and date.

**Reference design: light-and-physics check before sign-off**
| Check | Pass | Example |
|---|---|---|
| Flag | Hard shadows, reflective surface or support present | Pool deck shot flagged: sun, pool |
| Shadows | 3+ lines meet at one point | Umbrella and 2 chairs: fail, then pass after fix |
| Reflections | All objects present, nothing extra, lines meet | Extra table in pool: fail, then pass |
| Physics | Written expectation met | Umbrella base on deck, not floating |
| Version | Check on the exact file that runs | 1080x1350 post file |
| Sign-off | Named, dated | L. Ortega, Oct 29, 2026 |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every flagged image: give the shadow, reflection and physics result before anything else |
| Offer choices: 2-4 options plus "Something else", free text open | A defect remains after the try limit: overcast look, no mirror or shiny surface, real photo, something else. Not when the check passed. |
| Ask one clarifying question | The light is unclear: "Is this one sun outdoors, or a room with several lamps?" |
| Hand off to a person | Always for the line check and sign-off on anything published |

**Don't over-correct.** Do not flag flat lighting, overcast scenes or images with no visible cast shadows. A room with several lamps can cast several shadows in different directions; apply the one-point test per light, not to the whole room. Curved mirrors, rippled water and frosted glass do not follow the flat-mirror test; judge them by eye and note it (our judgment; no opened source tests them). Do not apply photo rules to an illustration or a style that ignores light on purpose. Do not remove every mirror and window from every scene as a reflex; in a property listing that would hide the real room.

**Hand-off rule.** If anyone reports a wrong shadow, reflection or impossible scene in a published image, the content owner pulls every copy the same day and sends the log to the approver. For a property listing, the listing agent also checks the photo against the real room. The [viral ad mistakes page](../../ai-image-generation-business-risks/failures/ai-image-mistakes-in-ads-go-viral.md) covers the public correction.

**Framework used:** none yet. Rules 2 and 3 follow Farid's shadow and reflection tests; rule 4 follows PhyBench's prompt rewrites; rule 5 follows Farid's note on human perception; rule 6's overcast option follows Farid's cloudy-day result; rule 7 follows the DC listing incident; rules 1 and 8 and the try limit are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-generator-broken-shadows-reflections-and-impossible-physics.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Sunny pool deck with umbrella and chairs | Flagged; shadow lines drawn and recorded | 1, 2 |
| 2 | Mirror shows an object not in the room | Caught; region fixed and re-checked | 3, 6 |
| 3 | "Elephant and mouse on a seesaw," seesaw level | Physics fail recorded; prompt states the physics on retry | 4 |
| 4 | Only a vision model said "lighting looks fine" | Publish blocked until a person checks | 5 |
| 5 | Virtual staging adds a bathroom mirror after approval | New check on the staged version | 7 |
| 6 | Overcast street scene with soft shadows | Not flagged | Over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unchecked-or-defective light-and-physics publish rate** (primary) | 0 (proposed) | Monthly sample of published flagged images: no check in the log, or a reviewer's line check fails / all sampled | Any |
| Flagged versions published without their own check | 0 (proposed) | Publish log: version that ran vs version with a recorded check | Any |
| Region-fix tries per flagged image | Track, no target | Generation log: tries before a pass or the switch to another scene | Rising for 2 months |
| False light flags (counter-metric) | Track, no target | Sample of flagged images marked "no defect: multiple lights, curved surface or intended style" | Rising for 2 months |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Prompt or edit names sun, mirror, pool, window or glass and the image has no light check | Prompt log plus check log | The image came out overcast or the surface is not visible; flag was correctly skipped |
| Virtual staging or AI edit applied to a listing photo and published without a new check | Editor history plus listing feed | Color-only edit, logged as such, with a check still recorded |
| Comments mention "shadow," "reflection," "mirror," "two suns" or "AI" | Social comments, listing inquiries | Deliberate surreal or stylized art |
| Ad paused or listing photo replaced within 48 hours of going live | Platform activity log | Scheduled end date or a price or wording change |

**Starter rule:** no photo-style AI-made or AI-edited image with hard shadows, a reflective surface or objects in support is published unless the log shows a person's line check on that exact version and a named sign-off.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-generator-broken-shadows-reflections-and-impossible-physics
runs: [post_generation, post_edit, pre_publish]
reads: [image.photo_style, image.version, image.ai_edited, image.hard_shadows, image.reflective_surface, image.support_or_balance, check.shadow_lines, check.reflection_lines, check.physics_expectation, fix.method, fix.tries, review.checker, review.signoff, scene.light_count]
trigger: flagged and no check on this version, or any check fails, or try limit reached, or no sign-off at publish
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Switch to an overcast or shaded look", "Remove the mirror or shiny surface", "Use a real photo", "Something else"]
on_miss: block_publish
metric: unchecked-or-defective light-and-physics publish rate
counter_metric: false light flags
status: proposed
```

## 8. Related patterns
- [AI image generator wrong hands, fingers and anatomy](ai-image-generator-wrong-hands-fingers-and-anatomy.md) - the closest existing page and the same check-before-publish shape. That page counts fingers and limbs on bodies; this one tests the whole scene's light and support with lines, and applies even when no person is in the image.
- [AI ad mistakes that go viral](../../ai-image-generation-business-risks/failures/ai-image-mistakes-in-ads-go-viral.md) - what to do once a defective ad is public.
- [AI product images show features it does not have](../../ai-image-generation-business-risks/failures/ai-product-images-show-features-it-does-not-have.md) - the false-advertising side, which an invented room in a listing can also raise.
- [AI image generator puts objects in the wrong position](../../ai-image-prompt-adherence/failures/ai-image-generator-puts-objects-in-the-wrong-position.md) - a placement the prompt asked for; here the prompt is met and the light or physics is wrong.
- [Quality drift in generated images](../../generation-artifacts/failures/quality-drift.md) and [artifact accumulation](../../generation-artifacts/failures/artifact-accumulation.md) - older pages on images getting worse over steps and regenerations; a broken shadow is there in the first image.

## 9. Common questions
### Why are shadows wrong in AI images?
The tool does not build a 3D scene with one light. It paints each part to look right on its own, so shadows can look fine locally and still point to different suns.

### How do I check shadows in an AI image?
Pick three or more points where a shadow ends and the matching point on the object. Draw a line through each pair. In a real sunlit photo the lines meet at one point, the light; if they don't, the shadows are inconsistent.

### Why does the mirror show the wrong thing in AI images?
Mirror reflections are rarer in training photos, Farid suggests, and the tool has no mirror rule. Check that everything in front of the mirror is in it, nothing extra is, and object-to-reflection lines meet at one point.

### Can AI virtual staging put fake things in listing mirrors?
A DC rental photo showed a disfigured figure in a bathroom mirror, and Reddit users suspected AI editing; it was not confirmed. Check every staged or edited listing photo's mirrors and windows before it goes live.

### Do newer AI image generators get physics right?
Not reliably in the sources we opened: in PhyBench (2024), DALL-E 3 drew a balanced seesaw under an elephant and a mouse. Stating the physics in the prompt helped, but still check the result.
