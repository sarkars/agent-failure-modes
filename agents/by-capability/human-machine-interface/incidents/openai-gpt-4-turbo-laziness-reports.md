---
title: "OpenAI Acknowledges Reports of GPT-4 Turbo Refusing Tasks and Giving Half-Completed Answers"
date: 2024-01-25
source: "https://www.ciodive.com/news/openai-laziness-gpt4-turbo-model-updates/705664/"
summary: "After users reported that GPT-4 Turbo refused tasks or returned half-completed responses, OpenAI acknowledged the complaints in December 2023 and on January 25, 2024 released an updated preview model it said completes tasks more thoroughly and is intended to reduce cases of laziness, per CIO Dive."
categories:
  - Accuracy
patterns:
  - deferring-work-to-the-user
---

CIO Dive reported on January 25, 2024 that OpenAI released an updated GPT-4 Turbo preview model that, in OpenAI's words, "completes tasks like code generation more thoroughly than the previous preview model and is intended to reduce cases of 'laziness' where the model doesn't complete a task." The article says users had reported that the model refused tasks or generated half-completed responses, and that OpenAI acknowledged the complaints in December 2023 and said teams were investigating. The source does not give a root cause.

A user report from December 7, 2023 on the OpenAI developer forum describes a related case: a developer said the model declined a code refactoring request, citing a platform limit, and returned examples of what a refactor might look like instead of doing it. That is one user's account and was not confirmed by OpenAI in the sources I opened.

**Pattern match:** [Deferring work to the user](/deferring-work-to-the-user/) covers an assistant that hands a task back when it could do it. The sources describe refusals and incomplete answers from a model in coding tasks, not a customer-service bot telling someone to look something up, so this is an adjacent case, not a direct match.

**The fix:** do the part the assistant can do, say plainly what it did not do and why, and ask only for what the user must supply.
