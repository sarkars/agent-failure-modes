# Corporate Hierarchy Misattribution

## Issue: Agent Attributes Risk, Exposure, or Performance Data to the Wrong Entity Within a Corporate Family Due to Incomplete Parent-Subsidiary Mapping

**Frequency**: Common

**Symptoms**
- Credit risk or exposure aggregation treats a subsidiary as an independent counterparty, missing concentration risk that should be aggregated at the ultimate parent level
- A subsidiary's financial distress signal is not propagated to the risk assessment of sibling subsidiaries or the parent, even when cross-default or guarantee provisions link them
- Ticker/entity resolution incorrectly merges or splits financial data between a parent and subsidiary that share similar names, attributing performance or news to the wrong entity in the hierarchy
- Recently completed mergers, spin-offs, or restructurings are not reflected in the hierarchy mapping promptly, causing exposure calculations to use a stale corporate structure

**Root Cause**
Corporate hierarchies are dynamic — entities merge, spin off, get acquired, and restructure — and accurately mapping exposure or risk to "the right entity" requires maintaining a current, complete parent-subsidiary-affiliate graph rather than treating each named counterparty as independent. Agents that resolve counterparties by name or ticker alone, without maintaining and continuously updating this hierarchy graph, will misattribute risk whenever the named entity is part of a larger structure whose relationships are not reflected in the data the agent is using.

**Example**
```
Scenario: Bank holds credit exposure to three separate subsidiaries of the same parent conglomerate, each booked as an independent counterparty
Risk aggregation: Computes single-name concentration limits per subsidiary, treating each as unrelated
Actual risk: All three subsidiaries are linked by parent guarantees and would likely default together in a parent-level distress scenario
True aggregated exposure: Exceeds the single-counterparty concentration limit when correctly rolled up to the parent
Risk system: Reports each subsidiary's exposure as within limits because the parent-level aggregation was never computed
Impact: Concentration risk is understated; a parent-level distress event would produce correlated losses across all three "independent" exposures simultaneously
```

**Key Statistics**
- Failure to aggregate exposure at the ultimate parent/beneficial-owner level (rather than at the immediate legal-entity level) is a recurring supervisory finding in credit risk management reviews
- Entity resolution errors involving similarly-named parent/subsidiary pairs are a documented data quality issue in financial reference data management
- Large-scale corporate restructuring events (M&A, spin-offs) create a documented lag window during which legacy hierarchy data remains in active use before being corrected, during which misattribution risk is elevated

---

## Mitigation Strategies

1. **Maintained Parent-Subsidiary Graph**: Maintain a continuously updated corporate hierarchy graph (ultimate parent, intermediate holding entities, subsidiaries, guarantee relationships) as a first-class data input to risk aggregation, not derived ad hoc from entity names
2. **Parent-Level Exposure Roll-Up**: Compute concentration and exposure limits at the ultimate parent level by default, with legal-entity-level figures reported as a supplementary breakdown, not the primary risk view
3. **Restructuring Event Monitoring**: Monitor for corporate restructuring events (M&A announcements, spin-offs, name changes) affecting held counterparties and prioritize hierarchy graph updates for affected entities
4. **Entity Resolution Disambiguation**: Use a unique, persistent entity identifier (not name/ticker matching alone) for all exposure and risk data to prevent misattribution between similarly-named related entities

### Metrics
- % of counterparty exposure correctly aggregated to ultimate parent level vs. legal-entity level only
- Hierarchy graph staleness (time since last verified update) for held counterparties, especially following a known restructuring event
- Entity resolution error rate detected in periodic reconciliation audits

### Alerts
- Aggregated parent-level exposure exceeds concentration limit while legal-entity-level exposures individually appear within limits → P1
- Known restructuring event affecting a held counterparty with no corresponding hierarchy graph update within a defined window → P2

---

## References

- [FinVault: Benchmarking Financial Agent Safety in Execution-Grounded Environments](https://arxiv.org/pdf/2601.07853)
- [Position: Standard Benchmarks Fail – LLM Agents Present Overlooked Risks](https://www.arxiv.org/pdf/2502.15865v1)
