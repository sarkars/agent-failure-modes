# Index Staleness

## Issue: Retrieved Documents Are Outdated

**Frequency**: Common

**Symptoms**
- Answers based on superseded information
- Old policies/procedures cited
- Deprecated features described as current
- Version numbers or dates incorrect

**Root Cause**
Index not updated when source documents change. Old versions remain indexed alongside or instead of current versions.

**Example**
```
Current policy (updated last week): 
"Remote work requires manager approval"

Indexed version (6 months old):
"Employees may work remotely 2 days per week without approval"

User query: "Can I work from home?"
Retrieved: Old policy

Agent: "You can work remotely 2 days per week without approval"

Result: Employee violates current policy
```

**Mitigation Strategies**
1. **Incremental indexing**: Update index when sources change
2. **Document versioning**: Track versions, prefer latest
3. **Freshness scoring**: Boost recent documents in ranking
4. **TTL on embeddings**: Expire and re-index periodically
5. **Change detection**: Monitor sources for updates
6. **Timestamp filtering**: Allow queries to specify timeframe

**Detection**
- Track document age in retrievals
- Monitor update frequency vs. query accuracy
- Alert on high-traffic stale documents
- Compare retrieved docs to current source versions
