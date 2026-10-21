# Test File: Visual Product Sold by Text or Voice

This file is a set of chat test conversations for people who build or review a shopping assistant, and want to check whether it sells clothing, furniture, art or paint with words alone.

**Pattern:** [Visual Product Sold by Text or Voice](../goals/channel-selection/failures/visual-product-sold-by-text-or-voice.md)
**Pattern ID:** visual-product-sold-by-text-or-voice
**Goal:** Each interaction happens in the channel that fits the job, and switching never costs the user their context.
**Primary metric:** Visual-format rate for high-visual-dependence products: replies that include cards, images or a visual follow-up, divided by all such replies. Starting target: over 95% (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and amounts below are invented. Text chat only; the voice rule is planned and not tested here. The setup holds what the harness shows the agent: the catalog record, the product's visual-dependence tag and what the chat surface can display.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Products are tagged by visual dependence | A high-dependence product (apparel, furniture, art, paint, jewelry) is handled as visual; a low one is handled as plain text | A sofa is described like a commodity, or a reorder gets a photo gallery |
| R2 | 2. In text chat, high-dependence products get photo cards, swatches or a fit tool, with one line of prose | Cards or images first; one line of prose | Prose only, or a paragraph with the images tacked on |
| R3 | 3. In voice, narrow by voice, then send visuals with permission | Planned (voice). Not tested in this file | Planned (voice). Not tested in this file |
| R4 | 4. Describe only what is in the catalog | Color, fabric and size match the catalog fields; a gap is admitted | An invented color, drape, fit or dimension |
| R5 | 5. Move forward after showing | One narrowing question or one next step, only when it changes what to show | No next step, a question that changes nothing, or two questions |
| R6 | Hand-off rule: high-touch categories | A video call or stylist is offered with a summary; none for plain reorders or if the user wants to stay | No offer for a wedding or custom order, or a hand-off on a reorder |
| R7 | Don't over-correct | No images for commodity reorders; no unrequested texts; the text answer and alt text stay | Images on a reorder, an unasked follow-up, or text removed |

## Conversations
1. **Dress for a wedding (R1, R2).**
   Setup: Fake retailer "Harbor & Pine" (fake). Dresses are tagged high dependence. The surface shows photo cards. Three dresses fit the request.
   User: "I need a dress for a summer wedding. Floral, under $150."
   Expect: Photo cards for the matching dresses with one line of prose.
   Failing reply: "I recommend our Floral Midi Dress. It has a V-neck and soft chiffon fabric." No card.

2. **Sofa tagged high (R1).**
   Setup: Same retailer. The "Alder" sofa (fake) is tagged high dependence. Cards are available.
   User: "do you have a gray three-seat sofa"
   Expect: Photo cards of gray three-seat sofas, treated as a visual product.
   Failing reply: "Yes, the Alder is a gray three-seat sofa with a firm seat." Prose only.

3. **Paper towels tagged low (R1).**
   Setup: Same retailer. "Hearth paper towels, 6 pack" (fake) is tagged low dependence. The user ordered it before.
   User: "add my usual paper towels"
   Expect: A short text answer that the item is added. No gallery.
   Failing reply: Four photo cards of paper towels and a swatch picker.

4. **Prose where cards were possible (R2).**
   Setup: Same retailer. Cards are available. A user asks about a high-dependence item.
   User: "show me wool coats in camel"
   Expect: Photo cards first, then one line.
   Failing reply: Three paragraphs on collar styles and lining. No images.

5. **Look and fit question (R2, R4).**
   Setup: Same retailer. The blush floral midi has photos on models in several sizes. The catalog has no field for how it drapes.
   User: "What does it look like on?"
   Expect: Shows the model photos and the size tool. Does not describe drape.
   Failing reply: "It has a flattering A-line cut that skims the hips."

6. **Color not in the catalog (R4).**
   Setup: Same retailer. The catalog lists the Alder sofa color as "slate". The user asks for a different word.
   User: "is that sofa more of a charcoal or a blue-gray"
   Expect: Says the catalog lists it as slate, and shows the swatch and photos so the user can judge.
   Failing reply: "It's a warm charcoal with blue undertones."

7. **Size stated wrong (R4).**
   Setup: Same retailer. The catalog gives the Alder sofa width as 84 inches.
   User: "will the sofa fit a 90 inch wall?"
   Expect: States 84 inches from the catalog and shows the dimensions.
   Failing reply: "It's about 90 inches wide, so it should fit."

8. **Next step after showing (R5).**
   Setup: Same retailer. Cards for three dresses have just been shown. The fabric changes by season.
   User: "Those are nice. The wedding is in July."
   Expect: One question that changes the pick, such as indoors or outdoors, or one next step such as holding a size.
   Failing reply: "Great! Let me know if you need anything else." No next step.

9. **Question that changes nothing (R5).**
   Setup: Same retailer. Cards have just been shown. Every dress comes in the same fabric.
   User: "ok, show me the navy one again"
   Expect: Shows the navy dress. No new question about fabric or occasion.
   Failing reply: "Is it for indoors or outdoors? What is your budget? What size are you?" Three questions.

10. **Wedding, high touch (R6).**
    Setup: Same retailer. A stylist video call is available. The user is choosing a bridesmaid dress for six people.
    User: "I'm buying for my whole wedding party, six people"
    Expect: Cards, then an offer of a stylist video call with the conversation summary attached.
    Failing reply: Cards only and no offer, or "Please call us and explain it again."

11. **No hand-off for a reorder (R6, R7).**
    Setup: Same retailer. The user reorders a low dependence item and says they want to stay in chat.
    User: "reorder my towels, I'll stay here"
    Expect: The reorder is done in chat. No stylist or call is offered.
    Failing reply: "This looks complex. Let me connect you with a stylist."

12. **Do nothing special: unrequested text (R7).**
    Setup: Same retailer. The user has not consented to texts. Cards are shown in chat.
    User: "ok thanks, I'll look at these"
    Expect: A short close. No text message and no email is sent.
    Failing reply: "I've also texted you these photos so you don't lose them." No consent on file.

13. **Do nothing special: user cannot see images (R7).**
    Setup: Same retailer. The user uses a screen reader. Each image has alt text and a catalog description.
    User: "I use a screen reader. what does the sage print look like"
    Expect: Reads the alt text and catalog description, and keeps the cards. No invented detail.
    Failing reply: "Just look at the photo above."

## Cannot be judged from a transcript alone
- **Visual-format rate.** It needs reply-format fields and visual-dependence tags across many sessions. Thirteen conversations do not measure it.
- **Attribute accuracy.** A transcript shows the claim, not the catalog record. It needs the record compared with each stated attribute.
- **Return rates.** It needs returns joined to conversation IDs.
- **Consent for follow-ups.** It needs the consent flag on each follow-up event.
- **Voice and visual-interface flows.** R3 is planned. This file is text only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
