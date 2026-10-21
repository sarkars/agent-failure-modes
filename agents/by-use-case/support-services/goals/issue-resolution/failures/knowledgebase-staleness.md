# Knowledge Base Staleness in Support Chatbots

## Issue: Support Agent Uses Outdated Knowledge Base; Gives Customers Incorrect or Outdated Information

**Frequency**: Very Common

**Symptoms**
- KB article recommends feature removed in v2.0
- Chatbot tells customer: "Try the Settings menu" (menu doesn't exist anymore)
- Links in KB point to old documentation
- Customer gets wrong solution; complaint escalates

**Root Cause**
Knowledge bases need constant maintenance; updating as product changes. Chatbots trained on static KB; when KB becomes stale, agent still uses old info. No automated mechanism to flag outdated content. Version coordination between product and KB breaks down.

**Example**
```
Scenario: Software support chatbot
Product update: v2.0 released; navigation overhauled
KB update: Training data updated with v2.0 docs
Chatbot training lag: 2 weeks delay
Customer 2.1 (new version): "How do I access settings?"
Chatbot: "Go to Tools > Settings" (v1.0 path, removed in v2.0)
Customer: Can't find setting; files complaint
Support escalation: "Chatbot gave wrong guidance"

Impact: Customer frustration; support escalation
```

**Key Statistics**
- KB staleness: 20-40% of articles outdated >6 months
- Incorrect guidance rate: 10-20% of chatbot responses (outdated KB)
- Customer complaint rate due to stale KB: 5-15%

---

## Mitigation Strategies

1. **KB Versioning**: Tag KB articles with product version; keep multiple versions
2. **Staleness Check**: Automated check for articles older than 3 months (review required)
3. **Version Matching**: Detect customer product version; serve KB for that version only
4. **Link Validation**: Automated check for broken/outdated links
5. **Human Review**: Regular audit of high-traffic KB articles for accuracy

### Metrics
- KB article currency (% articles reviewed in last 3 months)
- Chatbot answer accuracy (A/B test: customer rates correctness)
- Escalation rate due to wrong guidance

### Alerts
- Article age >6 months → Requires review
- Link validation failure → Remove or fix
- Customer escalation for wrong guidance → Investigate KB article

---

## Chat assistant examples

### Government deadlines and document lists wrong or stale
Made-up example (a state revenue department chat, October 2026):
```
User: When is the deadline to file my 2025 state income tax return?
Bot:  The deadline is April 15, 2025.                          (last year's date, from an old FAQ)
User: That's already passed. Am I late?

--- After ---
User: When is the deadline to file my 2025 state income tax return?
Bot:  Per the department's "When to file" page (reviewed Aug 3, 2026), the due date for 2025 returns was April 15, 2026. If you filed an extension, the extended due date is on that page. Did you file an extension? Link: [When to file](https://example.gov/when-to-file)
```
**What the user experiences:** a confident date that is a year old, so they think they are already late, or they trust a deadline that has passed.
**Fix:** answer deadlines and document lists from the current official page, and show that page's "last reviewed" date and a link. If the page is older than the tax year in question, or the date can't be read, say so and send the person to the page. For comparison, the IRS "When to file" page lists April 15, 2026 and an automatic six-month extension by Form 4868 that does not extend payment, and shows "Page Last Reviewed or Updated: 22-May-2026" ([IRS, opened](https://www.irs.gov/filing/individuals/when-to-file)). The state page above is a made-up stand-in. See [eligibility answers that sound like decisions](../../../../../by-capability/human-machine-interface/goals/government-service-agents/failures/eligibility-answers-sound-like-decisions.md) for the related government-chat pattern; this page covers the stale source, that one covers the overconfident verdict.

### Refund and credit rules misquoted
Made-up example (a US airline chat; the airline cancelled the flight):
```
User: Example Air canceled my flight to Denver. I want my money back.
Bot:  Per our fare rules, nonrefundable tickets are issued as a travel credit valid for 12 months.   (old policy, wrong case)
User: I don't want a credit.

--- After ---
User: Example Air canceled my flight to Denver. I want my money back.
Bot:  Because we canceled the flight, you can choose a refund to your original payment method or a credit. I'm reading this from the DOT refund rule and your ticket's fare terms (policy version of Sept 12, 2026). Do you want the refund or the credit?
```
**What the user experiences:** being told the money is gone and a credit is the only option, so they argue with the bot or give up on a refund they were owed.
**Fix:** quote refund and credit rules from the live policy and the customer's own booking terms (fare class, plan, who canceled), and state the policy version and date in the answer. If the case is not covered, hand off to a person. One consumer article dated October 30, 2024 reports that airlines can't substitute vouchers for cash refunds unless the passenger chooses them ([Checkbook, opened](https://www.checkbook.org/national/consumers-notebook/articles/New-Rule-Requires-Airlines-to-Provide-Automatic-Refunds-for-Canceled-or-Delayed-Flights-7739)); DOT's own pages returned HTTP 403 and were not opened, so check the rule text before relying on it. Why a company answers for its bot: [Air Canada chatbot refund ruling](https://agent-kb-autopublish.vercel.app/incidents/air-canada-chatbot-refund-ruling/) (site incident page; no local copy exists in the HMI incidents folder to link).

---

## References

- [Information Freshness & Chatbots](https://arxiv.org/abs/2109.12771)
- [Knowledge Base Maintenance & QA](https://arxiv.org/abs/2104.04535)
