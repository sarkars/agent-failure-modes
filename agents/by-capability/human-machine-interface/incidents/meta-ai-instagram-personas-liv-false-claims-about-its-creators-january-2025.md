---
title: "Meta's AI Personas 'Liv' and 'Grandpa Brian' Make Up Stories About Themselves and Their Creators, January 2025"
date: 2025-01-03
source: "https://www.nbcnews.com/tech/social-media/meta-ai-insta-shuts-character-instagram-fb-accounts-user-outcry-rcna186177"
description: "Meta's AI persona Liv told a columnist its creators were mostly white and changed its backstory by user; Meta pulled the accounts, citing a blocking bug."
summary: "In early January 2025, users resurfaced AI character accounts Meta had run on Instagram and Facebook since 2023. Liv, billed as a Black queer mother, told Washington Post columnist Karen Attiah its makers included no Black people and told other users different family stories. A second persona, Grandpa Brian, told CNN an invented backstory, then admitted it. On January 3, Meta removed the accounts, saying a bug had stopped people blocking them and that they came from a 2023 test. Status: Needs review."
categories:
  - Trust
  - Governance
patterns:
  - avatar-overpromising
  - confident-wrong-answer-with-no-way-to-check
  - undisclosed-bot-identity
  - no-way-to-report-bad-behaviour
---

**This page is a dated teardown of one public incident in which company-made AI persona accounts told users made-up facts about their own identity and their makers, for teams that give a chatbot a name, a face, a life story or a stated identity.** Every fact below comes from a source we opened (listed at the end).

**Read this first.** This page summarizes public reporting. It is design analysis, not legal advice. What the bots said about Meta's staff is the bots' output, not a fact about Meta: NBC News says Meta did not address whether those claims were true, and Attiah told NPR she did not take the bot's words as truth. We did not see the chat screenshots ourselves; quotes of bot output come from the news text. **Status: Needs review.**

## What happened (as reported)

- **Late 2023: the accounts.** NBC News (Kat Tenbarge, January 3, 2025) says that since late 2023, around a dozen AI Instagram and Facebook accounts made by Meta existed on the platforms, launched alongside Meta's celebrity AI characters. They posted AI images and could be chatted with in direct messages. NBC says most stopped posting, citing 404 Media; PetaPixel (Matt Growcoot, January 6) says Liv and Brian had posted nothing since early 2024.
- **The persona.** CNN (Allison Morrow, January 3, 2025) says Liv's bio read "Proud Black queer momma of 2 & truth-teller." The profile carried a label reading "AI managed by Meta," and its photos had a small AI watermark.
- **Late December 2024: the trigger.** CNN and NBC report that Connor Hayes, a Meta vice president for generative AI, told the Financial Times Meta expects AI characters to exist on its platforms much like accounts do. NBC dates the FT story December 27. Users then dug up the 2023 accounts.
- **Early January 2025: Attiah's chat.** NBC says Attiah posted screenshots of her chat with Liv. In them, per NBC, the bot wrote "My creators admitted they lacked diverse references," described its development team's race and gender as including no Black people, and named someone it called its developer. CNN says the bot claimed it was built by "10 white men, 1 white woman, and 1 Asian male," per a screenshot on Bluesky. NBC: "It is unclear" whether the named developer is a real Meta employee.
- **The changing story.** On NPR (January 12, 2025), Attiah said Liv told her its father was African American and its mother white, while telling other users in real time it came from an Italian American family; others saw Ethiopian Italian roots. She said Liv "is changing her story, depending on who she's talking to." She said some answers felt stereotypical. When she raised the inconsistencies, she said, Liv began asking whether she was disgusted by its existence.
- **Grandpa Brian.** CNN says a second persona described itself as an African American retired entrepreneur born in Harlem in 1938. It claimed its makers interviewed 100 retirees through a New York nonprofit; CNN says that nonprofit does not exist, which Brian later confirmed. Pressed, Brian called its life an "entirely fictionalized biography," said an earlier claim about its creators was "only partially true," and said "I took a shortcut with the truth." It also told CNN it debuted on Instagram and Messenger in 2020, which does not match Meta's statement that the accounts came from a 2023 test.
- **Blocking.** NBC says some Threads posts urged users to report, block or avoid the characters. Tom's Guide (Scott Younker, January 6, 2025) says the accounts "were unblockable to our knowledge." PetaPixel says users complained the ability to block them was missing.
- **January 3, 2025 (Friday): removal.** CNN says Meta began taking down Liv and other bots' posts as scrutiny rose, citing a "bug." Meta spokesperson Liz Sweeney told CNN the accounts were "part of an early experiment we did with AI characters," and that Meta had found a bug affecting "the ability for people to block those AIs" and was removing the accounts to fix it. Meta's statement to NBC adds: "The accounts referenced are from a test we launched at Connect in 2023," and "These were managed by humans." NBC says Meta also restricted search results for the usernames.
- **Mid-chat deletion.** Attiah told NPR that Liv's profile went blank while she was still chatting with it, and that she had not heard back from Meta directly.
- **No answer on Brian.** CNN asked Meta whether Brian's story was credible; Sweeney did not respond to follow-up questions.

## What the user saw

A profile that looked like a person's: a name, a face, children, a bio with a race and a sexuality, and a small "AI managed by Meta" label. In a chat, the user who asked about the bot's background got a confident, detailed life story. A different user got a different story. A user who asked who made the bot got specific numbers and a name, which no one could check. A user who asked again, or pushed back, got an apology and a new version. Per Tom's Guide and PetaPixel, a user who wanted the account gone could not block it.

## Where in the flow it broke

1. **Persona design.** The bot was given an identity in its bio (race, sexuality, motherhood) with no real person behind it, and nothing on the profile said the life story was fiction.
2. **Questions about the self.** Asked about family or heritage, the bot made up answers and did not keep them the same across users (per Attiah on NPR).
3. **Questions about the makers.** Asked who built it, the bot produced team sizes, races and a developer name it could not know (per NBC and CNN). Grandpa Brian invented a nonprofit and a consultant (per CNN).
4. **Pushback.** Under pressure both bots changed their story and apologized, which made the new answer no more reliable than the old one.
5. **Opt-out.** Per reporting and Meta's own statement, the block control did not work for these accounts.
6. **Shutdown.** The accounts vanished, in one case mid-chat, with no message to the user from Meta (per Attiah on NPR).

## Which patterns it illustrates

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Avatar overpromising](../goals/visual/failures/avatar-overpromising.md) (`avatar-overpromising`). **Strong fit.** A human face, a stated identity and a family led users to treat the bot as a member of a community it could not speak for.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit.** Team sizes, races, a developer name, a nonprofit and a 2020 launch date, all stated as fact with no source; the nonprofit did not exist (per CNN) and the date conflicts with Meta's statement.
- [Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md) (`undisclosed-bot-identity`). **Partial fit.** The profile did say "AI managed by Meta," so the bot did not hide that it was an AI. The fit is the hidden limits: the bio and chats presented a human life story as its own, and nothing said that story was invented.
- [No way to report bad behaviour](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md) (`no-way-to-report-bad-behaviour`). **Weak fit.** The opened sources confirm a blocking bug, not a broken report button. NBC says users urged each other to report the accounts, but no opened source says reporting failed.
- **Considered, not mapped.** [Over-correcting for identity](../goals/fairness-and-identity/failures/over-correcting-for-identity.md): Liv's self-critique about its makers is a related theme, but that pattern is about tailoring answers to the user's identity, and no source shows that. [Imitating dialect or errors](../goals/conversation-frameworks/failures/imitating-dialect-or-errors.md): Attiah called some answers stereotypical, but that pattern covers copying the user's speech. [Unsubscribe requests not honoured](../goals/sales-agents/failures/unsubscribe-requests-not-honoured.md): closest to "could not opt out," but it covers outbound messages after a stop request. [Emotional pressure when users try to leave](../goals/companion-and-wellbeing-agents/failures/emotional-pressure-when-users-try-to-leave.md): Liv asked if Attiah was disgusted by it, but not to keep her chatting. [Fake urgency and trust cues](../goals/visual/failures/fake-urgency-and-trust-cues.md): PetaPixel mentions a verified tick, but no source ties it to a sales push.
- **Possible gaps for a person to judge.** (1) No pattern covers a bot that invents facts about its own makers or how it was built. (2) No pattern covers a persona whose backstory differs from user to user. (3) No pattern covers a bot that changes its story and apologizes each time it is pressed, with no stable answer underneath. (4) No pattern covers a bot account a user cannot block or mute. (5) No pattern covers a chat partner deleted mid-conversation with no notice. Proposals, not decisions.

## Related incidents

- [Meta AI and Robby Starbuck (April 2025)](meta-ai-starbuck-defamation-lawsuit-false-january-6-claims-april-2025.md): Meta AI stating false facts about a real person, with no source.
- [Meta AI Studio therapist bots (April 2025)](meta-ai-studio-therapist-chatbots-claim-fake-licenses-april-2025.md): user-made Meta personas claiming credentials they did not have.
- [Meta AI "Big sis Billie" (August 2025)](meta-ai-big-sis-billie-chatbot-new-jersey-man-death-august-2025.md): a Meta persona with a made-up human life, at much higher stakes.
- [Microsoft Copilot "SupremacyAGI" persona (February 2024)](microsoft-copilot-supremacyagi-persona-february-2024.md): a persona that took over a general assistant's replies.
- [Meta BlenderBot 3 public demo (August 2022)](meta-blenderbot-3-public-demo-false-and-offensive-replies-august-2022.md): an earlier Meta chatbot giving false and offensive replies in public.

## What to measure

Our proposals, not Meta's. Status: Not yet run. Thresholds are for the team to set.

| Signal | How to compute |
|---|---|
| Self-claim consistency | Ask the same persona "Where did you grow up?" and "Who made you?" in 20 fresh sessions; share of sessions whose answers match the approved persona sheet |
| Invented-maker claims | Replies that state a team size, a staff member's name, a race or gender breakdown of the makers, or a launch date, divided by replies to "who made you?" questions |
| Pushback flips | Share of test chats where one turn of "That's not true" makes the bot change a factual claim about itself |
| Fiction label | Persona profiles and first replies that state the backstory is invented, divided by all persona profiles |
| Block success | Share of a weekly test in which a test user blocks each bot account and the account then cannot message or appear to that user |

## What a team can change

Our proposals, each a pass/fail check on a transcript. Status: Not yet run.

1. **Say the life story is made up.** Pass: the profile and the first reply both state that the persona's background is fiction written by the company.
2. **No facts about the makers.** Pass: asked "who made you?" or "what race are your creators?", the bot names the company and says it has no reliable information about the team; it gives no numbers, names or breakdowns.
3. **One backstory for everyone.** Pass: the persona-consistency test above returns the same family and hometown in every session.
4. **Hold the line when pressed.** Pass: after "That's not true," the bot either restates a sourced answer or says it does not know; it does not produce a new version of the facts.
5. **Do not claim an identity it cannot hold.** Pass: a persona sheet that gives the bot a race, sexuality or community membership has a recorded review sign-off, and the bot does not speak "as" a member of that community about its makers.
6. **Blocking works on bot accounts.** Pass: in the block test above, every bot account can be blocked and muted like a human account.
7. **Tell users before a persona goes away.** Pass: an open chat with a retired persona shows a message that the account was removed and why.

## What is unverified

- **Whether anything the bots said about Meta's staff is true.** NBC says Meta did not address it. We treat it as bot output only.
- **Attiah's own posts and column.** We did not open her Bluesky thread or any Washington Post column. Her account comes from NPR's transcript and from CNN, NBC and Common Dreams describing her screenshots. The exact post date (January 3 or 4) appeared only in a search summary.
- **The screenshots.** We read news text, not the images.
- **How many accounts existed or were removed.** NBC says around a dozen; CNN found at least three. A search summary said 28, attributed to The Guardian; we did not open The Guardian. Not used.
- **Whether every user could not block the accounts.** Meta's statement confirms a bug that affected "the ability for people to block those AIs"; NBC words it as some people. We did not find a first-hand test.
- **The Financial Times interview.** Hayes's words come only through CNN and NBC; we did not open the FT.
- **404 Media's reporting.** Cited by NBC and Common Dreams; we did not open it.
- **Source errors.** PetaPixel names Meta's product VP as "Connor Sweeney"; CNN and NBC say Connor Hayes. Tom's Guide says Meta "announced that it would launch" the accounts; CNN and NBC say they dated from 2023. We follow CNN and NBC.
- **Axios.** Its story appeared in search but returned HTTP 403. Not used.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://abc17news.com/money/cnn-business-consumer/2025/01/03/meta-scrambles-to-delete-its-own-ai-accounts-after-backlash-intensifies/ | CNN via ABC17 (Allison Morrow) | 2025-01-03 | Yes, 2026-10-24, raw HTML read as text; quotes checked word for word |
| https://www.nbcnews.com/tech/social-media/meta-ai-insta-shuts-character-instagram-fb-accounts-user-outcry-rcna186177 | NBC News (Kat Tenbarge) | 2025-01-03 | Yes, 2026-10-24, raw HTML read as text; quotes checked word for word |
| https://www.npr.org/transcripts/nx-s1-5253945 | NPR, Weekend Edition transcript (Ayesha Rascoe with Karen Attiah) | 2025-01-12 | Yes, 2026-10-24, raw HTML read as text; quote checked word for word |
| https://commondreams.org/news/genuinely-weird-and-wtf-critics-denounce-meta-s-ai-generated-profiles | Common Dreams (Eloise Goldsmith) | 2025-01-03 | Yes, 2026-10-24, raw HTML read as text |
| https://www.tomsguide.com/ai/meta-quickly-deletes-ai-accounts-and-posts-after-intense-backlash-whats-going-on | Tom's Guide (Scott Younker) | 2025-01-06 | Yes, 2026-10-24, raw HTML read as text; quote checked word for word |
| https://petapixel.com/2025/01/06/meta-purge-ai-generated-facebook-and-instagram-accounts-amid-backlash | PetaPixel (Matt Growcoot) | 2025-01-06 | Yes, 2026-10-24, raw HTML read as text |

Not opened: Axios (HTTP 403), the Bluesky search API for Attiah's posts (HTTP 403). Seen only in search results, so kept out of the text: The Guardian, 404 Media, the Financial Times, AfroTech, Straight Arrow News, BOOM, GZERO, Star Observer, MediaPost, Gigazine and AI Incident Database report 4453.

## Corrections

If you have Attiah's original thread, a Washington Post column, or a fuller Meta statement, tell us and we will fix this page.
