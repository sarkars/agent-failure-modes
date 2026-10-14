# Roadmap Tools: Rebuild the Index and Check Links

**Two small Python scripts keep the roadmap consistent.** Run both before committing roadmap changes.

| Script | What it does |
|---|---|
| [rebuild_summary.py](rebuild_summary.py) | Rebuilds the [index](../index.md), the count tables in the [roadmap README](../README.md), and the count in the area README from the catalog files |
| [check_links.py](check_links.py) | Checks internal links and anchors, that every catalog row has 9 columns, and that IDs are unique. Exits with an error if anything is wrong |

## Related

- [Roadmap](../)
- [Execution plan](../execution-plan.md)
