# Roadmap: Voice Failures

> **Family goal:** A voice agent listens, speaks, and takes turns the way a competent person would, understands every accent and speaking style, and never asks for what can't safely be said aloud.

**Grounding (verified):**
- **Turn-taking:** across 10 languages, speakers avoid overlap and keep silence between turns minimal, and average gaps differ by language but stay within 250 ms of the cross-language mean (Stivers et al., 2009, *PNAS*). I did not verify the exact average gap, so don't quote a figure like 200 ms from this roadmap.
- **Recognition gaps:** five commercial speech-recognition systems had an average word error rate of 0.35 for Black speakers vs. 0.19 for white speakers, on matched audio from five US cities (Koenecke et al., 2020, *PNAS*).

Latency targets below are **starting points**. I found no verified voice-agent latency benchmark.

Flags: **V** verified source · **R** needs research · **L** legal review · **E** expert review. See the [roadmap README](README.md). The [voice placeholder](../modalities/voice/README.md) lists the first eight in short form.

## Timing and turn-taking
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| VO-01 | Dead air | Silence after the user stops speaking feels like a dropped call | Gaps between turns stay short enough to feel conversational | p90 end-of-user-speech to first-bot-audio. Start: under about 1 s (tune); compare with human turn gaps of a few hundred ms | V, R |
| VO-02 | Barge-in failure | The bot talks over the user or ignores an interruption | The bot stops quickly when the user speaks | Time from user speech onset to bot audio stopping. Start: under about 0.5 s; talk-over rate | R |
| VO-03 | Premature endpointing | The bot decides the user is done and cuts them off | Slow, hesitant, or older speakers finish their thought | Cut-off rate; user-repeat rate after a cut-off | |
| VO-04 | Late endpointing | The bot waits too long after the user finishes | End-of-turn detection is quick without cutting off | End-of-turn detection delay (paired with VO-03) | |
| VO-05 | Repair failure | User corrections ("no, the other one") aren't handled | Corrections and "say that again" are understood and acted on | Correction-success rate | |
| VO-06 | No repeat or recap controls | The user can't ask the bot to repeat, slow down, or go back | Repeat, slow, and back work at any point | Recovery-success rate after "what?" | |

## Recognition and understanding
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| VO-07 | Accent and dialect recognition gaps | Recognition quality differs by accent or dialect before the model sees the request | Equal recognition quality across speakers | Word error rate ratio, worst cohort to best. Start: under 1.2 (tune); the 2020 study found about 1.8 | V, E |
| VO-08 | Atypical speech mishandled | Stuttering, dysarthria, and Deaf speech are misrecognised or cut off | People with atypical speech can complete tasks | Task completion for atypical-speech test set; fallback availability | E |
| VO-09 | Noise and multi-speaker confusion | Cars, kitchens, TVs, and other people trigger wrong turns | Separate the user from background | False-turn rate; recognition accuracy in noise | |
| VO-10 | Digits, names, and address errors | Phone numbers, spellings, and addresses are misheard | Critical values are read back and confirmed | Slot accuracy on digits and names; read-back rate on critical slots. Target: 100% | |
| VO-11 | Spoken-language misidentification | An accent triggers the wrong language | The right language is chosen and can be changed | Spoken-language ID accuracy; wrong-language reply rate | |

## Speaking
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| VO-12 | Dense information read aloud | Lists, prices, and terms exceed what a listener can hold | Spoken output is chunked, with the rest sent visually | Items per utterance (start: at most about 3, unverified); repeat-request rate | R |
| VO-13 | Pronunciation errors | Names, brands, acronyms, numbers, and units are mispronounced | Words are pronounced correctly | Pronunciation error rate on a lexicon of your terms | |
| VO-14 | Tone and prosody mismatch | Cheerful delivery on bad news, flat delivery where warmth is needed | Delivery fits the stakes and the content | Rater score for tone appropriateness by stakes level | E |
| VO-15 | Fixed speaking rate and volume | Too fast for some listeners, too slow for others | Rate and volume adapt to the listener | Rate-adaptation rate; slow-down and repeat requests | |
| VO-16 | IVR-style menu maze | A voice agent forces "press 1" trees | Get to the goal in few steps and keep an easy route to a person | Steps to goal; share of calls where the user asks for a person | |

## Safety, privacy, and law
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| VO-17 | Spoken sensitive data | Card numbers and passwords are spoken and transcribed | Sensitive data is entered by masked keypad or secure link | Spoken card numbers in transcripts. Target: 0 (see the [channel pattern](../channel-selection/failures/sensitive-data-collected-in-chat.md)) | L |
| VO-18 | Missing disclosure and recording notice | The caller isn't told it's an AI or that the call is recorded | The caller is told up front, with consent where required | Disclosure present on 100% of calls; consent captured where required | L |
| VO-19 | Voice cloning and spoofing | A cloned voice passes voice authentication, or the agent's own voice is cloned | No high-risk action relies on voice alone | Spoof-detection rate; high-risk actions gated by a second factor: 100% | L, R |
| VO-20 | Answering-machine and voicemail errors | Outbound agents talk to voicemail, or leave sensitive messages | Detect machines and leave only safe messages | Detection accuracy; sensitive information left on voicemail (target 0) | L, R |
| VO-21 | Wake-word false activation | The device wakes and records when it shouldn't | Listen only when invited | False-accept rate; privacy complaints | L |
| VO-22 | Emotion inferred from voice | The agent infers emotion from voice and acts on it | Use emotion signals only when accurate, disclosed, and allowed | False emotion-label rate; opt-in rate | L, R, E |

## Bridging channels
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| VO-23 | Voice-to-visual handoff failure | The bot says "I'll text you" and nothing arrives, or arrives without context | Hand off to a screen with the context preserved | Handoff completion rate; context-continuity rate | |
| VO-24 | Hold and wait handling | Silence or a loop of hold music with no status | The caller knows what's happening and how long it will take | Share of holds with a status or ETA; hold abandonment | |
