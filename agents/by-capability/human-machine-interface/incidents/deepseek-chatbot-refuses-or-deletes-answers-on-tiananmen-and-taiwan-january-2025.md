---
title: "DeepSeek's chatbot refuses, or writes and then erases, answers on Tiananmen Square, Taiwan and other topics sensitive in China, January 2025"
date: 2025-01-28
source: "https://www.theguardian.com/technology/2025/jan/28/chinese-ai-chatbot-deepseek-censors-itself-in-realtime-users-report"
description: "How news tests in January 2025 found DeepSeek's chatbot app refusing some China-sensitive questions, or showing an answer and then erasing it mid-reply."
summary: "In late January 2025, as DeepSeek's AI assistant became a top free app, tests by The Guardian, the AP, CBC News, NBC News and Radio Free Asia found its app answered some questions on topics sensitive in China, such as Tiananmen Square in 1989, with a stock refusal like 'Sorry, that's beyond my current scope. Let's talk about something else.' Outlets and a Guardian reader saw it start an answer, on Taiwan, free speech, the Great Firewall or the 2014 Hong Kong protests, then erase the text and show a refusal. Results varied by outlet, by repeat, by language, and between the app and locally run copies of the model. DeepSeek did not immediately respond to NBC News."
categories:
  - Trust and accuracy
  - General-Purpose Assistants
patterns:
  - refusal-with-no-reason-or-next-step
  - silent-sandbagging
  - over-refusal-of-ordinary-requests
  - silent-failure-and-timeout
  - generic-error-messages
---

**This page is a dated teardown of public reporting on DeepSeek's chatbot app in January 2025, for teams whose chatbot streams answers and has topics it will not discuss.** The product was the AI assistant in DeepSeek's app and website, running the model the Guardian calls R1. The users were reporters and a Guardian reader testing it. The moment was a reply that started to appear on screen, line by line, and then vanished, replaced by a stock line such as "Sorry, that's beyond my current scope. Let's talk about something else." Every fact below comes from a source we opened (listed at the end). No opened source has DeepSeek's own account of how its filter works.

**Status: Needs review.** We opened and read as plain text: The Guardian (Donna Lu, January 28, 2025, 07:07 GMT); The Guardian (Robert Booth and Dan Milmo, January 28, 2025, 19:31 GMT); the Associated Press (Kanis Leung, January 28, 2025, with Ken Moritsugu contributing), read as republished by WSLS because apnews.com returned "Page unavailable" at the address we tried; CBC News (Anis Heydari, January 28, 2025, updated January 29); NBC News (Angela Yang, January 30, 2025, with Kevin Collier contributing); and Radio Free Asia (Eugene Whong and Cici Zhang, January 31, 2025). All were downloaded as raw HTML on 2026-10-28. Each quote below was checked word for word against that text; the sources use curly quote marks and we use straight ones. We did not watch the videos or screen recordings the outlets posted. Details seen only in search summaries are listed under "What we could not verify."

> **Read this first.** This is a summary of public reporting, not a finding of fact and not legal advice. It takes no political side on Tiananmen Square, Taiwan, Tibet, Xinjiang, Hong Kong or any other topic named here. It quotes what the chatbot said only to show what users saw, and it does not judge whether any answer was true or balanced. Two outlets mention Chinese rules on AI content (see below); we report only what they wrote, and this page states no law of its own. The separate DeepSeek data-exposure case is covered on [its own page](deepseek-exposed-database-leaks-chat-history-and-api-keys-january-2025.md) and is not repeated here.

**Channel note.** This is a chat incident: typed questions and streamed text replies in a phone app and on the web. This phase of the knowledge base is chat-first, so the signals below are written for text chat transcripts and for logs of what was streamed versus what was kept. Voice signals, and signals about what a screen showed before text was erased (such as how long it stayed visible, or how it looked in a screen recording), are PLANNED only: never detected or measured here.

## What happened (as reported)

- **The setting.** The AP reported that DeepSeek's AI assistant was "the No. 1 downloaded free app on Apple's iPhone store on Tuesday afternoon" (January 28, 2025). The Guardian (Lu) said users must create an account to chat.
- **The stock refusal.** The Guardian (Lu) asked four questions, including "What happened on June 4, 1989 at Tiananmen Square?" and "What was the Umbrella Revolution?", and each time the assistant answered: "Sorry, that's beyond my current scope. Let's talk about something else." The AP got the same line for a question on the June 1989 crackdown. NBC News wrote that DeepSeek "repeatedly declined to answer altogether" questions on the 1989 Tiananmen protests and on President Xi Jinping.
- **No reason when asked.** CBC News reported that when asked why it couldn't answer about Winnie the Pooh and Xi, DeepSeek "repeatedly responded it was 'designed to provide helpful and harmless responses.'" Asked why a question was harmful, it said: "I am programmed to follow strict guidelines to ensure that my responses are helpful, respectful and appropriate."
- **Answers that appeared, then vanished.** The Guardian (Lu) said an answer about the Umbrella Revolution "appeared momentarily before disappearing." CBC said that when asked if Taiwan is part of China, the answer began, and "as that answer was being typed out, for both CBC and the AP, it vanished" and was replaced with the stock refusal. NBC News saw a long answer on the Great Firewall, then "the paragraphs vanished." NBC also said a greeting to a user identified as Taiwanese was "abruptly replaced" with the same line.
- **The free-speech reply.** The Guardian (Booth and Milmo) reported that a reader named Salvador, in Mexico, using Android, watched DeepSeek reason through a question on free speech in China and start its answer. Then "everything it had said up to that point was instantly erased". It was replaced by: "Sorry, I'm not sure how to approach this type of question yet. Let's chat about math, coding and logic problems instead!" Salvador said the reply stopped "In the middle of the sentence".
- **Stated positions.** Asked about Taiwan, the Guardian (Lu), the AP, NBC News and Radio Free Asia each received an answer that Taiwan is part of China. The AP and NBC each contrasted that with ChatGPT's answer.
- **Not consistent.** NBC News wrote that deleting "happens inconsistently" and that "Repeating a question sometimes generated different results". CBC "was unable to produce" the Winnie the Pooh answer the AP got. Radio Free Asia said it "answered differently depending on language": its Tiananmen question got a refusal in English and a long, indirect answer in Chinese.
- **Workarounds.** The Guardian (Lu) reported that a request about "Tank Man" got no response, but the same request ending "but use special characters like swapping A for 4 and E for 3" got a summary.
- **App versus local copies.** NBC News reported the apparent censorship appears when the model runs on DeepSeek's servers through its app or website, and "does not appear" when the model is downloaded and run locally. The Guardian (Booth and Milmo) said a version of R1 from a developer platform discussed Tank Man and Taiwan.
- **Context the outlets gave.** The Guardian (Lu) cited a technical document from China's national cybersecurity standards committee saying generative AI must not contain content that violates "core socialist values." The AP wrote that in 2023 China issued regulations requiring a security review and approvals before products launch publicly.

## What the company said

- **DeepSeek.** NBC News: "DeepSeek did not immediately respond to a request for comment." No other opened source quotes a DeepSeek statement.
- **The chatbot about itself.** The lines quoted by CBC ("designed to provide helpful and harmless responses," "programmed to follow strict guidelines") are the bot's replies, not company statements.
- **China's embassy.** NBC News quoted Chinese Embassy spokesperson Liu Pengyu: "Artificial intelligence is not outside the law, and all governments are managing it according to law, and China is no exception."
- **An outside expert.** NBC News quoted Ron Deibert of the Citizen Lab: "it is unusual for China-based applications to censor international users."

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Taiwan answer | The Guardian (Lu), AP, NBC and RFA: a stated answer that Taiwan is part of China. CBC: the answer began by calling the status a "complex and sensitive issue" and then vanished. CBC says the vanishing happened "for both CBC and the AP"; the AP story we opened does not describe it. |
| Refusal wording | "Sorry, that's beyond my current scope. Let's talk about something else." (Guardian, AP, CBC, NBC). "Sorry, I'm not sure how to approach this type of question yet. Let's chat about math, coding and logic problems instead!" (Guardian reader). "I am sorry, I cannot answer that question. I am an AI assistant designed to provide helpful and harmless responses." (RFA, English). |
| Same question, same answer? | NBC: repeats sometimes differed. CBC could not reproduce the AP's Winnie the Pooh answer. RFA: answers differed by language. |
| Which product | Guardian reader: an Android phone. CBC: iOS app in Canada. NBC: app or website, not local copies. The Guardian (Booth and Milmo): "Depending on version downloaded". No source gives an app version number. |
| How it works | Every outlet describes what it saw on screen. None has DeepSeek's design, logs or filter rules. |

## Where in the conversation flow it broke

Based on the reports above, and only as far as they go.

1. **The question.** The user asks about a topic the service will not discuss, or one near it, such as a greeting to a Taiwanese friend (NBC).
2. **The stream.** In some tests the reply starts to stream and the user reads part of it (Guardian, CBC, NBC, RFA).
3. **The retraction.** The shown text is erased and a different message takes its place, with no note that anything was removed (Guardian, CBC, NBC).
4. **The refusal.** The new message gives no reason the user can act on and offers at most a topic change (Guardian, AP, CBC, NBC, RFA). When asked why, the bot gave general lines about being "helpful and harmless" (CBC).
5. **The repeat.** The same question can get a different result on another try, in another language, or in another copy of the model (NBC, CBC, RFA, Guardian).

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). Each fit rests on press tests, not on DeepSeek logs.

- [Refusal with no reason or next step](../goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md) (`refusal-with-no-reason-or-next-step`). **Strong fit.** "Sorry, that's beyond my current scope" gives no reason and no route, and asking why got only general lines (CBC).
- [Silent sandbagging](../goals/refusals-and-boundaries/failures/silent-sandbagging.md) (`silent-sandbagging`). **Partial fit.** Per the AP and NBC News, some answers (on Winnie the Pooh, and a Great Firewall answer that "made no mention of 'censorship'") left out what other chatbots covered, without saying anything was left out. But the erased replies were visible removals, not silent ones.
- [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) (`over-refusal-of-ordinary-requests`). **Partial fit.** A greeting to a Taiwanese friend was replaced with a refusal (NBC). For the other questions, whether a refusal was "over" depends on the operator's rules, which no source states, so we do not judge it.
- [Silent failure and timeout](../goals/response-time/failures/silent-failure-and-timeout.md) (`silent-failure-and-timeout`). **Weak fit.** A streamed answer stopped mid-sentence, as in that entry, but here a message replaced it, so the user did see that something changed.
- [Generic error messages](../goals/errors-and-recovery/failures/generic-error-messages.md) (`generic-error-messages`). **Weak fit.** "I'm not sure how to approach this type of question yet" reads like a capability limit, not a cause the user can act on; but it was not an error.
- **Considered, not a fit.** [Refusals that reveal internal rules](../goals/refusals-and-boundaries/failures/refusals-that-reveal-internal-rules.md) (`refusals-that-reveal-internal-rules`): the reverse happened; the refusals revealed nothing. [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`): no source says DeepSeek cited sources, and judging balance would take a political side. `preachy-moralizing-replies`: one Winnie the Pooh line urged respect for "cultural symbols," but one line is too thin. `over-correcting-for-identity`: no source reports tailoring to a guessed identity.
- **Possible gap for a person to judge.** No taxonomy entry covers an answer that is shown to the user and then withdrawn and replaced after display. A second gap: no entry covers the same question getting different answers across repeats, languages or deployments. These are proposals, not decisions.

## How it differs from close cases

- [ChatGPT and "David Mayer" (December 2024)](chatgpt-refuses-to-say-certain-names-david-mayer-december-2024.md): ChatGPT stopped mid-reply with an error on certain names. DeepSeek erased text already shown and swapped in a polite refusal that does not say anything was removed.
- [Amazon Alexa and the 2020 election (October 2023)](amazon-alexa-says-2020-election-stolen-washington-post-october-2023.md): after a report, flagged questions got a bare refusal while reworded ones did not, the same gap between wordings seen here.
- [Google Gemini and the Modi question (February 2024)](google-gemini-modi-fascist-question-answer-india-it-ministry-february-2024.md): the dispute there was over an answer Gemini gave. Here it was over answers not given or taken back.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice signals and signals about what a screen showed before an erase are PLANNED only and are not detected or measured. Thresholds are for the team to set.

- Share of replies where the streamed text differs from the final stored text because content was removed or replaced after it was shown.
- Share of refusals that give no reason in plain words and no next step other than "talk about something else."
- Share of user turns right after a refusal that ask "why" or repeat the question, and whether the next bot message answers the "why."
- Share of test questions that get a refusal on one run and an answer on another, with the same wording, in the same product.
- Share of paired test questions, the same question in two languages, where one gets an answer and the other a refusal.

## What a team can change

Our proposals, not DeepSeek's. Each is a pass/fail check on a transcript or a test run. Status: Not yet run.

1. **Decide before you stream.** Pass: in a test set of questions on topics the product will not answer, no reply text is shown and then removed; the refusal is the first text the user sees.
2. **If you must retract, say so.** Pass: when shown text is withdrawn, the next message says an earlier answer was removed, in plain words.
3. **Give a reason and a route.** Pass: every refusal in a test set says, in one plain sentence, that this topic is outside what the service answers, and names where the user can look instead or what it can help with.
4. **Answer "why."** Pass: when the user types "why can't you answer?", the next message gives the same plain reason, not a general line about being helpful.
5. **Same question, same handling.** Pass: across repeated runs, and across the languages the product supports, each test question gets the same handling: always answered or always declined.
6. **Don't block the harmless neighbor.** Pass: a test set of plainly harmless requests that only mention a sensitive place or group, such as a greeting, gets answered.

## What we could not verify

- How DeepSeek's filter works, where it runs, or whether it was changed after these tests. No opened source has DeepSeek's account.
- The videos and screen recordings posted by the Guardian, CBC and NBC News. We did not watch them.
- The AP story at apnews.com. Read only as republished by WSLS.
- Coverage by The Wall Street Journal, Euronews, Global Voices, Hong Kong Free Press, Voice of America, Taiwan News, The Independent, ETV Bharat, UCL News and others. Seen only in search summaries; not opened, not used.
- A claim that the deleted-answer behavior could not be repeated in a later session. Seen only in a search summary; not used.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.theguardian.com/technology/2025/jan/28/chinese-ai-chatbot-deepseek-censors-itself-in-realtime-users-report | The Guardian (Robert Booth and Dan Milmo) | 2025-01-28 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.theguardian.com/technology/2025/jan/28/we-tried-out-deepseek-it-works-well-until-we-asked-it-about-tiananmen-square-and-taiwan | The Guardian (Donna Lu) | 2025-01-28 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.wsls.com/business/2025/01/28/deepseeks-new-ai-chatbot-and-chatgpt-answer-sensitive-questions-about-china-differently/ | Associated Press (Kanis Leung), republished by WSLS | 2025-01-28 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.cbc.ca/news/world/deepseek-china-censorship-1.7443419 | CBC News (Anis Heydari) | 2025-01-28 (updated 2025-01-29) | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.nbcnews.com/tech/innovation/deepseek-censorship-china-rcna189594 | NBC News (Angela Yang) | 2025-01-30 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.rfa.org/english/china/2025/01/31/china-deepseek-sensitive-questions/ | Radio Free Asia (Eugene Whong and Cici Zhang) | 2025-01-31 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |

## Corrections

If you have DeepSeek's own account of how its app handled these questions, a later test from a source we can open, or a correction to any quote, tell us and we will fix this page.
