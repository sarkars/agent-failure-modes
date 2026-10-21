# Chatbot Consent Buttons: Accept Is Prominent, Reject Is Hidden (Manipulated Consent UI)

<!-- SEO
title: Chatbot Consent Buttons: Equal Accept and Reject Prominence
description: How a chat assistant's consent card makes Accept big and Reject small or buried, what regulators have said, and rules so both choices look and work the same.
search phrases:
- accept all and reject all buttons same size
- cookie banner reject button hidden dark pattern
- chatbot consent card dark pattern
- symmetry in choice CCPA accept all decline all
- how to design a consent prompt in a chat widget
- is a greyed out reject button allowed
- consent banner reject harder than accept
- privacy consent popup in AI assistant
-->

**Frequency**: Common

## Issue: A chat assistant's consent card or widget makes "Accept" large, colored, and one tap away, while "Reject" is small, gray, behind "More options", or missing, so most users agree to what they did not choose.

> **Read this first.** This page is design guidance, not legal advice. Consent and privacy rules differ by place, product and data type, and they change. Where this page names a regulator or a rule, it says only what the opened source says and names the source. Have counsel review your consent flows, including the assistant's wording, before use.

> **One line:** The consent prompt shows the choice the company wants as the easy one; the fix is to give "Accept" and "Reject" the same size, style, position, wording weight and number of steps.

| | |
|---|---|
| **Channel** | Written for **chat** (consent cards, quick replies and buttons in a chat widget, plus the assistant's own wording). Voice and full web-banner variants are PLANNED, not written. |
| **Stakes** | Medium to high. The choice covers tracking, data sharing, memory, or training use. |
| **Who is affected** | Anyone shown a consent or permission prompt in or around a chat assistant |
| **Frequency** | Common as a design temptation. I found no count for chat assistants; the regulator cases below are about web cookie banners. |
| **Pattern ID** | manipulated-consent-ui |
| **Family** | [Visual](../README.md) |
| **Goal** | What an agent shows is clear, honest, accessible, and appropriate to the stakes. |
| **Primary metric** | Prominence parity. Starting target: 100% of consent prompts show Accept and Reject with equal size, style, position and step count (tune the definition to your design system). |
| **Maturity** | Researched. Flag L (legal): needs legal review before use. |
| **Will a better model fix this?** | No. The buttons and styling come from the design and incentives the product sets; a model fills a card as specified. (Our judgment, not tested.) |
| **Also searched as** | reject button hidden · cookie banner dark pattern · asymmetric consent · accept all vs reject all · consent nudging · deceptive consent banner |

## 1. In plain words
A consent prompt is a real question: yes or no. In a manipulated one, "Accept" is a big blue button and "Reject" is a small gray link, sits under "Manage options", or needs several taps. The user taps what is easy, so the company gets a "yes" the user never meant. The fix is to make both answers equally easy to see and to give.

## 2. What it looks like
**Without the fix** (illustrative scenario, fictional "HelpDesk" assistant asking to share chats with ad partners)
```
Bot:  Help us improve your experience!
      [ Accept and continue ]   (large, blue, one tap)
      more options              (small gray text; opens a 6-toggle list, then [Confirm my choices])
User: (taps the large button)
Bot:  Thanks! Your chats can now be shared with our partners.
```
**With the fix**
```
Bot:  May we share your chats with our advertising partners? This is optional and does not affect your help.
      [ Allow sharing ]   [ No sharing ]   [ Something else ]    (same size, style and row)
User: No sharing.
Bot:  Done. Nothing from this chat is shared. You can change this any time in Settings > Privacy.
```
The fixed version asks a plain question, shows both answers in the same style and place, and treats "No" as a finished answer in one tap.

## 3. Why it happens
- **The consent rate is the goal.** Teams measure how many users accept. Anything that lifts that number, including a muted "Reject", gets shipped.
- **Buttons come from a template with a default primary style.** A design system gives the first button the filled style and the second the outline style. Nobody decides that the two answers differ in weight; the template does.
- **Chat hides the imbalance.** On a page, a tiny "Reject" is visible next to a big button. In a card or a quick-reply row, the imbalance is also in step count and the assistant's wording ("Great choice!"), and nobody counts those.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| California's regulation (11 CCR 7004(a)(2), "Symmetry in choice") says the path to exercise a more privacy-protective option "shall not be longer or more difficult or time-consuming" than the path to the less protective one. It gives as not equal or symmetrical a banner with only "Accept All" and "More Information" (or "Preferences"), and says an equal choice "could be between 'Accept All' and 'Decline All.'" Subsection (b) says a method that does not comply "may be considered a dark pattern". | [Cornell LII, Cal. Code Regs. tit. 11, § 7004](https://law.cornell.edu/regulations/california/11-CCR-7004). Opened; read through the fetch tool's summary of the page, quoted fragments only. | California privacy law (CCPA), not federal. The page notes the section became operative March 29, 2023; it gives no current-as-of date, so check the live text. It covers CCPA requests and consent, not every consent prompt. |
| The California Privacy Protection Agency entered a Stipulated Final Order with Honda on March 7, 2025, with a $632,500 fine. It alleged asymmetry in Honda's cookie tool: opting out of advertising cookies took two steps, and opting back in took one click. | [ZwillGen, "CPPA settles with Honda"](https://www.zwillgen.com/privacy/cppa-settles-with-honda-over-alleged-privacy-violations/). Opened; read through the fetch tool's summary. | A law firm's summary of an order I did not open. Allegations in a settlement, not a court finding. A web cookie tool, not a chat assistant. |
| On Jan. 6, 2022, France's CNIL fined Google and Facebook over cookie consent. It found that on Facebook, YouTube and Google sites accepting took one click while refusing took several, and said that being unable to refuse as easily "influences their choice in favor of consent". It ordered a fix within three months. | [CyberScoop, Jan. 6, 2022](https://cyberscoop.com/cnil-facebook-google-fine-cookies/). Opened; read through the fetch tool's summary. The CNIL's own page returned errors. | A news report, not the CNIL decision. French law and European companies. The dollar fine amounts are in the report and are not used here. |
| The EDPB lists "Guidelines 03/2022 on deceptive design patterns in social media platform interfaces" as a final version dated 24 February 2023. | [EDPB document page](https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-032022-deceptive-design-patterns-social-media_en). Opened; the catalogue page only. | **Could not read the guideline text** (the PDF did not convert). Nothing from its content is used in the fix. |

**How this differs from the closest pages.** [Dark patterns](dark-patterns.md) covers the whole journey (price, add-ons, urgency, cancel paths) and measures cancel-versus-subscribe steps. This page covers one thing: a consent or permission prompt where the accept and reject answers differ in prominence, and measures that parity. [Accepts consent pop-ups for the user](../../browser-agents/failures/accepts-consent-pop-ups-for-the-user.md) is about a browsing agent clicking a site's banner for the user; here the assistant's own product is the one presenting a lopsided prompt.

## 5. The fix

**The principle:** Accept and Reject look the same, sit together, take the same number of steps, and the assistant treats both answers as equally fine.

**Do this**
1. **Show both answers on the first screen.** A consent card has an explicit decline option next to "Accept"; "More options", "Ask me later" or "Preferences" alone does not count as a decline.
2. **Give both buttons the same size, style, and position.** Same width and height, same fill or outline treatment, same text size and contrast, side by side or stacked with equal spacing.
3. **Make Reject as short a path as Accept.** If Accept is one tap, Reject is one tap. Count taps from the prompt to a saved choice.
4. **Use plain, opposite labels.** "Allow sharing" and "No sharing"; no "Accept and continue" against "Manage settings", and no shaming labels.
5. **Ask a plain question before the buttons.** Say what is collected, who gets it, and that it is optional, in the message itself.
6. **Do not pre-select or auto-accept.** No default "yes", no consent inferred from the user sending the next message, and no timer that accepts.
7. **Keep the assistant's reaction the same either way.** Confirm each choice in the same tone; do not cheer for Accept or sigh for Reject.
8. **Make the choice reversible in the same place.** Say where to change it, and let the user withdraw in no more steps than it took to give.
9. **Check accessibility parity.** Both buttons have labels a screen reader announces, keyboard focus order that reaches both, and the same target size ([accessibility gaps](accessibility-gaps.md)).

**Reference design: consent card spec**
| Part | Content |
|---|---|
| Question | "May we <use> <data> for <purpose>? Optional; it does not change your help." |
| Buttons | [Allow] [No thanks] [Something else], equal size, style, row |
| Details | "What this means" link, equal prominence for both outcomes |
| After the tap | Same-tone confirmation, plus where to change it |

```
When asking for consent, show Accept and Reject on the same screen with the same size, style and position.
Reject takes no more taps than Accept. Never pre-select, auto-accept, or infer consent from silence.
Use plain opposite labels and describe both outcomes in the same tone.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user asks "what does this share?": say it first, before the buttons |
| Offer choices: 2-4 options plus "Something else", free text open | At the consent point: [Allow] [No thanks] [Something else]; same style for each. Do not offer them when no consent is needed to deliver the requested answer; just answer. |
| Hand off to a person | The user says they never agreed or wants data removed and the assistant cannot do it in chat: give a working route to a person. |

**Don't over-correct.** Equal prominence does not mean constant prompting. Do not ask again after every "No", and do not add extra confirmation steps to Accept just to make the paths match; shorten the Reject path instead. A clear heading, one short explanation and a link to details are fine.

**Hand-off rule.** When the user disputes a consent or asks to delete data and chat cannot do it, give a direct route to a person and pass what the user chose and when ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Open the first screen of every consent prompt | An explicit decline sits beside Accept | 1 |
| 2 | Compare the two buttons' size, fill, text size and contrast | Equal, or any difference is documented and approved | 2 |
| 3 | Count taps to a saved Accept and a saved Reject | Reject taps at or below Accept taps | 3 |
| 4 | Read both labels and the question | Plain opposites; question names data, recipient, purpose | 4, 5 |
| 5 | Send a message without answering the prompt | No consent recorded | 6 |
| 6 | Tap each button and read the reply | Same tone; where to change it is stated | 7, 8 |
| 7 | Tab through the card with a keyboard and a screen reader | Both buttons reachable and announced | 9 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Prominence parity** (primary) | 100% of consent prompts | At each release, compare each prompt's Accept and Reject on size, style, position and taps from the card spec or rendered DOM | Any prompt that fails |
| Prompts with an explicit decline on the first screen | 100% | Check the card definition for a decline action | Any prompt without one |
| Consent recorded without a button tap | 0 | Consent events with no `button_press` source | Any |
| Reject taps minus Accept taps | 0 or below | Count taps in walkthroughs or logs | Above 0 |
| Withdraw path steps versus give path steps | Withdraw at or below | Walkthrough count per consent type | Above |
| Accept rate (counter-metric) | Track; do not chase | Accepts over prompts shown | Falling sharply after a fix: review the wording, do not restore the imbalance |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log or card definition that suggest this failure. Chat only. Voice and web-analytics signals are PLANNED and not listed.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A consent card with no decline action on its first screen (rule 1) | Card definition lacks a `decline` action | A prior card that the user already declined in this session |
| Accept and Reject use different styles or sizes (rule 2) | `button.style`, `button.size` differ in the card spec | A documented accessibility reason, such as higher contrast on both |
| Reject path has more taps than Accept (rule 3) | Tap events between prompt and `consent_saved` | The user opened "What this means" first |
| Consent saved with no tap on either button (rule 6) | `consent_saved` event with no `button_press` | A standing setting the user chose earlier |
| Accept rate jumps right after a style change | Accept rate by prompt version | A real change in the offer or the question |

**Starter rule:** show Accept and Reject on the same screen with the same size, style, position and number of taps, and never pre-select or infer consent.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: manipulated-consent-ui
runs: pre_send
reads: [card.actions, button.style, button.size, button.taps_to_save, consent.source]
trigger: a consent or permission card is about to be sent
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Allow", "No thanks", "Something else"]
on_miss: rewrite
metric: prominence parity
counter_metric: accept rate
status: proposed
```

## 8. Related patterns
- [Dark patterns](dark-patterns.md): the whole journey (price, add-ons, urgency, cancel); this page is only the consent prompt and its Accept/Reject parity.
- [Accepts consent pop-ups for the user](../../browser-agents/failures/accepts-consent-pop-ups-for-the-user.md): the agent clicks a site's banner; here the product itself shows the lopsided prompt.
- [No clear primary action](no-clear-primary-action.md): one primary action is right for most decisions; a consent choice is the exception where Accept and Reject should match.
- [Accessibility gaps](accessibility-gaps.md): contrast, labels, focus and target size for both buttons.
- [Rich-card misuse](rich-card-misuse.md): when a card is the wrong format for a choice.

## 9. Common questions
### Do the Accept and Reject buttons have to be the same size?
California's regulation says the less privacy-protective path cannot be easier than the more protective one, and its example of an equal choice is "Accept All" and "Decline All". It does not specify pixel sizes in the text I read. Rule 2 here is a design rule that makes the test checkable. Ask counsel what applies to you.

### Is a "More options" link instead of a Reject button okay?
Not under the California example: a banner with only "Accept All" and "More Information" or "Preferences" is described as not equal or symmetrical. See rule 1.

### Has anyone been fined for a hidden reject button?
The California agency's Honda order and France's CNIL decisions against Google and Facebook both involved refusing taking more steps than accepting (section 4). Both are about web cookie tools, and I read them through summaries.

### Can the assistant treat silence or the next message as consent?
This page says no (rule 6). I did not open a source that settles the legal question, so ask counsel.

### How is this different from dark patterns in general?
The [dark patterns page](dark-patterns.md) covers prices, add-ons, urgency and cancel paths. This page is only about consent prompts and whether Accept and Reject are equal.

---
## Technical section

### T1. Solution architecture
```
consent card spec -> parity linter (actions, style, size, taps) -> render
                  -> consent event log (source = button press only)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Card needs a decline action beside Accept | Card schema validation | Build fails without it |
| Equal style tokens for the two actions | Design-system component | Lint on the card spec |
| Consent saved only from a button press | Consent service | Log scan for other sources |

### T3. Evals
- **Dataset:** every consent prompt in the product, plus 20 generated variants with deliberate asymmetries (missing decline, smaller reject, extra step).
- **Judge rubric:** does the prompt show both answers on screen one, with equal style and taps, and plain opposite labels?
- **Metrics and starting thresholds:** prominence parity 100%; consent without a tap 0. Starting points to tune.
- **Release gate:** block a deploy if any prompt fails the parity lint.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Prompts failing parity | Any | Any in production | Roll back the card version |
| Consent without a tap | Any | Any | Find the code path that saves it |

### T5. Trade-offs
- Equal buttons may lower the accept rate; that is the point, and the number should be read as the honest rate.
- A parity lint catches size and style, not tone; keep a sampled human review.

---
### Deep dive
- **Open question.** I found no study of consent-card asymmetry in chat assistants. The evidence is regulation text and web cookie-banner cases.
- **Not verified.** I could not read the EDPB guideline text or the CNIL decision pages (fetch errors), so neither is used for any rule. A claim that these sources require equal prominence is unverified here.
- **Modality notes.** Voice: PLANNED (equal spoken weight for yes and no, and no pre-roll that only promotes yes). Visual banners on the web: PLANNED.
- **References.** [Cal. Code Regs. tit. 11, § 7004](https://law.cornell.edu/regulations/california/11-CCR-7004) (opened); [ZwillGen on the CPPA Honda order](https://www.zwillgen.com/privacy/cppa-settles-with-honda-over-alleged-privacy-violations/) (opened); [CyberScoop on the CNIL fines](https://cyberscoop.com/cnil-facebook-google-fine-cookies/) (opened); [EDPB Guidelines 03/2022 page](https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-032022-deceptive-design-patterns-social-media_en) (catalogue page only).
