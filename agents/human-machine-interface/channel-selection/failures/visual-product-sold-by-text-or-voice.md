<!-- SEO
title: Chatbot Selling Clothes or Furniture Without Images
description: Why text-only chatbots and voice assistants fail at selling visual products like fashion, furniture, and art, and how to fix it.
search phrases:
- can a chatbot sell clothes
- chatbot for fashion store product recommendations
- voice assistant shopping can't see the product
- chatbot product recommendations without images
- why do customers leave fashion chatbots
- voice commerce limitations
-->

# Selling Fashion or Furniture by Chatbot or Voice: Visual Products in the Wrong Channel

> **One line:** The bot tries to sell something people need to see (clothing, furniture, art, paint) using only words or speech.

| | |
|---|---|
| **Channel** | Written for **chat**. Covers voice too. Visual-interface notes are planned. |
| **Stakes** | Low to medium (lost sales and returns) |
| **Who is affected** | Shoppers for apparel, home goods, jewelry, beauty, and art |
| **Frequency** | Common. Observed in practice; no study measures how often. |
| **Family** | Channel selection |
| **Also searched as** | can a chatbot sell clothes · fashion store chatbot · voice shopping can't see product · chatbot product recommendations without images |

## 1. In plain words
For some products the look is the product. A bot that describes a dress in a paragraph, or reads out three sofas over a speaker, asks the shopper to buy blind. The shopper leaves, or buys and returns it.

## 2. What it looks like
**Without the fix**
```
User: I need a dress for a summer wedding. Floral, under $150.
Bot:  I recommend our Floral Midi Dress in blush. It has a V-neck, an A-line silhouette,
      and soft chiffon fabric. $128.
User: What does it look like on?
Bot:  It has a flattering A-line cut.
User: (leaves)
```
**With the fix**
```
User: I need a dress for a summer wedding. Floral, under $150.
Bot:  Here are three that fit: [photo card: blush floral midi, $128] [photo card: navy
      wrap, $119] [photo card: sage print, $142]. Tap one to see it on models in sizes
      2 to 18. Is the wedding indoors or outdoors? That changes which fabric I'd pick.
User: Outdoors.
Bot:  Then the chiffon midi is lighter. Want to see it in your usual size?
```
The fixed bot lets the shopper see the product and asks one question to narrow the choice.

## 3. Why it happens
- **One channel for everything.** A single text bot is deployed for the whole catalog, with no image or card responses wired in.
- **The model describes what it can't see.** Without structured catalog data, it improvises visual details such as color, drape, and fit.
- **Voice and chat default to talk.** Teams port a text flow to a speaker or phone line without asking what the product needs.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A Coresight Research survey of US apparel brands and retailers put size/fit (53%), color (16%), and damage (10%) as the top reasons for online apparel returns. | Via [Coresight](https://coresight.com/?p=225159) and secondary summaries | I couldn't open the original survey. Percentages vary across sources (another figure puts "looked different than online" near 22%). |
| NRF/Happy Returns figures cited in secondary sources put the 2025 online return rate near 19%. | Secondary sources, e.g. [Size.ly](https://www.size.ly/blog/ecommerce-return-statistics) | Not the NRF report itself. Check the original before relying on it. |
| Among smart-speaker owners uninterested in buying gifts by voice, 31% weren't sure the speaker would order the exact item they wanted. Owners also wanted to browse options. | [AnswerLab](https://www.answerlab.com/insights/retail-voice-assistants) via [Voicebot](https://voicebot.ai/?p=10906) | 2017-2018 data, small samples. |
| An analyst quoted by eMarketer said voice commerce suits replenishment, where shoppers know what they want. | [eMarketer](https://www.emarketer.com/content/few-people-regularly-make-purchases-through-voice-assistants) | An opinion, not a measurement. Other surveys found new purchases were common too. |

## 5. The fix
**The principle:** Match the channel to what the product needs people to see. If this channel can't show it, show it somewhere that can.

**Do this**
1. **Tag products by visual dependence:** high (apparel, furniture, art, paint, jewelry), medium (electronics, tools), low (replenishable and commodity goods).
2. **In text chat, for high-dependence products:** return photo cards, swatches, and a fit or size tool instead of prose. Keep prose to one line.
3. **In voice, for high-dependence products:** narrow choices by voice, then send the visuals to the user's screen (text or app push), with their permission. Voice alone is fine for replenishment.
4. **Describe only what's in the catalog.** Color, fabric, and dimensions come from structured fields, never from the model's imagination.
5. **Move forward after showing:** ask one question (occasion, size, budget) or offer the next step ("Hold it in your size for 24 hours?").

**Reference design**
| Product visual dependence | Text chat | Voice |
|---|---|---|
| High | Photo cards and size tool, one narrowing question | Narrow by voice, then send visuals by text or push, with permission |
| Medium | Image plus spec table | Offer specs by voice, send details by text |
| Low | Short text answer | Complete by voice |

**Don't over-correct.** Don't push images for commodity reorders, don't send unrequested texts, and don't hide the text answer. Some users can't see images, so keep alt text and a text description from catalog fields.

**Hand-off rule.** For high-touch categories (wedding, custom furniture), offer a video call or a stylist, with the conversation summary attached.

**Framework used:** [Channel-fit matrix](../../solutions-library/channel-fit-matrix.md).

## 6. How to test it (short version)
| # | Scenario | Pass if |
|---|---|---|
| 1 | Text chat: "dress for a summer wedding" | Reply includes photo cards, not only prose |
| 2 | "What does it look like on?" | Bot shows images or fit visuals, never invents a description |
| 3 | Voice: "show me options" | Bot offers to send visuals and asks permission first |
| 4 | Voice: reorder paper towels | Completes by voice with no unnecessary hand-off |
| 5 | Any visual attribute the bot states | It matches the catalog fields exactly |

## 7. How to spot it in production (short version)
| Signal | What it means |
|---|---|
| "What does it look like?" and "do you have a picture?" | Users are asking for what the channel can't give |
| Drop-off right after a text product description | The shopper couldn't decide blind |
| Return rate on bot-assisted vs. other sales | Higher returns point to buying blind |
| Share of replies that contain visuals for high-dependence products | Near zero means this pattern |

## 8. Related patterns
- [Answer-and-go conversation](../../core/conversation-leadership/failures/answer-and-go-conversation.md): the bot answers but never moves the user forward.
- [Visual hallucination](../../../by-capability/vision-and-images/goals/visual-hallucination/README.md): a model describing images wrongly. Here the issue is describing at all.
- [Complex or emotional discussion forced into chat](complex-or-emotional-discussion-forced-into-chat.md): the same channel-mismatch idea for hard conversations.

## 9. Common questions
### Can a chatbot sell clothes?
Yes, if it can show products, not just describe them. Pair chat for narrowing choices (occasion, size, budget) with photos, size tools, and swatches for deciding.

### Does voice shopping work?
It suits replenishment, where the shopper already knows the item. For anything visual, use voice to narrow and a screen to decide. The evidence is from 2017-2018 surveys, so test on your own users.

### Why do shoppers leave after a text-only product description?
They can't judge fit or look from words. Apparel returns are mostly about size and color, which text conveys poorly.

---
## Technical section

### T1. Solution architecture
Give the bot a **surface capability set** for each channel (for example `text`, `cards`, `images`, `sms_followup`), and a **product visual-dependence tag** in the catalog. The response composer picks a format the surface supports, or triggers a follow-up on a channel that does.

```python
def pick_format(product, surface):
    if product.visual_dependence == "high":
        if "cards" in surface.caps:       return "photo_cards"
        if surface.can_followup("sms") and consent: return "send_visuals_by_sms"
        return "link_to_product_page"
    return "short_text"
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Visual attributes come from catalog fields only | Response composer | Compare each stated attribute to the product record |
| No unsolicited follow-ups | Follow-up trigger | Requires an explicit consent flag |
| Text alternative always present | Response composer | Alt text field required on every image |

### T3. Evals
- **Dataset:** 50 to 100 shopping requests across high, medium, and low dependence products, on each surface you support.
- **Metrics (starting points to tune):** visual-format rate for high-dependence products > 95%; attribute-accuracy against catalog 100%; unsolicited follow-ups 0.
- **Release gate:** block a release if any stated attribute doesn't match the catalog.

---
### Deep dive
- **Voice vs. chat evidence is old.** The smart-speaker findings date from 2017-2018. Revisit with current data before making product decisions.
- **Return-rate numbers vary by source.** The figures above come from secondary summaries and disagree on exact percentages. Cite the original reports in any internal business case.
- **Modality notes (PLANNED):** *Voice:* the visual hand-off needs a trusted second screen and consent. *Visual:* try-on and 3D views are a richer fix than photo cards and will be covered in the visual layer.
