# Test File: AI Image Text in the Wrong Script or Broken Right-to-Left

**Pattern:** [AI Image Text in the Wrong Script or Broken Right-to-Left: Arabic, Hebrew and Chinese Promos That Readers Cannot Read](../goals/ai-image-generation-business-risks/failures/ai-image-text-wrong-script-or-broken-right-to-left.md)
**Pattern ID:** ai-image-text-wrong-script-or-broken-right-to-left
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Unchecked non-English text rate: published images with words in a language other than English that have no logged approval from a fluent reader of that language, divided by all sampled published images with non-English text (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's image workflow (the generator prompt step, an internal assistant or design tool that adds text, the image record and the print and publish gate) shows the failure. They are not a score for any vendor's model. Run them on test files and a test print queue; do not send anything to a real printer or post to a live account. All businesses, people, copy IDs and log IDs below are invented. A fluent reader of each test language is needed to grade tests 2, 3, 4 and 6. Covers image. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Generate art with no text | Non-Latin-script request produces art with no model-drawn text, or drawn text is removed | Model-drawn non-Latin text stays in the image |
| R2 | 2. Typeset the words | Text added as a text layer in a font that supports the script | Text comes from generator pixels |
| R3 | 3. Use approved copy | Text matches a copy ID approved by a translator or fluent staff member | Generator's own translation used |
| R4 | 4. Right-to-left layout | Arabic and Hebrew layouts read right to left; numbers stay left to right | Left-to-right layout or reversed numbers |
| R5 | 5. Check for leftover English | No unintended English words remain | English left in the target-language image |
| R6 | 6. Fluent reader approves final image | Reader name, language and date logged against the exported image | No approval, or approval of the copy doc only |
| R7 | 7. Hold until approval | Print and publish blocked without R6 | Print or publish proceeds |
| R8 | 8. Latin-script languages | Spanish image still gets approved copy and reader check | Spanish skipped as "the model can spell it" |
| H | Hand-off rule | Published image with model-drawn non-Latin text or no approval is pulled and sent to reader and owner same business day | Left up |
| O | Don't over-correct | Brand names, numbers and art-only changes proceed without extra review | Blocked or sent for translation |

## Test cases
1. **Arabic flyer request (R1, R3).**
   Setup: Test store "Warren Avenue Market, Dearborn" (fake). No approved Arabic copy on file.
   Action: Prompt: "Make an Eid sale flyer in Arabic: Eid Mubarak, 20% off lamb, Fri-Sun."
   Pass: Art is made with no text; the assistant asks for approved copy or offers to send to the translator.
   Fail: Returns a flyer with Arabic-looking text drawn by the generator.
2. **Hebrew copy supplied (R2, R4).**
   Setup: Approved Hebrew copy C-5120 (fake) with a price "$14.99" and a phone number.
   Action: Ask for a Passover catering post using C-5120.
   Pass: Text layer in a Hebrew-capable font; layout reads right to left; price and phone number read left to right; a fluent reader confirms.
   Fail: Letters in reverse order, or the price digits reversed.
3. **Model draws Chinese anyway (R1).**
   Setup: Prompt for a Lunar New Year banner art "with no text."
   Action: Generate, then run the post-generation scan.
   Pass: Any drawn characters are flagged and removed before the approved Chinese copy is overlaid.
   Fail: Drawn characters remain beside or under the overlay.
4. **Leftover English in Spanish (R5, R8).**
   Setup: Approved Spanish copy C-6001 (fake) for a back-to-school sale; generator art includes the word "SALE" on a sign.
   Action: Produce the final Instagram image.
   Pass: "SALE" flagged and removed or replaced from the approved copy; reader checks the image.
   Fail: Published with "SALE" in English.
5. **Machine translation offered as copy (R3).**
   Setup: No approved copy. The user says: "Just translate it yourself into Arabic."
   Action: Ask for the flyer.
   Pass: Draft translation is labeled a draft and routed to a fluent reader before use; it is not typeset as final.
   Fail: The assistant's translation is typeset and marked ready.
6. **Approval of copy only (R6).**
   Setup: Translator approved copy C-7710 in a document; nobody saw the exported image.
   Action: Ask to send the flyer to print.
   Pass: Blocked until the reader approves the exported image at final size.
   Fail: Printed on the copy approval alone.
7. **No reader logged (R7).**
   Setup: Finished Arabic flyer, image record has no reader approval.
   Action: Schedule the Facebook post and submit the print order.
   Pass: Both blocked, with the reason shown.
   Fail: Either goes through.
8. **Right-to-left page layout (R4).**
   Setup: Approved Arabic copy for a three-step "how to order" graphic with arrows.
   Action: Generate the graphic.
   Pass: Steps and arrows run right to left.
   Fail: Arabic words correct but steps run left to right.
9. **Published with model-drawn text (H).**
   Setup: A test post already live with Arabic text drawn by the generator and no approval.
   Action: Run the weekly sample.
   Pass: Post pulled; reader and campaign owner notified the same business day.
   Fail: Left up or only noted.
10. **DNS: brand name and numbers only (O).**
    Setup: English flyer whose only non-English element is the store's own Arabic logo file, supplied as a vector.
    Action: Make the flyer.
    Pass: Logo placed from the file; no translation request; English text follows the normal workflow.
    Fail: Sent to a translator or blocked.
11. **DNS: art-only change (O).**
    Setup: Approved Arabic flyer; only the background photo is swapped; text layer untouched.
    Action: Re-export.
    Pass: No new reader review required; change logged.
    Fail: Blocked for re-review.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | H | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |

## Notes
Tests 1 and 3 follow the Adobe Community Manager's suggestion to make the image without text and add the caption afterward, read on October 29, 2026. Tests 2 and 8 follow W3C's explanation that numbers run left to right inside right-to-left text, and the OpenAI forum report of correct Arabic in a left-to-right layout. Test 6 follows the MULTITEXTEDIT finding that errors sit in script fidelity while layout looks fine. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
