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

## References

- [Information Freshness & Chatbots](https://arxiv.org/abs/2109.12771)
- [Knowledge Base Maintenance & QA](https://arxiv.org/abs/2104.04535)
