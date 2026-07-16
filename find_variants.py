#!/usr/bin/env python3
"""
Find semantic variants of known consolidation candidates.
"""

import re
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

def similarity(s1, s2):
    if not s1 or not s2:
        return 0
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

def extract_issue_root(content):
    """Extract Issue and Root Cause from content."""
    issue_match = re.search(r'## Issue:?\s*\n(.*?)(?:\n\n|\n##|\Z)', content, re.DOTALL)
    issue = issue_match.group(1).strip() if issue_match else ""

    root_match = re.search(r'## (?:Root Cause|Root Cause Theory):?\s*\n(.*?)(?:\n\n|\n##|\Z)', content, re.IGNORECASE | re.DOTALL)
    root = root_match.group(1).strip() if root_match else ""

    return issue[:500], root[:500]

def main():
    # Find canonical patterns
    canonical_files = {
        'stale-training-knowledge': 'agent-defaults-to-stale-training-knowledge-over-live-lookup-tool.md',
        'self-verification-upstream': 'self-verification-cannot-catch-upstream-errors.md',
        'context-loss': 'long-session-context-loss-violates-earlier-constraints.md',
        'hallucinated-completion': 'hallucinated-completion-when-upstream-dependency-fails.md',
        'semantic-retrieval': 'semantic-similarity-retrieval-misses-structural-attributes.md',
        'handoff-schema': 'handoff-schema-loses-upstream-confidence-signal.md',
    }

    # Load canonicals
    canonicals = {}
    for name, filename in canonical_files.items():
        # Find the file
        matches = list(Path('./agents').glob(f'**/failures/{filename}'))
        if matches:
            filepath = matches[0]
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            issue, root = extract_issue_root(content)
            if issue and root:
                canonicals[name] = {
                    'filepath': str(filepath),
                    'filename': filename,
                    'issue': issue,
                    'root': root,
                    'variants': []
                }
                print(f"Loaded canonical: {name}")

    print(f"\nFound {len(canonicals)} canonical patterns\n")

    # Find all patterns and compare
    all_patterns = list(Path('./agents').glob('**/failures/*.md'))
    print(f"Scanning {len(all_patterns)} patterns for variants...\n")

    for filepath in all_patterns:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        issue, root = extract_issue_root(content)
        if not issue or not root:
            continue

        filename = filepath.name
        filepath_str = str(filepath)

        # Skip canonicals
        if filename in canonical_files.values():
            continue

        # Check against each canonical
        for canonical_name, canonical_data in canonicals.items():
            issue_sim = similarity(issue, canonical_data['issue'])
            root_sim = similarity(root, canonical_data['root'])

            avg_sim = (issue_sim + root_sim) / 2

            # Lower threshold for better detection
            if avg_sim > 0.40:
                canonical_data['variants'].append({
                    'filepath': filepath_str,
                    'filename': filename,
                    'issue_sim': issue_sim,
                    'root_sim': root_sim,
                    'score': avg_sim,
                })

    # Sort and print results
    print("Variant Analysis Results:\n")
    total_variants = 0

    for name, data in sorted(canonicals.items(), key=lambda x: -len(x[1]['variants'])):
        data['variants'].sort(key=lambda x: x['score'], reverse=True)
        count = len(data['variants'])
        total_variants += count
        print(f"{name}: {count} variants")

    print(f"\nTotal variants found: {total_variants}")

    # Generate report
    lines = []
    lines.append("# Semantic Variant Consolidation Report\n\n")
    lines.append("## Executive Summary\n\n")
    lines.append(f"- **Canonical Patterns Analyzed**: {len(canonicals)}\n")
    lines.append(f"- **Total Variants Found**: {total_variants}\n")
    lines.append(f"- **Average Variants Per Canonical**: {total_variants/len(canonicals):.1f}\n")
    lines.append(f"- **Estimated Consolidation Potential**: {max(0, total_variants-30)} patterns can be merged\n\n")

    for name, data in sorted(canonicals.items(), key=lambda x: -len(x[1]['variants'])):
        lines.append(f"## {name.replace('-', ' ').title()}\n\n")
        lines.append(f"**Canonical**: `{data['filepath']}`\n\n")
        lines.append(f"**Variants Found**: {len(data['variants'])}\n\n")

        if data['variants']:
            lines.append("**Top 25 Variants** (sorted by similarity):\n\n")
            for i, v in enumerate(data['variants'][:25], 1):
                lines.append(f"{i}. `{v['filepath']}`\n")
                lines.append(f"   - Similarity: {v['score']:.3f} (issue: {v['issue_sim']:.2f}, root: {v['root_sim']:.2f})\n")

            if len(data['variants']) > 25:
                lines.append(f"\n... and {len(data['variants']) - 25} more variants\n")

        lines.append("\n")

    with open('SEMANTIC_VARIANT_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(''.join(lines))

    print("\nReport saved to SEMANTIC_VARIANT_REPORT.md")

if __name__ == '__main__':
    main()
