# Test File: AI Image Generator Misspells Text in Images

**Pattern:** [AI Image Generator Misspells Text: Garbled Words on Signs, Posters and Menus](../goals/ai-image-prompt-adherence/failures/ai-image-generator-misspells-text-in-images.md)
**Pattern ID:** ai-image-generator-misspells-text-in-images
**Goal:** AI images and video show what the prompt asked for: the right number of objects, in the right places, with the right attributes and readable text.
**Primary metric:** Unproofed-or-misspelled text publish rate: published AI images with readable words where no word-by-word proof against approved copy was recorded, or any word differs from it, divided by all published AI images with readable words (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's image workflow (the generator, the assistant that writes prompts, the design template, the proofreader and the publish gate) shows the failure. They are not a text-rendering score for any vendor. Run them in a test workspace and publish only to a test page. All companies, people, prices and files below are invented. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Flag text-bearing requests | Request with quoted words or a sign, menu, poster, flyer, label, slide or banner marked "text matters" before generating | Not flagged |
| R2 | 2. Set information text | Prices, dates, times, addresses, phone numbers, URLs, names, menu items and text over 5 words set in a design tool, not generated | Any of these drawn by the generator |
| R3 | 3. Words from approved copy | Copy taken from the requester's text or approved brief, quoted once; never retyped from the image | Copy retyped from the image or changed |
| R4 | 4. Proof every readable word | Each word compared with approved copy and the result recorded; a person makes the final read | No proof, or OCR result used alone |
| R5 | 5. Remove stray text | Readable words not in the request blanked, removed or replaced with approved copy | Stray words left in the published image |
| R6 | 6. Fix by editing, then stop | Wrong headline fixed by text edit or setting; regeneration stops at the team's limit | Regenerates without limit or ships the error |
| R7 | 7. Named full-size proof | Recorded proof by a named person at print or display size before publish | Published without it |
| R8 | 8. Log it | Log has approved copy, method, proof result per word, stray text removed, reviewer, date | Any field missing |
| O | Don't over-correct | DNS cases run with no text flag, proof or block | Flagged, proofed or blocked |

## Test cases
1. **Menu board with prices (R1, R2).**
   Setup: Test workspace for "Lone Star Tacos" (fake), an Austin food truck.
   Action: Ask: "Chalkboard menu: Brisket Taco $4.50, Al Pastor Taco $3.75, Horchata $3.00."
   Pass: Flagged; chalkboard art generated with a blank panel; items and prices set in a template.
   Fail: Item names or prices drawn by the generator.
2. **Copy source (R3).**
   Setup: Same request as case 1.
   Action: Read the template text and the prompt as sent in the log.
   Pass: Text matches the owner's message exactly, including "$4.50"; nothing retyped from an image.
   Fail: A word or price differs from the owner's message.
3. **Short generated headline with a typo (R4, R6).**
   Setup: "Bayou Books" (fake), a New Orleans bookstore, asks for a window poster headline "Grand Opening Saturday"; seed a result reading "Grand Opennig Saturday."
   Action: Run the workflow.
   Pass: Proof catches "Opennig"; fixed with a text-edit tool or set in the design tool; the proof is recorded.
   Fail: Image offered as final with the typo.
4. **Retry limit (R6).**
   Setup: Retry limit set to 2; seed two results with misspelled headlines.
   Action: Run the workflow.
   Pass: Stops after two; says what was wrong; offers to set the words, fix them with a text-edit tool, move them to the post text, or something else.
   Fail: A third generation runs automatically.
5. **Stray gibberish (R5).**
   Setup: A Phoenix coffee shop (fake) asks for "a cozy cafe interior with our sign 'Desert Bean Coffee'"; seed a result with a readable gibberish chalkboard behind the counter.
   Action: Run the workflow.
   Pass: Gibberish board blanked or removed before the image is offered as final.
   Fail: Published with the gibberish board.
6. **Event flyer with date and address (R2).**
   Setup: A Columbus community center (fake) asks for a flyer: "Fall Festival, Saturday Nov 14, 10 a.m. to 2 p.m., 400 Oak St."
   Action: Run the workflow.
   Pass: Date, time and address set in the design tool; only art generated.
   Fail: Any of them generated.
7. **OCR only (R4, R7).**
   Setup: OCR reports every word matches; no person has proofed.
   Action: Try to publish to the test page.
   Pass: Blocked until a named person proofs.
   Fail: Published on the OCR result alone.
8. **OCR false alarm (R4).**
   Setup: A correctly spelled headline in a script font that OCR misreads.
   Action: Run the proof step.
   Pass: The person confirms the word is correct against the approved copy; the image is not regenerated for that word.
   Fail: Regenerated or rejected on the OCR result alone.
9. **Slide with a chart title (R1, R2).**
   Setup: A Seattle startup (fake) asks for "a title slide image that says 'Q3 Revenue Up 12%'."
   Action: Run the workflow.
   Pass: Flagged; the number is set, not generated.
   Fail: "12%" drawn by the generator.
10. **Full-size proof (R7).**
    Setup: A menu board approved from a phone-size thumbnail only.
    Action: Try to send it to the test print queue.
    Pass: Blocked until a proof at print size is recorded.
    Fail: Sent to print.
11. **Log fields (R8).**
    Setup: Any approved text-bearing image.
    Action: Read its log.
    Pass: All listed fields present.
    Fail: Any field missing.
12. **DNS: no words requested (O).**
    Setup: Ask for "a blurred Chicago street at night, rainy, neon glow."
    Action: Generate.
    Pass: No text flag or proof required; unreadable background signage left alone.
    Fail: Flagged as text-bearing or blocked.
13. **DNS: invented lettering on purpose (O).**
    Setup: Ask for "a fantasy map with made-up runes along the border, no real words."
    Action: Generate.
    Pass: No proof against copy; no block.
    Fail: Runes flagged as misspellings.
14. **DNS: internal draft (O).**
    Setup: A poster concept saved as "draft, not for publishing" with a generated placeholder headline.
    Action: Save to the team's concept board.
    Pass: Saved with no block.
    Fail: Blocked or forced through proof.
15. **DNS: number that is decoration (O).**
    Setup: Ask for "a 1950s diner exterior with a neon sign."
    Action: Generate.
    Pass: "1950s" not treated as information text; no forced setting step.
    Fail: Flagged as a date to set and proof.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Cases 1, 6 and 9 follow the Adobe Community Manager reply (generate without text, add it afterward) and CapCut's help page (add real text with the text editor). Cases 3 and 4 follow Adobe's "Edit text in image" advice; the retry limit of 2 and the 5-word headline cutoff are the page's proposals. Cases 7 and 8 follow Liu et al. (arXiv 2212.10562), whose hand check found OCR flagged correctly spelled words as errors. Case 5 follows the gibberish words in the "Willy's Chocolate Experience" images reported by NBC News and Hyperallergic (February 2024). Searches run for this page: "AI image generator misspelled text sign poster garbled letters," "text rendering benchmark text-to-image OCR accuracy spelling 2025 arXiv," "AI-generated poster misspelled words backlash company apologizes 2025," "Willy Wonka experience Glasgow AI images gibberish text," "STRICT benchmark stress test rendering long text image generation arXiv 2025." Cases 2, 10, 11 and 12 to 15 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
