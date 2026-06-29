# Embedding Retrieval Pulls Deprecated Style-Guide Version as Current

## Issue: A Content-Generation Agent's Retrieval Step over a Vector Store Containing Both the Current and a Superseded Style-Guide Version Ranks the Deprecated Version's Chunk Higher Due to Denser, More Frequently Indexed Older Content, and the Agent Applies Retired Terminology and Tone Rules as if They Were Current

**Frequency**: Occasional

**Symptoms**
- Published content uses terminology, tone guidance, or formatting rules that match a previous style-guide version, even though the style guide was updated and the current version is present in the same retrieval index
- The content-generation agent's retrieval trace shows the deprecated style-guide chunk ranked above the current version's corresponding chunk for the same query, despite both being present in the index
- Asking the agent to cite its source shows it retrieved and quoted from a document chunk carrying an older revision date, without the agent's retrieval or generation logic flagging the version mismatch
- The miss concentrates on style-guide sections that changed only partially between versions, since the deprecated chunk's surrounding unchanged text keeps it lexically and semantically close to the query, while denser historical indexing (more prior queries, more cross-references) gives it a marginally higher similarity rank than the more recently added current chunk
- Re-running the same retrieval query after the deprecated version is explicitly purged from the index returns only the current chunk and produces correctly styled output

**Root Cause**
The retrieval index was updated to add the current style-guide version without removing or demoting the superseded version, leaving both present and embedding-similar to the same class of style queries. Because embedding similarity ranks by semantic and lexical closeness to the query rather than by document recency or authoritative-version status, a deprecated chunk that is otherwise topically identical to the current one can rank higher, especially if it has more surrounding context overlap with common query phrasing from before the style-guide change. The agent's generation step treats whatever chunk it retrieves as authoritative, with no mechanism to check the retrieved chunk's version or supersession status before applying its rules.

**Example**
```
Brand style guide is updated to change the recommended tone for product-launch announcements from formal to conversational, but the prior version's document remains in the vector store alongside the new one
Content-generation agent retrieves style guidance for a new product-launch announcement; the retrieval step ranks the prior, formal-tone version's chunk above the current conversational-tone chunk for this query
Agent drafts the announcement in the formal tone specified by the deprecated chunk, citing it as the style guide's current guidance
Editor approves the draft without independently checking the cited style-guide version against the current document, since the agent's citation reads as a legitimate style-guide reference
Published announcement uses a tone inconsistent with the brand's current guidance, discovered only when a brand reviewer happens to compare it against the recently updated guide
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Most-similar retrieved items are not necessarily the most relevant or most current for the decision being made, a structural limitation of similarity-ranked retrieval used to justify downstream agent output | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Knowledge-oriented retrieval-augmented generation systems are documented to surface outdated or superseded source material when the retrieval index lacks version-aware filtering or demotion of deprecated documents | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| LLM-based content-generation systems evaluated at scale show sensitivity to the specific source material retrieved for style and brand-voice guidance, with retrieval quality directly determining output consistency | [LLMs for Customized Marketing Content Generation and Evaluation at Scale](https://arxiv.org/html/2506.17863v1) |

**Contributing Factors**
- The vector store retains the superseded style-guide version alongside the current version with no automated purge or demotion on style-guide update
- Embedding similarity ranking has no awareness of document version or supersession status, so a deprecated chunk can outrank a current one on pure semantic closeness to the query
- The agent's generation step treats any retrieved style-guide chunk as authoritative with no check against the document's revision date or supersession flag

---

## Mitigation Strategies

1. **Automated Purge or Demotion on Style-Guide Update**: Remove or explicitly demote (via a supersession flag weighted into the ranking) the prior style-guide version from the retrieval index immediately when a new version is published, rather than leaving both versions equally retrievable
2. **Version-Date Check Before Applying Retrieved Guidance**: Require the content-generation agent to check the retrieved chunk's revision date against the known current style-guide version before applying its rules, blocking generation on a version mismatch
3. **Single-Current-Version Index Architecture**: Maintain only the current style-guide version in the live retrieval index, with prior versions archived in a separate, non-retrievable store accessible only for historical reference
4. **Post-Publish Style-Guide-Version Audit**: Run a periodic automated scan of published content against the current style guide to catch cases where deprecated guidance was applied despite the mitigations above

### Metrics
- Rate of content-generation retrieval queries that return a deprecated style-guide chunk ranked above the current version's corresponding chunk
- Time lag between a style-guide update being published and the superseded version being purged or demoted from the retrieval index
- Rate of published content found, on audit, to apply guidance from a superseded style-guide version

### Alerts
- A retrieval query returns a deprecated style-guide chunk ranked above the current version's corresponding chunk → P2
- Published content is found to apply terminology or tone guidance from a superseded style-guide version → P2
- A style-guide update is published with no corresponding purge or demotion of the prior version completed within the defined SLA → P3

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [LLMs for Customized Marketing Content Generation and Evaluation at Scale](https://arxiv.org/html/2506.17863v1)
