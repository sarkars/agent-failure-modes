---
title: "OpenAI Acknowledges Reports of GPT-4 Turbo Refusing Tasks and Giving Half-Completed Answers"
date: 2024-01-25
source: "https://www.ciodive.com/news/openai-laziness-gpt4-turbo-model-updates/705664/"
summary: "After users reported that GPT-4 Turbo refused tasks or returned half-completed responses, OpenAI acknowledged the complaints in December 2023 and on January 25, 2024 released an updated preview model it said completes tasks more thoroughly and is intended to reduce cases of laziness, per CIO Dive."
categories:
  - Accuracy
patterns:
  - lazy-completion
  - deferring-work-to-the-user
---

CIO Dive reported on January 25, 2024 that OpenAI released an updated GPT-4 Turbo preview model that, in OpenAI's words, "completes tasks like code generation more thoroughly than the previous preview model and is intended to reduce cases of 'laziness' where the model doesn't complete a task." The article says users had reported that the model refused tasks or generated half-completed responses, and that OpenAI acknowledged the complaints in December 2023 and said teams were investigating. The source does not give a root cause.

Semafor and Gigazine, both of which I opened, relay a December 8, 2023 post from OpenAI's ChatGPT account on X: "we've heard all your feedback about GPT4 getting lazier! we haven't updated the model since Nov 11th, and this certainly isn't intentional. model behavior can be unpredictable, and we're looking into fixing it." A "winter break hypothesis" that the model gave shorter answers when told it was December came from one developer's API test, and one researcher who tried to reproduce it (at N=240) could not find a significant difference; the hypothesis is not established.

A user report from December 7, 2023 on the OpenAI developer forum describes a related case: a developer said the model declined a code refactoring request, citing a platform limit, and returned examples of what a refactor might look like instead of doing it. That is one user's account and was not confirmed by OpenAI in the sources I opened.

**Pattern match:** [Lazy completion](/lazy-completion/) covers an assistant that does part of a job and leaves the rest, and the reports above (half-completed responses, refusals) match it for a general-purpose model. [Deferring work to the user](/deferring-work-to-the-user/) covers handing a task back when the assistant could do it; the sources describe refusals and incomplete answers in coding tasks, not a customer-service bot telling someone to look something up, so that match is adjacent.

**The fix:** do the part the assistant can do, say plainly what it did not do and why, and ask only for what the user must supply.
