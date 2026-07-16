#!/usr/bin/env python3
"""
Detect semantic variants of known consolidation candidates.
Looks for patterns with similar issue descriptions and root causes.
"""

import re
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

def similarity(s1, s2):
    if not s1 or not s2:
        return 0
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

def extract_issue_root(filepath):
    """Extract Issue and Root Cause from pattern."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return None, None

    issue_match = re.search(r'## Issue:?\s*\n(.*?)(?:\n\n|\n##|\Z)', content, re.DOTALL)
    issue = issue_match.group(1).strip() if issue_match else ""

    root_match = re.search(r'## (?:Root Cause|Root Cause Theory):?\s*\n(.*?)(?:\n\n|\n##|\Z)', content, re.IGNORECASE | re.DOTALL)
    root = root_match.group(1).strip() if root_match else ""

    return issue[:300], root[:300]

# Known consolidation candidates
CANDIDATES = {
    'stale-training-knowledge': 'cross-cutting/accuracy/goals/knowledge-staleness/failures/agent-defaults-to-stale-training-knowledge-over-live-lookup-tool.md',
    'self-verification-upstream': 'cross-cutting/accuracy/goals/output-verification/failures/self-verification-cannot-catch-upstream-errors.md',
    'context-loss': 'cross-cutting/accuracy/goals/context-management/failures/long-session-context-loss-violates-earlier-constraints.md',
    'hallucinated-completion': 'cross-cutting/accuracy/goals/output-accuracy/failures/hallucinated-completion-when-upstream-dependency-fails.md',
    'semantic-retrieval': 'by-capability/knowledge-retrieval/goals/retrieval-relevance/failures/semantic-similarity-retrieval-misses-structural-attributes.md',
    'handoff-schema': 'by-capability/multi-agent-systems/goals/handoff-reliability/failures/handoff-schema-loses-upstream-confidence-signal.md',
}

def find_variants():
    """Find all variants of known candidates."""
    # Load canonical patterns
    canonicals = {}
    for name, rel_path in CANDIDATES.items():
        # Try different path separators
        full_path = Path('./agents') / rel_path.replace('/', '\\').replace('\\', '/')
        # Normalize path for current OS
        for part in rel_path.split('/'):
            if full_path == Path('./agents'):
                full_path = full_path / part
            else:
                full_path = full_path / part if part != full_path.name else full_path

        # Build path correctly
        full_path = Path('./agents') / rel_path.split('/')[-4] / rel_path.split('/')[-3] / rel_path.split('/')[-2] / rel_path.split('/')[-1]
        full_path = Path('./agents')
        for part in rel_path.split('/'):
            full_path = full_path / part

        if full_path.exists():
            issue, root = extract_issue_root(str(full_path))
            if issue and root:
                canonicals[name] = {
                    'path': str(full_path),
                    'issue': issue,
                    'root': root,
                    'variants': []
                }
        else:
            print(f"WARNING: Not found: {full_path}")

    print(f"Loaded {len(canonicals)} canonical patterns\n")

    # Scan all patterns for variants
    all_patterns = list(Path('./agents').glob('**/failures/*.md'))
    print(f"Scanning {len(all_patterns)} patterns for variants...\n")

    for filepath in all_patterns:
        issue, root = extract_issue_root(str(filepath))
        if not issue or not root:
            continue

        filename = filepath.name
        filepath_str = str(filepath).replace('\\', '/')

        # Skip the canonical itself
        if filepath_str in [c['path'].replace('\\', '/') for c in canonicals.values()]:
            continue

        # Check similarity to each canonical
        for canonical_name, canonical_data in canonicals.items():
            issue_sim = similarity(issue, canonical_data['issue'])
            root_sim = similarity(root, canonical_data['root'])

            # If either similarity is high, it's likely a variant
            if issue_sim > 0.50 or root_sim > 0.50:
                canonical_data['variants'].append({
                    'path': filepath_str,
                    'filename': filename,
                    'issue_sim': issue_sim,
                    'root_sim': root_sim,
                    'combined_score': (issue_sim + root_sim) / 2,
                })

    # Sort variants by combined score
    for name in canonicals:
        canonicals[name]['variants'].sort(key=lambda x: x['combined_score'], reverse=True)

    return canonicals

def generate_variant_report(canonicals):
    """Generate detailed variant report."""
    lines = []

    lines.append("# Semantic Variant Detection Report\n")
    lines.append("\n## Summary\n\n")

    total_variants = sum(len(c['variants']) for c in canonicals.values())
    lines.append(f"- **Total Canonical Patterns**: {len(canonicals)}\n")
    lines.append(f"- **Total Variants Found**: {total_variants}\n")
    lines.append("\n")

    # By canonical
    for name, data in sorted(canonicals.items(), key=lambda x: -len(x[1]['variants'])):
        lines.append(f"## {name.replace('-', ' ').title()}\n\n")
        lines.append(f"**Canonical Pattern**: `{data['path']}`\n\n")
        lines.append(f"**Variants Found**: {len(data['variants'])}\n\n")

        if data['variants']:
            lines.append("| Filename | Path | Issue Sim | Root Sim | Combined |\n")
            lines.append("|----------|------|-----------|----------|----------|\n")

            for v in data['variants'][:20]:  # Top 20
                score = f"{v['combined_score']:.2f}"
                issue_score = f"{v['issue_sim']:.2f}"
                root_score = f"{v['root_sim']:.2f}"
                lines.append(f"| {v['filename']} | `{v['path']}` | {issue_score} | {root_score} | {score} |\n")

            if len(data['variants']) > 20:
                lines.append(f"\n... and {len(data['variants']) - 20} more variants\n")

        lines.append("\n")

    # Consolidation strategy
    lines.append("## Consolidation Strategy\n\n")
    lines.append("### Recommended Actions\n\n")

    for name, data in sorted(canonicals.items(), key=lambda x: -len(x[1]['variants'])):
        if data['variants']:
            lines.append(f"### {name.replace('-', ' ').title()}\n\n")
            lines.append(f"- **Canonical**: `{data['path']}`\n")
            lines.append(f"- **Variant Count**: {len(data['variants'])}\n")
            lines.append(f"- **Action**: Create master pattern, consolidate variants into single canonical with cross-references\n")
            lines.append(f"- **Recommended Deletions**: Keep canonical + ~3 highest-value domain-specific variants\n")
            lines.append(f"- **Estimated Reduction**: ~{max(0, len(data['variants'])-3)} patterns for this candidate\n\n")

    return ''.join(lines)

def main():
    canonicals = find_variants()

    # Print summary
    print("Variant Analysis Results:\n")
    for name, data in sorted(canonicals.items(), key=lambda x: -len(x[1]['variants'])):
        print(f"{name}: {len(data['variants'])} variants")

    total_variants = sum(len(c['variants']) for c in canonicals.values())
    print(f"\nTotal variants found: {total_variants}")

    # Generate report
    report = generate_variant_report(canonicals)
    with open('VARIANT_CONSOLIDATION_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nVariant report saved to VARIANT_CONSOLIDATION_REPORT.md")

if __name__ == '__main__':
    main()
