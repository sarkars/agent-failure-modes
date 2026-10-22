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
