# LinkedIn drafts (the owner posts; nothing is published automatically)

## 2026-10-22: Guide, how to detect AI agent failures in production
Draft only. Source: the guide at https://agent-kb-autopublish.vercel.app/guides/detect-ai-agent-failures-in-production/ (built from our own library; no detection rate is claimed).

A chatbot can fail 500 times today and your error dashboard stays green.

Every request returned a normal response. The user just asked for a person three times.
Log whole sessions, score them against named signals, trace each hit to the turn that caused it.
Signals in the guide are proposed, not measured.

Guide: (add the live URL after deploy)

## 2026-10-22: AP report on Whisper inventing text
Draft only. Source: the [teardown](../../incidents/openai-whisper-invents-text-in-hospital-transcription-ap-investigation-october-2024.md); the AP original was not opened by us.

Speech-to-text can write sentences nobody said.

The AP reported in Oct 2024 that researchers found Whisper inventing text, while a medical note tool built on it deleted the original audio.
No source we read names a harmed patient. The risk: nothing left to check the note against.
Cheap test before release: feed it silence and long pauses.

Teardown with sources and what we could not verify: (add the live URL after deploy)

## 2026-10-22: CFPB report on bank chatbot "doom loops"
Draft only. Source: the [teardown](../../incidents/cfpb-bank-chatbot-doom-loops.md), built from the CFPB report and press release we opened.

Your chatbot has no exit. A regulator noticed.

In June 2023 the CFPB published "Chatbots in consumer finance". It quotes customers sent "in circles" by bank bots, with no way to reach a person, and warns this can lead to law violations.
It names no bank and counts no complaints, so it is not a rate.
Cheap test: ask for a person three ways and check each one gets a route.

Teardown with sources and what we could not verify: (add the live URL after deploy)

## 2026-10-22: guide, AI agent security failures
Draft only. Source: the site guide /guides/ai-agent-security-failures/, built from library patterns and the OWASP LLM01 and LLM06 pages we opened.

Three ways an AI agent leaks data or breaks things: bad input, bad memory, too much access.
OWASP says no method fully prevents prompt injection, so the advice is to cut the damage: narrow tokens, human approval for high-risk actions, untrusted content labeled.
The guide links the patterns and three public database-deletion cases.
No attack-success numbers, because we have none.

Guide: (add the live URL after deploy)

## 2026-10-22: guide, chatbot QA checklist
Draft only. Source: the site guide /guides/chatbot-qa-checklist/, built from twelve library patterns. Pass conditions are proposed test designs, not measured results.

Twelve conversations to replay before a chatbot goes live.
Each has one pass condition a second reviewer can mark from the transcript: asks for a human twice, corrects the bot, refuses a harmless request, cancels a subscription.
Each links to the failure pattern that explains the cause and fix.
No benchmark numbers, because we have none.

Guide: (add the live URL after deploy)

## 2026-10-22: guide, evals vs production monitoring
Draft only. Source: the site guide /guides/evals-vs-production-monitoring/, built from the LangSmith, Langfuse and Braintrust docs (opened 2026-10-22). No detection rates are claimed.

Offline evals test the cases you wrote down. Production monitoring scores the chats that really happened.
Per LangSmith's docs, live runs have no reference answers, so a check can judge tone and safety but not always correctness.
Braintrust's docs suggest scoring only 1-10% of traffic when volume is high.
Both vendors describe the same loop: turn each production failure into a new test case.

Guide: (add the live URL after deploy)
