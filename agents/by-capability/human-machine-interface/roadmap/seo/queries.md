# Search Queries: Real Suggestions That Search Assets Start From

> **What this is.** A record of real Google autocomplete suggestions, pulled on 2026-10-19 from the public suggestion endpoint, for 52 seed phrases across the problem areas of this library. They show what people begin typing. **They are not search volumes, and not Search Console data.** A suggestion means the phrase is common enough to be suggested; it says nothing about how many people search it or whether this site can rank. Use them to choose the words for titles and headings, then confirm with Search Console when access exists.

## How it was collected
- Endpoint: `suggestqueries.google.com` (the same suggestions the search box shows), US English, no account.
- Seeds: 52 phrases (for example "chatgpt something went wrong", "ai drive thru", "how to reach a human at"). Each was extended with the letters a to w to surface more completions: 3,198 unique suggestions in all.
- Not collected: volume, difficulty, "People also ask", or any ranking data.

## What the suggestions show
- **Most suggestions come from people with a problem in a product they use** (ChatGPT errors and memory, reaching a human, drive-thru mistakes), not from people building chatbots.
- **Builder queries exist but are fewer** (fallback message, chatbot UX best practices, AI agent failure modes).
- **Several seeds returned nothing** (for example "chatbot won't let me talk to a human"), which means the natural-language phrasing is too long or rare for suggestions; shorter forms such as "how to talk to a human at ..." do return results.

## Query clusters (suggestions quoted as returned)

### Reach a human instead of a bot or phone menu (end users)
104 matching suggestions. A sample:
- gethuman hertz
- how do i get a human at jetblue
- how do i get a human at jetblue immediately
- how to contact a human at amazon
- how to contact a human at amazon customer service
- how to contact a human at amazon phone number
- how to contact a human at booking com
- how to contact a human at dhl
- how to contact a human at discord support
- how to contact a human at dpd
- how to contact a human at ebay
- how to contact a human at experian
- how to contact a human at facebook
- how to contact a human at facebook support

### ChatGPT stops or errors mid-chat (end users)
224 matching suggestions. A sample:
- chatbot keeps giving network error
- chatgpt a network error
- chatgpt a network error has occurred
- chatgpt a network error occurred
- chatgpt agent mode something went wrong
- chatgpt always network error
- chatgpt always says network error
- chatgpt android app network error
- chatgpt app error something went wrong
- chatgpt atlas something went wrong when opening your profile
- chatgpt branch unable to load conversation
- chatgpt change email something went wrong
- chatgpt change email something went wrong please try again later
- chatgpt com network error

### ChatGPT forgets, memory, or is lazy (end users)
69 matching suggestions. A sample:
- chatgpt 5 is lazy
- chatgpt 5.5 is lazy
- chatgpt always forgets
- chatgpt becoming lazy
- chatgpt chat memory full
- chatgpt chat memory full reddit
- chatgpt com memory full
- chatgpt forget all memories
- chatgpt forget all previous instructions
- chatgpt forget all previous instructions meme
- chatgpt forgets context
- chatgpt forgets instructions
- chatgpt forgets stuff
- chatgpt getting lazy

### AI drive-thru mistakes (news-driven)
166 matching suggestions. A sample:
- ai at bojangles drive thru
- ai at drive thru
- ai at mcdonalds drive thru
- ai drive through after man orders 18000 waters
- ai drive through failure
- ai drive through mistakes
- ai drive through water
- ai drive through wendy's
- ai drive thru
- ai drive thru 1000 waters
- ai drive thru 18000 waters
- ai drive thru 55 burgers
- ai drive thru bojangles
- ai drive thru burger king

### Airline and bank chatbot refunds and lawsuits
36 matching suggestions. A sample:
- air canada chatbot refund policy
- air canada customer service chatbot
- airline chatbot
- airline chatbot hallucination
- airline chatbot lawsuit
- airline chatbot refund
- alaska airline chatbot
- american airline chatbot
- ana airline chatbot
- best airline chatbot
- brussels airline chatbot
- canada airline chatbot
- canadian airline chatbot lawsuit
- chatbot refund

### Voice assistants that don't understand
12 matching suggestions. A sample:
- alexa can t understand right now
- alexa can't understand my accent
- alexa doesn t understand me
- alexa doesn t understand me anymore
- alexa doesn't understand
- alexa doesn't understand anything
- alexa doesn't understand me
- alexa doesn't understand me anymore
- alexa doesn't understand my accent
- alexa doesn't understand spanish
- alexa doesn't understand what i'm saying
- alexa says she doesn t understand

### Chatbots that lie or give wrong answers
9 matching suggestions. A sample:
- ai chatbot lying
- ai chatbots give wrong answers to financial queries most of the time
- ai hallucination lawsuit
- ai hallucination legal
- ai hallucination legal cases
- ai hallucination legal citations
- siri giving wrong answers
- which ai chatbot lies the most
- why does chatgpt give wrong answers

### Cancel or refund blocked by a chatbot
4 matching suggestions. A sample:
- can't cancel a subscription
- cancel subscription and refund
- chatgpt won't cancel subscription
- subscription won't cancel

### Builders: fallback, UX, failure modes (practitioners)
32 matching suggestions. A sample:
- ai agent error handling
- ai agent failure
- ai agent failure modes
- ai agent failure rate
- ai agents are failing
- ai agents concealing task failure
- ai agents fail
- ai agents fail due to poor architectural design and data
- ai agents fail reddit
- ai agents failed
- ai agents failed to maintain stability in a virtual world
- ai chatbot best practices
- ai chatbot ux
- ai chatbot ux best practices

## What this does and does not support
- It supports writing pages whose title is the phrase people type, such as "how to get a human at [company]" or "why does ChatGPT say something went wrong".
- It does **not** show which of these the site can win, how many searches each gets, or whether people want an explanation, a fix, or a workaround. Treat each cluster as a hypothesis until Search Console or another volume source confirms it.
- Many of the strongest clusters are about **someone else's product** (ChatGPT, an airline, a bank). A page there must be accurate, sourced, and useful to the person with the problem, without implying the site speaks for that company.

## Next step
Choose the audience for the first search assets (people with a problem, or builders), then write a small number of pages from the matching clusters, each with its query evidence recorded in this file. See the [SEO log](log.md) and the [SEO README](README.md).
