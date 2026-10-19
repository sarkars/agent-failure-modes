---
title: "Virgin Money Chatbot Scolds Customer for Typing the Bank's Own Name"
date: 2025-01-30
source: "https://fortune.com/europe/2025/01/30/virgin-money-chatbot-scolds-customer-confuse-banks-name-insult"
summary: "A Virgin Money chatbot told a customer asking how to merge two ISAs not to use 'words like that' after he typed the bank's name; the bank apologized, removed the chatbot, and said it was an older model already scheduled for improvements, per Fortune."
categories:
  - Customer Service
patterns:
  - over-refusal-of-ordinary-requests
  - refusal-with-no-reason-or-next-step
---

Fortune reported on January 30, 2025 that fintech commentator David Birch posted on LinkedIn a screenshot of a chat in which he asked a Virgin Money chatbot whether he could merge his two Virgin Money ISA accounts. The chatbot replied: "Please don't use words like that. I won't be able to continue with our chat if you use this language," apparently referring to the word "virgin". Virgin Money's account apologized in a comment on the post and said "there's more at work than just single word exception", confirmed that he could merge the accounts, and a representative told Fortune the chatbot was promptly removed and improvements were coming. A person familiar with the matter told Fortune the error came from an older model using basic natural language processing, not the bank's newer chatbot. CX Today reported the same exchange.

**Pattern match:** [Over-refusal of ordinary requests](/over-refusal-of-ordinary-requests/) describes an assistant that declines a safe request because it looks like a risky one. This case involved an older, basic filter rather than a modern language model, and the bank says it was more than a single-word block, so it shows the user-facing failure and not any particular cause.

[Refusal with no reason or next step](/refusal-with-no-reason-or-next-step/) also matches: the reply said the chat would end if the language continued, and offered no way to complete the request.

**The fix:** check refusals against ordinary, on-topic requests before launch (including the company's own name), and give the user a way forward when a refusal fires.
