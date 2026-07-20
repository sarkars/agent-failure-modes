# Fact Source Confusion

## Issue
An agent retrieves facts about two distinct entities — companies, people, products, or regulations — that share a similar name, and conflates attributes from one with the other in its response. The resulting statement is internally coherent and often partially correct, but attributes a fact that belongs to Entity A to Entity B, because retrieval matched on name similarity rather than correctly disambiguating which entity the query actually concerns.

**Frequency**: Occasional

**Symptoms**
- Agent response attributes a fact, statistic, or event to the wrong one of two similarly-named entities
- The confused entities share a name, an abbreviation, or a former/subsidiary relationship
- Errors increase when the query itself doesn't include disambiguating detail (full legal name, jurisdiction, founding year)
- Corrections from users or experts specifically identify "that's not us, you're thinking of [other entity]"

## Root Cause
Retrieval systems match on semantic and lexical similarity, and two entities sharing a name (a common name reused across unrelated companies, a parent/subsidiary pair, a person sharing a name with someone more prominent) produce nearly identical embeddings or keyword matches for queries that don't include disambiguating context. Without an entity-resolution layer that maintains distinct, uniquely-keyed records for each entity and forces explicit disambiguation when a name match is ambiguous, the retrieval system treats "closest name match" as sufficient identification, and the generation step then merges facts from whichever record(s) were retrieved without any mechanism to detect that they describe two different things.

## Example
```
A user asks a business-research agent: "What's Acme Corp's revenue and
who is their CEO?" There are two unrelated companies both operating
under variants of "Acme Corp" — a publicly traded industrial
manufacturer, and a small private software startup — indexed in the
agent's knowledge base under near-identical names.

The agent retrieves the industrial manufacturer's revenue figure (a
large, well-documented public company financial) but the software
startup's CEO name (which appeared as a more recent, higher-relevance
match to the query's phrasing), producing a response that pairs a real
revenue figure with the wrong company's leadership, attributed to a
single "Acme Corp" as though it were one entity.

A user relying on this for a business decision (e.g. vetting a
counterparty) receives a materially wrong picture of the company they
are actually engaging with, since neither company's true profile
matches the merged description.
```

## Statistics
| Finding | Context |
|---------|---------|
| Entity-name collision affects an estimated 5-15% of queries about organizations/individuals in knowledge bases without dedicated entity-resolution/disambiguation | Estimated from entity-resolution audits of business/research knowledge bases |
| Queries lacking disambiguating detail (jurisdiction, founding year, ticker symbol) show a markedly higher source-confusion rate than queries including it | Typical pattern observed in retrieval-QA evaluation involving named entities |
| Forced disambiguation prompts (asking the user to confirm which entity when a name match is ambiguous) eliminate most source-confusion errors in tested systems, at the cost of an extra interaction turn | Reported range across teams that added disambiguation gating |

## Mitigations
1. **Entity-resolution layer with unique keys**: Maintain distinct, uniquely-keyed records for each entity (using stable identifiers like registration numbers, tickers, or DOIs rather than name strings alone), and require retrieval to resolve to a specific key rather than matching on name text.
2. **Ambiguity detection and forced clarification**: When a query's name reference matches multiple distinct entity records above a similarity threshold, have the agent explicitly ask the user to disambiguate rather than silently picking or merging records.
3. **Single-entity provenance enforcement**: Require every fact included in a response about a named entity to be traceable to a single resolved entity key, and reject/flag responses that merge facts sourced from two different entity keys under one name.
4. **Disambiguating-detail prompting**: When a name is known to be ambiguous in the knowledge base (tracked via a collision registry), proactively prompt for or surface disambiguating detail (jurisdiction, industry, founding year) before answering.
5. **Cross-entity consistency audit**: Periodically audit responses about entities known to have name collisions for internal consistency (e.g. does the cited CEO actually match records for the company whose revenue was cited), flagging mismatches for review.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| entity_resolution_confidence | Confidence score that retrieved facts resolve to a single, correctly-identified entity key | Alert if < 90% for queries matching a known name-collision entry |
| known_collision_disambiguation_rate | Rate at which queries matching a registered name-collision trigger a clarification prompt | Alert if < 95% |
| source_confusion_correction_rate | Rate of expert/user corrections identifying a cross-entity attribution error | Track trend; alert on sustained increase |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Cross-entity fact merge confirmed | Review confirms a response merged facts from two distinct entities under one name | High | Correct the response, add entity pair to the name-collision registry |
| Disambiguation gate bypassed | A query matching a registered name collision produced a direct answer without a clarification prompt | Medium | Audit disambiguation-gating logic for the affected entity pair |

## Related Patterns
- [Fact Inversion](./fact-inversion.md) - can produce a similarly-shaped symptom (attributes swapped) via a different mechanism, flipped polarity rather than conflated entities
- [Knowledge Scope Assumption Wrong](./knowledge-scope-assumption-wrong.md) - both involve applying a fact to the wrong scope, one for entity identity and one for jurisdiction/version
- [Knowledge Source Reliability Unknown](./knowledge-source-reliability-unknown.md) - related in that both stem from insufficient provenance tracking on retrieved facts
