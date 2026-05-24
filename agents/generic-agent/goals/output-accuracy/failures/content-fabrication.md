# Content Fabrication

## Issue: AI Generates False Content Presented as Fact

**Frequency**: Very Common

**Symptoms**
- AI-generated articles contain factual errors
- Legal citations refer to non-existent cases
- AI content plagiarizes existing sources
- Generated "interviews" with people who weren't interviewed
- Fake events or quotes presented as real

**Root Cause**
AI generates content that appears authoritative but contains fabrications, errors, or plagiarized material. Unlike hallucination in responses (which users can verify), content fabrication in published material reaches audiences who assume it's been fact-checked.

**Example**
```
Case 1: CNET AI Articles (2023)

What happened:
- CNET used AI to write 77 financial explainer articles
- Published without adequate human review
- Over half (41 articles) required corrections

Errors found:
- Simple math errors in interest rate calculations
- Misunderstanding of basic financial concepts
- Plagiarized passages from other websites
- "Phrases not entirely original" in several articles

Result: Program paused, editor-in-chief left

---

Case 2: Lawyer ChatGPT Citations (2023)

What happened:
- Attorney Steven Schwartz used ChatGPT for legal research
- ChatGPT fabricated 6 court case citations
- Citations included fake quotes and detailed summaries
- Submitted in federal court brief

Result: $5,000 fine for "bad faith" and false statements
        Similar incidents followed (MyPillow case: 30 fake cases,
        Minnesota AG: AI-generated fabrications in court)
```

**Key Statistics**
From Digital Defynd AI Disasters Analysis (2026):
- CNET: 41 of 77 AI articles needed corrections (53%)
- Legal hallucinations: At least 3 major court cases with fake citations
- Google Bard: Single factual error cost $100B in market cap
- Die Aktuelle: Fired editor for AI "interview" with incapacitated celebrity

**Fabrication Types**
- **Factual errors**: Incorrect statistics, dates, or facts
- **Citation hallucination**: References to non-existent sources
- **Plagiarism**: Copying existing content without attribution
- **Fake interviews**: Generated quotes from real people
- **Event fabrication**: Made-up events presented as real (Dublin parade)
- **Historical inaccuracy**: Wrong historical claims (Google AI Overview)

**Contributing Factors**
- AI optimizes for plausibility, not truth
- No built-in fact-checking mechanism
- Human reviewers trust AI output
- Pressure to publish quickly
- AI presents fabrications confidently
- Difficult to distinguish real from generated

**Mitigation Strategies**
1. **Mandatory fact-checking**: All AI content verified before publication
2. **Citation verification**: Check all references exist
3. **Plagiarism detection**: Run AI content through plagiarism checkers
4. **Human review requirements**: Expert review for domain content
5. **Disclosure**: Label AI-generated content clearly
6. **Confidence thresholds**: Don't publish when AI is uncertain

**Detection**
- Fact-checking reveals errors
- Sources/citations don't exist when checked
- Plagiarism detection tools flag copied content
- Subject-matter experts identify inaccuracies
- Legal/regulatory scrutiny

## References

- [Digital Defynd: Top 40 AI Disasters](https://digitaldefynd.com/IQ/top-ai-disasters/) - CNET (#16), Lawyer citations (#25-27), Die Aktuelle (#17)
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Legal citation fabrication
- [Air Canada Chatbot Lawsuit](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416) - Fabricated policy information
