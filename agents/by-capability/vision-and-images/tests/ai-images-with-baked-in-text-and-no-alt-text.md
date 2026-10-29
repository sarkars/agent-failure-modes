# Test File: AI Images With Baked-In Text and No Alt Text

**Pattern:** [AI Images With Baked-In Text and No Alt Text: Prices and Dates Screen Readers Cannot Read](../goals/ai-image-generation-business-risks/failures/ai-images-with-baked-in-text-and-no-alt-text.md)
**Pattern ID:** ai-images-with-baked-in-text-and-no-alt-text
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Unreadable-text rate: published images with information text in the pixels whose alt text is missing, empty, a file name, or not carrying that text, divided by all published images with information text sampled (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a publishing workflow (AI generator, copy sheet, CMS, email builder, social scheduler and live read-back) shows the failure. They do not test whether any site or post meets the ADA, WCAG or any other law; that is for a qualified reviewer. Run them on a staging site, a test email list and an unpublished or private social account, and never let a test post reach the public. All brands, people, copy sheets and IDs below are invented. Covers image and video. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting. Where a test reads alt text, check it with a screen reader (for example NVDA or VoiceOver) as well as the markup.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Information text live where the channel allows | On web and HTML email, prices, dates, hours and calls to action are live text; the art has no text | Offer exists only in the image pixels |
| R2 | 2. Overlay from approved copy when text must be in the image | Image text is overlaid from the copy sheet | Generator draws the information text |
| R3 | 3. Alt text from the copy, same words | Alt carries every information word from the copy sheet | Alt is a vague description, an auto-caption, or OCR of AI pixels that misses or misspells words |
| R4 | 4. Classify every image | Informative, linked, logo or decorative class set; alt fits the class | Missing alt, file name, "image," or empty alt on an image with text |
| R5 | 5. Block on a failed check | Failed image held on every channel and size; others proceed | Failed image publishes, or the whole batch is held |
| R6 | 6. Check the live version | Alt read back from the live page or post matches the publish log | Alt lost after publish goes unnoticed |
| R7 | 7. Video says what the screen shows | On-screen-only price, date, phone or URL is spoken or in the caption or description text | Information appears only as on-screen text |
| R8 | 8. Log every check | Log has image ID, channel, class, copy ID, alt text, read-back result, approver, date | Missing log or fields |
| O | Don't over-correct | Logos, decorative images and image-only social posts with good alt pass; no keyword stuffing or "Image of" | Decorative image given long alt, logo blocked, or alt padded with keywords |

## Test cases
1. **Web banner with the offer in the prompt (R1).**
   Setup: Prompt for "Prairie Fresh Market" (fake) home page banner: "BOGO chicken thighs, $2.99/lb, Sat-Sun only."
   Action: Generate and build the page.
   Pass: Art has no text; the offer appears as live text on the page from copy sheet C-2291.
   Fail: The offer exists only inside the image.
2. **Instagram post that needs text in the image (R2, R3).**
   Setup: Same offer for a 1080x1080 Instagram post; copy sheet C-2291 exists.
   Action: Generate, overlay and schedule.
   Pass: Text overlaid from C-2291; alt text contains the price, days and stores in the same words.
   Fail: Generator draws the text, or alt omits any of those words.
3. **Blank alt field (R4, R5).**
   Setup: Image with text uploaded to the CMS with the alt field left empty and not marked decorative.
   Action: Publish.
   Pass: Blocked with the reason shown.
   Fail: Publishes.
4. **File-name alt (R4).**
   Setup: Alt field auto-filled as "promo_gen_8812.png."
   Action: Publish.
   Pass: Blocked.
   Fail: Publishes; a screen reader reads the file name.
5. **Alt misses the price (R3).**
   Setup: Alt reads "Chicken thighs on a cutting board, weekend sale."
   Action: Run the publish check.
   Pass: Blocked; the missing "$2.99 a pound" and days are named.
   Fail: Passes.
6. **Alt copied from misspelled pixels (R3).**
   Setup: Generator drew "Satruday" in the image; alt is built from OCR of the image.
   Action: Run the publish check.
   Pass: Alt built from the copy sheet; the image is flagged for the spelling mismatch.
   Fail: Alt repeats "Satruday."
7. **Linked banner (R4).**
   Setup: Home page banner image is the link to the weekly ad; no link text.
   Action: Run the publish check.
   Pass: Alt names the destination or action, such as "See this week's ad," plus the offer.
   Fail: Link announced as an image or file name.
8. **Alt lost on cross-post (R6).**
   Setup: Scheduler posts to Instagram and cross-posts to Facebook; the cross-post drops alt text.
   Action: Run live read-back.
   Pass: Facebook post flagged and routed to the content owner.
   Fail: Not detected.
9. **Email hero image (R1, R4).**
   Setup: HTML email with the offer drawn into the hero image and images blocked in the test inbox.
   Action: Open the email.
   Pass: Offer readable as live text or alt text with images off.
   Fail: Reader sees an empty box.
10. **Video with on-screen-only phone number (R7).**
    Setup: 15-second AI-made video shows "Call 555-0147 to order" on screen; the voiceover never says it; no caption covers it.
    Action: Run the video check.
    Pass: Flagged; number added to voiceover or caption or description text.
    Fail: Passes.
11. **No copy sheet (hand-off).**
    Setup: Image with "Open late Friday until 10 p.m." and no copy sheet.
    Action: Publish.
    Pass: One question asks whether the text is information or decoration; held and routed to the content owner.
    Fail: Publishes with alt the tool wrote itself.
12. **Log completeness (R8).**
    Setup: Run tests 1 to 11.
    Action: Export the publish log.
    Pass: Every check has all fields listed in R8.
    Fail: Any check missing or with blank fields.
13. **DNS: decorative texture (O).**
    Setup: AI-made background texture with no text, marked decorative.
    Action: Publish.
    Pass: Empty alt accepted.
    Fail: Blocked, or long alt forced on it.
14. **DNS: logo (O).**
    Setup: Store logo image with the brand name as alt.
    Action: Publish.
    Pass: Passes; alt is the brand name without "logo of" padding.
    Fail: Blocked as an image of text.
15. **DNS: good alt on an image-only post (O).**
    Setup: Instagram graphic with text overlaid from the copy sheet and alt carrying the same words.
    Action: Publish.
    Pass: Passes with no change.
    Fail: Blocked for having text in the image, or alt rewritten with keywords or "Image of."

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Tests 1 and 9 follow WCAG 2.2 SC 1.4.5 (text rather than images of text). Tests 2 to 5 follow SC 1.1.1 and the W3C images tutorial's statement that alt text for an image of text must contain the same text. Test 7 follows WebAIM's finding that many images missing alt text are linked images, leaving links with no description. Tests 13 and 14 follow the SC 1.1.1 decoration exception and the SC 1.4.5 note that logotypes are essential. Test 10 is our judgment, not a cited rule. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
